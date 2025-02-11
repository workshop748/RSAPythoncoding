from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

def Generate():
    print("hello")
    keylen={1:1024,2:2048,3:3072}
    choice =input("Please select the key length you would like to generate: 1. 1024 2. 2048 3. 3072")
    key = RSA.generate(keylen[choice])
    pubFilename=f"public{keylen[choice]}.pem"
    privFilename=f"private{keylen[choice]}.pem"
    with open(pubFilename,"wb") as f:
        data = key.public_key.export_key()
        f.write(data)
    with open(privFilename,"wb") as f:
        data = key.export_key()
        f.write(data)
    print("both files have been created")
        
def pemPresnt():
    current_directory = os.getcwd()
    PossibleFiles = os.listdir(current_directory)
    for file in PossibleFiles:
        if file.endswith(".pem"):
            return True

    return False



def Encrypt(plainText, publicKey):
    cipherText = publicKey.encrypt(plainText, 32)
    
def Decrypt(cipherText, privateKey):
    plainText = privateKey.decrypt(cipherText)
while True:  
    print(" welcome to the RSA encryption/decryption program")
    print(" Please select an option")
    print("1. Generate a new key Pair")
    print("2. Encrypt a message")
    print("3. Decrypt a message")
    print("4. Exit")
    choice = input()
    if choice == "1":
        Generate()
    elif choice == "2":
        if pemPresnt():
          ## encryping the message
        else:
            print("No pem file present")
    elif choice == "3":
        if pemPresnt():
            ## decypting the message
        else:
            print("No pem file present")
    elif choice == "4":
        print("Goodbye and thank you for playing around with RSA encryption")
        break
    else:
        print("Invalid choice")

