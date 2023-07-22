"""
Use this script to generate the constants in ec.static.py.
"""

from core import ONE_POINT, ZERO_POINT
from typing import List, Optional, Tuple

IntPoint = Optional[Tuple[int, int]]


def point_xy() -> List[IntPoint]:
    current = ZERO_POINT
    xy = []

    while True:
        if current.is_zero():
            xy.append(None)
        else:
            xy.append((current.x.value, current.y.value))
        current += ONE_POINT

        if current == ZERO_POINT:
            break

    return xy


xy = ", ".join(["{}".format(xy) for xy in point_xy()])
print("XY = ({})".format(xy))
