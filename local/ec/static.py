import random
from typing import Tuple, Union

NUMBER_POINTS = 13


class CurvePoint:
    """
    A point on the curve.

    In contrast to AffinePoint, this point is guaranteed to be on the curve.
    Arbitrary points in affine space are not supported.
    """
    n: int
    """
    Number of the point (aka its discrete logarithm).
    """

    def __init__(self, n: int):
        self.n = n

    def xy(self) -> Tuple[int, int]:
        """
        Return the xy coordinates of the point in affine space.
        """
        return XY[self.n]

    def __repr__(self) -> str:
        if self.is_zero():
            return "(zero)"
        else:
            return repr(self.xy())

    def __hash__(self) -> hash:
        return hash(self.n)

    def __eq__(self, other: "CurvePoint") -> bool:
        return self.n == other.n

    def is_zero(self) -> bool:
        """
        Return whether the point is zero.
        """
        return self.n == 0

    def __add__(self, other: "CurvePoint") -> "CurvePoint":
        return CurvePoint((self.n + other.n) % NUMBER_POINTS)

    def __neg__(self) -> "CurvePoint":
        return CurvePoint(-self.n % NUMBER_POINTS)

    def __sub__(self, other: "CurvePoint") -> "CurvePoint":
        return CurvePoint((self.n - other.n) % NUMBER_POINTS)

    def discrete_log(self) -> "Scalar":
        """
        Return the discrete logarithm of the point.

        This is a scalar n such that n * One = self.
        """
        return Scalar(self.n)


ZERO_POINT = CurvePoint(0)
"""
Zero point. That is the zeroth point on the curve or the point with a discrete logarithm of zero.

The zero point is always the same.
"""
ONE_POINT = CurvePoint(1)
"""
One point. That is the first point on the curve or the point with a discrete logarithm of one.

Note that the choice of the one point is arbitrary.
On our particular curve, every non-zero point could be the one point.
The other points are numbered according to how many times the one point was added onto itself to arrive at that point.

The static EC module has a hardcoded one point.
"""


class Scalar:
    """
    Scalar of the curve.

    That is an integer modulo the number of points.
    """
    n: int
    """
    Value of the scalar.
    """

    def __init__(self, n: int):
        self.n = n

    def __int__(self) -> int:
        return self.n

    def __repr__(self) -> str:
        return repr(self.n)

    def __hash__(self) -> hash:
        return hash(self.n)

    def __eq__(self, other: "CurvePoint") -> bool:
        return self.n == other.n

    def __add__(self, other: "Scalar") -> "Scalar":
        return Scalar((self.n + other.n) % NUMBER_POINTS)

    def __neg__(self) -> "Scalar":
        return Scalar(-self.n % NUMBER_POINTS)

    def __sub__(self, other: "Scalar") -> "Scalar":
        return Scalar((self.n - other.n) % NUMBER_POINTS)

    def __mul__(self, other):
        ret = (self.n * other.n) % NUMBER_POINTS

        if isinstance(other, CurvePoint):
            return CurvePoint(ret)
        else:
            return Scalar(ret)

    def reciprocal(self) -> "Scalar":
        """
        Return the multiplicative inverse of the scalar.

        This is a scalar i such that self * i = 1.
        """
        return Scalar(pow(self.n, -1, NUMBER_POINTS))

    def __truediv__(self, other: "Scalar") -> "Scalar":
        return self * other.reciprocal()

    def __pow__(self, power: Union[int, "Scalar"]) -> "Scalar":
        if isinstance(power, Scalar):
            power = power.n
        return Scalar(pow(self.n, power, NUMBER_POINTS))


XY = (None, (4, 2), (3, 3), (1, 2), (2, 5), (5, 3), (6, 3), (6, 4), (5, 4), (2, 2), (1, 5), (3, 4), (4, 5))
"""
List of xy coordinates of all points in order (zeroth, first, second, ...).
"""


def random_point() -> CurvePoint:
    """
    Return a uniformly random point on the curve.
    """
    return CurvePoint(random.randrange(0, NUMBER_POINTS))


def random_scalar() -> Scalar:
    """
    Return a uniformly random scalar.
    """
    return Scalar(random.randrange(0, NUMBER_POINTS))
