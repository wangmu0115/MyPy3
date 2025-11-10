import operator
from functools import singledispatch
from typing import Union

from _interpreter import Token
from _interpreter.ast import (
    BinaryOpExpression,
    BlockStatement,
    BoolLiteralExpression,
    ExprStatement,
    IdenExpression,
    IfExpression,
    IntLiteralExpression,
    LetStatement,
    Node,
    Program,
    ReturnStatement,
    UnaryOpExpression,
)
from _interpreter.datamodel import Boolean, Integer, Null, Object, ObjectType, ReturnObj
from _interpreter.environment import Env, standard_env
from _interpreter.parser import TokenError, TokenLiteralError, TokenTypeError
from _interpreter.tokens import TokenType

_Null = Null()

_STANDARD_ENV = standard_env()


@singledispatch
def evaluate(node: Union[Node | Program], env: Env = _STANDARD_ENV) -> Object: ...


@evaluate.register
def _(program: Program, env: Env = _STANDARD_ENV) -> Object:
    if len(program.stmts) == 0:
        return _Null
    for stmt in program.stmts:
        res = evaluate(stmt, env)
        if res.type == ObjectType.RETURN:
            return res.value
    return res


@evaluate.register
def _(node: Node, env: Env = _STANDARD_ENV) -> Object:
    match node:
        case LetStatement():
            value = evaluate(node.value)
            env.set_value(node.iden, value.value if value.type == ObjectType.RETURN else value)
            return _Null
        case BlockStatement():
            return _eval_block_statement(node, env)
        case ExprStatement():
            return evaluate(node.expression, env)
        case ReturnStatement():
            return ReturnObj(evaluate(node.value, env))

        case IdenExpression():
            val = env.get_value(node.iden)
            if val is None:
                raise TokenLiteralError()
            return val
        case IntLiteralExpression():
            return Integer(node.literal)
        case BoolLiteralExpression():
            return Boolean(node.literal)
        case UnaryOpExpression():
            right = evaluate(node.right, env)
            return _evaluate_unaryop_expr(node.operator, right)
        case BinaryOpExpression():
            left = evaluate(node.left, env)
            right = evaluate(node.right, env)
            return _evaluate_binaryop_expr(node.operator, left, right, env)
        case IfExpression():
            cond = evaluate(node.condition, env)
            if bool(cond.value):  # 使用 Python 的真值判断 https://docs.python.org/3/library/stdtypes.html#truth
                return evaluate(node.consequence, env)
            elif node.alternative is not None:
                return evaluate(node.alternative, env)
            else:
                return _Null
        case _:
            return _Null


def _eval_block_statement(block_stmt: BlockStatement, env: Env) -> Object:
    if len(block_stmt) == 0:
        return _Null
    for stmt in block_stmt.stmts:
        result = evaluate(stmt, env)
        if result.type == ObjectType.RETURN:
            return result
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


def _evaluate_binaryop_expr(op: Token, left: Object, right: Object, env: Env) -> Object:
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
