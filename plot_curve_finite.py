import matplotlib.pyplot as plt
import numpy as np
from ec.static import XY
from ec.core import MAX_COORDINATE, PARAMETER_A, PARAMETER_B

# Initialize an array of zeros (white squares)
points = np.zeros((MAX_COORDINATE, MAX_COORDINATE))

# Add points on the curve
for xy in XY:
    if xy:
        points[xy[0], xy[1]] = 1

# Plot the curve
plt.imshow(points, cmap='gray_r', origin='lower')

plt.title("Elliptic curve $y^2 \equiv x^3 + {}x + {}$ (mod {})".format(PARAMETER_A.value, PARAMETER_B.value, MAX_COORDINATE))
plt.show()
