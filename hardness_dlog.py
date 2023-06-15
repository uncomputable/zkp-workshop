import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
#%matplotlib ipympl

from myec import *

# Customization
marker_color='#283F4E' 
marker_size = 25
button_color = 'lightblue'
button_hover_color = 'skyblue'

# Skeleton
fig, ax = plt.subplots(subplot_kw = dict(aspect="equal"))
ax.set_xlim(0, MAX_COORDINATE)
ax.set_ylim(0, MAX_COORDINATE)
ax.set_xlabel("x")
ax.set_ylabel("y")

init_x, init_y = ONE_POINT.xy()
scat = ax.scatter([init_x.value], [init_y.value], c=marker_color, s=marker_size)

# Iteration slider
ax_slider = fig.add_axes([0.1, 0.1, 0.05, 0.75])  # [left, bottom, width, height]
slider = Slider(
    ax=ax_slider,
    label="Point number",
    valmin=0,
    valmax=NUMBER_POINTS,
    valstep=1,
    valinit=1,
    orientation="vertical"
)

def update(n):
    x, y = (Scalar(n) * ONE_POINT).xy()
    scat.set_offsets([[x.value, y.value]])
    # scat.set_offsets(np.column_stack((x.value, y.value)))
    fig.canvas.draw_idle()

slider.on_changed(update)

# Increment button
ax_inc = plt.axes([0.8, 0.5, 0.15, 0.25])  # [left, bottom, width, height]
button_inc = Button(ax_inc, '+1', color=button_color, hovercolor=button_hover_color)

def increment(event):
    val = slider.val
    if val < slider.valmax:
        slider.set_val(val + 1)

button_inc.on_clicked(increment)

# Decrement button
ax_dec = plt.axes([0.8, 0.2, 0.15, 0.25])  # [left, bottom, width, height]
button_dec = Button(ax_dec, '-1', color=button_color, hovercolor=button_hover_color)

def decrement(event):
    val = slider.val
    if val > slider.valmin:
        slider.set_val(val - 1)

button_dec.on_clicked(decrement)

# Show plot
plt.show()
