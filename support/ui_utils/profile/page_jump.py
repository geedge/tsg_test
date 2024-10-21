import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from support.ui_utils.element_position.object_element_position import *
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
import configparser
from datetime import datetime 

class PageJump:
    def __init__(self, driver):
        self.driver = driver

    def jump_sub_profile_page(self, page_jump_element_position, vsys_name=""):
        """
        vsys_name:空值时，参数来自配置文件
        """
        # 菜单操作，先判断是否是当前Vsys再判断是否重新选择Vsys
        btn = self.driver.find_element(By.XPATH, page_jump_element_position["mainPage_navigationBar_logo_posCss"])
        self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
        #self.change_vsys(vsys_name=vsys_name, page_jump_element_position=page_jump_element_position)   # 调整到页面登录时切换vsys
        btn = self.driver.find_element(By.XPATH, page_jump_element_position["mainPage_profileFirstLevelMenu_posId"])
        self.driver.execute_script("arguments[0].click()", btn)
        btn = self.driver.find_element(By.XPATH, page_jump_element_position["mainPage_profileSecondLevelMenu_posId"])
        self.driver.execute_script("arguments[0].click()", btn)
        # self.driver.find_element(By.ID, page_jump_element_position["mainPage_profileFirstLevelMenu_posId"]).click()
        # self.driver.find_element(By.ID, page_jump_element_position["mainPage_profileSecondLevelMenu_posId"]).click()

    def change_vsys(self, vsys_name="", page_jump_element_position=""):
        current_vsys_name = self.driver.find_element(By.XPATH, mainPage_currentPage_vsysName_posXpath).text.strip().lower()
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"the current vsys: {current_vsys_name}")
        current_path = os.path.dirname(__file__)   # 当前文件目录
        temp_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
        conf_path = os.path.join(temp_path, "configuration_file.ini")
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], conf_path)
        conf = configparser.ConfigParser()
        conf.read(conf_path, encoding="utf-8")
        id_for_ui = conf.get("vsys", "for_traffic_verification")
        id_vsys_format = "vsys{}".format(id_for_ui)   # 使用配置变量值
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], id_vsys_format)
        # 传入vsys_name值区分
        if vsys_name == "":     # 空，vsys值来自配置文件
            change_vsys_name = id_vsys_format
        else:     # 切换到指定vsys
            change_vsys_name = vsys_name
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"the change_vsys_name: {change_vsys_name}")
        if change_vsys_name != current_vsys_name:
            self.driver.find_element(By.CSS_SELECTOR,page_jump_element_position["mainPage_navigationBar_logo_posCss"]).click()
        self.driver.find_element(By.CSS_SELECTOR, mainPage_button_menu_posXCss).click()     # 点击vsys menu
        vsys_tree_name_list = self.driver.find_elements(By.XPATH, mainPage_vsysTree_vsysName_posXpath)
        time.sleep(0.5)
        flag_num = 0
        for el_vsys_item in vsys_tree_name_list:
            vsys_item_name = el_vsys_item.text.strip().lower()
            vsys_item_name_list = vsys_item_name.split("\n")
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], vsys_item_name_list)
            if change_vsys_name.lower() in vsys_item_name_list:
                flag_num = 1
                el_vsys_item.find_element(By.XPATH, ".//div[@class='menu-title']").click()
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Change to vsys {current_vsys_name}")
                break
        if flag_num == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"no vsys: {change_vsys_name}", flush=True)