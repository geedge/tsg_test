# -*- coding: utf-8 -*-
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
        p = subprocess.Popen(traffic_data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = p.communicate()
        result = output + error
        
        # mail_type = traffic_data["mail_type"]
        # mail_port = traffic_data["mail_port"]
        # sender = traffic_data["sender"]
        # password = traffic_data["password"]
        # receiver = traffic_data["receiver"]
        # subject = traffic_data["subject"]
        # body = traffic_data["body"]
        # attach = traffic_data["attach"]
        # msg = MIMEMultipart()
        # msg['From'] = Header(sender, 'utf-8')
        # msg['To'] = Header(receiver, 'utf-8')
        # msg['Subject'] = Header(subject, 'utf-8')
        # msg['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # # 邮件正文内容，MIMEText是纯文本
        # msg.attach(MIMEText(body, 'plain', 'utf-8'))
        # # 附件
        # with open(attach, "rb") as attachment:
        #     part = MIMEBase("application", "octet-stream")
        #     part.set_payload((attachment).read())
        #     encoders.encode_base64(part)
        #     part.add_header("Content-Disposition", f"attachment; filename= {attach}")
        # msg.attach(part)
        # try:
        #     if mail_type == "gmail":
        #         smtp_obj = smtplib.SMTP_SSL("smtp.gmail.com", mail_port)
        #     else:
        #         smtp_obj = smtplib.SMTP_SSL("192.168.40.206", mail_port)
        #     # 如果服务器不支持STARTTLS，需注释掉下面这行
        #     # smtp_obj.starttls()
        #     smtp_obj.login(sender, password)
        #     smtp_obj.sendmail(sender, receiver, msg.as_string())
        #     return "Email sent successfully"
        # except smtplib.SMTPException as e:
        #     return f"SMTPException: {e}"
        # finally:
        #     smtp_obj.quit()
            
        return result
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "mail",
            "type": "client", # client/curl
            "mail_type": "other", # gmail or other smtp
            "mail_port": 465, # gmail：465（用于SSL）、587（用于启动TLS）。smtp默认：25
            "sender": "hbn@163.com",
            "password": "111111",
            "receiver": "autotest@163.com",
            "subject": "aaa",
            "body": "123",
            "attach": "d:/test.txt"
        }
    }
    traffic_data = test_data["traffic"]
    mail_player = MailPlayer()
    mail_player.send_mail_traffic(traffic_data, "ui", False)
