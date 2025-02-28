# Linflex

A linear algebra package written in Python

## Installation

Install using either `pip` or `rye`:

```bash
pip install linflex
```

```bash
rye add linflex
```

## Getting started

```python
from linflex import Vec2

a = Vec2(3, 4)
b = Vec2(2, -1)

assert a + b == Vec2(5, 3)
assert a - b == Vec2(1, 5)
assert a.length() == 5
assert -Vec2(2, -3) == Vec2(-2, 3)

c = Vec2(1, 1)
c += Vec2(0, 1)
assert c == Vec2(1, 2)
```

## Rational

`linflex` was created to fill the need for a common `Vec2` class accross my projects and packages. It is lightweight, as it only depends on `typing-extensions`. Aside from linear algebra, I also needed helper functions like `lerp`, `sign` and `clamp`, which was put into good use by `<Vec2>.lerp`, and alike.

## Includes

- Functions
  - `lerp`
  - `sign`
  - `clamp`
- Datastructures
  - `Vec2`
  - `Vec2i`
  - `Vec3`

## License

MIT
