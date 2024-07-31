# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import dns.resolver

class DnsPlayer:
    def send_dns_query(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send dns traffic for effect verification.", flush=True)
        p = subprocess.Popen(traffic_data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = p.communicate()
        result = output + error
        
        # try:
        #     domain = traffic_data["domain"]
        #     query_type = traffic_data["query_type"]
        #     # 发送DNS查询请求
        #     answers = dns.resolver.query(domain, query_type)  
        #     # 获取查询结果
        #     result = [str(rdata) for rdata in answers]  
        #     return result
        # except dns.resolver.NXDOMAIN:
        #     return "Domain name does not exist."
        # except dns.resolver.NoAnswer:
        #     return "No record found."
        # except dns.resolver.NoNameservers:
        #     return "The DNS server cannot be found."
        # except Exception as e:
        #     return f"Exception: {e}"
        
        return result
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "dns",
            "domain": "www.google.com",
            "query_type": "A" # A, AAAA
        }
    }
    traffic_data = test_data["traffic"]
    dns_player = DnsPlayer()
    dns_player.send_dns_query(traffic_data, "ui", False)
