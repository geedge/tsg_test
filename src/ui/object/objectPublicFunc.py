import configparser
import os
import sys
import shutil
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from myWebDriver import MyWebDriver
from element_position.objectElementPosition import *
from element_position.objectElementPosition import *
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

class ObjectPublicFunc():
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
    
    def delete(self, listPage_object_delButton_posId, listPage_dialogTips_delButton_yes_posCss, listPage_dialogTips_delButton_no_posCss):
        """
        直接删除函数，
        :param listPage_object_delButton_posId: 删除按钮id
        :param listPage_dialogTips_delButton_yes_posCss: 提示删除框中yes定位CSS
        :param listPage_dialogTips_delButton_no_posCss: 提示删除框中no定位CSS
        :return:
        """
        self.driver.find_element(By.ID, listPage_object_delButton_posId).click()  # 点击删除按钮
        random_yes_or_no = random.randint(0, 1)
        if random_yes_or_no == 0:  # 点击yes，删除
            self.driver.find_element(By.XPATH, listPage_dialogTips_delButton_yes_posCss).click()  # 直接删除
        else:
            # self.driver.find_element(By.CSS_SELECTOR, listPage_dialogTips_delButton_no_posCss).click()  # 先取消，再删除
            # self.driver.find_element(By.ID, listPage_object_delButton_posId).click()  # 点击删除按钮
            self.driver.find_element(By.XPATH, listPage_dialogTips_delButton_yes_posCss).click()  # 点击yes，删除
        time.sleep(0.5)