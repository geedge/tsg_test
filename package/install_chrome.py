# -*- coding: UTF-8 -*-
import os
import platform
import subprocess

def install_package():
    try:
        with open("/usr/bin/yum", "r") as file:
            content = file.readlines()
        content[0] = "#!/usr/bin/python2.7\n"
        with open("/usr/bin/yum", "w") as file:
            file.writelines(content)
        # subprocess.check_call(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm"])
        # subprocess.check_call(["yum", "localinstall", "-y", "google-chrome-stable_current_x86_64.rpm"])
        # result = subprocess.check_output("google-chrome --version", shell=True)
        # output = result.decode("utf-8")
        # if len(output) > 0:
        #     temp = output.split(" ", 2)
        #     if len(temp) > 2:
        #         chrome_version = temp[2].rstrip()
        #         url = "https://storage.googleapis.com/chrome-for-testing-public/{}/linux64/chromedriver-linux64.zip".format(chrome_version)
        #     subprocess.check_call(["wget", url])
        #     subprocess.check_call(["unzip", "chromedriver-linux64.zip"])
        #     subprocess.check_call(["mv", "chromedriver-linux64/chromedriver", "/usr/local/bin"])
        #     subprocess.check_call(["chmod", "777", "/usr/local/bin/chromedriver"])
        subprocess.check_call(["wget", "https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-122.0.6261.111-1.x86_64.rpm"])
        subprocess.check_call(["yum", "localinstall", "-y", "google-chrome-stable-122.0.6261.111-1.x86_64.rpm"])
        subprocess.check_call(["wget", "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chromedriver-linux64.zip"])
        subprocess.check_call(["unzip", "chromedriver-linux64.zip"])
        subprocess.check_call(["mv", "chromedriver-linux64/chromedriver", "/usr/local/bin"])
        subprocess.check_call(["chmod", "777", "/usr/local/bin/chromedriver"])
        print("Install chrome and chromedriver successfully.")
    except:
        print("Fail to install chrome and chromedriver.")
        
if __name__ == '__main__':
    install_package()