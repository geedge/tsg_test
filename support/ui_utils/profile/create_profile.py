import os
import sys
import time
from support.ui_utils.profile.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
import traceback
from support.ui_utils.profile.create_statistics_template import *
from support.ui_utils.element_position.map_element_position_library import *

class CreateProfile():
    def __init__(self, driver):
        self.driver = driver

    def create(self, profile_data, profile_element_position):
        page_jump_element_position = profile_element_position["page_jump"]
        create_element_position = profile_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击create
            self.driver.find_element(By.ID, create_element_position["profileListPage_createButton_posId"]).click()
            if profile_data["profile_type"] == "response_page":  # response page创建
                self._create_response_page(profile_data["profile_file"])
            elif profile_data["profile_type"] == "statistics_template":  # response page创建
                self._create_statistics_template_page(profile_data["profile_file"])
            # 其它 profile创建
            return 200
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 400

    def _create_response_page(self, data):
        """
        resposne page 创建函数
        """
        # 在create resposne page页面操作
        profile_name = data["name"]
        self.driver.find_element(By.ID, responsePage_input_Name_posId).clear()
        self.driver.find_element(By.ID, responsePage_input_Name_posId).send_keys(profile_name)
        # 上传文件
        create_file = data["file"].split("->")[0]  # 提取上传文件绝对路径
        profile_path = os.path.dirname(os.path.abspath(__file__))    #  ...support\ui_utils\profile
        resposne_file_abs = os.path.join(profile_path, "profile_file", "response_pages", create_file)
        # 打印出文件路径
        # print(create_file)
        # print(profile_path)
        # print(resposne_file_abs)
        self.driver.find_element(By.XPATH, responsePage_input_file_posXpath).send_keys(resposne_file_abs)
        self.driver.find_element(By.CSS_SELECTOR, responsePage_button_oK_posCss).click()
        if self.driver.element_isExist(By.CSS_SELECTOR, responsePage_button_warningSaveYes_posCss):
            self.driver.find_element(By.CSS_SELECTOR, responsePage_button_warningSaveYes_posCss).click()
        time.sleep(3)
        return profile_name

    def _create_statistics_template_page(self, data):
        statistics_templates = data["statistics_template"]
        cond_status = 0
        for statistics_template in statistics_templates:
            # create_statistics_template = CreateProfile(driver)
            create_statistics_template = CreateStatisticsTemplate(self.driver)
            element_position_map = get_profile_element_position("statistics_template")
            cond_code = create_statistics_template.create(statistics_template, element_position_map)
            if cond_code == 200:
                print("Create {} Profile successfully.".format("statistics_template"))
            else:
                result = "Fail to create {} Profile.".format("statistics_template")
                cond_status = 1
                break
            if cond_status == 1:  # 创建失败，退出遍历创建
                break
        return cond_code
