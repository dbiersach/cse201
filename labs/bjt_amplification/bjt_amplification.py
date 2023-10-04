# bjt_amplification.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
import serial
import sys


# Open the USB data port
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
if sys.platform == "win32":
    ser.port = "COM10"
if sys.platform == "darwin":
    ser.port = "/dev/tty.usbserial-110"
ser.open()

# Send MCU the command to (r)un the experiment
ser.write(b"r\n")
print("Transistor Amplification experiment is running...")

# Read samples from USB into arrays
n = int(ser.readline().decode("ASCII").strip())
volts_be = np.zeros(n, float)
volts_ce = np.zeros(n, float)
for i in range(n):
    volts_be[i] = float(ser.readline().decode("ASCII").strip())
for i in range(n):
    volts_ce[i] = float(ser.readline().decode("ASCII").strip())
ser.close()
print(f"Received {n} BE volt and CE volt samples...")

plt.figure("bjt_amplification.py")
plt.gca().set_facecolor("black")
plt.plot(volts_be, volts_ce, color="yellow", linewidth=2)
plt.title("PN2222A (NPN) BJT Amplification")
plt.xlabel("Base-Emitter Voltage (V)")
plt.ylabel("Collector-Emitter Voltage (V)")
plt.gca().xaxis.set_major_locator(MultipleLocator(0.02))
plt.gca().xaxis.set_major_formatter(FormatStrFormatter("%.2f"))
plt.gca().yaxis.set_major_locator(MultipleLocator(0.2))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
plt.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)
plt.show()
