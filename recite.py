# File: recite.py
# ECE 3872 Spring 2022 Wonderland Project
# Author: Navneet Lingala
# Robot Program for Decoding and Processing
# Students must complete this program to process their scripts
# An example has been provided below.

import os
import time
import threading
import board
import neopixel

from gpiozero import Servo 
from time import sleep 

SERVER_DATA_PATH = r'/home/pi/Documents'    # MODIFIABLE: Change robot data path as needed.
SCRIPTS = 3     # MODIFIABLE: Change number of files expected to be received by Director.

# reads file on cue
# Other computation can be coded here

##################################
# Start of LIGHTING Section
##################################
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 30


# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    if ORDER in (neopixel.RGB, neopixel.GRB):
        return (r, g, b)
    else :
        (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def lighting_show():
    pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(1)

    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

##################################
# End of LIGHTING Section
##################################


def main():
    count = 1
    read = []
    light_thread = threading.Thread(target = lighting_show, args = None)
    # Directory will be continuously polled for new files until
    # the number of files dictated by SCRIPTS has been polled.
    while count <= SCRIPTS:
        files = os.listdir(SERVER_DATA_PATH)[-1]
        if files is None:
            pass
        elif files not in read:
            # Some code has been written to get you started
            # *********** Your code goes here *********** # 
            read.append(files)
            count = count + 1
            f = open(files, "r")
            print(f.read())


            # *********** Your code goes here *********** #

        ##############################################
        # Start of procedure for the Lighting_Show
        # Comment this line out if you have RGBW/GRBW NeoPixels
        
        lighting_show()

        ##################################
        # End of Lighting_Show procedure
        ##################################
    
    print("End Of Wonderland")


# Script to call main function
if __name__ == "__main__":
    main()