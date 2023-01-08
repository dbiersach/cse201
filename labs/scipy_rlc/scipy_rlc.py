# scipy_rlc.py

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.integrate import solve_ivp

R = 0.1  # resistance in ohms
L = 0.01  # inductance in henries
C = 0.01  # capacitance in farads
I_0 = 1  # current in amps (initial)


def model(time, state_vector):
    dI, I = state_vector
    # TODO: Implement the correct diffrential equation on the next line
    ddI = 0
    return [ddI, dI]


def main():
    plt.figure(__file__)
    ax = plt.axes()

    t0, tf, ts = 0, 1, 1000  # time in secs, 1000 time steps

    sol = solve_ivp(model, (t0, tf), [0, I_0], max_step=(tf - t0) / ts)
    t = sol.t
    _, I = sol.y

    ax.plot(t, I, zorder=3)

    ax.set_title("Resistor-Inductor-Capacitor (RLC) Circuit")
    ax.set_xlabel("Time (secs)")
    ax.set_ylabel("Current (Amps)")
    ax.axhline(y=0.0, color="lightgray")
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.figure.set_size_inches(10, 8)
    plt.savefig("rlc_circuit", dpi=600)

    plt.show()


main()
