# rlc_resonance.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter
import serial
import traceback
import sys


def usb_readline(usb_data_port):
    s = usb_data_port.readline().decode("ASCII").strip()
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
        print("RLC Resonance experiment is running...")
        print("This experiment will take 2 minutes to complete...")

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

        freq = freq / 1000  # Convert to kHz

        # Resonant frequency is at the peak voltage
        max_volt = np.max(volts)
        print(f"Resonance voltage = {max_volt:0.4f} V")

        resonance_freq = freq[np.argmax(volts)]
        print(f"Resonance freq = {resonance_freq:0.4f} kHz")

        # Create a plot window with a black background
        plt.figure("rlc_resonance.py")
        ax = plt.axes()
        ax.set_facecolor("black")

        # Plot the graph on the main axes
        ax.plot(freq, volts, color="magenta", linewidth=2)

        # Plot resonant frequency
        ax.vlines(resonance_freq, 0, max_volt, color="yellow", linewidth=2)

        # Give the graph a title and axis labels
        ax.set_title("RLC Circuit Resonance (Actual)")
        ax.set_xlabel("Frequency (kHz)")
        ax.set_ylabel("Voltage (V)")

        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.xaxis.set_major_formatter(FormatStrFormatter("%0.3f"))
        ax.set_xlim(-0.2, 5.2)
        ax.set_ylim(0, 0.1)

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
