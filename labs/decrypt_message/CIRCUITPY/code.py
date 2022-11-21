# decrypt_message.py for KB2040

import board
import neopixel
import time


# Configure NeoPixel
pixel_builtin = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel_builtin.brightness = 0.1

colors = {    
    "w": (255, 255, 255),
    "r": (255, 0, 0),
    "g": (0, 255, 0),
    "b": (0, 0, 255),    
    "k": (0, 0, 0, 0),
    "p": (255, 0, 255),
}

msg = "kkpkpkpkkwwrrggbbkkpkpkpkkrkwkgkwkkrkgkrkrkkrkgkbkwkkrkgkbkwkkrkgkbkb"


def flash_led(color):
    pixel_builtin.fill(colors[color])
    time.sleep(1)


while True:
    for c in msg:
        flash_led(c)
