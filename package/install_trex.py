# -*- coding: UTF-8 -*-
import os
import platform
import subprocess

def install_trex():
    try:
        subprocess.check_call(["mkdir", "-p", "/opt/trex"])
        os.chdir("/opt/trex")
        subprocess.check_call(["wget", "--no-check-certificate", "--no-cache", "https://trex-tgn.cisco.com/trex/release/latest"])
        subprocess.check_call(["tar", "-xzf", "latest"])
        print("Install TRex successfully.")
    except:
        print("Fail to install TRex.")
        
if __name__ == '__main__':
    install_trex()