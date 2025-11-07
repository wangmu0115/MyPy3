from enum import IntEnum
from typing import Callable, Iterator, Optional, Type, Union

from _interpreter import Lexer, Token, TokenType
from _interpreter.ast import (
    BinaryOpExpression,
    BlockStatement,
    BoolLiteralExpression,
    Expression,
    ExprStatement,
    IdenExpression,
    IfExpression,
    IntLiteralExpression,
    LetStatement,
    Program,
    ReturnStatement,
    Statement,
    UnaryOpExpression,
)


class TokenError(Exception): ...


class TokenTypeError(Exception): ...


class TokenLiteralError(Exception): ...


class TokenParseFuncMissError(Exception): ...  # token 无解析函数


class Precedence(IntEnum):  # 语言优先级
    DEFAULT = 1
    EQUALS = 2  # ==, !=
    LEGE = 3  # <, <=, >, >=
    ADDSUB = 4  # +, -
    MULDIV = 5  # *, /
    UNARY = 6  # !, -
    CALLABLE = 7  # fn(x)


def _token_precedence(tk: Union[Token | TokenType]) -> Precedence:  # 运算符对应的优先级
    token_type = tk.type if isinstance(tk, Token) else tk
    match token_type:
        case TokenType.EQ | TokenType.NEQ:
            return Precedence.EQUALS
        case TokenType.LT | TokenType.LE | TokenType.GT | TokenType.GE:
            return Precedence.LEGE
        case TokenType.ADD | TokenType.SUB:
            return Precedence.ADDSUB
        case TokenType.MUL | TokenType.DIV:
            return Precedence.MULDIV
        case TokenType.NOT | TokenType.SUB:
            return Precedence.UNARY
        case TokenType.FUNCTION:
            return Precedence.CALLABLE
        case _:
            return Precedence.DEFAULT


def parse_trace(parse_phase):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            trace: Trace = getattr(self, "trace")
            debug: bool = getattr(self, "debug", False)
            trace.begin(parse_phase) if debug else ...
            result = func(self, *args, **kwargs)
            trace.end(parse_phase, result) if debug else ...
            return result

        return wrapper

    return decorator


class Trace:
    def __init__(self):
        self.level = 0
        self.placeholder = " "

    def begin(self, phase: str, *args):
        print(f"{self.placeholder * self.level}>>> {phase}", *args)
        self.level += 4

    def end(self, phase: str, *args):
        self.level -= 4
        print(f"{self.placeholder * self.level}<<< {phase}:", *args)


class Parser:
    """语法解析器"""

    def __init__(self, lexer: Lexer):
        self.__lexer = lexer
        self.curr_token = None
        self.peek_token = None
        self.trace = Trace()
        self.debug = False

    def parse(self, debug: bool = False) -> Program:
        self.debug = debug
        self.trace = Trace()
        # 初始化 token 迭代
        it = self.__prepare_parse()
        program = Program()

        while self.curr_token is not None and self.curr_token.type != TokenType.EOF:
            stmt = self._parse_statement(it)
            if stmt is not None:
                program.append(stmt)
            self.__next_token(it)  # 将 curr_token 指向下一条语句的开头
        return program

    def _parse_statement(self, it: Iterator[Token]) -> Type[Statement]:  # 解析语句
        match self.curr_token.type:
            case TokenType.LET:
                return self.__parse_let_statement(it)
            case TokenType.RETURN:
                return self.__parse_return_statement(it)
            case TokenType.LBRACE:
                return self.__parse_block_statement(it)
            case _:
                return self.__parse_expr_statement(it)

    @parse_trace("Expression")
    def _parse_expression(self, it: Iterator[Token], precedence: Precedence = Precedence.DEFAULT) -> Type[Expression]:  # 解析表达式
        left_parse_func = self.__nuds_parse_func(self.curr_token)  # 中缀表达式 左侧
        if left_parse_func is None:
            raise TokenParseFuncMissError(f"`{self.curr_token}` expression parsing function does not exist.")
        left_expr = left_parse_func(it)

        while self.peek_token is not None and self.peek_token.type != TokenType.SEMICOLON and precedence < _token_precedence(self.peek_token):
            infix_parse_func = self.__leds_parse_func(self.peek_token)
            if infix_parse_func is None:
                return left_expr
            self.__next_token(it)  # 将 curr_token 移动到二元运算符处
            left_expr = infix_parse_func(left_expr, it)
        return left_expr

    @parse_trace("Let-Statement")
    def __parse_let_statement(self, it: Iterator[Token]) -> LetStatement:  # let <标识符> = <表达式>;
        if self.peek_token is None or self.peek_token.type != TokenType.IDENTIFIER:
            raise TokenError("The `identifier` for let statement does not exist.")
        self.__next_token(it)
        iden = self.curr_token.literal  # 标识符
        if self.peek_token is None or self.peek_token.type != TokenType.ASSIGN:
            raise TokenError("The assign operator(`=`) for let statment doest not exist.")
        self.__next_token(it)
        self.__next_token(it)  # 跳过 `=`
        if self.curr_token is None or self.curr_token.type == TokenType.SEMICOLON:
            raise TokenError("The assignment `expression` for the let statement does not exist.")
        expr = self._parse_expression(it)
        self.__next_token(it)  # 将 curr_token 移动到语句的结尾处 `;`
        if self.curr_token is None or self.curr_token.type != TokenType.SEMICOLON:
            raise TokenError("Let statements must end with a semicolon(`;`)")

        return LetStatement(iden, expr)

    @parse_trace("Return-Statement")
    def __parse_return_statement(self, it: Iterator[Token]) -> ReturnStatement:  # return <表达式>;
        self.__next_token(it)  # 将 curr_token 移动到表达式开头处
        if self.curr_token is None or self.curr_token.type == TokenType.SEMICOLON:
            raise TokenError("The value `expression` for the return statement does not exist.")
        expr = self._parse_expression(it)
        self.__next_token(it)  # 将 curr_token 移动到语句的结尾处 `;`
        if self.curr_token is None or self.curr_token.type != TokenType.SEMICOLON:
            raise TokenError("Return statements must end with a semicolon(`;`)")

        return ReturnStatement(expr)

    @parse_trace("Expression-Statement")
    def __parse_expr_statement(self, it: Iterator[Token]) -> ExprStatement:  # add(1, 2);
        expr = self._parse_expression(it)
        self.__next_token(it)  # 将 curr_token 移动到语句的结尾处 `;`
        if self.curr_token is None or self.curr_token.type != TokenType.SEMICOLON:
            raise TokenError("Expression statements must end with a semicolon(`;`)")

        return ExprStatement(expr)

    @parse_trace("Block-Statement")
    def __parse_block_statement(self, it: Iterator[Token]) -> BlockStatement:  # {1+2;}
        if self.curr_token is None or self.curr_token.type != TokenType.LBRACE:
            raise TokenError("Block statement must begin with a left brace(`{`).")
        self.__next_token(it)  # 将 curr_token 移动到块语句内部的开头处
        if self.curr_token is None:
            raise TokenError("Block statement must end with a right brace(`}`).")
        statements = []
        while self.curr_token.type != TokenType.RBRACE:
            stmt = self._parse_statement(it)
            if stmt is not None:
                statements.append(stmt)
            self.__next_token(it)  # 将 curr_token 指向下一条语句的开头
        return BlockStatement(*statements)

    @parse_trace("Identifier Expression")
    def __parse_iden_expression(self, *args) -> IdenExpression:  # 解析 `标识符表达式`
        return IdenExpression(self.curr_token.literal)

    @parse_trace("IntLiteral Expression")
    def __parse_int_literal_expression(self, *args) -> IntLiteralExpression:  # 解析 `整型字面量表达式`
        try:
            if self.curr_token.literal.startswith("0x") or self.curr_token.literal.startswith("0X"):
                base = 16
            elif self.curr_token.literal.startswith("0"):
                base = 8
            else:
                base = 10
            return IntLiteralExpression(int(self.curr_token.literal, base))
        except ValueError as err:
            raise TokenLiteralError(str(err))

    @parse_trace("BoolLiteral Expression")
    def __parse_bool_literal_expression(self, *args) -> BoolLiteralExpression:  # 解析 `布尔字面量表达式`
        if self.curr_token.type == TokenType.TRUE:
            return BoolLiteralExpression(True)
        elif self.curr_token.type == TokenType.FALSE:
            return BoolLiteralExpression(False)
        else:
            raise TokenLiteralError("Boolean literal expression only support `true` and `false`.")

    @parse_trace("Unary Operator Expression")
    def __parse_unary_op_expression(self, it: Iterator[Token], *args) -> UnaryOpExpression:  # 解析 `一元运算符表达式`
        op_token = self.curr_token
        self.__next_token(it)  # 将 curr_token 移动到一元预算符后面的表达式
        if self.curr_token is None or self.curr_token.type == TokenType.SEMICOLON:
            raise TokenError("The `expression` for the unary operater does not exist.")
        return UnaryOpExpression(op_token, self._parse_expression(it, _token_precedence(op_token)))

    @parse_trace("Grouped Expression")
    def __parse_grouped_expression(self, it: Iterator[Token], *args) -> Type[Expression]:  # 解析 `分组()表达式`
        self.__next_token(it)  # 将 curr_token 移动到括号内的表达式
        expr = self._parse_expression(it, Precedence.DEFAULT)
        self.__next_token(it)  # 将 curr_token 移动到右括号`)`处
        if self.curr_token is None or self.curr_token.type != TokenType.RPAREN:
            raise TokenError("Grouped Expression must end with a right parenthesis(`)`).")
        return expr

    @parse_trace("Binary Operator Expression")
    def __parse_binary_op_expression(self, left: Type[Expression], it: Iterator[Token], *args) -> BinaryOpExpression:  # 解析 `二元运算符表达式`
        op_token = self.curr_token
        precedence = _token_precedence(op_token)  # 当前运算符的优先级
        self.__next_token(it)  # 将 curr_token 移动到右侧表达式起始处
        if self.curr_token is None or self.curr_token.type == TokenType.SEMICOLON:
            raise TokenError("The `right expression` for the binary operater does not exist.")
        right = self._parse_expression(it, precedence)
        return BinaryOpExpression(op_token, left, right)

    @parse_trace("If Expression")
    def __parse_if_expression(self, it: Iterator[Token], *args) -> IfExpression:  # if (<条件表达式>) {<结果>} else {<可替代的结果>}
        if self.peek_token is None or self.peek_token.type != TokenType.LPAREN:
            raise TokenError("The `if` keyword must be followed by a conditional expression.")
        self.__next_token(it)
        self.__next_token(it)  # 将 curr_token 移动到`(`后面的表达式开头处
        cond_expr = self._parse_expression(it, Precedence.DEFAULT)
        self.__next_token(it)  # 将 curr_token 移动到右括号`)`处
        if self.curr_token is None or self.curr_token.type != TokenType.RPAREN:
            raise TokenError("The conditional expression in if statement must be enclosed in parentheses.")
        self.__next_token(it)  # 将 curr_token 移动到 <结果> 的块语句处
        conseq_stmt = self.__parse_block_statement(it)
        if self.peek_token is not None and self.peek_token.type == TokenType.ELSE:  # 是否存在else语句块
            self.__next_token(it)
            self.__next_token(it)  # 将 curr_token 移动到 <可替代的结果> 的块语句处
            return IfExpression(cond_expr, conseq_stmt, self.__parse_block_statement(it))
        return IfExpression(cond_expr, conseq_stmt)

    def __prepare_parse(self) -> Iterator[Token]:
        it = iter(self.__lexer)
        self.curr_token = next(it, None)
        self.peek_token = next(it, None)
        return it

    def __next_token(self, it: Iterator[Token]):
        self.curr_token = self.peek_token
        self.peek_token = next(it, None)

    def __nuds_parse_func(self, tok: Union[Token | TokenType]) -> Optional[Callable]:
        token_type = tok.type if isinstance(tok, Token) else tok
        match token_type:
            case TokenType.IDENTIFIER:
                return self.__parse_iden_expression
            case TokenType.INTEGER:
                return self.__parse_int_literal_expression
            case TokenType.TRUE | TokenType.FALSE:
                return self.__parse_bool_literal_expression
            case TokenType.SUB | TokenType.NOT:  # 一元运算符: `-`, `!`
                return self.__parse_unary_op_expression
            case TokenType.LPAREN:  # `(`
                return self.__parse_grouped_expression
            case TokenType.IF:
                return self.__parse_if_expression
            case _:
                return None

    def __leds_parse_func(self, tok: Union[Token | TokenType]) -> Optional[Callable]:
        token_type = tok.type if isinstance(tok, Token) else tok
        match token_type:
            case (
                TokenType.ADD
                | TokenType.SUB
                | TokenType.MUL
                | TokenType.DIV
                | TokenType.AND
                | TokenType.OR
                | TokenType.LT
                | TokenType.LE
                | TokenType.GT
                | TokenType.GE
                | TokenType.EQ
                | TokenType.NEQ
            ):
                return self.__parse_binary_op_expression
            case _:
                return None
