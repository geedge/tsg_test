# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.ui.object.pageJump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from element_position.objectElementPosition import *

class CreateObject():
    def __init__(self, driver):
        self.driver = driver
        
    def create(self, data, object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击create
            object_name = data["name"]
            self.driver.find_element(By.ID, create_element_position["objectListPage_createButton_posId"]).click()
            self.driver.find_element(By.ID, create_element_position["objectListPage_dropDown_createIpButton_posId"]).click()
            # 输入name
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            # 添加item
            for item in data["item"]:
                self.driver.find_element(By.ID, create_element_position["objectPage_addItem_posId"]).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"]).send_keys(item)
                self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            # 确认创建
            self.driver.find_element(By.ID, create_element_position["objectPage_okButton_posId"]).click()
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except:
            return 400