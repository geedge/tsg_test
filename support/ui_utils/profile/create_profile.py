import os
import sys
import time
from support.ui_utils.profile.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
import traceback
from support.ui_utils.profile.create_statistics_template import CreateStatisticsTemplate
from support.ui_utils.element_position.map_element_position_library import get_profile_element_position
from support.ui_utils.profile.create_hijack_profile import CreateHijackProfile
from support.ui_utils.profile.create_insert_profile import CreateInsertProfile
from support.ui_utils.profile.create_run_script_profile import CreateRunScriptProfile
from support.ui_utils.profile.create_response_page import CreateResponsePage
from datetime import datetime 

class CreateProfile:
    def __init__(self, driver):
        self.driver = driver

    def create(self, profile_data, profile_element_position):
        page_jump_element_position = profile_element_position["page_jump"]
        create_element_position = profile_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_profile_page(page_jump_element_position)
            # 点击create
            self.driver.find_element(By.ID, create_element_position["profileListPage_createButton_posId"]).click()
            if profile_data["profile_type"] == "response_page":  # response page创建
                self._create_response_page(profile_data["profile_file"])
            elif profile_data["profile_type"] == "statistics_template":  # response page创建
                self._create_statistics_template_page(profile_data["profile_file"])
            elif profile_data["profile_type"] == "hijack_file":    # hijack file 创建
                self._create_hijack_file(profile_data["profile_file"])
            elif profile_data["profile_type"] == "insert_script":    # insert script 创建
                self._create_insert_script(profile_data["profile_file"])
            elif profile_data["profile_type"] == "run_script":    # run script 创建
                self._create_run_script(profile_data["profile_file"])
            # 其它 profile创建
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            traceback.print_exc()
            return 400

    def _create_response_page(self, data):
        """
        resposne page 创建函数
        """
        Pl = CreateResponsePage(self.driver)
        Pl.create_response_page(data)

    def _create_hijack_file(self, data):
        # 新建hijack_file
        Pl = CreateHijackProfile(self.driver)
        Pl.create_hijack_file(data)

    def _create_insert_script(self, data):
        # 新建hijack_file
        Pl = CreateInsertProfile(self.driver)
        Pl.create_hijack_file(data)

    def _create_run_script(self, data):
        # 新建 run script
        Pl = CreateRunScriptProfile(self.driver)
        Pl.create_run_script_file(data)

    def _create_statistics_template_page(self, data):
        statistics_templates = data["statistics_template"]
        cond_status = 0
        for statistics_template in statistics_templates:
            # create_statistics_template = CreateProfile(driver)
            create_statistics_template = CreateStatisticsTemplate(self.driver)
            element_position_map = get_profile_element_position("statistics_template")
            cond_code = create_statistics_template.create(statistics_template, element_position_map)
            if cond_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} Profile successfully.".format("statistics_template"), flush=True)
            else:
                result = "Fail to create {} Profile.".format("statistics_template")
                cond_status = 1
                break
            if cond_status == 1:  # 创建失败，退出遍历创建
                break
        return cond_code


