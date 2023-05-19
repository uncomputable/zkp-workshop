max_coordinate = 1009
assert max_coordinate.is_prime()
Coordinates = FiniteField(max_coordinate)
Curve = EllipticCurve([Coordinates(0), Coordinates(11)])

number_points = Curve.order()
assert number_points.is_prime()
max_scalar = number_points
Scalars = FiniteField(max_scalar)

Zero = Curve(0)
One = Curve.gens()[0]
zero = Scalars(0)
one = Scalars(1)
