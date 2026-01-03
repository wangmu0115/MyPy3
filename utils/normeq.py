"""Normalizing Unicode for reliable comparisons."""

from unicodedata import combining, normalize


def nfc_equal(unistr1: str, unistr2: str) -> bool:
    """使用 NFC 规范化形式比较，区分大小写"""
    if unistr1 is None or unistr2 is None:
        raise ValueError("Comparison strings cannot be None.")
    return normalize("NFC", unistr1) == normalize("NFC", unistr2)


def fold_equal(unistr1: str, unistr2: str) -> bool:
    """用 NFC 规范化形式比较，大小写同一化"""
    if unistr1 is None or unistr2 is None:
        raise ValueError("Comparison strings cannot be None.")
    return normalize("NFC", unistr1).casefold() == normalize("NFC", unistr2).casefold()


def shave_marks(txt):
    """删除所有变音符"""
    norm_txt = normalize("NFD", txt)  # Decompose all characters into base character and combining mark.
    shaved = "".join(ch for ch in norm_txt if not combining(ch))
    return normalize("NFC", shaved)


if __name__ == "__main__":
    print("\n" + "=" * 40, "shave_marks", "=" * 40)
    order = 'Herr Voß: • ½ cup of OEtker™ caffè latte • bowl of açaí."'
    print(">>>", shave_marks(order))
    greek = "Ζέφυρος, Zéfiro"
    print(">>>", shave_marks(greek))
    print("\n" + "=" * 40, "shave_marks", "=" * 40)
