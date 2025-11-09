from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any


class ObjectType(StrEnum):
    INTEGER = "Integer"
    BOOLEAN = "Boolean"
    NULL = "Null"


class Object(ABC):
    def __init__(self, value: Any):
        self._value = value

    @property
    @abstractmethod
    def type(self) -> ObjectType: ...

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any):
        self._value = new_value

    def __str__(self):
        return f"{self.type}({self.value})"

    def __repr__(self):
        return f"{self.__class__.__name__}(value={repr(self.value)})"


class Integer(Object):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Integer value must be int.")
        super().__init__(value)

    @property
    def type(self):
        return ObjectType.INTEGER


class Boolean(Object):
    def __init__(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Boolean value must be boolean.")
        super().__init__(value)

    @property
    def type(self):
        return ObjectType.BOOLEAN


class Null(Object):
    def __init__(self):
        super().__init__(None)

    @property
    def type(self):
        return ObjectType.NULL
