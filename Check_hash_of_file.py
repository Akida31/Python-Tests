import hashlib,os
from pathlib import Path

inputting = True
hasha = True
while inputting:
    input1 = input('Put in the Path of your file: ')
    input2 = input('Put in the algorithm: ')
    vers = input2
    input3 = input('Put in the hash: ')
    if not vers in hashlib.algorithms_available:
        print('ERROR: Algorithm can\'t be used')
    elif not os.path.isfile(Path(input1)):
        print('File not ')
    elif len(input3)<5:
        hasha = False
    else:
        inputting = False

fname = input1
exec('hash1 = hashlib.' + str(vers) + '()')
with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        hash1.update(chunk)
        hashb = (hash1.hexdigest())

print('\n\n\n\n')
if hasha:
    if input3 == hashb:
        print('FILE DOWNLOADED CORRECTLY\nHashes are same')
        input()
    elif input3 != hashb:
        print('ERROR: HASHES ARE DIFFERENT')
        print(input3)
        print(hashb)
        input()
else:
    print('HASH:\n'+ hashb)
    input()
