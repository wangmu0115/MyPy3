from _builtins.pprint import console_print


def make_averager():
    series = []
    size = 0

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        nonlocal size
        size = len(series)
        return total / size

    return averager


# python -m fluent_python_2nd.chapter09.average
if __name__ == "__main__":
    avg = make_averager()
    console_print(avg(10))
    console_print(avg(11))
    console_print(avg(12))
    print(avg.__code__.co_varnames)
    print(avg.__code__.co_freevars)
    for name, value_cell in zip(avg.__code__.co_freevars, avg.__closure__):
        print(f"{name}: {value_cell.cell_contents}")
