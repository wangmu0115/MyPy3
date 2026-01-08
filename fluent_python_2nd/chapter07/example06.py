from functools import reduce
from operator import add, mul

from _builtins.pprint import console_print, head_print, tail_print

# cd ${MyPy3 Path}
# python -m fluent_python_2nd.chapter07.example06
if __name__ == "__main__":
    head_print("Example 7.6 functools.reduce, sum")
    console_print("reduce(add, seq):", reduce(add, range(100)))
    console_print("reduce(mul, seq, initial):", reduce(mul, range(1, 6), 10))
    console_print("sum:", sum(range(100)))
    all_trues = [42, True, "hello", 3.14]
    console_print("all:", all(all_trues))
    console_print("all:", all([]))
    all_falses = [0, False, "", 0.0]
    console_print("any:", any(all_falses))
    console_print("any:", any([]))
    tail_print("Example 7.6 functools.reduce, sum")
