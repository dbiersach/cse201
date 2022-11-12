# plot_equation.py

import numpy as np
import matplotlib.pyplot as plt


def main():
    plt.figure(__file__)
    ax = plt.axes()
    ax.set_facecolor("black")

    V_s = 3.3  # in Volts
    R = 10_000  # 10K Ohms in Ohms
    C = 1e-5  # 10 uF in Farads
    tau = R * C

    t = np.linspace(0, 1, 100)
    v_c = V_s * (1 - np.exp(-t / tau))

    ax.plot(t, v_c, color="cyan", linewidth=2)

    ax.set_title("Capacitor Voltage vs. Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")

    ax.axhline(V_s, color="yellow", linewidth=2)

    ax.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)

    plt.show()


main()
