import operator
from functools import singledispatch
from typing import Union

from _interpreter import Token
from _interpreter.ast import (
    BinaryOpExpression,
    BlockStatement,
    BoolLiteralExpression,
    CallExpression,
    ExprStatement,
    FuncExpression,
    IdenExpression,
    IfExpression,
    IntLiteralExpression,
    LetStatement,
    Node,
    Program,
    ReturnStatement,
    UnaryOpExpression,
)
from _interpreter.datamodel import Boolean, BuiltinCallable, DataModelSystem, FunctionObj, Integer, Null, Object, ObjectType, ReturnObj
from _interpreter.environment import Env, standard_env
from _interpreter.parser import TokenError, TokenLiteralError, TokenTypeError
from _interpreter.tokens import TokenType


class UnsupportedOperatorException(Exception): ...


class UndefinedIdenException(Exception): ...


class UndefinedCallException(Exception): ...


class CallArgumentsException(Exception): ...


class EvalException(Exception): ...


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
            value = evaluate(node.value, env)
            env.update(node.iden, __unwrap_return_obj(value))
            return _Null
        case BlockStatement():
            return _eval_block_statement(node, env)
        case ExprStatement():
            return evaluate(node.expression, env)
        case ReturnStatement():
            return ReturnObj(evaluate(node.value, env))

        case IdenExpression():
            value = env.get(node.iden)
            if value is None:
                raise UndefinedIdenException(f"Undefined identifier: {node.iden}")
            return value
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
        case FuncExpression():
            return FunctionObj(node.params, node.body, env)
        case CallExpression():
            callable = evaluate(node.callable, env)
            arguments = [evaluate(arg, env) for arg in node.args]  # 实参列表
            return _apply_callable(callable, arguments)
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
    op_callable = env.get(op.literal)
    if op_callable is None or op_callable.type != ObjectType.BUILTINCALL:
        raise UnsupportedOperatorException(f"Unsupported operator: {op.literal}")
    return _apply_callable(op_callable, [left, right])


def _apply_callable(callable: Object, arguments: list[Object]) -> Object:
    match callable.type:
        case ObjectType.FUNCTION:
            extended_env = __extend_func_env(callable, arguments)
            res = evaluate(callable.body, extended_env)
            return __unwrap_return_obj(res)
        case ObjectType.BUILTINCALL:
            call = callable.call
            return DataModelSystem.from_value(call(*(__unwrap_return_obj(arg).value for arg in arguments)))
        case _:
            raise UndefinedCallException(f"Undefined callable: {callable.value}")


def __extend_func_env(callable: FunctionObj, arguments: list[Object]) -> Env:
    if len(arguments) != len(callable.parameters):
        raise CallArgumentsException(f"Expected {len(callable.parameters)} arguments, got {len(arguments)}")
    env = Env(outer=callable.env)
    for param_index, param in enumerate(callable.parameters):
        env.update(param.iden, arguments[param_index])
    return env


def __unwrap_return_obj(obj: Object) -> Object:
    if obj.type == ObjectType.RETURN:
        return obj.value
    else:
        return obj
