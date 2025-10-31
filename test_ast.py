from _interpreter.ast import Identifier

iden = Identifier("x")
print(iden)
print(f"{iden!r}")
print(iden.name)
