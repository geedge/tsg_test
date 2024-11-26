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

    def delete(self,object_tuple,first_row_checkbox_element):
        try:
            for obj in object_tuple:
                element_position_library = get_element_position(obj["type"])
                delete_element_position = element_position_library["delete"]
                first_row_checkbox_element.click()
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