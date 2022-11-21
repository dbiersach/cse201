# simple_pendulum.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

phase_constant = 9.81 / 1.0  # (m/s^2 = g / pendulum length)


def d_omega(omega, theta, time):
    return -phase_constant * theta


def d_theta(omega, theta, time):
    return omega


def euler(v1, v2, u, h, f1, f2):
    # Implements Euler's method for linked ODEs (f1, f2),
    # with two dependent variables (v1, v2) and the
    # independent variable (u) having step size (h)
    next_v1 = v1 + f1(v1, v2, u) * h
    next_v2 = v2 + f2(v1, v2, u) * h
    u += h
    return next_v1, next_v2, u


def main():
    plt.figure(__file__)
    ax = plt.axes()

    time_stop = 10  # Model out to ten seconds
    time_steps = 250

    delta_time = time_stop / time_steps

    omega = np.zeros(time_steps)
    theta = np.zeros(time_steps)
    time = np.zeros(time_steps)

    theta[0] = np.pi / 18  # 10 degrees (small angle)

    for step in range(time_steps - 1):
        omega[step + 1], theta[step + 1], time[step + 1] = euler(
            omega[step], theta[step], time[step], delta_time, d_omega, d_theta
        )

    ax.plot(time, theta, zorder=3)

    ax.set_title("Simple Pendulum (Euler's Method)")
    ax.set_xlabel("time (secs)")
    ax.set_ylabel("theta (radians)")

    ax.axhline(y=0.0, color="lightgray")

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    
    ax.figure.set_size_inches(10, 8)
    plt.savefig("simple_pendulum.png", dpi=600)    

    plt.show()


main()
