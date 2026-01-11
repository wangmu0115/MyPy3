from functools import cache

from _builtins.pprint import console_print

from .clockdecorator import clock


@cache
@clock
def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# python -m fluent_python_2nd.chapter09.example17
if __name__ == "__main__":
    console_print(fibonacci(30))
