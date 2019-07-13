import os
import shutil

import crypter
import tools
from exceptions import MissingRequirements


directories = ['logs', '.settings', 'chats', 'keys']
files = [tools.std_dir + r'.settings\usernames.txt']


def write_settings():
    with open(tools.std_dir + '.settings/path.py', 'w') as f:
        f.write(r'_global_path = "PASTE/HERE/THE/PAST/OF/YOUR/GLOBAL/DIRECTORY"')
    with open(tools.std_dir + '.settings/user.txt', 'w') as f:
        f.write('Username: ' + tools.getusername())


def install():
    for directory in directories:
        try:
            os.mkdir(directory)
        except FileExistsError:
            print('Files are already present! Reinstalling instead!')
            uninstall()
            os.mkdir(directory)
    for file in files:
        open(file, 'w').close()
        # TODO
    crypter.generate_keys()
    os.chdir(tools.std_dir)
    write_settings()
    tools.write_pubkey()
    tools.make_globalfolder()
    print('SUCCESS: Installation complete')
    return True


def uninstall():
    directories.append('__pycache__')
    for directory in directories:
        try:
            shutil.rmtree(directory)
        except FileNotFoundError:
            pass
    directories.remove('__pycache__')
    for file in files:
        try:
            os.rmdir(file)
        except FileNotFoundError:
            pass
    print('SUCCESS: Uninstallation complete')
    return True


def reinstall():
    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)
    for file in files:
        if not os.path.isfile(file):
            open(file, 'w').close()
    try:
        crypter.load_pubkey(tools.std_dir + '.settings/public_key.pem')
        crypter.load_prkey(tools.std_dir + '.settings/private_key.pem')
    except ValueError:
        pbkey, prkey = crypter.generate_keys()
        crypter.write_keys(pbkey, prkey,
                           tools.std_dir + '.settings/public_key.pem',
                           tools.std_dir + '.settings/private_key.pem')
    write_settings()
    check()


def check():
    # checks if all requirements are available,
    # else start install
    missing_file = ''
    missing = False
    for directory in directories:
        if not os.path.exists(directory):
            missing = True
            missing_file = directory
    for file in files:
        if not (os.path.exists(file)):
            missing = True
            missing_file = file
    try:
        _global_path = tools.oimport(tools.std_dir + '.settings/path.py', '_global_path')
    except MissingRequirements:
        missing = True
        missing_file = '.settings/path.py'
    try:
        crypter.load_pubkey(tools.std_dir + '.settings/public_key.pem')
        crypter.load_prkey(tools.std_dir + '.settings/private_key.pem')
    except ValueError:
        missing_file = 'key files'
        missing = True
    if missing:
        print('ERROR: MISSING REQUIREMENTS: ' + missing_file)
        if 'y' in input('Do you want to reinstall? [y/n]\n'):
            tools.log('info', 'missing requirements, reinstalling')
            reinstall()
        else:
            tools.log('error', 'missing requirements, reinstallation stopped! Breaking')
            raise MissingRequirements
    with open(tools.std_dir + r'.settings\user.txt', 'r') as f:
        for line in f:
            if line.startswith('Username: '):
                username = line.replace('Username: ', '').replace(' ', '')
                if username != tools.username:
                    tools.log('warning', 'Different Usernames: ' +
                              username + ' && ' + tools.username)
    return True

