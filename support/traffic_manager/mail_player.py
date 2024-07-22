# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.header import Header 

class MailPlayer():
    def send_mail_traffic(self, command, script_type, debug_flag):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send mail traffic for effect verification.", flush=True)
        # command = "curl -kv --connect-timeout {} -m {} {}".format(command_dict["connect_timeout"], command_dict["timeout"], command_dict["url"])
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = p.communicate()
        cmd_result = output + error
        return cmd_result
    
    def send_email(sender, password, receiver, subject, body):  
        # 创建一个带附件的 email 消息实例，MIMEText 是纯文本
        msg = MIMEMultipart()
        msg['From'] = Header(sender, 'utf-8')
        msg['To'] = Header(receiver, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        # 邮件正文内容
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        try:
            # 连接到邮件服务器
            smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # 对于Gmail
            # smtpObj = smtplib.SMTP('smtp.example.com', 587)  # 其他SMTP服务器和端口
            # smtpObj.starttls()  # 如果服务器支持STARTTLS，则取消注释
            # 登录到服务器  
            smtpObj.login(sender, password)
            # 发送邮件
            smtpObj.sendmail(sender, [receiver], msg.as_string())
            return "Email sent successfully"
        except smtplib.SMTPException as e:  
            return f"SMTPException: {e}"
        finally:  
            smtpObj.quit()
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
