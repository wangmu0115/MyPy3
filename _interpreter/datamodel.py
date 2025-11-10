from abc import ABC, abstractmethod
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Callable, Type

from _interpreter.ast import BlockStatement, IdenExpression

if TYPE_CHECKING:
    from _interpreter.environment import Env


class ObjectType(StrEnum):
    INTEGER = "Integer"
    BOOLEAN = "Boolean"
    STRING = "String"
    NULL = "Null"

    RETURN = "ReturnObj"
    FUNCTION = "FunctionObj"

    BUILTINCALL = "BuiltinCallableObj"


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


class String(Object):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("String value must be text.")
        super().__init__(value)

    @property
    def type(self):
        return ObjectType.STRING


class Null(Object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__(None)

    @property
    def type(self):
        return ObjectType.NULL


class ReturnObj(Object):
    def __init__(self, obj: Object):
        super().__init__(obj)

    @property
    def type(self):
        return ObjectType.RETURN


class FunctionObj(Object):
    def __init__(self, parameters: list[IdenExpression], body: BlockStatement, env: "Env"):
        super().__init__(None)
        self.__parameters = parameters
        self.__body = body
        self.__env = env

    @property
    def type(self):
        return ObjectType.FUNCTION

    @property
    def params(self):
        return self.parameters

    @property
    def parameters(self):
        return self.__parameters

    @property
    def body(self):
        return self.__body

    @property
    def env(self):
        return self.__env


class BuiltinCallable(Object):
    def __init__(self, callable: Type[Callable]):
        super().__init__(callable.__name__)
        self.__callable = callable

    @property
    def type(self):
        return ObjectType.BUILTINCALL

    @property
    def callable(self):
        return self.__callable

    @property
    def call(self):
        return self.callable


class DataModelSystem:
    @classmethod
    def from_value(cls, value: Any) -> Object:
        if value is None:
            return Null()
        match value:
            case int():
                return Integer(value)
            case bool():
                return Boolean(value)
            case _:
                raise ValueError(f"Unsupported value type: {type(value)}({value})")
