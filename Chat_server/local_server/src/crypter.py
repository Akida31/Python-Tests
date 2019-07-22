import hashlib
import random
import string

from Crypto.Cipher import AES
import rsa

from exceptions import AsymmetricDecryptionError, SymmetricDecryptionError


# https://stuvel.eu/python-rsa-doc/usage.html#bigfiles


def generate_keys() -> (rsa.PublicKey, rsa.PrivateKey):
    return rsa.newkeys(2048, poolsize=4)


def write_keys(pubkey: rsa.PublicKey, prkey: rsa.PrivateKey,
               pub_filename: str = 'public_key.pem', pr_filename: str = 'private_key.pem'):
    with open(pub_filename, 'wb') as f:
        f.write(pubkey.save_pkcs1())
    with open(pr_filename, 'wb') as f:
        f.write(prkey.save_pkcs1())


def load_pubkey(pub_filename: str = 'public_key.pem')-> rsa.PublicKey:
    with open(pub_filename, 'rb') as f:
        return rsa.PublicKey.load_pkcs1(f.read())


def load_prkey(pr_filename: str = 'private_key.pem')-> rsa.PrivateKey:
    with open(pr_filename, 'rb') as f:
        return rsa.PrivateKey.load_pkcs1(f.read())


def asym_encrypt(message: str, pubkey: rsa.PublicKey) -> bytes:
    return rsa.encrypt(message.encode(), pubkey)


def asym_decrypt(message: bytes, prkey: rsa.PrivateKey) -> str:
    try:
        return rsa.decrypt(message, prkey).decode()
    except rsa.pkcs1.DecryptionError:
        raise AsymmetricDecryptionError


def hashof(msg: str):
    h = hashlib.new('SHA512')
    h.update(msg.encode())
    return h.hexdigest()


def random_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits + '{!@}#$[]?&^') for i in range(length))


def sym_encrypt(message: str, key):
    if len(key) != 32:
        key = hashof(key)[:32].encode()
    iv = random_key(AES.block_size).encode()
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return iv + cipher.encrypt(message.encode())


def sym_decrypt(encrypted: bytes, key):
    if len(key) != 32:
        key = hashof(key)[:32].encode()
    decoder = AES.new(key, AES.MODE_CFB, encrypted[:16])
    try:
        readed = decoder.decrypt(encrypted[16:]).decode('utf-8')
        return readed
    except UnicodeDecodeError:
        raise SymmetricDecryptionError
