# -*- coding: UTF-8 -*-
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime 
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.map_element_position_library import *
from support.ui_utils.policies.page_jump import PageJump

class DeleteRules:
    def __init__(self, driver):
        self.driver = driver
        
    def delete_rules(self, rule_uuids_tuple):
        try:
            time.sleep(0.3)
            rule_uuids_linst = list(rule_uuids_tuple)
            for i in range(len(rule_uuids_linst)):
                element_position_library = get_element_position(rule_uuids_linst[i]["type"])
                search_element_position = element_position_library["search"]
                deletion_element_position = element_position_library["delete"]
                page_jump_element_position = element_position_library["page_jump"]
                page_jump = PageJump(self.driver)
                page_jump.jump_sub_policy_page(page_jump_element_position)
                btn = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_posXpath"])
                self.driver.execute_script("arguments[0].click()", btn)
                self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_input_itemContent_posXpath"]).send_keys(rule_uuids_linst[i]["uuid"])
                dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLabel_dropDown_item_posXpath"].format(replaceValue="UUID")
                btn = self.driver.find_element(By.XPATH, dropdown_item_posXpath)
                self.driver.execute_script("arguments[0].click()", btn)
                self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_searchButton_posId"]).click()
                time.sleep(0.3)
                element_tr = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_tableTbody_posXpath"])
                row = element_tr.find_elements(By.XPATH, "div")
                if len(row) != 0:
                    first_row = row[0]
                    first_row_checkbox_element = first_row.find_element(By.XPATH, '//*[@inputprops="[object Object]"]')
                    first_row_checkbox_element.click()
                    time.sleep(0.3)
                    self.driver.find_element(By.XPATH, deletion_element_position["policyRuleListPage_deleteButton_posXpath"]).click()
                    self.driver.find_element(By.XPATH, deletion_element_position["policyRuleListPage_okButton_warningYes_posXpath"]).click()
                    time.sleep(2)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting rule, the exception error: ", str(e), flush=True)
            # raise
            return 400