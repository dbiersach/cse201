# fluorine_18.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# Fluorine-18 half life (hrs)
tau = 1.829


def d_n(n):
    return -n / tau


def euler(v1, u, h, f1):
    # Implements Euler's method for a single ODE (f1)
    # with one dependent variable (v1) and one
    # independent variable (u) having step size (h)
    next_v1 = v1 + f1(v1) * h
    next_u = u + h
    return next_v1, next_u


def main():
    plt.figure(__file__)
    ax = plt.axes()

    time_steps = 100

    delta_time = 12 / time_steps  # model decay over 12 hours

    time = np.zeros(time_steps)
    nuclei = np.zeros(time_steps)

    nuclei[0] = 100  # set initial concentration

    for step in range(time_steps - 1):
        nuclei[step + 1], time[step + 1] = euler(
            nuclei[step], time[step], delta_time, d_n
        )

    ax.plot(time, nuclei, color="red", linewidth=2)

    ax.set_title("Fluorine-18 Radioactive Decay (Euler's Method)")
    ax.set_xlabel("time (hrs)")
    ax.set_ylabel("concentration")

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.figure.set_size_inches(10, 8)
    plt.savefig("fluorine_18.png", dpi=600)

    plt.show()


main()
