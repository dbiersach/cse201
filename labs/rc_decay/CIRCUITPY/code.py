 # rc_decay for KB2040

# Uses 10K ohm resistor (1/2 watt, 1% tolerance)
# Uses 10uF 25V electrolytic capacitor (20% tolerance)

import analogio
import board
import digitalio
import neopixel
import time
import supervisor
import usb_cdc

# Wait until USB console port is ready
while not supervisor.runtime.usb_connected:
    pass

# Configure pins
pin_adc = analogio.AnalogIn(board.A1)
pin_charge = digitalio.DigitalInOut(board.D4)
pin_charge.direction = digitalio.Direction.OUTPUT

# Configure NeoPixel
pixel_builtin = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel_builtin.brightness = 0.1
pixel_builtin.fill((0, 255, 0))  # GREEN

# Create USB data port
ser = usb_cdc.data


def usb_writeline(usb_data_port, x):
    usb_data_port.write(bytes(str(x) + "\n", "utf-8"))
    usb_data_port.flush()


def read_samples():
    # Set number of samples (NOT number of seconds!)
    n1 = 1000
    n2 = n1 * 2
    volts = [int] * n2
    times = [int] * n2

    # Drain circuit (discharge capacitor)
    pixel_builtin.fill((0, 0, 255))  # BLUE
    pin_charge.value = False
    time.sleep(5)

    # Energize circuit (charge capacitor)
    pixel_builtin.fill((255, 0, 0))  # RED
    pin_charge.value = True
    for i in range(n1):
        volts[i] = pin_adc.value
        times[i] = time.monotonic_ns()
        time.sleep(0.001)

    # Drain circuit (discharge capacitor)
    pin_charge.value = False
    for i in range(n1, n2):
        volts[i] = pin_adc.value
        times[i] = time.monotonic_ns()
        time.sleep(0.001)

    # Transfer data over USB
    pixel_builtin.fill((255, 255, 0))  # YELLOW
    # Send number of samples
    usb_writeline(ser, n2)  # number of samples
    for val in times:
        usb_writeline(ser, val)  # times array
    for val in volts:
        usb_writeline(ser, val)  # volts array
    pixel_builtin.fill((0, 255, 0))  # GREEN


while True:
    cmd = ser.readline().strip().decode("utf-8")
    if cmd == "r":
        read_samples()
