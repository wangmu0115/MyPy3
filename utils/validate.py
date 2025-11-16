from functools import wraps
from typing import Any


class ParameterValidator:
    @staticmethod
    def type(param_name: str, expected_type: type):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                arg_value = ParameterValidator._get_argument_value(func, param_name, args, kwargs)
                if arg_value is not None and not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"The parameter `{param_name}` should be of type `{expected_type.__name__}`, "
                        f"the it is actually of type `{param_name.__class__.__name__}`."
                    )
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def values(param_name: str, allowed_values: list[Any]):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                arg_value = ParameterValidator._get_argument_value(func, param_name, args, kwargs)
                if arg_value is not None and arg_value not in allowed_values:
                    raise ValueError(
                        f"The argument `{arg_value}` for parameter `{param_name}` is not allowed, "
                        f"the allowed values are {allowed_values}."
                    )
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def _get_argument_value(func, param_name, args, kwargs):
        func_sig = func.__code__  # function signature
        param_names: tuple[str] = func_sig.co_varnames[: func_sig.co_argcount]  # positional-only parameters
        if param_name in param_names:  # positional param
            param_index = param_names.index(param_name)
            if param_index < len(args):
                return args[param_index]
        if param_name in kwargs:  # keyward param
            return kwargs[param_name]
        return None
