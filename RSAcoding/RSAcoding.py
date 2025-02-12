from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import pandas as pd
LOG_FILE = "log_encryption.csv"


if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["filename","key_length"]).to_csv(LOG_FILE,index=False)

def Generate():
    
    keylen={1:1024,2:2048,3:3072}
    choice =int(input("Please select the key length you would like to generate: 1. 1024 2. 2048 3. 3072: "))
    
    #sanity checks
    if choice not in keylen:
        print("Invalid choice!")
        return
    allPem =pemPresnt()
    if len(allPem)==6:
        print("All public/private keys have been created.")
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
    return [file.endswith(".pem") for file in os.listdir(current_directory)if file.endswith(".pem")]

    

def files(searchname):
    current_directory = os.getcwd()
    return[file for file in os.listdir(current_directory) if file.startswith(searchname) and file.endswith(".pem")]
 
def log_encryption(filename,key_length):
    df = pd.read_csv(LOG_FILE)
    newEntry=pd.DataFrame([{"filename":filename,"key_length":key_length}])
    df=pd.concat([df,newEntry],ignore_index=True)
    df.to_csv(LOG_FILE,index=False)

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
       public_key =RSA.import_key(pubFile.read())
   
   message = input("please enter a message: ").encode()

   cipher=PKCS1_OAEP.new(public_key)
   cipherText = cipher.encrypt(message)

   name = input("please enter a name for your file: ")
   name= f"{name}.bin"
   with open(f"{name}","wb") as cipherFile:
       cipherFile.write(cipherText)
   key_length = int(publicKeyFile.split("public")[1].split(".pem")[0])
   log_encryption(name,key_length)

   print("The message has been encrypted and saved to a file")

    
def Decrypt():

   private_key=files("private")
   df=pd.read_csv(LOG_FILE)

   if df.empty:
         print("No log file found")
         return
   
   print("Available encrypted files:")
   for i,row in df.iterrows():
       print(f"{i+1}. {row['filename']} (Key length: {row['key_length']})")

   choice = int(input("Please select the private key you would like to use: "))

   if choice<1 or choice>len(df):
        print("Invalid choice")
        return
   selected_row=df.iloc[choice-1]
   filename=selected_row["filename"]
   key_length = selected_row["key_length"]
   Private_key_file = f"private{key_length}.pem"

   if not os.path.exists(Private_key_file):
         print("Private key file not found")
         return
       

   private_key = RSA.import_key(open(Private_key_file).read())
   
   try:
        with open(filename,"rb") as cipher_file:
            ciphertexting= cipher_file.read()
        cipher=PKCS1_OAEP.new(private_key)
        message=cipher.decrypt(ciphertexting)
        print(f"the plaintext message: {message.decode()}")
   except FileNotFoundError:
        print("the file was not found")
   except ValueError as e:
        print(f"there was an error {e}")
   
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

