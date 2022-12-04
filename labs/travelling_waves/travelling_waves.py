# travelling_wave.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from collections import namedtuple

WaveParms = namedtuple("WaveParms", ["Amplitude", "WaveNumber", "Omega"])

wave1_params = WaveParms(Amplitude=0, WaveNumber=0, Omega=0)
wave2_params = WaveParms(Amplitude=0, WaveNumber=0, Omega=0)

wave1, wave2, wave3 = [], [], []

xa = np.linspace(0, 6 * np.pi, 600)


def plot(ax, show_waves):
    global wave1, wave2, wave3

    ya1 = wave1_params.Amplitude * np.sin(wave1_params.WaveNumber * xa)
    ya2 = wave2_params.Amplitude * np.sin(wave2_params.WaveNumber * xa)
    ya3 = (ya1 + ya2) / 2

    if show_waves:
        (wave1,) = ax.plot(xa, ya1, color="blue", label="wave 1")
        (wave2,) = ax.plot(xa, ya2, color="red", label="wave 2")
    else:
        (wave1,) = ax.plot(xa, ya1, color="white")
        (wave2,) = ax.plot(xa, ya2, color="white")

    # Plot the liner superposition (sum) of wave1 and wave2
    (wave3,) = ax.plot(xa, ya3, color="black", label="sum")

    ax.set_title("Travelling Waves")
    ax.set_xlabel("Location")
    ax.set_ylabel("Amplitude")

    ax.legend(loc="upper right")


def anim_frame_counter():
    n = 0
    while n < 160:  # 4 secs at 40 frames/sec
        n += 1
        yield n


def anim_draw_frame(t):
    ya1 = wave1_params.Amplitude * np.sin(
        wave1_params.WaveNumber * xa + wave1_params.Omega * t
    )
    wave1.set_data(xa, ya1)
    ya2 = wave2_params.Amplitude * np.sin(
        wave2_params.WaveNumber * xa + wave2_params.Omega * t
    )
    wave2.set_data(xa, ya2)
    ya3 = (ya1 + ya2) / 2
    wave3.set_data(xa, ya3)
    return wave1, wave2, wave3


def plot_waves(label, show_waves):
    plt.figure(label)
    ax = plt.axes()

    plot(ax, show_waves)

    anim = FuncAnimation(
        ax.figure,
        anim_draw_frame,
        anim_frame_counter,
        interval=25,
        blit=False,
        repeat=False,
    )

    plt.show()


def main():
    global wave1_params, wave2_params

    mode = 1

    if mode == 1:
        # Wave 2 has zero amplitude, zero wave number, and zero velocity
        wave1_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 16)
        wave2_params = WaveParms(Amplitude=0, WaveNumber=0, Omega=0)
        plot_waves("Mode 1", show_waves=True)
    elif mode == 2:
        # Wave 2 has half amplitude, same wave number, same wave velocity
        wave1_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 16)
        wave2_params = WaveParms(Amplitude=1 / 2, WaveNumber=1, Omega=1 / 16)
        plot_waves("Mode 2", show_waves=True)
    elif mode == 3:
        # Wave 2 has same amplitude, half wave number, same wave velocity
        wave1_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 16)
        wave2_params = WaveParms(Amplitude=1, WaveNumber=1 / 2, Omega=1 / 16)
        plot_waves("Mode 3", show_waves=True)
    elif mode == 4:
        # Wave 2 has same amplitude, same wave number, half wave velocity
        wave1_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 16)
        wave2_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 8)
        plot_waves("Mode 4", show_waves=True)
    elif mode == 5:
        # Wave 2 has same amplitude, same wave number, *negative* half wave velocity
        wave1_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 16)
        wave2_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=-1 / 8)
        plot_waves("Mode 5", show_waves=True)
    elif mode == 6:
        # Wave 2 now same amplitude, same wave number, *negative* wave velocity
        wave1_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 16)
        wave2_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=-1 / 16)
        plot_waves("Mode 6", show_waves=True)
    elif mode == 7:
        # Wave 2 now same amplitude, same wave number, *negative* wave velocity
        # and we show only the linear superposition of both waves
        wave1_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=1 / 16)
        wave2_params = WaveParms(Amplitude=1, WaveNumber=1, Omega=-1 / 16)
        plot_waves("Mode 7", show_waves=False)


main()
