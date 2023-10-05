# op_amp.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FormatStrFormatter
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
print("Op-Amp experiment is running...")

# Read times and volts samples from KB2040 into arrays
n = int(ser.readline().decode("ASCII").strip())
times = np.zeros(n, float)
volts_opamp = np.zeros(n, float)
for i in range(n):
    times[i] = int(ser.readline().decode("ASCII").strip())
for i in range(n):
    volts_opamp[i] = int(ser.readline().decode("ASCII").strip())
print(f"Received {n} time and volt samples...")
ser.close()

# Set times to be elapsed time & scale to seconds
times -= times[0]
times *= 1e-9
# Scale volts to fall between 0 and 3.3V
volts_opamp /= 65535
volts_opamp *= 3.3

# Read in the volts from the raw AD9833 (before amplification)
volts_ad9833 = np.genfromtxt("ad9833_volts.txt")

plt.figure("op_amp.py")
plt.gca().set_facecolor("black")

plt.plot(times, volts_ad9833, color="magenta", linewidth=2, label="AD9833")
plt.plot(times, volts_opamp, color="lime", linewidth=2, label="AD9833+TLV2462")
plt.legend()

plt.title("TLV2462 Operational Amplifier")
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
plt.axhline(np.mean(volts_opamp), color="yellow", linestyle="--", alpha=0.65)
plt.axvline(0.0, color="yellow", linestyle="--", alpha=0.65)
plt.axvline(1.0, color="yellow", linestyle="--", alpha=0.65)

plt.show()
