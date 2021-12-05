# File: server.py
# ECE 3872 Spring 2022 Wonderland Project
# Author: Navneet Lingala
# Director Program for "Team Computer-Director" Connection
# Establishes team computer connections and handles commands from the team computers. 
# Line Files will be stored in the specified in the file path below.
# ONLY modify lines that have been highlighted as MODIFIABLE

import os
import socket
import threading
import zipfile

# Global Variables
IP = "192.168.137.43"       # MODIFIABLE: Change server IP as needed. Should be hardcoded already
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1000000
FORMAT = "utf-8"
SERVER_DATA_PATH = r"/home/pi/Documents/upload_files"        # MODIFIABLE: Change server data path as needed.

## Function that handles new Team Computer Connections
 # Commands available for each Client Computer:
 # LIST: List all the files on the server.
 # UPLOAD <path>: Upload a file to the server.
 # DELETE <filename>: Delete a file from the server.
 # LOGOUT: Disconnect from the server.
 # HELP: List all the commands.
 # SEND: <Type_your_message> (No spaces in message) send a message.
 #
 # Students will use these commands to check the files on the server and upload new scripts.
 # - File Naming Format:[(ROBOT#)_(CueTime in Milliseconds).xxx] for example: [R01_1000.txt]
 # - If sending multiple files you can place it in a .zip
 # - Director will automatically extract all files in zip. 
 # CAUTION: Zip folder will be deleted after extraction. 
 ##
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@", 1)
        cmd = data[0]
        if cmd == "UPLOAD":
            filename, filesize = data[1].split("@", 1)
            data[1] = filename
            data.append(filesize)

        if cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, size = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "wb") as f:
                text = conn.recv(int(size))
                f.write(text)
                f.close()
                if ".zip" in name:
                    with zipfile.ZipFile(filepath,"r") as zip_ref:
                        zip_ref.extractall(SERVER_DATA_PATH)
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")          # MODIFIABLE: ONLY either of these options: ---os.system(f"rm {SERVER_DATA_PATH}/{filename}")--- on linux             ---os.system(f"del /f {SERVER_DATA_PATH}\{filename}")--- on windows
            

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")          # MODIFIABLE: ONLY either of these options: ---os.system(f"rm {SERVER_DATA_PATH}/{filename}")--- on linux             ---os.system(f"del /f {SERVER_DATA_PATH}\{filename}")--- on windows
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))
        elif cmd == "SEND":
            send_data = "OK@"
            msg = data[1]
            send_data += msg

            print(f"[{addr}] {msg}")
            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        elif cmd == "HELP":
            data = "OK@"
            data += "LIST: List all the files from the server.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands.\n"
            data += "SEND: <Type_your_message> send a message."

            conn.send(data.encode(FORMAT))
        else:
            msg = "OK@Illegal Argument"
            conn.send(msg.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

## Main Function that creates new threads for each new Team Computer Connection
 # Server has no limit to number of connections and will always listen.
 ##
def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

# Script to call main function
if __name__ == "__main__":
    main()
