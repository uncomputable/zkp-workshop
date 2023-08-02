"""
Use this script to generate small elliptic curves.

An elliptic curve is defined as y^2 = x^3 + a * x + b (mod p)
where a, b, p are parameters.
Any point (x, y) that satisfies this equation is on the curve.

a and b are coefficients and p is the field modulus.

There is also the number of points on a curve, denoted n.
We can calculate this for every curve and it should be prime,
so that our group has the desired arithmetic properties (cyclic, etc.).

This script keeps a = 0. This simplifies our equations and
enables an optimized implementation of EC operations.
secp256k1 uses the same trick.

You need sage(math) to run this script!
"""
from typing import Tuple
import meta
import os

def find_curve(p: int) -> Tuple[int, int, int, int]:
    for _ in range(0, 10000):
        p = next_prime(p)
        F = FiniteField(p)
        a = 0

        for b in range(1, 20):
            try:
                C = EllipticCurve([F(a), F(b)])
            except ArithmeticError:
                continue
            n = C.order()

            if n.is_prime():
                return p, a, b, n

    raise StopIteration


p = input("Initial field modulus (positive integer): ")

try:
    p = int(p)
    p, a, b, n = find_curve(p)

    patterns = (
        lambda x: f"MAX_COORDINATE = {x}",
        lambda x: f"PARAMETER_A = Coordinate({x})",
        lambda x: f"PARAMETER_B = Coordinate({x})",
        lambda x: f"NUMBER_POINTS = {x}"
    )
    updated_values = (p, a, b, n)

    meta.update_variables(os.path.join("ec", "core.py"), patterns, updated_values)
except ValueError:
    print("Field modulus must be an integer")
except StopIteration:
    print("Could not find any curves within the given search space")
