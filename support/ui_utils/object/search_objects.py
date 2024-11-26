import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.object.page_jump import PageJump

class SearchObject:
    def __init__(self, driver):
        self.driver = driver
        
    def search(self, name, object_element_position, vsys_name="", search_key="Name"):
        search_element_position = object_element_position["search"]
        page_jump_element_position = object_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        time.sleep(0.5)
        page_jump.jump_sub_object_page(page_jump_element_position)
        """
        self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"] ).send_keys(name)
        self.driver.find_element(By.XPATH, ipObjectPage_searchLable_dropDown_item_posXpath).click()
        #input_item_posXpath = search_element_position["objectListPage_searchLabel_selectName_posXpath"].format(replaceValue="Name")
        # self.driver.find_element(By.XPATH, '//*[@class="MuiInput-input css-1u0jcuo"]').send_keys(name)
        self.driver.find_element(By.XPATH, mainPage_objectSearch_buttonSearch_posXpath).click()
        time.sleep(0.5)
        """
        # 通过name 查询时
        # 先输入Name，下拉列表显示Name contains objectname后选择对应选项
        self.driver.find_element(By.XPATH, search_element_position["objectListPage_search_input_posXpath"]).send_keys(Keys.CONTROL + "a")
        self.driver.find_element(By.XPATH, search_element_position["objectListPage_search_input_posXpath"]).send_keys(name)
        if search_key == None:
            btn = self.driver.find_element(By.XPATH, objectListPage_full_text_search_dropDown_item_posXpath)
        else:# 下拉列表显示Name contains profilename后选择对应选项
            btn = self.driver.find_element(By.XPATH, search_element_position["objectListPage_search_dropDown_item_posXpath"].format(replaceValue=search_key))
        self.driver.execute_script("arguments[0].click()", btn)  # 点击查询下拉菜单中item
        # 点击查询按钮
        element_search = self.driver.find_element(By.XPATH, search_element_position["objectListPage_search_button_posXpath"])
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        time.sleep(0.5)
        element_tr = self.driver.find_element(By.XPATH, search_element_position["objectListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "div")
        if len(row) != 0 :
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, '//*[@inputprops="[object Object]"]')
            return 200, first_row_checkBox_element
        else:
            return 400, ""


