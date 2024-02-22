# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.object.pageJump import PageJump
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
            self.driver.find_element(By.ID, create_element_position["objectListPage_createButton_posId"]).click()
            self.driver.find_element(By.ID, create_element_position["objectListPage_dropDown_createIpButton_posId"]).click()
            # 输入name
            object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            # 添加item
            if data["objectType"] == "http_signature":
                for i in data["item"]:
                    self.driver.find_element(By.ID, create_element_position["objectPage_addItem_posId"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_item_key_dropDown_posXpath"]).click()
                    temp_element_position = create_element_position["objectPage_item_key_dropDown_select_posXpath"].format(replaceValue=i["itemKey"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    temp_element_position = create_element_position["objectPage_item_value_select_posXpath"].format(replaceValue=i["itemValue"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    num = 0
                    for t in i["value"]:
                        num += 1
                        temp_element_position = create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=num)
                        self.driver.find_element(By.XPATH, temp_element_position).send_keys(t)
                        if data["plus"] == True and num < len(i["value"]):
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_item_value_plus_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif data["objectType"] == "keyword":
                print("to be added...")
            elif data["objectType"] == "url" or data["objectType"] == "account" or data["objectType"] == "phone_number":
                print("to be added...")
            elif data["objectType"] == "tunnel":
                print("to be added...")
            elif data["objectType"] == "flag":
                print("to be added...")
            elif data["objectType"] == "interval":
                print("to be added...")
            elif data["objectType"] == "application":
                print("to be added...")
            else:
                for x in data["item"]:
                    self.driver.find_element(By.ID, create_element_position["objectPage_addItem_posId"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"]).send_keys(x)
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            # 确认创建
            self.driver.find_element(By.ID, create_element_position["objectPage_okButton_posId"]).click()
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except:
            return 400
    
    def create_group(self, data, object_element_position):
        try:
            return 200
        except:
            return 400
        