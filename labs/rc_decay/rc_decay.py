# rc_decay.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.collections import LineCollection
import serial
import adafruit_board_toolkit.circuitpython_serial

# Open the USB data port
cdc_data = adafruit_board_toolkit.circuitpython_serial.data_comports()[0]
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
ser.port = cdc_data.device
ser.open()

# Send to MCU the command to (r)un the experiment
ser.write(b"r\n")
ser.flush()
print("RC Decay experiment is running...")

# Read from MCU the number of samples
n = int(ser.readline().decode("ASCII").strip())

# Declare numpy arrays to store the samples
times = np.zeros(n, float)
volts = np.zeros(n, float)

# Read from MCU the times and volts samples into arrays
for i in range(n):
    times[i] = int(ser.readline().decode("ASCII").strip())
for i in range(n):
    volts[i] = int(ser.readline().decode("ASCII").strip())
print(f"Received {n} time and volt samples...")

# Close the USB connection to the KB2040
ser.close()

# Set times to be elapsed time & scale to seconds
times -= times[0]
times *= 1e-9

# Find the middle time value
mid_time = times[-1] / 2

# Scale volts to fall between 0 and 3.3V
volts /= 65535
volts *= 3.3

# Calculate theoretical performance curve
V_s = 3.3  # Volts
R = 10_121  # Ohms
C = 0.00001069  # Farads
tau = R * C
t = np.linspace(0, mid_time, 100)
v1_c = V_s * (1 - np.exp(-t / tau))  # Charge
v2_c = V_s * np.exp(-t / tau)  # Decay

# Create a plot window
plt.figure("rc_decay.py")
plt.gca().set_facecolor("black")

# Plot actual voltage
plt.plot(times, volts, color="magenta", linewidth=2, label="Actual")

# Plot theoretical voltage
plt.plot(t, v1_c, color="cyan", linewidth=2, label="Theory")
plt.plot(t + mid_time, v2_c, color="cyan", linewidth=2)

# Give the graph a title, axis labels, and display the legend
plt.title("Capacitor Voltage vs. Time")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()

# Set tick marks
plt.gca().xaxis.set_major_locator(MaxNLocator(11))
plt.gca().xaxis.set_major_formatter(FormatStrFormatter("%.3f"))
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().xaxis.set_major_locator(MultipleLocator(0.25))
plt.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)

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
plt.gca().add_collection(lc)
plt.axvline(0.1, color="yellow", linestyle=(0, (5, 6)), alpha=0.65)
plt.axvline(mid_time + 0.1, color="yellow", linestyle=(0, (5, 6)), alpha=0.65)
plt.show()
