def factorial(n: int) -> int:
    """Return n!"""
    return 1 if n < 2 else n * factorial(n - 1)


def reverse(word: str) -> str:
    return word[::-1]
