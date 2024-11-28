import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *

class CreateResponsePage:
    def __init__(self, driver):
        self.driver = driver

    def create_response_page(self, policy_configuration):
        """
        resposne page 创建函数
        """
        # 在create resposne page页面操作
        data = policy_configuration["action_parameter"]
        profile_name = data["html_profile"]["name"]
        self.driver.find_element(By.XPATH, responsePage_input_Name_posXpath).clear()
        self.driver.find_element(By.XPATH, responsePage_input_Name_posXpath).send_keys(profile_name)
        # 上传文件
        create_file = data["html_profile"]["file_path"]  # 提取上传文件绝对路径
        root_path = policy_configuration["parameter"]["root_path"]# ...support/configuration_management/profile
        file_abs = os.path.join(root_path, "support" ,"configuration_management", "profile", create_file)
        self.driver.find_element(By.XPATH, responsePage_input_file_posXpath).send_keys(file_abs)
        self.driver.find_element(By.XPATH, responsePage_button_oK_posXpath).click()
        if self.driver.is_element_exist_by_value(By.XPATH, responsePage_button_warningSaveYes_posXpath):
            self.driver.find_element(By.XPATH, responsePage_button_warningSaveYes_posXpath).click()
        time.sleep(3)
        return profile_name

