"""
Linflex
=======

A linear algebra package written in Python

Includes
--------

- `lerp`
- `sign`
- `clamp`
- `Vec2`
- `Vec2i`
- `Vec3`
"""

__all__ = (
    "lerp",
    "sign",
    "clamp",
    "Vec2",
    "Vec2i",
    "Vec3",
)

from ._numerical_tools import lerp, sign, clamp
from ._vec2 import Vec2
from ._vec2i import Vec2i
from ._vec3 import Vec3
