def test_coding_readwrite():
    with open("cafe.txt", "w", encoding="utf_8") as f:
        f.write("café")
    with open("cafe.txt", "r", encoding="gb2312") as f:
        print(f.read())


if __name__ == "__main__":
    test_coding_readwrite()
