if __name__ == "__main__":
    for codec in ["latin_1", "utf_8", "utf_16"]:
        print(codec, "El Niño".encode(encoding=codec), sep="\t")
    UnicodeError
    SyntaxError