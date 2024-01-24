from reportlab.pdfbase import pdfmetrics  # 注册字体
from reportlab.pdfbase.ttfonts import TTFont  # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image, Table  # 报告内容相关类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.lib.units import cm  # 单位：cm
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String
from reportlab.platypus import SimpleDocTemplate, Paragraph
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import os
import pandas as pd

class GenerateReport():
    def generate_report(self, table_data, pie_data, pie_table_data, project_path):
        # pdfmetrics.registerFont(TTFont('simfang', 'simfang.ttf'))
        style_list = getSampleStyleSheet()
        pdf = list()
        pdf.append(self.insert_full_title(style_list, "API Automation Test Report"))
        pdf.append(self.insert_text(style_list, "API automation scripts are uesd to verify restful api interface and module function, like Security, Proxy, Statistics, and Service Chaining. In addition, when fixing some bugs or having emergency situation for release version, tester can execute the coverage and verification of basic functions quickly."))
        pdf.append(self.insert_text(style_list, "The general process is as follows: after configure a rule by API, the traffic that the test pc send hit this rule, verify the rule/function correctness by the return value and log or source test data."))
        pdf.append(self.insert_lettle_title(style_list, "Test result overview:"))
        report_folder_name = "report_" + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        os.mkdir(project_path + "/report/" + report_folder_name)
        report_folder_path = project_path + "/report/" + report_folder_name
        self.create_pie(pie_data, pie_table_data, report_folder_path)
        pdf.append(self.insert_image(report_folder_path + "/pie.png"))
        pdf.append(self.insert_lettle_title(style_list, "Test result detail:"))
        # 往PDF中写入大量数据较耗时（如10万条数据需要7-8分钟）且PDF不像Excel或CSV容易过滤信息和进行问题分析，所以单独生成一个毫秒级的CSV文件
        df = pd.DataFrame(table_data, columns=["", "", ""])
        df.to_csv(project_path + "/report/" + report_folder_name + "/report.csv")
        pdf.append(self.insert_table(table_data))
        report_path = project_path + "/report/" + report_folder_name + "/report.pdf"
        pdf_template = SimpleDocTemplate(report_path, pagesize=letter)
        pdf_template.build(pdf)
        
    def insert_full_title(self, style_list, title_name):
        font_ = style_list['Heading1']
        # font_.fontName = 'simfang'
        font_.fontSize = 20
        font_.leading = 50
        font_.textColor = colors.green
        font_.alignment = 1
        font_.bold = True
        return Paragraph(title_name, font_)
    
    def insert_text(self, style_list, text):
        font_ = style_list['Normal']
        # font_.fontName = 'simfang'
        font_.fontSize = 12
        font_.wordWrap = 'CJK'
        font_.alignment = 0
        font_.firstLineIndent = 32
        font_.leading = 25
        return Paragraph(text, font_)
    
    def create_pie(self, pie_data, pie_table_data, project_path):
        y = np.array(pie_data)
        plt.figure(figsize=(8, 4))
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] #指定字体为雅黑，解决文字乱码问题
        temp_list = []
        if pie_data[0] == 0 and pie_data[1] != 0 and pie_data[2] != 0:
            temp_list.append(pie_data[1])
            temp_list.append(pie_data[2])
            plt.pie(temp_list, labels=['Fail', 'Noexecuted'], autopct="(%1.1f%%)", colors=("r", "blue"), explode=[0, 0])
        elif pie_data[1] == 0 and pie_data[0] != 0 and pie_data[2] != 0:
            temp_list.append(pie_data[0])
            temp_list.append(pie_data[2])
            plt.pie(temp_list, labels=['Pass', 'Noexecuted'], autopct="(%1.1f%%)", colors=("#88c999", "blue"), explode=[0, 0])
        elif pie_data[2] == 0 and pie_data[0] != 0 and pie_data[1] != 0:
            temp_list.append(pie_data[0])
            temp_list.append(pie_data[1])
            plt.pie(temp_list, labels=['Pass', 'Fail'], autopct="(%1.1f%%)", colors=("#88c999", "r"), explode=[0, 0])
        elif pie_data[0] == 0 and pie_data[1] == 0 and pie_data[2] != 0:
            temp_list.append(pie_data[2])
            plt.pie(temp_list, labels=['Noexecuted'], autopct="(%1.1f%%)", colors=("blue"), explode=[0])
        elif pie_data[0] == 0 and pie_data[2] == 0 and pie_data[1] != 0:
            temp_list.append(pie_data[1])
            plt.pie(temp_list, labels=['Fail'], autopct="(%1.1f%%)", colors=("r"), explode=[0])
        elif pie_data[1] == 0 and pie_data[2] == 0 and pie_data[0] != 0:
            temp_list.append(pie_data[0])
            plt.pie(temp_list, labels=['Pass'], autopct="(%1.1f%%)", colors=("#88c999"), explode=[0])
        else:
            plt.pie(y, labels=['Pass', 'Fail', 'Noexecuted'], autopct="(%1.1f%%)", colors=("#88c999", "r", "blue"), explode=[0, 0, 0])
        plt.legend(loc='upper right')
        plt.table(cellText=pie_table_data, cellLoc='center', colLabels=['Total test cases', 'Passed test cases', 'Failed test cases', 'Noexecuted test cases'], colColours=['#d5dae6', '#d5dae6', '#d5dae6', '#d5dae6'], colLoc='center', loc='bottom')
        plt.axis('equal')
        plt.savefig(project_path + "/pie.png")
    
    def insert_image(self, image_path):
        img = Image(image_path)
        img.drawWidth = 20 * cm
        img.drawHeight = 10 * cm
        return img
    
    def insert_lettle_title(self, style_list, lettle_name):
        font_ = style_list['Normal']
        # font_.fontName = 'simfang'
        font_.fontSize = 15
        font_.leading = 30
        font_.textColor = colors.black
        return Paragraph(lettle_name, font_)
    
    def insert_table(self, args):
        # col_width = 120
        col_width = [200, 50, 200]
        style = [
            # ('FONTNAME', (0, 0), (-1, -1), 'simfang'),  # 字体
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # 第一行的字体大小
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # 第二行到最后一行的字体大小
            ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),  # 设置第一行背景颜色
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 第一行水平居中
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # 第二行到最后一行左右左对齐
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有表格上下居中对齐
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkslategray),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 设置表格框线为grey色，线宽为0.5
        ]
        table = Table(args, colWidths=col_width, style=style)
        table.autofit = True
        return table
        
if __name__ == '__main__':
    table_data = [
        ["Name", "Result", "Failure Reason"]
    ]
    i = 1
    while i <= 10:
        case_name = "shunt_ip_flag_app-allow_ip_flag_app_" + str(i)
        result_data = ["", "Pass", "The verification results of policy effect and logs are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs."]
        result_data[0] = case_name
        table_data.append(result_data)
        i += 1
    pie_data = [0, 0, 70]
    pie_table_data = [
        [100, 80, 20, 0]
    ]
    path = "D:/Document/Project-TSG/Code/git/tsg_policy_api"
    report = GenerateReport()
    report.generate_report(table_data, pie_data, pie_table_data, path)