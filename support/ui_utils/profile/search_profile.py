import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from support.ui_utils.object.page_jump import PageJump


class SearchProfile():
    def __init__(self,driver):
        self.driver = driver
    def search(self,profile_name,profile_element_position):
        profile_search_element = profile_element_position["search"]
        sff_pagejump_element = profile_element_position["page_jump"]
        page_jump = PageJump(self.driver)
        page_jump.jump_sub_object_page(sff_pagejump_element)
        # 点击搜索框并搜索数据
        self.driver.find_element(By.ID,profile_search_element["profileListPage_searchLabel_posId"]).click()
        self.driver.find_element(By.XPATH,profile_search_element["profileListPage_selectName_posXpath"].format(replaceName="Name")).click()
        input_item_posXpath = profile_search_element["profileListPage_searchLable_input_itemContent_posXpath"].format(replaceName="Name")
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(profile_name)
        self.driver.find_element(By.ID,mainPage_profileSearch_buttonSearch_posId ).click()
        time.sleep(10)
        element_tr = self.driver.find_element(By.XPATH, profile_search_element["profileListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "tr") 
        if len(row) != 0 :
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
            return 200, first_row_checkBox_element
        else:
            return 400, ""

