# -*- coding: utf-8 -*-
import os
import ssl
import configparser
from socket import socket, AF_INET, SOCK_DGRAM
from dtls import do_patch
from support.traffic_manager.workpath import workdir

class DtlsServer:
    def recv_dtls_traffic(self):
        parse = configparser.ConfigParser()
        parse_dir = os.path.join(workdir, "configuration_file.ini")
        parse.read(parse_dir, encoding="utf-8")
        server_ip = parse.get("dtls", "server_ip")
        server_port = int(parse.get("dtls", "server_port"))
        do_patch()
        server_sock = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM))
        server_sock.bind((server_ip, server_port))
        while True:
            data, addr = server_sock.recvfrom(1024)
            # print(f"Received data from {addr}: {data}")

if __name__ == "__main__":
    print("test")
    dtls_server = DtlsServer()
    dtls_server.recv_dtls_traffic()
