import random
from typing import Optional, Tuple, Union, List
import hashlib
import unittest

MAX_COORDINATE = 7
MINUS_ONE_COORDINATE = MAX_COORDINATE - 1


class ModInt:
    """
    Integer n modulo p, where p is prime
    """
    value: int
    modulus = None
    """
    Modulus p, should be prime
    """

    def __init__(self, value):
        self.value = value % self.modulus

    def __add__(self, other: "ModInt") -> "ModInt":
        return self.__class__(self.value + other.value)

    def __sub__(self, other: "ModInt") -> "ModInt":
        return self.__class__(self.value - other.value)

    def __neg__(self) -> "ModInt":
        return self.__class__(-self.value)

    def __mul__(self, other: "ModInt") -> "ModInt":
        return self.__class__(self.value * other.value)

    def reciprocal(self) -> "ModInt":
        """
        Return multiplicative inverse of self.

        Finds coordinate i such that self * i = 1.
        """
        return self.__class__(pow(self.value, -1, self.modulus))

    def __truediv__(self, other: "ModInt") -> "ModInt":
        return self * other.reciprocal()

    def __pow__(self, power: Union[int, "ModInt"], modulo=None) -> "ModInt":
        if isinstance(power, ModInt):
            power = power.value
        return self.__class__(pow(self.value, power, modulo))

    def __mod__(self, modulus: Union[int, "ModInt"]):
        if isinstance(modulus, ModInt):
            modulus = modulus.value
        return self.__class__(self.value % modulus)

    def __eq__(self, other: "ModInt") -> bool:
        return self.value == other.value

    def __repr__(self) -> str:
        return repr(self.value)

    def __int__(self) -> int:
        return self.value

    def __hash__(self) -> hash:
        return hash(self.value)

    @classmethod
    def nth(cls, n: int) -> "ModInt":
        """
        Return the nth modular integer.

        The integer n is internally scaled to the right size.
        """
        return cls(n)

    @classmethod
    def random(cls) -> "ModInt":
        """
        Return a uniformly random modular integer.
        """
        return cls(random.randrange(cls.modulus))

    def legendre_symbol(self) -> int:
        """
        Return the Legendre symbol. Also known as Euler's criterion.

        Returns 1 if self is a quadratic residue modulo p (and self != 0).
        Return -1 (modulo p) if self is a quadratic nonresidue modulo p.
        Returns 0 if self is = 0.

        https://en.wikipedia.org/wiki/Legendre_symbol
        https://en.wikipedia.org/wiki/Euler%27s_criterion
        """
        return (self ** ((self.modulus - 1) // 2)).value

    def sqrt(self) -> Optional["ModInt"]:
        """
        Return the square root of self.

        Finds coordinate r such that r^2 = self.
        About half of all coordinates have square roots.
        If r is a solution, then -r is another solution.

        Uses the Tonelli–Shanks algorithm.

        https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm
        """
        # Easy cases
        if self.value == 0:
            return self.__class__(0)
        if self.modulus == 2:
            return self
        if self.legendre_symbol() != 1:
            return None
        # This is the case for secp256k1
        if self.modulus % 4 == 3:
            return self ** ((self.modulus + 1) // 4)

        # Factor out powers of 2 to find q and s
        # such that p - 1 = q * 2^s with q odd
        q, s = self.modulus - 1, 0
        while q % 2 == 0:
            s += 1
            q //= 2
        assert q > 0
        assert q % 2 == 1

        # Search for z that is quadratic nonresidue
        # Half of all coordinates are quadratic nonresidues
        z = self.__class__(1)
        while z.legendre_symbol() + 1 != self.modulus:
            z.value += 1

        m = s
        c = z ** q
        t = self ** q
        r = self ** ((q + 1) // 2)

        while t.value != 1:
            # Use repeated squaring to find least 0 < i < m
            # such that t^(2^i) = 1
            i, e = 0, 2
            for i in range(1, m):
                if (t ** e).value == 1:
                    break
                e *= 2

            b = c ** (2 ** (m - i - 1))
            m = i
            c = b ** 2
            t = t * b ** 2
            r = r * b

        return r


class Coordinate(ModInt):
    """
    Coordinate of curve point
    """
    modulus = MAX_COORDINATE

    def lift_x(self) -> Optional["AffinePoint"]:
        """
        Return curve point that corresponds to given x coordinate, if such point exists.
        """
        # y^2 = x^3 + a * x + b
        y_squared = self ** 3 + PARAMETER_A * self + PARAMETER_B
        # y_squared may or may not have a square root
        y = y_squared.sqrt()
        if y is None or y ** 2 != y_squared:
            return None
        return AffinePoint(self, y)


PARAMETER_A = Coordinate(0)
PARAMETER_B = Coordinate(3)


class TestCoordinate(unittest.TestCase):
    def test_modulo(self):
        x = random.randrange(MAX_COORDINATE)
        self.assertEqual(Coordinate(x) + Coordinate(MAX_COORDINATE - x), Coordinate(0))

    def test_inverse(self):
        x = random.randrange(MAX_COORDINATE)
        self.assertEqual(Coordinate(x) * Coordinate(x).reciprocal(), Coordinate(1))

    def test_pow(self):
        x = Coordinate(random.randrange(MAX_COORDINATE))
        self.assertEqual(x * x * x, x ** 3)

    def test_legendre_symbol(self):
        for x in range(MAX_COORDINATE):
            x = Coordinate(x)
            ls = x.legendre_symbol()
            self.assertTrue(ls == MINUS_ONE_COORDINATE or ls == 0 or ls == 1)

    def test_sqrt(self):
        for x in range(MAX_COORDINATE):
            y_squared = Coordinate(x)
            y = y_squared.sqrt()

            if y is not None:
                self.assertEqual(y ** 2, y_squared)


class AffinePoint:
    """
    Curve point in affine space.
    """
    x: Optional[Coordinate]
    y: Optional[Coordinate]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        if self.is_zero():
            return "(zero)"
        else:
            return repr(self.xy())

    def __hash__(self) -> hash:
        return hash((self.x, self.y))

    def is_zero(self) -> bool:
        """
        Return whether self is the zero-point.
        """
        return self.x is None

    def is_on_curve(self) -> bool:
        """
        Return whether self is on the curve.

        The curve is given by the equation `y^2 = x^3 + a * x + b`
        for some parameters a and b.
        Points have to satisfy this equation to be on the curve.
        """
        return self.is_zero() or self.y ** 2 == self.x ** 3 + PARAMETER_A * self.x + PARAMETER_B

    def xy(self) -> Optional[Tuple[Coordinate, Coordinate]]:
        """
        Return x and y coordinates of self, if they exist.

        The zero-point has no coordinates.
        """
        if self.is_zero():
            return None
        return self.x, self.y

    def __eq__(self, other: "AffinePoint") -> bool:
        if self.is_zero() and other.is_zero():
            return True
        if self.is_zero() or other.is_zero():
            return False
        return self.x == other.x and self.y == other.y

    def double(self) -> "AffinePoint":
        """
        Return self + self (point doubling).

        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_doubling
        """
        # Zero + Zero = Zero
        if self.is_zero():
            return ZERO_POINT
        # self = -self:
        # self + (-self) = Zero
        if self.y.value == 0:
            return ZERO_POINT

        s = (Coordinate(3) * self.x * self.x + PARAMETER_A) / (Coordinate(2) * self.y)
        x = s * s - Coordinate(2) * self.x
        y = s * (self.x - x) - self.y

        return AffinePoint(x, y)

    def __neg__(self) -> "AffinePoint":
        """
        Return -self (point negation).

        -self is a point such that self + (-self) = Zero.
        """
        if self.is_zero():
            return self
        return AffinePoint(self.x, -self.y)

    def __add__(self, other: "AffinePoint") -> "AffinePoint":
        """
        Return self + other (point addition).

        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_addition
        """
        # Zero + other = other
        if self.is_zero():
            return other
        # self + Zero = self
        if other.is_zero():
            return self
        if self.x == other.x:
            # Double point since s (below) would be division by zero
            if self.y == other.y:
                return self.double()
            # self + (-self) = Zero
            else:
                return ZERO_POINT

        s: Coordinate = (other.y - self.y) / (other.x - self.x)
        x = s * s - self.x - other.x
        y = s * (self.x - x) - self.y

        return AffinePoint(x, y)

    def __sub__(self, other: "AffinePoint") -> "AffinePoint":
        """
        Return self - other (point subtraction).

        self - other is the same as self + (-other).
        """
        return self + -other

    def __mul__(self, scalar: "Scalar") -> Optional["AffinePoint"]:
        """
        Return scalar * self (scalar multiplication).

        Uses binary expansion (aka double and add).

        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        """
        if ONE_POINT is None:
            return None

        tmp = self
        ret = ZERO_POINT

        while scalar.value != 0:
            if scalar.value & 1 != 0:  # same as scalar.value % 2 != 0
                ret += tmp
            tmp = tmp.double()
            scalar = Scalar(scalar.value >> 1)  # same as scalar.value // 2

        return ret

    def discrete_log(self) -> Optional["Scalar"]:
        """
        Return scalar k such that self = One * k (discrete logarithm).

        Uses Pollard's rho algorithm.

        https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm_for_logarithms
        """
        if ONE_POINT is None:
            return None

        def step(p: AffinePoint, a: "Scalar", b: "Scalar") -> Tuple[AffinePoint, "Scalar", "Scalar"]:
            if p.is_zero() or p.x.value % 3 == 0:
                return p + ONE_POINT, a + Scalar(1), b
            elif p.x.value % 3 == 1:
                return p + self, a, b + Scalar(1)
            else:
                return p + p, a + a, b + b

        # Different initializations for Tortoise
        #
        # This avoids the unlikely case b1 == b2 below
        # where we cannot compute the inverse of zero
        #
        # Usually this loop will run for one iteration
        for i in range(NUMBER_POINTS):
            # Loop invariant: p_i = ONE_POINT * a_i * self * b_i
            # Tortoise (gets a head start of i steps)
            p1, a1, b1 = ONE_POINT * Scalar(i), Scalar(i), Scalar(0)
            # assert p1 == ONE_POINT * a1 + self * b1

            # Hare (starts at step 0)
            p2, a2, b2 = ONE_POINT, Scalar(1), Scalar(0)
            # assert p2 == ONE_POINT * a2 + self * b2

            # Guaranteed to halt because group is cyclic and finite
            while True:
                # Tortoise makes one step
                p1, a1, b1 = step(p1, a1, b1)
                # assert p1 == ONE_POINT * a1 + self * b1

                # Hare makes two steps
                p2, a2, b2 = step(p2, a2, b2)
                # assert p2 == ONE_POINT * a2 + self * b2
                p2, a2, b2 = step(p2, a2, b2)
                # assert p2 == ONE_POINT * a2 + self * b2

                # Hare catches up to Tortoise (in cycle)
                if p1 == p2:
                    break

            # Unlikely case where we have to try different initialization
            if b1 == b2:
                continue

            k: Scalar = (a2 - a1) * (b1 - b2).reciprocal()
            return k

        raise ArithmeticError

    @classmethod
    def nth(cls, n: int) -> "AffinePoint":
        """
        Return the n-th point on the curve.

        The integer n is internally scaled to the size of the curve.
        """
        return ONE_POINT * Scalar.nth(n)

    @classmethod
    def random(cls) -> "AffinePoint":
        """
        Return a uniformly random point on the curve.
        """
        return ONE_POINT * Scalar(random.randrange(NUMBER_POINTS))

    @classmethod
    def sample_greater_one(cls, n_sample: int) -> "List[AffinePoint]":
        """
        Randomly sample distinct points on the curve that are greater than one (not zero and not one).
        """
        return [ONE_POINT * Scalar(i) for i in random.sample(range(2, NUMBER_POINTS), n_sample)]


ZERO_POINT = AffinePoint(None, None)
"""
Zero-point
"""
NUMBER_POINTS = 13
"""
Total number of points on the curve
"""


class TestAffinePoint(unittest.TestCase):
    def test_double(self):
        points = RandomPoints()
        one = points.next()
        p = ZERO_POINT

        for _ in range(NUMBER_POINTS):
            self.assertTrue(p.is_on_curve())
            two_p = p.double()
            self.assertTrue(two_p.is_on_curve())
            self.assertEqual(two_p, p + p)

            if two_p.is_zero():
                self.assertEqual(two_p, ZERO_POINT)
            if two_p == -two_p:
                self.assertEqual(two_p, ZERO_POINT)

            p += one

        # p finished cycle through curve
        self.assertEqual(p, ZERO_POINT)

    # XXX: Expensive test
    def test_add(self):
        points = RandomPoints()
        one = points.next()
        p = ZERO_POINT

        for _ in range(NUMBER_POINTS):
            self.assertTrue(p.is_on_curve())
            q = ZERO_POINT

            for _ in range(NUMBER_POINTS):
                self.assertTrue(q.is_on_curve())
                p_plus_q = p + q
                self.assertTrue(p_plus_q.is_on_curve())

                if p.is_zero():
                    self.assertEqual(p_plus_q, q)
                if q.is_zero():
                    self.assertEqual(p_plus_q, p)
                if p == -q:
                    self.assertEqual(p_plus_q, ZERO_POINT)

                q += one

            # q finished cycle through curve
            self.assertEqual(q, ZERO_POINT)

            p += one

        # p finished cycle through curve
        self.assertEqual(p, ZERO_POINT)

    def test_negation(self):
        p = ZERO_POINT

        for _ in range(NUMBER_POINTS):
            self.assertTrue(p.is_on_curve())
            minus_p = -p
            self.assertTrue(minus_p.is_on_curve())
            self.assertEqual(p + minus_p, ZERO_POINT)

            p += ONE_POINT

        # p finished cycle through curve
        self.assertEqual(p, ZERO_POINT)

    # XXX: Very expensive test
    def test_scalar_mul(self):
        p = ZERO_POINT

        for _ in range(NUMBER_POINTS):
            self.assertTrue(p.is_on_curve())

            for j in range(NUMBER_POINTS):
                scalar_j = Scalar(j)
                p_times_j = p * scalar_j
                self.assertTrue(p_times_j.is_on_curve())

                p_plus_dot_dot_dot_plus_p = ZERO_POINT

                for _ in range(j):
                    p_plus_dot_dot_dot_plus_p += p

                self.assertEqual(p_times_j, p_plus_dot_dot_dot_plus_p)

            p += ONE_POINT

        # p finished cycle through curve
        self.assertEqual(p, ZERO_POINT)

    def test_discrete_log(self):
        p = ZERO_POINT

        for _ in range(NUMBER_POINTS):
            self.assertTrue(p.is_on_curve())
            k = p.discrete_log()
            self.assertEqual(p, ONE_POINT * k)

            p += ONE_POINT

        # p finished cycle through curve
        self.assertEqual(p, ZERO_POINT)


def int_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")


def reset_one_point(point: AffinePoint):
    """
    Set the one-point to the given point.

    **Warning: This changes the definition of scalar multiplication and the discrete logarithm!**
    These methods will return different outputs for different definitions of the one-point.
    All previous results are invalid for a different one-point.
    """
    global ONE_POINT
    ONE_POINT = point


def number_points() -> Optional[int]:
    """
    Return the number of points on the curve.
    """
    if ONE_POINT is None:
        return None

    minus_one_point = -ONE_POINT
    k = minus_one_point.discrete_log()
    assert ONE_POINT * k == minus_one_point
    assert ONE_POINT + minus_one_point == ZERO_POINT
    assert minus_one_point + ONE_POINT == ZERO_POINT
    return k.value + 1


class TestNumberPoints(unittest.TestCase):
    def test_number_points(self):
        i = 0
        tmp = ZERO_POINT

        while True:
            tmp += ONE_POINT
            i += 1

            if tmp.is_zero():
                self.assertEqual(NUMBER_POINTS, i)
                break

        self.assertEqual(NUMBER_POINTS, number_points())


class RandomPoints:
    """
    Deterministic sequence of random non-zero curve points.

    Always returns the same points in the same order.

    Use a seed to jump ahead in the sequence and generate different points.
    """
    index: int
    max_sub_index = 1000

    def __init__(self):
        self.index = 0

    def seed(self, n: int):
        """
        Jump ahead in the sequence by n steps.

        Let A be the n-th point in the sequence with seed zero (default).
        Let B be the 1-st point in the sequence with seed n - 1.
        Then A and B are the same.
        """
        self.index = n * self.max_sub_index

    def next(self) -> "AffinePoint":
        """
        Return random non-zero curve point.
        """
        for sub_index in range(self.max_sub_index):
            h = hashlib.sha256((self.index + sub_index).to_bytes(2, byteorder='big')).digest()
            x = Coordinate(int_from_bytes(h))
            p = x.lift_x()

            if p is None:
                continue

            self.index += self.max_sub_index
            return p

        raise StopIteration


class TestRandomPoints(unittest.TestCase):
    def test_next(self):
        points = RandomPoints()
        first = points.next()
        self.assertFalse(first.is_zero())
        self.assertTrue(first.is_on_curve())

        second = points.next()
        self.assertFalse(second.is_zero())
        self.assertTrue(second.is_on_curve())
        self.assertNotEqual(first, second)

        another_points = RandomPoints()
        another_first = another_points.next()
        self.assertEqual(first, another_first)

    def test_seed(self):
        points = RandomPoints()
        for _ in range(10):
            points.next()
        tenth = points.next()

        another_points = RandomPoints()
        another_points.seed(10)
        first = another_points.next()

        self.assertEqual(tenth, first)


GLOBAL_POINTS = RandomPoints()
"""
Global sequence of random non-zero curve points.
"""
ONE_POINT = GLOBAL_POINTS.next()
"""
Global one-point.
"""


class Scalar(ModInt):
    """
    Curve scalar.
    """
    modulus = NUMBER_POINTS
