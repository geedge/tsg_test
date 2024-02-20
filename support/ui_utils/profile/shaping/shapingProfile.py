import configparser
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from myWebDriver import MyWebDriver
from selenium.webdriver.common.by import By
from workpath import workdir
from element_position.profileElementPosition import *
from screenshot import screenshot_on_failure
# from randomName import RandomName
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from profilePublicFunc import ProfilePublicFunc
from logInOut import LogInOut
import pytest_check
import inspect

class ShapingProfile:
    def __init__(self, driver):
        self.workdir = workdir
        # self.my_random = RandomName()
        self.driver = driver
        # 调用profile公共方法操作、删除、查询，
        self.profile_pub_func = ProfilePublicFunc(self.driver)
        self.ep_error_part_path = "ancestor::div[@class='el-form-item__content']//div[@class='el-form-item__error']"   # 创建页面错误提示信息部分定位信息

    # @screenshot_on_failure
    def create(self, data):
        # 页面跳转
        self.jump_sub_profile_page()
        # 点击create
        self.profile_name = data["name"]
        self.driver.find_element(By.ID, listPage_profile_shaping_profile_createButton_posId).click()
        self.driver.find_element(By.ID, shapingProfilePage_input_Name_posId).send_keys(self.profile_name)
        # 输入小于4个字符判断
        if len(self.profile_name) < 4:
            # 点击OK
            self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_oK_posCss).click()
            ep_name_error = "//*[@id='{}']/{}".format(shapingProfilePage_input_Name_posId, self.ep_error_part_path)
            ep_name_error_value = self.driver.find_element(By.XPATH, ep_name_error).text.strip()
            ep_name_error_value_except = "The length of the name is at most 128 characters and cannot be less than 4 characters"
            pytest_check.is_in(ep_name_error_value_except, ep_name_error_value, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            return 999
        # 判断点击哪种类型
        self.select_type(data)
        select_limits_result = self.select_limits(data, model=0)
        if select_limits_result == 999:
            return 999
        # 点击ok
        self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_oK_posCss).click()
        self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_warningSaveYes_posCss).click()
        return 200
    
    # @screenshot_on_failure
    def search(self, data, require_assertion=0, vsys_name="", **kwargs):
        """
        查询函数,根据输入的类型查询
        :param require_assertion: =0默认情况不需要断言，=1为创建后使用的断言预期，=2为编辑修改后使用的断言预期
        :param kwargs: 例如 ：可以查询使用的关键字，ID=None,Name=None,
        :return:
        """
        # 打开该列表
        self.jump_sub_profile_page(vsys_name=vsys_name)
        # first_row查询到的第一行内容。map_header_className为需要使用的到字典，用来提取第一行的结果。
        first_row, map_header_className = \
            self.profile_pub_func.search(listPage_profileSearch_shaping_profile_selectLabel_posId, listPage_profileSearch_shaping_profile_dropDown_item_posXpath,
                                listPage_profileSearch_shaping_profile_input_itemContent_posXpath, listPage_profileSearch_shaping_profile_buttonSearch_posId,
                                listPage_profilTable_shaping_profile_tableTbody_posXpath, listPage_profilTable_shaping_profile_tableHeader_posXpath, **kwargs)
        # 第一行的勾选定位，给修改、删除使用
        if first_row == 0:     # 没有查询到数据
            return "no data"
        self.first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
        self.first_row_ID_content = first_row.find_element(By.XPATH, "//div[@class='table-status-item-id']/span").text.strip()
        first_row_referenceCount_class = map_header_className["Reference Count"]
        self.first_row_referenceCount_element = first_row.find_element(By.XPATH, f"//td[contains(@class, '{first_row_referenceCount_class}')]//div[contains(@class, 'obj-charts-btn')]")
        self.first_row_referenceCount_content = first_row.find_element(By.XPATH, f"//td[contains(@class, '{first_row_referenceCount_class}')]").text.strip()
        first_row_id_content = first_row.find_element(By.XPATH, "//div[@class='table-status-item-id']//span").text.strip()
        first_row_Name_class = map_header_className["Name"]
        first_row_Name_content = first_row.find_element(By.XPATH, f"//td[contains(@class, '{first_row_Name_class}')]//span").text.strip()
        first_row_Type_class = map_header_className["Type"]
        first_row_Type_content = first_row.find_element(By.XPATH, f"//td[contains(@class, '{first_row_Type_class}')]//span").text.strip()
        first_row_IncomingOutgoing_class = map_header_className["Incoming/Outgoing"]
        first_row_IncomingOutgoing_contents = first_row.find_element(By.XPATH, f"//td[contains(@class, '{first_row_IncomingOutgoing_class}')]//span").text.strip()
        print(first_row_id_content, first_row_Name_content, first_row_Type_content, first_row_IncomingOutgoing_contents)
        # 不同操作后的断言，创建后、修改后、无断言
        if require_assertion == 1:  # 直接创建后，使用的断言
            pytest_check.equal(first_row_Name_content, self.profile_name, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            pytest_check.equal(first_row_Type_content, data["type"].strip(), msg="所在行数{}".format(inspect.currentframe().f_lineno))
            if data["outgoing"].strip().split("->")[0] == "0":    #为0时，直接断言Unlimit
                pytest_check.is_in("Unlimit", first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            else:
                outgoing_value, outgoing_unit = self._format_bps_custom(data["outgoing"].strip().split("->")[0])     # 转进率
                pytest_check.is_in(outgoing_value, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
                pytest_check.is_in(outgoing_unit, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            if data["incoming"].strip().split("->")[0] == "0":
                pytest_check.is_in("Unlimit", first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            else:
                incoming_value, incoming_unit = self._format_bps_custom(data["incoming"].strip().split("->")[0])     # 转进率
                pytest_check.is_in(incoming_value, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
                pytest_check.is_in(incoming_unit, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
        elif require_assertion == 2 and data["model"].strip().lower() == "modify":   #修改数据后，使用的断言
            pytest_check.equal(first_row_Name_content, self.profile_name, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            pytest_check.equal(first_row_Type_content, data["type"].split("->")[-1], msg="所在行数{}".format(inspect.currentframe().f_lineno))
            if data["outgoing"].strip().split("->")[-1] == "0":    #为0时，直接断言Unlimit
                pytest_check.is_in("Unlimit", first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            else:
                outgoing_value, outgoing_unit = self._format_bps_custom(data["outgoing"].strip().split("->")[-1])     # 转进率
                pytest_check.is_in(outgoing_value, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
                pytest_check.is_in(outgoing_unit, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            if data["incoming"].strip().split("->")[-1] == "0":
                pytest_check.is_in("Unlimit", first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            else:
                incoming_value, incoming_unit = self._format_bps_custom(data["incoming"].strip().split("->")[-1])     # 转进率
                pytest_check.is_in(incoming_value, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
                pytest_check.is_in(incoming_unit, first_row_IncomingOutgoing_contents, msg="所在行数{}".format(inspect.currentframe().f_lineno))
        else:  # 不适用断言
            pass
        # 强制点击清空查询按钮
        element_clear = self.driver.find_element(By.ID, listPage_profileSearch_shaping_profile_buttonClear_posId)
        self.driver.execute_script("arguments[0].click()", element_clear)  # 强制点击
        # return self.first_row_ID_content
    
    # @screenshot_on_failure
    def modify(self, data):
        """
        修改数据，使用方法
        :param data:
        :return:
        """
        if data["model"].strip().lower() == "create":
            return 0
        # 进入编辑页面
        self.jump_edit_page()
        # 根据修改数据，重新输入limits
        self.select_limits(data, model=-1)
        # 点击ok
        self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_oK_posCss).click()
        if self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_warningSaveYes_posCss).is_displayed():
            self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_warningSaveYes_posCss).click()
    
    # @screenshot_on_failure
    def delete(self, is_del_all=False):
        """
        默认删除查询到的第一个结果
        :return:
        """
        if is_del_all == True:
            self.driver.find_element(By.XPATH, listPage_profileBottomPage_shaping_profile_button_allSelect_posXpath).click()    # 点击all按钮
        else:
            # 点击勾选第一行选择框
            self.first_row_checkBox_element.click()     # 变量来自查询函数
        # 调用profile的功能删除方法
        self.profile_pub_func.delete_profile(listPage_profile_shaping_profile_delButton_posId, listPage_dialogTips_shaping_profile_button_yes_posCss,
                                listPage_dialogTips_shaping_profile_button_no_posCss)
    
    # @screenshot_on_failure
    def select_type(self, data):
        """
        选择type类型点击
        :param data:
        :return:
        """
        type: str = data["type"].strip().lower()
        argument: str = data["argument"].strip().lower()
        if type == "generic":
            element_type_pos = shapingProfilePage_radioButton_generic_posXpath
        elif type == "fair share":
            element_type_pos = shapingProfilePage_radioButton_fairShare_posXpath
            if argument == "Max Min Host Fairness".lower():
                element_argument_pos = shapingProfilePage_radioButton_maxMinHostFairness_posXpath
            else:
                raise ValueError(f"用例参数argument：{argument}")
        else:
            element_type_pos = shapingProfilePage_radioButton_splitBy_posXpath
            if argument == "Local Host".lower():
                element_argument_pos = shapingProfilePage_radioButton_localHost_posXpath
            else:
                raise ValueError(f"用例参数argument：{argument}")
        # 点击type类型
        self.driver.find_element(By.XPATH, element_type_pos).click()
        # 判断是否点击argument
        if type != "generic":
            self.driver.find_element(By.XPATH, element_argument_pos).click()
    
    # @screenshot_on_failure
    def jump_sub_profile_page(self, vsys_name=""):
        """
        :param vsys_name:   Mvsys1    Default Vsys  或者为空字符串  空位当前默认vsys
        :return:
        """
        # 菜单操作,定位到shaping profile列表页
        self.driver.find_element(By.CSS_SELECTOR, mainPage_navigationBar_logo_posCss).click()
        self.profile_pub_func.change_vsys(vsys_name=vsys_name)
        self.driver.find_element(By.ID, mainPage_firstLevelMenu_profiles_posId).click()
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_shaping_profile_posId).click()
        
    # @screenshot_on_failure
    def select_limits(self, data, model=0):
        """
        输入limits
        :param data:
        :param model: =0表示创建时调用。-1表示修改时调用
        :return:
        """
        unitItem = data["unit"].strip().split("->")[model]
        element_dropDown_unitItem = shapingProfilePage_drowDown_unitItem_posXpath.format(replaceName=unitItem)
        # 点击unit并选择单位
        self.driver.find_element(By.ID, shapingProfilePage_inputSelect_unit_posId).click()
        self.driver.find_element(By.XPATH, element_dropDown_unitItem).click()
        # 输入incoming、outgoing
        input_incoming = data["incoming"].strip().split("->")[model]
        input_outgoing = data["outgoing"].strip().split("->")[model]
        self.driver.find_element(By.ID, shapingProfilePage_input_incoming_posId).clear()
        self.driver.find_element(By.ID, shapingProfilePage_input_incoming_posId).send_keys(input_incoming)
        self.driver.find_element(By.ID, shapingProfilePage_input_outgoing_posId).clear()
        self.driver.find_element(By.ID, shapingProfilePage_input_outgoing_posId).send_keys(input_outgoing)
        # 输入框不输入值测试用例
        if input_incoming == "空" or input_outgoing == "空":
            # 点击ok
            self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_oK_posCss).click()
            if input_incoming == "空":
                incoming_error_execpt = "Cannot be empty"
                ep_incoming_error = "//*[@id='{}']/{}".format(shapingProfilePage_input_incoming_posId, self.ep_error_part_path)
                incoming_error_info = self.driver.find_element(By.XPATH, ep_incoming_error).text.strip()
                pytest_check.is_in(incoming_error_execpt, incoming_error_info, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            if input_outgoing == "空":
                outgoing_error_execpt = "Cannot be empty"
                ep_outgoing_error = "//*[@id='{}']/{}".format(shapingProfilePage_input_outgoing_posId, self.ep_error_part_path)
                outgoing_error_info = self.driver.find_element(By.XPATH, ep_outgoing_error).text.strip()
                pytest_check.is_in(outgoing_error_execpt, outgoing_error_info, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            return 999
        else:
            # 输入框极限值之外判断
            input_incoming = int(input_incoming)
            input_outgoing = int(input_outgoing)
            if input_incoming > 1000000000000 or input_outgoing > 1000000000000:
                # 点击ok
                self.driver.find_element(By.CSS_SELECTOR, shapingProfilePage_button_oK_posCss).click()
                if input_incoming > 1000000000000:
                    incoming_error_execpt = "Cannot exceed 1000Gbps"
                    ep_incoming_error = "//*[@id='{}']/{}".format(shapingProfilePage_input_incoming_posId, self.ep_error_part_path)
                    incoming_error_info = self.driver.find_element(By.XPATH, ep_incoming_error).text.strip()
                    pytest_check.is_in(incoming_error_execpt, incoming_error_info, msg="所在行数{}".format(inspect.currentframe().f_lineno))
                if input_outgoing > 1000000000000:
                    outgoing_error_execpt = "Cannot exceed 1000Gbps"
                    ep_outgoing_error = "//*[@id='{}']/{}".format(shapingProfilePage_input_outgoing_posId, self.ep_error_part_path)
                    outgoing_error_info = self.driver.find_element(By.XPATH, ep_outgoing_error).text.strip()
                    pytest_check.is_in(outgoing_error_execpt, outgoing_error_info, msg="所在行数{}".format(inspect.currentframe().f_lineno))
                return 999
            else:
                # limit value符合要求
                return 1

    # @screenshot_on_failure
    def jump_edit_page(self):
        """
        默认选择第一个数据，并进入编辑页面
        :return:
        """
        #点击勾选第一行选择框
        self.first_row_checkBox_element.click()     #变量来自查询函数
        self.driver.find_element(By.ID, listPage_profile_shaping_profile_editButton_posId).click()