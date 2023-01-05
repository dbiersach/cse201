# op_amp for KB2040

# Uses AITRIP AD9833 Signal Generator
# Uses TLV2462 Omp Amp

import analogio
import board
import neopixel
import time
import supervisor
import usb_cdc
import ad9833

# Wait until USB console port is ready
while not supervisor.runtime.usb_connected:
    pass

# Configure analog input pin (from AD9833)
pin_adc = analogio.AnalogIn(board.A0)

# Configure AITRIP AD9833 Signal Generator
wave_gen = ad9833.AD9833(select="D10")

# Configure NeoPixel
pixel_builtin = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel_builtin.brightness = 0.1
pixel_builtin.fill((0, 255, 0))  # Green

# Create USB data port
ser = usb_cdc.data


def usb_writeline(usb_data_port, x):
    usb_data_port.write(bytes(str(x) + "\n", "utf-8"))
    usb_data_port.flush()


def read_samples():
    pixel_builtin.fill((255, 0, 0))  # RED

    # Set number of samples (NOT number of seconds!)
    n = 2000
    volts = [int] * n
    times = [int] * n

    # Start generating 10 Hz sine waves
    wave_gen.reset()
    wave_gen.update_freq(10)  # Hz
    wave_gen.start()

    # Read voltage samples
    for i in range(n):
        times[i] = time.monotonic_ns()
        volts[i] = pin_adc.value
        time.sleep(0.001)

    # Transfer data over USB data port
    pixel_builtin.fill((255, 255, 0))  # YELLOW
    usb_writeline(ser, n)  # number of samples
    for val in times:
        usb_writeline(ser, val)  # times array
    for val in volts:
        usb_writeline(ser, val)  # volts array
    pixel_builtin.fill((0, 255, 0))  # GREEN


while True:
    cmd = ser.readline().strip().decode("utf-8")
    if cmd == "r":
        read_samples()
