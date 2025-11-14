from functools import wraps


def validate_params(rules: dict[str, list]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_sign = func.__code__  # function signature
            print(func_sign.co_varnames[: func_sign.co_argcount])

            print(func_sign.co_varnames)
            print(func.__type_params__)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@validate_params(rules=dict({"x": [1, 2, 3]}))
def test(x: int, y: str, z: list, *, a: bool = True):
    print("Hello world")


if __name__ == "__main__":
    test(12, "", [], a=12)
