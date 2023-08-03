import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button

MAX_COORDINATE = 103
PARAMETER_A = 0
PARAMETER_B = 5
NUMBER_POINTS = 97
XY = (None, (94, 93), (67, 27), (23, 92), (3, 49), (8, 38), (30, 15), (86, 97), (52, 92), (68, 94), (60, 80), (28, 11), (6, 85), (66, 50), (59, 38), (87, 21), (32, 15), (49, 50), (19, 13), (36, 65), (33, 43), (97, 43), (41, 88), (2, 42), (100, 94), (95, 27), (47, 101), (44, 76), (82, 80), (9, 42), (91, 53), (50, 13), (27, 85), (38, 9), (102, 101), (11, 93), (101, 10), (57, 101), (64, 23), (42, 97), (31, 21), (76, 60), (88, 21), (65, 49), (70, 18), (92, 42), (78, 6), (35, 54), (34, 13), (34, 90), (35, 49), (78, 97), (92, 61), (70, 85), (65, 54), (88, 82), (76, 43), (31, 82), (42, 6), (64, 80), (57, 2), (101, 93), (11, 10), (102, 2), (38, 94), (27, 18), (50, 90), (91, 50), (9, 61), (82, 23), (44, 27), (47, 2), (95, 76), (100, 9), (2, 61), (41, 15), (97, 60), (33, 60), (36, 38), (19, 90), (49, 53), (32, 88), (87, 82), (59, 65), (66, 53), (6, 18), (28, 92), (60, 23), (68, 9), (52, 11), (86, 6), (30, 88), (8, 65), (3, 54), (23, 11), (67, 76), (94, 10))

# Initialize plot
fig, ax = plt.subplots()
ax.set_title("Elliptic curve $y^2 \equiv x^3 + {}x + {}$ (mod {})".format(PARAMETER_A, PARAMETER_B, MAX_COORDINATE))
ax.set_xlabel("x")
ax.set_ylabel("y")

# Initialize an array of zeros (white squares)
points = np.zeros((MAX_COORDINATE, MAX_COORDINATE))

# Draw first point
x, y = XY[1]
points[y, x] = 1
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
    points[y, x] = 0

    if n > 0:
        # Set next point
        x, y = XY[n]
        points[y, x] = 1

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
