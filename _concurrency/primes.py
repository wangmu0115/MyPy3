import math
from datetime import datetime


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


if __name__ == "__main__":
    begin = datetime.now()
    print(is_prime(5_000_111_000_222_021))
    print(datetime.now() - begin)
