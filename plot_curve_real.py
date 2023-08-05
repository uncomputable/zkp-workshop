import numpy as np
import matplotlib.pyplot as plt
from local.ec.core import PARAMETER_A, PARAMETER_B


def plot():
    # Initialize the plot
    fig, ax = plt.subplots()
    ax.set_title(f"Elliptic curve $y^2 = x^3 + {PARAMETER_A.value}x + {PARAMETER_B.value}$ over ℝ")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.grid(True)

    # Compute points on the curve
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = pow(y, 2) - pow(x, 3) - x * PARAMETER_A.value - PARAMETER_B.value

    # Plot the curve
    plt.contour(x, y, z, [0])

    # Show plot
    plt.show()


if __name__ == "__main__":
    plot()
