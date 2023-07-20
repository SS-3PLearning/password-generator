import os
import string
import random
import platform
import subprocess
# pip3 install cryptography
from cryptography.fernet import Fernet  

# resiszes console window
os.system('mode 143,20') 

# ensures that any file that is created is created in the file path of application
__location__ = os.path.realpath(  
    os.path.join(os.path.dirname(__file__)))

current_os = platform.system()
get_cwd = (os.getcwd())
version = '1.2.0'
banner = ('\n'
                  r' ______  _____  _______ _______ _  _  _  _____   ______  _____       ______  ______ __   _  ______  ______  _____  _______  _____   ______' '\n'
                  r'|_____] |_____| |_____  |_____  |  |  | |     | |_____/ |     \     |  ____ |______ | \  | |______ |_____/ |_____|    |    |     | |_____/' '\n'
                  r'|       |     | ______| ______| |__|__| |_____| |    \_ |_____/     |_____| |______ |  \_| |______ |    \_ |     |    |    |_____| |    \_' '\n')

NORM = '\033[0m'
BOLD = '\033[1m'
RED = '\033[91m'
GREEN = '\033[92m'

def display_banner():
    print(
        banner 
        + '\n[>] Created by : Shubham Sharma'
        + '\n[>] Version    : ' + version 
        + BOLD + "\n\n[>] Input 'h' or 'help' to view the list of in-built commands and necessary arguments")

def generate_password():
    while True:
        try:
            user_input_length = int(input(BOLD + "\n[>] Enter the no. of characters for the length of the password, to cancel process input '0': " + NORM))
            if user_input_length == 0:
                print(BOLD + GREEN + '\n[+] Password generation successfully cancelled')
                main()
        except ValueError:
            print(BOLD + RED + '\n[-] ERROR : Non-numeric value inputted' + NORM)
            continue
        else:
            password_set = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.SystemRandom().choice(password_set)
                for _ in range(user_input_length))
            with open('passwords.txt', 'a') as passwordfile:
                passwordfile.writelines(password + '\n\n')
            print(BOLD + GREEN + '\n[+] Password has been generated successfully')
            main()
        break

def generate_key():  # generates symmetric cryptographic key
    if os.path.exists('passwords-key.key'):
        print(BOLD + RED + "\n[-] ERROR: Key already exists")
    else:
        key = Fernet.generate_key()
        with open('passwords-key.key', 'wb') as filekey:
            filekey.write(key)
        print(BOLD + GREEN + "\n[+] Symmetric cryptographic key has successfully been created")
    main()

def wipe_key():
    if os.path.exists("passwords-key.key"):
        os.remove("passwords-key.key")
        print(BOLD + GREEN + '\n[+] Key has successfully been wiped')
    else:
        print(BOLD + RED + "\n[-] ERROR: Cryptographic key does not exist")
    main()

def wipe_text_file():
    if os.path.exists('passwords.txt'):
        os.remove('passwords.txt')
        print(BOLD + GREEN + "\n[+] Text file has successfully been wiped")
    else:
        print(BOLD + RED + "\n[-] ERROR: Text file does not exist")
    main()

def open_text_file():
    if os.path.exists('passwords.txt'):
        if current_os == "Windows":
            subprocess.call(["start", 'passwords.txt'], shell=True)
            print(
            BOLD + GREEN + 
            "\n[+] Text file successfully opened"
            + NORM + BOLD + 
            '\n\n[>] Close the Notepad window to continue using the Password Generator')
        elif current_os == "Darwin":
            subprocess.call(["open", 'passwords.txt'])
            print(
            BOLD + GREEN + 
            "\n[+] Text file successfully opened")
        elif current_os == "Linux":
            subprocess.call(["xdg-open", 'passwords.txt'])
            print(
            BOLD + GREEN + 
            "\n[+] Text file successfully opened"
            + NORM + BOLD + 
            '\n\n[>] Close the window of the text editor to continue using the Password Generator')
    else:
        print(BOLD + RED + "\n[-] ERROR: Text file does not exist")
    main()

def encrypt_text_file():  # encrypts text file with symmetric cryptographic key
    if os.path.exists('passwords-key.key') and os.path.exists('passwords.txt'):
        with open('passwords-key.key', 'rb') as filekey:
            key = filekey.read()  # opens symmetric cryptographic key; checks for an existing key 
        fernet = Fernet(key)  # creates symmetric cryptographic key
        with open('passwords.txt', 'rb') as text_file:  
            original_text_file = text_file.read() # opens to-be-encrypted text file
        encrypted = fernet.encrypt(original_text_file)  # creates encrypted data
        with open('passwords.txt','wb') as encrypted_text_file:  
            encrypted_text_file.write(encrypted) # opens text file in write only mode and replaces original data with encrypted data
        print(BOLD + GREEN + '\n[+] Text file has successfully been encrypted')
    else:
        print(BOLD + RED + '\n[-] ERROR: Key and/or text file is missing')
    main()

def decrypt_text_file():  # decrypts text file with symmetric cryptographic key
    if os.path.exists('passwords-key.key') and os.path.exists('passwords.txt'):
        with open('passwords-key.key', 'rb') as filekey:
                key = filekey.read()  # opens symmetric cryptographic key; checks for an existing key
        fernet = Fernet(key)  # creates symmetric cryptographic key
        with open('passwords.txt', 'rb') as enc_text_file: 
            encrypted = enc_text_file.read()  # opens encrypted text file using generated key
        decrypted = fernet.decrypt(encrypted)  
        with open('passwords.txt', 'wb') as dec_text_file:
            # opens text file in write only mode and replaces encrypted data with decrypted data
            dec_text_file.write(decrypted)  
        print(BOLD + GREEN + '\n [+] Text file has been successfully decrypted')
    else:
        print(BOLD + RED + '\n[-] ERROR: Key and/or text file is missing')
    main()

def commands_and_arguments():
    print(
        BOLD +
        '\n[>] -g [p/k], --gen [p/k]  : generate password/symmetric cryptographic key'
        '\n    -w [t/k], --wipe [t/k] : wipe text file/symmetric cryptographic key'
        '\n    o                      : open text file'
        '\n    e                      : encrypt text file'
        '\n    d                      : decrypt text file'
        '\n    exit                   : exit script'
        '\n    h, help                : shows this list of in-built commands and necessary arguments')
    main()

def main():
    user_input = input(NORM + '\n' + get_cwd + '> ')
    if user_input in ['-g p', '--gen p']:
        generate_password()
    elif user_input in ['-g k', '--gen k']:
        generate_key()
    elif user_input in ['-w t', '--wipe t']:
        wipe_text_file()
    elif user_input in ['-w k', '--wipe k']:
        wipe_key()
    elif user_input == 'o':
        open_text_file()
    elif user_input == 'e':
        encrypt_text_file()
    elif user_input == 'd':
        decrypt_text_file()
    elif user_input in ['h', 'help']:
        commands_and_arguments()
    elif user_input == 'exit':
        print(BOLD + GREEN + "\n[+] Exiting script...\n")
        # exits the script   
        raise SystemExit()   
    else:
        print(
            BOLD + RED +
            "\n[-] ERROR : '" + user_input + "' is not recognised as a command or an argument"
            + NORM + BOLD +
            "\n\n[>] Use 'h' or 'help' to view the list of in-built commands and necessary arguments")
        main()
    
if __name__ == "__main__":
    display_banner()
    main()