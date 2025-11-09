import operator
from typing import Type, Union

from _interpreter import Token
from _interpreter.ast import (
    BinaryOpExpression,
    BoolLiteralExpression,
    ExprStatement,
    IntLiteralExpression,
    Node,
    Program,
    Statement,
    UnaryOpExpression,
)
from _interpreter.datamodel import Boolean, Integer, Null, Object
from _interpreter.environment import Env, standard_env
from _interpreter.parser import TokenError, TokenTypeError
from _interpreter.tokens import TokenType

_Null = Null()

_STANDARD_ENV = standard_env()


def evaluate(node: Union[Node | Program], env: Env = _STANDARD_ENV) -> Object:
    match node:
        case Program():
            return _evaluate_statments(node.statements)
        case ExprStatement():
            return evaluate(node.expression)

        case IntLiteralExpression():
            return Integer(node.literal)
        case BoolLiteralExpression():
            return Boolean(node.literal)
        case UnaryOpExpression():
            right = evaluate(node.right)
            return _evaluate_unaryop_expr(node.operator, right)
        case BinaryOpExpression():
            left = evaluate(node.left)
            right = evaluate(node.right)
            return _evaluate_binaryop_expr(env, node.operator, left, right)
        case _:
            return _Null


def _evaluate_statments(statements: list[Type[Statement]]) -> Object:
    if len(statements) == 0:
        return _Null
    for statement in statements:
        result = evaluate(statement)
    return result


def _evaluate_unaryop_expr(op: Token, right: Object) -> Object:
    match op.type:
        case TokenType.NOT:
            value = operator.not_(right.value)
            return Boolean(value)
        case TokenType.SUB:
            value = operator.neg(right.value)
            return Integer(value)
        case _:
            raise TokenTypeError()


def _evaluate_binaryop_expr(env: Env, op: Token, left: Object, right: Object) -> Object:
    op_func = env.get(op.literal)
    if op_func is None:
        raise TokenError()
    match op.type:
        case TokenType.ADD | TokenType.SUB | TokenType.MUL | TokenType.DIV:
            value_type = Integer
        case TokenType.EQ | TokenType.NEQ | TokenType.LT | TokenType.LE | TokenType.GT | TokenType.GE:
            value_type = Boolean
        case _:
            value_type = None

    return value_type(op_func(left.value, right.value))
