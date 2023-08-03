"""
Use this script to generate the constants in ec.static.py and hardness_dlog.py.
"""

from ec.core import ONE_POINT, ZERO_POINT, NUMBER_POINTS, MAX_COORDINATE, PARAMETER_A, PARAMETER_B
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

patterns = (
    lambda x: f"NUMBER_POINTS = {x}",
    lambda x: f"XY = {x}",
)
updated_values = (NUMBER_POINTS, xy)

meta.update_variables(os.path.join("ec", "static.py"), patterns, updated_values)

patterns = (
    lambda x: f"MAX_COORDINATE = {x}",
    lambda x: f"PARAMETER_A = {x}",
    lambda x: f"PARAMETER_B = {x}",
    lambda x: f"NUMBER_POINTS = {x}",
    lambda x: f"XY = {x}",
)
updated_values = (MAX_COORDINATE, PARAMETER_A.value, PARAMETER_B.value, NUMBER_POINTS, xy)

meta.update_variables("hardness_dlog.py", patterns, updated_values)
