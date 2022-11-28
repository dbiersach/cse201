# rk4_ode.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def d_y(y, x):
    return y * np.cos(x)


def euler(v1, u, h, f1):
    # Implements Euler's method for a single ODE (f1)
    # with one dependent variable (v1) and one
    # independent variable (u) having step size (h)
    next_v1 = v1 + f1(v1, u) * h
    next_u = u + h
    return next_v1, next_u


def rk4(v1, u, h, f1):
    # Implements 4th order Runge-Kutta method
    # for a single ODE (f1) with one dependent variable (v1)
    # and one independent variable (u) having step size (h)
    k1_v1 = f1(v1, u)
    k2_v1 = f1(v1 + (h / 2.0) * k1_v1, u)
    k3_v1 = f1(v1 + (h / 2.0) * k2_v1, u)
    k4_v1 = f1(v1 + h * k3_v1, u)
    next_v1 = v1 + h * (k1_v1 + 2.0 * k2_v1 + 2.0 * k3_v1 + k4_v1) / 6.0
    next_u = u + h
    return next_v1, next_u


def main():
    plt.figure(__file__)
    ax = plt.axes()

    steps = 1000
    dx = 12 * np.pi / steps

    x_euler = np.zeros(steps)
    y_euler = np.zeros(steps)

    x_rk4 = np.zeros(steps)
    y_rk4 = np.zeros(steps)

    y_euler[0] = 1  # set initial conditions
    y_rk4[0] = 1

    for step in range(steps - 1):
        y_euler[step + 1], x_euler[step + 1] = euler(
            y_euler[step], x_euler[step], dx, d_y
        )
        y_rk4[step + 1], x_rk4[step + 1] = rk4(y_rk4[step], x_rk4[step], dx, d_y)

    ax.set_title(
        r"$\frac{dy}{dx} = y\cdot\cos(x),\; y(0)=1\quad\rightarrow\quad y=e^{\sin(x)}$"
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.plot(
        x_euler, y_euler, label="Euler", color="red", linewidth=2, linestyle="solid"
    )
    ax.plot(x_rk4, y_rk4, label="RK4", color="blue", linewidth=2, linestyle="solid")

    ax.legend(loc="best")

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.figure.set_size_inches(10, 8)
    plt.savefig("rk45_ode.png", dpi=600)

    plt.show()


main()
