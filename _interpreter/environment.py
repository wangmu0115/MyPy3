import operator
from typing import Callable


class Env:
    def __init__(self):
        self.callables = dict()

    def register(self, extra_callables: dict[str, Callable]):
        self.callables.update(extra_callables)

    def get(self, op: str) -> Callable:
        return self.callables.get(op, None)


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
