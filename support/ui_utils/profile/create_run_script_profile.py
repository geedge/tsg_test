import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from datetime import datetime 

class CreateRunScriptProfile:
    def __init__(self, driver):
        self.driver = driver

    def create_run_script_file(self, data):
        profile_name = data["name"]
        self.driver.find_element(By.XPATH, tsgProxyScripts_input_Name_posXpath).clear()
        self.driver.find_element(By.XPATH, tsgProxyScripts_input_Name_posXpath).send_keys(profile_name)
        self.driver.find_element(By.XPATH, "//label[text()='Name']").click()
        #页面其它选项操作
        self._operate_page(data, operation_type="create")
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, tsgProxyScripts_button_oK_posCss).click()
        if self.driver.is_exist_element_by_value(By.CSS_SELECTOR,tsgProxyScripts_button_warningSaveYes_posCss):
            self.driver.find_element(By.CSS_SELECTOR, tsgProxyScripts_button_warningSaveYes_posCss).click()

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
        #File文件上传操作
        file = self._get_value_from_data(data, key="script", data_index=data_index)   #解析file文件名称
        if file != no_modify:      #判断修改时不修改时跳过操作。
            if file != "":
                #上传文件
                create_file = data["script"].split("->")[data_index]  # 提取上传文件绝对路径
                profile_path = os.path.dirname(os.path.abspath(__file__))  # ...support\ui_utils\profile
                file_abs = os.path.join(profile_path, "profile_file", "tsg_proxy_scripts", create_file)
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], file_abs)
                self.driver.find_element(By.XPATH, tsgProxyScripts_input_runScripts_posXpath).send_keys(file_abs)
            elif file == "" and data_index == -1:
                element_del = self.driver.find_element(By.XPATH, "//div[@id='runScriptTitleUpload']//i[@class='el-icon-close']")
                self.driver.execute_script("arguments[0].click()", element_del)  #强制点击
        #maximum execution time 操作
        max_exec_time = self._get_value_from_data(data, key="max_exec_time", data_index=data_index)
        if max_exec_time != no_modify:        #修改操作时，不修改数据则跳过操作。
            self.driver.find_element(By.XPATH, tsgProxyScripts_input_maximumExecutionTime_posXpath).clear()
            #输入数据
            self.driver.find_element(By.XPATH, tsgProxyScripts_input_maximumExecutionTime_posXpath).send_keys(max_exec_time)

    def _get_value_from_data(self, data, key="", data_index=0):
        """
        从data数据中，根据key提取值
        :param data:
        :param key:
        :param data_index: 0 -1
        :return:
        """
        try:
            data_value: str = data[key].split("->")[data_index].strip().lower()    #用例数据
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
        return data_value