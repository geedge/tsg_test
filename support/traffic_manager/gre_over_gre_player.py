# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.traffic_manager.workpath import workdir
import configparser
import subprocess
import random
from scapy.all import *
from scapy.contrib.mpls import *
from scapy.layers.inet import IP, TCP
from datetime import datetime

class GreOverGrePlayer:
    def send_gre_over_gre_traffic(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send gre over gre traffic for effect verification.", flush=True)
        try:
            pcap = traffic_data["pcap_name"] + ".pcap"
            parse = configparser.ConfigParser()
            parse_dir = os.path.join(workdir, "configuration_file.ini")
            parse.read(parse_dir, encoding="utf-8")
            traffic_manager_path = parse.get("traffic_playback", "traffic_playback_workpath")
            intf = parse.get("tcpreplay", "intf")
            inner_client_ip = parse.get("tcpreplay", "client_ip")
            inner_server_ip = parse.get("tcpreplay", "server_ip")
            # inner_client_ip = "192.64.{}.{}".format(random.randint(1, 254), random.randint(1, 254))
            # inner_server_ip = "192.64.{}.{}".format(random.randint(1, 254), random.randint(1, 254))
            client_port = random.randint(1000, 60000)
            
            pcap_root_path = traffic_manager_path + "/traffic_pcap/"
            pcap_path = traffic_manager_path + "/traffic_pcap/" + pcap
            pkts = rdpcap(pcap_path)
            first_client_ip = pkts[0][MPLS][MPLS][IP].src

            new_pkts_list, new_pkts_list_sum = [], []
            current_time = time.time()
            sum_time = 5
            pkts_temp = copy.deepcopy(pkts)
            unit_time = sum_time / len(pkts_temp)
            pkt_count = 1
            for pkt in pkts_temp:
                pkt_count = pkt_count + 1
                if pkt[4].src == first_client_ip:
                    pkt[4].src = inner_client_ip
                    pkt[4].dst = inner_server_ip
                    pkt[TCP].sport = client_port
                else :
                    pkt[4].src = inner_server_ip
                    pkt[4].dst = inner_client_ip
                    pkt[TCP].dport = client_port
                current_time += unit_time
                pkt.time = current_time
                new_pkts_list.append(pkt)
            new_pkts_list_sum.extend(copy.deepcopy(new_pkts_list))

            temp_pcap_name = "temp_{}.pcap".format(traffic_data["pcap_name"])
            temp_pcap_name_path = os.path.join(pcap_root_path, temp_pcap_name)
            # 写文件pcap
            wrpcap(temp_pcap_name_path, new_pkts_list_sum)
            # 流量包回放
            tcpreplay_cmd = "tcpreplay -i {} {}".format(intf, temp_pcap_name_path)
            p = subprocess.Popen(tcpreplay_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
            output, error = p.communicate()
            result = output + error
            return result
        except Exception as e:
            return f"Exception: {e}"
        finally:
            if os.path.exists(temp_pcap_name_path):
                os.remove(temp_pcap_name_path)

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "gre",
            "type": "gre_over_gre",
            "pcap_name": "gre_over_gre"
        }
    }
    traffic_data = test_data["traffic"]
    gre_over_gre_player = GreOverGrePlayer()
    gre_over_gre_player.send_gre_over_gre_traffic(traffic_data, "ui", False)