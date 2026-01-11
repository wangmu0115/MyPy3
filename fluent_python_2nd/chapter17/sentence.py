import re
import reprlib

from _builtins.pprint import console_print

RE_WORD = re.compile(r"\w+")


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        cls_name = self.__class__.__name__

        return f"{cls_name}({reprlib.repr(self.text)})"


# python -m fluent_python_2nd.chapter17.sentence
if __name__ == "__main__":
    s = Sentence("'The time has come,' the Walrus said,")
    console_print(s)
    for word in s:
        console_print(word)
    console_print(list(s))
