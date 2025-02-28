from math import isclose, pi as PI

from linflex import Vec2i


DIAGONAL_LENGTH = Vec2i(1, 1).length()  # ~1.414


def test_from_angle():
    v1 = Vec2i.from_angle(PI)
    assert isclose(v1.length(), 1)
    assert v1.x == -1 and v1.y == 0
    v2 = Vec2i.from_angle(PI / 2)
    assert isclose(v2.length(), 1)
    assert v2.x == 0 and v2.y == 1
    # Angles that lays *in* a quadrant
    v3 = Vec2i.from_angle(PI / 8)
    assert isclose(v3.length(), DIAGONAL_LENGTH)
    assert v3.x == 1 and v3.y == 1
    v4 = Vec2i.from_angle(-PI / 8)
    assert isclose(v4.length(), DIAGONAL_LENGTH)
    assert v4.x == 1 and v4.y == -1
