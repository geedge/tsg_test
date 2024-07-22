# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import requests

class SslPlayer():
    def send_ssl_traffic(self, command, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send ssl traffic for effect verification.", flush=True)
        # command = "curl -kv --connect-timeout {} -m {} {}".format(command_dict["connect_timeout"], command_dict["timeout"], command_dict["url"])
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = p.communicate()
        cmd_result = output + error
        return cmd_result
    
    def send_get_request(url):  
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"RequestException: {e}"

    def send_post_request(url, data=None, json=None):  
        try:
            # 可以根据需要选择发送data（表单数据）或json（JSON数据）
            if json:
                response = requests.post(url, json=json)
            else:  
                response = requests.post(url, data=data)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:  
            return f"RequestException: {e}"
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
