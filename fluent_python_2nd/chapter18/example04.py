from _builtins.pprint import console_print, head_print, tail_print

from .mirror import LookingGlass

# python -m fluent_python_2nd.chapter18.example04
if __name__ == "__main__":
    head_print("Example18.04")

    manager = LookingGlass()
    console_print(manager)
    monster = manager.__enter__()
    console_print(monster)
    console_print(monster == "JABBERWOCKY")
    console_print(manager)
    manager.__exit__(ZeroDivisionError, ZeroDivisionError(), None)
    console_print(monster)

    tail_print("Example18.04")
