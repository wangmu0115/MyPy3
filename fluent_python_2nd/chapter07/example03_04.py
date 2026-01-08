from _builtins.pprint import console_print, head_print, tail_print

from .chapter07 import reverse

# cd ${MyPy3 Path}
# python -m fluent_python_2nd.chapter07.example03_04
if __name__ == "__main__":
    head_print("Example 7.3&7.4 higher-order function")
    fruits = ["strawberry", "fig", "apple", "cherry", "raspberry", "banana"]
    console_print(sorted(fruits, key=len))  # sorted is a higher-order function
    console_print(reverse("testing"))
    console_print(sorted(fruits))
    console_print(sorted(fruits, key=reverse))
    tail_print("Example 7.3&7.4 higher-order function")
