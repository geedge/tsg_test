# -*- coding: utf-8 -*-
import os
import sys
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
    def run(self, policy_configuration, traffic_generation):
        self.traffic_generation = traffic_generation
        debug = "local"
        if debug == "local":
            #traffic_generation["type"]=traffic_generation["tool"]
            traffic_generation_json_str = json.dumps(traffic_generation)
            parse = configparser.ConfigParser()
            parse_dir = os.path.join(workdir, "configuration_file.ini")
            parse.read(parse_dir, encoding="utf-8")
            traffic_server = parse.get("traffic_server", "url")
            port = parse.get("traffic_port", "server_port")
            url = traffic_server + ":" + port + "/v1/traffic"
            headers = {"Content-Type": "application/json"}
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send traffic for effect verification.", flush=True)
            response = requests.post(url, data=traffic_generation_json_str, headers=headers)
            #print(response.text)
            if response.status_code == 200:
                # 如果response.text是json格式，则需要通过json.loads解析。如果不是json格式，则直接返回赋值
                parse_boolean = True
                try:
                    json_data = json.loads(response.text)
                except:
                    parse_boolean = False
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "json loads failed:", flush=True)
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{} {} \n{}".format(url, traffic_generation_json_str, response.text), flush=True)
                if parse_boolean == False:
                    json_data = {}
                    json_data = response.text
                result = json_data["result"]
        else:
            if traffic_generation["tool"] == "http":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate http traffic.", flush=True)
                player = HttpPlayer()
                result = player.send_http_traffic(traffic_generation)
            elif traffic_generation["tool"] == "https" or traffic_generation["tool"] == "ssl":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate ssl traffic.", flush=True)
                player = SSLPlayer()
                result = player.send_ssl_traffic(traffic_generation)
            elif traffic_generation["tool"] == "ftp":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate ftp traffic.", flush=True)
                player = FtpPlayer()
                result = player.send_ftp_traffic(traffic_generation)
            elif traffic_generation["tool"] == "dns":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate dns traffic.", flush=True)
                player = DnsPlayer()
                result = player.send_dns_query(traffic_generation)
            elif traffic_generation["tool"] == "mail":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate mail traffic.", flush=True)
                player = MailPlayer()
                result = player.send_mail_traffic(traffic_generation)
            elif traffic_generation["tool"] == "doh":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate doh traffic.", flush=True)
                player = DohPlayer()
                result = player.send_doh_query(traffic_generation)
            elif traffic_generation["tool"] == "dtls":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate dtls traffic by client.", flush=True)
                # player = DtlsPlayer()
                # result = player.send_dtls_traffic(traffic_generation)
            elif traffic_generation["tool"] == "quic":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate quic traffic by client.", flush=True)
                result = quic_player.asyncio.run(quic_player.send_quic_traffic(traffic_generation))
            elif traffic_generation["tool"] == "mpls_one_label":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate mpls traffic by tcpreplay.", flush=True)
                player = MplsOneLabelPlayer()
                result = player.send_mpls_one_label_traffic(traffic_generation)
            elif traffic_generation["tool"] == "gre_over_gre":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate gre traffic by tcpreplay.", flush=True)
                player = GreOverGrePlayer()
                result = player.send_gre_over_gre_traffic(traffic_generation)
            elif traffic_generation["tool"] == "unordered_tcp":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate unordered tcp by tcpreplay.", flush=True)
                player = UnorderedTcpPlayer()
                result = player.send_unordered_tcp_traffic(traffic_generation)
            elif traffic_generation["tool"] == "vxlan":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Simulate vxlan traffic by tcpreplay.", flush=True)
                print("todo")
            elif traffic_generation["tool"] == "trex":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Use trex to replay traffic.", flush=True)
                pcap_name = traffic_generation.get("pcap_name") + ".pcap"
                yaml_name = traffic_generation.get("yaml_name") + ".yaml"
                m = traffic_generation.get("m",0)
                d = traffic_generation.get("d",0)
                if policy_configuration.get("type") == "dos_protection" and policy_configuration["action_parameter"]["type"] == "concurrency":
                    active_flows = policy_configuration.get("active_flows")
                else:
                    active_flows = 0
                clients_start_ip = traffic_generation.get("clients_start_ip")
                clients_end_ip = traffic_generation.get("clients_end_ip")
                servers_start_ip = traffic_generation.get("servers_start_ip")
                servers_end_ip = traffic_generation.get("servers_end_ip")
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
    
    def result(self, verification, traffic_result):
        try:
            if self.traffic_generation["tool"] == "trex":
                return True, ""
            expected_result_temp = verification["excepted_traffic_result"]
            result = all(word in traffic_result for word in expected_result_temp)
            #if not result:
            #    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'DEBUG:excepted_traffic_result:{};expected_result_temp:{};traffic_result_temp：{}'.format(result, expected_result_temp, traffic_result_temp), flush=True)
            if result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The traffic return traffic result match the expected result.', flush=True)
                return True, ""
            elif result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The traffic return result does not match the expected result.', flush=True)
                return False, "The traffic returned result does not match the expected result."
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception Error: ", str(e), flush=True)
            return False, "Exception Error when verify excepted traffic result: " + str(e)
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
