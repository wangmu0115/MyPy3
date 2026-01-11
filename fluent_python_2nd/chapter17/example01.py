class Spam:
    def __getitem__(self, index):
        print("->", index)
        raise IndexError()


if __name__ == "__main__":
    spam = Spam()
    print(iter(spam))
    print(list(spam))
    for i in spam:
        print(i)
    print(spam[0])
