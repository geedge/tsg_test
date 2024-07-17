# -*- coding: utf-8 -*-
# from scapy.all import *
from scapy.all import sniff, IP
from datetime import datetime
 
class CapturePacket():
    def __init__(self):
        self.packet_count_in = 0
        self.packet_count_out = 0
        self.packet_count_total = 0
        self.byte_count_in = 0
        self.byte_count_out = 0
        self.byte_count_total = 0
    
    def packet_callback(self, packet):
        if packet is None:
            return
        
        if packet.lastlayer is not None:
            self.source_ip
            self.packet_count_total += 1
            self.byte_count_total += len(packet)
            if packet[IP].src == self.source_ip:
                self.packet_count_out += 1
                self.byte_count_out += len(packet)

    def capture_packet(self, intf, filter, source_ip, timeout):
        self.source_ip = source_ip
        pkt = sniff(iface=intf, filter=filter, prn=capture.packet_callback, timeout=timeout)
        # wrpcap("/opt/test.pcap", pkt)
        self.packet_count_in = self.packet_count_total-self.packet_count_out
        self.byte_count_in = self.byte_count_total-self.byte_count_out
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Received Packets: {self.packet_count_in}, Received Bytes: {self.byte_count_in}", flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Sent Packets: {self.packet_count_out}, Sent Bytes: {self.byte_count_out}", flush=True)
        return self.packet_count_in, self.byte_count_in, self.packet_count_out, self.byte_count_out

if __name__ == '__main__':
    capture = CapturePacket()
    intf = "ens19"
    filter = "host 192.168.64.80 and not port 22 and not port 53"
    source_ip = "192.168.64.80"
    timeout = 10
    # source_ip = "192.168.38.119"
    # filter = "host 192.168.38.119"
    capture.capture_packet(intf, filter, source_ip, timeout)