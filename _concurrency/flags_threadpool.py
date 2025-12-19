from concurrent import futures

from _concurrency.flags_sequential import get_flag, main, save_flag


def download_one(cc: str):
    img = get_flag(cc)
    save_flag(img, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc


def download_many(cc_list: list[str]) -> list:
    with futures.ThreadPoolExecutor() as executor:
        resp = executor.map(download_one, sorted(cc_list))
    return len(list(resp))


if __name__ == "__main__":
    main(download_many)
