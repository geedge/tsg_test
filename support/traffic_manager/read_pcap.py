import os
from scapy.all import *
from scapy.layers.inet import IP

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
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], pcap_info_dict)
        return pcap_info_dict