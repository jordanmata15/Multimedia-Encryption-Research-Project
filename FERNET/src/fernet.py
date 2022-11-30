#!/usr/bin/python3

#prerequisite
#%pip install cryptography

import os
import sys
from cryptography.fernet import Fernet

SCRIPT_PATH = os.path.dirname(os.path.abspath( __file__ ))
KEY_DIR = os.path.join(SCRIPT_PATH, '..')
KEY_PATH = os.path.join(KEY_DIR, "secret.key")


def encrypt(input_file, output_file):
    key = open(KEY_PATH, "rb").read()
    fernet = Fernet(key)

    with open(input_file, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(output_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)



def decrypt(input_file, output_file):
    key = open(KEY_PATH, "rb").read()
    fernet = Fernet(key)

    with open(input_file, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)

    with open(output_file, 'wb') as dec_file:
        dec_file.write(decrypted)



if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise Exception("Unexpected number of args!")

    input_filename = sys.argv[2]
    output_filename = sys.argv[3]
    if (sys.argv[1] == 'encrypt'):
        encrypt(input_filename, output_filename)
    else:
        decrypt(input_filename, output_filename)