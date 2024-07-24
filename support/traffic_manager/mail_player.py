# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders

class MailPlayer():
    def send_mail_traffic(self, traffic_data, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send mail traffic for effect verification.", flush=True)
        # command = "curl -kv --connect-timeout {} -m {} {}".format(command_dict["connect_timeout"], command_dict["timeout"], command_dict["url"])
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
        #     if mail_type == "gamail":
        #         smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', mail_port)
        #     else:
        #         smtpObj = smtplib.SMTP('smtp.example.com', mail_port)
        #     # 如果服务器不支持STARTTLS，需注释掉下面这行
        #     smtpObj.starttls()
        #     smtpObj.login(sender, password)
        #     smtpObj.sendmail(sender, [receiver], msg.as_string())
        #     return "Email sent successfully"
        # except smtplib.SMTPException as e:  
        #     return f"SMTPException: {e}"
        # finally:  
        #     smtpObj.quit()
            
        return result
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "mail",
            "mail_type": "gmail", # gmail or other smtp
            "mail_port": 587,
            "sender": "abc.com",
            "password": "123",
            "receiver": "def.com", 
            "subject": "aaa", 
            "body": "1111111",
            "attach": "test.txt"
        }
    }
    traffic_data = test_data["traffic"]
    mail = MailPlayer()
    mail.send_mail_traffic(traffic_data, "ui", False)
