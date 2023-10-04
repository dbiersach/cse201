# rlc_driven.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter


def calc_rms(w):
    Emf = 1.21  # Potential in Volts
    R1, R2 = 10.05, 99.32  # Resistance in Ohms
    R = R1 + R2  # Total Resistance in Ohms

    L = 100.8e-3  # Inductance in Henries
    C = 91.2e-9  # Capacitance in Farads

    Q = C * Emf  # Initial capacitor charge
    I = 0.0  # Initial capacitor current is zero
    V = 0.0  # Initial capacitor voltage is zero

    t = 0.0
    tf = 1.0  # End time in seconds
    dt = 0.00001
    n = (tf - t) / dt  # Number of intervals

    while t < tf:  # Simulate circuit
        alpha = (Emf * np.sin(w * t) - I * R - Q / C) / L
        I = I + alpha * dt
        Q = Q + I * dt
        V = V + (I * R1) ** 2  # Voltage through R1
        t = t + dt

    return np.sqrt(V / n)  # RMS value


omega = np.linspace(5, 30_000, 2000)  # Angular frequency
volts = calc_rms(omega) + 0.017  # Due to AD9833 DC offset

freq = omega / 2 / np.pi / 1000  # Rad/s to kHz

max_volt = np.max(volts)
print(f"Resonance voltage = {max_volt:0.4f} V")

resonance_freq = freq[np.argmax(volts)]
print(f"Resonance freq = {resonance_freq:0.4f} kHz")

plt.figure("rlc_driven.py")
plt.gca().set_facecolor("black")
plt.plot(freq, volts, color="magenta", linewidth=2)
plt.vlines(resonance_freq, 0, max_volt, color="yellow", linewidth=2)
plt.title("RLC Circuit Resonance (Simulated)")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Voltage (V)")
plt.xlim(-0.2, 5.2)
plt.ylim(0, 0.1)
plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
plt.gca().xaxis.set_major_formatter(FormatStrFormatter("%0.3f"))
plt.show()
