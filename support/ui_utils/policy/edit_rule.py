# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.policy.page_jump import PageJump

class EditRule():
    def __init__(self, driver):
        self.driver = driver
        
    def edit(self, type, name, rule_element_position, vsys_name=""):
        try:
            search_element_position = rule_element_position["search"]
            page_jump_element_position = rule_element_position["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_policy_page(page_jump_element_position)
            # 点击search查询框
            self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_posId"]).click()
            dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLable_dropDown_item_posXpath"].format(replaceValue="Name")
            self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
            input_item_posXpath = search_element_position["policyRuleListPage_searchLable_input_itemContent_posXpath"].format(replaceValue="Name")
            self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)
            self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_searchButton_posId"]).click()
            time.sleep(1)
            rule_id = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            all_button_position = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
            self.driver.find_element(By.XPATH, all_button_position).click()
            edit_button_position = "appEdit-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"
            self.driver.find_element(By.ID, edit_button_position).click()
            return 200, rule_id
        except Exception as e:
            print(e)
            return 400, None
