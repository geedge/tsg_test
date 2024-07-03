# -*- coding: UTF-8 -*-
import subprocess

def update_tsg_ca():
    try:
        tsg_ca_file = 'tsg_ca.txt'
        subprocess.check_call(["chmod", "777", "/etc/pki/tls/certs/ca-bundle.crt"])
        with open('/etc/pki/tls/certs/ca-bundle.crt', 'r', encoding='utf-8') as file:
            content = file.read()
        if "TSG CA" not in content:
            # 读取证书文件内容
            with open(tsg_ca_file, 'r', encoding='utf-8') as cert_file:
                cert_content = cert_file.read()
            # 将证书内容追加到ca-bundle.crt文件中
            with open('/etc/pki/tls/certs/ca-bundle.crt', 'a', encoding='utf-8') as ca_bundle:
                ca_bundle.write(cert_content)
                ca_bundle.write('\n')
            # 更新证书信任库
            # subprocess.run(['sudo', 'update-ca-trust', 'extract'])
            print("Update TSG CA successfully.")
        else:
            print("TSG CA was found in ca-bundle.crt, so no content was appended.")
    except:
        print("Fail to update TSG CA.")
        
if __name__ == '__main__':
    update_tsg_ca()