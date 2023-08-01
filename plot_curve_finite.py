import matplotlib.pyplot as plt
import numpy as np
from ec.static import XY
from ec.core import MAX_COORDINATE, PARAMETER_A, PARAMETER_B

# Initialize the plot
fig, ax = plt.subplots()
ax.set_title("Elliptic curve $y^2 \equiv x^3 + {}x + {}$ (mod {})".format(PARAMETER_A.value, PARAMETER_B.value, MAX_COORDINATE))
ax.set_xlabel("x")
ax.set_ylabel("y")

# Initialize an array of zeros (white squares)
points = np.zeros((MAX_COORDINATE, MAX_COORDINATE))

# Add points on the curve
for (dlog, xy) in enumerate(XY):
    if xy:
        # Inverted coordinates
        # because imshow treats first component as rows (y coordinate)
        # and second component as columns (x coordinate)
        points[xy[1], xy[0]] = 1
        ax.text(xy[0], xy[1], str(dlog), ha="center", va="center", color="white")

# Plot the curve
# Set origin to the bottom left
# because imshow places it at the top left by default
ax.imshow(points, cmap='gray_r', origin='lower')

# Show plot
plt.show()
