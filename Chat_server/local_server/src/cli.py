import os
import time
import threading

import communicate
import static
import text
import tools
from exceptions import MissingPublicKey

# http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


def start():
    t = threading.Thread(target=loop)
    t.start()
    inputloop()


def inputloop():
    status = Status()
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
        if not cmd_found and user_input.startswith(Commands.SIGN) and len(user_input) > 2:
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
                    decorate('$yellow$This command is currently not working ' +
                             'because you are ' + is_in_chat_text + 'in a chat!')
                    break
            if not cmd_found2:
                decorate('$yellow$Command not found. Try "' + Commands.SIGN
                         + 'help" to get information about available commands')
        elif not cmd_found and status.is_in_chat:
            try:
                communicate.send(status.current_chat, user_input)
                print('Message sent!')
            except MissingPublicKey:
                decorate('$red$MESSAGE CANNOT BE SENT, MISSING KEY')
        elif not cmd_found:
            decorate('$yellow$This is not available! Try "' + Commands.SIGN
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
    new_msgs = communicate.read()
    for msg in new_msgs:
        new_messages.append(msg)
    del_msgs = tools.del_read_messages()
    if new_messages:
        decorate('$blue$You have $green${}$blue$ new messages! $reset$Read them with {}show!'
                 .format(int(len(new_messages)), Commands.SIGN))


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
            print('$yellow$You are not in a chat')
        return status

    @staticmethod
    def archive(status, args):
        print('Archiving currently not available!')

    @staticmethod
    def chatlist(status, args):
        for chat in tools.get_all_chats():
            name = chat.rstrip('.txt')
            msg_time = time.ctime(os.stat(static.STD_DIR + 'chats/' + chat).st_mtime)
            decorate('$blue${}$reset$: {}'.format(name, str(msg_time)))

    @staticmethod
    def chat(status, args):
        if not status.is_in_chat and len(args) > 2:
            if (args + '.txt') in tools.get_all_chats():
                status.go_in_chat(args)
                Commands.show_msgs(args)
                return status
            else:
                print('Chat not found')

    @staticmethod
    def show_msgs(chat):
        with open(static.STD_DIR + 'chats/' + chat + '.txt') as f:
            for line in f.readlines():
                msg_time, msg = line.rstrip('\n').split('::')
                decorate('{}: {}'.format(time.ctime(int(msg_time)), msg))

    @staticmethod
    def show(status=0, args=0):
        if new_messages:
            decorate('$red$New Messages:')
            users = {}
            for msg in new_messages:
                try:
                    users[msg['user']] += 1
                except KeyError:
                    users[msg['user']] = 1
            for user in users:
                decorate('$blue$' + user + ': $bold$' + str(users[user]))

    @staticmethod
    def new_chat(status, args):
        try:
            tools.read_pub_key(args)
        except MissingPublicKey:
            decorate('$red$This username is not been taken! You can\'t start a chat with nothing')
            return
        open(static.STD_DIR + 'chats/' + args + '.txt', 'w').close()
        decorate('$green$Chat started successfully')


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
        if len(args) < 3:
            Helper.standart()
        else:
            found = False
            for command in Helper.commands:
                if args.startswith(command) and len(args) < len(command) * 1.3:
                    Helper.commands[command]()
                    found = True
                    break
            if not found:
                print('Your Help is here')

    @staticmethod
    def prefix(status=0, args=0):
        print('Your current prefix is {}'.format(Commands.SIGN))

    @staticmethod
    def standart():
        print(('If you want to get all commands, type %sihelp commands.\n'
               + 'You can get your prefix with %sihelp prefix.').replace('%si', Commands.SIGN))

    @staticmethod
    def commands():
        print('All commands are:')
        commands = {**default_cmds, **normal_cmds, **chat_cmds}
        for command in commands:
            print(command)

    commands = {'prefix': prefix.__func__,
                'commands': commands.__func__}


decorate = text.Decorations.print_decor
default_cmds = {'quit': Commands.quit,
                'exit': Commands.quit,
                'help': Helper.help,
                'show': Commands.show}
chat_cmds = {'block': ChatCommands.block,
             'back': ChatCommands.back}
normal_cmds = {'archive': Commands.archive,
               'chatlist': Commands.chatlist,
               'chats': Commands.chatlist,
               'chat': Commands.chat,
               'new': Commands.new_chat}
new_messages = []
