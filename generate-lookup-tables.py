"""
Use this script to generate the constants in ec.static.py.
"""

from ec.core import ONE_POINT, ZERO_POINT
from typing import List, Optional, Tuple
import meta
import os

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


xy = "({})".format(", ".join(["{}".format(xy) for xy in point_xy()]))
meta.update_variable(os.path.join("ec", "static.py"), lambda x: f"XY = {x}", xy)
