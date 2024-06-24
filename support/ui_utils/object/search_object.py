import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.object.page_jump import PageJump

class SearchObject():
    def __init__(self, driver):
        self.driver = driver
        
    def search(self, name, object_element_position, vsys_name=""):
        search_element_position = object_element_position["search"]
        page_jump_element_position = object_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        time.sleep(3)
        page_jump.jump_sub_object_page(page_jump_element_position, "UIwithTrafficTestVsys")
        self.driver.find_element(By.ID, search_element_position["objectListPage_searchLabel_posId"]).send_keys(name)
        self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_selectName_posXpath"]).click()
        btn = self.driver.find_element(By.ID, mainPage_objectSearch_buttonSearch_posId)
        self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
        time.sleep(2)
        element_tr = self.driver.find_element(By.XPATH, search_element_position["objectListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "tr") 
        if len(row) != 0 :
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
            return 200, first_row_checkBox_element
        else:
            return 400, ""
