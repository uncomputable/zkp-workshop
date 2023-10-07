import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Initialize the plot
fig, ax = plt.subplots()
# Leave space for UI
fig.subplots_adjust(bottom=0.25)

# Parameters
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
index = 0
step = 1


def update_plot(n_nodes: int, step: int):
    # Clear previous plot
    ax.cla()
    ax.axis('off')

    next_prime_text.set_text(f"Number of nodes: {primes[index]}")
    step_text.set_text(f"Step size: {step}")

    # Calculate node coordinates
    theta = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    x = np.cos(theta)
    y = np.sin(theta)

    # Draw nodes
    for i in range(n_nodes):
        ax.plot(x[i], y[i], 'o', markersize=10)

    # Draw edges
    i = step % n_nodes

    for number in range(n_nodes):
        j = (i + step) % n_nodes
        ax.plot([x[i], x[j]], [y[i], y[j]], 'k-')
        ax.text(x[i] * 1.1, y[i] * 1.1, str((number + 1) % n_nodes), horizontalalignment='center')
        i = j

    # Draw plot
    plt.draw()


def next_prime(_):
    global index, step
    if index < len(primes) - 1:
        index += 1
        step = 1
    update_plot(primes[index], step)


def previous_prime(_):
    global index, step
    if index > 0:
        index -= 1
        step = 1
    update_plot(primes[index], step)


def next_step(_):
    global step
    if step < primes[index] - 1:
        step += 1
    update_plot(primes[index], step)


def previous_step(_):
    global step
    if step > 0:
        step -= 1
    update_plot(primes[index], step)


# Buttons for changing parameters
ax_next_prime = fig.add_axes([0.1, 0.1, 0.2, 0.03])
ax_previous_prime = fig.add_axes([0.3, 0.1, 0.2, 0.03])
ax_next_step = fig.add_axes([0.5, 0.1, 0.2, 0.03])
ax_previous_step = fig.add_axes([0.7, 0.1, 0.2, 0.03])

next_prime_button = Button(ax=ax_next_prime, label="Next prime")
previous_prime_button = Button(ax=ax_previous_prime, label="Previous prime")
next_step_button = Button(ax=ax_next_step, label="Next step")
previous_step_button = Button(ax=ax_previous_step, label="Previous step")

next_prime_button.on_clicked(next_prime)
previous_prime_button.on_clicked(previous_prime)
next_step_button.on_clicked(next_step)
previous_step_button.on_clicked(previous_step)

# Text showing current parameters
next_prime_text = ax_next_prime.text(0.4, -0.1, "", ha="center", transform=ax.transAxes, verticalalignment="top")
step_text = ax_next_prime.text(0.6, -0.1, "", ha="center", transform=ax.transAxes, verticalalignment="top")

# Show plot
update_plot(primes[index], 1)
plt.show()
