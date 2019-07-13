import os
import platform
import time
import threading

import communicate
import tools
from exceptions import MissingPublicKey

# http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html



def start():
    t = threading.Thread(target=loop)
    t.start()
    inputloop()


def inputloop():
    status = Status()
    default_cmds = {'quit': Commands.quit,
                    'exit': Commands.quit,
                    'help': Helper.help}
    chat_cmds = {'block': ChatCommands.block,
                 'back': ChatCommands.back}
    normal_cmds = {'archive': Commands.archive,
                   'chatlist': Commands.chatlist,
                   'chat': Commands.chat}
    while True:
        if status.is_in_chat:
            input_string = '>>>'
            commands = chat_cmds
            not_working_commands = normal_cmds
        else:
            input_string = '>'
            commands = normal_cmds
            not_working_commands = chat_cmds
        user_input = input(input_string)
        commands = {**default_cmds, **commands}
        cmd_found = False
        for cmd in commands:
            if (user_input.startswith(Commands.SIGN + cmd + ' ') or
                    user_input.startswith(Commands.SIGN + cmd) and
                    len(user_input) == len(Commands.SIGN + cmd)):
                args = user_input.strip(Commands.SIGN + cmd + ' ')
                new_status = commands[cmd](status, args)
                if new_status:
                    status = new_status
                cmd_found = True
                break
        if not cmd_found and user_input.startswith(Commands.SIGN):
            cmd_found2 = False
            for cmd in not_working_commands:
                if (user_input.startswith(Commands.SIGN + cmd + ' ') or
                        user_input.startswith(Commands.SIGN + cmd) and
                        len(user_input) == len(Commands.SIGN + cmd)):
                    cmd_found2 = True
                    if status.is_in_chat:
                        is_in_chat_text = ''
                    else:
                        is_in_chat_text = 'not '
                    print('This command is currently not working because you are '
                          + is_in_chat_text + 'in a chat!')
                    break
            if not cmd_found2:
                print('Command not found. Try "' + Commands.SIGN
                      + 'help" to get information about available commands')
        elif not cmd_found and status.is_in_chat:
            try:
                communicate.send(status.current_chat, user_input)
            except MissingPublicKey:
                print('MESSAGE CANNOT BE SENT, MISSING KEY')

            print('Message sent!')
        elif not cmd_found:
            print('This is not available! Try "' + Commands.SIGN
                  + 'help" to get information about available commands')


def loop():
    timer = 0
    reading_time = 0.1
    loop_time = 0.1
    status_time = 0.5
    while True:
        if timer % reading_time == 0:
            readrun()
        if timer % status_time == 0:
            communicate.status_actualization()
        time.sleep(loop_time)
        timer += loop_time


def readrun():
    decorate = Decorations.decorate
    new_messages = communicate.read()
    del_msgs = tools.del_read_messages()
    if new_messages:
        Decorations.decorate('$blue$New Messages:')
        for msg in new_messages:
            the_time = str(time.ctime(int(msg['time'])))
            text1 = ' ' * (tools.terminal_size[0] - 1 -
                           len(msg['user'] + ': ' + the_time))
            print('\n' + msg['user'] + ': ' + text1 + the_time)
            print(msg['message'])


class Commands:
    SIGN = '.'

    @staticmethod
    def quit(status, args):
        quit()

    @staticmethod
    def chats(status, args):
        if status.is_in_chat:
            status.leave_chat()
        else:
            print('OOUCH')
        return status

    @staticmethod
    def archive(status, args):
        print('Archiving currently not available!')

    @staticmethod
    def chatlist(status, args):
        for chat in tools.get_all_chats():
            print(chat.rstrip('.txt'))

    @staticmethod
    def chat(status, args):
        if not status.is_in_chat:
            if (args + '.txt') in tools.get_all_chats():
                status.go_in_chat(args)
                return status
            else:
                print('Chat not found')


class ChatCommands:
    @staticmethod
    def block(status, args):
        print('Blocking currently not available!')

    @staticmethod
    def back(status, args):
        status.leave_chat()
        return status


class Status:
    def __init__(self):
        self.is_in_chat = False
        self.can_send_msg = False
        self.current_chat = ''

    def go_in_chat(self, chat):
        self.is_in_chat = True
        self.can_send_msg = True
        self.current_chat = chat

    def leave_chat(self):
        self.is_in_chat = False
        self.can_send_msg = False
        self.current_chat = ''


class Helper:
    @staticmethod
    def help(status=0, args=""):
        print('Your Help is here')

    @staticmethod
    def prefix(status=0, args=0):
        print('Your current prefix is {}'.format(Commands.SIGN))


class Decorations:
    reset = u'\u001b[0m'
    black = u'\001b[30'
    red = u'\u001b[31m'
    green = u'\u001b[32m'
    yellow = u'\001b[33m'
    blue = u'\001b[34'
    magenta = u'\001b[35'
    cyan = u'\001b[36'
    white = u'\001b[37'
    bright_black = u'\001b[30;1m'
    bright_red = u'\001b[31;1m'
    bright_green = u'\001b[32;1m'
    bright_yellow = u'\001b[33;1m'
    bright_blue = u'\001b[34;1m'
    bright_magenta = u'\001b[35;1m'
    bright_cyan = u'\001b[36;1m'
    bright_white = u'\001b[37;1m'
    bold = u'\001b[1m'
    underline = u'\001b[4m'

    # same as above, but as a dict
    colors = {'black': u'\001b[30', 'red': u'\u001b[31m', 'green': u'\u001b[32m',
              'yellow': u'\001b[33m', 'blue': u'\001b[34', 'magenta': u'\001b[35',
              'cyan': u'\001b[36', 'white': u'\001b[37',
              'bright_black': u'\001b[30;1m', 'bright_red': u'\001b[31;1m',
              'bright_green': u'\001b[32;1m', 'bright_yellow': u'\001b[33;1m',
              'bright_blue': u'\001b[34;1m', 'bright_magenta': u'\001b[35;1m',
              'bright_cyan': u'\001b[36;1m', 'bright_white': u'\001b[37;1m'}
    special = {'reset': u'\u001b[0m', 'bold': u'\001b[1m', 'underline': u'\001b[4m'}

    @staticmethod
    def decorate(text: str) -> str:
        # TODO change 'a' to 'Windows' if you are not developing
        if platform.system() == 'a':
            for color in Decorations.colors:
                text = text.replace('$' + color + '$', '')
            for spec in Decorations.special:
                text = text.replace('$' + spec + '$', '')
        else:
            for color in Decorations.colors:
                text = text.replace('$' + color + '$', Decorations.colors[color])
            for spec in Decorations.special:
                text = text.replace('$' + spec + '$', Decorations.special[spec])
            text += Decorations.reset
        print(text)
