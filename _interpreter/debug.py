def parse_trace(parse_phase):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            trace: Trace = getattr(self, "trace")
            debug: bool = getattr(self, "debug", False)
            trace.begin(parse_phase) if debug else ...
            result = func(self, *args, **kwargs)
            trace.end(parse_phase, result) if debug else ...
            return result

        return wrapper

    return decorator


class Trace:
    def __init__(self):
        self.level = 0
        self.placeholder = " "

    def begin(self, phase: str, *args):
        print(f"{self.placeholder * self.level}>>> {phase}", *args)
        self.level += 4

    def end(self, phase: str, *args):
        self.level -= 4
        print(f"{self.placeholder * self.level}<<< {phase}:", *args)
