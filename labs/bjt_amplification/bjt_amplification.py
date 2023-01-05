# bjt_amplification.py

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
        print("Transistor Amplification experiment is running...")

        # Read number of samples from USB
        n = int(usb_readline(ser))

        # Declare numpy arrays to store the samples
        volts_be = np.zeros(n, float)
        volts_ce = np.zeros(n, float)

        # Read volts and amps samples from USB into arrays
        for i in range(n):
            volts_be[i] = float(usb_readline(ser))
        for i in range(n):
            volts_ce[i] = float(usb_readline(ser))

        print(f"Received {n} BE volt and CE volt samples...")
        
        # Create a plot window
        plt.figure("bjt_amplification.py")
        ax = plt.axes()
        ax.set_facecolor("black")

        # Plot the graph on the main axes
        ax.plot(volts_be, volts_ce, color="yellow", linewidth=2)

        # Give the graph a title and axis labels
        ax.set_title("PN2222A (NPN) BJT Amplification")
        ax.set_xlabel("Base-Emitter Voltage (V)")
        ax.set_ylabel("Collector-Emitter Voltage (V)")

        ax.xaxis.set_major_locator(MultipleLocator(0.02))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        ax.yaxis.set_major_locator(MultipleLocator(0.2))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        ax.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)

        ax.figure.set_size_inches(10, 8)
        plt.savefig("bjt_amplification.png", dpi=600)
        plt.show()

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
