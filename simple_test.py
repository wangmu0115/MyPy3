import operator

from _interpreter.ast import BoolLiteralExpression, IntLiteralExpression, StrLiteralExpression
from _interpreter.datamodel import BuiltinCallable, DataModelSystem, Integer, ReturnObj
from _interpreter.environment import standard_env
from _interpreter.tokens import Token, TokenType

obj = BuiltinCallable(operator.add)
print(f"{obj!r}")
print(obj.call(1, 2))


env = standard_env()

print(env.store)

print(operator.add(1, 2))


print(DataModelSystem.from_value(1))


print(f"{Token(TokenType.ADD)!r}")
print(Token(TokenType.IDENTIFIER, "Hello"))
print(Token(TokenType.STRING, "Hello World"))


value: int = 12

print(f"{value.__class__.__name__}")


int_expr = IntLiteralExpression(42)
bool_expr = BoolLiteralExpression(True)
str_expr = StrLiteralExpression("Hello World")

print(f"{int_expr!r}-----{int_expr}")
print(f"{bool_expr!r}-----{bool_expr}")
print(f"{str_expr!r}-----{str_expr}")
