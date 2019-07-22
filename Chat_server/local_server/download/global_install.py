import os
import requests

def make_dirs():
    folders = ['.chats', '.users', 'scripts']
    for folder in folders:
        os.mkdir(GLOBAL_PATH + folder)

def is_connected():
    try:
        requests.get('http://google.com')
        return True
    except requests.exceptions.ConnectionError:
        print('For installing you have to have an internet connection!')
        quit()

def get_file(file: str) -> str:
    resp = requests.get(GITHUB_PATH + file)
    return resp.content.decode().rstrip('\n')

def download(addr: str, name: str):
    print(get_file(addr))
    with open(GLOBAL_PATH + 'scripts/' + name, 'w') as f:
        f.write(get_file(addr).replace('\n', ''))

if __name__ == "__main__":
    GLOBAL_PATH = input('Put in the path where the folder should be made:\n').replace('\\','/' )
    GLOBAL_PATH += '/' if not GLOBAL_PATH.endswith('/') else ''
    GITHUB_PATH = 'https://raw.githubusercontent.com/Akida31/Python-Tests/master/Chat_server/local_server/'
    make_dirs()
    is_connected()
    version = get_file('version.txt')
    with open(GLOBAL_PATH + 'version.txt', 'w') as f:
        f.write(version)
    requirements = get_file('requirements.txt')
    with open(GLOBAL_PATH + 'requirements.txt', 'w') as f:
        f.write(requirements)
    scriptlist = get_file('scriptlist.txt')
    for script in scriptlist.split('\n'):
        download(GITHUB_PATH + 'src/' + script, script)
    print('SUCCESS!')
