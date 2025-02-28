from __future__ import annotations

from math import isclose, cos, sin

from typing_extensions import Self

from ._vec2 import Vec2
from ._numerical_tools import sign
from ._annotations import Radians


class Vec2i(Vec2):
    """`Vector2 integer` data structure

    Components: `x`, `y` only type `int`

    Usefull for storing whole numbers in 2D space
    """

    __slots__ = ("x", "y")

    @classmethod
    def from_angle(cls, angle: Radians, /) -> Self:
        """Creates a snapped direction vector of length 1 from given angle

        Snapping is done by taking the `sign` of each `component`.
        Formulas used: `x = sign(cos(angle))` and `y = sign(sin(angle))`

        Args:
            angle (Radians): angle in radians

        Returns:
            Self: snapped direction vector of length 1
        """
        x = cos(angle)
        if isclose(x, 0, abs_tol=1e-9):
            x_snapped = 0
        else:
            x_snapped = sign(x)

        y = sin(angle)
        if isclose(y, 0, abs_tol=1e-9):
            y_snapped = 0
        else:
            y_snapped = sign(y)

        return cls(x_snapped, y_snapped)

    def __init__(self, x: int = 0, y: int = 0, /) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x + other.x), int(self.y + other.y))
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vec2i) -> Vec2i:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x - other.x), int(self.y - other.y))
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vec2i) -> Vec2i:
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x * other.x), int(self.y * other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return Vec2(self.x * other, self.y * other)

    def __imul__(self, other: Vec2i) -> Vec2i:
        self.x *= other.x
        self.y *= other.y
        return self

    def __floordiv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(
                self.x // other.x,
                self.y // other.y,
            )
        elif isinstance(other, Vec2):
            return Vec2(
                self.x // other.x,
                self.y // other.y,
            )
        elif isinstance(other, int):
            return Vec2i(
                self.x // other,
                self.y // other,
            )
        return Vec2(
            self.x // other,
            self.y // other,
        )

    def __ifloordiv__(self, other: Vec2i) -> Vec2i:
        self.x //= other.x
        self.y //= other.y
        return self

    def __truediv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(
                int(self.x / other.x),
                int(self.y / other.y),
            )
        elif isinstance(other, Vec2):
            return Vec2(
                self.x / other.x,
                self.y / other.y,
            )
        return Vec2(
            self.x / other,
            self.y / other,
        )

    def __itruediv__(self, other: Vec2i) -> Vec2i:
        self.x /= other.x
        self.y /= other.y
        return self

    def __mod__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x % other.x), int(self.y % other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x % other.x, self.y % other.y)
        return Vec2(self.x % other, self.y % other)

    def __imod__(self, other: Vec2i) -> Vec2i:
        self.x %= other.x
        self.y %= other.y
        return self

    def __copy__(self) -> Vec2i:
        return __class__(self.x, self.y)

    def __deepcopy__(self) -> Vec2i:
        return __class__(self.x, self.y)

    def to_tuple(self) -> tuple[int, int]:
        """Converts the vector to a tuple representation

        Returns:
            tuple[int, int]: x and y as tuple
        """
        return (self.x, self.y)

    def copy(self) -> Vec2i:
        """Returns a copied Vec2i

        Returns:
            Vec2i: a new copy
        """
        return __class__(self.x, self.y)
