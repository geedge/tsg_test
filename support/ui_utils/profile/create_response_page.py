import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *

class CreateResponsePage():
    def __init__(self, driver):
        self.driver = driver

    def create_response_page(self, data):
        """
        resposne page 创建函数
        """
        # 在create resposne page页面操作
        profile_name = data["name"]
        self.driver.find_element(By.ID, responsePage_input_Name_posId).clear()
        self.driver.find_element(By.ID, responsePage_input_Name_posId).send_keys(profile_name)
        # 上传文件
        create_file = data["file"].split("->")[0]  # 提取上传文件绝对路径
        profile_path = os.path.dirname(os.path.abspath(__file__))  # ...support\ui_utils\profile
        file_abs = os.path.join(profile_path, "profile_file", "response_pages", create_file)
        # 打印出文件路径
        # print(create_file)
        # print(profile_path)
        # print(resposne_file_abs)
        self.driver.find_element(By.XPATH, responsePage_input_file_posXpath).send_keys(file_abs)
        self.driver.find_element(By.CSS_SELECTOR, responsePage_button_oK_posCss).click()
        if self.driver.element_isExist(By.CSS_SELECTOR, responsePage_button_warningSaveYes_posCss):
            self.driver.find_element(By.CSS_SELECTOR, responsePage_button_warningSaveYes_posCss).click()
        time.sleep(3)
        return profile_name

