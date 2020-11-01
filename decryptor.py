import os, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

userinput = input("\nEnter your password: ").encode('utf-8')

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), 
                length=32, 
                salt=userinput, 
                iterations=100000)

key = base64.urlsafe_b64encode(kdf.derive(userinput))

f = Fernet(key)

with open('C:/path/to/file/encrypted_file.txt', 'rb') as encrypted_file:
    encrypted = encrypted_file.read()

decrypted = f.decrypt(encrypted)

with open('C:/path/to/file/decrypted.txt', 'wb') as decrypted_file:
    decrypted_file.write(decrypted)