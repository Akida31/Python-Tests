# hash checker by Akida
# version 1.0.1
# compare a given hash with the hash of a file
# or generate the hash of a file

import argparse
import hashlib
import os
from pathlib import Path


def get_file(file=None):
    if file:
        if os.path.isfile(Path(file)):
            return file
    while True:
        file = input('Put in the Path of your file: ')
        if os.path.isfile(Path(file)):
            return file
        files = []
        for f in os.listdir():
            if os.path.isfile(Path(f)):
                files.append(f)
        for f in files:
            if f.startswith(file[:5]):
                if 'y' in input('Do you mean "' + f + '"? [y/n] '):
                    return f
        print('File not available')


def get_algo(algorithm=None):
    if algorithm:
        if algorithm in hashlib.algorithms_available:
            return algorithm
    while True:
        algorithm = input('Put in the algorithm: ')
        if algorithm in hashlib.algorithms_available:
            return algorithm
        print("ERROR: Algorithm can't be used")


def get_info():
    in_path = get_file(args.file)
    in_algo = get_algo(args.algorithm)
    if not args.hash:
        hasha = input('Put in the hash or put in nothing to print the hash: ')
    else:
        hasha = args.hash
    if len(hasha) < 5:
        hasha = None
    return in_path, in_algo, hasha


def check(file, algorithm, hasha=None):
    hash1 = hashlib.new(algorithm)
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash1.update(chunk)
        hashb = hash1.hexdigest()
    if hasha:
        return hasha == hashb
    return hashb


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='the file you of which you want to check')
    parser.add_argument('-a', '--algorithm', help='the algorithm to check')
    parser.add_argument('--hash', help='the hash of the file')
    args = parser.parse_args()
    print('\n')
    path, algo, a_hash = get_info()
    result = check(path, algo, a_hash)
    print('\n\n')
    if a_hash:
        if result:
            print('FILE DOWNLOADED CORRECTLY\nHashes are same')
        else:
            print('ERROR: HASHES ARE DIFFERENT')
    else:
        print('HASH:\n' + result)
    input()
