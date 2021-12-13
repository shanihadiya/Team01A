## Director
- Linux server that is responsible for mediating file transfers from Team Computers to Robots.
### Contents of Folder:
- server.py:
    - Establishes team computer connections and handles commands from the team computers. 
    - Line Files will be stored in the specified file path variable
- play.py:
    - reponsible for creating the local line file buffer and establishing robot connections.
    - Once the correct number of robots have been connected, line files will automatically be sent at the appropriate cue time.
- Both these files must be run first before the Team Computer and Robot can establish connections
### How to Run:
- server.py:
    - Run "python3 server.py" in Thonny IDE
    - Read comments if modifications are needed (i.e. IP address changes, file path)
- play.py:
    - Run "python3 play.py" in Thonny IDE
    - Read comments if modifications are needed (i.e. IP address changes, file path)
    - Note: Director will only load the the file buffer once in the beginning.
        - If new files are transfered play.py will have to be ran again.
