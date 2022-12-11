import threading
from Server.Module import ConnectionHandler as CoHa
from Server.Module import ContextEngine as CoEn
from Server.Module import Interface as Itf

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 2424


# TODO CREATE A MASTER HANDLING ENGINE
#  computer can you analise my current motivation of working on this
#       analysing.... analysing..........
#            RESULT:  error err$% er543or motivation under nine thousand!
def main():

    sock_handler = CoHa.SocketHandler(server_host=SERVER_HOST, server_port=SERVER_PORT)
    cli_handler = Itf.Cli()

    # Send reference of current socket handler to the context engine
    # TODO handle this better... maybe the thread engine could become the master controller
    #   he could then talk to other master controller to give me a multi master controller context and
    #   a more ergonomic way of controlling multiple master, could also make part of server offloadable

    CoEn.sock_handler = sock_handler

    create_Thread(sock_handler.looker)
    create_Thread(sock_handler.handler)
    create_Thread(cli_handler.handler)

def create_Thread(target):
    try:
        threading.Thread(target=target).start()
        return 'Ok'
    except:
        return 'Err'
