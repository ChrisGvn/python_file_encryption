import os, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

userinput = input("\nEnter your password: ").encode('utf-8')

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), 
                length=32, 
                salt=userinput, 
                iterations=100000)

pre_key = kdf.derive(userinput) 
key = base64.urlsafe_b64encode(pre_key) 

f = Fernet(key)

with open('C:/path/to/file/text_sample.txt','rb') as text_sample:
    unencrypted = text_sample.read()

encrypted = f.encrypt(unencrypted)

with open('C:/path/to/file/encrypted_file.txt', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)