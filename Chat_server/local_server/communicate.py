import os
import time

import crypter
import tools
from exceptions import MissingPublicKey

_global_path = tools.oimport(tools.std_dir + r'.settings\path.py', '_global_path')
username = tools.getusername()
new_messages = []


def status_actualization():
    with open(_global_path + '.users/status/' + username + '.txt', 'w') as f:
        f.write('[LastOnline]: ' + str(time.time()))


def send(msg_receiver: str, msg_text: str):
    number = 0
    while os.path.isfile(_global_path + '.chats/' + msg_receiver + str(number) + '.txt'):
        number += 1
    filename = _global_path + '.chats/' + msg_receiver + str(number) + '.txt'
    with open(filename, 'wb') as f:
        text = username + '::' + msg_text
        pubkey = tools.read_pub_key(msg_receiver)
        f.write(crypter.asym_encrypt(text, pubkey))
    return tools.send_messages([[int(time.time()), msg_receiver, filename]])
# time.ctime(time.time())


def read():
    for file in os.listdir(_global_path + '.chats/'):
        if not file.startswith(username):
            continue
        filename = _global_path + '.chats/' + file
        with open(filename, 'rb') as f1:
            decoded = crypter.asym_decrypt(f1.read(), crypter.load_prkey(
                tools.std_dir + '.settings/private_key.pem'))
            user, message = decoded.split('::', 1)
            last_modification = int(os.stat(filename).st_mtime)
            new_messages.append({'user': user, 'message': message,
                                 'time': last_modification})

    very_new_messages = []
    for msg in new_messages:
        sort_files = []
        user = msg['user']
        message = msg['user']
        last_modification = msg['time']
        filepath = tools.std_dir + 'chats/' + user + '.txt'
        if not os.path.isfile(filepath):
            open(filepath, 'w').close()
        with open(filepath) as f1:
            with open(filepath, 'a') as f2:
                found = False
                for line in f1.readlines():
                    if line == (str(last_modification) + '::' + message + '\n'):
                        found = True
                if not found:
                    f2.write(str(last_modification) + '::' + message + '\n')
                    sort_files.append(filepath)
                    very_new_messages.append(msg)
    tools.sort_files(sort_files)
    return very_new_messages
