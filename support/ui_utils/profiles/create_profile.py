import os
import sys
import time
from support.ui_utils.profiles.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
import traceback
from support.ui_utils.profiles.create_statistics_template import CreateStatisticsTemplate
from support.ui_utils.element_position.map_element_position_library import get_profile_element_position
from support.ui_utils.profiles.create_hijack_profile import CreateHijackProfile
from support.ui_utils.profiles.create_insert_profile import CreateInsertProfile
from support.ui_utils.profiles.create_run_script_profile import CreateRunScriptProfile
from support.ui_utils.profiles.create_response_page import CreateResponsePage
from support.ui_utils.profiles.create_ssl_decryption_keyring_profile import CreateSSLDecryptionKeyringProfile
from support.ui_utils.profiles.create_ssl_decryption_profile import CreateSSLDecryptionProfile
from support.ui_utils.profiles.create_tcp_proxy_profile import CreateTcpProxyProfile
from support.ui_utils.profiles.create_traffic_mirroring_profile import CreateMonitorProfile
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
            self.driver.find_element(By.XPATH, create_element_position["profileListPage_createButton_posXpath"]).click()
            if profile_data["profile_type"] == "response_page":  # response page创建
                self._create_response_page(profile_data["profile_file"])
            elif profile_data["profile_type"] == "statistics_template":  # response page创建
                self._create_statistics_template_page(profile_data)
            elif profile_data["profile_type"] == "hijack_file":    # hijack file 创建
                self._create_hijack_file(profile_data["profile_file"])
            elif profile_data["profile_type"] == "insert_script":    # insert script 创建
                self._create_insert_script(profile_data["profile_file"])
            elif profile_data["profile_type"] == "run_script":    # run script 创建
                self._create_run_script(profile_data["profile_file"])
            elif profile_data["profile_type"] == "ssl_keyring":    # ssl decrpytion keyring 创建
                self._create_run_ssl_decryption_keyring(profile_data["profile_file"])
            elif profile_data["profile_type"] == "ssl_decryption":    # ssl decrpytion profile 创建
                self._create_run_ssl_decryption_profile(profile_data["profile_file"])
            elif profile_data["profile_type"] == "tcp_option":  # tcp proxy 创建
                self._create_run_tcp_proxy_profile(profile_data["profile_file"])
            elif profile_data["profile_type"] == "traffic_mirror":  # traffic mirror 创建
                self._create_traffic_mirroring_profile(profile_data["profile_file"])
            # 其它 profile创建
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            raise

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

    def _create_run_ssl_decryption_keyring(self, data):
        # 新建 ssl_decryption_keyring
        Pl = CreateSSLDecryptionKeyringProfile(self.driver)
        Pl.create_ssl_decryption_keyring_file(data)

    def _create_run_ssl_decryption_profile(self, data):
        # 新建 ssl_decryption_proile
        Pl = CreateSSLDecryptionProfile(self.driver)
        Pl.create_ssl_decryption_file(data)

    def _create_run_tcp_proxy_profile(self, data):
        # 新建 tcp_proxy_profile
        Pl = CreateTcpProxyProfile(self.driver)
        Pl.create_tcp_proxy_profile(data)

    def _create_traffic_mirroring_profile(self, data):
        # 新建 tcp_proxy_profile
        Pl = CreateMonitorProfile(self.driver)
        Pl.create_traffic_mirroring_profile(data)

    def _create_statistics_template_page(self, data):
        cond_code = 0
        # create_statistics_template = CreateProfile(driver)
        if data != None and len(data) >= 0:
            create_statistics_template = CreateStatisticsTemplate(self.driver)
            element_position_map = get_profile_element_position("statistics_template")
            cond_code = create_statistics_template.create(data, element_position_map)
        return cond_code


