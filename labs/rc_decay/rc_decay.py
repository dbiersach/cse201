# rc_decay.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.collections import LineCollection
import serial
import traceback
import sys


def usb_readline(usb_data_port):
    s = usb_data_port.readline().decode("ASCII").strip()
    return s


def main():
    ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
    try:
        # Open the USB data port
        port = "COM5"
        if sys.platform == "linux":
            port = "/dev/ttyAMA0"
        if sys.platform == "darwin":
            port = "/dev/tty.usbserial-110"
        ser.port = port
        ser.open()

        # Send to MCU the command to (r)un the experiment
        ser.write(b"r\n")
        ser.flush()
        print("RC Decay experiment is running...")

        # Read from MCU the number of samples
        n = int(usb_readline(ser))

        # Declare numpy arrays to store the samples
        times = np.zeros(n, float)
        volts = np.zeros(n, float)

        # Read from MCU the times and volts samples into arrays
        for i in range(n):
            times[i] = int(usb_readline(ser))
        for i in range(n):
            volts[i] = int(usb_readline(ser))

        print(f"Received {n} time and volt samples...")

        # Set times to be elapsed time & scale to seconds
        times -= times[0]
        times *= 1e-9

        # Find the middle time value
        mid_time = times[-1] / 2

        # Scale volts to fall between 0 and 3.3V
        volts /= 65535
        volts *= 3.3

        # Create a plot window
        plt.figure("rc_decay.py")
        ax = plt.axes()
        ax.set_facecolor("black")

        # Plot the measured voltage curve
        ax.plot(times, volts, color="magenta", linewidth=2, label="Actual")

        # Plot theoretical charge & decay curves
        V_s = 3.3  # Volts
        R = 10_121  # Ohms
        C = 0.00001069  # Farads
        tau = R * C
        # Charge curve (rise time)
        t = np.linspace(0, mid_time, 100)
        v_c = V_s * (1 - np.exp(-t / tau))
        ax.plot(t, v_c, color="cyan", linewidth=2, label="Theory")
        # Decay curve (fall time)
        t = np.linspace(0, mid_time, 100)
        v_c = V_s * np.exp(-t / tau)
        ax.plot(t + mid_time, v_c, color="cyan", linewidth=2)

        # Give the graph a title, axis labels, and display the legend
        ax.set_title("Capacitor Voltage vs. Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        ax.legend()

        # Set tick marks
        ax.xaxis.set_major_locator(MaxNLocator(11))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.3f"))
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(0.25))
        ax.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)

        # Create straight lines to depict charging pin status over time
        line_on = [(0, 0), (0, 3.3)]
        line_charging = [(0, 3.3), (mid_time, 3.3)]
        line_off = [(mid_time, 3.3), (mid_time, 0)]
        line_discharging = [(mid_time, 0), (times[-1], 0)]
        lc = LineCollection(
            [line_on, line_charging, line_off, line_discharging],
            color="yellow",
            linewidth=2,
            zorder=2.5,
        )
        ax.add_collection(lc)
        ax.axvline(0.1, color="yellow", linestyle=(0, (5, 6)), alpha=0.65)
        ax.axvline(mid_time + 0.1, color="yellow", linestyle=(0, (5, 6)), alpha=0.65)

        # Set figure size and save as a PNG image file
        ax.figure.set_size_inches(10, 8)
        plt.savefig("rc_decay.png", dpi=600)
        plt.show()

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
