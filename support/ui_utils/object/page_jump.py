import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from support.ui_utils.element_position.object_element_position import *
from selenium.webdriver.common.by import By
import configparser

class PageJump():
    def __init__(self, driver):
        self.driver = driver
        
    def jump_sub_object_page(self, page_jump_element_position, vsys_name=""):
        # 菜单操作
        btn = self.driver.find_element(By.CSS_SELECTOR, page_jump_element_position["mainPage_navigationBar_logo_posCss"], find_before_wait_time=1.0)
        btn = self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
        self.change_vsys(vsys_name=vsys_name)
        self.driver.find_element(By.ID, page_jump_element_position["mainPage_policyFirstLevelMenu_posId"]).click()
        self.driver.find_element(By.ID, page_jump_element_position["mainPage_policySecondLevelMenu_posId"]).click()
        
    def change_vsys(self, vsys_name=""):
        current_vsys_name = self.driver.find_element(By.XPATH, mainPage_currentPage_vsysName_posXpath).text.strip().lower()
        #print(f"the current vsys: {current_vsys_name}")
        current_path = os.path.dirname(__file__)   # 当前文件目录
        temp_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
        conf_path = os.path.join(temp_path, "configuration_file.ini")
        #print(conf_path)
        conf = configparser.ConfigParser()
        conf.read(conf_path, encoding="utf-8")
        id_for_ui = conf.get("vsys", "id_for_ui")
        id_vsys_format = "vsys{}".format(id_for_ui)   # 使用配置变量值
        #print(id_vsys_format)
        # 传入vsys_name值区分
        if vsys_name == "":     # 空，vsys值来自配置文件
            change_vsys_name = id_vsys_format
        else:     # 切换到指定vsys
            change_vsys_name = vsys_name
        self.driver.find_element(By.CSS_SELECTOR, mainPage_button_menu_posXCss).click()     # 点击vsys menu
        vsys_tree_name_list = self.driver.find_elements(By.XPATH, mainPage_vsysTree_vsysName_posXpath)
        time.sleep(1)
        flag_num = 0
        for el_vsys_item in vsys_tree_name_list:
            vsys_item_name = el_vsys_item.text.strip().lower()
            vsys_item_name_list = vsys_item_name.split("\n")
            #print(vsys_item_name_list)
            if change_vsys_name.lower() in vsys_item_name_list:
                flag_num = 1
                el_vsys_item.find_element(By.XPATH, ".//div[@class='menu-title']").click()
                #print(f"Change to vsys {change_vsys_name}")
                break
        if flag_num == 0:
            print(f"no vsys: {change_vsys_name}", flush=True)
