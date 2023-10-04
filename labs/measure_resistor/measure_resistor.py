# measure_resistor.py

import numpy as np
import serial
import sys

# Ask user which resistor they are measuring
# Note: 47Ω=1, 56Ω=2, or 68Ω=3
resistor_num = input("Which resistor are you measuring (1, 2, or 3)?")

# Open the USB data port
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
if sys.platform == "win32":
    ser.port = "COM10"
if sys.platform == "darwin":
    ser.port = "/dev/tty.usbserial-110"
ser.open()

# Send MCU the command to (r)un the experiment
ser.write(b"r\n")
print(f"Measuring voltage vs. current for Resistor #{resistor_num}")
print("This experiment may take up 90 seconds to complete...")

# Read number of samples from USB
n = int(ser.readline().decode("ASCII").strip())

# Declare numpy arrays to store the samples
volts = np.zeros(n, float)
amps = np.zeros(n, float)

# Read times and volts samples from USB into arrays
for i in range(n):
    volts[i] = float(ser.readline().decode("ASCII").strip())
for i in range(n):
    amps[i] = float(ser.readline().decode("ASCII").strip())
ser.close()

# Save measured resistance values to a CSV file
file_name = f"resistor{resistor_num}.csv"
np.savetxt(
    file_name,
    np.vstack((volts, amps)).T,
    fmt="%6.3f",
    delimiter=", ",
)
print(f"{file_name} created.")
