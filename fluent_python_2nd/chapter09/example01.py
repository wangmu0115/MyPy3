def deco(func):
    def inner():
        print("Running inner.")

    return inner


@deco
def target():
    print("Running target.")


if __name__ == "__main__":
    target()
    print(target)
