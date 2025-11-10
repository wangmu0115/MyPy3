from __future__ import annotations

import operator
from typing import Optional

from _interpreter.datamodel import BuiltinCallable, Object


class Env:
    def __init__(self, builtins: Optional[dict[str, Object]] = None, outer: Optional[Env] = None):
        self.store: dict[str, Object] = builtins or dict()
        self.outer = outer

    def get(self, name: str) -> Object:
        val = self.store.get(name, None)
        if val is None and self.outer is not None:
            return self.outer.get(name)
        return val

    def update(self, name: str, value: Object) -> Object:
        self.store[name] = value
        return value


def standard_env() -> Env:
    builtin_operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,  # TODO
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
    }

    builtins = dict()
    builtins.update({op[0]: BuiltinCallable(op[1]) for op in builtin_operators.items()})

    return Env(builtins)


def build_enclosed_env(outer_env: Env):
    env = Env()
    env.outer = outer_env
    return env
