import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from datetime import datetime 

class CreateSSLDecryptionProfile:
    def __init__(self, driver):
        self.driver = driver

    def create_ssl_decryption_file(self, data):
        profile_name = data["name"]
        self.driver.find_element(By.ID, sslDecryptionProfiles_input_Name_posId).send_keys(profile_name)
        #页面其它选项操作
        result_code = self._operate_page(data, operation_type="create")
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, sslDecryptionProfiles_button_oK_posCss).click()
        if self.driver.find_element(By.CSS_SELECTOR, sslDecryptionProfiles_button_warningSaveYes_posCss, find_before_wait_time=1).is_displayed():
            self.driver.find_element(By.CSS_SELECTOR, sslDecryptionProfiles_button_warningSaveYes_posCss).click()

    def _operate_page(self, data: {}, operation_type="create"):
        """"""
        if operation_type == "create":
            data_index = 0   #新增数据索引
        else:
            data_index = -1   #编辑数据索引
        no_modify = "不修改"
        #解析输入data数据的数据
        #页面开关操作 common name,issuer,selfSigned,expiryDate
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="common_name", element_position=sslDecryptionProfiles_switch_commonName_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="issuer", element_position=sslDecryptionProfiles_switch_issuer_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="self_signed", element_position=sslDecryptionProfiles_switch_selfSigned_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify,  switch_name="expiry_date", element_position=sslDecryptionProfiles_switch_expiryDate_posXpath)
        #Fail Action操作
        fail_action = self._get_value_from_data(data, key="fail_action", data_index=data_index)    #用例数据提取 Pass-through   Fail-close
        if fail_action != no_modify:
            if "pass-through" == fail_action:        #点击pass through
                self.driver.find_element(By.XPATH, sslDecryptionProfiles_radio_passThrough_posXpath).click()
            else:                                    #点击fail close
                self.driver.find_element(By.XPATH, sslDecryptionProfiles_radio_failClose_posXpath).click()
        #页面开关操作ev_certificate  certificate_transparency mutual_authentication protocol_errors certificate_pinning certificate_not_installed allow_HTTP2 mirror_client_versions
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="ev_certificate", element_position=sslDecryptionProfiles_switch_evCert_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="certificate_transparency", element_position=sslDecryptionProfiles_switch_certificateTransparency_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="mutual_authentication", element_position=sslDecryptionProfiles_switch_mutualAuthentication_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="protocol_errors", element_position=sslDecryptionProfiles_switch_onProtocolErrors_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="certificate_pinning", element_position=sslDecryptionProfiles_switch_certificatePinning_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="certificate_not_installed", element_position=sslDecryptionProfiles_switch_certificateNotInstalled_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="mirror_client_versions", element_position=sslDecryptionProfiles_switch_mirrorClientVersions_posXpath)
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="allow_HTTP2", element_position=sslDecryptionProfiles_switch_allowHTTP2_posXpath)
        #Min Max version操作
        mirror_client_versions = self._get_value_from_data(data, key="mirror_client_versions", data_index=data_index)   #提取数据
        mirror_client_versions_class = self.driver.find_element(By.XPATH, sslDecryptionProfiles_switch_mirrorClientVersions_posXpath).get_attribute("class")   #该开关当前属性状态
        allowHTTP2_class = self.driver.find_element(By.XPATH, sslDecryptionProfiles_switch_allowHTTP2_posXpath).get_attribute("class")  # 该开关当前属性状态
        print(allowHTTP2_class)
        if "is-checked" not in mirror_client_versions_class:    #只有 当前状态为关时，才可以操作版本大小。
            min_version = self._get_value_from_data(data, key="min_client_version", data_index=data_index)
            max_version = self._get_value_from_data(data, key="max_client_version", data_index=data_index)
            print(min_version)
            print(max_version)
            version_index_list = ['sslv3.0', 'tlsv1.0', 'tlsv1.1', 'tlsv1.2', 'tlsv1.3']
            if min_version != no_modify:    #编辑时不修改，则不用操作
                self.driver.find_element(By.XPATH, sslDecryptionProfiles_input_minVersion_posXpath).click()
                element_pos_min_drop_down_item = sslDecryptionProfiles_dropDown_minVersion_posXpath.format(replaceIndex=version_index_list.index(min_version))   #组定位
                self.driver.find_element(By.XPATH, element_pos_min_drop_down_item).click()
                # allow HTTP/2打开时，校验Min version
                if "is-checked" in allowHTTP2_class and (min_version not in ["tlsv1.2", "tlsv1.3"]):
                    assert self.driver.element_isExist(By.XPATH, "//p[@class='el-message__content']")
                    error_content = self.driver.find_element(By.XPATH, "//p[@class='el-message__content']").text.strip()
                    # print("error_content=", error_content)
            time.sleep(2)
            if max_version != no_modify:     #编辑时不修改，则不用操作
                self.driver.find_element(By.XPATH, sslDecryptionProfiles_input_maxVersion_posXpath).click()
                element_pos_max_drop_down_item = sslDecryptionProfiles_dropDown_maxVersion_posXpath.format(replaceIndex=version_index_list.index(max_version))   #组定位
                self.driver.find_element(By.XPATH, element_pos_max_drop_down_item).click()
                # allow HTTP/2打开时，校验Max version
                if "is-checked"  in allowHTTP2_class and (min_version not in ["tlsv1.2", "tlsv1.3"]):
                    assert self.driver.element_isExist(By.XPATH, "//p[@class='el-message__content']")
                    error_content = self.driver.find_element(By.XPATH, "//p[@class='el-message__content']").text.strip()
                    # print("error_content=", error_content)
                    time.sleep(2)

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

    def _get_value_from_data(self, data: {}, key="", data_index=0):
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
            print(e)
        return switch_value



