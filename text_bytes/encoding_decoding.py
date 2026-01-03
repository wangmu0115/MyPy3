def test_encode_error():
    city = "São Paulo"
    for codec in ["utf_8", "utf_16", "iso8859_1", "cp437"]:
        try:
            print(city.encode(encoding=codec))
        except UnicodeEncodeError as e:
            print(e)


if __name__ == "__main__":
    s = "café"
    print(">>>", len(s))  # Unicode 字符数
    b = s.encode("utf-8")
    print(">>>", b, f"len={len(b)}")
    print(">>>", b.decode("utf-8"))
    print("\n" + "*" * 80)
    test_encode_error()
