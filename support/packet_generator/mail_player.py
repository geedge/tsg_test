# -*- coding: utf-8 -*-
import json
import subprocess
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders

class MailPlayer:
    def send_mail_traffic(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send mail traffic for effect verification.", flush=True)
        if "command" in traffic_data:
            p = subprocess.Popen(traffic_data["command"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
            output, error = p.communicate()
            result = output + error
            return result
        elif "command" not in traffic_data:
            try:
                mail_type = traffic_data["mail_type"]
                mail_server = traffic_data["mail_server"]
                mail_port = traffic_data["mail_port"]
                mail_timeout = traffic_data["mail_timeout"]
                sender = traffic_data["sender"]
                password = traffic_data["password"]
                receiver = traffic_data["receiver"]
                subject = traffic_data["subject"]
                body = traffic_data["body"]
                attach = traffic_data["attach"]
                msg = MIMEMultipart()
                msg['From'] = Header(sender, 'utf-8')
                msg['To'] = Header(receiver, 'utf-8')
                msg['Subject'] = Header(subject, 'utf-8')
                msg['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 邮件正文内容，MIMEText是纯文本
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
                # 附件
                with open(attach, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename= {attach}")
                msg.attach(part)
                server_code = 0
                server_resp = "None"
                if mail_type == "gmail":
                    smtp_obj = smtplib.SMTP_SSL(mail_server, mail_port, timeout=mail_timeout)
                elif mail_type == "smtp_ssl":
                    smtp_obj = smtplib.SMTP_SSL(mail_server, mail_port, timeout=mail_timeout)
                elif mail_type == "smtp":
                    smtp_obj = smtplib.SMTP(mail_server, mail_port, timeout=mail_timeout)
                # 如果服务器不支持STARTTLS，需注释掉下面这行
                # smtp_obj.starttls()
                # 设置debuglevel，会实时打印信息
                # smtp_obj.set_debuglevel(1)
                smtp_obj.login(sender, password)
                smtp_obj.sendmail(sender, receiver, msg.as_string())
                return "Email sent successfully"
            except (Exception, smtplib.SMTPException) as e:
                if isinstance(smtp_obj.ehlo_resp, bytes):
                    server_resp = smtp_obj.ehlo_resp.decode("utf-8")
                    if "Mail was identified as spam" in server_resp:
                        server_code = 550
                    elif "User not local; please try" in server_resp:
                        server_code = 551
                return f"smpt_exception: {e}, server_code: {server_code}, server_resp: {server_resp}"
            finally:
                if server_code != 0 and server_code != 550 and server_code != 551:
                    smtp_obj.quit()
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "mail",
            "type": "client", # client/curl
            "mail_type": "smtp", # gmail or smtp or smtp_ssl
            "mail_server": "192.168.40.206", # gmail: smtp.gmail.com
            "mail_port": 25, # gmail：465（用于SSL）、587（用于启动TLS）。smtp默认：25
            "mail_timeout": 20,
            "sender": "hbn@163.com",
            "password": "111111",
            "receiver": "autotest@163.com",
            "subject": "aaa",
            "body": "123",
            "attach": "/opt/test.txt"
        }
        # "traffic": {
        #     "protocol": "mail",
        #     "type": "curl",
        #     "command": "curl -kv --connect-timeout 25 -m 25 --url 'smtp://192.168.40.206' --mail-from 'hbn@163.com'  --mail-rcpt 'autotest@163.com'  --upload-file '/opt/test.txt' --user 'hbn@163.com:111111'"
        # }
    }
    traffic_data = test_data["traffic"]
    mail_player = MailPlayer()
    mail_player.send_mail_traffic(traffic_data, "ui", False)
