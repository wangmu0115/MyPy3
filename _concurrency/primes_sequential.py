import math
from time import perf_counter
from typing import NamedTuple

PRIME_FIXTURE = [
    (2, True),
    (142702110479723, True),
    (299593572317531, True),
    (3333333333333301, True),
    (3333333333333333, False),
    (3333335652092209, False),
    (4444444444444423, True),
    (4444444444444444, False),
    (4444444488888889, False),
    (5555553133149889, False),
    (5555555555555503, True),
    (5555555555555555, False),
    (6666666666666666, False),
    (6666666666666719, True),
    (6666667141414921, False),
    (7777777536340681, False),
    (7777777777777753, True),
    (7777777777777777, False),
    (9999999999999917, True),
    (9999999999999999, False),
]

NUMBERS = [n for n, _ in PRIME_FIXTURE]


def is_prime(num: int) -> bool:
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, math.isqrt(num) + 1):
            if num % i == 0:
                return False
        return True


class Result(NamedTuple):
    prime: bool
    elapsed: float


def check(num: int) -> Result:
    t0 = perf_counter()
    prime = is_prime(num)
    return Result(prime, perf_counter() - t0)


def main() -> None:
    print(f"Checking {len(NUMBERS)} numbers sequentially:")
    t0 = perf_counter()
    for num in NUMBERS:
        prime, elapsed = check(num)
        label = "P" if prime else " "
        print(f"{num:16} {label} {elapsed: 9.6f}s")
    print(f"Total time: {perf_counter() - t0: .2f}s")


if __name__ == "__main__":
    main()
