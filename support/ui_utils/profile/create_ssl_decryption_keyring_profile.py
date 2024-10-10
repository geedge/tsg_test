import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from datetime import datetime 

class CreateSSLDecryptionKeyringProfile:
    def __init__(self, driver):
        self.driver = driver

    def create_ssl_decryption_keyring_file(self, data):
        profile_name = data["name"]
        self.driver.find_element(By.ID, sslDecryptionKeyrings_input_Name_posId).send_keys(profile_name)
        #页面其它选项操作
        result_code = self._operate_page(data, operation_type="create")
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, sslDecryptionKeyrings_button_oK_posCss).click()
        if self.driver.find_element(By.CSS_SELECTOR, sslDecryptionKeyrings_button_warningSaveYes_posCss, find_before_wait_time=1).is_displayed():
            self.driver.find_element(By.CSS_SELECTOR, sslDecryptionKeyrings_button_warningSaveYes_posCss).click()

    def _operate_page(self, data, operation_type="create"):
        """
        除name的其它选项操作，共创建、修改逻辑调用
        :param data:
        :param operation_type: create modify。创建 修改时调用
        :return:
        """
        if operation_type == "create":
            data_index = 0   #新增数据索引
        else:
            data_index = -1   #编辑数据索引
        no_modify = "不修改"
        #script type脚本类型操作 --先操作文件类型

        #File文件上传操作 证书
        file = self._get_value_from_data(data, key="file_certificate", data_index=data_index)   #解析file文件名称
        if file != no_modify:      #判断修改时不修改时跳过操作。
            if file != "":
                create_file = data["file_certificate"].split("->")[data_index]  # 提取上传文件绝对路径
                profile_path = os.path.dirname(os.path.abspath(__file__))  # ...support\ui_utils\profile
                file_abs = os.path.join(profile_path, "profile_file", "ssl_decryption_keyring", create_file)
                #上传文件
                self.driver.find_element(By.XPATH, sslDecryptionKeyrings_input_certificateFile_posXpath).send_keys(file_abs)
        #File文件上传操作 私钥
        file_pri = self._get_value_from_data(data, key="file_private_key", data_index=data_index)   #解析file文件名称
        if file_pri != no_modify:      #判断修改时不修改时跳过操作。
            if file_pri != "":
                create_file_pri = data["file_private_key"].split("->")[data_index]  # 提取上传文件绝对路径
                profile_path = os.path.dirname(os.path.abspath(__file__))  # ...support\ui_utils\profile
                file_abs_pri = os.path.join(profile_path, "profile_file", "ssl_decryption_keyring", create_file_pri)
                #上传文件
                self.driver.find_element(By.XPATH, sslDecryptionKeyrings_input_privateKeyFile_posXpath).send_keys(file_abs_pri)


        #证书时间选择
        reissue_expiry_hours: str = data["reissue_expiry_hours"].split("->")[data_index].strip()
        if reissue_expiry_hours != no_modify:
            if reissue_expiry_hours.startswith("MSC"):     #'MSC'
                self.driver.find_element(By.ID, sslDecryptionKeyrings_radio_mirrorServerCertificate_poId).click()
            else:
                self.driver.find_element(By.ID, sslDecryptionKeyrings_radio_customized_poId).click()
                self.driver.find_element(By.ID, sslDecryptionKeyrings_input_customized_poId).clear()
                self.driver.find_element(By.ID, sslDecryptionKeyrings_input_customized_poId).send_keys(reissue_expiry_hours.lstrip("C-"))     #‘C-234'
        #证书类型操作
        if "type" in data.keys():
            type = data["type"].split("->")[data_index].strip()
            if type != no_modify:
                type_index_dict = {"": 3, "Root-Certificate": 0, "Intermediate-Certificate": 1, "End-entity": 2}
                if type not in type_index_dict.keys():
                    raise f"certificate type error：type={type}."
                if type !="":
                    element_pos_type_droplist_item = sslDecryptionKeyrings_dropdown_certificateTypeSelect_poId.format(replaceIndex=type_index_dict[type])
                    self.driver.find_element(By.ID, sslDecryptionKeyrings_input_certificateType_poId).click()    #点击类型列表选择框
                    self.driver.find_element(By.ID, element_pos_type_droplist_item).click()            #点击列表下拉参数具体选项
        #公钥算法
        pka = data["public_key_algorithm"].split("->")[data_index].strip()
        if pka != no_modify:
            pka_idex_dict = {"": 4, "RSA-1024": 0, "RSA-2048": 1, "SECP-256r1": 2, "SECP-384r1": 3}    #下拉列表定位索引
            if pka not in pka_idex_dict.keys():
                raise f"public key algorithm error：pka={pka}."
            if pka != "":
                element_pos_pka_droplist_item = sslDecryptionKeyrings_dropdown_publickKeyAlgorithmSelect_poId.format(replaceIndex=pka_idex_dict[pka])
                self.driver.find_element(By.ID, sslDecryptionKeyrings_input_publickKeyAlgorithm_poId).click()
                self.driver.find_element(By.ID, element_pos_pka_droplist_item).click()   #点击公钥算法下拉选项定位
        #输入Certificate Revocation List
        if data["certificate_revocation_list"].split("->")[data_index].strip() != no_modify:
            self.driver.find_element(By.ID, sslDecryptionKeyrings_input_certificateRevocationList_poId).clear()
            self.driver.find_element(By.ID, sslDecryptionKeyrings_input_certificateRevocationList_poId).send_keys(data["certificate_revocation_list"].split("->")[data_index].strip())
        include_root = data["include_root"].split("->")[data_index].strip().lower()    #用例数据
        if include_root != no_modify:
            #先获取页面中包含根证书当前状态   include_root_current_class ： class="el-switch is-checked"   有is-checked当前状态为开，没有is-chedked当前状态为关
            include_root_current_class = self.driver.find_element(By.XPATH, sslDecryptionKeyrings_input_includeRoot_poXpath).find_element(By.XPATH, "parent::*").get_attribute("class")
            if "on" == include_root:   #开
                if "is-checked" in include_root_current_class:   #页面当前为开，不用点击开关
                    pass
                else:                                            #页面当前为关，需要点击开关
                    self.driver.find_element(By.XPATH, sslDecryptionKeyrings_input_includeRoot_poXpath).click()
                    self.include_root_statue = "on"    #修改时会使用判断
            else:                     #用例输入为关
                if "is-checked" in include_root_current_class:   #页面当前为开，需要点击开关
                    self.driver.find_element(By.XPATH, sslDecryptionKeyrings_input_includeRoot_poXpath).click()
                    self.include_root_statue = "on"  # 修改时会使用判断
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




