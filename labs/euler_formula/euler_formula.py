# euler_formula.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def plot_real_exponential(ax):
    # Plot y = e^x
    x = np.linspace(-10, 10, 1000, endpoint=True)
    ax.plot(x, np.exp(x), color="green", label=r"$e^x$")


def plot_euler_formula(ax):
    # Plot y = e^ix
    x = np.linspace(-10, 10, 1000, endpoint=True)
    z = np.zeros(len(x), dtype=complex)

    for idx, val in enumerate(x):
        z[idx] = np.exp(complex(0, val))

    ax.plot(np.real(z), np.imag(z), color="blue", linewidth=2, label=r"$e^{i x}$")


def plot_complex_exponential(ax, z):
    # Plot a complex exponential on this Argand diagram
    x, y = np.real(z), np.imag(z)
    ax.scatter(x, y, color="black")

    line_hypot = [(0, 0), (x, y)]
    line_opp = [(x, 0), (x, y)]
    line_adj = [(0, 0), (x, 0)]
    lc = LineCollection([line_hypot, line_opp, line_adj], color="red", zorder=2.5)
    ax.add_collection(lc)

    ax.annotate(
        r"$1.7e^{0.62 i}$",
        xy=(x, y),
        size=15,
        color="black",
        xytext=(5, 0),
        textcoords="offset pixels",
    )

    ax.annotate(
        r"$1.7\sin(0.62)$",
        xy=(x, y / 3),
        color="red",
        xytext=(5, 0),
        textcoords="offset pixels",
    )

    ax.annotate(
        r"$1.7\cos(0.62)$",
        xy=(x / 3, 0),
        color="red",
        xytext=(-20, 10),
        textcoords="offset pixels",
    )


def plot_complex_number(ax, z):
    # Plot complex number
    x, y = np.real(z), np.imag(z)
    ax.scatter(x, y, color="purple")

    line_hypot = [(0, 0), (x, y)]
    line_opp = [(x, 0), (x, y)]
    line_adj = [(0, 0), (x, 0)]
    lc = LineCollection([line_hypot, line_opp, line_adj], color="purple", zorder=2.5)
    ax.add_collection(lc)

    hypot = np.hypot(np.real(z), np.imag(z))
    theta = np.arctan(np.imag(z) / np.real(z)) - np.pi

    ax.annotate(
        rf"$({x}{y}i) = {hypot:.3f}e^{{ {theta:.3f} i }}$",
        xy=(x, y),
        xytext=(-50, -25),
        textcoords="offset pixels",
        color="purple",
    )


def main():
    plt.figure(__file__)
    ax = plt.axes()

    plot_real_exponential(ax)
    plot_euler_formula(ax)

    z = -1 - 1.5j
    plot_complex_number(ax, z)

    z = 1.7 * np.exp(complex(0, 0.62))
    plot_complex_exponential(ax, z)

    ax.grid()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axvline(x=0, color="black", linewidth=2)
    ax.axhline(y=0, color="black", linewidth=2)
    ax.set_title(r"Euler's Formula: $z=e^{\pm i\theta}=\cos\theta\pm i\sin\theta$")
    ax.set_xlabel("Real z")
    ax.set_ylabel("Imaginary z")
    ax.legend(loc="best")

    ax.figure.set_size_inches(10, 8)
    plt.savefig("euler_formula.png", dpi=600)

    plt.show()


main()
