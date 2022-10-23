from cryptography.fernet import Fernet

# Reading the key from file
key = ''
with open('secretLoginKey.key','rb') as file:
    key = file.read()

# Reading the encrypted data from file
encryptedData = ''
with open ("resources/encryptedLogins.txt","rb") as file:
    encryptedData = file.read()

# Decreypt the data
f = Fernet(key)

decryptedData = f.decrypt(encryptedData)

print('Encrypted data: ', encryptedData.decode())

print('Decrypted data: ', decryptedData.decode())