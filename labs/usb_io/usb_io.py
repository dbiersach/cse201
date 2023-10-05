# usb_io.py

import serial
import adafruit_board_toolkit.circuitpython_serial

# Open the USB data port
cdc_data = adafruit_board_toolkit.circuitpython_serial.data_comports()[0]
ser = serial.Serial(None, 115200, 8, "N", 1, timeout=120)
ser.port = cdc_data.device
ser.open()

# Ask user for string to send to KB2040
print("Enter a string containing r, g, or b characters:")
color_string = input()

# Convert input to bytes and send to KB2040
color_string += "\n"
ser.write(color_string.encode())

# Read and dislay the reversed color string from the KB2040
reversed_string = ser.readline().decode("ASCII").strip()
print("The reversed string is:")
print(reversed_string)

ser.close()



