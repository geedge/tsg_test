import os
import sys
import time
from datetime import datetime
from selenium.webdriver.common.by import By

from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.read_data import ReadData


class ExportObjects:

    def __init__(self,driver):
        self.driver = driver
        self.my_files = ReadData()

    def export_objects(self,object_info,first_row_checkbox_element):
        try:
            first_row_checkbox_element.click()  # 选择第一个对象
            self.driver.find_element(By.XPATH, main_ObjectPage_Input_Import_files_button_posXpath).click()  # 点击导出文件
            self.driver.find_element(By.XPATH, list_PageObject_Export_files_yes_button_posXpath).click()

        # # 校验文件内容
        # time.sleep(3)
        # self.file_name = get_txt_filenames(path=self.my_files._obj_files_dowload_path())
        # self.file_path = self.my_files._obj_files_dowload_path() + "\\" + self.file_name
        # self.content = open(self.file_path, "rb").read()
        # try:
        #     assert str(object_info["ip"]) in str(self.content), "断言导出内容是否在txt文件中"
        #     os.remove(self.file_path)
        #     print("文件删除成功")
        # except:
        #     print("文件不存在")
        # # 3、断言成功后，删除文件
        # self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
        # self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()
            first_row_checkbox_element.click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",file=sys.stderr, flush=True)
            return 400

def get_txt_filenames(path):  # 《不需要实例化类》不写在类方法下
    filenames = []
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            filenames.append(filename)

    return str(filenames[0])