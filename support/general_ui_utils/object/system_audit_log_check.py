import configparser
import os
import random
import time
from datetime import datetime

from selenium.webdriver import Keys
from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.workpath import workdir
from selenium.webdriver.common.by import By

class SystemAuditLogCheck():

    def __init__(self,driver):
        self.driver = driver
        self.loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir,"configuration_file.ini")
        self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        self.target_type = {
            "ip":"IP Address Object",
            "ip_learning":"IP Address Object"
        }

    def system_audit_log_check(self,test_data,object_info):
        try:
            user_name = self.loginout_parse.get("account", "username")
            self.driver.find_element(By.ID, mainPage_firstLevelMenu_System_posId).click()
            self.driver.find_element(By.ID, mainPage_secondLevelMenu_auditLogs_posId).click()
            time.sleep(3)
            self.driver.find_element(By.ID, mainPage_ObjectSearch_selectLabel_posId).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_select_TagrgetID_posXpath).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_targetid_text_posXpath).send_keys(object_info["id"] + Keys.ENTER)
            ###校验["Create", "Edit", "Delete", "Import", "Query Verbose"]
            # 选择Target Type
            self.driver.find_element(By.ID, mainPage_ObjectSearch_selectLabel_posId).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_select_TargetType_posXpath).click()
            scrollable_div = self.driver.find_element(By.XPATH,f"//div[@class='el-select-dropdown el-popper select-popper']//span[text()='{self.target_type[test_data['object_type']]}']")
            self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)
            scrollable_div.click()
            # 选择当前用户
            self.driver.find_element(By.ID, mainPage_ObjectSearch_selectLabel_posId).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_select_UserName_posXpath).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_username_text_posXpath).send_keys(user_name)
            time.sleep(2)
            element_user_name = self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{user_name}']")
            self.driver.execute_script("arguments[0].click()", element_user_name)  # 强制点击搜索出来的Name
            # 搜索
            self.driver.find_element(By.ID, mainPage_objectSearch_buttonSearch_posXpath).click()
            # 搜索结果校验
            assert len(self.driver.find_elements(By.XPATH,"//div[@class='el-table__body-wrapper is-scrolling-none']//span[text()='Create']")) == 1, "Create日记大于1"
            assert len(self.driver.find_elements(By.XPATH,"//div[@class='el-table__body-wrapper is-scrolling-none']//span[text()='Edit']")) == 1, "Edit日志大于1"
            assert len(self.driver.find_elements(By.XPATH,"//div[@class='el-table__body-wrapper is-scrolling-none']//span[text()='Delete']")) == 1, "Delete日志大于1"
            operation = ["Create", "Edit", "Delete", "Import", "Query Verbose"]
            operation_text = []
            operation_text_elements = self.driver.find_elements(By.XPATH,"(//table[@class='el-table__body'])[1]//tbody/tr/td[3]//span")
            for i in range(len(operation_text_elements)):
                text = self.driver.find_element(By.XPATH,f"((//table[@class='el-table__body'])[1]//tbody/tr/td[3]//span)[{i + 1}]").text
                operation_text.append(text)
            self.check_audit_log_detail("0")
            if set(operation_text) != set(operation):
                raise Exception("存在未记录日志")

            ###校验["Export","Query List"]
            # 清除筛选框
            search_clear_btn = self.driver.find_element(By.XPATH, '//*[@id="searchClear"]')
            self.driver.execute_script("arguments[0].scrollIntoView();", search_clear_btn)
            search_clear_btn.click()
            object_type = "Object"
            self.driver.find_element(By.ID, mainPage_ObjectSearch_selectLabel_posId).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_select_TargetType_posXpath).click()
            scrollable_div = self.driver.find_element(By.XPATH,f"//div[@class='el-select-dropdown el-popper select-popper']//span[text()='{object_type}']")
            self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)
            scrollable_div.click()
            # 选择当前用户
            self.driver.find_element(By.ID, mainPage_ObjectSearch_selectLabel_posId).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_select_UserName_posXpath).click()
            self.driver.find_element(By.XPATH, listPage_auditlogSearch_username_text_posXpath).send_keys(user_name)
            time.sleep(2)
            self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{user_name}']").click()
            # 搜索
            self.driver.find_element(By.ID, mainPage_objectSearch_buttonSearch_posXpath).click()

            time.sleep(7)
            operation_text_elements = self.driver.find_elements(By.XPATH,"(//table[@class='el-table__body'])[1]//tbody/tr/td[3]//span")
            other_operation_text = []
            other_operation = ["Export", "Query List"]
            for i in range(len(operation_text_elements)):
                text = self.driver.find_element(By.XPATH,f"((//table[@class='el-table__body'])[1]//tbody/tr/td[3]//span)[{i + 1}]").text
                other_operation_text.append(text)
            self.check_audit_log_detail("1")
            if set(other_operation_text) != set(other_operation):
                raise Exception("存在未记录日志")

            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",file=sys.stderr, flush=True)
            return 400




    def check_audit_log_detail(self,type):
        if type == "0":  # 首次对operation = ["Create", "Edit", "Delete", "Import", "Query Verbose"]的校验
            detaile_elements = self.driver.find_elements(By.XPATH,"//button[@id='test-compareHistorical-_system_PolicyConfigurationLog_Home_App_anonymousComponent']")
            for i in range(len(detaile_elements)):
                detaile_text = self.driver.find_element(By.XPATH,f"(//button[@id='test-compareHistorical-_system_PolicyConfigurationLog_Home_App_anonymousComponent'])[{i + 1}]").text
                self.driver.find_element(By.XPATH,f"(//button[@id='test-compareHistorical-_system_PolicyConfigurationLog_Home_App_anonymousComponent'])[{i + 1}]").click()
                if detaile_text == "Compare":
                    compare_verision = self.driver.find_elements(By.XPATH,"//div[@class='rm-content']//div[@class='el-table__body-wrapper is-scrolling-none']//tr[@class='el-table__row']")
                    assert len(compare_verision) != 0, "Compare存在修改信息"
                elif detaile_text == "View":
                    assert self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath).text != ""
                    assert self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_type_posXpath).text != ""
                    assert self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_ip_posXpath).text != ""
                    assert self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_time_posXpath).text != ""
                    assert self.driver.find_element(By.XPATH,ObjectDetailPage_audit_log_compare_user_posXpath).text != ""
                self.driver.find_element(By.ID,"interceptionadd_allcancelobject10-_AuditLogs_system_PolicyConfigurationLog_Home_App_anonymousComponent").click()
        elif type == "1":  # 对 other_operation = ["Export", "Query List"]的校验
            detaile_elements = self.driver.find_elements(By.XPATH,"//button[@id='test-compareHistorical-_system_PolicyConfigurationLog_Home_App_anonymousComponent']")
            detaile_index = random.randint(1, len(detaile_elements) + 1)
            self.driver.find_element(By.XPATH,f"(//button[@id='test-compareHistorical-_system_PolicyConfigurationLog_Home_App_anonymousComponent'])[{detaile_index}]").click()
            assert self.driver.find_element(By.XPATH,url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath).text != ""
            assert self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_type_posXpath).text != ""
            assert self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_ip_posXpath).text != ""
            assert self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_time_posXpath).text != ""
            assert self.driver.find_element(By.XPATH, ObjectDetailPage_audit_log_compare_user_posXpath).text != ""