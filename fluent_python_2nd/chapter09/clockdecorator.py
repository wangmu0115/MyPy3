import functools
import time


def clock(func):
    """clock is a decorator that clocks every invocation of the decorated function
    and displays the elapsed time, the arguments passed, and the result of the call.
    """

    @functools.wraps(func)
    def clocked(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)  # called
        elapsed = time.perf_counter() - start

        name = func.__name__
        arg_list = [repr(arg) for arg in args]
        arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_list)
        print(f"[{elapsed: .8f}s] {name}({arg_str}) -> {result!r}")

        return result

    return clocked
