from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

def Generate():
    
    keylen={1:1024,2:2048,3:3072}
    choice =int(input("Please select the key length you would like to generate: 1. 1024 2. 2048 3. 3072"))
    
    #sanity checks
    if choice not in keylen:
        print("Invalid choice!")
        return
    
    #generate the RSA KEy
    key_length =keylen[choice]
    key = RSA.generate(key_length)
   
    pubFilename=f"public{keylen[choice]}.pem"
    privFilename=f"private{keylen[choice]}.pem"
    
    ## created the pem files
    with open(pubFilename,"wb") as f:
        data = key.publickey().export_key()
        f.write(data)
    with open(privFilename,"wb") as f:
        data = key.export_key()
        f.write(data)
    
        print("both files have been created")
        
def pemPresnt():
    current_directory = os.getcwd()
    return any(file.endswith(".pem") for file in os.listdir(current_directory))

    

def files(searchname):
    current_directory = os.getcwd()
    return[file for file in os.listdir(current_directory) if file.startswith(searchname) and file.endswith(".pem")]
    

def Encrypt():
   publicKey=files("public")
   
   if not publicKey:
       print("No public pem file found, please generate text first")
       return
   print("These are the public keys found that are aviable")

   for i,key_file in enumerate(publicKey, start =1):
       print(f"{i}. {key_file}")

   choice = int(input("Please select the public key you would like to use: "))

   if choice<1 or choice>len(publicKey):
         print("Invalid choice")
         return
   publicKeyFile = publicKey[choice-1]

   with open(publicKeyFile,"rb") as pubFile:
       public_key =RSA.importKey(pubFile.read())
   
   message = input("please enter a message").encode()

   cipher=PKCS1_OAEP.new(public_key)
   cipherText = cipher.encrypt(message)

   name = input("please enter a name for your file")

   with open(f"{name}.bin","wb") as cipherFile:
       cipherFile.write(cipherText)
   print("The message has been encrypted and saved to a file")

    
def Decrypt():
   private_key=files("private")
   
   if not private_key:
       print("No public pem file found, please generate text first")
       return
   print("These are the private keys found that are aviable")

   for i,key_file in enumerate(private_key, start =1):
       print(f"{i}. {key_file}")

   choice = int(input("Please select the private key you would like to use: "))

   if choice<1 or choice>len(private_key):
        print("Invalid choice")
        return
   Private_key_file = private_key[choice-1]

   with open(Private_key_file,"rb") as priv_file:
       privateKey =RSA.importKey(priv_file.read())
   
   try:
        filename = input("please enter your file name you want to decrypt")
        with open(filename,"rb") as cipher_file:
            ciphertexting= cipher_file.read()
        cipher=PKCS1_OAEP.new(privateKey)
        message=cipher.decrypt(ciphertexting)
        print(f"the plaintext message: {message}")
   except FileNotFoundError:
        print("the file was not found")
   except ValueError as e:
        print(f"there was an error {e}")
   


      
   print("The message has been encrypted and saved to a file")
while True:  
    print(" welcome to the RSA encryption/decryption program")
    print(" Please select an option")
    print("1. Generate a new key Pair")
    print("2. Encrypt a message")
    print("3. Decrypt a message")
    print("4. Exit")
    choice = input()
    if choice == "1":
        ##generate the key pairs
        Generate()
    elif choice == "2":
        ## Encrypting the message
        Encrypt()
    elif choice == "3":
        ## decypting the message
        Decrypt()
    elif choice == "4":
        print("Goodbye and thank you for playing around with RSA encryption")
        break
    else:
        print("Invalid choice")

