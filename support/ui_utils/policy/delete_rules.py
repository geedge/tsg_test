# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
import random
import time
from datetime import datetime 

class DeleteRules:
    def __init__(self, driver):
        self.driver = driver
        
    def delete_rules(self, rule_element_position, first_row_checkbox_element, is_del_all):
        delete_element_position = rule_element_position["delete"]
        try:
            time.sleep(0.3)
            if is_del_all == True:
                self.driver.find_element(By.XPATH, delete_element_position["policyRuleListPage_allSelect_posXpath"]).click()
            else:
                first_row_checkbox_element.click()
            time.sleep(0.3)
            self.driver.find_element(By.XPATH, delete_element_position["policyRuleListPage_deleteButton_posXpath"]).click()
            self.driver.find_element(By.XPATH, delete_element_position["policyRuleListPage_okButton_warningYes_posXpath"]).click()
            time.sleep(2)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            #return 400