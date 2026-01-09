import sys

from _builtins.pprint import head_print, tail_print


class LookingGlass:
    def __enter__(self):
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return "JABBERWOCKY"

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("Please DO NOT divide by zero!")
            return True

    def reverse_write(self, text):
        self.original_write(text[::-1])


# python -m fluent_python_2nd.chapter18.mirror
if __name__ == "__main__":
    head_print("context manager: LookingGlass")
    text = "Hello World"
    with LookingGlass() as what:
        print(text)
    print(what)
    print(text)
    tail_print("context manager: LookingGlass")
