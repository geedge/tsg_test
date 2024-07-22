# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import dns.resolver

class DnsPlayer():
    def send_dns_traffic(self, command, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send dns traffic for effect verification.", flush=True)
        # command = "curl -kv --connect-timeout {} -m {} {}".format(command_dict["connect_timeout"], command_dict["timeout"], command_dict["url"])
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = p.communicate()
        cmd_result = output + error
        return cmd_result
    
    def query_dns(domain_name, record_type):  
        """  
        查询指定域名的DNS记录。  
        :param domain_name: 要查询的域名  
        :param record_type: DNS记录类型，默认为'A'（IPv4地址）  
        :return: 记录的列表  
        """  
        try:
            # 发送DNS查询请求
            answers = dns.resolver.resolve(domain_name, record_type)  
            # 获取查询结果
            result = [str(rdata) for rdata in answers]  
            return result  
        except dns.resolver.NXDOMAIN:
            return "Domain name does not exist."
        except dns.resolver.NoAnswer:
            return "No record found."
        except dns.resolver.NoNameservers:
            return "The DNS server cannot be found."
        except Exception as e:
            return f"Exception: {e}"
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
