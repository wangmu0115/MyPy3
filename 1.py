print(round(3.4), round(3.5), round(3.6))

print(round(4.4), round(4.5), round(4.6))

import math
import numbers

print(math.trunc(-3.4), math.trunc(3.4))
print(math.ceil(-3.4), math.ceil(3.4))
print(math.floor(-3.4), math.floor(3.4))


class Data:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        if not isinstance(other, numbers.Number) and not isinstance(other, type(self)):
            raise TypeError(f"{type(other)}")
        _othervalue = other.value if isinstance(other, Data) else other
        if self.value < _othervalue:
            return True
        else:
            return False

    def __index__(self):
        return int(self.value)


d1 = Data(10.5)
d2 = Data(12)
print(d1 < d2)
print(bin(d1))
