import os  
import subprocess  
from datetime import datetime 

def install_go():
    try:
        os.chdir("/opt")
        subprocess.check_call(["wget", "https://golang.google.cn/dl/go1.23.2.linux-amd64.tar.gz"])
        subprocess.check_call(["tar", "-C", "/usr/local", "-xzf", "go1.23.2.linux-amd64.tar.gz"])
        # command_1 = f'echo \'export PATH=$PATH:/usr/local/go/bin\' >> {os.path.expanduser("~")}/.bash_profile'
        # subprocess.check_call(command_1, shell=True)
        # command_2 = f'echo \'export GOPATH={os.path.expanduser("~")}/go\' >> {os.path.expanduser("~")}/.bash_profile'
        # subprocess.check_call(command_2, shell=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Install go successfully.")
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to install go.")

if __name__ == "__main__":
    install_go()