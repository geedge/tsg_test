import configparser
import os
import sys
import time
from datetime import datetime
from support.ui_utils.workpath import workdir
import socket
from selenium.webdriver.common.by import By
from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.random_name import *

class AuditLogCheck():

    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir,"configuration_file.ini")
        self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        self.object_type = {
            "ip":"IP Address Object",
            "ip_learning":"IP Address Object"
        }


    def audit_log_check(self,object_info,object_element_position,first_row_checkbox_element):
        try:
            edit_element_position = object_element_position["edit"]
            #点击进入object详情页
            first_row_checkbox_element.click()
            edit_button_position = edit_element_position["objectListPage_editButton_posId"]
            self.driver.find_element(By.ID, edit_button_position).click()
            #校验object详情页audit log记录
            # 点击audit Logs
            self.driver.find_element(By.XPATH, main_button_audit_button_posXpath).click()
            if object_info["operation"] == 'Create':
                assert len(self.driver.find_elements(By.XPATH,"//div[@class='el-table__body-wrapper is-scrolling-none']//tbody/tr")) == 1
            elif object_info["operation"] == 'Edit':
                assert len(self.driver.find_elements(By.XPATH,"//div[@class='el-table__body-wrapper is-scrolling-none']//tbody/tr")) == 2
            self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath).click()  # 勾选第一行log CheckBox
            self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath).click()  # 点击compare 按钮
            source_ip = self.loginout_parse.get("selenium_server", "url").replace("http://", "").split(":")[0]  # 获取字符串http://192.168.39.77:4444地址中的ip
            if source_ip == 'localhost':
                source_ip = str(socket.gethostbyname(socket.gethostname()))
            assert self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_version_posXpath).text != "", "断言版本不为空"
            assert self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_id_posXpath).text == object_info["id"]
            # 页面获取元素文本
            operation_text = self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath).text
            type_text = self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_type_posXpath).text
            source_ip_text = self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_ip_posXpath).text
            time_text = self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_time_posXpath).text
            user_text = self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_user_posXpath).text
            assert operation_text == object_info["operation"], "校验失败！预期：{}，页面实际：{}".format(object_info["operation"], operation_text)
            assert type_text == self.object_type[object_info["sub_type"]], "校验失败！预期：{}，页面实际：{}".format(self.object_type[object_info["sub_type"]], type_text)
            assert source_ip_text == source_ip, "校验失败！预期：{}，页面实际：{}".format(source_ip, source_ip_text)
            assert time_text != "", "校验失败！页面实际：{}".format(time_text)
            user_name = self.loginout_parse.get("account", "username")
            assert user_name in user_text, "校验失败！预期：{}，页面实际：{}".format(user_name, user_text)
            if object_info["operation"] == "Edit":
                self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_cancel_posXpath).click()
                self.driver.find_element(By.XPATH, main_button_audit_button_posXpath).click()
                self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath).click()
                self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath).click()
                self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath).click()  # 点击compare 按钮
                assert (self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_id_posXpath + "[1]").text
                        == self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_id_posXpath + "[2]").text)
                assert (self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_type_posXpath + "[1]").text
                        == self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_type_posXpath + "[2]").text)
                assert (self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_ip_posXpath + "[1]").text
                        == self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_ip_posXpath + "[2]").text)
                assert (self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_user_posXpath + "[1]").text
                        == self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_user_posXpath + "[2]").text)
                assert self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath + "[1]").text == "Create"
                assert self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath + "[2]").text == "Edit"

            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400


