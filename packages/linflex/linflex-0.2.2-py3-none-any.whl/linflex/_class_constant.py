from typing import TypeVar


T = TypeVar("T")


# TODO: Add the remaining annotations
class class_constant:
    def __init__(self, method) -> None:
        self.fget = method

    def __get__(self, _instance, owner: type[T]) -> T:
        return self.fget(owner)
