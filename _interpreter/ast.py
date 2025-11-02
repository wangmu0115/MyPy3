from typing import Iterator, Type

from _interpreter import Token, TokenType


class Node:
    """抽象语法树的节点类，节点类型为表达式或语句"""

    def __repr__(self):
        return "Node()"


class Statement(Node):
    """抽象语法树中的语句节点"""

    def __repr__(self):
        return "Statement()"


class Expression(Node):
    """抽象语法树中的表达式节点"""

    def __repr__(self):
        return "Expression()"


class Program:
    """每个有效的程序都由一系列的语句构成"""

    def __init__(self, *statements: Iterator[Statement]):
        self.statements = list(statements)

    def append(self, statement: Statement):
        self.statements.append(statement)

    def __str__(self):
        return "\n".join(str(stmt) for stmt in self.statements)


class Identifier(Expression):
    """标识符，在let语句的等号左边不会产生值，在右边会产生值"""

    def __init__(self, name: str):
        if not name:
            raise ValueError("标识符名称不能为空")
        self.__token = Token(TokenType.IDENTIFIER, name)

    @property
    def name(self):
        return self.__token.literal

    def __repr__(self):
        return f"Identifier(token={self.__token!r})"

    def __str__(self):
        return self.name


class LetStatement(Statement):
    """let 语句: `let <标识符> = <表达式>;`"""

    def __init__(self, name: str, value: Type[Expression]):
        self.__iden = Identifier(name)
        self.__value = value

    @property
    def iden(self) -> Identifier:
        return self.__iden

    @property
    def name(self) -> str:
        return self.iden.name

    @property
    def value(self) -> Type[Expression]:
        return self.__value

    def __repr__(self):
        return f"LetStatement(identifier={self.iden!r}, value={self.value!r})"

    def __str__(self):
        return f"let {self.name} = {self.value};"


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


class ExpressionStatement(Statement):
    """表达式语句，example: x+10;"""

    def __init__(self, expression: Type[Expression]):
        self.__expression = expression

    @property
    def expression(self):
        return self.__expression

    def __repr__(self):
        return f"ExpressionStatement(expression={self.expression!r})"

    def __str__(self):
        return f"{self.expression}"
