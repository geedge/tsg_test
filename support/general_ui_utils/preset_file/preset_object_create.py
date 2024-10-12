import sys
import time
from datetime import datetime

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from support.general_ui_utils.object.page_jump import PageJump
from support.ui_utils.read_data import ReadData
from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.random_name import *

class PresetObjectCreate():

    def __init__(self,driver):
        self.driver = driver
        self.my_random = RandomName()
        self.random_name = self.my_random.random_name()
        self.object_info = {"id": "", "name": "", "details": "", "ip": "", "sub_type": "", "description": "",
                            "subName": "", "operation": "", "object_exit": False}

        self.ip_test_data = {
            "type": "objects",
            "name": "create_ip_four_group_nest",
            "case_type": "single",
            "object_type": "ip",
            "object_operation": {
                "create": [
                    {
                        "item_operation": "add",
                        "item_type": "",
                        "item_value": ["1.1.1.1"]
                    },
                ]
            },
            "search": {
                "is_fuzzy": False,
                "type": "id"
            },
            "statistics": "",  # random
            "audit_log": False  # system
        }

    def create(self,object_type,object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
        data = []
        if object_type == "ip":
            data = self.ip_test_data

        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击create
            self.driver.find_element(By.ID, create_element_position["objectListPage_createButton_posId"], find_after_wait_time=0.5).click()
            self.driver.find_element(By.ID, create_element_position["objectListPage_dropDown_createButton_posId"]).click()
            time.sleep(1)
            # 输入name
            if data["name"] == "random":
                self.object_info["name"] = object_name = self.my_random.random_name()
            else:
                self.object_info["name"] = object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            self.object_info["description"] = object_description = self.random_name
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputDescription_posXpath"]).send_keys(object_description)

            if data['object_type'] == 'ip':
                self.object_info["sub_type"] = "ip"
                self.driver.find_element(By.ID, create_element_position["objectPage_ipType_posId"]).click()
            elif data['object_type'] == 'ip_learning':
                self.object_info["sub_type"] = "ip_learning"
                self.driver.find_element(By.ID, create_element_position["objectPage_ipLearing_type_posId"]).click()
                self.driver.find_element(By.XPATH, ip_addressObjectPage_button_IP_learn_from_protocols_posXpath).click()
                for learn_from_protocols in data['learn_from_protocols']:
                    if learn_from_protocols == "HTTP":
                        self.driver.find_element(By.XPATH,ip_addressObjectPage_button_IP_learn_from_protocols_Select_HTTP_posXpath).click()
                    elif learn_from_protocols == "SSL":
                        self.driver.find_element(By.XPATH,ip_addressObjectPage_button_IP_learn_from_protocols_Select_SSL_posXpath).click()
                self.driver.find_element(By.XPATH,ip_addressObjectPage_button_IP_learn_from_protocols_up_posXpath).click()
                self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Input_Aging_Times_posXpath).send_keys(data['aging_times'])
                self.driver.find_element(By.XPATH,ip_addressObjectPage_button_Input_Vote_Clients_Number_posXpath).send_keys(data['vote_clients_Number'])
                self.driver.find_element(By.XPATH,ip_addressObjectPage_button_Input_Learned_IP_Limits_posXpath).send_keys(data['learned_ip_limits'])
                self.driver.find_element(By.XPATH, '//div/span[contains(text(),"seconds")]').click()
            for i in range(len(data["object_operation"]['create'])):
                if data["object_operation"]['create'][i]['item_operation'] == 'add':
                    self.object_info["ip"] = self.object_info["details"] = data["object_operation"]['create'][i]['item_value'][0]
                    for j in range(len(data["object_operation"]['create'][i]['item_value'])):
                        if data["object_operation"]['create'][i]['item_value'][j] != "null":
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_posXpath"]).send_keys(data["object_operation"]['create'][i]['item_value'][j])
                            self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()
                            if data["object_operation"]['create'][i]["item_type"] == "error_item":
                                self.error_item_tips = self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_error_tips_posXpath"]).text
                                assert self.error_item_tips == create_element_position["error_tips_text"], "错误item的提示"
                                return 200
                elif data["object_operation"]['create'][i]['item_operation'] == 'import':
                    self.is_import = True
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_importItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH,create_element_position["importPage_uploadFile_posXpath"]).send_keys(self.my_files._obj_files_path(file_name=data["object_operation"]['create'][i]['item_value']))
                    if data["object_operation"]['create'][0]['item_type'] == "files_error_type":
                        assert self.driver.find_element(By.XPATH,main_Import_Mobile_Identity_files_error_type_posXpath).text == "Only txt formats can be uploaded", "断言错误提示"
                    time.sleep(10)

            # 修改Statistics统计状态
            if data["statistics"] != "":
                self.driver.find_element(By.XPATH, ObjectDetailPage_statistics_select_box_posXpath).click()
                if data["statistics"] == "elaborate":
                    self.driver.find_element(By.XPATH,
                                             ObjectDetailPage_statistics_select_elaborate_posXpath).click()
                elif data["statistics"] == "brief":
                    self.driver.find_element(By.XPATH,ObjectDetailPage_statistics_select_brief_posXpath).click()

            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            time.sleep(3)
            self.object_info["id"] = self.driver.find_element(By.XPATH,"//div[@class='table-status-item-id']/span").text
            self.object_info["object_exit"] = True
            # # 确认创建
            # if self.is_import == True:
            #     if "error_item" in data['item'][0]['item_value']:
            #         assert self.driver.find_element(By.XPATH,main_Import_files_error_format_posXpath).text == "IP addresses format error", "错误item校验"
            #     else:
            #         self.driver.find_element(By.XPATH,create_element_position["objectPage_import_ok_button_posXpath"]).click()
            #
            # self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            # self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            #获取Object ID
            # time.sleep(1)
            # self.object_info["id"] = self.driver.find_element(By.XPATH,"//div[@class='table-status-item-id']/span").text
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400
