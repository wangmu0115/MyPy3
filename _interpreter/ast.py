from __future__ import annotations

from typing import Generic, Iterator, Optional, Type, TypeVar

from _interpreter import Token


class Node: ...  # AST 节点，分为语句和表达式


class Statement(Node): ...  # 语句


class Expression(Node): ...  # 表达式节


class Program:
    """程序由一系列的语句构成"""

    def __init__(self, *statements: Iterator[Type[Statement]]):
        self.statements = list(statements)

    def append(self, statement: Type[Statement]):
        self.statements.append(statement)

    def __repr__(self):
        return "\n".join(repr(stmt) for stmt in self.statements)

    def __str__(self):
        return "\n".join(str(stmt) for stmt in self.statements)


class IdenExpression(Expression):
    """标识符表达式"""

    def __init__(self, iden: str):
        self.__iden = iden

    @property
    def iden(self):
        return self.__iden

    def __repr__(self):
        return f"IdenExpression(iden={self.iden!r})"

    def __str__(self):
        return self.iden


LiteralType = TypeVar("T")


class LiteralExpression(Expression, Generic[LiteralType]):
    def __init__(self, literal: LiteralType):
        self.__literal = literal

    @property
    def literal(self) -> LiteralType:
        return self.__literal

    def __repr__(self):
        return f"LiteralExpression(literal={self.literal!r}, type={type(self.literal)})"

    def __str__(self):
        return str(self.literal)


class BoolLiteralExpression(LiteralExpression[bool]): ...


class IntLiteralExpression(LiteralExpression[int]): ...


class UnaryOpExpression(Expression):
    """一元运算符表达式"""

    def __init__(self, operator: Token, right: Type[Expression]):
        self.__operator = operator
        self.__right = right

    @property
    def operator(self) -> Token:
        return self.__operator

    @property
    def right(self) -> Type[Expression]:
        return self.__right

    def __repr__(self):
        return f"UnaryOpExpression(operator={self.operator!r}, right={self.right!r})"

    def __str__(self):
        return f"({self.operator.literal}{str(self.right)})"


class BinaryOpExpression(Expression):
    """二元运算符表达式，使用中缀表达式表示"""

    def __init__(self, operator: Token, left: Type[Expression], right: Type[Expression]):
        self.__operator = operator
        self.__left = left
        self.__right = right

    @property
    def operator(self) -> Token:
        return self.__operator

    @property
    def left(self) -> Type[Expression]:
        return self.__left

    @property
    def right(self) -> Type[Expression]:
        return self.__right

    def __repr__(self):
        return f"BinaryOpExpression(operator={self.operator!r}, left={self.left!r}, right={self.right!r})"

    def __str__(self):
        return f"({str(self.left)} {self.operator.literal} {str(self.right)})"


class IfExpression(Expression):
    def __init__(self, condition: Expression, consequence: BlockStatement, alternative: Optional[BlockStatement] = None):
        self.__condition = condition
        self.__consequence = consequence
        self.__alternative = alternative

    @property
    def condition(self) -> Type[Expression]:
        return self.__condition

    @property
    def consequence(self) -> BlockStatement:
        return self.__consequence

    @property
    def alternative(self) -> BlockStatement:
        return self.__alternative

    def __repr__(self):
        return f"IfExpression(condition={self.condition!r}, consequence={self.consequence!r}, alternative={self.alternative!r})"

    def __str__(self):
        expr_str = f"if{self.condition}{self.consequence}"
        if self.alternative is not None:
            expr_str += f"else{self.alternative}"
        return expr_str


class FuncExpression(Expression):
    """函数表达式: fn <参数列表> <块语句>"""

    def __init__(self, parameters: list[IdenExpression], body: BlockStatement):
        self.__parameters = list(parameters)
        self.__body = body

    @property
    def params(self) -> list[IdenExpression]:
        return self.paramters

    @property
    def paramters(self) -> list[IdenExpression]:
        return self.__parameters

    @property
    def body(self) -> BlockStatement:
        return self.__body

    def __repr__(self):
        return f"FuncExpression(parameters={self.paramters!r}, body={self.body!r})"

    def __str__(self):
        params = ",".join(str(p) for p in self.params)
        return f"fn({params}){self.body}"


class LetStatement(Statement):
    """let 语句: `let <标识符> = <表达式>;`"""

    def __init__(self, iden: str, value: Type[Expression]):
        self.__iden_expr = IdenExpression(iden)
        self.__value = value

    @property
    def iden_expr(self) -> IdenExpression:
        return self.__iden_expr

    @property
    def iden(self) -> str:
        return self.iden_expr.iden

    @property
    def value(self) -> Type[Expression]:
        return self.__value

    def __repr__(self):
        return f"LetStatement(iden={self.iden_expr!r}, value={self.value!r})"

    def __str__(self):
        return f"let {self.iden} = {self.value};"


class ReturnStatement(Statement):
    """return 语句: `return <表达式>;`"""

    def __init__(self, value: Type[Expression]):
        self.__value = value

    @property
    def value(self):
        return self.__value

    def __repr__(self):
        return f"ReturnStatement(value={self.value!r})"

    def __str__(self):
        return f"return {self.value};"


class ExprStatement(Statement):
    """表达式语句，example: x+10;"""

    def __init__(self, expression: Type[Expression]):
        self.__expression = expression

    @property
    def expression(self):
        return self.__expression

    def __repr__(self):
        return f"ExpressionStatement(expression={self.expression!r})"

    def __str__(self):
        return f"{self.expression};"


class BlockStatement(Statement):
    """块语句: {...}"""

    def __init__(self, *statements: Iterator[Type[Statement]]):
        self.__statements = list(statements)

    def append(self, statement: Type[Statement]):
        self.__statements.append(statement)

    def __len__(self):
        return len(self.__statements)

    def __repr__(self):
        return f"BlockStatment(statements={self.__statements!r})"

    def __str__(self):
        if len(self.__statements) == 0:
            return "{ }"
        elif len(self.__statements) == 1:
            return "{ " + str(self.__statements[0]) + " }"
        else:
            return "{\n  " + "\n  ".join(str(stmt) for stmt in self.__statements) + "\n}"
