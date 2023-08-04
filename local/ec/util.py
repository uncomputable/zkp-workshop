from typing import Tuple
import unittest

# Use this in conjunction with ec.core
# from ec.core import Scalar, AffinePoint, ONE_POINT, random_scalar, random_point
# Point = AffinePoint

# Use this in conjunction with ec.static
from local.ec.static import Scalar, CurvePoint, ONE_POINT, random_scalar, random_point
Point = CurvePoint


class Opening:
    """
    Opening of a cryptographic commitment to a value.
    """
    v: Scalar
    """
    Contained value
    """
    r: Scalar
    """
    Blinding factor
    """
    g: Point
    """
    Generator for value
    """
    h: Point
    """
    Generator for blinding factor

    **Both generators must be independent from each other!**
    """

    def __init__(self, v: Scalar, g: Point, h: Point):
        self.v = v
        self.g = g
        self.r = random_scalar()
        self.h = h

    def __repr__(self) -> str:
        return "{}: {}".format(self.value(), self.close())

    def value(self) -> Scalar:
        return self.v

    def close(self) -> Point:
        """
        Return the commitment that corresponds to the opening.
        """
        return self.r * self.h + self.v * self.g

    def verify(self, commitment: Point) -> bool:
        """
        Return whether the given commitment corresponds to this opening.
        """
        return commitment == self.close()

    def serialize(self) -> Tuple[Scalar, Scalar]:
        """
        Serialize the opening as it would be broadcast in an interactive proof.
        """
        return self.v, self.r


class TestOpening(unittest.TestCase):
    def test_hiding(self):
        one_point = ONE_POINT
        punto_uno = random_point()

        v = Scalar(2)
        c1 = Opening(v, one_point, punto_uno)
        c2 = Opening(v, one_point, punto_uno)

        self.assertNotEquals(c1.close(), c2.close())
