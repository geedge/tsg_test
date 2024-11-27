import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from datetime import datetime 

class CreateTcpProxyProfile:
    def __init__(self, driver):
        self.driver = driver

    def create_tcp_proxy_profile(self, data):
        profile_name = data["name"]
        self.driver.find_element(By.ID, tcpProxyProfiles_input_Name_posId).send_keys(profile_name)
        #页面其它选项操作
        result_code = self._operate_page(data, operation_type="create")
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, tcpProxyProfiles_button_oK_posCss).click()
        if self.driver.find_element(By.CSS_SELECTOR, tcpProxyProfiles_button_warningSaveYes_posCss, find_before_wait_time=1).is_displayed():
            self.driver.find_element(By.CSS_SELECTOR, tcpProxyProfiles_button_warningSaveYes_posCss).click()

    def _operate_page(self, data, operation_type="create"):
        """
        除name的其它选项操作，供创建、修改逻辑调用
        :param data:
        :param operation_type: create modify。创建 修改时调用
        :return:
        """
        no_modify = "不修改"
        if operation_type == "create":
            data_index = 0   #新增数据索引
        else:
            data_index = -1   #编辑数据索引

        #解析输入data数据的数据
        #enable TCP Passthrough 开关操作
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="enable_TCP_passthrough", element_position=tcpProxyProfiles_switch_enableTCPPassthrough_posXpath)
        #Client_side 开关操作 override MSS, no delay, keepalive
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="c_override_MSS", element_position=tcpProxyProfiles_switch_clientOverrideMSS_posXpath)
        # Client_side 输入操作 override MSS, ttl, user Timeout
        c_overrideMSS_test = self._get_value_from_data(data, key="c_override_MSS", data_index=data_index)
        if c_overrideMSS_test == "on" or c_overrideMSS_test == no_modify:
            c_overrideMSS = self._get_value_from_data(data, key="c_overrideMSS", data_index=data_index)
            if c_overrideMSS != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientOverrideMSS_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientOverrideMSS_posXpath).send_keys(c_overrideMSS)
                self.driver.find_element(By.XPATH, "//label[text()='Override MSS']").click()

        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="c_no_delay", element_position=tcpProxyProfiles_switch_clientNoDelay_posXpath)
        c_ttl = self._get_value_from_data(data, key="c_ttl", data_index=data_index)
        if c_ttl != no_modify:  # 判断不修改时跳过操作
            self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientTTL_posXpath).clear()
            self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientTTL_posXpath).send_keys(c_ttl)
            self.driver.find_element(By.XPATH, "//label[text()='TTL']").click()

        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="c_keepalive", element_position=tcpProxyProfiles_switch_clientKeepalive_posXpath)
        c_keepalive_test = self._get_value_from_data(data, key="c_keepalive", data_index=data_index)
        if c_keepalive_test == "on":
            c_probe_number = self._get_value_from_data(data, key="c_probe_number", data_index=data_index)
            if c_probe_number != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientProbeNumber_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientProbeNumber_posXpath).send_keys(c_probe_number)
                self.driver.find_element(By.XPATH, "//label[text()='Probe Number']").click()
            c_idle_time = self._get_value_from_data(data, key="c_idle_time", data_index=data_index)
            if c_idle_time != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientIdleTime_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientIdleTime_posXpath).send_keys(c_idle_time)
                self.driver.find_element(By.XPATH, "//label[text()='Idle Time']").click()
            c_interval = self._get_value_from_data(data, key="c_interval", data_index=data_index)
            if c_interval != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientInterval_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientInterval_posXpath).send_keys(c_interval)
                self.driver.find_element(By.XPATH, "//label[text()='Interval']").click()

        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="c_UserTimeout_switch",
                             element_position=tcpProxyProfiles_switch_clientUserTimeout_posXpath)
        c_UserTimeout_test = self._get_value_from_data(data, key="c_UserTimeout_switch", data_index=data_index)
        if c_UserTimeout_test == "on" or c_overrideMSS_test == no_modify:
            c_userTimeout = self._get_value_from_data(data, key="c_userTimeout", data_index=data_index)
            if c_userTimeout != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientUserTimeout_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_clientUserTimeout_posXpath).send_keys(c_userTimeout)
                self.driver.find_element(By.XPATH, "//label[text()='User Timeout']").click()

        # Server_side 开关操作 override MSS, no delay, keepalive
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="s_override_MSS", element_position=tcpProxyProfiles_switch_serverOverrideMSS_posXpath)
        # Server_side 输入操作 override MSS, ttl, user Timeout
        s_overrideMSS_test = self._get_value_from_data(data, key="s_override_MSS", data_index=data_index)
        if s_overrideMSS_test == "on":
            s_overrideMSS = self._get_value_from_data(data, key="s_overrideMSS", data_index=data_index)
            if s_overrideMSS != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverOverrideMSS_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverOverrideMSS_posXpath).send_keys(s_overrideMSS)
                self.driver.find_element(By.XPATH, "//label[text()='Override MSS']").click()

        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="s_no_delay", element_position=tcpProxyProfiles_switch_serverNoDelay_posXpath)
        s_ttl = self._get_value_from_data(data, key="s_ttl", data_index=data_index)
        if s_ttl != no_modify:  # 判断不修改时跳过操作
            self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverTTL_posXpath).clear()
            self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverTTL_posXpath).send_keys(s_ttl)
            self.driver.find_element(By.XPATH, "//label[text()='TTL']").click()

        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="s_keepalive", element_position=tcpProxyProfiles_switch_serverKeepalive_posXpath)
        s_keepalive_test = self._get_value_from_data(data, key="s_keepalive", data_index=data_index)
        if s_keepalive_test == "on":
            s_probe_number = self._get_value_from_data(data, key="s_probe_number", data_index=data_index)
            if s_probe_number != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverProbeNumber_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverProbeNumber_posXpath).send_keys(s_probe_number)
                self.driver.find_element(By.XPATH, "//label[text()='Probe Number']").click()
            s_idle_time = self._get_value_from_data(data, key="s_idle_time", data_index=data_index)
            if s_idle_time != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverIdleTime_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverIdleTime_posXpath).send_keys(s_idle_time)
                self.driver.find_element(By.XPATH, "//label[text()='Idle Time']").click()
            s_interval = self._get_value_from_data(data, key="s_interval", data_index=data_index)
            if s_interval != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverInterval_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverInterval_posXpath).send_keys(s_interval)
                self.driver.find_element(By.XPATH, "//label[text()='Interval']").click()

        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="s_UserTimeout_switch",
                             element_position=tcpProxyProfiles_switch_serverUserTimeout_posXpath)
        s_UserTimeout_test = self._get_value_from_data(data, key="s_UserTimeout_switch", data_index=data_index)
        if s_UserTimeout_test == "on":
            s_userTimeout = self._get_value_from_data(data, key="s_userTimeout", data_index=data_index)
            if s_userTimeout != no_modify:  # 判断不修改时跳过操作
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverUserTimeout_posXpath).clear()
                self.driver.find_element(By.XPATH, tcpProxyProfiles_input_serverUserTimeout_posXpath).send_keys(s_userTimeout)
                self.driver.find_element(By.XPATH, "//label[text()='User Timeout']").click()

    def _operate_switch(self, data: {}, data_index=0, no_modify="不修改", switch_name="", element_position=""):
        """
        页面中，开关状态操作。
        :param data:
        :param data_index: 0 -1来自上层
        :param no_modify:"不修改" 来自上次调用
        :param operation_type: create modify两个状态，
        :param switch_name: 数据中开关名称
        :param elementPosition: 开关的定位
        :return:
        """
        #解析输入data数据的数据
        switch_value: str = self._get_value_from_data(data, key=switch_name, data_index=data_index)     #提取数据
        # print("switch_value=", switch_value)
        if switch_value != no_modify:            #编辑时，有不修改则不用执行
            #先获取当前页面中开关状态   include_root_current_class ： class="el-switch is-checked"   有is-checked当前状态为开，没有is-chedked当前状态为关
            swith_current_class = self.driver.find_element(By.XPATH, element_position).get_attribute("class")
            if "on" == switch_value:    #数据中为开
                if "is-checked" in swith_current_class:   #页面当前为开，不用点击开关
                    pass
                else:                                            #页面当前为关，需要点击开关
                    self.driver.find_element(By.XPATH, element_position).click()
            else:                     #用例输入为关
                if "is-checked" in swith_current_class:     #页面当前为开，需要点击开关
                    self.driver.find_element(By.XPATH, element_position).click()
                else:                                            #页面当前为关，不用点击开关
                    pass

    def _get_value_from_data(self, data, key="", data_index=0):
        """
        从data数据中，根据key提取值
        :param data:
        :param key:
        :param data_index: 0 -1
        :return:
        """
        try:
            switch_value: str = data[key].split("->")[data_index].strip().lower()    #用例数据
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
        return switch_value




