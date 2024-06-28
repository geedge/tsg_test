# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
import random
import time

class DeleteRule():
    def __init__(self, driver):
        self.driver = driver
        
    def delete(self, rule_element_position, first_row_checkbox_element, is_del_all):
        delete_element_position = rule_element_position["delete"]
        try:
            if is_del_all == True:
                time.sleep(1)
                self.driver.find_element(By.XPATH, delete_element_position["policyRuleListPage_allSelect_posXpath"]).click()
            else:
                time.sleep(1)
                first_row_checkbox_element.click()
            time.sleep(1)
            self.driver.find_element(By.ID, delete_element_position["policyRuleListPage_deleteButton_posId"]).click()
            self.driver.find_element(By.XPATH, delete_element_position["policyRuleListPage_okButton_warningYes_posXpath"]).click()
            time.sleep(3)
            return 200
        except Exception as e:
            print(e)
            return 400