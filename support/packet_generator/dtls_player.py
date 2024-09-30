# -*- coding: utf-8 -*-
import ctypes
import platform
from datetime import datetime
from ctypes import c_long

class DtlsPlayer:
    def send_dtls_traffic(self, ip, port):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send dtls traffic for effect verification.", flush=True)
        
        os_name = platform.system()
        if os_name == "Linux":
            lib = ctypes.CDLL('/app/support/packet_generator/dtlsclient/dtlsclient.so')
        elif os_name == "Windows":
            lib = ctypes.CDLL('D:/Document/Project-TSG/Code/git/dtlsclient/dtlsclient.dll')
        # lib.SimulateDtlsClient.argtypes = [ctypes.c_long, ctypes.c_long]  
        # lib.SimulateDtlsClient.restype = ctypes.c_long
        result = lib.SimulateDtlsClient(ip, port)
        return result
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    server_ip = "127.0.0.1"
    server_port = "4433"
    dtls_player = DtlsPlayer()
    dtls_player.send_dtls_traffic(server_ip, server_port)
