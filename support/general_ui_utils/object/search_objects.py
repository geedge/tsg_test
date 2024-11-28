import random
import time
from datetime import datetime

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.random_name import *
from support.general_ui_utils.object.page_jump import PageJump
# from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.element_position.object_element_position import *

class SearchObjects:

    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.my_random = RandomName()

    def search(self,object_info,search,object_element_position):
        try:
            page_jump_element_position = object_element_position["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            time.sleep(0.5)
            page_jump.jump_sub_object_page(page_jump_element_position)
            search_types = search["type"].split('&')
            for search_type in search_types:
                search_value = self.get_search_value(object_info,search_type,search["is_fuzzy"])
                if search_type == "uuid":
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).click()
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH, objectListPage_search_select_Id_posXpath).click()
                elif search_type == "name":
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).click()
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH, objectListPage_search_select_Name_posXpath).click()
                elif search_type == "description":
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).click()
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH, objectListPage_search_select_Description_posXpath).click()
                elif search_type == "details":
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).click()
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH, objectListPage_search_select_Details_posXpath).click()
                elif search_type == "sub_type":
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).click()
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH, objectListPage_search_select_subType_posXpath).click()
                elif search_type == 'sub_name':
                    # 删除Group下的sub mobile
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).click()
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH, objectListPage_search_select_Name_posXpath).click()
                elif search_type == "ip":
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).click()
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH, objectListPage_search_select_IP_posXpath).click()
                elif "global" in search_type :
                    self.driver.find_element(By.XPATH,ipObjectListPage_searchLabel_posXpath).send_keys(search_value)
                    self.driver.find_element(By.XPATH,listPage_objectSearch_ip_address_select_Search_posXpath).click()
            # self.driver.find_element(By.XPATH, mainPage_objectSearch_buttonSearch_posXpath).click()
            # time.sleep(0.5)
            # row = self.driver.find_elements(By.XPATH, "//div[@class='MuiDataGrid-virtualScrollerContent css-0']/div/div")
            # if len(row) != 0:
            #     first_row = row[0]
            #     first_row_checkBox_element = first_row.find_element(By.XPATH, '//input[@aria-label="Select row"]')
                return 200
        except Exception as e:
            raise


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
            if search_type == "uuid":
                search_value = object_info["uuid"]
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

    def get_objects_uuid(self,name,object_element_position):
        try:
            page_jump_element_position = object_element_position["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            time.sleep(0.5)
            page_jump.jump_sub_object_page(page_jump_element_position)
            time.sleep(3)
            self.driver.find_element(By.XPATH, ipObjectListPage_searchLabel_posXpath).click()
            self.driver.find_element(By.XPATH, ipObjectListPage_searchLabel_posXpath).send_keys(name)
            self.driver.find_element(By.XPATH, objectListPage_search_select_Name_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_objectSearch_buttonSearch_posXpath).click()
            time.sleep(2)
            # 展示所有列获取uuid
            column_setting_btn = self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath)  # 列设置按钮
            self.driver.execute_script("arguments[0].scrollIntoView();", column_setting_btn)
            column_setting_btn.click()  # 点击列设置
            self.driver.find_element(By.XPATH, '//span[text()="UUID"]').click()
            self.driver.find_element(By.XPATH, '//div[text()="Name"]').click()
            object_uuid = self.driver.find_element(By.XPATH, '//div[@aria-rowindex="2"]//div[@data-field="uuid"]').text
            description = self.driver.find_element(By.XPATH,'//div[@aria-rowindex="2"]//div[@data-field="description"]').text
            return 200,object_uuid, description
        except Exception as e:
            raise

    def get_first_object(self,uuid,object_element_position):
        try:
            page_jump_element_position = object_element_position["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            time.sleep(0.5)
            page_jump.jump_sub_object_page(page_jump_element_position)
            time.sleep(3)
            self.driver.find_element(By.XPATH, ipObjectListPage_searchLabel_posXpath).click()
            self.driver.find_element(By.XPATH, ipObjectListPage_searchLabel_posXpath).send_keys(uuid)
            self.driver.find_element(By.XPATH, objectListPage_search_select_Id_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_objectSearch_buttonSearch_posXpath).click()
            time.sleep(2)
            row = self.driver.find_elements(By.XPATH,"//div[@class='MuiDataGrid-virtualScrollerContent css-0']/div/div")
            if len(row) != 0:
                first_row = row[0]
                first_row_checkBox_element = first_row.find_element(By.XPATH, '//input[@aria-label="Select row"]')
                return 200, first_row_checkBox_element
        except Exception as e:
            raise
    # def main_page_item_search(self,object_info):
    #     try:
    #         self.driver.find_element(By.XPATH,listPage_item_search_details_first_posXpath).click()
    #         self.driver.find_element(By.XPATH, listPage_item_search_text_posXpath).click()
    #         if object_info["sub_type"] == "ip":
    #             item_search_type = random.choice(["IP","Port"])
    #             self.driver.find_element(By.XPATH,f"//div[@class='select_info_list']/ul/li[normalize-space(text())='{item_search_type}']").click()
    #             if item_search_type == "IP":
    #                 search_value = object_info["ip"]
    #             elif item_search_type == "Port":
    #                 search_value = random.randint(0,65535)
    #         else:
    #             pass
    #         # 首先进行错误搜索校验
    #         self.driver.find_element(By.XPATH, listPage_item_search_text_posXpath).send_keys(self.my_random.random_number() + Keys.ENTER)
    #         assert self.driver.find_element(By.XPATH, listPage_item_search_total_text_posXpath).text == "Total:0"
    #         # 正确校验
    #         self.driver.find_element(By.XPATH, listPage_item_search_text_posXpath).clear()
    #         self.driver.find_element(By.XPATH, listPage_item_search_text_posXpath).send_keys(str(search_value) + Keys.ENTER)
    #         assert self.driver.find_element(By.XPATH,listPage_item_search_total_text_posXpath).text != "Total:0", "搜索结果错误"
    #         self.driver.find_element(By.XPATH,listPage_item_search_close_posXpath).click()
    #         return 200
    #     except Exception as e:
    #         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
    #         return 400

