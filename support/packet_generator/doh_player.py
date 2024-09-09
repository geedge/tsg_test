# -*- coding: utf-8 -*-
from datetime import datetime
import requests

class DohPlayer:
    def send_doh_query(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send doh query for effect verification.", flush=True)
        
        domain = traffic_data["domain"]
        query_type = traffic_data["query_type"]
        doh_server_url = traffic_data["doh_server_url"]
        
        query = {  
            "type": query_type,
            "name": domain
        }
        headers = {  
            "accept": "application/dns-json",
            "content-type": "application/dns-json"
        }
        response = requests.post(doh_server_url, json=query, headers=headers)
        
        response_data = ""
        if response.status_code == 200:
            response_data = response.json()
            if 'Answer' in response_data:
                for answer in response_data['Answer']:
                    return f"Name: {answer['name']}, Type: {answer['type']}, Data: {answer['data']}"
            else:  
                return "No answer found."
        else:
            return f"Error querying DoH server: {response.status_code}"
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "doh",
            "type": "client",
            "domain": "www.baidu.com", # ipv6.google.com
            "query_type": "A", # AAAA
            "doh_server_url": "https://dns9.quad9.net"
        }
    }
    traffic_data = test_data["traffic"]
    doh_player = DohPlayer()
    doh_player.send_doh_query(traffic_data, "ui", False)
