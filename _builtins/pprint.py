def head_print(title: str = ""):
    print("\n" + "=" * 40 + f" {title} " + "=" * 40)


def tail_print(title: str = ""):
    print("=" * 40 + f" {title} " + "=" * 40 + "\n")


def console_print(*values: object, sep: str | None = " ", end: str | None = "\n", flush: bool = False):
    print(">>>", *values, sep=sep, end=end, flush=flush)
