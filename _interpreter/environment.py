import operator
from typing import Callable, Optional

from _interpreter.datamodel import Object


class Env:
    def __init__(self):
        self.callables = dict()
        self.store: dict[str, Object] = dict()

    def register(self, extra_callables: dict[str, Callable]):
        self.callables.update(extra_callables)

    def get(self, op: str) -> Callable:
        return self.callables.get(op, None)

    def set_value(self, name: str, value: Object) -> Object:
        self.store[name] = value
        return value

    def get_value(self, name: str) -> Optional[Object]:
        return self.store.get(name, None)


def standard_env() -> Env:
    env = Env()
    env.register(
        {
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
    )
    return env


if __name__ == "__main__":
    env = standard_env()

    print(env.callables)
