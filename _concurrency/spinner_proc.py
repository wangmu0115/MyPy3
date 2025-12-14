import itertools
import math
import time
from multiprocessing import Event, Process, synchronize


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


def spin(msg: str, done: synchronize.Event) -> None:
    for ch in itertools.cycle(r"\|/-"):
        status = f"\r{ch} {msg}"
        print(status, end="")
        if done.wait(0.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


def slow():
    is_prime(5_000_111_000_222_021)
    # time.sleep(3)
    return 42


def supervisor() -> int:
    done = Event()
    spinner = Process(target=spin, args=("thinking", done))
    print(f"Spinner object: {spinner}")
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


def main():
    print(f"Answer: {supervisor()}.")


if __name__ == "__main__":
    main()
