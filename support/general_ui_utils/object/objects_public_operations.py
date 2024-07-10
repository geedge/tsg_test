import configparser
import os
from selenium.webdriver.remote.webelement import WebElement
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
from workpath import workdir
from element_position.objects_element_position import *
from element_position import objects_element_position
from support.general_ui_utils.login_logout import loginout
from support.ui_utils.my_web_driver import MyWebDriver
from support.general_ui_utils.read_data import ReadData
from support.general_ui_utils.profile.profiles_public_operations import ProfilesPublicOperations
from support.general_ui_utils.workpath import workdir
from support.general_ui_utils.element_position.objects_element_position import *
from support.general_ui_utils.element_position.ln_objects_element_positionMERGELAST import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
from support.general_ui_utils.login_logout.loginout import LogInOut


# 下载文件《不需要实例化类》不写在类方法下
def download_files():
    my_files = ReadData()
    options = webdriver.ChromeOptions()

    options.add_argument("--incognito")  # 添加启用无痕模式的选项
    options.add_argument("--window-size=1920,1080")  # 启动时默认大小窗口
    options.add_argument('--headless')  # 启用Headless模式
    options.add_argument('--disable-gpu')  # 禁用 GPU 硬件加速

    prefs = {'download.default_directory': my_files._obj_files_dowload_path()}
    options.add_experimental_option('prefs', prefs)
    loginout_parse = configparser.ConfigParser()
    loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
    loginout_parse.read(loginout_parse_dir, encoding="utf-8")
    driver = MyWebDriver(
        command_executor=loginout_parse.get("remote_url", "url"),
        options=options)
    tsglogin_url = loginout_parse.get("tsg_url", "login_url")
    driver.get(tsglogin_url)
    driver.maximize_window()

    # Login
    # 需要判断，遇到https不安全时，点击高级-继续登录才可以访问https-tsg
    if "https" in tsglogin_url:
        print(2)
        driver.is_exist_element("//*[@id='details-button']")
        if driver.Exist:
            print(3)
            if "高级" in driver.find_element(By.XPATH, "//*[@id='details-button']").text.strip():
                print(4)
                driver.find_element(By.XPATH, "//*[@id='details-button']").click()
                driver.find_element(By.XPATH, "//*[@id='proceed-link']").click()
    # 输入账户和密码
    driver.find_element(By.NAME, loginPage_userName_posName).send_keys(loginout_parse.get("ui_account_1", "username"))
    driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(loginout_parse.get("ui_account_1", "passwd"))
    driver.find_element(By.ID, "login").click()
    myloginout = LogInOut
    # 消除右上角弹框
    close_button_elem_Xpath = '(//i[@class="iconfont icon-Delete_X"])[last()]'  # 全局右上提示窗关闭按钮（最新的一个）
    driver.is_exist_element(close_button_elem_Xpath)
    loop_count = 2
    while loop_count > 0:
        try:
            driver.is_exist_element(close_button_elem_Xpath)
            if driver.Exist:
                driver.find_element(By.XPATH, close_button_elem_Xpath).click()
            loop_count -= 1
        except:
            loop_count -= 1
            pass
    # 切换至默认ui_vsys
    # loginout_parse = configparser.ConfigParser()
    # loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
    loginout_parse.read(loginout_parse_dir, encoding="utf-8")
    # 切换UI自动化使用vsys
    vsys_name = loginout_parse.get("vsys", "vsys_name")  # 登录后vsys切换为UIAutoTestVsys
    # print(vsys_name)
    profile_pub = ProfilesPublicOperations(driver)
    profile_pub.change_vsys(vsys_name=vsys_name)
    # 默认更改为英语
    # myloginout._default_language()
    return driver


def _vsys_account():
    options = webdriver.ChromeOptions()
    loginout_parse = configparser.ConfigParser()
    loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
    loginout_parse.read(loginout_parse_dir, encoding="utf-8")
    driver = MyWebDriver(
        command_executor=loginout_parse.get("remote_url", "url"),
        options=options)
    tsglogin_url = loginout_parse.get("tsg_url", "login_url")
    driver.get(tsglogin_url)
    driver.maximize_window()
    driver.find_element(By.XPATH, "//div[1]/div/div[1]/div[2]/div[2]/div/input").send_keys(
        loginout_parse.get("ui_vsys_Case_1", "username"))
    driver.find_element(By.XPATH, "//div/div[1]/div[2]/div[3]/div/input").send_keys(
        loginout_parse.get("ui_vsys_Case_1", "passwd"))
    driver.find_element(By.ID, "login").click()
    login = loginout()
    login.dismiss_rightTopTips()
    return driver


def get_txt_filenames(path):  # 《不需要实例化类》不写在类方法下
    filenames = []
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            filenames.append(filename)

    return str(filenames[0])


def get_lua_filenames(path):  # 《不需要实例化类》不写在类方法下
    filenames = []
    for filename in os.listdir(path):
        if filename.endswith('.lua'):
            filenames.append(filename)

    return str(filenames[0])


class ObjectsPublicOperations:
    def __init__(self, driver):
        self.driver = driver
        self.my_files = ReadData()
        self.loginout_parse = configparser.ConfigParser()
        self._query = 1
        loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
        self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")

    # 修改内容时，当内容为value，不是text时使用
    def clear_Name(self, path):
        """
        清除输入框内容
        :param path: path 也可是Selenium元素 XD
        :return:
        """
        # print("goTo_input {}".format(pathOrElement), type(pathOrElement))
        if isinstance(path, WebElement):  # 变量是WebElement类型
            element = path
        else:  # path
            element = self.driver.find_element(By.XPATH, path)
        # element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.CONTROL + 'A')
        element.send_keys(Keys.DELETE)

    def assert_len_Name(self, data):
        j = 0
        for i in data["Name"]:
            j += 1
        return j

    def clear_name_by_id(self, id):
        element = self.driver.find_element(By.ID, id)
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.DELETE)

    # 提取ID、Name、Description、Detail
    def extract_ele(self, need_exclude=1):
        """
        :param need_exclude: 是否需要获取exclude，默认1则获取，不为1则略过
        :return:
        """
        # self.driver.is_exist_element(Element='//div/div[3]/table/tbody/tr[1]')  # 查看第一行是否存在数据
        self.driver.is_exist_element(
            Element='((//div[@class!="itemDetails cursor"]//table[@class="el-table__body"])[1]//tr)[1]')  # 查看第一行是否存在数据
        if self.driver.Exist:
            # 展示所有列
            self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath).click()  # 点击列设置
            all_checked_xpath = '//*[@class="all-btn"]//*[@class="el-checkbox__input is-checked"]'
            if self.driver.is_exist_element_by_value(By.XPATH, all_checked_xpath):  # 如果全选被选中
                self.driver.find_element(By.XPATH,
                                         mainPage_ObjectSearch_Column_settings_click_Cancel_Button_posXpath).click()  # 点击Cancel按钮
            else:
                self.driver.find_element(By.XPATH,
                                         mainPage_ObjectSearch_Column_settings_select_allCheckBox_posXpath).click()  # 全选
                self.driver.find_element(By.XPATH,
                                         mainPage_ObjectSearch_Column_settings_click_OK_Button_posXpath).click()  # 点击OK按钮

            # 公共方法 Detail特殊，需要使用时特殊提取
            list_headers_template = '//div[@class="el-table__header-wrapper"]//span[text()="{}"]'
            list_firstRow_values_template = '//div[contains(@class,"el-table__body-wrapper")]//tr[1]//td[count({a}/../../../preceding-sibling::th)+1]{b}'

            list_headers_id_posXpath = list_headers_template.format("ID")
            list_headers_vsys_id_posXpath = list_headers_template.format("Vsys ID")
            list_headers_name_posXpath = list_headers_template.format("Name")

            list_headers_description_posXpath = list_headers_template.format("Description")
            list_headers_refer_count_posXpath = list_headers_template.format("Reference Count")

            list_firstRow_values_id_posXpath = list_firstRow_values_template.format(a=list_headers_id_posXpath,
                                                                                    b='//div[@class="table-status-item-id"]//span')
            list_firstRow_values_vsys_id_posXpath = list_firstRow_values_template.format(
                a=list_headers_vsys_id_posXpath, b='//*[text()]')
            list_firstRow_values_name_posXpath = list_firstRow_values_template.format(a=list_headers_name_posXpath,
                                                                                      b='//span')

            list_firstRow_values_description_posXpath = list_firstRow_values_template.format(
                a=list_headers_description_posXpath, b='//span') + "|" + list_firstRow_values_template.format(
                a=list_headers_description_posXpath, b='//p')
            list_firstRow_values_refer_count_posXpath = list_firstRow_values_template.format(
                a=list_headers_refer_count_posXpath, b='//div[contains(@class,"textCenter")]')

            self.key_id = self.driver.find_element(By.XPATH, list_headers_id_posXpath).text
            self.value_id = self.driver.find_element(By.XPATH, list_firstRow_values_id_posXpath).text
            self.key_vsys_id = self.driver.find_element(By.XPATH, list_headers_vsys_id_posXpath).text
            self.value_vsys_id = self.driver.find_element(By.XPATH, list_firstRow_values_vsys_id_posXpath).text
            self.key_name = self.driver.find_element(By.XPATH, list_headers_name_posXpath).text
            self.value_name = self.driver.find_element(By.XPATH, list_firstRow_values_name_posXpath).text

            self.key_des = self.driver.find_element(By.XPATH, list_headers_description_posXpath).text
            self.value_des = self.driver.find_element(By.XPATH, list_firstRow_values_description_posXpath).text
            self.key_refer_count = self.driver.find_element(By.XPATH, list_headers_refer_count_posXpath).text
            self.value_refer_count = self.driver.find_element(By.XPATH, list_firstRow_values_refer_count_posXpath).text

            if need_exclude == 1:
                list_headers_exclude_posXpath = list_headers_template.format("Exclude Members")
                list_firstRow_values_exclude_posXpath = list_firstRow_values_template.format(
                    a=list_headers_exclude_posXpath,
                    b='//div[@class="bifangWidth"]|div[@class="three-row list-popover-click"]')
                self.key_exclude = self.driver.find_element(By.XPATH, list_headers_exclude_posXpath).text
                self.value_exclude = self.driver.find_element(By.XPATH, list_firstRow_values_exclude_posXpath).text
                self.table_dict = {self.key_id: self.value_id, self.key_vsys_id: self.value_vsys_id,
                                   self.key_name: self.value_name, self.key_exclude: self.value_exclude,
                                   self.key_des: self.value_des,
                                   "Datails": "null", self.key_refer_count: self.value_refer_count}

            else:
                self.table_dict = {self.key_id: self.value_id, self.key_vsys_id: self.value_vsys_id,
                                   self.key_name: self.value_name, self.key_des: self.value_des,
                                   "Datails": "null", self.key_refer_count: self.value_refer_count}
            print("extract_ele TEST:{}".format(self.table_dict))

        #     try:
        #         self.driver.is_exist_element(Element=list_second_row_sixth_column_posXpath)
        #         if self.driver.Exist:
        #             self.value26 = self.driver.find_element(By.XPATH, list_second_row_sixth_column_posXpath).text
        #         else:
        #             self.driver.is_exist_element(Element='//table/tbody/tr[1]/td[6]/div/span')
        #             if self.driver.Exist:
        #                 self.value26 = self.driver.find_element(By.XPATH, '//table/tbody/tr[1]/td[6]/div/span').text
        #             else:
        #                 self.value26 = "null"
        #     except:
        #         pass
        #     self.table_dict = {self.key11: self.value12, self.key12: self.value22, self.key13: self.value23,
        #                        "Datails": "null", self.key15: self.value25, self.key16: self.value26}
        # else:
        #     assert self.driver.Exist

    # def extract_ele(self):
    #     # self.driver.is_exist_element(Element='//div/div[3]/table/tbody/tr[1]')  # 查看第一行是否存在数据
    #     self.driver.is_exist_element(Element='((//div[@class!="itemDetails cursor"]//table[@class="el-table__body"])[1]//tr)[1]')  # 查看第一行是否存在数据
    #     if self.driver.Exist:
    #         # 公共方法 Detail特殊，需要使用时特殊提取
    #         # ID
    #         self.key11 = self.driver.find_element(By.XPATH, list_first_row_first_column_posXpath).text
    #         self.value12 = self.driver.find_element(By.XPATH, list_second_row_first_column_posXpath).text
    #         # Vsy_ID
    #         self.key12 = self.driver.find_element(By.XPATH, list_first_row_second_column_posXpath).text
    #         self.value22 = self.driver.find_element(By.XPATH, list_second_row_second_column_posXpath).text
    #         # Name
    #         self.key13 = self.driver.find_element(By.XPATH, list_first_row_third_column_posXpath).text
    #         self.value23 = self.driver.find_element(By.XPATH, list_second_row_third_column_posXpath).text
    #         # Exclude Members
    #         self.key15 = self.driver.find_element(By.XPATH, list_first_row_fifth_column_posXpath).text
    #         self.value25 = self.driver.find_element(By.XPATH, list_second_row_fifth_column_posXpath).text
    #         # Description
    #         self.key16 = self.driver.find_element(By.XPATH, list_first_row_sixth_column_posXpath).text
    #         try:
    #             self.driver.is_exist_element(Element=list_second_row_sixth_column_posXpath)
    #             if self.driver.Exist:
    #                 self.value26 = self.driver.find_element(By.XPATH, list_second_row_sixth_column_posXpath).text
    #             else:
    #                 self.driver.is_exist_element(Element='//table/tbody/tr[1]/td[6]/div/span')
    #                 if self.driver.Exist:
    #                     self.value26 = self.driver.find_element(By.XPATH, '//table/tbody/tr[1]/td[6]/div/span').text
    #                 else:
    #                     self.value26 = "null"
    #         except:
    #             pass
    #         self.table_dict = {self.key11: self.value12, self.key12: self.value22, self.key13: self.value23,
    #                            "Datails": "null", self.key15: self.value25, self.key16: self.value26}
    #     else:
    #         assert self.driver.Exist

    # print(self.table_dict)

    # if data["Createmodel"] == "0" and data["Createtype"] != "IP_Learnig":
    #     self.Details = self.driver.find_element(By.XPATH,listPage_object_mobileIdentities_new_Details_extract_posXpath).text
    # self.ID = self.driver.find_element(By.XPATH,listPage_object_mobileIdentities_new_ID_extract_posXpath).text
    # self.Name = self.driver.find_element(By.XPATH,listPage_object_mobileIdentities_new_Name_extract_posXpath).text
    # self.Description = self.driver.find_element(By.XPATH,listPage_object_mobileIdentities_new_Description_extract_posXpath).text

    def licenese_Check(self):
        try:
            self.driver.is_exist_element(Element='//div/div[1]/div[2]/div/div/div[3]/i')
            if self.driver.Exist:
                self.driver.find_element(By.XPATH, '//div/div[1]/div[2]/div/div/div[3]/i').click()
            else:
                pass
        except:
            pass

    # 修改后元素===》断言
    def assert_ele(self):
        self.driver.is_exist_element(Element='//div/div[3]/table/tbody/tr[1]')  # 查看第一行是否存在数据
        if self.driver.Exist:
            # ID
            self.key11 = self.driver.find_element(By.XPATH, list_first_row_first_column_posXpath).text
            self.value12 = self.driver.find_element(By.XPATH, list_second_row_first_column_posXpath).text
            # Vsy_ID
            self.key12 = self.driver.find_element(By.XPATH, list_first_row_second_column_posXpath).text
            self.value22 = self.driver.find_element(By.XPATH, list_second_row_second_column_posXpath).text
            # Name
            self.key13 = self.driver.find_element(By.XPATH, list_first_row_third_column_posXpath).text
            self.value23 = self.driver.find_element(By.XPATH, list_second_row_third_column_posXpath).text
            # Details特殊，需要使用时特殊提取
            # Exclude Members
            self.key15 = self.driver.find_element(By.XPATH, list_first_row_fifth_column_posXpath).text
            self.value25 = self.driver.find_element(By.XPATH, list_second_row_fifth_column_posXpath).text
            # Description
            self.key16 = self.driver.find_element(By.XPATH, list_first_row_sixth_column_posXpath).text
            try:
                self.driver.is_exist_element(Element=list_second_row_sixth_column_posXpath)
                if self.driver.Exist:
                    self.value26 = self.driver.find_element(By.XPATH, list_second_row_sixth_column_posXpath).text
                else:
                    self.driver.is_exist_element(Element='//table/tbody/tr/td[6]/div//span')
                    if self.driver.Exist:
                        self.value26 = self.driver.find_element(By.XPATH, '//table/tbody/tr/td[6]/div//span').text
            except:
                self.value26 = "null"

            self.edit_table_dict = {self.key11: self.value12, self.key12: self.value22, self.key13: self.value23,
                                    "Datails": "null", self.key15: self.value25, self.key16: self.value26}
        else:
            assert self.driver.Exist

    #   根据"->"进行分割，进行修改
    def Modify_object(self, data):
        self.output = data.get("Name")
        self.Name_list = self.output.split("->")
        # 判断是否需要修改Name
        self.create_name = self.Name_list[0]
        try:
            self.modify_name = self.Name_list[1]
        except:
            self.modify_name = None

    # 下载文件
    def download_files(self):
        my_files = ReadData()
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': my_files._obj_files_dowload_path()}
        options.add_experimental_option('prefs', prefs)
        driver = MyWebDriver(
            command_executor=self.loginout_parse.get("remote_url", "url"),
            options=options)
        return driver

    def _split_assert(self, assert_content):
        self.count = assert_content.split("Total:")
        self.after_count = int(self.count[1]) + 1
        return "Total:{}".format(self.after_count)

    def Column_settings(self, Column):
        # 24.02待修改-已修改
        # 点击列设置
        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath).click()
        # 全不选并确认
        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_select_allCheckBox_posXpath).click()
        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_select_allCheckBox_posXpath).click()
        # self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_select_Cancel_Button_posXpath).click()
        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_click_OK_Button_posXpath).click()
        # 全不选,选择展示Column并确认
        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath).click()
        self.Column_text = self.driver.find_element(By.XPATH, Column).text
        # print(self.Column_text)
        self.driver.find_element(By.XPATH, Column).click()  # 选择目标Column
        self.driver.find_element(By.XPATH,
                                 mainPage_ObjectSearch_Column_settings_click_OK_Button_posXpath).click()  # 点击OK按钮
        self.Column_ele_ex(Column_text=self.Column_text)  # 调用校验方法
        # 全选并确认
        # self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath).click() # 点击列设置
        # self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_select_All_Button_posXpath).click()
        # self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_click_OK_Button_posXpath).click()

        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath).click()  # 点击列设置
        self.driver.find_element(By.XPATH,
                                 mainPage_ObjectSearch_Column_settings_select_allCheckBox_posXpath).click()  # 全选
        self.driver.find_element(By.XPATH,
                                 mainPage_ObjectSearch_Column_settings_click_OK_Button_posXpath).click()  # 点击OK按钮
        # 全选并取消
        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath).click()  # 点击列设置
        self.driver.find_element(By.XPATH,
                                 mainPage_ObjectSearch_Column_settings_select_allCheckBox_posXpath).click()  # 全选
        self.driver.find_element(By.XPATH,
                                 mainPage_ObjectSearch_Column_settings_click_Cancel_Button_posXpath).click()  # 点击Cancel按钮

    def View_statistics(self, edit_element):
        # 主界面View验证
        self.driver.find_element(By.XPATH, main_listPage_object_statistics_view_postXpath).click()
        self.driver.is_exist_element(Element="(//div[@class='ObjectStatisticSlider'])[1]")
        assert self.driver.Exist, "Statistics界面打开"
        self.driver.find_element(By.XPATH, "(//div[@class='ObjectStatisticSlider']//span[text()='Cancel'])[2]").click()
        # 详情界面Statistics验证
        self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()
        self.driver.find_element(By.ID, edit_element).click()
        self.driver.find_element(By.XPATH, "//div[@class='paper-grid-right']//span[text()='Statistics']").click()
        self.driver.is_exist_element(Element="(//div[@class='ObjectStatisticSlider'])[1]")
        assert self.driver.Exist, "Statistics界面打开"

    def Duplicate_check(self, data):
        self.driver.is_exist_element(Element=listPage_object_reprtition_check_postXpath)
        assert self.driver.Exist, "重复ip"
        if data["Search_type"] == "Name":
            self.driver.find_element(By.XPATH, listPage_object_reprtition_check_postXpath).click()
            self.total_count = self.driver.find_element(By.XPATH,
                                                        "//div[@class='tab-content floatleft height100 width100']/p").text
            self.count = self.total_count.split("Total:")
            print(self.count[1])
            assert self.count[1] == '1'

    # 判断列元素
    def Column_ele_ex(self, Column_text):
        data = "//div/div/div[1]/div/div[2]/div/div[2]/table/thead/tr/th['replace']"
        # for i in range(1, 13):
        self.result = True
        i = 1
        while self.result == False:
            if i == 1:
                self.title = data.replace("th['replace']", "th[{}]/div/span/span[1]".format(i))
                self.title_text = self.driver.find_element(By.XPATH, self.title)
                if Column_text == self.title_text:
                    self.result = True
                    break
                else:
                    i += 1

            else:
                self.title = data.replace("th['replace']", "th[{}]/div/div/span".format(i))
                self.title_text = self.driver.find_element(By.XPATH, self.title)
                if Column_text == self.title_text:
                    self.result = True
                    break
                else:
                    i += 1

    # 翻页操作
    def pages_turning(self, data, page_flag=1):
        """
        页码跳转
        :param data:
        :param page_flag: 1-Object列表页，2-对象组添加对象时的侧滑列表页
        :return:
        data示例：{
          "ids": "翻页操作T014-1",
          "//": "注释！直接跳转至对应页面，如destination_page为0则进行随机遍历跳转",
          "turn_mode": 1,
          "destination_page": "0"
          },
        :param page_flag: 1-Object列表页，2-对象组添加对象时的侧滑列表页
        """

        # self.driver.implicitly_wait(5)
        turn_mode = data["turn_mode"]  # data中翻页模式
        destination_page_number = data["destination_page"]  # data中目标页码
        self.turn_page_falg = 1

        listPage_max_page_elem_is_exist = self.driver.is_exist_element_by_value(By.XPATH,
                                                                      listPage_object_pages_maxPageNumber_posXpath)
        DrawerlistPage_max_page_elem_is_exist = self.driver.is_exist_element_by_value(By.XPATH,
                                                                            DrawerlistPage_object_pages_maxPageNumber_posXpath)
        if listPage_max_page_elem_is_exist or DrawerlistPage_max_page_elem_is_exist:  # 存在页码
            if page_flag == 1:  # 1-Object列表页

                # 获取页面中最大页码
                max_page_elem_Xpath = listPage_object_pages_maxPageNumber_posXpath
                max_page_number = self.driver.find_element(By.XPATH, max_page_elem_Xpath).text
                # print("max_page_number:{}".format(max_page_number))
                # 前一页按钮
                previousPage_button = self.driver.find_element(By.XPATH,
                                                               listPage_object_pages_previousPage_button_poxXpath)
                # 后一页按钮
                nextPage_button = self.driver.find_element(By.XPATH, listPage_object_pages_nextPage_button_poxXpath)
                # Goto 输入框
                goTo_input = self.driver.find_element(By.XPATH, listPage_object_pages_goTo_input_poxXpath)
                # 当前页码元素
                currentPageNumber_posXpath = listPage_object_pages_currentPageNumber_posXpath
                # 页面中目标页码元素模板
                destination_page_elem_XpathTemple = '//div[@class="page-box-containcheck"]//li[text()={}]'
                # # 快速后翻页按钮Xpath
                # quicNext_button_Xpath = listPage_object_pages_quickNextPage_button_poxXpath
                # # 快速前翻页按钮Xpath
                # quickPrevious_button_Xpath = listPage_object_pages_quickPreviousPage_button_poxXpath
            else:  # 2-对象组添加对象时的侧滑列表页
                # 获取页面中最大页码
                max_page_elem_Xpath = DrawerlistPage_object_pages_maxPageNumber_posXpath
                max_page_number = self.driver.find_element(By.XPATH, max_page_elem_Xpath).text
                # print("max_page_number:{}".format(max_page_number))
                # 前一页按钮
                previousPage_button = self.driver.find_element(By.XPATH,
                                                               DrawerlistPage_object_pages_previousPage_button_poxXpath)
                # 后一页按钮
                nextPage_button = self.driver.find_element(By.XPATH,
                                                           DrawerlistPage_object_pages_nextPage_button_poxXpath)
                # Goto 输入框
                goTo_input = self.driver.find_element(By.XPATH, DrawerlistPage_object_pages_goTo_input_poxXpath)
                # 当前页码元素
                currentPageNumber_posXpath = DrawerlistPage_object_pages_currentPageNumber_posXpath
                # 页面中目标页码元素模板
                destination_page_elem_XpathTemple = '//div[@class="ToggleDraw"]//li[text()={}]'

                # # 快速后翻页按钮Xpath
                # quicNext_button_Xpath = listPage_object_pages_quickNextPage_button_poxXpath
                # # 快速前翻页按钮Xpath
                # quickPrevious_button_Xpath = listPage_object_pages_quickPreviousPage_button_poxXpath

            if int(max_page_number) == 1:  # 只有1页则跳过
                self.turn_page_falg = 0
                try:
                    # 切换至Vsys0
                    loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
                    self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")
                    vsys_name = self.loginout_parse.get("vsys0", "vsys_name")
                    profile_pub = ProfilesPublicOperations(self.driver)
                    profile_pub.change_vsys(vsys_name=vsys_name)
                    # self.driver.implicitly_wait(4)

                    max_page_number_elem = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, max_page_elem_Xpath))
                    )
                    max_page_number = max_page_number_elem.text
                    if int(max_page_number) == 1:  # 只有1页则跳过
                        self.driver.refresh()
                        raise Exception("页码仅为1页，无法进行翻页操作！")
                        # pytest.skip("页码仅为1页，无法进行翻页操作！")
                    else:
                        self._turn_page(turn_mode, destination_page_number, max_page_number, previousPage_button,
                                        nextPage_button,
                                        goTo_input, currentPageNumber_posXpath, destination_page_elem_XpathTemple)
                except Exception as e:
                    print(e)
            else:
                self._turn_page(turn_mode, destination_page_number, max_page_number, previousPage_button,
                                nextPage_button,
                                goTo_input, currentPageNumber_posXpath, destination_page_elem_XpathTemple)
        else:
            print(" 无页码元素，无法进行翻页操作--跳过")
            pass

    def _turn_page(self, turn_mode, destination_page_number, max_page_number, previousPage_button, nextPage_button,
                   goTo_input, currentPageNumber_posXpath, destination_page_elem_XpathTemple):
        if turn_mode == 1:  # 直接跳转至对应页面，如destination_page为0则进行随机跳转
            if destination_page_number == "0" or int(destination_page_number) > int(
                    max_page_number):  # 如destination_page为0或大于最大页码则进行随机跳转
                # 随机页码list
                # random_list = [(lambda a, b: random.randrange(a, b + 1))(1, int(max_page_number)) for i in
                #                range(int(int(max_page_number) / 2))]
                list_lenth = int(int(max_page_number) / 2)
                if list_lenth > 10:
                    list_lenth = 10
                    random_list = [(lambda a, b: random.randrange(a, b + 1))(1, int(max_page_number)) for i in
                                   range(list_lenth)]  # 10个随机页码，视情况自定义
                else:
                    random_list = [(lambda a, b: random.randrange(a, b + 1))(1, int(max_page_number)) for i in
                                   range(list_lenth)]
                    print("--------------------------------random_list:{}".format(random_list))
                for i in random_list:
                    # 或取页面中目标页码元素
                    destination_page_elem_Xpath = destination_page_elem_XpathTemple.format(i)

                    print("--------------------------------before _operate_turn_pages")
                    self._operate_turn_pages(i, destination_page_elem_Xpath, currentPageNumber_posXpath, goTo_input)
                    print("--------------------------------after _operate_turn_pages")
                    destination_page_elem = self.driver.find_element(By.XPATH, destination_page_elem_Xpath)
                    destination_page_elem.click()
                    current_page_number = self.driver.find_element(By.XPATH,
                                                                   currentPageNumber_posXpath).text
                    # print("current_page_number:{a}|destination_page_number:{b}".format(a=current_page_number, b=str(i)))
                    assert current_page_number == str(i), "校验页码跳转失败！！"
            else:  # 正常跳转至目标页
                destination_page_elem_Xpath = destination_page_elem_XpathTemple.format(
                    destination_page_number)
                self._operate_turn_pages(destination_page_number, destination_page_elem_Xpath,
                                         currentPageNumber_posXpath, goTo_input)
                destination_page_elem = self.driver.find_element(By.XPATH, destination_page_elem_Xpath)
                destination_page_elem.click()
                assert self.driver.find_element(By.XPATH,
                                                currentPageNumber_posXpath).text == str(
                    destination_page_number), "校验页码跳转失败！！"
                print("翻页成功，{}".format(self.driver.find_element(By.XPATH,
                                                                    currentPageNumber_posXpath).text))

        elif turn_mode == 2:  # 使用前一页或后一页按钮进行翻页，如destination_page为0则进行随机跳转
            if destination_page_number == "0" or int(destination_page_number) > int(
                    max_page_number):  # 如destination_page为0或大于最大页码则进行随机跳转
                random_page_number = random.randint(1, int(max_page_number))
                # print("random_page_number:{}".format(random_page_number))
                current_page_number = self.driver.find_element(By.XPATH,
                                                               currentPageNumber_posXpath).text
                while int(current_page_number) != random_page_number:
                    if int(current_page_number) < random_page_number:
                        nextPage_button.click()
                        current_page_number = self.driver.find_element(By.XPATH,
                                                                       currentPageNumber_posXpath).text
                    elif int(current_page_number) > random_page_number:
                        previousPage_button.click()
                        current_page_number = self.driver.find_element(By.XPATH,
                                                                       currentPageNumber_posXpath).text
                    else:
                        break
                # print("current_page_number:{a}|destination_page_number:{b}".format(a=current_page_number,
                #                                                                    b=str(random_page_number)))
                assert self.driver.find_element(By.XPATH,
                                                currentPageNumber_posXpath).text == str(
                    random_page_number), "校验页码跳转失败！！"

            else:  # 正常跳转至目标页
                current_page_number = self.driver.find_element(By.XPATH,
                                                               currentPageNumber_posXpath).text
                while current_page_number != destination_page_number:
                    if int(current_page_number) < int(destination_page_number):
                        nextPage_button.click()
                        current_page_number = self.driver.find_element(By.XPATH,
                                                                       currentPageNumber_posXpath).text
                    elif int(current_page_number) > int(destination_page_number):
                        previousPage_button.click()
                        current_page_number = self.driver.find_element(By.XPATH,
                                                                       currentPageNumber_posXpath).text
                    else:
                        break
                # print("current_page_number:{a}|destination_page_number:{b}".format(a=current_page_number,
                #                                                                    b=destination_page_number))
                assert self.driver.find_element(By.XPATH,
                                                currentPageNumber_posXpath).text == str(
                    destination_page_number), "校验页码跳转失败！！"
        elif turn_mode == 3:  # 使用Go to页码数进行翻页，如destination_page为0则进行随机跳转
            if destination_page_number == "0" or int(destination_page_number) > int(
                    max_page_number):  # 如destination_page为0或大于最大页码则进行随机跳转
                random_page_number = random.randint(1, int(max_page_number))
                self.clear_Name(goTo_input)
                # 搜索框中键入搜索值
                goTo_input.send_keys(random_page_number)
                # 确认并执行跳转
                goTo_input.send_keys(Keys.ENTER)  # 输入框中执行回车

                # current_page_number = self.driver.find_element(By.XPATH,
                #                                                currentPageNumber_posXpath).text

                # print("current_page_number:{a}|destination_page_number:{b}".format(a=current_page_number,
                #                                                                    b=str(random_page_number)))
                assert self.driver.find_element(By.XPATH,
                                                currentPageNumber_posXpath).text == str(
                    random_page_number), "校验页码跳转失败！！"

            else:  # 正常跳转至目标页
                self.clear_Name(goTo_input)
                # 搜索框中键入搜索值
                goTo_input.send_keys(destination_page_number)
                # 确认并执行跳转
                goTo_input.send_keys(Keys.ENTER)  # 输入框中执行回车
                # current_page_number = self.driver.find_element(By.XPATH,
                #                                                currentPageNumber_posXpath).text

                # print("current_page_number:{a}|destination_page_number:{b}".format(a=current_page_number,
                #                                                                    b=str(destination_page_number)))
                assert self.driver.find_element(By.XPATH,
                                                currentPageNumber_posXpath).text == str(
                    destination_page_number), "校验页码跳转失败！！"

        elif turn_mode == 4:  # 使用快速翻页按钮进行翻页，如destination_page为0则进行随机跳转
            if int(max_page_number) <= 6:
                pass
            else:
                if destination_page_number == "0" or int(destination_page_number) > int(
                        max_page_number):  # 如destination_page为0或大于最大页码则进行随机跳转
                    list_lenth = int(int(max_page_number) / 2)
                    if list_lenth > 10:
                        list_lenth = 10
                        # 随机页码list
                        random_list = [(lambda a, b: random.randrange(a, b + 1))(6, int(max_page_number)) for i in
                                       range(list_lenth)]
                    else:
                        random_list = [(lambda a, b: random.randrange(a, b + 1))(1, int(max_page_number)) for i in
                                       range(list_lenth)]
                    # print("random_list:{}".format(random_list))
                    for i in random_list:
                        # 或取页面中目标页码元素
                        destination_page_elem_Xpath = destination_page_elem_XpathTemple.format(
                            i)

                        self._operate_turn_pages(i, destination_page_elem_Xpath, currentPageNumber_posXpath, goTo_input)
                        destination_page_elem = self.driver.find_element(By.XPATH, destination_page_elem_Xpath)
                        destination_page_elem.click()
                        current_page_number = self.driver.find_element(By.XPATH,
                                                                       currentPageNumber_posXpath).text
                        # print("current_page_number:{a}|destination_page_number:{b}".format(a=current_page_number,
                        #                                                                    b=str(i)))
                        assert current_page_number == str(i), "校验页码跳转失败！！"
                else:  # 正常跳转至目标页
                    destination_page_elem_Xpath = destination_page_elem_XpathTemple.format(
                        destination_page_number)
                    self._operate_turn_pages(destination_page_number, destination_page_elem_Xpath,
                                             currentPageNumber_posXpath, goTo_input)
                    destination_page_elem = self.driver.find_element(By.XPATH, destination_page_elem_Xpath)
                    destination_page_elem.click()
                    assert self.driver.find_element(By.XPATH,
                                                    currentPageNumber_posXpath).text == str(
                        destination_page_number), "校验页码跳转失败！！"

    def _operate_turn_pages(self, destination_page, destination_page_elem_Xpath, currentPageNumber_posXpath,
                            goTo_input):
        """
        针对页码快速跳转操作
        :param destination_page: 上层传递的目标页码
        :param destination_page_elem_Xpath: 上层传递的目标页码元素的Xpath
        :param currentPageNumber_posXpath: 上层传递的当前页码元素的Xpath
        :param goTo_input: 上层传递的Goto输入框元素的Xpath
        :return:
        """
        if int(destination_page) > 20:
            # print(f"destination_page{destination_page}")
            self.clear_Name(goTo_input)
            goTo_input.send_keys(int(destination_page) - 9)
            # 确认并执行跳转
            goTo_input.send_keys(Keys.ENTER)  # 输入框中执行回车
        while True:  # 判断目标页码元素是否存在
            print("----------------In while")
            self.driver.is_exist_element(Element=destination_page_elem_Xpath)
            # print("is_exist_element:{}".format(self.driver.Exist))
            current_page_number = self.driver.find_element(By.XPATH,
                                                           currentPageNumber_posXpath).text
            if not self.driver.Exist:
                print("-----------quick exist!!!!")

                if int(destination_page) > int(current_page_number):
                    # time.sleep(0.1)
                    self.driver.find_element(By.XPATH, listPage_object_pages_quickNextPage_button_poxXpath).click()
                elif int(destination_page) < int(current_page_number):
                    # time.sleep(0.1)
                    self.driver.find_element(By.XPATH, listPage_object_pages_quickPreviousPage_button_poxXpath).click()
            else:
                print("-----------quick not exist!!!! break")
                break

    # def pages_turning_case(self):
    #     # 1、获取当前页码 2、点击下一页翻页 3、断言翻页后，页码为当前页码+1
    #     self.current_page = int(
    #         self.driver.find_element(By.XPATH, listPage_object_pages_currentPageNumber_posXpath).text)
    #     self.max_page = int(
    #         self.driver.find_element(By.XPATH, listPage_object_pages_currentPageArea_MaxNumber_posXpath).text)
    #     if self.max_page > self.current_page:
    #         self.driver.find_element(By.XPATH, listPage_object_pages_nextPage_button_poxXpath).click()
    #         assert self.current_page + 1 == int(
    #             self.driver.find_element(By.XPATH, listPage_object_pages_currentPageNumber_posXpath).text)
    #     # 2、获取当前页码 2、点击上一页翻页 3、断言翻页后，页码展示为当前页码-1
    #     self.current_page = int(
    #         self.driver.find_element(By.XPATH, listPage_object_pages_currentPageNumber_posXpath).text)
    #     if self.current_page > 1:
    #         self.driver.find_element(By.XPATH, listPage_object_pages_previousPage_button_poxXpath).click()
    #         assert self.current_page - 1 == int(
    #             self.driver.find_element(By.XPATH, listPage_object_pages_currentPageNumber_posXpath).text)
    #     # 3、输入页码回车进行翻页
    #     self.max_page = int(
    #         self.driver.find_element(By.XPATH, listPage_object_pages_currentPageArea_MaxNumber_posXpath).text)
    #     if self.max_page <= 2:
    #         pass
    #     elif self.max_page > 2:
    #         self.clear_Name(path=listPage_object_pages_goTo_input_poxXpath)
    #         self.driver.find_element(By.XPATH, listPage_object_pages_goTo_input_poxXpath).send_keys(
    #             str(self.max_page / 2 + 1) + Keys.ENTER)
    #         assert int(self.max_page / 2 + 1) == int(self.driver.find_element(By.XPATH,
    #                                                                           listPage_object_pages_currentPageNumber_posXpath).text), "断言所翻页码处于当前页"
    #     # 4、点击第五页进行翻页
    #     self.driver.is_exist_element(Element=listPage_object_pages_currentPageAreaMaxNumber_posXpath)
    #     if self.driver.Exist:
    #         self.last_page = int(
    #             self.driver.find_element(By.XPATH, listPage_object_pages_currentPageAreaMaxNumber_posXpath).text)
    #         self.driver.find_element(By.XPATH, listPage_object_pages_currentPageAreaMaxNumber_posXpath).click()
    #         assert self.last_page == int(self.driver.find_element(By.XPATH,
    #                                                               listPage_object_pages_currentPageNumber_posXpath).text), "断言所翻页码处于当前页"
    #     else:
    #         pass

    # 判断元素是否可点击
    def is_element_clickable(self, elm, elm_type="XPATH"):
        """判断元素是否存在
        :param elm: 元素定位
        :param elm_type: 元素定位方式
        :return: 是否可点击
        """
        try:
            # 设置一个最大等待时间
            timeout = WebDriverWait(self.driver, 5)
            if elm_type == 'ID':
                # 等待元素可点击
                timeout.until(EC.element_to_be_clickable((By.ID, elm)))
                return True
            elif elm_type == 'XPATH':
                # 等待元素可点击
                timeout.until(EC.element_to_be_clickable((By.XPATH, elm)))
                return True
            elif elm_type == 'CSS_SELECTOR':
                # 等待元素可点击
                timeout.until(EC.element_to_be_clickable((By.CSS_SELECTOR, elm)))
                return True
            elif elm_type == 'NAME':
                # 等待元素可点击
                timeout.until(EC.element_to_be_clickable((By.NAME, elm)))
                return True
        except:
            return False

    # 消除右上提示弹窗
    def dismiss_rightTopTips(self, close_button_elem_Xpath=mainPage_rightTopTips_closeButton_posXpath):
        """
        :param close_button_elem_Xpath:
        :return:
        """
        # print("消除弹窗")
        # time.sleep(3)
        self.driver.is_exist_element(close_button_elem_Xpath)
        loop_count = 2
        while loop_count > 0:
            try:
                self.driver.is_exist_element(close_button_elem_Xpath)
                if self.driver.Exist:
                    self.driver.find_element(By.XPATH, close_button_elem_Xpath).click()
                loop_count -= 1
            except:
                loop_count -= 1
                pass

        # try:
        #     self.driver.is_exist_element(Element="//div/div[1]/div[2]/div/div[2]/div[3]/i")
        #     if self.driver.Exist:
        #         self.driver.find_element(By.XPATH,'//div/div[1]/div[2]/div/div[2]/div[3]/i').click()
        # except:
        #     pass
        # try:
        #     self.driver.is_exist_element(Element="//div/div[1]/div[2]/div/div/div[3]/i")
        #     if self.driver.Exist:
        #         self.driver.find_element(By.XPATH,'//div/div[1]/div[2]/div/div/div[3]/i').click()
        # except:
        #     pass

        # self.driver.implicitly_wait(5)
        # self.driver.is_exist_element(close_button_elem_Xpath)
        # flag = self.driver.Exist
        # loop_count = 2
        # while flag and loop_count > 0:
        #     try:
        #         self.driver.is_exist_element(close_button_elem_Xpath)
        #         flag = self.driver.Exist
        #         # close_button_elem = self.driver.find_element(By.XPATH, close_button_elem_Xpath)
        #         if flag:
        #             # 1
        #             # for i in self.driver.find_elements(By.XPATH,close_button_elem_Xpath):
        #             #     i.click()
        #             # 2
        #             close_button_elem = self.driver.find_element_by_xpath(close_button_elem_Xpath)
        #             close_button_elem.click()
        #     except:
        #         self.driver.refresh()
        #         loop_count -= 1
        #         # break

    # 删除选中对象
    def delete(self, listPage_object_subObjects_delButton_posId, listPage_dialogTips_subObjects_button_yes_posCss,
               listPage_dialogTips_subObjects_button_no_posCss, ):
        """
        直接删除函数，
        :param listPage_object_subObjects_delButton_posId: 删除按钮id
        :param listPage_dialogTips_subObjects_button_yes_posCss: 提示删除框中yes定位CSS
        :param listPage_dialogTips_subObjects_button_no_posCss: 提示删除框中no定位CSS
        :return:
        """
        self.driver.find_element(By.ID, listPage_object_subObjects_delButton_posId).click()  # 点击删除按钮
        random_yes_or_no = random.randint(0, 1)
        if random_yes_or_no == 0:  # 点击yes，删除
            self.driver.find_element(By.CSS_SELECTOR,
                                     listPage_dialogTips_subObjects_button_yes_posCss).click()  # 直接删除
        else:
            self.driver.find_element(By.CSS_SELECTOR,
                                     listPage_dialogTips_subObjects_button_no_posCss).click()  # 先取消，再删除
            self.driver.find_element(By.ID, listPage_object_subObjects_delButton_posId).click()  # 点击删除按钮
            self.driver.find_element(By.CSS_SELECTOR,
                                     listPage_dialogTips_subObjects_button_yes_posCss).click()  # 点击yes，删除
        time.sleep(0.5)

    #

    # 判断某目录下是否为空
    def delete_folder_contents(self, folder):
        # time.sleep(3)
        # 判断文件夹是否为空
        if os.listdir(folder):
            print('不为空')
            # 遍历文件夹下的所有文件和子文件夹
            for item in os.listdir(folder):
                # 拼接完整的路径
                path = os.path.join(folder, item)
                # 判断是文件还是文件夹
                if os.path.isfile(path):
                    # 删除文件
                    os.remove(path)
                elif os.path.isdir(path):
                    # 删除文件夹及其内容
                    shutil.rmtree(path)
        else:
            # 文件夹为空，不做任何操作
            print('该目录为空')
            pass

    def extract_ele_userdefinedAttributesAndSignatures(self):
        self.driver.find_element(By.XPATH, mainPage_ObjectSearch_Column_settings_posXpath).click()  # 点击列设置
        all_checked_xpath = '//*[@class="all-btn"]//*[@class="el-checkbox__input is-checked"]'
        if self.driver.is_exist_element_by_value(By.XPATH, all_checked_xpath):  # 如果全选被选中
            self.driver.find_element(By.XPATH,
                                     mainPage_ObjectSearch_Column_settings_click_Cancel_Button_posXpath).click()  # 点击Cancel按钮
        else:
            self.driver.find_element(By.XPATH,
                                     mainPage_ObjectSearch_Column_settings_select_allCheckBox_posXpath).click()  # 全选
            self.driver.find_element(By.XPATH,
                                     mainPage_ObjectSearch_Column_settings_click_OK_Button_posXpath).click()  # 点击OK按钮
        # 公共方法 Detail特殊，需要使用时特殊提取
        # ID
        self.key11 = self.driver.find_element(By.XPATH, Userdefined_first_row_first_column_posXpath).text
        self.value12 = self.driver.find_element(By.XPATH, Userdefined_second_row_first_column_posXpath).text
        # Vsy_ID
        self.key12 = self.driver.find_element(By.XPATH, Userdefined_first_row_second_column_posXpath).text
        self.value22 = self.driver.find_element(By.XPATH, Userdefined_second_row_second_column_posXpath).text
        # Name
        self.key13 = self.driver.find_element(By.XPATH, Userdefined_first_row_third_column_posXpath).text
        self.value23 = self.driver.find_element(By.XPATH, Userdefined_second_row_third_column_posXpath).text
        # 字典
        self.table_dict1 = {self.key11: self.value12, self.key12: self.value22, self.key13: self.value23}
        print(self.table_dict1)

    # 提取Attributes的ID、Name
    def assert_ele_userdefined_attributes_and_signatures(self):
        # 公共方法 Detail特殊，需要使用时特殊提取
        # ID
        self.key11 = self.driver.find_element(By.XPATH, Userdefined_first_row_first_column_posXpath).text
        self.value12 = self.driver.find_element(By.XPATH, Userdefined_second_row_first_column_posXpath).text
        # Vsy_ID
        self.key12 = self.driver.find_element(By.XPATH, Userdefined_first_row_second_column_posXpath).text
        self.value22 = self.driver.find_element(By.XPATH, Userdefined_second_row_second_column_posXpath).text
        # Name
        self.key13 = self.driver.find_element(By.XPATH, Userdefined_first_row_third_column_posXpath).text
        self.value23 = self.driver.find_element(By.XPATH, Userdefined_second_row_third_column_posXpath).text
        # 字典
        self.edit_table_dict1 = {self.key11: self.value12, self.key12: self.value22, self.key13: self.value23}
        print(self.edit_table_dict1)

    def Export_different_types(self):
        try:
            time.sleep(3)
            self.driver.find_element(By.XPATH,
                                     mobileIdentitiesObjectPage_Export_Mobile_Identity_files_OK_Button_posXpath).click()
            self.driver.is_exist_element(Element=mobileIdentitiesObjectPage_Export_Mobile_type_imsi_posXpath)  # imsi导出展示
            assert self.driver.Exist
            self.driver.is_exist_element(
                Element=mobileIdentitiesObjectPage_Export_Mobile_type_phone_number_posXpath)  # imsi导出展示
            assert self.driver.Exist
            self.driver.is_exist_element(Element=mobileIdentitiesObjectPage_Export_Mobile_type_imei_posXpath)  # imsi导出展示
            assert self.driver.Exist
            self.driver.find_element(By.XPATH, '//div/div[3]/span/button[2]').click()
            print("点击导出按钮，断言可以导出多个不同type类型 == Sucess")
        except:
            print("点击导出按钮，断言可以导出多个不同type类型 == Fail")

    '''
    data:{
        "vsys_opearte": {"step1": "super_Tvsys1->create", "step2": "super_Mvsys3->search"}, # 操作模式：可以引用本vsys方法操作
        "delete_mode":"intercept"   # 清理数据 清理模式 
        }
    '''

    def Switch_vsys(self, vsys_id):
        time.sleep(2)
        self.driver.find_element(By.XPATH, objects_element_position.mainPage_navigationBar_Menu_posXpath).click()
        try:
            self.driver.is_exist_element(Element=mobile_Identities_Group_confirm_leave_posXpath)
            time.sleep(2)
            if self.driver.Exist:
                time.sleep(3)
                self.driver.find_element(By.XPATH, mobile_Identities_Group_confirm_leave_posXpath).click()
        except:
            pass
        time.sleep(2)
        if vsys_id == "Tvsys10":
            self.driver.find_element(By.XPATH, mainPage_navigationBar_Tvsys10_posXpath).click()
        elif vsys_id == "Mvsys2":
            self.driver.find_element(By.XPATH, test_mainPage_navigationBar_Mvsys2_Tvsys4_posXpath).click()
        elif vsys_id == "Tvsys3":
            self.driver.find_element(By.XPATH, test_mainPage_navigationBar_Tvsys3_posXpath).click()
        elif vsys_id == "super_Mvsys3":
            # print("切换为super_Mvsys3")
            self.driver.find_element(By.XPATH,
                                     objects_element_position.mainPage_navigationBar_Mvsys3_Tvsys5_posXpath).click()
            # print("切换为super_Mvsys3",objects_element_position.mainPage_navigationBar_Mvsys3_Tvsys5_posXpath)
        elif vsys_id == "super_Tvsys10":
            self.driver.find_element(By.XPATH, mainPage_navigationBar_super_Tvsys10_posXpath).click()
        # elif vsys_id == "super_Tvsys3":
        #     self.driver.find_element(By.XPATH, mainPage_navigationBar_super_Tvsys3_posXpath).click()

    def Watch_list(self):
        self.extract_ele()
        # 清空watch列表页
        self.driver.find_element(By.XPATH, listPage_objectSearch_mobileIdentities_right_list_watch_posXpath).click()
        self.driver.find_element(By.XPATH,
                                 listPage_objectSearch_mobileIdentities_right_list_watch_object_posXpath).click()
        self.driver.find_element(By.XPATH,
                                 listPage_objectSearch_mobileIdentities_right_list_watch_select_all_posXpath).click()
        self.driver.find_element(By.XPATH,
                                 listPage_objectSearch_mobileIdentities_right_list_watch_select_clear_posXpath).click()
        # 添加watch列表页
        self.driver.find_element(By.XPATH, listPage_object_mobileIdentities_select_First_object_posXpath).click()
        self.driver.find_element(By.XPATH, listPage_objectSearch_mobileIdentities_add_watch_posXpath).click()
        # 查看watch_list
        time.sleep(3)
        self.watch_ID = self.driver.find_element(By.XPATH, '//ul/li[1]/div/label/span[2]/p[1]').text
        self.watch_Name = self.driver.find_element(By.XPATH, '//ul/li[1]/div/label/span[2]/p[2]').text
        assert self.table_dict["ID"] == self.watch_ID, "断言添加到watch列表中的ID是否正确"
        assert self.table_dict["Name"] == self.watch_Name, "断言添加到watch列表中的Name是否正确"

    def assert_del(self):
        time.sleep(3)
        self.driver.is_exist_element(Element=listPage_object_mobileIdentities_select_First_object_posXpath)
        if self.driver.Exist == False:
            self.Page_Tips = self.driver.find_element(By.XPATH,
                                                      listPage_object_mobileIdentities_del_after_ele_posXpath).text
            try:
                assert self.Page_Tips == "No Data", "校验是否删除成功生效"
                print("未查询到该Object，该Object不存在，断言成功")
            except:
                print("仍然可以查询到Object，断言失败")
        else:
            pass

    def compare_vsys(self, vsys1, vsys2):
        # _query=1,则可查询、断言ID、Name、查看操作权限
        # _query=0,不可查询，del断言,引用断言
        if vsys1[0] == vsys2[0] == "T" and vsys1 != vsys2:  # T1  T2
            self._query = 0  # 不可查询
        elif vsys1[0] == vsys2[0] == "T" and vsys1 == vsys2:  # T1 == T1
            self._query = 1  # 相同vsys，可查询
        elif vsys1[0] == vsys2[0] == "M" and vsys1 == vsys2:  # M1 = M1
            self._query = 1  # 相同Mvsys,可查询
        elif vsys1[0] == "M" and vsys2[0] == "T":  # M1 T1
            self._query = 0  # Tvsys只能查看当前Vsys
        elif vsys1[0] == "T" and vsys2[0] == "M":  # T1 M1
            self._query = 0  # Mvsys没有supervisor权限,无法查看下层vsys
        elif vsys1[0] == vsys2[0] == "s" and vsys1[6] == vsys2[6] == "T" and vsys1 != vsys2:  # ST1  ST2
            self._query = 0  # 不可查询
        elif vsys1[0] == vsys2[0] == "s" and vsys1[6] == vsys2[6] == "T" and vsys1 == vsys2:  # ST1  ST1
            self._query = 1  # 可查询
        elif vsys1[0] == vsys2[0] == "s" and vsys1[6] == "M" and vsys2[6] == "T":  # SM1  ST2
            self._query = 0  # 不可查询
        elif vsys1[0] == vsys2[0] == "s" and vsys1[6] == "T" and vsys2[6] == "M":  # ST1  SM2
            self._query = 1  # 可查询、断言ID、Name、查看操作权限
        else:
            pass

    # 没有编辑权限
    def Unauthorized_operation(self):
        self.driver.find_element(By.XPATH, listPage_object_mobileIdentities_allButton_posId).click()
        # 1、导出按钮置灰
        try:
            self.driver.is_exist_element(
                Element=mobileIdentitiesObjectPage_Export_Mobile_Identity_Button_posXpath)  # 导出按钮置灰
            assert self.driver.Exist, "导出按钮置灰"
            print("导出按钮置灰，测试 == Success")
        except:
            print("导出按钮置灰，测试 == Fail")
        # 2、编辑按钮置灰
        try:
            self.driver.is_exist_element(
                Element=mobileIdentitiesObjectPage_Edit_Mobile_Identity_Button_posXpath)  # 编辑按钮置灰
            assert self.driver.Exist, "编辑按钮置灰"
            print("编辑按钮置灰，测试 == Success")
        except:
            print("编辑按钮置灰，测试 == Fail")
        # 3、删除按钮置灰
        try:
            self.driver.is_exist_element(
                Element=mobileIdentitiesObjectPage_Delete_Mobile_Identity_Button_posXpath)  # 删除按钮置灰
            assert self.driver.Exist, "删除按钮置灰"
            print("删除按钮置灰，测试 == Success")
        except:
            print("删除按钮置灰，测试 == Fail")

    # 刷新、翻页后元素不为选中状态
    def Clear_selection(self):
        try:
            self.driver.find_element(By.XPATH, listPage_object_mobileIdentities_allButton_posId).click()  # 选择all
            time.sleep(5)
            self.driver.find_element(By.ID, mainPage_secondLevelMenu_Mobile_Identities_posId).click()  # 刷新
            self.driver.is_exist_element(Element=mobileIdentitiesObjectPage_selete_Mobile_Identity_Button_posXpath)
            time.sleep(5)
            assert self.driver.Exist, "刷新导致元素不勾选"
            print("刷新后元素不勾选，测试 == Success")
            time.sleep(5)
            self.driver.find_element(By.XPATH, listPage_object_mobileIdentities_allButton_posId).click()  # 选择all
            self.driver.find_element(By.XPATH, listPage_object_pages_nextPage_button_poxXpath).click()  # 第二页
            self.driver.is_exist_element(Element=mobileIdentitiesObjectPage_selete_Mobile_Identity_Button_posXpath)
            time.sleep(5)
            assert self.driver.Exist, "翻页导致元素不勾选"
            print("翻页后元素不勾选，测试 == Success")
        except:
            print("翻页后元素不勾选，测试 == Fail")

    def Unable_to_upload(self):
        try:
            # 选择创建1
            self.driver.find_element(By.ID, listPage_object_mobileIdentities_createButton_posId).click()
            self.driver.find_element(By.ID,
                                     listPage_object_mobileIdentities_create_Mobile_Identity_Button_posId).click()
            self.driver.find_element(By.ID, mainPage_ObjectSearch_buttonAddItem_posId).click()
            time.sleep(3)
            self.driver.is_exist_element(Element=mobileIdentitiesObjectPage_import_files_Mobile_Identity_Button_posXpath)
            assert self.driver.Exist
            print("导入按钮置灰，测试 == Success")
        except:
            print("导入按钮未置灰，测试 == Fail")

    def download_delete_import_files(self, data):
        try:
            # 选择创建1
            self.driver.find_element(By.ID, listPage_object_mobileIdentities_createButton_posId).click()
            self.driver.find_element(By.ID,
                                     listPage_object_mobileIdentities_create_Mobile_Identity_Button_posId).click()
            # 上传文件
            self.driver.find_element(By.XPATH,
                                     mobileIdentitiesObjectPage_Button_Import_Mobile_Identity_files_posXpath).click()
            self.driver.find_element(By.XPATH,
                                     mobileIdentitiesObjectPage_Input_path_Import_Mobile_Identity_files_posXpath).send_keys(
                self.my_files._obj_files_path(file_name=data["files_name"]))
            self.driver.find_element(By.XPATH,
                                     mobileIdentitiesObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath).click()
            self.driver.is_exist_element(Element='//li/i[@class="iconfont icon-DownNormal fontsize16"]')
            assert self.driver.Exist
            print("存在下载按钮，测试 == Success")
            self.driver.is_exist_element(Element='//li/i[@class="el-icon-close fontsize18"]')
            assert self.driver.Exist
            print("存在删除按钮，测试 == Success")
        except:
            print("测试失败，不存在下载、删除按钮")

    def switch_checked(self):
        # 选择创建2 Group
        self.driver.find_element(By.ID, listPage_object_mobileIdentities_createButton_posId).click()
        self.driver.find_element(By.ID,
                                 listPage_object_mobileIdentities_create_Mobile_Identity_Group_Button_posId).click()
        # 查看可以开启Exclude/Include开关
        self.driver.is_exist_element(
            Element=mobileIdentitiesObjectPage_Exclude_Objects_close_Mobile_Identity_Button_posXpath)
        if self.driver.Exist:
            print("Exclude_Objects按钮开关为关，测试 == Success")
        else:
            print("Exclude_Objects按钮开关为开，测试 == Fail")
        # 查看可以开启Exclude/Include开关
        self.driver.find_element(By.XPATH,
                                 mobileIdentitiesObjectPage_Exclude_Objects_operation_Mobile_Identity_Button_posXpath).click()
        self.driver.is_exist_element(
            Element=mobileIdentitiesObjectPage_Exclude_Objects_open_Mobile_Identity_Button_posXpath)
        if self.driver.Exist:
            print("Exclude_Objects按钮开关为关，测试 == Success")
        else:
            print("Exclude_Objects按钮开关为开，测试 == Fail")

    def random_object_statistics(self):
        random_object_statistic = random.choice(["Elaborate", "Brief", "None"])
        print(random_object_statistic)
        return random_object_statistic

# path = my_files._obj_files_dowload_path()  # 替换为你的路径
# txt_filenames = get_txt_filenames(path)
# print(txt_filenames)

if __name__ == '__main__':
    print("test")
