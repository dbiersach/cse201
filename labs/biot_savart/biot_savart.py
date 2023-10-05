# biot_savart.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import serial
import adafruit_board_toolkit.circuitpython_serial


def fit_linear(x, y):
    m = len(x) * np.sum(x * y) - np.sum(x) * np.sum(y)
    m = m / (len(x) * np.sum(x**2) - np.sum(x) ** 2)
    b = (np.sum(y) - m * np.sum(x)) / len(x)
    return m, b


# Open the USB data port
cdc_data = adafruit_board_toolkit.circuitpython_serial.data_comports()[0]
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
ser.port = cdc_data.device
ser.open()

# Send MCU the command to (r)un the experiment
ser.write(b"r\n")
print("Biot-Savart experiment is running...")
print("This experiment may take up 90 seconds to complete...")

# Read samples into arrays
n = int(ser.readline().decode("ASCII").strip())
current = np.zeros(n, float)
field_strength = np.zeros(n, float)
for i in range(n):
    current[i] = float(ser.readline().decode("ASCII").strip())
for i in range(n):
    field_strength[i] = float(ser.readline().decode("ASCII").strip())
ser.close()
print(f"Received {n} current and field_strength samples...")

# Create a plot window with a black background
plt.figure("biot_savart.py")
ax = plt.axes()
plt.gca().set_facecolor("black")

# Plot the samples
plt.scatter(current, field_strength, marker=".", color="yellow", label="Sensor Data")

# Plot line of best fit using linear regression
x = np.linspace(np.min(current), np.max(current), 1000)
m, b = fit_linear(current, field_strength)
plt.plot(x, m * x + b, label="Linear")

plt.title("Biot-Savart Law")
plt.xlabel("Current (mA)")
plt.ylabel("Magnetic Field Strength (uT)")
plt.legend()
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))
plt.show()
