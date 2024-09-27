import sys
import time
from datetime import datetime

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from support.general_ui_utils.object.page_jump import PageJump
from support.ui_utils.read_data import ReadData
from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.random_name import *

class CreateObjects:


    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.my_files = ReadData()
        self.my_random = RandomName()
        self.random_number = "test_" + self.my_random.random_number()
        self.random_name = self.my_random.random_name()
        self.object_info = {"id":"","name":"","details":"","ip":"","sub_type":"","description":"","subName":"","operation":"","object_exit":False}
        self.is_import = False
        self.is_group = False


    def create(self,data,object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
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

            self.confirm_creation(data, create_element_position)
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


    def create_group(self,data,object_element_position):
        self.is_group = True
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击create group
            self.driver.find_element(By.ID, create_element_position["objectListPage_createButton_posId"]).click()
            if data['object_type'] == "ApplicationGroup":
                pass
            else:
                self.driver.find_element(By.ID, create_element_position["objectListPage_dropDown_createGroupButton_posId"]).click()
            # 输入name
            self.object_info["name"] = object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            # 点subordinate的+
            self.driver.find_element(By.XPATH,create_element_position["groupObjectPage_addSubordinate_posXpath"]).click()
            if data["select_type"] == True:
                pass
            else:
                #点击侧滑框+
                # self.driver.find_element(By.XPATH,ip_address_Group_sub_Object_addButton_posXpath).click()  # 添加sub_Object
                self.driver.find_element(By.XPATH,ip_address_Group_sub_Object_add_new_Button_posXpath).click()  # add new sub_object
                self.driver.find_element(By.XPATH,ip_address_Group_sub_Object_add_new_Select_one_Button_posXpath).click()  # new mobile_Identities
                self.driver.find_element(By.XPATH,ip_address_Group_sub_Object_add_new_one_inputName_posXpath).send_keys(object_name)
                #添加item
                for i in range(len(data["object_operation"]['create'])):
                    if data["object_operation"]['create'][i]['item_operation'] == 'add':
                        self.object_info["ip"] = self.object_info["details"] = data["object_operation"]['create'][i]['item_value'][0]
                        for j in range(len(data["object_operation"]['create'][i]['item_value'])):
                            if data["object_operation"]['create'][i]['item_value'][j] != "null":
                                self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                                self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"]).send_keys(data["object_operation"]['create'][i]['item_value'][j])
                                self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
                    elif data['item'][i]["item_type"] == "quote":
                        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_buttonSearch_Item_posXpath).send_keys(data['Create']['sub_name'] + Keys.ENTER)
                        self.driver.find_element(By.XPATH,main_Group_sub_Object_input_frame_select_one_posXpath).click()
                    elif data["object_operation"]['create'][i]['item_operation'] == 'import':
                        self.is_import = True
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_importItem_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["importPage_uploadFile_posXpath"]).send_keys(self.my_files._obj_files_path(file_name=data["object_operation"]['create'][i]['item_value']))
                        time.sleep(5)
            self.confirm_creation(data,create_element_position)
            # self.driver.find_element(By.XPATH,create_element_position["groupObjectPage_subObject_OK_button_posXpath"]).click()
            # self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_subObject_OK_Warning_Yes_posXpath"]).click()
            # #Group页面确认
            # self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            # self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            # 获取Object ID
            # time.sleep(1)
            # self.object_info["id"] = self.driver.find_element(By.XPATH,"//div[@class='table-status-item-id']/span").text
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", file=sys.stderr, flush=True)
            return 400

    def confirm_creation(self,data,create_element_position):
        if self.is_group == False:
            if self.is_import == True:
                if data["object_operation"]['create'][0]['item_type'] == "files_error_item" or data["object_operation"]['create'][0]['item_type'] == "files_error_format":
                    assert self.driver.find_element(By.XPATH,main_Import_files_error_format_posXpath).text == "IP addresses format error", "错误item校验"
                elif  data["object_operation"]['create'][0]['item_type'] == "true_files":
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_import_ok_button_posXpath"]).click()
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
                    time.sleep(3)
                    self.object_info["id"] = self.driver.find_element(By.XPATH,"//div[@class='table-status-item-id']/span").text
                    self.object_info["object_exit"] = True
            elif len(data['name']) < 4:
                self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
                self.Name_tip = self.driver.find_element(By.XPATH, main_ObjectPage_tips_Name_input_Xpath).text
                assert self.Name_tip == "The length of the name is at most 128 characters and cannot be less than 4 characters", "Name字符不符合要求"
            elif data["object_operation"]['create'][0]['item_value'][0] == "null":
                self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
                self.alert_tip = self.driver.find_element(By.XPATH,main_Import_Mobile_Identity_files_error_type_posXpath).text
                assert self.alert_tip == "Item of policy object and referenced sub-objects cannot be empty at the same time"
            else: #正常添加item点击OK创建
                self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
                self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
                time.sleep(3)
                self.object_info["id"] = self.driver.find_element(By.XPATH,"//div[@class='table-status-item-id']/span").text
                self.object_info["object_exit"] = True
        elif self.is_group == True:
            #subObject页面点击OK创建
            self.driver.find_element(By.XPATH,create_element_position["groupObjectPage_subObject_OK_button_posXpath"]).click()
            self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_subObject_OK_Warning_Yes_posXpath"]).click()
            # Group页面确认
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            time.sleep(1)
            self.object_info["id"] = self.driver.find_element(By.XPATH,"//div[@class='table-status-item-id']/span").text
            self.object_info["object_exit"] = True



