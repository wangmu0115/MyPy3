from functools import wraps
from typing import Any, Callable


class ParameterValidator:
    @staticmethod
    def types(param_name: str, allowed_types):
        def decorator(func):
            if not hasattr(func, "_validation_rules"):  # 链式传导，用于支持多验证器叠加生效
                func._validation_rules = []
            func._validation_rules.append(("allowed_types", param_name, allowed_types))

            @wraps(func)
            def wrapper(*args, **kwargs):
                ParameterValidator._validate_validation_rules(func, args, kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def values(param_name: str, allowed_values: list[Any]):
        def decorator(func):
            if not hasattr(func, "_validation_rules"):  # 链式传导，用于支持多验证器叠加生效
                func._validation_rules = []
            func._validation_rules.append(("allowed_values", param_name, allowed_values))

            @wraps(func)
            def wrapper(*args, **kwargs):
                ParameterValidator._validate_validation_rules(func, args, kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def range(param_name: str, min_value: Any = None, max_value: Any = None):
        def decorator(func):
            if not hasattr(func, "_validation_rules"):  # 链式传导，用于支持多验证器叠加生效
                func._validation_rules = []
            func._validation_rules.append(("value_range", param_name, (min_value, max_value)))

            @wraps(func)
            def wrapper(*args, **kwargs):
                ParameterValidator._validate_validation_rules(func, args, kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def custom(param_name: str, validator: Callable):
        def decorator(func):
            if not hasattr(func, "_validation_rules"):  # 链式传导，用于支持多验证器叠加生效
                func._validation_rules = []
            func._validation_rules.append(("custom_validate", param_name, validator))

            @wraps(func)
            def wrapper(*args, **kwargs):
                ParameterValidator._validate_validation_rules(func, args, kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def _validate_validation_rules(func, args, kwargs):
        func_sig = func.__code__
        positional_param_names = func_sig.co_varnames[: func_sig.co_argcount]  # positional-only parameters

        if hasattr(func, "_validation_rules"):
            for rule_type, param_name, param_rule in func._validation_rules:
                if rule_type == "allowed_types":
                    _validate_allowed_types(param_name, param_rule, args, kwargs, positional_param_names)
                elif rule_type == "allowed_values":
                    _validate_allowed_values(param_name, param_rule, args, kwargs, positional_param_names)
                elif rule_type == "value_range":
                    _validate_value_range(param_name, param_rule[0], param_rule[1], args, kwargs, positional_param_names)
                elif rule_type == "custom_validate":
                    _validate_custom(param_name, param_rule, args, kwargs, positional_param_names)
                else:
                    raise NotImplementedError("Parameter validation rules not implemented.")


def comprehensive_validator(rules: dict[str, dict[str, Any]]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_sig = func.__code__
            param_names: tuple[str] = func_sig.co_varnames[: func_sig.co_argcount]  # positional-only parameters

            for param_name, param_rules in rules.items():
                if "allowed_values" in param_rules:
                    _validate_allowed_values(param_name, param_rules["allowed_values"], args, kwargs, param_names)
                if "allowed_types" in param_rules:
                    _validate_allowed_types(param_name, param_rules["allowed_types"], args, kwargs, param_names)
                if "min_value" in param_rules or "max_values" in param_rules:
                    _validate_value_range(param_name, param_rules.get("min_value", None), param_rules.get("max_value", None), args, kwargs, param_names)
                if "custom_validate" in param_rules:
                    _validate_custom(param_name, param_rules["custom_validate"], args, kwargs, param_names)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def _validate_allowed_values(param_name, allowed_values, args, kwargs, positional_param_names):
    param_value = _param_value(param_name, args, kwargs, positional_param_names)
    if param_value is not None and param_value not in allowed_values:
        raise ValueError(f"The `{param_name}`'s value: `{param_value}` is invalid, allowed values: {allowed_values}")


def _validate_allowed_types(param_name, allowed_types, args, kwargs, positional_param_names):
    param_value = _param_value(param_name, args, kwargs, positional_param_names)
    if param_value is not None and not isinstance(param_value, allowed_types):
        raise TypeError(f"The `{param_name}`'s type: `{param_value.__class__.__name__}` is invalid, allowed types: {allowed_types}")


def _validate_value_range(param_name, min_value, max_value, args, kwargs, positional_param_names):
    param_value = _param_value(param_name, args, kwargs, positional_param_names)
    if param_value is not None:
        if min_value is not None and param_value < min_value:
            raise ValueError(f"The `{param_name}`'s value: `{param_value}` is less than `{min_value}`.")
        if max_value is not None and param_value > max_value:
            raise ValueError(f"The `{param_name}`'s value: `{param_value}` is greater than `{min_value}`.")


def _validate_custom(param_name, validation, args, kwargs, positional_param_names):
    param_value = _param_value(param_name, args, kwargs, positional_param_names)
    if param_value is not None and not validation(param_value):
        raise ValueError(f"The parameter `{param_name}` value: `{param_value}` is invalid.")


def _param_value(param_name, args, kwargs, positional_param_names):
    if param_name in positional_param_names:  # positional param
        param_index = positional_param_names.index(param_name)
        if param_index < len(args):
            return args[param_index]
    if param_name in kwargs:  # keyward param
        return kwargs[param_name]
    return None
