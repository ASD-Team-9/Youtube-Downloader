from cryptography.fernet import Fernet

# reading key from file
key = ''
with open('secretLoginKey.key','rb') as file:
    key = file.read()

# reading data from file
data = ''
with open ("resources/logins.txt","rb") as file:
    data = file.read()

# encrypting the data
f = Fernet(key)

encryptedData = f.encrypt(data)

# saving the encrypted data into a file
with open('resources/encryptedLogins.txt', 'wb') as file:
    file.write(encryptedData)