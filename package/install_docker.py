# -*- coding: UTF-8 -*-
import os
import subprocess

def install_trex():
    try:
        subprocess.check_call(["yum", "install", "-y", "yum-utils", "device-mapper-persistent-data", "lvm2"])
        subprocess.check_call(["yum-config-manager", "--add-repo", "https://download.docker.com/linux/centos/docker-ce.repo"])
        subprocess.check_call(["yum", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"])
        subprocess.check_call(["systemctl", "start", "docker"])
        subprocess.check_call(["systemctl", "enable", "docker"])
        print("Install docker successfully.")
    except:
        print("Fail to install docker.")
        
if __name__ == '__main__':
    install_trex()