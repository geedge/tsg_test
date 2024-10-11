# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.policy.page_jump import PageJump

class SearchRule:
    def __init__(self, driver):
        self.driver = driver
        
    def search(self, type, name, rule_element_position, vsys_name=""):
        search_element_position = rule_element_position["search"]
        page_jump_element_position = rule_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        page_jump.jump_sub_policy_page(page_jump_element_position)
        # 点击search查询框
        btn = self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_posId"])
        self.driver.execute_script("arguments[0].click()", btn) 
        dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLable_dropDown_item_posXpath"].format(replaceValue="Name")
        btn = self.driver.find_element(By.XPATH, dropdown_item_posXpath)
        self.driver.execute_script("arguments[0].click()", btn)
        input_item_posXpath = search_element_position["policyRuleListPage_searchLable_input_itemContent_posXpath"].format(replaceValue="Name")
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)
        # 强制点击js方法
        btn = self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_searchButton_posId"])
        self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
        time.sleep(0.3)
        #self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_searchButton_posId"]).click()
        element_tr = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "tr")
        if len(row) != 0:
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
            return 200, first_row_checkBox_element
        else:
            return 400, ""

    def get_rule_id(self, type, name, rule_element_position, vsys_name=""):
        search_element_position = rule_element_position["search"]
        page_jump_element_position = rule_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        page_jump.jump_sub_policy_page(page_jump_element_position)
        # 强制点击search查询框
        btn = self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_posId"])
        self.driver.execute_script("arguments[0].click()", btn) 
        dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLable_dropDown_item_posXpath"].format(replaceValue="Name")
        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
        input_item_posXpath = search_element_position["policyRuleListPage_searchLable_input_itemContent_posXpath"].format(replaceValue="Name")
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)
        btn = self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_searchButton_posId"])
        self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
        time.sleep(1)
        if type == "security":
            rule_id = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            return 200, rule_id
        elif type == "service_chaining":
            rule_id = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault mouseSchedule el-popover__reference']//span").text
            return 200, rule_id
        elif type == "monitor":
            rule_id = self.driver.find_element(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            return 200, rule_id
        elif type == "pxy_intercept":
            rule_id = self.driver.find_elements(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span")[0].text.strip()
            return 200, rule_id
        elif type == "pxy_manipulation":
            rule_id = self.driver.find_elements(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span")[0].text.strip()
            return 200, rule_id
        elif type == "statistics":
            rule_id = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            return 200, rule_id
        elif type == "dos_protection":
            rule_id = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            return 200, rule_id
        else:
            return 400, ""