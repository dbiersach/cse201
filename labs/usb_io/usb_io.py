# usb_io.py

import serial
import sys

# Ask user for string to send to KB2040
print("Enter a string containing r, g, or b characters:")
color_string = input()

# Open the USB data port
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
if sys.platform == "win32":
    ser.port = "COM10"
if sys.platform == "darwin":
    ser.port = "/dev/tty.usbserial-110"
ser.open()

# Convert input to bytes and send to KB2040
color_string += "\n"
ser.write(color_string.encode())

# Read and dislay the reversed color string from the KB2040
reversed_string = ser.readline().decode("ASCII").strip()
print("The reversed string is:")
print(reversed_string)

ser.close()



