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
    threading.Thread(target=sock_handler.looker).start()
    threading.Thread(target=sock_handler.run).start()
    threading.Thread(target=cli_handler.handle).start()
