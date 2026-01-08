from _builtins.pprint import console_print, head_print, tail_print

from .chapter07 import factorial

# cd ${MyPy3 Path}
# python -m fluent_python_2nd.chapter07.example05
if __name__ == "__main__":
    head_print("Example 7.5 map, filter, listcomp, genexp")
    console_print("map:     ", list(map(factorial, range(6))))
    console_print("genexp:  ", list(factorial(i) for i in range(6)))
    console_print("listcomp:", [factorial(i) for i in range(6)])
    console_print("map&filter:", list(map(factorial, filter(lambda x: not x % 2, range(6)))))
    console_print("genexp&if: ", list(factorial(i) for i in range(6) if not i % 2))
    tail_print("Example 7.5 map, filter, listcomp, genexp")
