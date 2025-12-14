from typing import TYPE_CHECKING

from _import_utils import import_attr

if TYPE_CHECKING:
    pass

__all__ = []

_dynamic_imports = {}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return __all__
