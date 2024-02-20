#!/usr/bin/python3
# coding=utf-8
from scapy.all import *
from scapy.layers.inet import IP
import os
import subprocess
import sys
import time
import re
import yaml
import select


# trex_workpath = "/opt/trex/v3.03"        # trex安装目录
# traffic_playback_workpath = "/opt/tsg_policy_api/traffic_replay"
# traffic_pcap = "traffic_pcap"

class TrafficReplay():
    def __init__(self, path_dict):
        """
        :param path_dict: 路径dict，里面包含项目路径和trex的路径
        """
        self.path_dict = path_dict
        self.traffic_trex_workpath = path_dict["trex_workpath"]
        self.traffic_playback_workpath = path_dict["traffic_playback_workpath"]
        self.pcap_yaml_path = os.path.join(self.traffic_playback_workpath, "traffic_pcap")

    def trex_playback(self, yaml_name, pcap_name, m=1, d=1,
                      clients_start="10.50.36.1", clients_end="10.50.36.1", servers_start="10.50.66.1", servers_end="10.50.66.1"):
        """
        :param yaml_name:  yaml文件名称
        :param pcap_name:  数据包文件名称
        :param m:   trex命令的-m参数3
        :param d:  trex命令的-d时间w3
        :return:
        """
        # 获取pcap数据包信息
        rd_http = ReadPcap(self.path_dict)
        pcap_info_dict = rd_http.get_info(pcap_name)
        # 更具传入的pcap_name，修改yanl文件内容
        rwya = RWyaml(self.path_dict)
        rwya.replace_from_yaml(yaml_name, pcap_name, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
        # cd /opt/trex/v3.03/ && /opt/trex/v3.03/t-rex-64 -f /opt/trex/v3.03/cap2_my/http_50.yaml -m 1 -d 100
        # 重组trex执行命令
        template_trex_command = "cd {trex_workpath} && {trex_workpath}/t-rex-64 -f {yaml_abs_path} -m {m} -d {d}"
        self.yaml_abs_path = os.path.join(self.pcap_yaml_path, yaml_name)
        trex_command = template_trex_command.format(trex_workpath=self.traffic_trex_workpath, yaml_abs_path=self.yaml_abs_path, m=m, d=d)
        print(trex_command)
        # 执行trex命令
        p = subprocess.Popen(trex_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout_flag = 0  # 0表示不输出
        open_flows = 0
        line_row_num = 0

        while p.poll() is None:    #实时打印输入
            stdout_line = p.stdout.readline()
            if not stdout_line.isspace():
                stdout_line = stdout_line.rstrip()
                # 只输出最终结果数据
                if line_row_num <= 25:    # 输入前20行内容
                    print(stdout_line)
                line_row_num += 1
                if stdout_flag == 0:    # 不输出时需要判断
                    if "normal" in stdout_line:
                        stdout_flag = 1
                        print("\n", stdout_line)
                else:   # 需要打印
                    print(stdout_line)
                    if "Open-flows" in stdout_line:
                        open_flows_ori = stdout_line
                        match_flows = re.search(r"Open-flows\s*:\s*(\d+)", open_flows_ori)
                        open_flows = int(match_flows.group(1))

        p.wait()
        print("单个session统计如下：")
        print(pcap_info_dict)
        sum_count = m * d
        print(f"数据包预期回放{sum_count}次，回放cps：{m}，回放持续时间为：{d}。预期统计结果如下：")
        print(f"数据包实际回放{open_flows}次。")
        metric_info_dict = {key:(value*open_flows) for key, value in pcap_info_dict.items()}
        print(metric_info_dict)
        return metric_info_dict

class ReadPcap():
    def __init__(self, path_dict):
        self.traffic_playback_workpath = path_dict["traffic_playback_workpath"]
        self.pcap_path = os.path.join(self.traffic_playback_workpath, "traffic_pcap")

    def get_info(self, file_name):
        """
        获取数据包 包数、字节数统计信息
        :param file_name:
        :return:
        """
        # 字节和包数统计变量
        pcap_info_dict = {
            "total_packets" : 0,
            "total_packets_sent": 0,
            "total_packets_received": 0,
            "total_bytes": 0,
            "total_bytes_sent": 0,
            "total_bytes_received": 0,
            "total_syn_pkt": 1
        }
        file_abspath = os.path.join(self.pcap_path, file_name)
        packets = rdpcap(file_abspath)
        # 定义第一个包方向
        src_ip = packets[0]["IP"].src
        dst_ip = packets[0]["IP"].dst
        # 计算包数和字节数
        for pkt in packets:
            ip_layer: IP = pkt["IP"]
            pkt_length = len(pkt)
            if pkt_length < 60:  # 数据包长度小于60，按60计算
                pkt_length = 60
            # 根据方向判断字节数和包数
            if ip_layer.src == src_ip:
                pcap_info_dict["total_packets"] += 1
                pcap_info_dict["total_packets_sent"] += 1
                pcap_info_dict["total_bytes"] += pkt_length
                pcap_info_dict["total_bytes_sent"] += pkt_length
            else:
                pcap_info_dict["total_packets"] += 1
                pcap_info_dict["total_packets_received"] += 1
                pcap_info_dict["total_bytes"] += pkt_length
                pcap_info_dict["total_bytes_received"] += pkt_length
        print(pcap_info_dict)
        return pcap_info_dict

class RWyaml():
    def __init__(self, path_dict):
        self.traffic_playback_workpath = path_dict["traffic_playback_workpath"]
        self.data_path = os.path.join(self.traffic_playback_workpath, "traffic_pcap")

    def replace_from_yaml(self, yaml_name, pcap_name, clients_start="10.50.36.1", clients_end="10.50.36.1", servers_start="10.50.66.1", servers_end="10.50.66.1"):
        # 组织yaml路径、pcap路径
        yaml_abs_path = os.path.join(self.data_path, yaml_name)
        pcap_abs_path = os.path.join(self.data_path, pcap_name)
        #print(yaml_abs_path, pcap_abs_path)
        with open(yaml_abs_path, "r", encoding="utf-8") as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        # 修改pcap文件路径
        result[0]["cap_info"][0]["name"] = pcap_abs_path
        result[0]["generator"]["clients_start"] = clients_start
        result[0]["generator"]["clients_end"] = clients_end
        result[0]["generator"]["servers_start"] = servers_start
        result[0]["generator"]["servers_end"] = servers_end
        # 修改后重写数据
        with open(yaml_abs_path, "w", encoding="utf-8") as f:
            yaml.dump(result, f)
        print(result)

if __name__ == '__main__':
    clients_start = "10.64.7.16"
    clients_end = "10.64.7.16"
    servers_start = "10.64.7.16"
    servers_end = "10.64.7.16"
    servers_end = servers_start
    clients_end = clients_start
    # servers_start = "123.151.49.188"
    # servers_end = "123.151.49.188"
    m = 100
    d = 1
    yaml_name = "http_50.yaml"
    pcap_name = "http_get_347pkts.pcap"
    #pcap_name = "http_87pkts.pcap"

    # trex_workpath = "/opt/trex/v3.03"        # trex安装目录
    # traffic_playback_workpath = "/opt/tsg_policy_api/traffic_replay"
    path_dict = {
        "trex_workpath": "/opt/trex/v3.03",
        "traffic_playback_workpath": "/opt/tsg_policy_api/traffic_replay"
    }

    tp = TrafficReplay(path_dict)
    metric_info_dict = tp.trex_playback(yaml_name, pcap_name, m=m, d=d, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
