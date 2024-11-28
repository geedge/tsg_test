# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
import time
import traceback
from datetime import datetime
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.policies.page_jump import PageJump
from support.ui_utils.element_position.map_element_position_library import *

class EditRules:
    def __init__(self, driver):
        self.driver = driver
        
    def edit_rules(self, policy_configuration):
        try:
            type = policy_configuration["type"]
            name = policy_configuration["name"]
            element_position_library = get_element_position(policy_configuration["type"])
            search_element_position = element_position_library["search"]
            page_jump_element_position = element_position_library["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_policy_page(page_jump_element_position)
            # 点击search查询框
            btn = self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_posId"])
            self.driver.execute_script("arguments[0].click()", btn)
            time.sleep(1) 
            dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLable_dropDown_item_posXpath"].format(replaceValue="Name")
            btn = self.driver.find_element(By.XPATH, dropdown_item_posXpath)
            self.driver.execute_script("arguments[0].click()", btn) 
            # self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
            input_item_posXpath = search_element_position["policyRuleListPage_searchLable_input_itemContent_posXpath"].format(replaceValue="Name")
            self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)
            btn = self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_searchButton_posId"])
            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
            time.sleep(0.5)
            if type == "security":
                rule_uuid = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault el-popover__reference']//span").text
                edit_button_position = "appEdit-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"
            elif type == "service_chaining":
                rule_uuid = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault mouseSchedule el-popover__reference']//span").text
                edit_button_position = "appEdit-_OperateBtns_ElRow_policy_ServiceChaining_Home_App_anonymousComponent"
            elif type == "monitor":
                rule_uuid = self.driver.find_element(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span").text
                edit_button_position ="appEdit-_OperateBtns_ElRow_policy_monitor_Home_App_anonymousComponent"
            elif type == "proxy_intercept":
                rule_uuid = self.driver.find_elements(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span")[0].text.strip()
                edit_button_position = "appEdit-_OperateBtns_ElRow_policy_Intercept_Home_App_anonymousComponent"
            elif type == "proxy_manipulation":
                rule_uuid = self.driver.find_elements(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span")[0].text.strip()
                edit_button_position = "appEdit-_OperateBtns_ElRow_policy_Manipulation_Home_App_anonymousComponent"
            elif type == "statistics":
                rule_uuid = self.driver.find_element(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span").text
                edit_button_position = "appEdit-_OperateBtns_ElRow_policy_statistics_Home_App_anonymousComponent"
            elif type == "dos_protection":
                rule_uuid = self.driver.find_element(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span").text
                edit_button_position = "appEdit-_OperateBtns_ElRow_policy_DoSProtection_Home_App_anonymousComponent"
            all_button_position = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
            all_selectBox_position = "//table//*[@class='el-checkbox']//span//span"
            self.driver.find_elements(By.XPATH, all_selectBox_position)[0].click()
            self.driver.find_element(By.ID, edit_button_position).click()
            return ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When editing rule, the exception error: ", str(e), flush=True)
            # raise
            return "When editing rule, the exception error: " + str(e)
