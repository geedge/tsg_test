import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from myWebDriver import MyWebDriver
# from randomName import RandomName
from screenshot import screenshot_on_failure
from element_position.policyElementPosition import *
from readData import ReadData
from workpath import workdir
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from policy.shapingRulePublicFunc import ShapingRulePublicFunc
import pytest_check
import inspect

class ShapingRuleWithGeneric:
    def __init__(self, driver):
        self.workdir = workdir
        # self.my_random = RandomName()
        self.driver = driver
        self.rule_pub_func = ShapingRulePublicFunc(self.driver)
        
    def _create(self, ip_name, profile_name, rule_name):
        # 页面跳转
        self._goto_subPolicyPage()
        # 点击create
        self.driver.find_element(By.ID, shapingRuleListPage_createButton_posId).click()
        # 输入name
        self.rule_name = rule_name
        self.driver.find_element(By.XPATH, shapingRulePage_inputName_posXpath).send_keys(self.rule_name)
        # 点source ip address的+
        self.driver.find_element(By.XPATH, shapingRulePage_addCondition_srcIP_posXpath).click()
        # 通过ip name搜索并选中
        self.driver.find_element(By.XPATH, shapingRulePage_searchSrcIP_posXpath).send_keys(ip_name)
        self.driver.find_element(By.XPATH, shapingRulePage_searchSrcIP_posXpath).send_keys(Keys.ENTER)
        self.driver.find_element(By.XPATH, shapingRulePage_selectSrcIP_posXpath).click()
        # 点profile的+
        self.driver.find_element(By.XPATH, shapingRulePage_addProfile_posXpath).click()
        # 通过profile name搜索并选中
        self.driver.find_element(By.XPATH, shapingRulePage_searchProfile_posXpath).send_keys(profile_name)
        self.driver.find_element(By.XPATH, shapingRulePage_searchProfile_posXpath).send_keys(Keys.ENTER)
        self.driver.find_element(By.XPATH, shapingRulePage_selectProfile_posXpath).click()
        # 点enable
        self.driver.find_element(By.XPATH, shapingRulePage_enable_posXpath).click()
        # 确认创建
        self.driver.find_element(By.ID, shapingRulePage_okButton_yes_posId).click()
        self.driver.find_element(By.XPATH, shapingRulePage_okButton_warningYes_posXpath).click()
        return 200
    
    def _search(self, name):
        # 打开该列表
        self._goto_subPolicyPage()
        # 点击search查询框
        self.driver.find_element(By.ID, shapingRuleListPage_searchLable_posId).click()
        dropdown_item_posXpath = shapingRuleListPage_searchLable_dropDown_item_posXpath.format(replaceName="Name")
        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()    # 点击下拉item
        input_item_posXpath = shapingRuleListPage_searchLable_input_itemContent_posXpath.format(replaceName="Name")
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)       # 输入查询值
        self.driver.find_element(By.ID, shapingRuleListPage_searchLable_searchButton_posId).click()
        element_tr = self.driver.find_element(By.XPATH, shapingRuleListPage_tableTbody_posXpath)
        row = element_tr.find_elements(By.XPATH, "tr") 
        if len(row) != 0 :
            first_row = row[0]
            self.first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
    
    def _delete(self, is_del_all=False):
        if is_del_all == True:
            self.driver.find_element(By.XPATH, shapingRuleListpage_allButton_posXpath).click()    # 点击all按钮
        else:
            # 点击勾选第一行选择框
            self.first_row_checkBox_element.click()     # 变量来自查询函数
        self.rule_pub_func.delete(shapingRuleListpage_deleteButton_posId, shapingRuleListpage_okButton_warningYes_posXpath, shapingRuleListpage_okButton_warningNo_posXpath)
    
    def _goto_subPolicyPage(self, vsys_name=""):
        # 菜单操作
        self.driver.find_element(By.CSS_SELECTOR, mainPage_navigationBar_logo_posCss).click()
        self.rule_pub_func.change_vsys(vsys_name=vsys_name)
        self.driver.find_element(By.ID,mainPage_firstLevelMenu_policy_posId).click()
        self.driver.find_element(By.ID,mainPage_secondLevelMenu_shaping_posId).click()