from _concurrency import download_flags, get_flag, save_flag


def download_many(cc_list: list[str]) -> int:
    for cc in sorted(cc_list):
        img = get_flag(cc)  # flag image
        save_flag(img, f"{cc}.gif")
        print(cc, end=" ", flush=True)
    return len(cc_list)


# python -m _concurrency.flags_sequential
if __name__ == "__main__":
    download_flags(download_many)
