from math import isclose, pi as PI

from linflex import Vec2


def test_initialization():
    v = Vec2(3, 4)
    assert v.x == 3
    assert v.y == 4


def test_constants():
    assert Vec2.ZERO == Vec2(0, 0)
    assert Vec2.ONE == Vec2(1, 1)
    assert Vec2.INF == Vec2(float("inf"), float("inf"))
    assert Vec2.LEFT == Vec2(-1, 0)
    assert Vec2.RIGHT == Vec2(1, 0)
    assert Vec2.UP == Vec2(0, -1)
    assert Vec2.DOWN == Vec2(0, 1)
    # Constants should generate a new unique instance each time to avoid mutation
    assert Vec2.ZERO is not Vec2.ZERO
    assert Vec2.ONE is not Vec2.ONE
    assert Vec2.INF is not Vec2.INF
    assert Vec2.LEFT is not Vec2.LEFT
    assert Vec2.RIGHT is not Vec2.RIGHT
    assert Vec2.UP is not Vec2.UP
    assert Vec2.DOWN is not Vec2.DOWN


def test_from_angle():
    v1 = Vec2.from_angle(PI)
    assert isclose(v1.length(), 1)
    assert isclose(v1.x, -1) and isclose(v1.y, 0, abs_tol=1e-9)
    v2 = Vec2.from_angle(PI / 2)
    assert isclose(v2.length(), 1)
    assert isclose(v2.x, 0, abs_tol=1e-9) and isclose(v2.y, 1)


def test_addition():
    v1 = Vec2(1, 2)
    v2 = Vec2(3, 4)
    assert v1 + v2 == Vec2(4, 6)


def test_subtraction():
    v1 = Vec2(5, 6)
    v2 = Vec2(3, 2)
    assert v1 - v2 == Vec2(2, 4)


def test_multiplication():
    v = Vec2(2, 3)
    assert v * 2 == Vec2(4, 6)
    assert v * Vec2(2, 3) == Vec2(4, 9)


def test_division():
    v = Vec2(8, 6)
    assert v / 2 == Vec2(4, 3)
    assert v / Vec2(2, 3) == Vec2(4, 2)


def test_length():
    v = Vec2(3, 4)
    assert v.length() == 5


def test_normalized():
    v = Vec2(3, 4).normalized()
    assert isclose(v.length(), 1)


def test_dot_product():
    v1 = Vec2(1, 2)
    v2 = Vec2(3, 4)
    assert v1.dot(v2) == 11


def test_cross_product():
    v1 = Vec2(1, 2)
    v2 = Vec2(3, 4)
    assert v1.cross(v2) == -2


def test_angle():
    v = Vec2(1, 1)
    assert isclose(v.angle(), PI / 4)


def test_lerp():
    v1 = Vec2(0, 0)
    v2 = Vec2(10, 10)
    assert v1.lerp(v2, 0.5) == Vec2(5, 5)


def test_rotation():
    v = Vec2(1, 0).rotated(PI / 2)
    assert isclose(v.x, 0, abs_tol=1e-9)
    assert isclose(v.y, -1, abs_tol=1e-9)


def test_clamped():
    v = Vec2(5, 10)
    assert v.clamped(Vec2(0, 0), Vec2(4, 8)) == Vec2(4, 8)


def test_abs():
    v = Vec2(1, -2)
    assert abs(v) == Vec2(1, 2)


def test_round():
    v = Vec2(0.6, 0.29)
    assert round(v) == Vec2(1, 0)
    assert round(v, 1) == Vec2(0.6, 0.3)


def test_neg():
    v = Vec2(1, -1)
    assert -v == Vec2(-1, 1)
