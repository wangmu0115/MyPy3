from typing import TYPE_CHECKING

from _import_utils import import_attr

if TYPE_CHECKING:
    from flags_base import download_flags, get_flag, save_flag

__all__ = [
    "get_flag",
    "save_flag",
    "download_flags",
]

_dynamic_imports = {
    "get_flag": "flags_base",
    "save_flag": "flags_base",
    "download_flags": "flags_base",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return __all__
