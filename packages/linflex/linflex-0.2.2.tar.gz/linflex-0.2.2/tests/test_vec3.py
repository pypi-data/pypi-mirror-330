from math import isclose, pi

from linflex import Vec3


def test_initialization():
    v = Vec3(1, 2, 3)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3


def test_constants():
    assert Vec3.ZERO == Vec3(0, 0, 0)
    assert Vec3.ONE == Vec3(1, 1, 1)
    assert Vec3.INF == Vec3(float("inf"), float("inf"), float("inf"))
    assert Vec3.LEFT == Vec3(-1, 0, 0)
    assert Vec3.RIGHT == Vec3(1, 0, 0)
    assert Vec3.UP == Vec3(0, 1, 0)
    assert Vec3.DOWN == Vec3(0, -1, 0)
    assert Vec3.FORWARD == Vec3(0, 0, 1)
    assert Vec3.BACK == Vec3(0, 0, -1)
    # Constants should generate a new unique instance each time to avoid mutation
    assert Vec3.ZERO is not Vec3.ZERO
    assert Vec3.ONE is not Vec3.ONE
    assert Vec3.INF is not Vec3.INF
    assert Vec3.LEFT is not Vec3.LEFT
    assert Vec3.RIGHT is not Vec3.RIGHT
    assert Vec3.UP is not Vec3.UP
    assert Vec3.DOWN is not Vec3.DOWN
    assert Vec3.FORWARD is not Vec3.FORWARD
    assert Vec3.BACK is not Vec3.BACK


def test_default():
    v = Vec3()
    assert v.x == 0
    assert v.y == 0
    assert v.z == 0


def test_addition():
    v1 = Vec3(1, 2, 3)
    v2 = Vec3(4, 5, 6)
    v3 = v1 + v2
    assert v3.x == 5
    assert v3.y == 7
    assert v3.z == 9


def test_subtraction():
    v1 = Vec3(5, 6, 7)
    v2 = Vec3(1, 2, 3)
    v3 = v1 - v2
    assert v3.x == 4
    assert v3.y == 4
    assert v3.z == 4


def test_multiplication():
    v1 = Vec3(1, 2, 3)
    v2 = v1 * 2
    assert v2.x == 2
    assert v2.y == 4
    assert v2.z == 6


def test_division():
    v1 = Vec3(6, 8, 10)
    v2 = v1 / 2
    assert v2.x == 3
    assert v2.y == 4
    assert v2.z == 5


def test_dot_product():
    v1 = Vec3(1, 2, 3)
    v2 = Vec3(4, 5, 6)
    assert isclose(v1.dot(v2), 32)


def test_cross_product():
    v1 = Vec3(1, 2, 3)
    v2 = Vec3(4, 5, 6)
    cross = v1.cross(v2)
    assert cross.x == -3
    assert cross.y == 6
    assert cross.z == -3


def test_length():
    v = Vec3(3, 4, 0)
    assert isclose(v.length(), 5)


def test_normalized():
    v = Vec3(3, 4, 0)
    norm = v.normalized()
    assert isclose(norm.length(), 1)
    assert isclose(norm.x, 0.6)
    assert isclose(norm.y, 0.8)


def test_lerp():
    v1 = Vec3(1, 1, 1)
    v2 = Vec3(2, 2, 2)
    v3 = v1.lerp(v2, 0.5)
    assert v3.x == 1.5
    assert v3.y == 1.5
    assert v3.z == 1.5


def test_copy():
    v1 = Vec3(1, 2, 3)
    v2 = v1.copy()
    assert v1 == v2


def test_clamped():
    v = Vec3(10, 15, 20)
    min_vec = Vec3(5, 5, 5)
    max_vec = Vec3(10, 10, 10)
    clamped = v.clamped(min_vec, max_vec)
    assert clamped == Vec3(10, 10, 10)


# Test rotation methods
def test_rotation():
    v = Vec3(1, 0, 0)
    angle = pi / 2  # 90 degrees in radians
    rotated = v.rotated_around_z(angle)
    assert isclose(rotated.x, 0, abs_tol=1e-9)
    assert isclose(rotated.y, 1, abs_tol=1e-9)


# Test equality methods
def test_equality():
    v1 = Vec3(1, 2, 3)
    v2 = Vec3(1, 2, 3)
    assert v1 == v2


def test_inequality():
    v1 = Vec3(1, 2, 3)
    v2 = Vec3(4, 5, 6)
    assert v1 != v2
