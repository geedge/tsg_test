import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.object.page_jump import PageJump

class SearchObject:
    def __init__(self, driver):
        self.driver = driver
        
    def search(self, name, object_element_position, vsys_name=""):
        search_element_position = object_element_position["search"]
        page_jump_element_position = object_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        time.sleep(0.5)
        page_jump.jump_sub_object_page(page_jump_element_position)
        self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"] ).send_keys(name)
        self.driver.find_element(By.XPATH, ipObjectPage_searchLable_dropDown_item_posXpath).click()
        #input_item_posXpath = search_element_position["objectListPage_searchLabel_selectName_posXpath"].format(replaceValue="Name")
        # self.driver.find_element(By.XPATH, '//*[@class="MuiInput-input css-1u0jcuo"]').send_keys(name)
        self.driver.find_element(By.XPATH, mainPage_objectSearch_buttonSearch_posXpath).click()
        time.sleep(0.5)
        element_tr = self.driver.find_element(By.XPATH, search_element_position["objectListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "div")
        if len(row) != 0 :
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, '//*[@inputprops="[object Object]"]')
            return 200, first_row_checkBox_element
        else:
            return 400, ""


