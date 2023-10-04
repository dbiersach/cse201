# sig_gen.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FormatStrFormatter
import serial
import sys


# Open the USB data port
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
if sys.platform == "win32":
    ser.port = "COM10"
if sys.platform == "darwin":
    ser.port = "/dev/tty.usbserial-110"
ser.open()

# Send to MCU the command to (r)un the experiment
ser.write(b"r\n")
ser.flush()
print("Signal Generator experiment is running...")

# Read times and volts samples from KB2040 into arrays
n = int(ser.readline().decode("ASCII").strip())
times = np.zeros(n, float)
volts = np.zeros(n, float)
for i in range(n):
    times[i] = int(ser.readline().decode("ASCII").strip())
for i in range(n):
    volts[i] = int(ser.readline().decode("ASCII").strip())
print(f"Received {n} time and volt samples...")
ser.close()

# Set times to be elapsed time & scale to seconds
times -= times[0]
times *= 1e-9
# Scale volts to fall between 0 and 3.3V
volts /= 65535
volts *= 3.3

# Save these samples for comparison with the omp_amp lab
np.savetxt("ad9833_volts.txt", volts)

# Create a plot window with a black background
plt.figure("sig_gen.py")
plt.gca().set_facecolor("black")

plt.plot(times, volts, color="magenta", linewidth=2)

plt.title("AD9833 Signal Generator")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")

plt.gca().xaxis.set_major_locator(MaxNLocator(11))
plt.gca().xaxis.set_major_formatter(FormatStrFormatter("%.3f"))
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().yaxis.set_major_locator(MultipleLocator(0.25))

plt.grid(which="both", color="gray", linestyle="dotted", alpha=0.5)

plt.axhline(0, color="gray", linestyle="--", alpha=0.65)
plt.axhline(3.3, color="red")
plt.axhline(np.mean(volts), color="yellow", linestyle="--", alpha=0.65)
plt.axvline(0.0, color="yellow", linestyle="--", alpha=0.65)
plt.axvline(1.0, color="yellow", linestyle="--", alpha=0.65)

plt.show()
