from _builtins.pprint import console_print


class Averager:
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)

        return sum(self.series) / len(self.series)


# python -m fluent_python_2nd.chapter09.average_oo
if __name__ == "__main__":
    avg = Averager()
    console_print(avg(10))
    console_print(avg(11))
    console_print(avg(12))
