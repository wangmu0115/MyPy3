from pathlib import Path
from time import perf_counter
from typing import Callable

import httpx

POP20_CC = list("CH IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR".split())
DEST_DIR = Path("/tmp/downloaded")
BASE_URL = "http://mp.ituring.com.cn/files/flags"


def get_flag(cc: str):
    url = f"{BASE_URL}/{cc}/{cc}.gif".lower()
    resp = httpx.get(url, timeout=15.0, follow_redirects=True)
    resp.raise_for_status()
    return resp.content


def save_flag(img: bytes, filename: str) -> None:
    (DEST_DIR / filename).write_bytes(img)


def download_flags(downloader: Callable[[list[str]], int]) -> None:
    DEST_DIR.mkdir(exist_ok=True)
    t0 = perf_counter()
    count = downloader(POP20_CC)
    print(f"\n{count} downloads in {perf_counter() - t0:.2f}s")
