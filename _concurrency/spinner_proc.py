import itertools
import time
from multiprocessing import Event, Process, synchronize


def spin(msg: str, done: synchronize.Event) -> None:
    for ch in itertools.cycle(r"\|/-"):
        status = f"\r{ch} {msg}"
        print(status, end="")
        if done.wait(0.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


def slow():
    time.sleep(3)
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
