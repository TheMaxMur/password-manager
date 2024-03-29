import os, sys
from Crypto.Cipher import AES


if sys.platform == 'linux':
    FOLDER_PATH = os.environ['HOME'] + '/' + '.passwordmanager' + '/'
    TEXT_COLOR = "#FFFFFF"

if sys.platform == 'win32':
    FOLDER_PATH = 'C:\\' + os.environ['HOMEPATH'] + '\\' + '.passwordmanager\\'
    TEXT_COLOR = "#000000"

if sys.platform == "darwin":
    FOLDER_PATH = os.environ['HOME'] + '/' + '.passwordmanager/'
    TEXT_COLOR = "#FFFFFF"


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key):
    message = pad(message)
    iv = os.urandom(16)
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name, 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    return dec.decode('utf-8')

