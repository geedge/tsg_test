# -*- coding: utf-8 -*-
import os
import ssl
import configparser
from socket import socket, AF_INET, SOCK_DGRAM
from dtls import do_patch
from support.traffic_manager.workpath import workdir
from datetime import datetime

class DtlsPlayer:
    def send_dtls_traffic(self):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send dlts traffic for effect verification.", flush=True)
        parse = configparser.ConfigParser()
        parse_dir = os.path.join(workdir, "configuration_file.ini")
        parse.read(parse_dir, encoding="utf-8")
        server_ip = parse.get("dtls", "server_ip")
        server_port = int(parse.get("dtls", "server_port"))
        do_patch()
        try:
            blocksize = 1024
            client_sock = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM), cert_reqs=ssl.CERT_NONE)
            client_sock.settimeout(5)
            client_sock.connect((server_ip, server_port))
            # client_sock.send('Hi there'.encode('utf-8'))
            # self.execute_action(client_sock, blocksize)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Error: {e}.", flush=True)
            return f"Error: {e}."
    
    def execute_action(self, client_sock, blocksize):
        try:
            while True:
                send_msg = input(">")
                cmd, filename = send_msg.split(" ")
                try:
                    client_sock.send(send_msg.encode())
                    if cmd == "ls":
                        # input ls <dir> to list files in dir.
                        data = client_sock.recv(blocksize)
                        print(data.decode())
                    else:
                        # input get <filename> to get files from dir.
                        filename = filename.split("/")[-1]
                        filedir = "./"+filename
                        with open(filedir,"wb") as fd :
                            while True:
                                data = client_sock.recv(blocksize)
                                if data.decode() == "Already Send":
                                    print("Already Receive.")
                                    break
                                fd.write(data)
                except Exception as e:
                    print("Can not receive Data.")
        except KeyboardInterrupt:
            client_sock.close()

if __name__ == "__main__":
    print("test")
    dtls_player = DtlsPlayer()
    dtls_player.send_dtls_traffic()