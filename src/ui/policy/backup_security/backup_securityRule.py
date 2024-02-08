import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from myWebDriver import MyWebDriver
from screenshot import screenshot_on_failure
from element_position.policyElementPosition import *
from readData import ReadData
from workpath import workdir
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from securityRulePublicFunc import SecurityRulePublicFunc
import pytest_check
import inspect

class SecurityRule():
    def __init__(self, driver):
        self.workdir = workdir
        # self.my_random = RandomName()
        self.driver = driver
        self.rule_pub_func = SecurityRulePublicFunc(self.driver)
        
    def _create(self, test_data):
        # 页面跳转
        self._goto_subPolicyPage()
        # 点击create
        self.driver.find_element(By.ID, securityRuleListPage_createButton_posId).click()
        # 输入name
        rule_name = test_data["ruleName"]
        self.driver.find_element(By.XPATH, securityRulePage_inputName_posXpath).send_keys(rule_name)
        ip_data = test_data["ip"]
        if len(ip_data) != 0:
            # 点source ip address的+
            self.driver.find_element(By.XPATH, securityRulePage_addCondition_srcIP_posXpath).click()
            # 通过ip name搜索并选中
            for i in range(len(ip_data)):
                self.driver.find_element(By.XPATH, securityRulePage_searchSrcIP_posXpath).send_keys(ip_data[i]["name"])
                self.driver.find_element(By.XPATH, securityRulePage_searchSrcIP_posXpath).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, securityRulePage_selectSrcIP_posXpath).click()
                self.driver.find_element(By.XPATH, securityRulePage_closeSrcIP_posXpath).click()
        application_data = test_data["application"]
        if len(application_data) != 0:
            # 点application的+
            self.driver.find_element(By.XPATH, securityRulePage_addCondition_application_posXpath).click()
            # 通过application name搜索并选中
            for j in range(len(application_data)):
                self.driver.find_element(By.XPATH, securityRulePage_searchApplication_posXpath).send_keys(application_data[j]["name"])
                self.driver.find_element(By.XPATH, securityRulePage_searchApplication_posXpath).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, securityRulePage_selectApplication_posXpath).click()
        profile_data = test_data["profile"]
        if len(profile_data) != 0:
            # 点profile的+
            self.driver.find_element(By.XPATH, shapingRulePage_addProfile_posXpath).click()
            # 通过profile name搜索并选中
            profile_data = test_data["profile"]
            for j in range(len(profile_data)):
                self.driver.find_element(By.XPATH, shapingRulePage_searchProfile_posXpath).send_keys(profile_data[j]["name"])
                self.driver.find_element(By.XPATH, shapingRulePage_searchProfile_posXpath).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, shapingRulePage_selectProfile_posXpath).click()
        # 点enable
        self.driver.find_element(By.XPATH, securityRulePage_enable_posXpath).click()
        # 确认创建
        self.driver.find_element(By.ID, securityRulePage_okButton_yes_posId).click()
        self.driver.find_element(By.XPATH, securityRulePage_okButton_warningYes_posXpath).click()
        return 200
    
    def _search(self, name, vsys_name=""):
        # 打开该列表
        self._goto_subPolicyPage()
        # 点击search查询框
        self.driver.find_element(By.ID, securityRuleListPage_searchLable_posId).click()
        dropdown_item_posXpath = securityRuleListPage_searchLable_dropDown_item_posXpath.format(replaceName="Name")
        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()    # 点击下拉item
        input_item_posXpath = securityRuleListPage_searchLable_input_itemContent_posXpath.format(replaceName="Name")
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)       # 输入查询值
        self.driver.find_element(By.ID, securityRuleListPage_searchLable_searchButton_posId).click()
        element_tr = self.driver.find_element(By.XPATH, securityRuleListPage_tableTbody_posXpath)
        row = element_tr.find_elements(By.XPATH, "tr") 
        if len(row) != 0 :
            first_row = row[0]
            self.first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
    
    def _delete(self, is_del_all=False):
        if is_del_all == True:
            self.driver.find_element(By.XPATH, securityRulelistPage_allSelect_posXpath).click()    # 点击all按钮
        else:
            # 点击勾选第一行选择框
            self.first_row_checkBox_element.click()     # 变量来自查询函数
        self.rule_pub_func.delete(securityRuleListPage_deleteButton_posId, securityRuleListpage_okButton_warningYes_posXpath, securityRuleListpage_okButton_warningNo_posXpath)
    
    def _goto_subPolicyPage(self, vsys_name=""):
        # 菜单操作
        self.driver.find_element(By.CSS_SELECTOR, mainPage_navigationBar_logo_posCss).click()
        self.rule_pub_func.change_vsys(vsys_name=vsys_name)
        self.driver.find_element(By.ID, mainPage_firstLevelMenu_policy_posId).click()
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_security_posId).click()