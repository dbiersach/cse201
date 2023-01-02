# usb_io for KB2040


import board
import neopixel
import supervisor
import time
import usb_cdc

# Wait until USB console port is ready
while not supervisor.runtime.usb_connected:
    pass

# Configure NeoPixel
pixel_builtin = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel_builtin.brightness = 0.1
pixel_builtin.fill((255, 0, 255))  # PURPLE

# Create USB data port
ser = usb_cdc.data


def usb_writeline(usb_data_port, x):
    usb_data_port.write(bytes(str(x) + "\n", "utf-8"))
    usb_data_port.flush()


def flash_led(color_string):
    reversed_string = ""

    for c in color_string:
        if c == "r":
            pixel_builtin.fill((255, 0, 0))  # RED
            time.sleep(0.5)
        elif c == "g":
            pixel_builtin.fill((0, 255, 0))  # GREEN
            time.sleep(0.5)
        elif c == "b":
            pixel_builtin.fill((0, 0, 255))  # BLUE
            time.sleep(0.5)

        # Prepend character to front of reversed string
        reversed_string = c + reversed_string

    # Send the reversed string back to the main PC
    usb_writeline(ser, reversed_string)

    pixel_builtin.fill((255, 0, 255))  # PURPLE


while True:
    cmd = ser.readline().strip().decode("utf-8")
    flash_led(cmd)
