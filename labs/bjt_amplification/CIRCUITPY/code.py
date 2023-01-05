# bjt_amplification for KB2040

# Uses PN2222A BJT
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
pixel_builtin.brightness = 0.3
pixel_builtin.fill((0, 255, 0))  # GREEN

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
    n = 450
    volts_be = [float] * n  # Base-Emitter voltage
    volts_ce = [float] * n  # Collector-Emitter voltage

    # Read volts from ADC
    for i in range(n):
        # Set DAC output voltage which is the volts between
        # the BJT base and emitter as emitter is at GND
        dac.raw_value = 572 + i
        volts_be[i] = dac.raw_value / 4096 * 3.3
        # Read the voltage drop across the collector's resistor
        volts_ce[i] = adc_chan.voltage

    # Turn off DAC voltage to circuit
    dac.raw_value = 0

    # Transfer data over USB
    pixel_builtin.fill((255, 255, 0))  # YELLOW
    usb_writeline(ser, n)  # number of samples
    for val in volts_be:
        usb_writeline(ser, val)  # Base-Emitter volts array
    for val in volts_ce:
        usb_writeline(ser, val)  # Collector-Emitter volts array
    pixel_builtin.fill((0, 255, 0))  # GREEN


while True:
    cmd = ser.readline().strip().decode("utf-8")
    if cmd == "r":
        read_samples()
