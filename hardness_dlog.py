import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from ec.core import MAX_COORDINATE, NUMBER_POINTS, PARAMETER_A, PARAMETER_B, ONE_POINT, Scalar

# Initialize plot
fig, ax = plt.subplots()
ax.set_title("Elliptic curve $y^2 \equiv x^3 + {}x + {}$ (mod {})".format(PARAMETER_A.value, PARAMETER_B.value, MAX_COORDINATE))
ax.set_xlabel("x")
ax.set_ylabel("y")

# Initialize an array of zeros (white squares)
points = np.zeros((MAX_COORDINATE, MAX_COORDINATE))

# Draw first point
x, y = ONE_POINT.xy()
points[y.value, x.value] = 1
im = ax.imshow(points, cmap='gray_r', origin='lower', animated=True)

# Iteration slider
ax_slider = fig.add_axes([0.1, 0.1, 0.05, 0.75])  # [left, bottom, width, height]
slider = Slider(
    ax=ax_slider,
    label="Point number",
    valmin=0,
    valmax=NUMBER_POINTS - 1,
    valstep=1,
    valinit=1,
    orientation="vertical"
)

def update(n: int):
    global x, y

    # Reset previous point
    points[y.value, x.value] = 0

    if n > 0:
        # Set next point
        x, y = (Scalar(n) * ONE_POINT).xy()
        points[y.value, x.value] = 1

    # Redraw
    im.set_array(points)

slider.on_changed(update)

# Increment button
ax_inc = plt.axes([0.8, 0.5, 0.15, 0.25])  # [left, bottom, width, height]
button_inc = Button(ax_inc, '+1')

def increment(event):
    if slider.val < slider.valmax:
        slider.set_val(slider.val + 1)
    else:
        slider.set_val(slider.valmin)

button_inc.on_clicked(increment)

# Decrement button
ax_dec = plt.axes([0.8, 0.2, 0.15, 0.25])  # [left, bottom, width, height]
button_dec = Button(ax_dec, '-1')

def decrement(event):
    if slider.val > slider.valmin:
        slider.set_val(slider.val - 1)
    else:
        slider.set_val(slider.valmax)

button_dec.on_clicked(decrement)

# Show plot
plt.show()
