# ohms_law.py

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def read_samples(file_name):
    samples = np.genfromtxt(file_name, delimiter=",")
    return samples[:, 0], samples[:, 1]


def fit_linear(vec_x, vec_y):
    vec_x = vec_x.reshape(-1, 1)
    model = LinearRegression().fit(vec_x, vec_y)
    m = model.coef_[0]
    b = model.intercept_
    score = model.score(vec_x, vec_y)
    return m, b, score


def main():
    # Read in the sample data files
    volts1, amps1 = read_samples("resistor1.csv")
    volts2, amps2 = read_samples("resistor2.csv")
    volts3, amps3 = read_samples("resistor3.csv")

    # Find the line of best fit y = mx + b
    # where m = slope and b = y-intercept
    m1, b1, _ = fit_linear(amps1, volts1)
    m2, b2, _ = fit_linear(amps2, volts2)
    m3, b3, _ = fit_linear(amps3, volts3)

    # Create a plot window with a black background
    plt.figure("ohms_law.py")
    ax = plt.axes()
    ax.set_facecolor("black")

    # Plot the sample data values
    ax.scatter(amps1, volts1)
    ax.scatter(amps2, volts2)
    ax.scatter(amps3, volts3)

    # Find the maximum amps across all samples
    max_amps = np.max((amps1, amps2, amps3))
    # Increase the max amps by 10%
    max_amps *= 1.1

    # Plot the line of best fit for each resistor
    x = np.linspace(0, max_amps, 100)
    ax.plot(x, m1 * x + b1, label=f"Resistor 1 : Slope = {m1:.3f}")
    ax.plot(x, m2 * x + b2, label=f"Resistor 2 : Slope = {m2:.3f}")
    ax.plot(x, m3 * x + b3, label=f"Resistor 3 : Slope = {m3:.3f}")

    # Set the domain of the graph
    ax.set_xlim(0, max_amps)

    # Set the graph title and axis labels, and show the legend
    ax.set_title("Ohm's Law (Voltage vs. Current)")
    ax.set_xlabel("Current (A)")
    ax.set_ylabel("Voltage (V)")
    ax.legend()

    # Show the plot window
    ax.figure.set_size_inches(10, 8)
    plt.savefig("ohms_law.png", dpi=600)
    plt.show()


main()
