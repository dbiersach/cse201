# space_signals.py

import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def plot_samples(ax, ts, ys):
    num_samples = ts.size
    ax.plot(ts, ys, color="lightgray")
    ax.set_title(f"Sampled Wave ({num_samples} samples)")
    ax.set_xlabel("scaled time", loc="right")
    ax.set_ylabel("amplitude")


def plot_dft(ax, ct):
    num_terms = 40
    ax.bar(
        range(0, num_terms),
        abs(ct.real[:num_terms]),
        color="blue",
        label="cosine",
        zorder=2,
    )
    ax.bar(
        range(0, num_terms),
        abs(ct.imag[:num_terms]),
        color="red",
        label="sine",
        zorder=2,
    )

    ax.grid(which="major", axis="x", color="black", linewidth=1)
    ax.grid(which="minor", axis="x", color="lightgray", linewidth=1)
    ax.grid(which="major", axis="y", color="black", linewidth=1)
    ax.grid(which="minor", axis="y", color="lightgray", linewidth=1)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_title("Fast Fourier Transform")
    ax.set_xlabel("frequency", loc="right")
    ax.set_ylabel("amplitude")
    ax.legend(loc="best")


def plot_idft(ax, ts, yr):
    num_samples = ts.size
    ax.plot(ts, yr, color="purple")
    ax.set_title(f"Inverse FFT ({num_samples} samples)")
    ax.set_xlabel("scaled time", loc="right")
    ax.set_ylabel("amplitude")


def plot_power_spectrum(ax, ct):
    num_terms = 40
    ax.bar(
        range(0, num_terms), abs(ct[:num_terms]), color="green", label="sine", zorder=2
    )
    ax.grid(which="major", axis="x", color="black", linewidth=1)
    ax.grid(which="minor", axis="x", color="lightgray", linewidth=1)
    ax.grid(which="major", axis="y", color="black", linewidth=1)
    ax.grid(which="minor", axis="y", color="lightgray", linewidth=1)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_title("Power Spectrum")
    ax.set_xlabel("frequency", loc="right")
    ax.set_ylabel(r"$\Vert amplitude \Vert$")


def main():
    file_name = "space_signal1"
    #file_name = "space_signal2"
    #file_name = "space_signal3"

    plt.rcParams["figure.constrained_layout.use"] = True
    fig, (((ax1), (ax2)), ((ax3), (ax4))) = plt.subplots(2, 2)
    fig.canvas.manager.set_window_title(file_name)
    fig.set_size_inches(12, 8)

    samples = np.genfromtxt(file_name + ".csv", delimiter=",")
    ts = samples[:, 0]
    ys = samples[:, 1]

    ct = fft(ys) / (len(ys) / 2)
    yr = ifft(ct)

    plot_samples(ax1, ts, ys)
    plot_dft(ax2, ct)
    plot_idft(ax3, ts, yr)
    plot_power_spectrum(ax4, ct)

    fig.savefig(f"{file_name}.png", dpi=600)
    plt.show()


main()
