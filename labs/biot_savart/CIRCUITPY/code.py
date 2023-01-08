# biot_savart for KB2040

# Uses DRV8833 Motor Driver
# Uses MMC5603 Triple-axis Magnetometer
# Uses 5V Electromagnet - 5 Kg Holding Force [P25-20]

import adafruit_mmc56x3
import analogio
import board
import busio
import digitalio
import pwmio
import neopixel
import supervisor
import time
import usb_cdc
from adafruit_motor import motor
from math import sqrt

# Wait until USB console port is ready
while not supervisor.runtime.usb_connected:
    pass

# Configure analog input pin
pin_adc = analogio.AnalogIn(board.A0)

# Configure NeoPixel
pixel_builtin = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel_builtin.brightness = 0.1
pixel_builtin.fill((0, 255, 0))  # Green

# Initialize I2C bus
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Configure MMC5603 Triple-axis Magnetometer
magnetometer = adafruit_mmc56x3.MMC5603(i2c_bus)

# Configure DRV8833 DC/Stepper Motor Driver
motor_pwm_1 = pwmio.PWMOut(board.D9, frequency=4150)
motor_pwm_2 = pwmio.PWMOut(board.D8, frequency=4150)
motor_driver = motor.DCMotor(motor_pwm_1, motor_pwm_2)
motor_driver.decay_mode = motor.SLOW_DECAY
# Initialize motor driver to 10% of Vcc
motor_driver.throttle = 0.1
# Take motor driver out of sleep mode
motor_sleep_pin = digitalio.DigitalInOut(board.D6)
motor_sleep_pin.direction = digitalio.Direction.OUTPUT
motor_sleep_pin.value = True

# Create USB data port
ser = usb_cdc.data


def usb_writeline(usb_data_port, x):
    usb_data_port.write(bytes(str(x) + "\n", "utf-8"))
    usb_data_port.flush()


def read_samples():
    pixel_builtin.fill((255, 0, 0))  # RED

    # Set number of samples
    n = 40
    current = [float] * n
    field_strength = [float] * n

    # Read sensor data and store in sample arrays
    for i in range(0, n):
        motor_driver.throttle = 0.1 + i / 100
        time.sleep(2)
        volts = 0
        for _ in range(1337):
            volts += pin_adc.value
        # Convert avg volts to milliamps via Ohm's law
        current[i] = volts / 1337 / 65535 * 4.72 / 1015 * 1000
        mag_x, mag_y, mag_z = magnetometer.magnetic
        field_strength[i] = sqrt(mag_x**2 + mag_y**2 + mag_z**2)

    # Turn off motor driver (enter sleep state)
    motor_sleep_pin.value = False

    # Transfer data over USB
    pixel_builtin.fill((255, 255, 0))  # YELLOW
    usb_writeline(ser, n)  # number of samples
    for val in current:
        usb_writeline(ser, val)  # current array
    for val in field_strength:
        usb_writeline(ser, val)  # field_strength array
    pixel_builtin.fill((0, 255, 0))  # GREEN


while True:
    cmd = ser.readline().strip().decode("utf-8")
    if cmd == "r":
        read_samples()
