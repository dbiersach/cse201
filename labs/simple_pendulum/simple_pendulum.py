# simple_pendulum.py

import numpy as np
import matplotlib.pyplot as plt

phase_constant = 9.81 / 1.0  # (m/s^2 = g / pendulum length)


def d_omega(omega, theta, time):
    return -phase_constant * np.sin(theta)


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


time_stop = 10  # Model out to ten seconds
time_steps = 250

d_t = time_stop / time_steps

omega = np.zeros(time_steps)
theta = np.zeros(time_steps)
time = np.zeros(time_steps)

theta[0] = np.radians(75)

for step in range(time_steps - 1):
    omega[step + 1], theta[step + 1], time[step + 1] = euler(
        omega[step], theta[step], time[step], d_t, d_omega, d_theta
    )

plt.figure("simple_pendulum.py")
plt.plot(time, theta, label="theta")
plt.plot(time, omega, label="omega")
plt.title("Simple Pendulum (Euler's Method)")
plt.xlabel("time (secs)")
plt.ylabel("theta (radians)")
plt.axhline(y=0.0, color="lightgray")
plt.legend(loc="upper right")
plt.show()
