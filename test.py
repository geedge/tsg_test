# -*- coding: UTF-8 -*-
import os
import subprocess

def test(file_path, replacement_value):
    try:
        xx = "aa"
        yy = " " + xx + "  " + xx
        target_value = "interfaces"
        with open(file_path, 'r') as file:
            lines = file.readlines()
        print(lines[3])
        fourth_line_parts = lines[3].split(": ")
        if target_value == fourth_line_parts[0].strip():
            print(111)
            temp = "[" + ','.join(f"'{item}'" for item in replacement_value) + "]"
            lines[3] = " " + " " + target_value + " " + + ": " + temp + "\n"
            print(lines[3])
        with open(file_path, 'w') as file:  
            file.writelines(" " + " " + target_value + " " + + ": " + temp + "\n")  
        print("Overwrite successfully.")
    except:
        print("Fail to overwrite.")
        
if __name__ == '__main__':
    test("/etc/trex_cfg.yaml", ['0000:00:13.0', '0000:00:14.0'])