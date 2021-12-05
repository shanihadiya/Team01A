# File: client.py
# ECE 3872 Spring 2022 Wonderland Project
# Author: Navneet Lingala
# Team Computer Program for "Team Computer-Director" Connection
# Responsible for sending line files and commands to the director from the team computer
# server.py must be running on the director before this file can be ran on the team computer.
# ONLY modify lines that have been highlighted as MODIFIABLE

import socket
import sys
import os

# Global Variables 
IP = "192.168.137.43"       # MODIFIABLE: Change server IP as needed. Should be hardcoded already 
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1000000
ERR = "error"

## Function that sends commands to Director
 # Commands available for each Client Computer:
 # LIST: List all the files on the server.
 # UPLOAD <path>: Upload a file to the server.
 # DELETE <filename>: Delete a file from the server.
 # LOGOUT: Disconnect from the server.
 # HELP: List all the commands.
 # SEND: <Type_your_message> (No spaces in message) send a message.
 #
 # Students will use these commands to check the files on the server and upload new scripts.
 #
 # File Naming Format:[(ROBOT#)_(CueTime in Milliseconds).xxx] for example: [R01_1000.txt]
 # If sending multiple files you can place it in a .zip
 # Director will automatically extract all files in zip. 
 # CAUTION: Zip folder will be deleted after extraction. 
 # 
 ##
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@", 1)

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        if len(data) <= 2:   
            cmd = data[0]

            if cmd == "HELP":
                client.send(cmd.encode(FORMAT))
            elif cmd == "LOGOUT":
                client.send(cmd.encode(FORMAT))
                break
            elif cmd == "LIST":
                client.send(cmd.encode(FORMAT))
            elif cmd == "DELETE" and len(data) == 2:
                client.send(f"{cmd}@{data[1]}".encode(FORMAT))
            elif cmd == "UPLOAD" and len(data) == 2:
                path = data[1]
                try:
                    with open(f"{path}", "rb") as f:
                        filesize = os.path.getsize(path)
                        text = f.read(filesize)
                        filename = path.split("/")[-1]                 # MODIFIABLE: ONLY either of these options: ---filename = path.split("/")[-1]--- on linux          ---filename = path.split("\\")[-1]--- on Windows 
                        send_data = f"{cmd}@{filename}@{filesize}"
                        client.sendall(send_data.encode(FORMAT))
                        client.sendall(text)
                except OSError as err:
                    print("OS error: {0}".format(err))
                    client.send(ERR.encode(FORMAT))
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    client.send(ERR.encode(FORMAT))
                    raise
            elif cmd == "SEND" and len(data) == 2:
                client.send(f"{cmd}@{data[1:]}".encode(FORMAT))
            else:
                client.send(ERR.encode(FORMAT))
        else:
            client.send(ERR.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()

# Script to call main function
if __name__ == "__main__":
    main()
