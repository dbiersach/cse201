# rlc_resonance for KB2040

# Uses AITRIP AD9833 Signal Generator
# Uses TLV2462 Omp Amp
# Uses 10 Ohm & 100 Ohm Resistor (R) Voltage Divider
# Uses 100 mH inductor (L)
# Uses 100nF capacitor (C)


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
wave_gen.reset()
wave_gen.update_freq(1000)  # Hz
wave_gen.start()

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
    n = 500
    freq = [float] * n
    volts = [float] * n

    # Read voltage samples
    pixel_builtin.fill((255, 0, 0))
    for i in range(n):
        # Set new sine wave frequency
        freq[i] = i * 10
        wave_gen.update_freq(freq[i])
        wave_gen.start()
        time.sleep(0.10)
        # Read 10,000 ADC samples at current frequency
        v = 0
        for _ in range(10_000):
            v += pin_adc.value
        # Find average ADC reading and covert to volts
        volts[i] = v / 10_000 / 65536 * 3.3

    # Transfer data over USB data port
    pixel_builtin.fill((255, 255, 0))  # YELLOW
    usb_writeline(ser, n)  # number of samples
    # Send times and volts array elements
    for val in freq:
        usb_writeline(ser, val)  # freq array
    for val in volts:
        usb_writeline(ser, val)  # volts array
    pixel_builtin.fill((0, 255, 0))  # GREEN


while True:
    cmd = ser.readline().strip().decode("utf-8")
    if cmd == "r":
        read_samples()
