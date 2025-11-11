from typing import TYPE_CHECKING

from _import_utils import import_attr

if TYPE_CHECKING:
    from lexer import Lexer
    from parser import Parser
    from tokens import BUILTIN_KEYWORDS, BUILTIN_OPERATORS, Token, TokenType

__all__ = [
    "Token",
    "TokenType",
    "BUILTIN_KEYWORDS",
    "BUILTIN_OPERATORS",
    "Lexer",
    "Parser",
]

_dynamic_imports = {
    "Token": "tokens",
    "TokenType": "tokens",
    "BUILTIN_KEYWORDS": "tokens",
    "BUILTIN_OPERATORS": "tokens",
    "Lexer": "lexer",
    "Parser": "parser",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return __all__
