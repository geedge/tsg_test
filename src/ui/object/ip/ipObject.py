import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from myWebDriver import MyWebDriver
# from randomName import RandomName
from screenshot import screenshot_on_failure
from element_position.objectElementPosition import *
from readData import ReadData
from workpath import workdir
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from objectPublicFunc import ObjectPublicFunc
import pytest_check
import inspect

class IpAddress:
    def __init__(self, driver):
        self.workdir = workdir
        # self.my_random = RandomName()
        self.driver = driver
        self.object_pub_func = ObjectPublicFunc(self.driver)
        
    def _create(self, data):
        # 页面跳转
        self._goto_subObjectPage()
        # 点击create
        self.object_name = data["name"]
        self.driver.find_element(By.ID, listPage_object_ip_address_createButton_posId).click()
        self.driver.find_element(By.ID, listPage_object_ip_address_create_ip_address_Button_posId).click()
        self.driver.find_element(By.XPATH, ip_addressObjectPage_input_name_posXpath).send_keys(self.object_name)
        # 添加item
        for item in data["item"]:
            self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_inputItem_posXpath).send_keys(item)
            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_saveItem_posXpath).click()
        # 确认创建
        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_saveYes_posXpath).click()
        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_warningSaveYes_posXpath).click()
        return 200
    
    def _search(self, name, vsys_name=""):
        # 打开该列表
        self._goto_subObjectPage(vsys_name=vsys_name)
        self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(name)
        self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Name_posXpath).click()
        self.driver.find_element(By.ID, mainPage_objectSearch_buttonSearch_posId).click()
        element_tr = self.driver.find_element(By.XPATH, listPage_objectTable_ip_tableTbody_posXpath)
        row = element_tr.find_elements(By.XPATH, "tr") 
        if len(row) != 0 :
            first_row = row[0]
            self.first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
    
    def _delete(self, is_del_all=False):
        if is_del_all == True:
            self.driver.find_element(By.XPATH, listPage_objectBottomPage_ip_object_button_allSelect_posXpath).click()    # 点击all按钮
        else:
            # 点击勾选第一行选择框
            self.first_row_checkBox_element.click()     # 变量来自查询函数
        self.object_pub_func.delete(listPage_object_delButton_posId, listPage_dialogTips_delButton_yes_posCss, listPage_dialogTips_delButton_no_posCss)
    
    def _goto_subObjectPage(self, vsys_name=""):
        # 菜单操作
        self.driver.find_element(By.CSS_SELECTOR, mainPage_navigationBar_logo_posCss).click()
        self.object_pub_func.change_vsys(vsys_name=vsys_name)
        self.driver.find_element(By.ID,mainPage_firstLevelMenu_Objects_posId).click()
        self.driver.find_element(By.ID,mainPage_secondLevelMenu_ipAddress_posId).click()