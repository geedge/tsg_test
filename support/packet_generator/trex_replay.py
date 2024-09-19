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
from overwrite_yaml import OverwriteYaml
from read_pcap import ReadPcap

# trex_workpath = "/opt/trex/v3.03"        # trex安装目录
# traffic_playback_workpath = "/opt/tsg_policy_api/traffic_replay"
# traffic_pcap = "traffic_pcap"

class TrafficReplay:
    def __init__(self, path_dict):
        """
        :param path_dict: 路径dict，里面包含项目路径和trex的路径
        """
        self.path_dict = path_dict
        self.traffic_trex_workpath = path_dict["trex_workpath"]
        self.traffic_playback_workpath = path_dict["traffic_playback_workpath"]
        self.pcap_yaml_path = os.path.join(self.traffic_playback_workpath, "traffic_pcap")

    def trex_playback(self, yaml_name, pcap_name, active_flows=0, m=1, d=1, clients_start="10.50.36.1", clients_end="10.50.36.1", servers_start="10.50.66.1", servers_end="10.50.66.1"):
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
        overwrite_yaml = OverwriteYaml(self.path_dict)
        overwrite_yaml.replace_from_yaml(yaml_name, pcap_name, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
        # cd /opt/trex/v3.03/ && /opt/trex/v3.03/t-rex-64 -f /opt/trex/v3.03/cap2_my/http_50.yaml -m 1 -d 100
        # 重组trex执行命令
        if active_flows == 0:
            template_trex_command = "cd {trex_workpath} && {trex_workpath}/t-rex-64 -f {yaml_abs_path} -m {m} -d {d}"
        elif active_flows > 0:
            template_trex_command = "cd {trex_workpath} && {trex_workpath}/t-rex-64 -f {yaml_abs_path} --active-flows {active_flows} -d {d}"
        self.yaml_abs_path = os.path.join(self.pcap_yaml_path, yaml_name)
        trex_command = template_trex_command.format(trex_workpath=self.traffic_trex_workpath, yaml_abs_path=self.yaml_abs_path, m=m, d=d)
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
                # if line_row_num <= 25:    # 输入前20行内容
                #     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], stdout_line)
                line_row_num += 1
                if stdout_flag == 0:    # 不输出时需要判断
                    if "normal" in stdout_line:
                        stdout_flag = 1
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "\n", stdout_line)
                else:   # 需要打印
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], stdout_line)
                    if "Open-flows" in stdout_line:
                        open_flows_ori = stdout_line
                        match_flows = re.search(r"Open-flows\s*:\s*(\d+)", open_flows_ori)
                        open_flows = int(match_flows.group(1))

        p.wait()
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The statistics of a single session are as follows: ", flush=True)
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], pcap_info_dict, flush=True)
        # sum_count = m * d
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Replay packet {sum_count} time, replay cps: {m}, replay duration: {d}. The expected statistical results are as follows: ", flush=True)
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Actual replay packet {open_flows} time", flush=True)
        metric_info_dict = {key:(value*open_flows) for key, value in pcap_info_dict.items()}
        metric_info_dict["session"] = open_flows
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], metric_info_dict, flush=True)
        return metric_info_dict

if __name__ == '__main__':
    clients_start = "10.64.7.16"
    clients_end = "10.64.7.16"
    servers_start = "10.64.7.16"
    servers_end = "10.64.7.16"
    servers_end = servers_start
    clients_end = clients_start
    # servers_start = "123.151.49.188"
    # servers_end = "123.151.49.188"
    active_flows = 11
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
    metric_info_dict = tp.trex_playback(yaml_name, pcap_name, active_flows=active_flows, m=m, d=d, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
