from selenium.webdriver.common.by import By
from element_position.objectElementPosition import *
from src.ui.object.pageJump import PageJump

class SearchObject():
    def __init__(self, driver):
        self.driver = driver
        
    def search(self, name, object_element_position, vsys_name=""):
        search_element_position = object_element_position["search"]
        page_jump_element_position = object_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        page_jump.jump_sub_object_page(page_jump_element_position)
        self.driver.find_element(By.ID, search_element_position["objectListPage_searchLabel_posId"]).send_keys(name)
        self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_selectName_posXpath"]).click()
        self.driver.find_element(By.ID, mainPage_objectSearch_buttonSearch_posId).click()
        element_tr = self.driver.find_element(By.XPATH, search_element_position["objectListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "tr") 
        if len(row) != 0 :
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
            return 200, first_row_checkBox_element
        else:
            return 400, ""
