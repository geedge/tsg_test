import configparser
import os
import sys
import shutil
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from myWebDriver import MyWebDriver
# from element_position.objectElementPosition import *
from element_position.profileElementPosition import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from page_element.ln_objects_element_positionMERGELAST import *
# from common.driver_common.screenshot import screenshot_on_failure
# from common.read_data.read_data import ReadData
# from config.workpath import workdir
# from cases.conftest import demo_fixture
# from common.ui_common.login_logout import loginout

class ShapingRulePublicFunc():
    def __init__(self, driver):
        self.driver = driver
        
    def change_vsys(self, vsys_name=""):
        """
        调整vsys，vsys_name可以为空字符串，不用切换vsys。vsys_name=空时，默认切换到UIAutoTestVsys
        :param vsys_name:  vsys name, 例如：Default Vsys 、或者空。vsys_name与当前vsys一直或者为空字符串时，不要操作vsys
        :return:
        """
        current_vsys_name = self.driver.find_element(By.XPATH, mainPage_currentPage_vsysName_posXpath).text.strip().lower()
        if vsys_name.lower() == current_vsys_name:
            print(f"the current vsys: {current_vsys_name}")
            return 0
        else:    # 空为切换默认   剩下为指定切换
            if vsys_name == "":     # 空，切换到默认vsys
                change_vsys_name = "UIAutoTestVsys"
                if change_vsys_name.lower() == current_vsys_name:    # 如果默认系统和当前一直，也不用点击
                    print(f"the current vsys: {current_vsys_name}")
                    return 0
            else:     # 切换到指定vsys
                change_vsys_name = vsys_name
            print(f"the current vsys: {current_vsys_name}, switch to vsys: {change_vsys_name}")
            self.driver.find_element(By.CSS_SELECTOR, mainPage_button_menu_posXCss).click()     # 点击vsys menu
            vsys_tree_name_list = self.driver.find_elements(By.XPATH, mainPage_vsysTree_vsysName_posXpath)
            flag_num = 0
            for el_vsys_item in vsys_tree_name_list:
                vsys_item_name = el_vsys_item.text.strip().lower()
                if vsys_item_name == change_vsys_name.lower():
                    flag_num = 1
                    el_vsys_item.click()
                    break
            if flag_num == 0:
                print(f"no vsys: {change_vsys_name}")
                raise ValueError(f"no vsys: {change_vsys_name}")
            
    def search(self, mainPage_profileSearch_selectLabel_posId, listPage_profileSearch_subProfiles_dropDown_item_posXpath,
              listPage_profileSearch_subProfiles_input_itemContent_posXpath, mainPage_profileSearch_buttonSearch_posId,
              listPage_profilTable_subProfiles_tableTbody_posXpath, listPage_profilTable_subProfiles_tableHeader_posXpath,
              listPage_profileSearch_subProfiles_dropDown_typeItem_posXpath="", **kwargs):
        """
        profiles模块中从点击查询到查询到结果使用方法，并返回第一行数据和表头、class的字典
        :param mainPage_profileSearch_selectLabel_posId: 查询框id
        :param listPage_profileSearch_subProfiles_dropDown_item_posXpath: 下拉列表item的xpath
        :param listPage_profileSearch_subProfiles_input_itemContent_posXpath: 选中item后，输入input的xpath
        :param mainPage_profileSearch_buttonSearch_posId: 查询按钮id
        :param listPage_profilTable_subProfiles_tableTbody_posXpath: 列表页body的部分xpath
        :param listPage_profilTable_subProfiles_tableHeader_posXpath: 列表页header的部分xpath
        :param listPage_profileSearch_subProfiles_dropDown_typeItem_posXpath: 如果有下拉列表item的枚举选项定位，需要增补
        :param kwargs: 需要查询的内容，来自调用函数
        :return: [first_row, map_header_className]
        """
        # 点击search查询框
        self.driver.find_element(By.ID, mainPage_profileSearch_selectLabel_posId).click()
        # 循环输入查询内容
        for key, value in kwargs.items():
            if "_" in key:
                key = key.replace("_", " ")   # 将下划线替换为空格
            dropdown_item_posXpath = listPage_profileSearch_subProfiles_dropDown_item_posXpath.format(replaceName=key)
            self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()    # 点击下拉item
            if key != "type":
                input_item_posXpath = listPage_profileSearch_subProfiles_input_itemContent_posXpath.format(replaceName=key)
                self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(value.strip())       # 输入查询值
                self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(Keys.ENTER)         # 模拟回车按键
            else:
                dropdown_typeItem_posXpath = listPage_profileSearch_subProfiles_dropDown_typeItem_posXpath.format(replaceName=value.split("->")[0])
                self.driver.find_element(By.XPATH, dropdown_typeItem_posXpath).click()    # 点击type的下拉item
        # 点击查询按钮
        element_search = self.driver.find_element(By.ID, mainPage_profileSearch_buttonSearch_posId)
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        element_tbody = self.driver.find_element(By.XPATH, listPage_profilTable_subProfiles_tableTbody_posXpath)  # 找到所有的行，table的body
        element_header = self.driver.find_element(By.XPATH, listPage_profilTable_subProfiles_tableHeader_posXpath)   # 查询table的header
        # 获取table header的text、th.class
        headers = element_header.find_elements(By.XPATH, "th")     # table header
        rows = element_tbody.find_elements(By.XPATH, "tr")     # table body
        if len(rows) == 0:
            print(f"没有查询到数据：查询条件：{kwargs}")
            return [0, 0]
        map_header_className = {}  # 表头名称和th.class的映射，为了从表body中取对应列的值{"ID":"33"}
        for th in headers:
            self.driver.execute_script("arguments[0].scrollIntoView();", th)
            header_content = th.text.strip()
            classNames = th.get_attribute("class").split()
            for c_name in classNames:
                if "el-table" in c_name:
                    tableBodyRowClassName = c_name
            if header_content and tableBodyRowClassName:
                map_header_className[header_content] = tableBodyRowClassName
        # 从第一行查询的结果中，取出需要断言的值、name
        first_row = rows[0]
        return [first_row, map_header_className]
    
    def delete(self, shapingRuleListpage_deleteButton_posId, shapingRuleListpage_okButton_warningYes_posXpath, shapingRuleListpage_okButton_warningNo_posXpath):
        """
        直接删除函数，
        :param listPage_object_delButton_posId: 删除按钮id
        :param listPage_dialogTips_delButton_yes_posCss: 提示删除框中yes定位CSS
        :param listPage_dialogTips_delButton_no_posCss: 提示删除框中no定位CSS
        :return:
        """
        self.driver.find_element(By.ID, shapingRuleListpage_deleteButton_posId).click()  # 点击删除按钮
        # random_yes_or_no = random.randint(0, 1)
        random_yes_or_no = 0
        if random_yes_or_no == 0:  # 点击yes，删除
            self.driver.find_element(By.XPATH, shapingRuleListpage_okButton_warningYes_posXpath).click()  # 直接删除
        else:
            self.driver.find_element(By.XPATH, shapingRuleListpage_okButton_warningNo_posXpath).click()  # 先取消，再删除
            self.driver.find_element(By.ID, shapingRuleListpage_deleteButton_posId).click()  # 点击删除按钮
            self.driver.find_element(By.XPATH, shapingRuleListpage_okButton_warningYes_posXpath).click()  # 点击yes，删除
        time.sleep(0.5)