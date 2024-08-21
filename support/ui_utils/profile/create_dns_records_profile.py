# import os
import inspect
import sys
import time
import traceback
import pytest_check

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.profile.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *

import re
import random
import copy

from support.ui_utils.random_name import RandomName
from datetime import datetime 

class CreateProfile():
    def __init__(self, driver, secy_dnsRecords_profile_element_position):
        self.driver = driver
        self.page_jump_element_position = secy_dnsRecords_profile_element_position["page_jump"]
        self.create_element_position = secy_dnsRecords_profile_element_position["create"]

    def create_dns_records_profile(self, data, secy_dnsRecords_profile_element_position,source_name):
        page_jump_element_position = secy_dnsRecords_profile_element_position["page_jump"]
        create_element_position = secy_dnsRecords_profile_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_profile_page(page_jump_element_position)
            self.driver.find_element(By.ID, create_element_position["profileListPage_createButton_posId"]).click()
            # 在create 创建页面操作
            self.my_random = RandomName()
            if source_name:
                self.random_name = source_name
                self.driver.find_element(By.ID, create_element_position["profilePage_inputName_posId"]).send_keys(self.random_name)
            else:
                self.random_name = self.my_random.random_name()
                self.driver.find_element(By.ID,create_element_position["profilePage_inputName_posId"] ).send_keys(self.random_name)
            # 选择Type
            if data['type'] == 'A':
                self.driver.find_element(By.ID, create_element_position["profilePage_Type_A_posId"]).click()
            elif data['type'] == 'AAAA':
                self.driver.find_element(By.ID, create_element_position["profilePage_Type_AAAA_posId"]).click()
            elif data['type'] == 'CNAME':
                self.driver.find_element(By.ID, create_element_position["profilePage_Type_CNAME_posId"]).click()
            # 只有1个item，直接输入
            if len(data['items']) == 1:
                self.driver.find_element(By.XPATH, create_element_position["dnsRecordsProfiles_input_item_posXpath"]).send_keys(data['items'][0])
                #点击保存
                temp_element_position = create_element_position["dnsRecordsProfile_save_item_posXpath"].format(replaceName=str(0))
                self.driver.find_element(By.ID, temp_element_position).click()
            # 点击OK
            self.driver.find_element(By.CSS_SELECTOR, create_element_position["profilePage_button_oK_posCss"]).click()
            self.driver.find_element(By.CSS_SELECTOR, self.create_element_position["profilePage_button_warningSaveYes_posCss"]).click()

            
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
            traceback.print_exc()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], str(e))
            return 400




