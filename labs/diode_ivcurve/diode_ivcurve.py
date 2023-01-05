# diode_ivcurve.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
import serial
import traceback
import sys


def usb_readline(ser):
    s = ser.readline().decode("ASCII").strip()
    while len(s) == 0:
        s = ser.readline().decode("ASCII").strip()
    return s


def main():
    ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
    try:
        port = "COM5"
        if sys.platform == "linux":
            port = "/dev/ttyAMA0"
        if sys.platform == "darwin":
            port = "/dev/tty.usbserial-110"

        ser.port = port
        ser.open()

        # Send MCU the command to (r)un the experiment
        ser.write(b"r\n")
        print("Diode I-V Curve experiment is running...")

        # Read number of samples from USB
        n = int(usb_readline(ser))

        # Declare numpy arrays to store the samples
        volts = np.zeros(n, float)
        amps = np.zeros(n, float)

        # Read volts and amps samples from USB into arrays
        for i in range(n):
            volts[i] = float(usb_readline(ser))
        for i in range(n):
            amps[i] = float(usb_readline(ser))

        print(f"Received {n} volt and amp samples...")

        # Create a plot window
        plt.figure("diode_ivcurve.py")
        ax = plt.axes()
        ax.set_facecolor("black")

        # Plot the graph on the main axes
        ax.plot(volts, amps, color="yellow", linewidth=2)

        # Give the graph a title and axis labels
        ax.set_title("1N4001 Diode I-V Characteristic Curve")
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (mA)")

        ax.xaxis.set_major_locator(MultipleLocator(0.1))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        ax.yaxis.set_major_locator(MultipleLocator(1.0))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        ax.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)

        ax.figure.set_size_inches(10, 8)
        plt.savefig("diode_ivcurve.png", dpi=600)
        plt.show()

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
