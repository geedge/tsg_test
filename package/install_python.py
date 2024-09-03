# -*- coding: UTF-8 -*-
import os
import subprocess
from datetime import datetime 

def install_python():
    try:
        # output = subprocess.check_output(["python3", "-V"], shell=True)
        # match = re.search(r'Python (\d+\.\d+\.\d+)', output)
        # if match:
        #     version_str = match.group(1)
        #     version_tuple = tuple(map(int, version_str.split('.')))
        #     if version_tuple < tuple(map(int, "3.12.4".split('.'))):
        # subprocess.check_call(["yum", "clean", "all"])
        # subprocess.check_call(["yum", "makecache"])
        # subprocess.check_call(["yum", "install", "-y", "epel-release", "zlib-devel", "bzip2-devel", "openssl-devel", "ncurses-devel", "sqlite-devel", "readline-devel", "tk-devel", "gcc", "make"])
        os.chdir("/opt")
        subprocess.check_call(["wget", "https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz"])
        subprocess.check_call(["tar", "xvf", "Python-3.12.4.tgz"])
        os.chdir("/opt/Python-3.12.4")
        subprocess.check_call(["./configure", "--enable-optimizations"])
        subprocess.check_call(["make", "altinstall"])
        subprocess.check_call(["ln", "-s", "-f", "/usr/local/bin/python3.12", "/usr/bin/python3"])
        subprocess.check_call(["ln", "-s", "-f", "/usr/local/bin/pip3.12", "/usr/bin/pip3"])
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Install python successfully.")
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to install python.")
        
if __name__ == '__main__':
    install_python()