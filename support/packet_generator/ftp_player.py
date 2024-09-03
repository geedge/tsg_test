# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
from ftplib import FTP

class FtpPlayer:
    def send_ftp_traffic(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send ftp traffic for effect verification.", flush=True)
        if "command" in traffic_data["traffic"]:
            p = subprocess.Popen(traffic_data["traffic"]["command"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
            output, error = p.communicate()
            result = output + error
        elif "command" not in traffic_data["traffic"]:
            try:
                result = ""
                ftp_server = traffic_data["host"]
                user = traffic_data["user"]
                password = traffic_data["password"]
                action = traffic_data["action"]
                path = traffic_data["path"]
                if len(traffic_data["local_file"]) > 0:
                    local_file = traffic_data["local_file"]
                if len(traffic_data["remote_file"]) > 0:
                    remote_file = traffic_data["remote_file"]
                ftp = self.ftp_connect(ftp_server, user, password)
                if action == "list":
                    self.list_directory(ftp, path)
                elif action == "upload":
                    self.upload_file(ftp, local_file, remote_file)
                elif action == "download":
                    self.download_file(ftp, remote_file, local_file)
                result += "FTP traffic sent successfully"
            except Exception as e:
                result += f"Exception: {e}"
            finally:
                ftp.quit()
        return result
    
    def ftp_connect(self, host, user, password):
        ftp = FTP(host)
        ftp.login(user, password)
        return ftp
    
    def list_directory(self, ftp, path='.'):
        # 列出FTP服务器上的目录内容
        ftp.cwd(path)  # 切换到指定目录
        ftp.retrlines('LIST')
    
    def upload_file(self, ftp, local_file, remote_file):
        # 上传文件到FTP服务器
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        # print(f"File {local_file} uploaded successfully as {remote_file}")  
    
    def download_file(self, ftp, remote_file, local_file):
        # 从FTP服务器下载文件
        with open(local_file, 'wb') as f:
            ftp.retrbinary(f'RETR {remote_file}', f.write)
        # print(f"File {remote_file} downloaded successfully as {local_file}")
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "ftp",
            "type": "client", # client/curl
            "host": "192.168.40.206",
            "user": "ftpuser",
            "password": "111111",
            "action": "list", # "list", "upload" or "download"
            "path": "/autoFtp",
            "local_file": "test.py",
            "remote_file": "test.txt"
        }
    }
    traffic_data = test_data["traffic"]
    ftp_player = FtpPlayer()
    ftp_player.send_ftp_traffic(traffic_data, "ui", False)
