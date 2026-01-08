from _builtins.pprint import console_print, head_print, tail_print

from .chapter07 import factorial

# cd ${MyPy3 Path}
# python -m fluent_python_2nd.chapter07.example02
if __name__ == "__main__":
    head_print("Example 7.2")
    fact = factorial
    console_print(fact(10))
    console_print(list(map(factorial, range(11))))
    tail_print("Example 7.2")
