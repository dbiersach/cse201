# plot_equation.py

import numpy as np
import matplotlib.pyplot as plt

V_s = 3.3  # in Volts
R = 10_000  # 10K Ohms in Ohms
C = 1e-5  # 10 uF in Farads
tau = R * C

t = np.linspace(0, 1, 100)
v_c = V_s * (1 - np.exp(-t / tau))

plt.figure()
plt.gca().set_facecolor("black")
plt.plot(t, v_c, color="cyan", linewidth=2)
plt.title("Capacitor Voltage vs. Time")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.axhline(V_s, color="yellow", linewidth=2)
plt.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)
plt.show()
