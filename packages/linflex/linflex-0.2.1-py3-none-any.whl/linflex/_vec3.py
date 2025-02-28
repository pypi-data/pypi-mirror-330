from __future__ import annotations

from math import sqrt, cos, sin, atan2, inf as INF
from typing import Iterator, Literal

from typing_extensions import Self

from ._numerical_tools import lerp, sign, clamp
from ._class_constant import class_constant
from ._annotations import Radians


class Vec3:
    """`Vector3` data structure

    Components: `x`, `y`, `z`

    Usefull for storing position or direction in 3D space
    """

    __slots__ = ("x", "y", "z")

    @class_constant
    def ZERO(cls: type[Self]) -> Self:  # type: ignore
        """Zero vector, a vector with all components set to `0`"""
        return cls(0, 0, 0)

    @class_constant
    def ONE(cls: type[Self]) -> Self:  # type: ignore
        """One vector, a vector with all components set to `1`"""
        return cls(1, 1, 1)

    @class_constant
    def INF(cls: type[Self]) -> Self:  # type: ignore
        """Infinity vector, a vector with all components set to `math.inf`"""
        return cls(INF, INF, INF)

    @class_constant
    def LEFT(cls: type[Self]) -> Self:  # type: ignore
        """Left unit vector. Represents the local direction of left, and the global direction of west"""
        return cls(-1, 0, 0)

    @class_constant
    def RIGHT(cls: type[Self]) -> Self:  # type: ignore
        """Right unit vector. Represents the local direction of right, and the global direction of east"""
        return cls(1, 0, 0)

    @class_constant
    def UP(cls: type[Self]) -> Self:  # type: ignore
        """Up unit vector"""
        return cls(0, 1, 0)

    @class_constant
    def DOWN(cls: type[Self]) -> Self:  # type: ignore
        """Down unit vector"""
        return cls(0, -1, 0)

    @class_constant
    def FORWARD(cls: type[Self]) -> Self:  # type: ignore
        """Forward unit vector. Represents the local direction of forward, and the global direction of north"""
        return cls(0, 0, 1)

    @class_constant
    def BACK(cls: type[Self]) -> Self:  # type: ignore
        """Back unit vector. Represents the local direction of back, and the global direction of south"""
        return cls(0, 0, -1)

    @classmethod
    def from_angles(cls, angles: Vec3, /) -> Self:
        """Creates a direction vector of length 1 from given angle

        Args:
            angles (Vec3): vector representing rotation around each axis (x, y, z)

        Returns:
            Self: direction vector of length 1
        """
        x_cos = cos(angles.x)
        y_cos = cos(angles.y)
        z_cos = cos(angles.z)

        x_sin = sin(angles.x)
        y_sin = sin(angles.y)
        z_sin = sin(angles.z)

        x = y_cos * z_cos
        y = x_sin * y_sin * z_cos + x_cos * z_sin
        z = x_cos * y_sin * z_cos - x_sin * z_sin

        return cls(x, y, z)

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, /) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __reduce__(self) -> tuple[type[Self], tuple[float, float]]:
        return (self.__class__, (self.x, self.y))

    def __len__(self) -> Literal[3]:
        return 3

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y, self.z))

    def __getitem__(self, item: Literal[0, 1, 2]) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        raise ValueError(f"item '{item}' does not correspond to x or y or z axis")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __bool__(self) -> bool:
        """Returns whether x or y is not zero

        Returns:
            bool: truthiness
        """
        return bool(self.x or self.y or self.z)

    def __abs__(self) -> Self:
        return self.__class__(abs(self.x), abs(self.y))

    def __round__(self, ndigits: int = 0) -> Self:
        return self.__class__(
            round(self.x, ndigits),
            round(self.y, ndigits),
            round(self.z, ndigits),
        )

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __iadd__(self, other: Vec3) -> Vec3:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __isub__(self, other: Vec3) -> Vec3:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z,
            )
        return Vec3(
            self.x * other,
            self.y * other,
            self.z * other,
        )

    def __imul__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        else:
            self.x *= other
            self.y *= other
            self.z *= other
        return self

    def __floordiv__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:  # Any x, y, z == 0
                return Vec3.ZERO
            return Vec3(
                self.x // other.x,
                self.y // other.y,
                self.z // other.z,
            )
        return Vec3(
            self.x // other,
            self.y // other,
            self.z // other,
        )

    def __ifloordiv__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:  # Any x, y, z == 0
                return Vec3.ZERO
            self.x //= other.x
            self.y //= other.y
            self.z //= other.z
        else:
            self.x //= other
            self.y //= other
            self.z //= other
        return self

    def __truediv__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:  # any x, y, z == 0
                return Vec3.ZERO
            return Vec3(
                self.x / other.x,
                self.y / other.y,
                self.z / other.z,
            )
        return Vec3(
            self.x / other,
            self.y / other,
            self.z / other,
        )

    def __itruediv__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:  # Any x, y, z == 0
                return Vec3(0, 0, 0)
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        else:
            self.x /= other
            self.y /= other
            self.z /= other
        return self

    def __mod__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(
                self.x % other.x,
                self.y % other.y,
                self.z % other.z,
            )
        return Vec3(
            self.x % other,
            self.y % other,
            self.z % other,
        )

    def __imod__(self, other: Vec3 | int | float) -> Vec3:
        if isinstance(other, Vec3):
            self.x %= other.x
            self.y %= other.y
            self.z %= other.z
        else:
            self.x %= other
            self.y %= other
            self.z %= other
        return self

    def __eq__(self, other: Vec3) -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other: Vec3) -> bool:
        return (self.x != other.x) or (self.y != other.y) and (self.z != other.z)

    def __gt__(self, other: Vec3) -> bool:
        return (self.x > other.x) and (self.y > other.y) and (self.z > other.z)

    def __lt__(self, other: Vec3) -> bool:
        return (self.x < other.x) and (self.y < other.y) and (self.z < other.z)

    def __ge__(self, other: Vec3) -> bool:
        return (self.x >= other.x) and (self.y >= other.y) and (self.z >= other.z)

    def __le__(self, other: Vec3) -> bool:
        return (self.x <= other.x) and (self.y <= other.y) and (self.z <= other.z)

    def __copy__(self) -> Self:
        return self.__class__(self.x, self.y, self.z)

    def __deepcopy__(self, _memo) -> Self:
        return self.__class__(self.x, self.y, self.z)

    def copy(self) -> Self:
        return self.__copy__()

    def length(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalized(self) -> Vec3:
        length = self.length()
        if length == 0:
            return Vec3.ZERO
        return Vec3(
            self.x / length,
            self.y / length,
            self.z / length,
        )

    def lerp(self, target: Vec3, /, weight: float) -> Vec3:
        return Vec3(
            lerp(self.x, target.x, weight),
            lerp(self.y, target.y, weight),
            lerp(self.z, target.z, weight),
        )

    def sign(self) -> Vec3:
        return Vec3(
            sign(self.x),
            sign(self.y),
            sign(self.z),
        )

    def clamped(self, smallest: Vec3, /, largest: Vec3) -> Vec3:
        return Vec3(
            clamp(self.x, smallest.x, largest.x),
            clamp(self.y, smallest.y, largest.y),
            clamp(self.z, smallest.z, largest.z),
        )

    def distance_to(self, target: Vec3, /) -> float:
        return (target - self).length()

    def distance_squared_to(self, target: Vec3, /) -> float:
        return (target - self).length_squared()

    def direction_to(self, target: Vec3, /) -> Vec3:
        return (target - self).normalized()

    def dot(self, other: Vec3, /) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3, /) -> Vec3:
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vec3(x, y, z)

    def angles(self) -> Vec3:
        xy_length = sqrt(self.x * self.x + self.y * self.y)
        pitch = atan2(self.z, xy_length)
        yaw = atan2(self.y, self.x)
        return Vec3(pitch, yaw, 0)

    def angles_to(self, target: Vec3, /) -> Vec3:
        return (target - self).angles()

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def rotated_around_x(self, angle: float, /) -> Vec3:
        new_y = self.y * cos(angle) - self.z * sin(angle)
        new_z = self.y * sin(angle) + self.z * cos(angle)
        return Vec3(self.x, new_y, new_z)

    def rotated_around_y(self, angle: float, /) -> Vec3:
        new_x = self.x * cos(angle) + self.z * sin(angle)
        new_z = -self.x * sin(angle) + self.z * cos(angle)
        return Vec3(new_x, self.y, new_z)

    def rotated_around_z(self, angle: float, /) -> Vec3:
        new_x = self.x * cos(angle) - self.y * sin(angle)
        new_y = self.x * sin(angle) + self.y * cos(angle)
        return Vec3(new_x, new_y, self.z)

    def rotated(self, angles: Vec3, /) -> Vec3:
        return (
            self.rotated_around_x(angles.x)
            .rotated_around_y(angles.y)
            .rotated_around_z(angles.z)
        )

    def rotated_around(self, target: Vec3, /, angles: Vec3) -> Vec3:
        rel = self - target
        rotated_rel = (
            rel.rotated_around_x(angles.x)
            .rotated_around_y(angles.y)
            .rotated_around_z(angles.z)
        )
        return rotated_rel + target
