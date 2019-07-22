import os
import time

import crypter
import static
import tools


username = tools.getusername()
new_messages = []


def status_actualization():
    with open(static.GLOBAL_PATH + '.users/status/' + username + '.txt', 'w') as f:
        f.write('[LastOnline]: ' + str(time.time()))


def send(msg_receiver: str, msg_text: str):
    number = 0
    while os.path.isfile(static.GLOBAL_PATH + '.chats/' + msg_receiver + str(number) + '.txt'):
        number += 1
    filename = static.GLOBAL_PATH + '.chats/' + msg_receiver + str(number) + '.txt'
    with open(filename, 'wb') as f:
        text = username + '::' + msg_text
        pubkey = tools.read_pub_key(msg_receiver)
        f.write(crypter.asym_encrypt(text, pubkey))
    return tools.send_messages([[int(time.time()), msg_receiver, filename]])


def read():
    for file in os.listdir(static.GLOBAL_PATH + '.chats/'):
        if not file.startswith(username):
            continue
        filename = static.GLOBAL_PATH + '.chats/' + file
        with open(filename, 'rb') as f1:
            decoded = crypter.asym_decrypt(f1.read(), crypter.load_prkey(
                static.STD_DIR + 'settings/private_key.pem'))
            user, message = decoded.split('::', 1)
            last_modification = int(os.stat(filename).st_mtime)
            new_messages.append({'user': user, 'message': message,
                                 'time': last_modification})

    very_new_messages = []
    sort_files = []
    for msg in new_messages:
        user = msg['user']
        message = msg['message']
        last_modification = msg['time']
        filepath = static.STD_DIR + 'chats/' + user + '.txt'
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
