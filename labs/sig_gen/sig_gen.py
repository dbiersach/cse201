# sig_gen.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FormatStrFormatter
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
        print("Signal Generator experiment is running...")

        # Read number of samples from USB
        n = int(usb_readline(ser))

        # Declare numpy arrays to store the samples
        times = np.zeros(n, float)
        volts = np.zeros(n, float)

        # Read times and volts samples from USB into arrays
        for i in range(n):
            times[i] = int(usb_readline(ser))
        for i in range(n):
            volts[i] = int(usb_readline(ser))

        print(f"Received {n} time and volt samples...")

        # Set times to be elapsed time & scale to seconds
        times -= times[0]
        times *= 1e-9

        # Scale volts to fall between 0 and 3.3V
        volts /= 65535
        volts *= 3.3

        # Create a plot window with a black background
        plt.figure("sig_gen.py")
        ax = plt.axes()
        ax.set_facecolor("black")

        # Plot the graph on the main axes
        ax.plot(times, volts, color="magenta", linewidth=2)

        # Give the graph a title and axis labels
        ax.set_title("AD9833 Signal Generator")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")

        ax.xaxis.set_major_locator(MaxNLocator(11))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.3f"))
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))

        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(0.25))

        ax.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)

        ax.axhline(0, color="gray", linestyle="--", alpha=0.65)
        ax.axhline(3.3, color="red")

        mean_volts = np.mean(volts)
        ax.axhline(mean_volts, color="yellow", linestyle="--", alpha=0.65)

        ax.axvline(0.0, color="yellow", linestyle="--", alpha=0.65)
        ax.axvline(1.0, color="yellow", linestyle="--", alpha=0.65)

        # Save these samples for comparison with the omp_amp lab
        np.savetxt("ad9833_volts.txt", volts)

        # Show the plot window
        ax.figure.set_size_inches(10, 8)
        plt.savefig("sig_gen.png", dpi=600)
        plt.show()

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
