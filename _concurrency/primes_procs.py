import math
import sys
from multiprocessing import Process, SimpleQueue, queues
from os import cpu_count
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


class PrimeResult(NamedTuple):
    num: int
    prime: bool
    elapsed: float


JobQueue = queues.SimpleQueue[int]
ResultQueue = queues.SimpleQueue[PrimeResult]


def check(num: int) -> PrimeResult:
    t0 = perf_counter()
    return PrimeResult(num, is_prime(num), perf_counter() - t0)


def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while num := jobs.get():
        results.put(check(num))
    results.put(PrimeResult(0, False, 0.0))


def start_jobs(procs: int, jobs: JobQueue, results: ResultQueue) -> None:
    for num in NUMBERS:
        jobs.put(num)
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results))
        proc.start()
        jobs.put(0)


def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs:
        num, prime, elapsed = results.get()
        if num == 0:
            procs_done += 1
        else:
            checked += 1
            label = "P" if prime else " "
            print(f"{num:16} {label} {elapsed: 9.6f}s")
    return checked


def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])
    print(f"Checking {len(NUMBERS)} numbers with {procs} processes:")
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)
    checked = report(procs, results)
    print(f"{checked} checks in {perf_counter() - t0: .2f}s")


if __name__ == "__main__":
    main()
