# rlc_resonance.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter
import serial
import adafruit_board_toolkit.circuitpython_serial

# Open the USB data port
cdc_data = adafruit_board_toolkit.circuitpython_serial.data_comports()[0]
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
ser.port = cdc_data.device
ser.open()

# Send MCU the command to (r)un the experiment
ser.write(b"r\n")
print("RLC Resonance experiment is running...")
print("This experiment will take 2 minutes to complete...")

# Read frequencies and volts samples from USB into arrays
n = int(ser.readline().decode("ASCII").strip())
freq = np.zeros(n, float)
volts = np.zeros(n, float)
for i in range(n):
    freq[i] = float(ser.readline().decode("ASCII").strip())
for i in range(n):
    volts[i] = float(ser.readline().decode("ASCII").strip())
ser.close()
print(f"Received {n} frequency and voltage samples...")

freq = freq / 1000  # Convert to kHz

# Resonant frequency is at the peak voltage
max_volt = np.max(volts)
print(f"Resonance voltage = {max_volt:0.4f} V")

resonance_freq = freq[np.argmax(volts)]
print(f"Resonance freq = {resonance_freq:0.4f} kHz")

# Plot the graph on the main axes
plt.figure("rlc_resonance.py")
plt.gca().set_facecolor("black")
plt.plot(freq, volts, color="magenta", linewidth=2)

# Plot resonant frequency
plt.vlines(resonance_freq, 0, max_volt, color="yellow", linewidth=2)

plt.title("RLC Circuit Resonance (Actual)")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Voltage (V)")
plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
plt.gca().xaxis.set_major_formatter(FormatStrFormatter("%0.3f"))
plt.xlim(-0.2, 5.2)
plt.ylim(0, 0.1)
plt.show()
