import random
import time
from selenium.webdriver.common.by import By
from element_position.objectElementPosition import *

class DeleteObject():
    def __init__(self, driver):
        self.driver = driver
        
    def delete(self, object_element_position, first_row_checkbox_element, is_del_all):
        delete_element_position = object_element_position["delete"]
        try:
            if is_del_all == True:
                self.driver.find_element(By.XPATH, delete_element_position["objectListPage_allSelect_posXpath"]).click()
            else:
                first_row_checkbox_element.click()
            self.driver.find_element(By.ID, delete_element_position["objectListPage_deleteButton_posId"]).click()
            random_yes_or_no = random.randint(0, 1)
            if random_yes_or_no == 0:  # 点击yes，删除
                self.driver.find_element(By.XPATH, delete_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
            else:
                # self.driver.find_element(By.CSS_SELECTOR, ipObjectListPage_deleteButton_warningNo_posCss).click()
                # self.driver.find_element(By.ID, ipObjectListPage_deleteButton_posId).click()  # 点击删除按钮
                self.driver.find_element(By.XPATH, delete_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(0.5)
            return 200
        except:
            return 400