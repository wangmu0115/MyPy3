from typing import Iterator, Type

from _interpreter import Token, TokenType


class Node:
    """抽象语法树的节点抽象基类，它有两个子类，分别是 Statement 和 Expression ，表示语句和表达式"""

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
    def __init__(self, *statements: Iterator[Statement]):
        self.statements = list(statements)


class Identifier:
    def __init__(self, value: str):
        self.token = Token(TokenType.IDENTIFIER, value)
        self.value = value


class LetStatement:
    """let语句: let <标识符> = <表达式>;
    name 用来保存绑定的标识符;value 为产生 值的表达式。
    """

    def __init__(self, name: str, value: Type[Expression]):
        self.token = Token(TokenType.LET)
        self.name = Identifier(name)
        self.value = value
