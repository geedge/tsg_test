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
            self.driver.find_element(By.ID, create_element_position["objectListPage_dropDown_createButton_posId"]).click()
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
            elif data["objectType"] == "ip_learning":
                print("to be added...")
            else:
                for x in data["item"]:
                    if data["objectType"] == "ip":
                        self.driver.find_element(By.ID, create_element_position["objectPage_ipType_posId"]).click()
                    self.driver.find_element(By.ID, create_element_position["objectPage_addItem_posId"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"]).send_keys(x)
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            # 确认创建
            self.driver.find_element(By.ID, create_element_position["objectPage_okButton_posId"]).click()
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except:
            return 400
    
    def create_group(self, data, object_type, object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击create group
            self.driver.find_element(By.ID, create_element_position["objectListPage_createButton_posId"]).click()
            self.driver.find_element(By.ID, create_element_position["objectListPage_dropDown_createGroupButton_posId".format(object_type)]).click()
            # 输入name
            object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            # 切换type
            if data["selectType"] == True:
                self.driver.find_element(By.ID, create_element_position["groupObjectPage_selectType{}_posId".format(object_type)]).click()
            # 点subordinate的+
            self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_addSubordinate_posXpath"]).click()
            # 添加subordinate
            group_subordinate_data = data["groupSubordinate"]
            if len(group_subordinate_data) != 0:
                for x in range(len(group_subordinate_data)):
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = create_element_position["groupObjectPage_selectSubordinate{}_posXpath".format(object_type)].format(replaceValue=group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_closeSubordinate{}_posXpath".format(object_type)]).click()
                    if len(group_subordinate_data) > 1 and x < len(group_subordinate_data) - 1:
                        self.driver.find_element(By.ID, create_element_position["groupObjectPage_addSubordinateObject_posId"]).click()
            # 判断是否存在exclude
            group_exclude_data = data["groupExclude"]
            if len(group_exclude_data) != 0:
                # 使能exclude
                self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_enableExclude_posXpath"]).click()
                # 点exclude的+
                self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_addExclude_posXpath"]).click()
                # 添加exclude
                group_exclude_data = data["groupExclude"]
                for y in range(len(group_exclude_data)):
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = create_element_position["groupObjectPage_selectExclude{}_posXpath".format(object_type)].format(replaceValue=group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_closeExclude{}_posXpath".format(object_type)]).click()
                    if len(group_exclude_data) > 1 and y < len(group_exclude_data) - 1:
                        self.driver.find_element(By.ID, create_element_position["groupObjectPage_addExcludeObject_posId"]).click()
            # 确认创建
            self.driver.find_element(By.ID, create_element_position["objectPage_okButton_posId"]).click()
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except:
            return 400
        