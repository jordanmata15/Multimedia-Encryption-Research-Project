#prerequisite
#%pip install cryptography

from cryptography.fernet import Fernet
key = Fernet.generate_key()
 
# string the key in a file
with open('filekey.key', 'wb') as filekey:
   filekey.write(key)

with open('filekey.key', 'rb') as filekey:
    key = filekey.read()
 
# using the generated key
fernet = Fernet(key)
 
# opening the original file to encrypt
with open('data/data_to_encrypt/alice29.txt', 'rb') as file:
    original = file.read()
     
# encrypting the file
encrypted = fernet.encrypt(original)
 
# opening the file in write mode and
# writing the encrypted data
with open('data/encrypted_data/test.txt', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

fernet = Fernet(key)
 
# opening the encrypted file
with open('data/encrypted_data/test.txt', 'rb') as enc_file:
    encrypted = enc_file.read()
 
# decrypting the file
decrypted = fernet.decrypt(encrypted)
 
# opening the file in write mode and
# writing the decrypted data
with open('data/encrypted_data/detest.txt', 'wb') as dec_file:
    dec_file.write(decrypted)