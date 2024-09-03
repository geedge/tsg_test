# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import requests
# import http.client
from scapy.all import *
from scapy.layers.inet import TCP

class SSLPlayer:
    def send_ssl_traffic(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send ssl traffic for effect verification.", flush=True)
        if "command" in traffic_data:
            p = subprocess.Popen(traffic_data["command"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
            output, error = p.communicate()
            result = output + error
        elif "command" not in traffic_data:
            action = traffic_data["action"]
            url = traffic_data["url"]
            if action == "get":
                result = self.send_get_request(url)
            elif action == "post":
                result = self.send_post_request(url)
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
        
    def get_http_method(self):
        pcap_file = "d:/zk.pcap"
        packets = rdpcap(pcap_file)
        http_methods = []
        for p in packets:
            if TCP in p:
                for tls_record in p[TCP].payload:
                    if "handshake" in tls_record.payload:
                        handshake = tls_record.payload["handshake"]
                        if "ClientHello" in handshake:
                            tls_app_data = p[TCP:].payload.payload
                            if tls_app_data:
                                ssl_record = tls_app_data[0]
                                if "ApplicationData" in ssl_record.payload:
                                    http_payload = ssl_record.payload["ApplicationData"]
                                    http_request = http_payload.load
                                    http_methods.append(http_request.method)
                                    print(http_methods)
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "ssl",
            "type": "client", # client/curl
            "action": "post", # get/post
            "url": "https://www.google.com"
        }
    }
    traffic_data = test_data["traffic"]
    ssl_player = SSLPlayer()
    ssl_player.send_ssl_traffic(traffic_data, "ui", False)
    # ssl_player.get_http_method()
