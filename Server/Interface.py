import os
import time


class Cli:  # .......          s    TODO COMPLETE REWORK
    def __init__(self, sock_handler,wait_time= 0.25):
        self.sock_handler = sock_handler

        self.wait_time = wait_time
        #  TODO Add target I/O

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
                    time_out = 12 * self.wait_time
                    while context_connection.last_response == '' and time_out > 0:
                        time_out = time_out - 1
                        time.sleep(self.wait_time)
                    print(context_connection.last_response)
                    continue

    @staticmethod
    def clear():
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def print_help():
        pass

class Gui:
    # TODO GUI
    pass

class Api:
    # TODO Api
    pass