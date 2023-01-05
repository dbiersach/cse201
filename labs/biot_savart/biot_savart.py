# biot_savart.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from sklearn.linear_model import LinearRegression
import serial
import traceback
import sys


def fit_linear(vec_x, vec_y):
    vec_x = vec_x.reshape(-1, 1)
    model = LinearRegression().fit(vec_x, vec_y)
    m = model.coef_
    b = model.intercept_
    score = model.score(vec_x, vec_y)
    return m, b, score


def usb_readline(ser):
    s = ser.readline().decode("ASCII").strip()
    while len(s) == 0:
        s = ser.readline().decode("ASCII").strip()
    return s


def main():
    ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
    try:
        port = "COM6"
        if sys.platform == "linux":
            port = "/dev/ttyAMA0"
        if sys.platform == "darwin":
            port = "/dev/tty.usbserial-110"

        ser.port = port
        ser.open()

        # Send MCU the command to (r)un the experiment
        ser.write(b"r\n")
        print("Biot-Savart experiment is running...")
        print("This experiment may take up 90 seconds to complete...")

        # Read number of samples from USB
        n = int(usb_readline(ser))

        # Declare numpy arrays to store the samples
        current = np.zeros(n, float)
        field_strength = np.zeros(n, float)

        # Read samples into arrays
        for i in range(n):
            current[i] = float(usb_readline(ser))
        for i in range(n):
            field_strength[i] = float(usb_readline(ser))

        print(f"Received {n} current and field_strength samples...")

        # Create a plot window with a black background
        plt.figure("biot_savart.py")
        ax = plt.axes()
        ax.set_facecolor("black")

        # Plot the samples
        ax.scatter(
            current, field_strength, marker=".", color="yellow", label="Sensor Data"
        )

        # Fit a linear regression
        x = np.linspace(np.min(current), np.max(current), 1000)
        m, b, score = fit_linear(current, field_strength)
        ax.plot(x, m * x + b, label=f"Linear ($R^2$={score:.4f})")
        print(f"Turn Density = {m[0] / 1000 / 1.256e-3:0.4f}")

        # Format the plot
        ax.set_title("Biot-Savart Law")
        ax.set_xlabel("Current (mA)")
        ax.set_ylabel("Magnetic Field Strength (uT)")
        ax.legend()
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        # Show the plot window
        ax.figure.set_size_inches(10, 8)
        plt.savefig("biot_savart.png", dpi=600)
        plt.show()

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
