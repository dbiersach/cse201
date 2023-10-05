# diode_ivcurve.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
import serial
import adafruit_board_toolkit.circuitpython_serial

# Open the USB data port
cdc_data = adafruit_board_toolkit.circuitpython_serial.data_comports()[0]
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
ser.port = cdc_data.device
ser.open()

# Send MCU the command to (r)un the experiment
ser.write(b"r\n")
print("Diode I-V Curve experiment is running...")

# Read volts and amps samples from USB into arrays
n = int(ser.readline().decode("ASCII").strip())
volts = np.zeros(n, float)
amps = np.zeros(n, float)
for i in range(n):
    volts[i] = float(ser.readline().decode("ASCII").strip())
for i in range(n):
    amps[i] = float(ser.readline().decode("ASCII").strip())
ser.close()
print(f"Received {n} volt and amp samples...")

# Plot the graph on the main axes
plt.figure("diode_ivcurve.py")
plt.gca().set_facecolor("black")
plt.plot(volts, amps, color="yellow", linewidth=2)
plt.title("1N4001 Diode I-V Characteristic Curve")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (mA)")
plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
plt.gca().xaxis.set_major_formatter(FormatStrFormatter("%.2f"))
plt.gca().yaxis.set_major_locator(MultipleLocator(1.0))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
plt.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)
plt.show()
