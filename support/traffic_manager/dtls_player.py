# -*- coding: utf-8 -*-
import os
import ssl
import configparser
from socket import socket, AF_INET, SOCK_DGRAM
from dtls import do_patch
from support.traffic_manager.workpath import workdir
from datetime import datetime

class DtlsPlayer():
    def send_dtls_traffic():
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send dlts traffic for effect verification.", flush=True)
        parse = configparser.ConfigParser()
        parse_dir = os.path.join(workdir, "configuration_file.ini")
        parse.read(parse_dir, encoding="utf-8")
        client_ip = parse.get("dtls", "client_ip")
        server_port = int(parse.get("dtls", "server_port"))
        do_patch()
        client_sock = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM))
        client_sock.connect((client_ip, server_port))
        client_sock.send('Hi there'.encode('utf-8'))

if __name__ == "__main__":
    print("test")
    dtls_player = DtlsPlayer()
    dtls_player.send_dtls_traffic()