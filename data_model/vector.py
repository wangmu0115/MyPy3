import reprlib
from array import array


class Vector:
    typecode = "d"

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        return f"Vector({components[components.find('[') : components.find(']') + 1]})"

    def __str__(self):
        return str(tuple(self._components))


if __name__ == "__main__":
    v1 = Vector([3.1, 4.2])
    v2 = Vector((3, 4, 5))
    v3 = Vector(range(10))

    print(">>>", v1)
    print(">>>", v2)
    print(">>>", v3)
