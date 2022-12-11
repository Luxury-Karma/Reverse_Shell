# INTERFACE UNVERSION alpha 0.1.0
import os
import time
from Server.Module import ContextEngine as CoEn

# TODO THIS IS A TEMPORARY PATCH TO KEEP THIS THING WORKING WILE I BUTCHER OTHER PART OF HIS BRAIN
get_connection = CoEn.get_connection


class Cli:
    """
    Command line interface, easier to program is thus currently the only available interface.

    I see it as a simple view on every module giving a user mostly unsecure access to every module offer by the server.

    """

    def __init__(self, wait_time=1, time_out=10):
        """
        :param wait_time: Define how long before new interval when waiting
        :param time_out: Define how many interval will be executed when waiting
        """

        self.wait_time = wait_time
        self.time_out = time_out

        self.context = {'context_id': 'root', 'context_dir': ''}  # Store current context

        self.mark = ' $> '  # Keep it easy to edit

    def handler(self):
        """
            Loop handling user input...
            Should be keep as simple as possible for ease of code readability

            see print_help() for more information...

        """

        while True:

            # region Get and parse user input

            # Get input from console
            cmd = input(f'{self.context["context_id"]} | {self.context["context_dir"]}{self.mark}').strip()

            # Parse cmd to get root (connect,run,exit, etc...) and tail (PCID, CMD, ,etc...)
            cmd_root, cmd_arg = self.parse_input(cmd)

            # endregion

            # region Set Context to DEFAULT             |                                 <['exit', 'quit'] ::: COMMAND>
            if cmd_root in ['exit', 'quit']:
                message = self.exit_context()
                print(message)
                continue
            # endregion

            # region Clear Console                      |                                 <['clear', 'cls'] ::: COMMAND>
            if cmd_root in ['clear', 'cls']:
                self.clear()  # DONT WORK ON PYCHARM
                continue
            # endregion

            # region Print Help                         |                                    <['help', 'h'] ::: COMMAND>
            if cmd_root in ['help', 'h']:
                message = self.print_help()
                print(message)
                continue
            # endregion

            # region List all connection                |                            <['list', 'lst', 'ls'] ::: COMMAND>
            if cmd_root in ['list', 'lst', 'ls']:
                message = self.list_connection()
                print(message)
                continue
            # endregion

            # region Get health of context              |                                 <['exit', 'quit'] ::: COMMAND>
            if cmd_root in ['health', 'beat']:
                message = self.connection_health()
                print(message)
                continue
            # endregion

            # region Connect to a context               |                   <['connect', 'context', 'link'] ::: COMMAND>
            if cmd_root in ['connect', 'context', 'link']:
                message = self.set_context(cmd_arg)
                print(message)
                continue
            # endregion

            # region Push cmd to client in context      |                         <['execute', 'exec', ':'] ::: COMMAND>
            if cmd_root in ['execute', 'exec', ':']:
                message = self.push_execution(cmd_arg)
                print(message)
                continue
            # endregion

            # region Set and print a message if command is not part of the cli
            with_context_msg = f'do you mean -> execute {cmd_root}'
            without_context_msg = f'do you mean -> execute {cmd_root} --target [server_list]'
            additional_message = with_context_msg if self.context['context_id'] != 'root' else without_context_msg

            print(f'--> ERROR: {cmd_root} not recognised, {additional_message}')
            # endregion

    def connection_health(self):
        """
        Generate a message containing a client heath check intended to be digested as a user output

        ATTENTION :: USE ONLY IF YOU WANT A FULLY FORMATTED MESSAGE

        :return: formatted message intended to be digested as a user output
        """

        message = '\n-----------|       HEALTH CHECK      |-----------\n'

        if self.context['context_id'] == 'root':
            # TODO ADD -> argument support
            message += '\n ---> execute without context is not yet supported'
        else:
            connection = get_connection(self.context['context_id'], single=True)  # Single True return only on
            # Print Health
            message += f'\n ---> {self.context["context_id"]}' \
                       f'\n    `---> Last response was {connection.get_health()}s ago'

        return message

    def push_execution(self, cmd_arg):
        """
        This command is a full execution of a transaction with the user

            step 1: Get a lock on every CiC (client in context)

            step 2: Clean out of every CiC output

            step 3: Set a command in every client cmd

            step 4: Monitor client output

            step 5: Generate user message from client output

        :param cmd_arg: data that will be sent to all client
        :return: Formatted message intended to be digested as a user output
        """

        message = '\n-----------|    Execution  OutPut    |-----------\n'

        if self.context['context_id'] == 'root':
            # TODO ADD -> argument support
            message += '\n ---> execute without context is not yet supported'
            return message
        else:

            # Get single connection from context
            connection = get_connection(self.context['context_id'], single=True)

            # Clear last response
            connection.set_last_response()

            # Set command to be push
            connection.set_command(cmd_arg)

            # Wait for time_out number of cycle for a response
            time_out = self.time_out  # Set number of cycle max before timeout from default
            message_additional = ''

            while not message_additional:
                if connection.get_last_response().strip():
                    # Get last message send by client
                    message_additional = f'\n ---> RESPONSE' \
                                         f'\n    `---> ' \
                                         f'\n{connection.get_last_response().strip()}'
                    break

                # Time out if time out get to zero
                time_out = time_out - 1
                if time_out < 1:
                    message_additional = '\n ---> No response received' \
                                         f'\n    `---> Client Health  :  {connection.get_health(update_health=True)}'
                    continue
                time.sleep(self.wait_time)

            message += f'\n ---> {self.context["context_id"]}'
            message += message_additional

            # Update context (current_directory) and add message if error doing so
            message += f'\n{self.set_context(self.context["context_id"])}'

            return message

    def set_context(self, cmd_arg):
        """
        Set all variable necessary to define a context

        TODO transfer most of the responsibility to the future context engine
            this method should in the future only be use to generate a user output message

        :param cmd_arg:
        :return: Formatted message intended to be digested as a user output
        """

        message = '\n-----------|          Context        |-----------\n'

        if not cmd_arg:
            # If no arg specified default to current
            arg_dic = {'id': self.context['context_id']}
        else:
            # Parse arg to arg dic
            arg_dic = self.parse_command(cmd_arg, ['id'])

        if arg_dic['id']:  # Make sure a flag id have been found

            # If context root have been specified exit current context
            if arg_dic['id'] == 'root':
                message += '\n ---> Root context: exiting all context'
                message += self.exit_context()
                return message

            connection = get_connection(arg_dic['id'], single=True)

            if connection:
                # connection = connection[0]
                self.context['context_id'] = connection.get_id()
                self.context['context_dir'] = connection.get_current_dir()
            else:
                message += f'\n ---> No connection found for {arg_dic["id"]}'
        return message

    def exit_context(self):
        """
            SET context item to default value

            context_id:          = "root"

            context_dir:           = ""

        :return: Formatted message intended to be digested as a user output
        """

        self.context['context_id'] = 'root'
        self.context['context_dir'] = ''
        message = f'\n ---> Exiting context'

        return message

    # WILL PROBABLY LOSE STATIC AFTER A FEW ITERATION OF THE CODE
    @staticmethod
    def clear():
        """
        Send a command to clear a console

            ATTENTION THIS DOESN'T WORK FOR MOST CONSOLE
            PLEASE USE CMD IF YOU WANT TO HAVE
            AT LEAST A SPRINKLE OF HOPE
            OF SEEN THIS THING
            WORK....

        :return: clear command to user terminal
        """
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def list_connection():
        """
        Generate a message containing every connection
        :return: Formatted message intended to be digested as a user output
        """

        message = '\n-------------|     LIST  CONNECTION     |-------------\n'
        column_width = 11
        connection_list = get_connection(single=False)  # Single False return a list
        if len(connection_list) > 0:

            message += '\n|     ID    | Last Beat |           |           |           |\n'
            for connection in connection_list:
                if connection:
                    message += f'\n|{connection.get_id(): ^{column_width}}' \
                               f'|{connection.get_health(): ^{column_width}}' \
                               f'|{"": ^{column_width}}' \
                               f'|{"": ^{column_width}}' \
                               f'|{"": ^{column_width}}|\n'
        else:
            message += '\n ---> No active connection'
        return message

    @staticmethod
    def parse_input(command: str):
        """
        TODO REPLACE WITH PARSE_COMMAND AS IT IS A MORE POWERFUL VERSION OF THIS AND ANY TIME GAIN WONT BE FEEL
        Parse an input in is tuple

        This tuple is constituted of the input root and the input tail

        ______EXAMPLE______

        exec tasklist /fi "STATUS eq running"

        ROOT: exec

        TAIL: tasklist /fi "STATUS eq running"
        :param command : str containing user input to be parsed

        :return: (root,tail) - tuple (str,list) containing command and *arg
        """

        tail_lst = []
        split_cmd = command.strip().split(' ', 1)
        root = split_cmd[0]

        if len(split_cmd) > 1:
            tail_lst = split_cmd[1]
        return root, tail_lst

    @staticmethod
    def parse_command(command: str, expected_arg: list, force_first_flag=False):
        """
        Parse command or command tail in expected part

        The expected part is important since it will ignore most of your input if your input is high entropy

        :param command: command to be parse in is expected constituent
        :param expected_arg: list of expected constituent EX: [CMD,ARG1,ARG...
        :param force_first_flag: false remove the need of a flag in front of the first argument...

            Removing the first flag make it harder to use programmatically for the most part
            force_first_flag default should thus be True, but I don't want to take the time needed to modify my code
        :return: Dictionary containing { 'FLAG1':'ARG1',.. _____EX: { 'ID':'CLIENT_ID',..

        """
        cmd_parsed_dict = {}

        command = command.strip()  # Need to make specially sure no leading space is present
        # cmd_arg --> connect ID_OF_THE_CONNECTION

        # If allow will interpret a non flagged first arg as the first arg of the expected_arg list
        if not force_first_flag and command[0] != '-':  # Test if first character is NOT a HYPHEN (-)
            temp_lst = command.split(' ', 1)
            cmd_parsed_dict[expected_arg[0]] = temp_lst[0]
            if len(temp_lst) > 1:
                command = temp_lst[1]
            else:
                command = None

        if command:
            command = command.replace('--', '-')  # Make sure -ID is the same as --ID
            for arg in command.split('-'):
                if arg:
                    # Add argument to argument dictionary
                    root_arg, tail_arg = arg.split(' ', 1)
                    cmd_parsed_dict[root_arg] = tail_arg
        return cmd_parsed_dict

    @staticmethod
    def print_help():
        """
            Print cli specific command help

                'help, h'                   'Print this message'

                'exit, quit'                'Exit current context',

                'clear, cls'                'Clear console, doesn't work with pycharm and other software',

                'list, lst, ls'             'List all know connection',

                'connect, context, link'    'Set a context to target connection',

                'execute, exec, :'          'Send a command to the connection object to be execute'
        """

        padding = 6
        message = '\n-----------|           HELP          |-----------\n'

        # TODO -> HELP for specified command
        # Dictionary containing the forbidden knowledge of everything i cared to included in the cli for now
        message_dic = {
            # dict is double-quoted to allow (doesn't) without having to use \'
            "help, h": "Print this message",
            "exit, quit": "Exit current context",
            "clear, cls": "Clear console, doesn't work with pycharm and other software",
            "list, lst, ls": "List all know connection",
            "connect, context, link": "Set a context to target connection",
            "execute, exec, :": "Send a command to the connection object to be execute"

        }

        length = 0
        for key in message_dic.keys():
            if len(key) > length:
                length = len(key)
        for key in message_dic.keys():
            val = message_dic[key]
            message += f'\n{key}{" " * (padding + length - len(key))}{val}'
        return message




class Gui:
    # TODO GUI
    pass


class Api:
    # TODO Api
    pass
