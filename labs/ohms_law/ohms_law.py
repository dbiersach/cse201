# ohms_law.py

import numpy as np
import matplotlib.pyplot as plt


def read_samples(file_name):
    samples = np.genfromtxt(file_name, delimiter=",")
    return samples[:, 0], samples[:, 1]


def fit_linear(x, y):
    m = len(x) * np.sum(x * y) - np.sum(x) * np.sum(y)
    m = m / (len(x) * np.sum(x**2) - np.sum(x) ** 2)
    b = (np.sum(y) - m * np.sum(x)) / len(x)
    return m, b


# Read in the sample data files
volts1, amps1 = read_samples("resistor1.csv")
volts2, amps2 = read_samples("resistor2.csv")
volts3, amps3 = read_samples("resistor3.csv")

# Find the line of best fit y = mx + b
# where m = slope and b = y-intercept
m1, b1 = fit_linear(amps1, volts1)
m2, b2 = fit_linear(amps2, volts2)
m3, b3 = fit_linear(amps3, volts3)

plt.figure("ohms_law.py")
plt.gca().set_facecolor("black")

plt.scatter(amps1, volts1)
plt.scatter(amps2, volts2)
plt.scatter(amps3, volts3)

# Find the maximum amps across all samples
max_amps = np.max((amps1, amps2, amps3))
# Increase the max amps by 10%
max_amps *= 1.1

# Plot the line of best fit for each resistor
x = np.linspace(0, max_amps, 100)
plt.plot(x, m1 * x + b1, label=f"Resistor 1 : Slope = {m1:.3f}")
plt.plot(x, m2 * x + b2, label=f"Resistor 2 : Slope = {m2:.3f}")
plt.plot(x, m3 * x + b3, label=f"Resistor 3 : Slope = {m3:.3f}")

plt.xlim(0, max_amps)

plt.title("Ohm's Law (Voltage vs. Current)")
plt.xlabel("Current (A)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.show()
