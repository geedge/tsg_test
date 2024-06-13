# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *


class PageJump():
    def __init__(self, driver):
        self.driver = driver

    def jump_sub_profile_page(self, page_jump_element_position, vsys_name=""):
        # 菜单操作
        self.driver.find_element(By.CSS_SELECTOR,
                                 page_jump_element_position["mainPage_navigationBar_logo_posCss"]).click()
        self.change_vsys(vsys_name=vsys_name)
        self.driver.find_element(By.ID, page_jump_element_position["mainPage_profileFirstLevelMenu_posId"]).click()
        self.driver.find_element(By.ID, page_jump_element_position["mainPage_profileSecondLevelMenu_posId"]).click()

    def change_vsys(self, vsys_name=""):
        current_vsys_name = self.driver.find_element(By.XPATH,
                                                     mainPage_currentPage_vsysName_posXpath).text.strip().lower()
        if vsys_name.lower() == current_vsys_name:
            print(f"the current vsys: {current_vsys_name}")
            return 0
        else:
            if vsys_name == "":
                # change_vsys_name = "UIAutoTestVsys"
                change_vsys_name = "ApiAutoTestVsys"
                if change_vsys_name.lower() == current_vsys_name:
                    print(f"the current vsys: {current_vsys_name}")
                    return 0
            else:
                change_vsys_name = vsys_name
            # print(f"the current vsys: {current_vsys_name}, switch to vsys: {change_vsys_name}")
            self.driver.find_element(By.CSS_SELECTOR, mainPage_button_menu_posXCss).click()
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