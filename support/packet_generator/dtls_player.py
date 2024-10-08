# -*- coding: utf-8 -*-
import ctypes
import platform
from datetime import datetime
from ctypes import c_char_p

class DtlsPlayer:
    def send_dtls_traffic(self, ip, port):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send dtls traffic for effect verification.", flush=True)
        
        os_name = platform.system()
        if os_name == "Linux":
            lib = ctypes.CDLL("/app/support/packet_generator/dtls_client/dtls_client.so")
        elif os_name == "Windows":
            lib = ctypes.CDLL("D:/Document/Project-TSG/Code/git/dtls_client/dtls_client.dll")
        lib.SimulateDtlsClient.restype = c_char_p
        result = lib.SimulateDtlsClient()
        return result.decode('utf-8')
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    server_ip = "127.0.0.1"
    server_port = "4433"
    dtls_player = DtlsPlayer()
    dtls_player.send_dtls_traffic(server_ip, server_port)
