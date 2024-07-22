# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
from ftplib import FTP

class FtpPlayer():
    def send_ftp_traffic(self, command, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send ftp traffic for effect verification.", flush=True)
        # command = "curl -kv --connect-timeout {} -m {} {}".format(command_dict["connect_timeout"], command_dict["timeout"], command_dict["url"])
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = p.communicate()
        cmd_result = output + error
        return cmd_result
    
    def ftp_connect(host, user, password):
        ftp = FTP(host)
        ftp.login(user, password)
        return ftp
    
    def list_directory(ftp, path='.'):
        """列出FTP服务器上的目录内容"""
        ftp.cwd(path)  # 切换到指定目录
        print(f"Listing directory {path}:")
        ftp.retrlines('LIST')
    
    def upload_file(ftp, local_file, remote_file):
        """上传文件到FTP服务器"""
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        print(f"File {local_file} uploaded successfully as {remote_file}")  
    
    def download_file(ftp, remote_file, local_file):
        """从FTP服务器下载文件"""
        with open(local_file, 'wb') as f:
            ftp.retrbinary(f'RETR {remote_file}', f.write)
        print(f"File {remote_file} downloaded successfully as {local_file}")
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
