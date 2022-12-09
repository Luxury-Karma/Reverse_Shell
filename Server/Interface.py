import os
import time


class Cli:  # .......          s    TODO COMPLETE REWORK
    def __init__(self, sock_handler, wait_time=0.25):
        self.sock_handler = sock_handler

        self.wait_time = wait_time
        self.context = {'context_root':'root','context_dir':'','context_connection':None}
        #  TODO Add target I/O

    def handle(self):
        mark = ' $> '

        while True:
            # Connection_list need to be globally change
            connection_list = self.sock_handler.connection_list  # TODO please find a better way, i hate this list

            cmd = input(f'{self.context["context_root"]} {self.context["context_dir"]}{mark}').strip()


            # Parse cmd to get root (connect,run,exit, etc...) and tail (PCID,CMD, ,etc...)
            cmd_root, cmd_arg = self.parse_input(cmd)

            if cmd_root in ['exit','quit']:
                #  Set context to default
                self.exit_context()
                continue

            if cmd_root in ['help', 'h']:
                self.print_help()
                continue

            if cmd_root in ['clear', 'cls']:
                self.clear()  # DONT WORK ON PYCHARM
                continue

            if cmd_root in ['list', 'lst', 'ls']:
                # TODO make connection_list look good
                for e in connection_list:
                    print(f'| {e[0].id} |')
                # TODO add query
                # TODO print heartbeat
                # TODO add info (os? uptime? ping?)

            if cmd_root in ['connect','context','link']:
                self.set_context(cmd_arg,connection_list)
                continue

            if cmd_root in ['execute','exec',':']:
                if self.context['context_root'] == 'root':
                    # TODO test arg to get id then remove the continue and else to utilize else code here

                    continue
                elif(self.context['context_connection']):
                    # TODO keep stream open? or print last message? wait or continue?

                    # Clear last response
                    self.context['context_connection'].last_response = ''
                    # Set command to be push
                    self.context['context_connection'].command = cmd_arg
                    # TODO ...
                    time_out = 12 * self.wait_time
                    while self.context['context_connection'].last_response == '' and time_out > 0:
                        time_out = time_out - 1
                        time.sleep(self.wait_time)
                    print(f' ---> {self.context["context_root"]}')
                    print(self.context['context_connection'].last_response)
                    continue
                else:
                    continue

    def parse_input(self, command: str):
        '''
        :param command : str containing user input to be parsed
        :return: (root,tail) - tuple (str,list) containing command and *arg
        '''
        root = ''
        tail_lst = []
        split_cmd = command.strip().split(' ', 1)

        root = split_cmd[0]
        if len(split_cmd) > 1:
            tail_lst = split_cmd[1]
            #tail_lst = [e for e in split_cmd[1].split('-') if e]
        return root, tail_lst


    def exit_context(self):
        """
            SET context item to default value
            :var context_root:          = "root"
            :var context_dir:           = ""
            :var context_connection:    = None
        """
        self.context['context_root'] = 'root'
        self.context['context_dir'] = ''
        self.context['context_connection'] = None



    def set_context(self,cmd_arg,connection_list):
        message = '----------- Context Creation OutPut -----------' # TODO better i/o management
        # I don't even want to comment that part
        if not cmd_arg:
            message += '\n  -->   ERROR : connect <id> --flag '
            return message

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
                if arg:
                    root_arg, tail_arg = arg.split(' ', 1)
                    arg_dic[root_arg] = tail_arg
        if arg_dic['id']:
            for e in connection_list:
                if e[0].id == arg_dic['id']:
                    self.context['context_root'] = e[0].id
                    self.context['context_dir'] = e[0].current_dir
                    self.context['context_connection'] = e[0]

            if not self.context['context_dir']: # TODO Heartbeat and validate connection before trying to set context
                self.exit_context()
                message += f'\n  -->   No active connection with id {arg_dic["id"]}'


    def print_help(self):
        """
            Print cli specific command help
        """
        # TODO help for specific command
        message_dic = {
            '[help, h] ->':                'Print this message',
            '[exit, quit] ->':             'Exit current context',
            '[clear, cls] ->':             'Clear console, doesn\'t work with pycharm and other software',
            '[list, lst, ls] ->':          'List all know connection',
            '[connect, context, link] ->': 'Set a context to target connection',
            '[execute, exec, :] ->':       'Send a command to the connection object to be execute'

        }
        for key in message_dic:
            value = message_dic[key]
            print(key,value)

    @staticmethod
    def clear():
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')



class Gui:
    # TODO GUI
    pass


class Api:
    # TODO Api
    pass
