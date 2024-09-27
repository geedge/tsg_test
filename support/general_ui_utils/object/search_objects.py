import time
from datetime import datetime

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from support.general_ui_utils.object.page_jump import PageJump
from support.ui_utils.read_data import ReadData
from support.general_ui_utils.element_position.object_element_position import *

class SearchObjects:

    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(5)

    def search(self,object_info,data,object_element_position):
        page_jump_element_position = object_element_position["page_jump"]

        # 打开该列表
        page_jump = PageJump(self.driver)
        time.sleep(0.5)
        page_jump.jump_sub_object_page(page_jump_element_position)
        search_types = data["search"]["type"].split('&')
        for search_type in search_types:
            search_value = self.get_search_value(object_info,search_type,data["search"]["is_fuzzy"])
            if search_type == "id":
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).click()
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value)
                self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Id_posXpath).click()
            elif search_type == "name":
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).click()
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value)
                self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Name_posXpath).click()
            elif search_type == "description":
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).click()
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value)
                self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Description_posXpath).click()
            elif search_type == "details":
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).click()
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value)
                self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Details_posXpath).click()
            elif search_type == "sub_type":
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).click()
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value)
                self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_subType_posXpath).click()
            elif search_type == 'sub_Name':
                # 删除Group下的sub mobile
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).click()
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value)
                self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Name_posXpath).click()
            elif search_type == "ip":
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).click()
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value)
                self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_IP_posXpath).click()
            elif "global" in search_type :
                self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(search_value + Keys.ENTER)
        self.driver.find_element(By.ID, mainPage_ObjectSearch_buttonSearch_posId).click()
        row = self.driver.find_elements(By.XPATH, "//div[contains(@class,'ly-table1')]//tbody/tr")
        if len(row) != 0:
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
            return 200, first_row_checkBox_element
        else:
            return 400, ""

    def get_search_value(self,object_info,search_type,fuzzy_type):
        if fuzzy_type == True:
            if search_type == "name":
                search_value = object_info["name"][5:]
            elif search_type == "description":
                search_value = object_info["description"][5:]
            elif search_type == "ip" or search_type == "details":
                ip_address = object_info["ip"].split('.')
                search_value = '.'.join(ip_address[-2:])
        else:
            if search_type == "id":
                search_value = object_info["id"]
            elif search_type == "name":
                search_value = object_info["name"]
            elif search_type == "description":
                search_value = object_info["description"]
            elif search_type == "details":
                search_value = object_info["details"]
            elif search_type == "sub_type":
                search_value = object_info["sub_type"]
            elif search_type == "ip":
                search_value = object_info["ip"]
            elif search_type == "global_name":
                search_value = object_info["name"]
            elif search_type == "global_description":
                search_value = object_info["description"]
            elif search_type == "global_ip":
                search_value = object_info["ip"]
            elif search_type == "global_details":
                search_value = object_info["details"]

        return search_value



