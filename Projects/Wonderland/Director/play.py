# File: play.py
# ECE 3872 Spring 2022 Wonderland Project
# Author: Navneet Lingala
# Director Program for "Director-Robot" Connection
# This file is reponsible for creating the local line file buffer and establishing robot connections.
# Once the correct number of robots have been connected, line files will automatically be sent at the appropriate cue time.
# ONLY modify lines that have been highlighted as MODIFIABLE

import os
import socket
import threading
import time

# Global Variables
IP = "192.168.137.43"       # MODIFIABLE: Change server IP as needed. Should be hardcoded already 
SIZE = 1024
FORMAT = "utf-8"
PORT = 3030
ADDR = (IP, PORT)
NUM_R = 3
SERVER_DATA_PATH = r'/home/pi/Documents/upload_files'        # MODIFIABLE: Change server data path as needed.
SEPARATOR = "<SEPARATOR>"

# buffer initializer
def buffer_load(buf):
    files = os.listdir(SERVER_DATA_PATH)
    for f in files:
        rob, cue_time= f.split("_")
        cue_time = cue_time.split(".")[0]
        cue_time = int(cue_time)
        tup = (f, cue_time)
        if rob in buf:
            if not isinstance(buf[rob], list):
                buf[rob] = [buf[rob]]
            buf[rob].append(tup)
            buf[rob].sort(key=lambda tup: tup[1])
        else:
            buf[rob] = [tup]

# file enumeration
def buffer_enumerate_files(name, buffer):
    file = []
    for e in buffer[name]:
        file.append(e[0])
    return file

# Cue time calculations
def buffer_enumerate_times(name, buffer):
    time_after_cue = []
    for e in buffer[name]:
        if len(time_after_cue) == 0:
            time_after_cue.append(e[1])
        else:
            time_after_cue.append(e[1]-time_after_cue[-1])
    return time_after_cue

# returns ms since the epoch
def millis():
        return time.time() * 1000

# Time delay function
def switchTheThing(howlong):
    start = millis()
    while ( (start + howlong) > millis() ):
        pass

## Function that handles new Robot Connections
 # Appropriate files are sent to corresponding robots at cue time.
 # Files are automatically sent 3 seconds after the correct number of robots have connected to the Director
def handle_client(conn, addr, file_list, time_list, num):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True: 
        count = threading.active_count() - 1
        time.sleep(3)
        if count == num:  
            # print("started")
            # start = time.perf_counter()
            for i in range(len(file_list)):
                switchTheThing(time_list[i])
                filepath = os.path.join(SERVER_DATA_PATH, file_list[i])
                filesize = os.path.getsize(filepath)
                conn.send(f"{file_list[i]}{SEPARATOR}{filesize}".encode())
                with open(filepath, "rb") as f:
                    while True:
                        # read the bytes from the file
                        bytes_read = f.read(filesize)
                        if not bytes_read:
                            # file transmitting is done
                            f.close()
                            break
                        # we use sendall to assure transimission in busy networks
                        conn.sendall(bytes_read)

                # finish = time.perf_counter()
                # print(f'finished in {round(finish-start,3)} seconds(s)')
            break
    print(f"[DISCONNECTED] {addr} disconnected")
    conn.send("DISCONNECT".encode())
    conn.close()

# Unused function
# def robot_connection(addr, buffer):
#     return (buffer_enumerate_files(ROBOT[addr], buffer), buffer_enumerate_times(ROBOT[addr], buffer))

## Main Function that creates new threads for each new Robot Connection
 # Server has no limit to number of connections and will always listen.
 # 
 # At the start of program function asks for 2 arguments:
 #      - Number of Robots trying to connect to Director
 #      - Local IP of each robot. 
 #      Note: input order matters. For example first IP address corresponds to R01 (robot 1) as per file naming format
 # 
 # Line File Buffer initializes
 # 
 ##
def main():
    print("[STARTING] Server is starting") 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")
    robot_addr = []
    number_of_rob = input("Number of Robots: ")
    for i in range(int(number_of_rob)):
        rob_ip = input("Robot IP: ")
        robot_addr.append(rob_ip)
    print()
    buffer = {}
    buffer_load(buffer)
    while True:
        conn, addr = server.accept()
        file_list = []
        time_list = []
        for ind, i in enumerate(robot_addr):
            if addr[0] == i:
                file_list = buffer_enumerate_files("R0" + str(ind + 1), buffer)
                time_list = buffer_enumerate_times("R0" + str(ind + 1), buffer)
        
        thread = threading.Thread(target=handle_client, args=(conn, addr, file_list, time_list, number_of_rob))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

# Script to call main function
if __name__ == "__main__":
    main()
