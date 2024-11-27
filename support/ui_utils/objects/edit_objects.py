import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.objects.page_jump import PageJump
from datetime import datetime 

class EditObject:
    def __init__(self, driver):
        self.driver = driver
        
    def edit(self, name, object_element_position, vsys_name=""):
        try:
            edit_element_position = object_element_position["search"]
            page_jump_element_position = object_element_position["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            self.driver.find_element(By.ID, edit_element_position["objectListPage_searchLabel_posId"]).send_keys(name)
            self.driver.find_element(By.XPATH, edit_element_position["objectListPage_searchLabel_selectName_posXpath"]).click()
            self.driver.find_element(By.ID, mainPage_objectSearch_buttonSearch_posXpath).click()
            time.sleep(10)
            all_button_position = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
            self.driver.find_element(By.XPATH, all_button_position).click()
            edit_button_position = "appEdit-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"
            self.driver.find_element(By.ID, edit_button_position).click()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "todo")
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            #return 400
