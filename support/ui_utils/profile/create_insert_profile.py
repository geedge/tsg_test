import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from datetime import datetime 

class CreateInsertProfile:
    def __init__(self, driver):
        self.driver = driver

    def create_hijack_file(self, data):
        profile_name = data["name"]
        self.driver.find_element(By.ID, insertScripts_input_Name_posId).send_keys(profile_name)
        #页面其它选项操作
        result_code = self._operate_page(data, operation_type="create")
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, insertScripts_button_oK_posCss).click()
        if self.driver.find_element(By.CSS_SELECTOR, insertScripts_button_warningSaveYes_posCss).is_displayed():
            self.driver.find_element(By.CSS_SELECTOR, insertScripts_button_warningSaveYes_posCss).click()

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

        self._operate_scriptType(data, data_index=data_index)
        #File文件上传操作
        file = self._get_value_from_data(data, key="script", data_index=data_index)   #解析file文件名称
        if file != no_modify:      #判断修改时不修改时跳过操作。
            if file != "":
                create_file = data["script"].split("->")[data_index]  # 提取上传文件绝对路径
                profile_path = os.path.dirname(os.path.abspath(__file__))  # ...support\ui_utils\profile
                file_abs = os.path.join(profile_path, "profile_file", "insert_scripts", create_file)
                #上传文件
                self.driver.find_element(By.XPATH, insertScripts_input_scriptUpLoad_posXpath).send_keys(file_abs)

    def _operate_scriptType(self, data, data_index=0, no_modify="不修改"):
        """
        脚本类型操作,。
        :param data:
        :param data_index: 0 -1来自上层
        :param no_modify:"不修改" 来自上次调用
        :param operation_type: create modify两个状态，
        :return:
        """
        #解析输入data数据的数据，脚本类型
        script_type = self._get_value_from_data(data, key="script_type", data_index=data_index)
        if script_type != no_modify:     #编辑不修改时执行
            if script_type != "":
                self.driver.find_element(By.XPATH, insertScripts_input_scriptType_posXpath).click()   #点击输入列表框
                if "js" == script_type:   #js类型点击
                    self.driver.find_element(By.XPATH, insertScripts_dropdown_jsItem_posXpath).click()
                    #insert position操作
                    insert_position = self._get_value_from_data(data, key="insert_position", data_index=data_index)     #获取insert position等操作After Page Load
                    if insert_position != no_modify:
                        self.driver.find_element(By.XPATH, insertScripts_input_insertPosition_posXpath).click()
                        if ("after" in insert_position) and ("page" in insert_position) and ("load" in insert_position):      #点击 after Page Load选项
                            #点击下拉列表选项
                            self.driver.find_element(By.XPATH, insertScripts_dropdown_afterPageLoadItem_posXpath).click()
                        else:                    #点击 before Page Load选项
                            self.driver.find_element(By.XPATH, insertScripts_dropdown_beforePageLoadItem_posXpath).click()
                else:          #css类型点击列表
                    self.driver.find_element(By.XPATH, insertScripts_dropdown_cssItem_posXpath).click()

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




