from enum import StrEnum
from typing import Optional


class TokenType(StrEnum):
    ILLEGAL = "illegal"  # 未知不合法的词法单元
    EOF = "EOF"  # End Of File

    IDENTIFIER = "identifier"  # 标识符
    INTEGER = "int"  # 整数字面量

    ASSIGN = "="  # 运算符
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    IADD = "+="
    ISUB = "-="
    IMUL = "*="
    IDIV = "/="

    NOT = "!"
    AND = "&"
    OR = "|"
    IAND = "&="
    IOR = "|="

    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    EQ = "=="
    NEQ = "!="

    COMMA = ","
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    FUNCTION = "fn"  # 关键字
    LET = "let"


class Token:
    """词法单元"""

    def __init__(self, type: TokenType, literal: Optional[str] = None):
        self._type = type
        self._literal = literal or type.value

    def __repr__(self):
        return f"Token(type={self._type!r}, literal={self._literal!r})"

    def is_end(self):
        return self._type == TokenType.EOF
