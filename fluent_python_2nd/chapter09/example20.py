import html
from functools import singledispatch
from typing import Any

from _builtins.pprint import console_print, head_print, tail_print


@singledispatch
def htmlize(obj: Any) -> str:
    content = html.escape(repr(obj))
    return f"<pre>{content}</pre>"


@htmlize.register
def _(text: str) -> str:
    content = html.escape(text).replace("\n", "<br />\n")
    return f"<p>{content}</p>"


if __name__ == "__main__":
    head_print("singledispatch")

    console_print(htmlize({1, 2, 3}))
    console_print(htmlize(abs))
    console_print(htmlize("Heimlich & Co.\n- a game"))

    tail_print("singledispatch")
