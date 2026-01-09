registry = []


def register(func):
    print(f"Running register({func.__name__})")
    registry.append(func)
    return func


@register
def f1():
    print("Running f1")


@register
def f2():
    print("Running f2")


def f3():
    print("Running f3")


def main():
    print("Running main")
    print("Registry ->", registry)
    f1()
    f2()
    f3()


# python -m fluent_python_2nd.chapter09.registration
if __name__ == "__main__":
    main()
