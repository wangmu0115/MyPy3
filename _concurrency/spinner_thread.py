import itertools
import time
from threading import Event, Thread


def spin(msg: str, done: Event) -> None:
    """Run in a thread,
    Argument:
        msg:
        done: threading.Event，用于同步线程的简单对象
    """
    for ch in itertools.cycle("\|/-"):
        status = f"\r{ch} {msg}"  # 文本实现动画的技巧，通过回车符`\r`将光标移动到行头
        print(status, end="", flush=True)
        if done.wait(0.1):  # 暂停等待0.1秒，动画帧率设置为 10 fps
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")  # 显示空格，并把光标移到开头，清空状态行。


def slow() -> int:
    time.sleep(3)  # 调用 time.sleep() 阻塞所在的线程，但是释放 GIL，其他 Python 线程可以继续运行。
    return 42


def supervisor() -> int:
    done = Event()
    spipper = Thread(target=spin, args=("Thinking...", done))
    print(f"Spinner object: {spipper!r}")
    spipper.start()
    result = slow()
    done.set()
    spipper.join()
    return result


def main() -> None:
    result = supervisor()
    print(f"Answer: {result}.")


if __name__ == "__main__":
    main()
