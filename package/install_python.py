# -*- coding: UTF-8 -*-
import os
import platform
import subprocess
from datetime import datetime 

def install_python():
    try:
        subprocess.check_call(["yum clean all && yum makecache"])
        subprocess.check_call(["yum", "install", "-y", "libffi-devel zlib zlib-dev zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel mysql-devel readline-devel tk-devel libffi libffi-devel gcc gcc-c++ make"])
        os.chdir("/opt")
        subprocess.check_call(["wget", "https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz"])
        subprocess.check_call(["tar", "xvf", "Python-3.12.4.tgz"])
        os.chdir("/opt/Python-3.12.4")
        subprocess.check_call(["./configure --enable-optimizations"])
        subprocess.check_call(["make", "altinstall"])
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Install python successfully.")
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to install python.")
        
if __name__ == '__main__':
    install_python()