# -*- coding: UTF-8 -*-
import os
import platform
import subprocess
from datetime import datetime 

def install_package():
    try:
        os.chdir("/opt")
        subprocess.check_call(["wget", "https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-122.0.6261.111-1.x86_64.rpm"])
        subprocess.check_call(["yum", "localinstall", "-y", "google-chrome-stable-122.0.6261.111-1.x86_64.rpm"])
        subprocess.check_call(["wget", "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chromedriver-linux64.zip"])
        subprocess.check_call(["unzip", "chromedriver-linux64.zip"])
        subprocess.check_call(["mv", "chromedriver-linux64/chromedriver", "/usr/local/bin"])
        subprocess.check_call(["chmod", "777", "/usr/local/bin/chromedriver"])
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Install chrome and chromedriver successfully.")
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to install chrome and chromedriver.")
        
if __name__ == '__main__':
    install_package()