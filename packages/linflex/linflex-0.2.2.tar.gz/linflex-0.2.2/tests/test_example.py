from linflex import Vec2


def test_example():
    a = Vec2(3, 4)
    b = Vec2(2, -1)

    assert a + b == Vec2(5, 3)
    assert a - b == Vec2(1, 5)
    assert a.length() == 5
    assert -Vec2(2, -3) == Vec2(-2, 3)

    c = Vec2(1, 1)
    c += Vec2(0, 1)
    assert c == Vec2(1, 2)
