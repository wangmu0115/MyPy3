"""规范化 Unicode 字符串"""

import unicodedata


def test_ohm():
    ohm = "\u2126"
    print(f"{ohm} name>>>", unicodedata.name(ohm))
    ohm_c = unicodedata.normalize("NFC", ohm)
    print(f"{ohm_c} name>>>", unicodedata.name(ohm_c))
    print(">>>", ohm == ohm_c)
    print(">>>", unicodedata.normalize("NFC", ohm) == unicodedata.normalize("NFC", ohm_c))


if __name__ == "__main__":
    s1 = "café"
    s2 = "cafe\N{COMBINING ACUTE ACCENT}"
    print(">>>", s1, s2)
    print(">>>", len(s1), len(s2))
    print(">>>", s1 == s2)
    s1_nfc, s1_nfd = unicodedata.normalize("NFC", s1), unicodedata.normalize("NFD", s1)
    s2_nfc, s2_nfd = unicodedata.normalize("NFC", s2), unicodedata.normalize("NFD", s2)
    print("\n" + "*" * 40, "NFC", "*" * 40)
    print(">>>", s1_nfc, s2_nfc)
    print(">>>", len(s1_nfc), len(s2_nfc))
    print(">>>", s1_nfc == s2_nfc)
    print("\n" + "*" * 40, "NFD", "*" * 40)
    print(">>>", s1_nfd, s2_nfd)
    print(">>>", len(s1_nfd), len(s2_nfd))
    print(">>>", s1_nfd == s2_nfd)
    print("\n\n" + "=" * 80)
    test_ohm()
