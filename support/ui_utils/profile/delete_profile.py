import random
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.object_element_position import *

class DeleteProfile():
    def __init__(self, driver):
        self.driver = driver
        
    def delete(self, profile_element_position, first_row_checkbox_element, is_del_all):
        delete_element_position = profile_element_position["delete"]
        try:
            if is_del_all == True:
                self.driver.find_element(By.XPATH, delete_element_position["profileListPage_allSelect_posXpath"]).click()
            else:
                first_row_checkbox_element.click()
            self.driver.find_element(By.ID, delete_element_position["profileListPage_deleteButton_posId"]).click()
            self.driver.find_element(By.XPATH, delete_element_position["profileListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(0.5)
            return 200
        except Exception as e:
            print(e)
            return 400