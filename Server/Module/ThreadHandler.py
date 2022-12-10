import threading
from Server.Module import ConnectionHandler as CoHa
from Server.Module import Interface as Itf

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 2424


def main():

    sock_handler = CoHa.SocketHandler(server_host=SERVER_HOST, server_port=SERVER_PORT)
    Itf.sock_handler = sock_handler
    cli_handler = Itf.Cli()

    # TODO handle thread in any other way seriously
    create_Thread(sock_handler.looker)
    create_Thread(sock_handler.handler)
    create_Thread(cli_handler.handler)

def create_Thread(target):
    try:
        threading.Thread(target=target).start()
        return 'Ok'
    except:
        return 'Err'
