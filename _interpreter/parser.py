from typing import Callable, Iterator, Optional, Type

from _interpreter.ast import Expression, ExpressionStatement, Identifier, LetStatement, Program, ReturnStatement, Statement
from _interpreter.tokens import Token, TokenType


class TokenError(Exception):
    def __init__(self, expect: TokenType, actual: Optional[Token]):
        super().__init__()
        self.expect = expect
        self.actual = actual

    def __str__(self):
        return f"Expected token type to be `{self.expect}`, but actual is `{self.actual.type if self.actual else None}`."


class Parser:
    """语法解析器"""

    def __init__(self, lexer):
        self.__lexer = lexer

    def parse(self) -> Program:
        program = Program()
        it = iter(self.__lexer)
        curr_token: Token = next(it, None)  # 当前 Token
        while curr_token is not None and curr_token.type != TokenType.EOF:
            stmt = _parse_statement(curr_token, it)  # 解析语句
            if stmt is not None:
                program.append(stmt)
            curr_token = next(it, None)
        return program


def _parse_statement(curr_token: Token, it: Iterator[Token]) -> Type[Statement]:
    match curr_token.type:
        case TokenType.LET:
            return __parse_let_statement(it)  # 解析 let 语句
        case TokenType.RETURN:
            return __parse_return_statement(it)  # 解析 return 语句
        case _:
            return __parse_expression_statement(curr_token, it)  # 解析表达式语句


def __parse_let_statement(it: Iterator[Token]) -> LetStatement:  # let <标识符> = <表达式>;
    iden_token = next(it, None)  # <标识符>
    if not __check_token_type(iden_token, TokenType.IDENTIFIER):
        raise TokenError(TokenType.IDENTIFIER, iden_token)
    assign_token = next(it, None)  # =
    if not __check_token_type(assign_token, TokenType.ASSIGN):
        raise TokenError(TokenType.ASSIGN, assign_token)
    # TODO Expression
    expr_token = next(it, None)  # <表达式>
    while expr_token is not None and __check_token_type(expr_token, TokenType.SEMICOLON):
        expr_token = next(it, None)

    return LetStatement(iden_token.literal, None)


def __parse_return_statement(it: Iterator[Token]) -> ReturnStatement:
    # TODO Expression
    expr_token = next(it, None)  # <表达式>
    while expr_token is not None and __check_token_type(expr_token, TokenType.SEMICOLON):
        expr_token = next(it, None)
    return ReturnStatement(None)


def __parse_expression_statement(curr_token: Token, it: Iterator[Token]) -> Type[Expression]:
    expr = __parse_expression(curr_token, it)
    next_token = next(it, None)
    while next_token is not None and next_token.type != TokenType.SEMICOLON:
        next_token = next(it, None)
    return ExpressionStatement(expr)


def __parse_expression(curr_token: Token, it: Iterator[Token]):
    prefix = __prefix_parse_fn(curr_token.type)
    if prefix is None:
        return None
    else:
        return prefix(curr_token)


def __prefix_parse_fn(token_type: TokenType) -> Optional[Callable]:
    match token_type:
        case TokenType.IDENTIFIER:
            return lambda tok: Identifier(tok.literal)
        case _:
            return None


def __check_token_type(token: Optional[Token], token_type: TokenType) -> bool:  # 判断词法单元的类型
    return token is not None and token.type == token_type
