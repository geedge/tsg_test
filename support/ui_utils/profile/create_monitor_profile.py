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


class CreateProfile():
    def __init__(self, driver, monitor_profile_element_position):
        self.driver = driver
        self.page_jump_element_position = monitor_profile_element_position["page_jump"]
        self.create_element_position = monitor_profile_element_position["create"]

    def create_monitor_profile(self, data, monitor_profile_element_position,source_name):
        page_jump_element_position = monitor_profile_element_position["page_jump"]
        create_element_position = monitor_profile_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_profile_page(page_jump_element_position,"UIwithTrafficTestVsys")
            self.driver.find_element(By.ID, create_element_position["profileListPage_createButton_posId"]).click()
            # 在create 创建页面操作
            self.my_random = RandomName()
            if source_name:
                self.random_name = source_name
                self.driver.find_element(By.ID, create_element_position["profilePage_inputName_posId"]).send_keys(self.random_name)
            else:
                self.random_name = self.my_random.random_name()
                self.driver.find_element(By.ID,create_element_position["profilePage_inputName_posId"] ).send_keys(self.random_name)
            # 解析输入的vlan id数据
            #self.process_vlan_ids(data)
            elements_vlan_ids_input = self.driver.find_element(By.XPATH, self.create_element_position["trafficMirroringProfiles_input_vlanIdsInput_posXpath"])
            var = data["vlan_id"]
            elements_vlan_ids_input.send_keys(int(var))
            # 点击OK
            self.driver.find_element(By.CSS_SELECTOR, create_element_position["profilePage_button_oK_posCss"]).click()
            self.driver.find_element(By.CSS_SELECTOR, self.create_element_position["profilePage_button_warningSaveYes_posCss"]).click()

            # self.validate_after_ok(self,self.random_name)
            # if "reverse_case" in data.keys():  # 其它字符输入用例判断使用
            #     if data["reverse_case"] == "other_chars":
            #         execpt_info = "Please enter the integer"
            #         actual_info = self.driver.find_element(By.XPATH, "//div[@class='el-form-item__error']").text.strip()
            #         print(actual_info)
            #         pytest_check.equal(execpt_info, actual_info,msg="所在行数{}".format(inspect.currentframe().f_lineno))
            #         return 999
            return 200
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
            print(str(e))
            return 400





    def process_vlan_ids(self,data):
        vlan_ids = data["vlan_id"]
        vlan_ids_create = []  # 创建的vlan id
        for i in vlan_ids:
            if i.strip().split("->")[0] != "":
                vlan_ids_create.append(i.strip().split("->")[0])
        # 循环输入vlan id
        if len(vlan_ids_create) > 32:
            print("vlan id 数据超出32个，仅保留前32个")
            vlan_ids_create = vlan_ids_create[:32]
        for j in range(len(vlan_ids_create)):
            # 输入ipnut
            elements_vlan_ids_input = self.driver.find_elements(By.XPATH,self.create_element_position["trafficMirroringProfiles_input_vlanIdsInput_posXpath"])
            for element_vlan_id in elements_vlan_ids_input:
                if element_vlan_id.get_attribute("value") == "":  # 创建时，只是往input.value=none中键入数据
                    element_pos_by_id = element_vlan_id.get_attribute("id")
                    self.driver.find_element(By.ID, element_pos_by_id).send_keys(vlan_ids_create[j])  # 输入vlan id的值
                    self.driver.find_element(By.XPATH, "//label[text()='VLAN ID']").click()
                    if "reverse_case" in data.keys():  # 其它字符判断条件使用
                        error_vlan_id = ""
                        pass
                    else:
                        if int(vlan_ids_create[j]) < 3 or int(vlan_ids_create[j]) > 66:  # vlan id 不在正确范围内
                            # element_vlan_id.find_element(By.XPATH, "/ancestor::div[@class='el-form-item__content']/div[@class='el-form-item__error']")
                            # assert element_vlan_id.element_isExist(By.XPATH, "/ancestor::div[@class='el-form-item__content']/div[@class='el-form-item__error']")
                            error_content = self.driver.find_element(By.XPATH,
                                                                     f"//input[@id='{element_pos_by_id}']//ancestor::div[@class='el-form-item__content']/div[@class='el-form-item__error']").text.strip()
                            pytest_check.equal(error_content, "Range:3-66",
                                               msg="所在行数{}".format(inspect.currentframe().f_lineno))
                            error_vlan_id = element_pos_by_id
                        elif vlan_ids_create[:j + 1].count(vlan_ids_create[j]) > 1:  # 判断是否为重复项
                            error_content = self.driver.find_element(By.XPATH,
                                                                     f"//input[@id='{element_pos_by_id}']//ancestor::div[@class='el-form-item__content']/div[@class='el-form-item__error']").text.strip()
                            pytest_check.equal(error_content, "The VLAN ID cannot repeat",
                                               msg="所在行数{}".format(inspect.currentframe().f_lineno))
                            error_vlan_id = element_pos_by_id
                        else:
                            error_vlan_id = ""
                    break
            if (len(vlan_ids_create) - 1) - j > 0:  # 点击add按钮比数据个数少一次
                self.driver.find_element(By.CSS_SELECTOR,
                                         trafficMirroringProfiles_button_vlanIdAdd_posCss).click()  # 点击add添加
            if error_vlan_id != "":
                print("error_vlan_id=", error_vlan_id)
                element_vlan_del = self.driver.find_element(By.XPATH,
                                                            f"//input[@id='{error_vlan_id}']/ancestor::div[@class='el-form-item__content']/i")
                # print("element_vlan_del_style=", element_vlan_del.get_attribute("style"))
                if element_vlan_del.get_attribute("style") != "display: none;":
                    element_vlan_del.click()
                elif element_vlan_del.get_attribute("style") == "display: none;":
                    self.driver.find_element(By.ID, error_vlan_id).send_keys(Keys.CONTROL + "a")
                    self.driver.find_element(By.ID, error_vlan_id).send_keys(Keys.BACKSPACE)


    def validate_after_ok(self,name):
        try:
            # 如果名称长度小于4，检查错误消息并取消操作
            if len(name) < 4:
                error_message = "The length of the name is at most 128 characters and cannot be less than 4 characters"
                if self.driver.element_isExist(By.XPATH,
                                          "//label[text()='Name']/parent::div//div[@class='el-form-item__error']"):
                    print(error_message)
                    actual_error = self.driver.find_element(By.XPATH, "//div[@class='el-form-item__error']").text.strip()
                    assert error_message == actual_error, "Error message does not match expected"

                    # 点击取消
                    self.driver.find_element(By.CSS_SELECTOR,self.create_element_position["profilePage_button_oK_posCss"] ).click()

                    # 点击警告保存确认
                    self.driver.find_element(By.CSS_SELECTOR, self.create_element_position["profilePage_button_warningSaveYes_posCss"]).click()
                    return False
                else:
                    print("name less than 4，no error message")
                    return False

            # 检查是否未输入必填项
            if self.driver.element_isExist(By.XPATH, "//div[contains(text(),'Please enter the content')]"):
                error_message = self.driver.find_element(By.XPATH,"//div[contains(text(),'Please enter the content')]").text.strip()
                print("未输入必填项，报错：", error_message)

                # 点击取消
                self.driver.find_element(By.CSS_SELECTOR, self.create_element_position[ "profilePage_button_oK_posCss"]).click()

                # 点击警告保存确认
                self.driver.find_element(By.CSS_SELECTOR, self.create_element_position["profilePage_button_warningSaveYes_posCss"]).click()
                return False

            # 如果数据正确，点击警告保存确认按钮
            if self.driver.element_isExist(By.CSS_SELECTOR, self.create_element_position["profilePage_button_warningSaveYes_posCss"]):
                self.driver.find_element(By.CSS_SELECTOR, self.create_element_position["profilePage_button_warningSaveYes_posCss"]).click()
                return True

        except NoSuchElementException as e:
            print("Element not found: ", e)
            return False



