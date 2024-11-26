import time
from datetime import datetime
from selenium.webdriver.common.by import By

from support.ui_utils.element_position.map_element_position_library import get_element_position
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.object.page_jump import PageJump
from support.ui_utils.object.search_objects_example import SearchObjects
class DeleteObjects:

    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(5)

    def delete(self,parmameter,objects_tuple):
        try:
            for object in objects_tuple:
                element_position_library = get_element_position(object["type"])
                delete_element_position = element_position_library["delete"]
                page_jump_element_position = element_position_library["page_jump"]
                search_element_position = element_position_library["search"]
                page_jump = PageJump(self.driver)
                time.sleep(0.5)
                page_jump.jump_sub_object_page(page_jump_element_position)
                time.sleep(3)
                self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"]).click()
                self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"]).send_keys(object["uuid"])
                self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_selectID_posXpath"]).click()
                self.driver.find_element(By.XPATH,search_element_position["objectListPage_search_button_posXpath"]).click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, '(//input[@aria-label="Select row"])[1]').click()
                #点击删除按钮
                self.driver.find_element(By.XPATH, delete_element_position["objectListPage_deleteButton_posXpath"]).click()
                self.driver.find_element(By.XPATH,delete_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
                time.sleep(3)
                return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400

    def delete_sub_object(self,object_element_position,first_row_checkbox_element):
        delete_element_position = object_element_position["delete"]
        try:
            first_row_checkbox_element.click()
            self.driver.find_element(By.ID, delete_element_position["objectListPage_deleteButton_posId"]).click()
            self.driver.find_element(By.XPATH,delete_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(3)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",
                  flush=True)
            return 400