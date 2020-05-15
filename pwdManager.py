# Abiola Salau
# 11/13/2019
#
# This program stores passwords in a file 
# that is encrypted with a master password
#
# python packages: pycryptodomex 
# install using pip install pycryptodomex 
# 
# To run:
#     python pwdManager.py or python3 pwdManager.py if both Python2.x and 3.x is on machine
#
# To reset:
#     rm PasswordFile.txt.enc

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
import os
import shutil
import time
import random
import string

# Password Geneartor function: It generates a password with 10 characters
def PasswordGen():
    """Generate a random password """
    randomSource = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation)

    for i in range(6):
        password += random.choice(randomSource)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password

#Variable declaration and initialization
salt = b'\xe0\xc4\x10\xe0\n\xed)6\x1c\x9f\xff\x91~\x93\xf3U'
file_to_encrypt = 'PasswordFile.txt'
buffer_size = 65536  # 64kb
mpwd = input("Enter Master Password: ").encode()
#check if master password length is at least 10 characters
while 1:
    if len(mpwd)>=10:
        key = PBKDF2(mpwd, salt, dkLen=32)
        break
    else:
        print('Password length too short')
        mpwd = input("Enter Master Password: ").encode()

# Takes website from user
data = input('Enter website: ').lower().strip().encode()

# Check if Password file exists, otherwise creates it
if not os.path.isfile('PasswordFile.txt.enc'):
    file = open("PasswordFile.txt", "a+")
    file.close()
    print('Searching...')
    time.sleep(1)
    print('Account not in database')
    #Gets input option from user whether to input password manually or generate automatically
    print('Please Enter (1) to Input password manually or (2) to generate password for account')
    selection = input('Enter Selection: ')
    while 1:
        if selection == '1':
            password = input('Enter pwd: ').encode()
            #check if master password length is at least 10 characters
            while 1:
                if len(password)>=10:
                    password = password
                    break
                else:
                    print('Password length too short, Minimum of 10 characters')
                    password = input("Enter Master Password: ").encode()
            break      
        elif selection == '2':
            #generates a password for the website
            password = PasswordGen().encode()
            print(f'Generated password for account "{data.decode()}" is: "{password.decode()}"')
            break
        else:
            print('Invalid selection, Try Again')
            selection = input('Enter Selection: ')
            
#saves the website and passowrd ino the database
    with open('PasswordFile.txt', 'a+b') as f:
        acc = [data, b'\t', password, b'\n']
        f.writelines((acc))
        # === Encrypt ===

    # Open the input and output files
    input_file = open(file_to_encrypt, 'rb')
    output_file = open(file_to_encrypt + '.enc', 'wb')

    # Create the cipher object and encrypt the data
    cipher_encrypt = AES.new(key, AES.MODE_CFB)

    # Initially write the iv to the output file
    output_file.write(cipher_encrypt.iv)

    # Keeps reading the file into the buffer, encrypting then writing to the new file
    buffer = input_file.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher_encrypt.encrypt(buffer)
        output_file.write(ciphered_bytes)
        buffer = input_file.read(buffer_size)

    # Close the input and output files
    input_file.close()
    output_file.close()
    print('Saved!')
else:
    try:
        # === Decrypt ===

        # Open the input and output files
        input_file = open(file_to_encrypt + '.enc', 'rb')
        output_file = open(file_to_encrypt + '.dec', 'wb')

        # Read in the iv
        iv = input_file.read(16)

        # Create the cipher object and encrypt the data
        cipher_encrypt = AES.new(key, AES.MODE_CFB, iv)

        # Keep reading the file into the buffer, decrypting then writing to the new file
        buffer = input_file.read(buffer_size)
        while len(buffer) > 0:
            decrypted_bytes = cipher_encrypt.decrypt(buffer)
            output_file.write(decrypted_bytes)
            buffer = input_file.read(buffer_size)

        # Close the input and output files
        input_file.close()
        output_file.close()
        with open('PasswordFile.txt.dec', 'rb') as file:
            for acc in file:
                profile = acc.decode()
                account = profile.split('\t')[0]
                passwd = profile.split('\t')[1]
                #if the user input is found in database, it prints the account and the password
                if data.decode() in profile:
                    print('Account found')
                    print('Retrieving details...')
                    time.sleep(1)
                    print('Website: ', account)
                    print('Password: ', passwd)
                    break
            else:
                print('Searching...')
                time.sleep(1)
                print('Account not in db')
                print('Please Enter (1) to Input password manually or (2) to generate password for account')
                selection = input('Enter Selection: ')
                while 1:
                    if selection == '1':
                        password = input('Enter pwd: ').encode()
                        while 1:
                            if len(password)>=10:
                                password = password
                                break
                            else:
                                print('Password length too short, Minimum of 10 characters')
                                password = input("Enter Master Password: ").encode()
                        break
                    elif selection == '2':
                        password = PasswordGen().encode()
                        print(f'Generated password for account "{data.decode()}" is: "{password.decode()}"')
                        break
                    else:
                        print('Invalid selection, Try Again')
                        selection = (input('Enter Selection: '))
                #create a copy of the decrypted password file, enters the new data
                shutil.copy('PasswordFile.txt.dec', 'pwdup.txt')

                with open('pwdup.txt', 'a+b') as f:
                    acc = [data, b'\t', password, b'\n']
                    f.writelines(acc)
                    # === Encrypt the new file===

                # Open the input and output files
                input_file = open('pwdup.txt', 'rb')
                output_file = open(file_to_encrypt + '.enc', 'wb')

                # Create the cipher object and encrypt the data
                cipher_encrypt = AES.new(key, AES.MODE_CFB)

                # Initially write the iv to the output file
                output_file.write(cipher_encrypt.iv)

                # Keep reading the file into the buffer, encrypting then writing to the new file
                buffer = input_file.read(buffer_size)
                while len(buffer) > 0:
                    ciphered_bytes = cipher_encrypt.encrypt(buffer)
                    output_file.write(ciphered_bytes)
                    buffer = input_file.read(buffer_size)
                input_file.close()
                output_file.close()
                print('Stored!')

    except UnicodeDecodeError:
        print('Wrong Master password, Try again!')

#removes all non-encrypted files created.
if os.path.isfile('PasswordFile.txt.dec'):
    os.remove('PasswordFile.txt.dec')

if os.path.isfile('pwdup.txt'):
    os.remove('pwdup.txt')
if os.path.isfile('PasswordFile.txt'):
    os.remove('PasswordFile.txt')