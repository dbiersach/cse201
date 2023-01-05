# diode_ivcurve for KB2040

# Uses 1N4001 Diode & 330 Ohm Resistor
# Uses MCP4725 DAC
# Uses ADS1115 ADC

import board
import busio
import neopixel
import supervisor
import usb_cdc
import adafruit_mcp4725
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Wait until USB console port is ready
while not supervisor.runtime.usb_connected:
    pass

# Initialize I2C bus
i2c_bus = busio.I2C(board.A3, board.A2)

# Configure MCP4725 DAC
dac = adafruit_mcp4725.MCP4725(i2c_bus)
dac.raw_value = 0

# Configure ADS1115 ADC in differential mode (P0+, P1-)
adc = ADS.ADS1115(i2c_bus)
adc_chan = AnalogIn(adc, ADS.P0, ADS.P1)

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

    # Read 100 dummy values to initialize ADC
    for _ in range(100):
        _ = adc_chan.voltage

    # Set number of samples (NOT number of seconds!)
    n = 512
    volts = [float] * n
    amps = [float] * n

    # Read volts from ADC
    for i in range(n):
        # Set DAC output voltage
        dac.raw_value = i * 4
        volts[i] = dac.raw_value / 4096 * 3.3
        # Calculate current (mA) through 10 ohm resistor
        amps[i] = adc_chan.voltage / 10 * 1000

    # Turn off DAC voltage to circuit
    dac.raw_value = 0

    # Transfer data over USB
    pixel_builtin.fill((255, 255, 0))  # YELLOW
    usb_writeline(ser, n)  # number of samples
    for val in volts:
        usb_writeline(ser, val)  # volts array
    for val in amps:
        usb_writeline(ser, val)  # amps array
    pixel_builtin.fill((0, 255, 0))  # GREEN


while True:
    cmd = ser.readline().strip().decode("utf-8")
    if cmd == "r":
        read_samples()
