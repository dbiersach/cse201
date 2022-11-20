# identify_element.py

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def fit_linear(vec_x, vec_y):
    vec_x = vec_x.reshape(-1, 1)
    model = LinearRegression().fit(vec_x, vec_y)
    m = model.coef_
    b = model.intercept_
    return m, b


def main():
    plt.figure(__file__)
    ax = plt.axes()

    vec_temperature_celsius = np.array([-50.0, 0.0, 50.0, 100.0, 150.0])
    vec_temperature_kelvin = vec_temperature_celsius + 273.15

    vec_volume_liters = np.array([11.6, 14.0, 16.2, 19.4, 21.8])
    vec_volume_meters_cubed = vec_volume_liters / 1000

    m, b = fit_linear(vec_temperature_kelvin, vec_volume_meters_cubed)

    slope = m[0]  # Ratio of V to T (slope of best-fit V/T line)

    p = 2.0 * 101_325  # Convert atm to pascals
    r = 8.31446261815324  # Ideal gas constant (m^3*Pa/(K*mol))
    n = p / r * slope  # Moles of gas (rearrange ideal gas law equation)

    m_sample = 50  # grams
    molar_mass = m_sample / n  # sample mass divided by number of moles

    print(f"Molar mass of Unknown Gas: {molar_mass:.3f}u")
    print("      Molar mass of Argon: 39.948u")

    x = np.linspace(0, 500, 1000)
    ax.plot(x, m * x + b)
    ax.scatter(vec_temperature_kelvin, vec_volume_meters_cubed, color="red")
    ax.set_title(f"Unknown Gas ({molar_mass:.3f}u)")
    ax.set_xlabel(r"$Temperature\;(\degree K)$")
    ax.set_ylabel(r"$Volume\;(m^3)$")
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 0.025)

    plt.show()


main()
