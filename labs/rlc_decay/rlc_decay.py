# rlc_decay.py

import numpy as np
import matplotlib.pyplot as plt

R = 0.1  # resistance in ohms
L = 0.01  # inductance in henries
C = 0.01  # capacitance in farads
I_0 = 1  # current in amps (initial)


def d2_current(d_I, I, time):
    return -R / L * d_I - 1 / (L * C) * I


def d1_current(d_I, I, time):
    return d_I


def euler(v1, v2, u, h, f1, f2):
    # Implements Euler's method for linked ODEs (f1, f2),
    # with two dependent variables (v1, v2) and the
    # independent variable (u) having step size (h)
    next_v1 = v1 + f1(v1, v2, u) * h
    next_v2 = v2 + f2(next_v1, v2, u) * h  # Cromer's Fix
    u += h
    return next_v1, next_v2, u


time_stop = 1  # Model out to one second
time_steps = 250

d_t = time_stop / time_steps

d_I = np.zeros(time_steps)
I = np.zeros(time_steps)
time = np.zeros(time_steps)

I[0] = I_0

for step in range(time_steps - 1):
    d_I[step + 1], I[step + 1], time[step + 1] = euler(
        d_I[step], I[step], time[step], d_t, d2_current, d1_current
    )

plt.figure("rlc_decay.py")
plt.plot(time, I)
plt.title("Decaying RLC Circuit")
plt.xlabel("time (secs)")
plt.ylabel("current (amps)")
plt.axhline(y=0.0, color="lightgray", zorder=1)
plt.show()
