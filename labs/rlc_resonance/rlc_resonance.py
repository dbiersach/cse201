# rlc_resonance.py

import numpy as np
import matplotlib.pyplot as plt
import serial
import traceback
import sys


def usb_readline(usb_data_port):
    s = usb_data_port.readline().decode("ASCII").strip()
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
        print("RLC Resonance experiment is running...")
        print("This experiment may take up 90 seconds to complete...")

        # Read number of samples from USB
        n = int(usb_readline(ser))

        # Declare numpy arrays to store the samples
        freq = np.zeros(n, float)
        volts = np.zeros(n, float)

        # Read frequencies and volts samples from USB into arrays
        for i in range(n):
            freq[i] = float(usb_readline(ser))
        for i in range(n):
            volts[i] = float(usb_readline(ser))

        print(f"Received {n} frequency and voltage samples...")

        # Create a plot window with a black background
        plt.figure("lc_resonance.py")
        ax = plt.axes()
        ax.set_facecolor("black")

        # Plot the graph on the main axes
        ax.plot(freq, volts, color="magenta", linewidth=2)

        # Give the graph a title and axis labels
        ax.set_title("LC Circuit Impedance at Resonant Frequency")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Voltage (V)")

        # Show the plot window
        ax.figure.set_size_inches(10, 8)
        plt.savefig("rlc_resonance.png", dpi=600)
        plt.show()

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
