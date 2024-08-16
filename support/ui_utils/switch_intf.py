# -*- coding: UTF-8 -*-
import subprocess
from datetime import datetime 

class SwitchIntf:
    def switch_intf(self, intf_1, intf_2):
        try:
            subprocess.check_call(["ifconfig", intf_1, "up"])
            subprocess.check_call(["ifconfig", intf_2, "down"])
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Switch intf successfully.")
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to switch intf.")
        
if __name__ == '__main__':
    intf_1 = "ens22"
    intf_2 = "ens19"
    switch = SwitchIntf()
    switch.switch_intf(intf_1, intf_2)