import sys
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from support.general_ui_utils.object.page_jump import PageJump
from support.ui_utils.read_data import ReadData
from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.random_name import *

class CreateObjects:


    def __init__(self,driver):
        self.driver = driver
        self.my_files = ReadData()
        self.my_random = RandomName()
        self.random_number = "test_" + self.my_random.random_number()
        self.random_name = self.my_random.random_name()
        self.object_info = {"id":"","name":"","details":"","ip":"","sub_type":"","description":"","subName":""}



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

            for i in range(len(data['item'])):
                if data['item'][i]['item_operation'] == 'new':
                    self.object_info["ip"] = self.object_info["details"] = data['item'][i]['item_value'][0]
                    for j in range(len(data['item'][i]['item_value'])):
                        if data['item'][i]['item_value'][j] != "null":
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_posXpath"]).send_keys(data['item'][i]['item_value'][j])
                            self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()

            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            time.sleep(3)
            self.object_info["id"] = self.driver.find_element(By.XPATH,"//div[@class='table-status-item-id']/span").text

            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400