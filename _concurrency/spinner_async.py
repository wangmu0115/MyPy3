import asyncio
import itertools
import math


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


async def spin(msg: str) -> None:
    for ch in itertools.cycle(r"\|/-"):
        status = f"\r{ch} {msg}"
        print(status, flush=True, end="")
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


async def slow() -> int:
    # await asyncio.sleep(3)
    is_prime(5_000_111_000_222_021)
    return 42


async def supervisor() -> int:  # 原生协程使用 async def 定义
    spinner = asyncio.create_task(spin("thinking..."))  # 调度 spin 最终执行，立即返回一个 asyncio.Task 实例
    print(f"spinner object: {spinner}")
    result = await slow()  # 阻塞 supervisor 直到 slow()返回
    spinner.cancel()  # 在 spin 协程中抛出 CancelledError 异常
    return result


def main() -> None:
    result = asyncio.run(supervisor())  # 启动事件循环，驱动这个协程，最终也将启动其他协程
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
