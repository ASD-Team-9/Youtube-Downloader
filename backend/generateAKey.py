# generating a symmetric key
from cryptography.fernet import Fernet
key = Fernet.generate_key()

# saving the key into a file
with open('secretLoginKey.key', 'wb') as file:
    file.write(key)
    