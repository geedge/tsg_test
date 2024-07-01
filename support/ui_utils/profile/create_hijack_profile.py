import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *

class CreateHijackProfile():
    def __init__(self, driver):
        self.driver = driver

    def create_hijack_file(self, data):
        profile_name = data["name"]
        self.driver.find_element(By.ID, hijackFiles_input_Name_posId).clear()
        self.driver.find_element(By.ID, hijackFiles_input_Name_posId).send_keys(profile_name)
        self.driver.find_element(By.XPATH, "//label[text()='Name']").click()
        #页面其它选项操作
        self._operate_page(data, operation_type="create")
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, hijackFiles_button_oK_posCss).click()
        if self.driver.element_isExist(By.CSS_SELECTOR,hijackFiles_button_warningSaveYes_posCss):
            self.driver.find_element(By.CSS_SELECTOR, hijackFiles_button_warningSaveYes_posCss).click()

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
        #解析输入data数据的数据
        #File文件上传操作
        file = self._get_value_from_data(data, key="file", data_index=data_index)   #解析file文件名称
        # print(file)
        if file != no_modify:      #判断修改时不修改时跳过操作。
            create_file = data["file"].split("->")[data_index]  # 提取上传文件绝对路径
            profile_path = os.path.dirname(os.path.abspath(__file__))  # ...support\ui_utils\profile
            file_abs = os.path.join(profile_path, "profile_file", "hijack_file", create_file)
            #print(file_abs)
            self.driver.find_element(By.XPATH, hijackFiles_input_fileUpLoad_posXpath).send_keys(file_abs)
        #download name 下载文件名称操作
        self._operate_switch(data, data_index=data_index, no_modify=no_modify, switch_name="download_name", element_position=hijackFiles_switch_downLoadName_posXpath)
        #file type 文件类型操作
        file_type = self._get_value_from_data(data, key="file_type", data_index=data_index)
        if file_type != no_modify:    #修改时不用修改数据直接跳过
            #点击type添加按钮
            self.driver.find_element(By.XPATH, hijackFiles_button_fileType_posXpath).click()
            element_type_replace_name = {'gif': 'image/gif', 'jpeg': 'image/jpeg', 'png': 'image/png', 'svg+xml': 'image/svg+xml',
                                         'exe': 'application/x-msdos-program', 'apk': 'application/vnd.android.package-archive', 'html': 'text/html'}
            if file_type not in element_type_replace_name.keys():
                #raise f"文件类型错误。用例数据类型为：{file_type}, 可选择文件类型为：{list(element_type_replace_name.keys())}"
                print("please check")
                return 0
            element_tablist_type = self.driver.find_element(By.XPATH, hijackFiles_tablist_fileType_posXpath.format(replaceName=element_type_replace_name[file_type]))
            self.driver.execute_script("arguments[0].click()", element_tablist_type)  # 强制点击

    def _operate_switch(self, data, data_index=0, no_modify="不修改", switch_name="", element_position=""):
        """
        页面中，开关状态操作,。
        :param data:
        :param data_index: 0 -1来自上层
        :param no_modify:"不修改" 来自上次调用
        :param operation_type: create modify两个状态，
        :param switch_name: 数据中开关名称
        :param elementPosition: 开关的定位
        :return:
        """
        #解析输入data数据的数据
        switch_value: str = self._get_value_from_data(data, key=switch_name, data_index=data_index)     #提取数据 Mirror Server Response
        if switch_value != no_modify:            #编辑时，有不修改则不用执行
            #先获取当前页面中开关状态   include_root_current_class ： class="el-switch is-checked"   有is-checked当前状态为开，没有is-chedked当前状态为关
            swith_current_class = self.driver.find_element(By.XPATH, element_position).get_attribute("class")
            if ("mirror" in switch_value) and ("server" in switch_value) and ("response" in switch_value):    #数据中为Mirror Server Response，使用默认名称，不修改; on时需要打开这个开关
                if "is-checked" in swith_current_class:   #页面当前为开，不用点击开关
                    pass
                else:                                            #页面当前为关，需要点击开关
                    self.driver.find_element(By.XPATH, f"{element_position}/span[2]").click()
            else:                     ##数据中为其它名称，则需要修改默认名称
                if "is-checked" in swith_current_class:     #页面当前为开，需要先关闭开关，在输入值
                    self.driver.find_element(By.XPATH, f"{element_position}/span[2]").click()

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
            print(e)
        return switch_value


