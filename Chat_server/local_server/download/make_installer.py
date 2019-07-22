with open('requirements.txt') as f:
    import_text = ''
    for line in f:
        import_text+=('import ' + line.rstrip('\n') + ';')
text = """try:
    {}
except ModuleNotFoundError:
    print('MISSING MODULE! CANNOT INSTALL FUSION');quit()
""".format(import_text)
text += 'import os;os.mkdir(\'fusion\')\nfolders=['
folders = ['settings', 'chats', 'keys', 'logs' , 'scripts']
for folder in folders:
    text += '\'{}\','.format(folder)
text = text[:-1] + ']\n[os.mkdir(\'fusion/\' + folder) for folder in folders]\n'
text += 'STD_DIR = os.path.abspath(\'fusion/\').replace(\'\\\\\', \'/\') + \'/\'\nprint(STD_DIR)\n'
inp = input('Please paste the global path:\n').replace('\\','/')
inp += '/' if not inp.endswith('/') else ''
text += 'GLOBAL_PATH = \'{}\'\n'.format(inp)
text+= '''def copy(source, destination):
    destination += source.rsplit('/', 1)[1] if destination.endswith('/') else ''
    with open(source, 'rb') as f1, open(destination, 'wb') as f2:
        f2.write(f1.read())
for file in os.listdir(GLOBAL_PATH + 'download/scripts'):
    copy(GLOBAL_PATH + 'download/scripts/' + file, STD_DIR + 'scripts/')
with open(STD_DIR.rsplit('/',1)[0] + '/scripts/static.py', 'w') as f:
        f.write('STD_DIR=\\\'{}\\\'\\nGLOBAL_PATH=\\\'{}\\\''.format(STD_DIR, GLOBAL_PATH))
open(STD_DIR + 'chats/sent_messages.txt','w').close()
os.system('python3 {s} || python {s}'.format(s=STD_DIR+'scripts/setup.py'))'''
with open('install.py','w') as f:
    f.write(text)
with open('install.sh', 'w') as f:
    f.write('python3 install.py || python install.py')
