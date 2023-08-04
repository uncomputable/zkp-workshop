import numpy as np
import matplotlib.pyplot as plt
from local.ec.core import PARAMETER_A, PARAMETER_B

# Generate x values
x = np.linspace(-2, 2, 400)

# Calculate y values (note: this will include complex numbers)
y_squared = x**3 + PARAMETER_A.value * x + PARAMETER_B.value

# We'll take the real square roots as y values, and ignore the complex roots
y_positive = np.real(np.sqrt(y_squared))
y_negative = -np.real(np.sqrt(y_squared))

# Plot the curve
plt.plot(x, y_positive, "b")
plt.plot(x, y_negative, "b")

plt.title("Elliptic curve $y^2 = x^3 + {}x + {}$ over ℝ".format(PARAMETER_A.value, PARAMETER_B.value))
plt.grid(True)
plt.show()
