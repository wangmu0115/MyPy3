import time

from _builtins.pprint import console_print, head_print

from .clockdecorator import clock


@clock
def snooze(seconds: float) -> None:
    time.sleep(seconds)


@clock
def factorial(n: int) -> int:
    return 1 if n < 2 else n * factorial(n - 1)

# python -m fluent_python_2nd.chapter09.example15
if __name__ == "__main__":
    head_print("Calling snooze")
    snooze(0.5)
    head_print("Calling factorial")
    console_print("6! =", factorial(6))
    print(factorial.__name__)
