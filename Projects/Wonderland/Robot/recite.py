# File: recite.py
# ECE 3872 Spring 2022 Wonderland Project
# Author: Navneet Lingala
# Robot Program for Decoding and Processing
# Students must complete this program to process their scripts
# An example has been provided below.

import os

SERVER_DATA_PATH = r'/home/pi/Documents'    # MODIFIABLE: Change robot data path as needed.
SCRIPTS = 3     # MODIFIABLE: Change number of files expected to be received by Director.

# reads file on cue
# Other computation can be coded here
def main():
    count = 1
    read = []
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
    
    
    print("End Of Wonderland")


# Script to call main function
if __name__ == "__main__":
    main()
