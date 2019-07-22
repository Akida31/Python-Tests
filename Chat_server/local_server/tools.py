import getpass
import os
import time

import crypter
from exceptions import MissingRequirements, MissingPublicKey
import static


def send_messages(messages):
    # a message is a list of sending time, receiver and filename
    text = ''
    for message in messages:
        msg_time, receiver, filename = message
        text += str(msg_time) + '!:= ' + receiver + '!:= ' + filename + '\n'
    with open(static.STD_DIR + 'chats/sent_messages.txt', 'a') as f:
        f.write(text)
    return True


def removemessages(messages):
    # a message is a list of time of sending, receiver and filename
    ret_messages = []
    for message in getmessages():
        deleted = False
        for wrong_message in messages:
            if wrong_message == message:
                deleted = True
        if not deleted:
            ret_messages.append(message)
    os.remove(static.STD_DIR + 'chats/sent_messages.txt')
    if send_messages(ret_messages):
        return True


def getmessages():
    messages = []
    with open(static.STD_DIR + 'chats/sent_messages.txt', 'r') as f:
        for line in f:
            messages.append(line.split('!:= '))
    return messages


def del_read_messages():
    deleted = False
    messages = getmessages()
    for message in messages:
        msg_time, msg_receiver, msg_filename = message
        msg_time = int(msg_time)
        if (time.time() - msg_time) < _msg_timeout:
            continue
        if (
                (msg_time + _msg_timeout)
                < read_status(msg_receiver)
                < (time.time() - _msg_timeout)
        ):
            os.remove(msg_filename)
            removemessages(message)
            deleted = True
    return deleted


def add_contact(global_name: str, contact_name: str):
    with open(static.STD_DIR + 'settings/usernames.txt') as f:
        for line in f:
            if line.startswith(global_name):
                return
    with open(static.STD_DIR + 'settings/usernames.txt', 'a') as f:
        f.write(global_name + ': ' + contact_name + '\n')


def getusername() -> str:
    with open(static.STD_DIR + 'settings/user.txt', 'r') as f:
        for line in f:
            if line.startswith('Username: '):
                username = line.replace('Username: ', '').replace(' ', '')
    return username


def read_pub_key(user: str):
    # get the public key of a certain user
    try:
        pubkey = crypter.load_pubkey(static.GLOBAL_PATH + '.users/pbkeys/' + user + '.pem')
        return pubkey
    except FileNotFoundError:
        log('warning', 'can\'t read publickey of ' + user + ', FileNotFound')
        raise MissingPublicKey


def read_status(user: str):
    # get last online of a certain user
    try:
        with open(static.GLOBAL_PATH + '.users/status/' + user + '.txt', 'r') as f:
            for line in f:
                if line.startswith('[LastOnline]: '):
                    return float(line.replace('[LastOnline]: ', '').replace(' ', ''))
    except FileNotFoundError:
        log('warning', 'can\'t read lastonline of ' + user + ', FileNotFound')
        return 'Status not Found'


def get_all_chats():
    chatlist = os.listdir(static.STD_DIR + 'chats/')
    try:
        chatlist.remove('sent_messages.txt')
    except ValueError:
        pass
    return chatlist


def sort_files(chats):
    for chat in chats:
        messages = []
        with open(chat) as f:
            for line in f:
                messages.append(line.split('::'))
        messages.sort(key=lambda elem: elem[0])
        with open(chat, 'w') as f:
            for message in messages:
                f.write(message[0] + '::' + message[1])


def log(status: str, message: str):
    filepath = static.STD_DIR + 'logs/' + status + '.log'
    logger = Logger(filepath)
    logger.log(getusername(), message)
    del logger


class Logger:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def log(self, user: str, message: str):
        with open(self.filepath, 'a') as f:
            log_info = '[' + user + ']: ' + '{' + str(int(time.time())) + '}: '
            f.write(log_info + message + '\n')


_msg_timeout = 2  # time in seconds before deleting after the message is sent
try:
    terminal_size = [os.get_terminal_size().columns,
                     os.get_terminal_size().lines]
except OSError:
    # this is for testing in pycharm
    import shutil

    terminal_size = [shutil.get_terminal_size().columns,
                     shutil.get_terminal_size().lines]
