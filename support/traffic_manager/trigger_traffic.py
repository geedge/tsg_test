# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import requests
import configparser
from support.traffic_manager.http_player import HttpPlayer
from support.traffic_manager.ssl_player import SslPlayer
from support.traffic_manager.ftp_player import FtpPlayer
from support.traffic_manager.dns_player import DnsPlayer
from support.traffic_manager.mail_player import MailPlayer
from support.traffic_manager import trex_replay
from support.traffic_manager.workpath import workdir
from datetime import datetime

class TriggerTraffic():
    def trigger_traffic(self, parameter, test_data):
        script_type = parameter["script_type"]
        debug_flag = ""
        if "debug_flag" in parameter.keys():
            debug_flag = parameter["debug_flag"]
        if debug_flag == "local":
            temp_data = json.dumps(test_data["traffic"])
            parse = configparser.ConfigParser()
            parse_dir = os.path.join(workdir, "configuration_file.ini")
            parse.read(parse_dir, encoding="utf-8")
            if script_type == "api":
                traffic_server = parse.get("traffic_server", "api_server_url")
            elif script_type == "ui":
                traffic_server = parse.get("traffic_server", "ui_server_url")
            port = parse.get("traffic_port", "server_port")
            url = traffic_server + ":" + port + "/v1/traffic"
            headers = {"Content-Type": "application/json"}
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send traffic for effect verification.", flush=True)
            response = requests.post(url, data=temp_data, headers=headers)
            if response.status_code == 200:
                try:
                    jsonData = json.loads(response.text)
                except:    # json解析失败，直接返回json原文
                    jsonData = {}
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "json loads failed:", flush=True)
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{} {} \n{}".format(url, temp_data, response.text), flush=True)
                    jsonData["result"] = response.text
                result = jsonData
        else:
            if len(test_data["traffic"]["protocol"]) > 0:
                temp_data = test_data["traffic"]["command"]
            elif len(test_data["traffic"]["protocol"]) == 0:
                temp_data = test_data["traffic"]
            if test_data["traffic"]["protocol"] == "http":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use curl to simulate http/https traffic.", flush=True)
                player = HttpPlayer()
                result = player.send_http_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "https" or test_data["traffic"]["protocol"] == "ssl":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use curl to simulate http/https traffic.", flush=True)
                player = SslPlayer()
                result = player.send_ssl_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "ftp":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use curl to simulate ftp traffic.", flush=True)
                player = FtpPlayer()
                result = player.send_ftp_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "dns":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use curl to simulate nslookup traffic.", flush=True)
                player = DnsPlayer()
                result = player.send_dns_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "mail":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use curl to simulate mail traffic.", flush=True)
                player = MailPlayer()
                result = player.send_mail_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use trex to replay traffic.", flush=True)
                pcap_name = temp_data.get("pcap_name") + ".pcap"
                yaml_name = temp_data.get("yaml_name") + ".yaml"
                m = temp_data.get("m")
                d = temp_data.get("d")
                clients_start_ip = temp_data.get("clients_start_ip")
                clients_end_ip = temp_data.get("clients_end_ip")
                servers_start_ip = temp_data.get("servers_start_ip")
                servers_end_ip = temp_data.get("servers_end_ip")
                path_dict = {
                    "trex_workpath": "/opt/trex/v3.05",
                    "traffic_playback_workpath": "/opt/tsg_test/support/traffic_replay"
                }
                path = "/opt/trex"
                entries = os.listdir(path)  
                dir_names = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
                if len(dir_names) == 1:
                    join_trex_workpath = "/opt/trex/{}".format(dir_names[0])
                    path_dict["trex_workpath"] = join_trex_workpath
                parse = configparser.ConfigParser()
                parse_dir = os.path.join(workdir, "configuration_file.ini")
                parse.read(parse_dir, encoding="utf-8")
                path_dict["traffic_playback_workpath"] = parse.get("traffic_playback", "traffic_playback_workpath")
                tr = trex_replay.TrafficReplay(path_dict)
                result = tr.trex_playback(yaml_name, pcap_name, m, d, clients_start_ip, clients_end_ip, servers_start_ip, servers_end_ip)
        return result
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")