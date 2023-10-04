# measure_resistor for KB2040

# Uses IN219 I2C Current Sensor
# Uses MCP4725 DAC
# Uses ADS1115 ADC
# Uses 2N2222 BJT

import board
import busio
import neopixel
import supervisor
import usb_cdc
from adafruit_ina219 import ADCResolution, BusVoltageRange, Gain, INA219
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
dac.raw_value = 850

# Configure IN219 current sensor
ina219 = INA219(i2c_bus)
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V
ina219.gain = Gain.DIV_8_320MV
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_128S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_128S

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

    # Set number of samples (NOT number of seconds!)
    n = 50
    volts = [float] * n
    amps = [float] * n

    # Read 100 dummy values to initialize ADC
    for _ in range(100):
        _ = adc_chan.voltage

    # Read samples from sensors
    for i in range(n):
        # Set DAC output voltage (goes into base of BJT)
        dac.raw_value = 850 + 2 * i

        # Calculate average sensor values using 100 samples
        v, a = 0, 0
        for _ in range(100):
            # Read voltage drop across load resistor
            v += adc_chan.voltage
            # Read current flowing through load resistor
            a += ina219.current

        # Calculate average value for volts & amps
        volts[i] = v / 100
        a = a / 100
        # Convert milliamps to amps
        a = a / 1000
        # Adjust for 219a chip inaccuracy
        a = a - 0.13 * a
        amps[i] = a

    # Turn off DAC voltage to base pin of BJT
    dac.raw_value = 0

    # Transfer data over USB
    pixel_builtin.fill((255, 255, 0))  # YELLOW
    usb_writeline(ser, n)  # number of samples
    for val in volts:
        usb_writeline(ser, val)  # times array
    for val in amps:
        usb_writeline(ser, val)  # times array
    pixel_builtin.fill((0, 255, 0))  # Green


while True:
    cmd = ser.readline().strip().decode("utf-8")
    if cmd == "r":
        read_samples()
