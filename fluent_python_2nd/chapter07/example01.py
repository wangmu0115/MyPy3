from _builtins.pprint import console_print, head_print, tail_print

from .chapter07 import factorial

# cd ${MyPy3 Path}
# python -m fluent_python_2nd.chapter07.example01
if __name__ == "__main__":
    head_print("Example 7.1")
    console_print(factorial(10))
    console_print(factorial.__doc__)
    console_print(type(factorial))  # `factorial` is an instance of the `function` class.
    tail_print("Example 7.1")
