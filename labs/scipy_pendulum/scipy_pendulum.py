# scipy_pendulum.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.integrate import solve_ivp


def model(time, state_vector, phase_constant):
    omega, theta = state_vector  # unpack dependent variables
    d_omega = -phase_constant * np.sin(theta)
    d_theta = omega
    return d_omega, d_theta


def main():
    plt.figure(__file__)
    ax = plt.axes()

    # Precalculate phase constant
    pendulum_length = 1.0  # meters
    phase_constant = 9.81 / pendulum_length

    # Set initial conditions
    omega_initial = 0
    theta_initial = np.radians(75)  # 75 degrees

    # Set model duration (seconds)
    time_initial = 0
    time_final = 10

    # Calculate for an underdamped pendulum
    sol = solve_ivp(
        model,
        (time_initial, time_final),
        [omega_initial, theta_initial],
        max_step=0.01,
        args=(phase_constant,),
    )
    time_steps = sol.t
    omega, theta = sol.y

    ax.plot(time_steps, theta, linewidth=2, label=r"$\theta$ (rads)")
    ax.plot(time_steps, omega, linewidth=2, label=r"$\omega$ (rads/sec)")

    ax.set_title("Simple Pendulum (RKF45 Method)")
    ax.set_xlabel("Time (sec)")
    ax.axhline(y=0.0, color="lightgray")
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.legend(loc="upper right")

    ax.figure.set_size_inches(10, 8)
    plt.savefig("scipy_pendulum.png", dpi=600)

    plt.show()


main()
