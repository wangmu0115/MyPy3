from enum import StrEnum
from typing import Optional


class TokenType(StrEnum):
    ILLEGAL = "illegal"  # unsupported token
    EOF = "EOF"  # End Of File

    IDENTIFIER = "identifier"  # 标识符
    INTEGER = "integer"
    STRING = "string"

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

    TRUE = "True"  # Boolean
    FALSE = "False"

    LET = "let"
    RETURN = "return"
    FUNCTION = "fn"
    IF = "if"
    ELSE = "else"


class Token:
    def __init__(self, type: TokenType, literal: Optional[str] = None):
        self.__type = type
        self.__literal = literal or type.value

    @property
    def type(self):
        return self.__type

    @property
    def literal(self):
        return self.__literal

    def __repr__(self):
        return f"Token(type={self.type.name}, literal='{self.literal}')"

    def __str__(self):
        return f"{self.type.name}('{self.literal}')"
