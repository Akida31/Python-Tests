import getpass

import crypter
import static
import text
import tools
from exceptions import MissingPublicKey


def getusername() -> str:
    decorate = text.Decorations.print_decor
    suggestion = str(getpass.getuser())
    decorate('$red$WARNING:\nYOU CAN NOT CHANGE YOUR NAME!')
    while True:
        username = input('How do you want to be named?\n')
        if len(username) < 5:
            decorate('$yellow$Your name has to have a length of more than 4')
            decorate('$green$Suggestion: ' + suggestion)
            continue
        try:
            tools.read_pub_key(username)
            decorate('$red$This username is already taken!')
        except MissingPublicKey:
            break
    with open(static.STD_DIR + 'settings/user.txt', 'w') as f:
        f.write('Username: ' + username)
    return username


if __name__ == '__main__':
    username = getusername()
    key1, key2 = crypter.generate_keys()
    crypter.write_keys(key1, key2, static.STD_DIR + 'settings/public_key.pem', 
        static.STD_DIR + 'settings/private_key.pem')
    with open(static.STD_DIR + 'settings/public_key.pem', 'rb') as f:
        with open(static.GLOBAL_PATH + '.users/pbkeys/' + username + '.pem', 'wb') as fnew:
            fnew.write(f.read())
    decorate = text.Decorations.print_decor
    decorate('$green$Installation complete!')
