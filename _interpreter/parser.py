from typing import Iterator, Optional

from _interpreter.ast import LetStatement, Program, Statement
from _interpreter.tokens import Token, TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self) -> Program:
        program = Program()
        it = iter(self.lexer)
        curr_token = next(it, None)
        while curr_token is not None:
            stmt = _parse_statement(curr_token, it)
            if stmt is not None:
                program.append(stmt)
            curr_token = next(it, None)
        return program


def _parse_statement(curr_token: Token, it: Iterator[Token]):
    match curr_token._type:
        case TokenType.LET:
            return _parse_let_statement(it)
        case _:
            return None


def _parse_let_statement(it: Iterator[Token]):
    iden_token = next(it, None)
    if not __check_token_type(iden_token, TokenType.IDENTIFIER):
        return None
    assign_token = next(it, None)
    if not __check_token_type(assign_token, TokenType.ASSIGN):
        return None
    # TODO Expression
    expr_token = next(it, None)
    while expr_token is not None and __check_token_type(expr_token, TokenType.SEMICOLON):
        expr_token = next(it, None)

    return LetStatement(iden_token._literal, None)


def __check_token_type(tk: Optional[Token], tt: TokenType) -> bool:
    return tk is not None and tk._type == tt
