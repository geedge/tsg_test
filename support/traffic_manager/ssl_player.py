# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import requests
import http.client

class SslPlayer():
    def send_ssl_traffic(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send ssl traffic for effect verification.", flush=True)
        # command = "curl -kv --connect-timeout {} -m {} {}".format(command_dict["connect_timeout"], command_dict["timeout"], command_dict["url"])
        p = subprocess.Popen(traffic_data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = p.communicate()
        result = output + error
        
        # type = traffic_data["type"]
        # url = traffic_data["url"]
        # if type == "get":
        #     result = self.send_get_request(url)
        # elif type == "post":
        #     result = self.send_post_request(url)
            
        return result
    
    def send_get_request(self, url):  
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"RequestException: {e}"

    def send_post_request(self, url, data=None, json=None):  
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
    test_data = {
        "traffic": {
            "protocol": "ssl",
            "type": "get", # get/post
            "url": "https://192.168.40.206:1443/go"
        }
    }
    traffic_data = test_data["traffic"]
    ssl = SslPlayer()
    ssl.send_ssl_traffic(traffic_data, "ui", False)
