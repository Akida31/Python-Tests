import hashlib,os
from pathlib import Path

#cd to download
#certutil -hashfile [filename] [method]
#method can be md5 or sha256 etc.

class Checker():
    def input(self):
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
                print('File not available')
            elif len(input3)<5:
                hasha = False
                inputting = False
            else:
                inputting = False

        self.fname = input1
        self.hasha = hasha
        self.input3 = input3
        self.vers = vers
        self.check()

    def check(self,*args):
        getargs = False
        if len(args)==0:
            try:
                fname = self.fname
                getargs = True
            except:
                self.input()
                getargs = True
        else:
            try:
                fname = args[0]
                vers = args[1]
                hasha = args[2]
                input3 = args[3]
            except:
                self.input()
                getargs = True
        if getargs:
            fname = self.fname
            hasha = self.hasha
            vers = self.vers
            input3 = self.input3
        exec('self.hash1 = hashlib.' + str(vers) + '()')
        with open(fname, "rb") as f:
            #hash1.update(f.read())
            #hashb = (hash1.hexdigest())
            for chunk in iter(lambda: f.read(4096), b""):
                self.hash1.update(chunk)
                hashb = (self.hash1.hexdigest())

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

if __name__ == "__main__":
    checker = Checker()
    checker.input()
