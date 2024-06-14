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
from support.ui_utils.profile.page_jump import PageJump
from selenium.webdriver.common.keys import Keys


class SearchProfile():
    def __init__(self, driver):
        self.driver = driver

    def search(self, name, profile_element_position, vsys_name=""):
        search_element_position = profile_element_position["search"]
        page_jump_element_position = profile_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        page_jump.jump_sub_object_page(page_jump_element_position)
        self.driver.find_element(By.ID, search_element_position["profileListPage_searchLabel_posId"]).click()
        # 通过name 查询
        dropdown_item_posXpath = search_element_position["profileListPage_searchLabel_selectName_posXpath"].format(replaceName="Name")
        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()  # 点击查询下拉菜单中item
        input_item_posXpath = search_element_position["profileListPage_searchLabel_inputContent_posXpath"].format( replaceName="Name")
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)  # 输入查询值
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(Keys.ENTER)  # 模拟回车按键
        # 点击查询按钮
        element_search = self.driver.find_element(By.ID, mainPage_profileSearch_buttonSearch_posId)
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        time.sleep(1)
        element_tr = self.driver.find_element(By.XPATH, search_element_position["profileListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "tr")
        if len(row) != 0 :
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
            return 200, first_row_checkBox_element
        else:
            return 400, ""

