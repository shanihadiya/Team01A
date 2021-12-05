# File: rob.py
# ECE 3872 Spring 2022 Wonderland Project
# Author: Navneet Lingala
# Robot Program for "Director-Robot" Connection
# Accepts incomming line files from the director
# play.py must be running on the director before this file can be ran on the robot.
# ONLY modify lines that have been highlighted as MODIFIABLE

import socket
import os

# Global Variables
IP = "192.168.137.43"    # MODIFIABLE: Change server IP as needed. Should be hardcoded already
SERVER_DATA_PATH = r'/home/pi/Documents/robot_files'    # MODIFIABLE: Change robot data path as needed.
PORT = 3030
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
ERR = "error"
SEPARATOR = "<SEPARATOR>"

## Function that accepts incomming files.
 # Files are stored in the path stated above.
 ##
def listen_for_director():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    while True:
        msg = client.recv(SIZE).decode()
        if msg == "DISCONNECT":
            break
        filename, filesize = msg.split(SEPARATOR)
        filepath = os.path.join(SERVER_DATA_PATH, filename)
        f = open(filepath, "wb")
        bytes_read = client.recv(int(filesize))
        f.write(bytes_read)
        f.close()
    client.close()

# runs file listener
# Other computation can be coded here
def main():
    listen_for_director()
    
    # *********** Your code goes here *********** #


# Script to call main function
if __name__ == "__main__":
    main()
