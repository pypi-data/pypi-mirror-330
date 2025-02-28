from __future__ import annotations

from typing import Generic, TypeVar

from widget_state import NumberState, DictState

NT = TypeVar("NT", int, float)


class PointState(DictState, Generic[NT]):
    """
    Point state that represents 2D pixel coordinates.

    It is often used for drawing.
    """

    def __init__(
        self,
        x: NT | NumberState[NT],
        y: NT | NumberState[NT],
    ):
        super().__init__()

        self.x = x if isinstance(x, NumberState) else NumberState(x)
        self.y = y if isinstance(y, NumberState) else NumberState(y)

    def __add__(self, other: NumberState | PointState[NT]) -> PointState[NT]:
        other = other if isinstance(other, PointState) else PointState(other, other)
        return PointState(self.x + other.x, self.y + other.y)

    def __sub__(self, other: NumberState | PointState[NT]) -> PointState[NT]:
        other = other if isinstance(other, PointState) else PointState(other, other)
        return PointState(self.x - other.x, self.y - other.y)

    def __mul__(self, other: NumberState | PointState[NT]) -> PointState[NT]:
        other = other if isinstance(other, PointState) else PointState(other, other)
        return PointState(self.x * other.x, self.y * other.y)


if __name__ == "__main__":
    pt1 = PointState(5.0, 3.141)
    pt2 = PointState(2.0, 2.7)

    res = pt2 * NumberState(5)
    # res = pt1 - pt2
    res.on_change(lambda _: print(f"Res: {res}"), trigger=True)
    print()

    pt2.x.value = 200
    print()
