# measure_resistor.py

import numpy as np

import serial
import traceback
import sys


def usb_readline(usb_data_port):
    s = usb_data_port.readline().decode("ASCII").strip()
    return s


def main():
    resistor_num = 0
    while resistor_num == 0:
        try:
            print("Which resistor are you measuring? (1, 2, or 3)", end=": ")
            n = int(input())
            if n < 1 or n > 3:
                raise ValueError()
            resistor_num = n
        except ValueError:
            print("Please enter a 1, 2, or 3")

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
        print(f"Measuring voltage vs. current for Resistor #{resistor_num}")
        print("This experiment may take up 90 seconds to complete...")

        # Read number of samples from USB
        n = int(usb_readline(ser))

        # Declare numpy arrays to store the samples
        volts = np.zeros(n, float)
        amps = np.zeros(n, float)

        # Read times and volts samples from USB into arrays
        for i in range(n):
            volts[i] = float(usb_readline(ser))
        for i in range(n):
            amps[i] = float(usb_readline(ser))

        file_name = f"resistor{resistor_num}.csv"

        np.savetxt(
            file_name,
            np.vstack((volts, amps)).T,
            fmt="%6.3f",
            delimiter=", ",
        )

        print(f"{file_name} created.")

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
