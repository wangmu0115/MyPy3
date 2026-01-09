import contextlib
import sys

from _builtins.pprint import console_print, head_print, tail_print


@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write
    sys.stdout.write = lambda text: original_write(text[::-1])

    yield "JABBERWOCKY"

    sys.stdout.write = original_write


# python -m fluent_python_2nd.chapter18.mirror_gen
if __name__ == "__main__":
    head_print("contextlib.contextmanager")
    with looking_glass() as what:
        console_print("Alice, Kitty and Snowdrop")
        console_print(what)
    print("-" * 40, " end with ", "-" * 40)
    console_print(what)
    console_print("Alice, Kitty and Snowdrop")
    tail_print("contextlib.contextmanager")
