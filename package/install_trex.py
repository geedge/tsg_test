# -*- coding: UTF-8 -*-
import os
import subprocess

def install_trex():
    try:
        output = subprocess.check_output("find /etc -name 'trex_cfg.yaml'", shell=True).decode('utf-8')
        if len(output) > 0:
            print("TRex has been installed.")
        else:
            subprocess.check_call(["mkdir", "-p", "/opt/trex"])
            os.chdir("/opt/trex")
            subprocess.check_call(["wget", "--no-check-certificate", "--no-cache", "https://trex-tgn.cisco.com/trex/release/latest"])
            subprocess.check_call(["tar", "-xzf", "latest"])
            subprocess.check_call(["cp", "/opt/trex/v3.04/cfg/simple_cfg.yaml", "/etc/trex_cfg.yaml"])
            os.chdir("/opt/trex/v3.04")
            output = subprocess.check_output("./dpdk_setup_ports.py -s", shell=True).decode('utf-8')
            # 注意：eth1和eth2是网卡名称，根据实际情况修改，并且需要保证这两个网卡的防火墙是关闭的
            intf_list = search(output, ["eth1", "eth2"])
            file_path = "/etc/trex_cfg.yaml"
            file_overwrite(file_path, intf_list)
            print("Install TRex successfully.")
    except:
        print("Fail to install TRex.")

def search(output, list):
    try:
        temp_list = []
        lines = output.split('\n')
        for i in range(len(list)):
            for line in lines:
                if list[i] in line:
                    temp = line.split()
                    if temp:
                        temp_list.append(temp[0])
        print("Search successfully.")
        return temp_list
    except:
        print("Fail to search.")
        return temp_list
    
def file_overwrite(file_path, replacement_value):
    try:
        target_value = "interfaces"
        with open(file_path, 'r') as file:
            lines = file.readlines()
        fourth_line_parts = lines[3].split(": ")
        if target_value == fourth_line_parts[0].strip():
            temp = "[" + ','.join(f"'{item}'" for item in replacement_value) + "]"
            lines[3] = "  " + target_value + ": " + temp + "\n"
        with open(file_path, 'w') as file:  
            file.writelines(lines) 
        print("Overwrite successfully.")
    except:
        print("Fail to overwrite.")
        
if __name__ == '__main__':
    install_trex()