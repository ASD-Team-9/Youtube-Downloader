# reading key from file
key = ''
with open('secretLoginKey.key','rb') as file:
    key = file.read()

# reading data from file
data = ''
with open ("resources/logins.txt","rb", encoding="utf-8") as file:
    data = file.read()

# encrypting the data
from cryptography.fernet import Fernet

f = Fernet(key)


# saving the encrypted data into a file