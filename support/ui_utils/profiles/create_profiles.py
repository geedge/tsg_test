import os
import sys
import time
from support.ui_utils.profiles.page_jump import PageJump
from selenium.webdriver.common.by import By
from datetime import datetime
from support.ui_utils.profiles.create_response_page import CreateResponsePage
from support.ui_utils.profiles.create_dns_resource_record import CreateDnsResourceReccord
from support.ui_utils.profiles.create_traffic_mirroring_profile import CreateMonitorProfile
from support.ui_utils.profiles.create_ssl_decryption_keyring_profile import CreateSSLDecryptionKeyringProfile
from support.ui_utils.profiles.create_ssl_decryption_profile import CreateSSLDecryptionProfile
from support.ui_utils.profiles.create_tcp_option_profile import CreateTcpOptionProfile
from support.ui_utils.profiles.create_replacement_file import CreateReplacementFile
from support.ui_utils.profiles.create_js_file import CreateJSFile
from support.ui_utils.profiles.create_css_file import CreateCSSFile
from support.ui_utils.profiles.create_lua_script import CreateLuaScript
from support.ui_utils.profiles.create_sc_profile import CreateServiceFunctionForwarderProfile
from support.ui_utils.profiles.create_statistics_template import CreateStatisticsTemplate
from support.ui_utils.profiles.elemen_position import ElementPosition

class CreateProfiles:
    def __init__(self, driver):
        self.driver = driver

    def create_profiles(self, parameter, policy_configuration):
        result = ""
        if "action_parameter" not in policy_configuration.keys():
            return ""
        # 遍历创建
        profile_list = ["html_profile", "resolution", "traffic_mirroring", "keyring_for_trusted", "keyring_for_untrusted",
                        "decryption_profile", "tcp_option_profile", "replacement_file", "js_file", "css_file", "lua_script",
                        "profile_chain", "sff_profiles", "template_profile"]
        policy_configuration["parameter"] = parameter
        for k, v in policy_configuration["action_parameter"].items():
            if k not in profile_list:   # 没有则不用执行profile
                continue
            profile_element_position, key_name = ElementPosition(policy_configuration).get_profile_element_position_library
            if len(profile_element_position) == 0:
                return ""
            try:   #页面Profile菜单跳转
                page_jump_element_position = profile_element_position["page_jump"]
                page_jump = PageJump(self.driver)
                page_jump.jump_sub_profile_page(page_jump_element_position)
            except Exception as e:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When jumping profile, the exception error: ", str(e), flush=True)
                return "When jumping profile, the exception error: " + str(e)
            try:   #点击create button
                create_element_position = profile_element_position["create"]
                self.driver.find_element(By.XPATH, create_element_position["profileListPage_createButton_posXpath"]).click()
            except Exception as e:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When clicking create button, the exception error: ", str(e), flush=True)
                return "When clicking create button, the exception error: " + str(e)

            if key_name == "response_page":
                result = self._create_response_page(policy_configuration)
            elif key_name == "dns_resource_record":
                result = self._create_dns_resource_record(policy_configuration)
            elif key_name == "traffic_mirroring_profile":
                result = self._create_traffic_mirroring_profile(policy_configuration)
            elif key_name == "ssl_decryption_keyring":
                result = self._create_run_ssl_decryption_keyring(policy_configuration)
            elif key_name == "ssl_decryption_profile":
                result = self._create_run_ssl_decryption_profile(policy_configuration)
            elif key_name == "tcp_option_profile":
                result = self._create_run_tcp_option_profile(policy_configuration)
            elif key_name == "replacement_file":
                result = self._create_replacement_file(policy_configuration)
            elif key_name == "js_file":
                result = self._create_js_file(policy_configuration)
            elif key_name == "css_file":
                result = self._create_cs_file(policy_configuration)
            elif key_name == "run_script":
                result = self._create_run_script(policy_configuration)
            elif key_name == "shaping_profile":
                result = "shaping_profile"
            elif key_name == "sff_profiles":
                result = self._create_sff_script(policy_configuration)
            elif key_name == "statistics_template":
                result = self._create_statistics_template_page(policy_configuration)
            else:
                result = ""
        return result

    def _create_response_page(self, policy_configuration):
        # resposne page 创建函数
        Pl = CreateResponsePage(self.driver)
        return Pl.create_response_page(policy_configuration)

    def _create_dns_resource_record(self, policy_configuration):
        # dns resource record 创建函数
        Pl = CreateDnsResourceReccord(self.driver)
        return Pl.create_dns_resource_record(policy_configuration)

    def _create_traffic_mirroring_profile(self, policy_configuration):
        # 新建 tcp_proxy_profile
        Pl = CreateMonitorProfile(self.driver)
        return Pl.create_traffic_mirroring_profile(policy_configuration)

    def _create_run_ssl_decryption_keyring(self, policy_configuration):
        # 新建 ssl_decryption_keyring
        Pl = CreateSSLDecryptionKeyringProfile(self.driver)
        return Pl.create_ssl_decryption_keyring_file(policy_configuration)

    def _create_run_ssl_decryption_profile(self, policy_configuration):
        # 新建 ssl_decryption_proile
        Pl = CreateSSLDecryptionProfile(self.driver)
        return Pl.create_ssl_decryption_file(policy_configuration)

    def _create_run_tcp_option_profile(self, policy_configuration):
        # 新建 tcp_option_profile
        Pl = CreateTcpOptionProfile(self.driver)
        return Pl.create_tcp_option_profile(policy_configuration)

    def _create_replacement_file(self, policy_configuration):
        # 新建replacement file
        Pl = CreateReplacementFile(self.driver)
        return Pl.create_Replacement_file(policy_configuration)

    def _create_js_file(self, policy_configuration):
        # 新建js file
        Pl = CreateJSFile(self.driver)
        return Pl.create_js_file(policy_configuration)

    def _create_cs_file(self, policy_configuration):
        # 新建js file
        Pl = CreateCSSFile(self.driver)
        return Pl.create_css_file(policy_configuration)

    def _create_run_script(self, policy_configuration):
        # 新建 run script
        Pl = CreateLuaScript(self.driver)
        return Pl.create_lua_script(policy_configuration)

    def _create_sff_script(self, policy_configuration):
        # 新建 sff
        Pl = CreateServiceFunctionForwarderProfile(self.driver)
        return Pl.create_sff_profile(policy_configuration)

    def _create_statistics_template_page(self, policy_configuration):
        # 新建 statistics_template
        Pl = CreateStatisticsTemplate(self.driver)
        return Pl.create_statistics_template(policy_configuration)



