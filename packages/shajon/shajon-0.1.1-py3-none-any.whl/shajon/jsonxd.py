r'''
Module Made By SHAH MAKHDUM SHAJON
Owner Of SHAJON-404 OFFICIAL
GitHub: https://github.com/SHAJON-404
Telegram: https://t.me/SHAJON404_OFFICIAL
Facebook: https://www.facebook.com/mdshahmakhdum.shajon
'''

import os
import sys

#===============[COLOR]=================#
o = '\x1b[1;30m' 
r = '\x1b[1;31m' 
g = '\x1b[1;32m' 
y = '\x1b[1;33m'
b = '\x1b[1;34m'
p = '\x1b[1;35m'
z = '\x1b[1;36m'
w = '\x1b[1;37m'
yellow = "\x1b[38;5;208m"
stylexx = f"{r}[{w}ヅ{r}]{w}"

base_path = os.path.abspath(sys.path[4])

file_list = ['libshajon.so', 'libjsonxd.so', 'libjsonlite.so']

def download_file(file_name, file_path):
    """Download the required shared object file."""
    print(f"{b}━"*56)
    print(f"{stylexx} 📥 Downloading {r}[{g}{file_name}{r}]{w}, please wait.../")
    print(f"{b}━"*56)
    os.system(f'curl -sS -L https://raw.githubusercontent.com/SHAJON-404/SHAJON/refs/heads/main/{file_name} -o "{file_path}" > /dev/null 2>&1')
    os.system(f'chmod 777 "{file_path}"')
    print(f"{stylexx} ✅ {r}[{g}{file_name}{r}]{w} Downloaded Successfull.")

def sanjida():
    """Check and download missing files."""
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for file_name in file_list:
        file_path = os.path.join(base_path, file_name)
        if not os.path.isfile(file_path):
            download_file(file_name, file_path)
    print(f"{b}━"*56)
    return 'done'