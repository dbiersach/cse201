# usb_io.py

import serial
import traceback
import sys


def usb_readline(usb_data_port):
    s = usb_data_port.readline().decode("ASCII").strip()
    return s


def main():
    print("Enter a string containing r, g, or b characters:")
    color_string = input()

    ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
    try:
        port = "COM9"
        if sys.platform == "linux":
            port = "/dev/ttyACM1"
        if sys.platform == "darwin":
            port = "/dev/tty.usbmodem2203"

        ser.port = port
        ser.open()

        # Append a linefeed at end of input string
        color_string += "\n"

        # Convert input to bytes and send to the MCU
        ser.write(color_string.encode())

        # Read the reversed color string from the MCU
        reversed_string = usb_readline(ser)

        print("The reversed string is:")
        print(reversed_string)

    except:
        print("Error with MCU serial I/O")
        traceback.print_exc()

    if ser.is_open:
        # Close the serial port connection to the MCU
        ser.close()


main()
