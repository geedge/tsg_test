# -*- coding: utf-8 -*-
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import requests
import configparser
from support.packet_generator.http_player import HttpPlayer
from support.packet_generator.ssl_player import SSLPlayer
from support.packet_generator.ftp_player import FtpPlayer
from support.packet_generator.dns_player import DnsPlayer
from support.packet_generator.mail_player import MailPlayer
# from support.packet_generator.dtls_player import DtlsPlayer
import support.packet_generator.quic_player as quic_player
from support.packet_generator import trex_replay
from support.packet_generator.doh_player import DohPlayer
from support.packet_generator.mpls_one_label_player import MplsOneLabelPlayer
from support.packet_generator.gre_over_gre_player import GreOverGrePlayer
from support.packet_generator.unordered_tcp_player import UnorderedTcpPlayer
from support.packet_generator.workpath import workdir
from datetime import datetime

class TrafficGenerator:
    def generate_traffic(self, parameter, test_data):
        script_type = parameter["script_type"]
        debug_flag = ""
        if "debug_flag" in parameter.keys():
            debug_flag = parameter["debug_flag"]
        if debug_flag == "local":
            if test_data["policy_type"] == "statistics" or test_data["policy_type"] == "service_chaining" and test_data["targeted_traffic"] == "raw" or test_data["policy_type"] == "dos_protection" or (test_data["policy_type"] == "monitor" and test_data["traffic"]["type"] == "trex"):
                test_data = self.replace_trex_ip(test_data, script_type)
            temp_data = json.dumps(test_data["traffic"])
            parse = configparser.ConfigParser()
            parse_dir = os.path.join(workdir, "configuration_file.ini")
            parse.read(parse_dir, encoding="utf-8")
            traffic_server = parse.get("traffic_server", "url")
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
                if test_data["policy_type"] == "statistics" or (test_data["policy_type"] == "service_chaining" and test_data["targeted_traffic"] == "raw")  or (test_data["policy_type"] == "monitor" and test_data["traffic"]["type"] == "trex") or test_data["policy_type"] == "dos_protection":
                    jsonData = jsonData["result"]
                result = jsonData
        else:
            if test_data["policy_type"] == "statistics" or test_data["policy_type"] == "service_chaining" and test_data["targeted_traffic"] == "raw" or  (test_data["policy_type"] == "monitor" and test_data["traffic"]["type"] == "trex") or test_data["policy_type"] == "dos_protection":
                test_data = self.replace_trex_ip(test_data, script_type)
            temp_data = test_data["traffic"]
            if test_data["traffic"]["protocol"] == "http":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate http traffic.", flush=True)
                player = HttpPlayer()
                result = player.send_http_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "https" or test_data["traffic"]["protocol"] == "ssl":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate ssl traffic.", flush=True)
                player = SSLPlayer()
                result = player.send_ssl_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "ftp":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate ftp traffic.", flush=True)
                player = FtpPlayer()
                result = player.send_ftp_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "dns":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate dns traffic.", flush=True)
                player = DnsPlayer()
                result = player.send_dns_query(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "mail":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate mail traffic.", flush=True)
                player = MailPlayer()
                result = player.send_mail_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "doh":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate doh traffic.", flush=True)
                player = DohPlayer()
                result = player.send_doh_query(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "dtls":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate dtls traffic by client.", flush=True)
                # player = DtlsPlayer()
                # result = player.send_dtls_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "quic":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate quic traffic by client.", flush=True)
                result = quic_player.asyncio.run(quic_player.send_quic_traffic(temp_data, script_type, debug_flag))
            elif test_data["traffic"]["protocol"] == "mpls":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate mpls traffic by tcpreplay.", flush=True)
                if test_data["traffic"]["type"] == "one_label":
                    player = MplsOneLabelPlayer()
                    result = player.send_mpls_one_label_traffic(temp_data, script_type, debug_flag)
                elif test_data["traffic"]["type"] == "two_label":
                    print("to be added")
            elif test_data["traffic"]["protocol"] == "gre":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate gre traffic by tcpreplay.", flush=True)
                if test_data["traffic"]["type"] == "gre_over_gre":
                    player = GreOverGrePlayer()
                    result = player.send_gre_over_gre_traffic(temp_data, script_type, debug_flag)
                elif test_data["traffic"]["type"] == "gre":
                    print("to be added")    
            elif test_data["traffic"]["protocol"] == "unordered_tcp":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate unordered tcp by tcpreplay.", flush=True)
                player = UnorderedTcpPlayer()
                result = player.send_unordered_tcp_traffic(temp_data, script_type, debug_flag)
            elif test_data["traffic"]["protocol"] == "vxlan":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate vxlan traffic by tcpreplay.", flush=True)
                print("to be added")
            elif test_data["traffic"]["protocol"] == "":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use trex to replay traffic.", flush=True)
                pcap_name = temp_data.get("pcap_name") + ".pcap"
                yaml_name = temp_data.get("yaml_name") + ".yaml"
                m = temp_data.get("m",0)
                d = temp_data.get("d",0)
                if test_data.get("policy_type") == "dos_protection" and test_data.get("threshold") and test_data["threshold"].get("type") == "concurrency":
                    active_flows = temp_data.get("active_flows")
                else:
                    active_flows = 0
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
                result = tr.trex_playback(yaml_name, pcap_name, active_flows, m, d, clients_start_ip, clients_end_ip, servers_start_ip, servers_end_ip)
        return result
    
    def replace_trex_ip(self, test_data, script_type):
        if script_type == "ui":
            if "source_ip" in test_data["condition"].keys():
                source_ip = test_data["condition"]["source_ip"]
                for ip_item in source_ip:
                    if ip_item["item"] == []:#UDP IP源目的方向不确定时把IP放到双方向时使用
                        continue
                    if "-" in ip_item["item"][0]["item_value"]:
                        test_data["traffic"]["clients_start_ip"] = ip_item["item"][0]["item_value"].split("-")[0]
                        test_data["traffic"]["clients_end_ip"] = ip_item["item"][0]["item_value"].split("-")[-1]
                    else:
                        test_data["traffic"]["clients_start_ip"] = ip_item["item"][0]["item_value"]
                        test_data["traffic"]["clients_end_ip"] = test_data["traffic"]["clients_start_ip"]
            if "destination_ip" in test_data["condition"].keys():
                destination_ip = test_data["condition"]["destination_ip"]
                for ip_item in destination_ip:
                    if ip_item["item"] == []:#UDP IP源目的方向不确定时把IP放到双方向时使用
                        continue
                    if "-" in ip_item["item"][0]["item_value"]:
                        test_data["traffic"]["servers_start_ip"] = ip_item["item"][0]["item_value"].split("-")[0]
                        test_data["traffic"]["servers_end_ip"] = ip_item["item"][0]["item_value"].split("-")[-1]
                    else:
                        test_data["traffic"]["servers_start_ip"] = ip_item["item"][0]["item_value"]
                        test_data["traffic"]["servers_end_ip"] = test_data["traffic"]["servers_start_ip"]
        elif script_type == "api":
            for ip_item in test_data["obj_condition_1"]:
                if "ATTR_SOURCE_IP" in ip_item.values():
                    if "-" in ip_item["object_list"][0]["add_item_list"][0]["ip_address"]:
                        test_data["traffic"]["clients_start_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[0]
                        test_data["traffic"]["clients_end_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[-1]
                    else:
                        test_data["traffic"]["clients_start_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"]
                        test_data["traffic"]["clients_end_ip"] = test_data["traffic"]["clients_start_ip"]
                if "ATTR_DESTINATION_IP" in ip_item.values():
                    if "-" in ip_item["object_list"][0]["add_item_list"][0]["ip_address"]:
                        test_data["traffic"]["servers_start_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[0]
                        test_data["traffic"]["servers_end_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[-1]
                    else:
                        test_data["traffic"]["servers_start_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"]
                        test_data["traffic"]["servers_end_ip"] = test_data["traffic"]["servers_start_ip"]
            if "library_condition" in test_data.keys():
                for ip_item in test_data["library_condition"]:
                        if "ATTR_SOURCE_IP" in ip_item.values():
                            if "-" in ip_item["library"][0]["catalogs"][0]["ip_entries"]:
                                test_data["traffic"]["clients_start_ip"] = ip_item["library"][0]["catalogs"][0]["ip_entries"].split("-")[0]
                                test_data["traffic"]["clients_end_ip"] = ip_item["library"][0]["catalogs"][0]["ip_entries"].split("-")[-1]
                            else:
                                test_data["traffic"]["clients_start_ip"] = ip_item["library"][0]["catalogs"][0]["ip_entries"]
                                test_data["traffic"]["clients_end_ip"] = test_data["traffic"]["clients_start_ip"]
                        if "ATTR_DESTINATION_IP" in ip_item.values():
                            if "-" in ip_item["library"][0]["catalogs"][0]["ip_entries"]:
                                test_data["traffic"]["servers_start_ip"] = ip_item["library"][0]["catalogs"][0]["ip_entries"].split("-")[0]
                                test_data["traffic"]["servers_end_ip"] = ip_item["library"][0]["catalogs"][0]["ip_entries"].split("-")[-1]
                            else:
                                test_data["traffic"]["servers_start_ip"] = ip_item["library"][0]["catalogs"][0]["ip_entries"]
                                test_data["traffic"]["servers_end_ip"] = test_data["traffic"]["servers_start_ip"]
        return test_data
    
if __name__ == "__main__":
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test"

    parameter = {
        "username": "lina2024",
        "password": "lina2024",
        "test_pc_ip": "192.168.64.96",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
        "module_name": "dos_protection",
        "test_case_name":"dos_trex_replay_test"
    }

    test_data = {
        "is_multi_priority": False,
        "rule_num": 1,
        "policy_type": "dos_protection",
        "rule_name": "dos_protect_srcip_http_concurrency_srcip_d3",
        "rule_action": "protect",
        "rule_type": "create",
        "do_log": 2,
        "condition": {
            "source_ip": [
                {
                    "name": "dos_srcip",
                    "object_type": "ip",
                    "select_type": False,
                    "negate": False,
                    "item": [
                        {
                            "item_operation": "add",
                            "item_type": "ipv4",
                            "item_value": "10.64.9.1",
                        }
                    ]
                }
            ],
            "application": [
                {
                    "name": "http",
                    "object_type": "application",
                    "negate": False
                }
            ]
        },
        "threshold": {
            "type": "concurrency",
            "concurrency_threshold": {
                "group_by": "source_ip",
                "concurrent_sessions": 1
            }
        },
        "mitigation": {
            "behavior": "deny",
            "timeout": "5min"
        },
        "expected_return": "",
        "counters": {"hits": "many"},
        "log_query_param": [
            # {"query_field_key": "basic_attack_type", "query_value": "tcp_syn_flood"},
            # {"query_field_key": "basic_sessions", "query_value": ""},
            # {"query_field_key": "basic_session_rate", "query_value": ""},
            # {"query_field_key": "basic_packets", "query_value": ""},
            # {"query_field_key": "basic_packet_rate", "query_value": ""},
            # {"query_field_key": "basic_bytes", "query_value": ""},
            # {"query_field_key": "basic_bit_rate", "query_value": ""},
            {"query_field_key": "attack_type", "query_value": "custom_network_attack"},
            {"query_field_key": "sessions", "query_value": ""},
            {"query_field_key": "packets", "query_value": ""},
            {"query_field_key": "bytes", "query_value": ""},
            {"query_field_key": "bit_rate", "query_value": ""},
            {"query_field_key": "packet_rate", "query_value": ""},
            {"query_field_key": "session_rate", "query_value": ""},
        ],
         "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "1.1.1.1",
                "clients_end_ip": "1.1.1.1",
                "servers_start_ip": "2.1.1.9",
                "servers_end_ip": "2.1.1.9",
                "active_flows":2,
                "m": 1,
                "d": 5,
                "yaml_name": "test",
                "pcap_name": "http"

            },
        "token": ""
    }
    sender = TrafficGenerator()
    result = sender.generate_traffic(parameter, test_data)
