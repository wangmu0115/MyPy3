import math
from array import array


class Vector2d:
    # Class attribute, used for convert `Vector2d` instances to/from `bytes`
    typecode = "d"

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

    def __iter__(self):  # Makes `Vector2d` iterable
        yield self.x
        yield self.y

    def __repr__(self):
        class_name = self.__class__.__name__
        return "{}({!r}, {!r})".format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        # It will also return True when comparing `Vector2d` instances
        # to other iterables holding the same numeric values(e.g., Vector2d(3, 4) == [3, 4]).
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))


if __name__ == "__main__":
    v1 = Vector2d(3, 4)
    print(">>>", v1.x, v1.y)
    x, y = v1
    print(">>>", (x, y))
    print(">>>", v1)
    print(">>>", f"{v1!r}")
    v1_clone = eval(repr(v1))
    print(">>>", v1 == v1_clone)
    print(">>> Vector2d(3, 4) == [3, 4]: ", v1 == [3, 4])
    octets = bytes(v1)
    print(">>>", f"{octets!r}")
    print(">>>", abs(v1))
    print(">>>", bool(v1), bool(Vector2d(0, 0)))
    print(">>>", hash(v1), hash(Vector2d(3.1, 4.2)))
