import configparser
import inspect
import os
import time
import pytest_check
import random
import ipaddress
from selenium import webdriver
from support.ui_utils.my_web_driver import MyWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from support.ui_utils.random_name import RandomName
from support.ui_utils.read_data import ReadData
from support.ui_utils.workpath import workdir
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.element_position.profile_element_position import *


class ProfilePublicFunc:
    def __init__(self, driver):
        self.driver = driver
        self.my_random = RandomName()

    def search(self, mainPage_profileSearch_selectLabel_posId, listPage_profileSearch_subProfiles_dropDown_item_posXpath,
              listPage_profileSearch_subProfiles_input_itemContent_posXpath, mainPage_profileSearch_buttonSearch_posId,
              listPage_profilTable_subProfiles_tableTbody_posXpath, listPage_profilTable_subProfiles_tableHeader_posXpath,
              listPage_profileSearch_subProfiles_dropDown_typeItem_posXpath="", **kwargs):
        """
        profiles模块中从点击查询到查询到结果使用方法，并返回第一行数据和表头、class的字典
        :param mainPage_profileSearch_selectLabel_posId: 查询框id
        :param listPage_profileSearch_subProfiles_dropDown_item_posXpath: 下拉列表item的xpath
        :param listPage_profileSearch_subProfiles_input_itemContent_posXpath: 选中item后，输入input的xpath
        :param mainPage_profileSearch_buttonSearch_posId: 查询按钮id
        :param listPage_profilTable_subProfiles_tableTbody_posXpath: 列表页body的部分xpath
        :param listPage_profilTable_subProfiles_tableHeader_posXpath: 列表页header的部分xpath
        :param listPage_profileSearch_subProfiles_dropDown_typeItem_posXpath: 如果有下拉列表item的枚举选项定位，需要增补
        :param kwargs: 需要查询的内容，来自调用函数
        :return: [first_row, map_header_className]
        """
        # 点击search查询框
        self.driver.find_element(By.ID, mainPage_profileSearch_selectLabel_posId).click()
        # 循环输入查询内容
        for key, value in kwargs.items():
            if "_" in key:
                key = key.replace("_", " ")   # 将下划线替换为空格
            dropdown_item_posXpath = listPage_profileSearch_subProfiles_dropDown_item_posXpath.format(replaceName=key)
            self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()    # 点击下拉item
            if key != "type":
                input_item_posXpath = listPage_profileSearch_subProfiles_input_itemContent_posXpath.format(replaceName=key)
                self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(value.strip())       # 输入查询值
                self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(Keys.ENTER)         # 模拟回车按键
            else:
                dropdown_typeItem_posXpath = listPage_profileSearch_subProfiles_dropDown_typeItem_posXpath.format(replaceName=value.split("->")[0])
                self.driver.find_element(By.XPATH, dropdown_typeItem_posXpath).click()    # 点击type的下拉item
        # 点击查询按钮
        element_search = self.driver.find_element(By.ID, mainPage_profileSearch_buttonSearch_posId)
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        element_tbody = self.driver.find_element(By.XPATH, listPage_profilTable_subProfiles_tableTbody_posXpath)  # 找到所有的行，table的body
        element_header = self.driver.find_element(By.XPATH, listPage_profilTable_subProfiles_tableHeader_posXpath)   # 查询table的header
        # 获取table header的text、th.class
        headers = element_header.find_elements(By.XPATH, "th")     # table header
        rows = element_tbody.find_elements(By.XPATH, "tr")     # table body
        if len(rows) == 0:
            print(f"没有查询到数据：查询条件：{kwargs}")
            return [0, 0]
        map_header_className = {}  # 表头名称和th.class的映射，为了从表body中取对应列的值{"ID":"33"}
        for th in headers:
            self.driver.execute_script("arguments[0].scrollIntoView();", th)
            header_content = th.text.strip()
            classNames = th.get_attribute("class").split()
            for c_name in classNames:
                if "el-table" in c_name:
                    tableBodyRowClassName = c_name
            if header_content and tableBodyRowClassName:
                map_header_className[header_content] = tableBodyRowClassName
        # 从第一行查询的结果中，取出需要断言的值、name
        first_row = rows[0]
        return [first_row, map_header_className]

    def delete_profile(self, listPage_profile_subProfiles_delButton_posId, listPage_dialogTips_subProfiles_button_yes_posCss,
               listPage_dialogTips_subProfiles_button_no_posCss):
        """
        直接删除函数，
        :param listPage_profile_subProfiles_delButton_posId: 删除按钮id
        :param listPage_dialogTips_subProfiles_button_yes_posCss: 提示删除框中yes定位css
        :param listPage_dialogTips_subProfiles_button_no_posCss: 提示删除框中no定位css
        :return:
        """
        self.driver.find_element(By.ID, listPage_profile_subProfiles_delButton_posId).click()   # 点击删除按钮
        random_yes_or_no = random.randint(0, 1)
        if random_yes_or_no == 0:    # 点击yes，删除
            self.driver.find_element(By.CSS_SELECTOR, listPage_dialogTips_subProfiles_button_yes_posCss).click()   # 直接删除
        else:
            self.driver.find_element(By.CSS_SELECTOR, listPage_dialogTips_subProfiles_button_no_posCss).click()   # 先取消，再删除
            self.driver.find_element(By.ID, listPage_profile_subProfiles_delButton_posId).click()  # 点击删除按钮
            self.driver.find_element(By.CSS_SELECTOR, listPage_dialogTips_subProfiles_button_yes_posCss).click()
        time.sleep(0.5)

    def is_valid_ip(self, ip):
        "判断ip字符串是否为ip格式数据，是返回True"
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def get_name_from_data(self, data):
        """
        从用例dict中获取name，含有随机判断效果
        :param data:
        :return:
        """
        if "name" in data.keys():
            name = data["name"]
            # random_name = self.my_random.random_name(source_name=name, is_none=True)
        else:
            name = self.my_random.random_name()
        return name

    def change_vsys(self, vsys_name=""):
        """
        调整vsys，vsys_name可以为空字符串，不用切换vsys。vsys_name=空时，默认切换到UIAutoTestVsys
        :param vsys_name:  vsys name, 例如：Default Vsys 、或者空。vsys_name与当前vsys一直或者为空字符串时，不要操作vsys
        :return:
        """
        current_vsys_name = self.driver.find_element(By.XPATH, mainPage_currentPage_vsysName_posXpath).text.strip().lower()
        if vsys_name.lower() == current_vsys_name:
            print(f"the current vsys: {current_vsys_name}")
            return 0
        else:    # 空为切换默认   剩下为指定切换
            if vsys_name == "":     # 空，切换到默认vsys
                change_vsys_name = "UIAutoTestVsys"
                if change_vsys_name.lower() == current_vsys_name:    # 如果默认系统和当前一直，也不用点击
                    print(f"the current vsys: {current_vsys_name}")
                    return 0
            else:     # 切换到指定vsys
                change_vsys_name = vsys_name
            print(f"the current vsys: {current_vsys_name}, switch to vsys: {change_vsys_name}")
            self.driver.find_element(By.CSS_SELECTOR, mainPage_button_menu_posXCss).click()     # 点击vsys menu
            vsys_tree_name_list = self.driver.find_elements(By.XPATH, mainPage_vsysTree_vsysName_posXpath)
            flag_num = 0
            for el_vsys_item in vsys_tree_name_list:
                vsys_item_name = el_vsys_item.text.strip().lower()
                if vsys_item_name == change_vsys_name.lower():
                    flag_num = 1
                    el_vsys_item.click()
                    break
            if flag_num == 0:
                print(f"no vsys: {change_vsys_name}")
                raise ValueError(f"no vsys: {change_vsys_name}")

    def column_setting(self, mainPage_profileColumn_columnSetting_posId,listPage_profileColumn_button_columnAll_posId,
                        listPage_profileColumn_button_columnCancel_posId,listPage_profileColumn_button_cancel_posId,
                        listPage_profileColumn_button_ok_posId, Profiles, column_flags, column):
        """
        列设置函数,
        column_flags: 0---保持当前状态   1---仅显示默认列   2---显示所有列   3---显示自定义列
        :param mainPage_profileColumn_columnSetting_posId:
        :param listPage_profileColumn_button_columnAll_posId:
        :param listPage_profileColumn_button_columnCancel_posId:
        :param listPage_profileColumn_button_cancel_posId:
        :param listPage_profileColumn_button_ok_posId:
        :param Profiles:   profile模块名称定位
        :param column:     自定义需要调整列内容
        :return:
        """

        self.driver.find_element(By.ID, mainPage_profileColumn_columnSetting_posId).click()  # 点击列设置按钮
        if column_flags == 0:  #保持当前状态
            self.driver.find_element(By.ID, listPage_profileColumn_button_cancel_posId).click()  # 点击cancel按钮
        elif column_flags == 1:    #仅显示默认列
            self.driver.find_element(By.ID, listPage_profileColumn_button_columnCancel_posId).click()  # 点击列选择Cancel按钮
            self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
        elif column_flags == 2:   #显示所有列
            self.driver.find_element(By.ID, listPage_profileColumn_button_columnAll_posId).click()  # 点击列选择All按钮
            self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
        else:
            for name in column:
                # print("name=", name)
                self.driver.find_element(By.XPATH, f"//*[@id='dropColRes-_ElementSet_{Profiles}_Home_App_anonymousComponent']/span[text()='{name}']").click()  # 选择指定列按钮
            self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
        element_header = self.driver.find_element(By.XPATH, "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead//tr")  # 查询table的header
        headers = element_header.find_elements(By.XPATH, "//th[@colspan='1']")  # table header
        headers_content = []
        for th in headers:
            self.driver.execute_script("arguments[0].scrollIntoView();", th)
            header_content = th.text.strip()
            # print("header_content=", header_content)
            if header_content != "":
                headers_content.append(header_content)
        return headers_content

    def turn_pages(self, profiles, pages):
        """
        翻页函数
        pages：当前模块页数；如果页数>8，则有快速翻页功能（页面翻至第5页，显示左快速翻页按钮；当前页为左/右第4页时，不显示快速翻页按钮）
        :param profiles:
        :param pages:
        :return:
        """
        # 右翻页
        max_page_num = self.driver.find_element(By.XPATH,f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']").find_element(By.XPATH, ".//li[last()]").text.strip()
        max_page_num = int(max_page_num)
        if pages > max_page_num:    # 如果传入的页数大于最大的也是，则取最大页数值
            pages = max_page_num
        for number in range(1, pages):
            self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn-next')]").click()
            time.sleep(0.5)
            # 当前页XPATH
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = self.driver.find_element(By.XPATH, current_page).text.strip()
            # print("current_page_content=", current_page_content)
            flag = str(number + 1)
            pytest_check.equal(current_page_content, flag, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            time.sleep(0.5)
        # 左快速翻页
        if pages >= 8:
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            if current_page_content > 5:
                self.driver.find_element(By.XPATH, "//li[contains(@class, 'btn-quickprev')]").click()
                flag = current_page_content - 5
                if flag < 0:
                    flag = 1
                time.sleep(0.5)
                current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
                pytest_check.equal(current_page_content, flag, msg="所在行数{}".format(inspect.currentframe().f_lineno))
        # Go to
        for _ in range(3):
            random_page = random.sample(range(1, pages+1), 1)[0]
            print("random_page=", random_page)
            self.driver.find_element(By.XPATH, "//span[text()='Go to']//input").send_keys(Keys.CONTROL + "a")
            self.driver.find_element(By.XPATH, "//span[text()='Go to']//input").send_keys(Keys.BACKSPACE)
            self.driver.find_element(By.XPATH, "//span[text()='Go to']//input").send_keys(random_page)
            time.sleep(0.5)
            self.driver.find_element(By.XPATH, "//span[text()='Go to']//input").send_keys(Keys.RETURN)
            time.sleep(0.5)
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            pytest_check.equal(current_page_content, random_page, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            time.sleep(0.5)
        # 随机点击某页
        for _ in range(3):
            enview_pages_element = self.driver.find_elements(By.XPATH, "//ul[@class='el-pager']//li")
            enview_pages = []
            if pages < 8:
                random_page = random.sample(range(1, pages+1), 1)[0]
                print("random_page=", random_page)
                self.driver.find_element(By.XPATH, f"//li[text()='{random_page}']").click()
            if pages >= 8:
                for i in range(len(enview_pages_element)):
                    print("1=", enview_pages_element[i].text)
                    if enview_pages_element[i].text != "":
                        enview_pages.append(enview_pages_element[i].text)
                # print(enview_pages)
                random_page = random.sample(range(1, len(enview_pages) + 1), 1)[0]
                random_page = int(enview_pages[random_page-1])
                self.driver.find_element(By.XPATH, f"//li[text()='{random_page}']").click()
            time.sleep(0.5)
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            pytest_check.equal(current_page_content, random_page, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            time.sleep(0.5)
        if pages >= 8:
            self.driver.find_element(By.XPATH, f"//li[text()='1']").click()
        else:
            self.driver.find_element(By.XPATH, f"//li[text()='{pages}']").click()
        # 右快速翻页
        if pages >= 8:
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            if current_page_content < (pages - 4):
                self.driver.find_element(By.XPATH, "//li[contains(@class, 'btn-quicknext')]").click()
                flag = current_page_content + 5
                if flag > pages:
                    flag = pages
                time.sleep(0.5)
                current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
                pytest_check.equal(current_page_content, flag, msg="所在行数{}".format(inspect.currentframe().f_lineno))
        # 左翻页
        self.driver.find_element(By.XPATH, f"//li[text()='{pages}']").click()
        while pages - 1:
            self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn-prev')]").click()
            time.sleep(0.5)
            # 当前页XPATH
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            pages = pages - 1
            pytest_check.equal(current_page_content, pages, msg="所在行数{}".format(inspect.currentframe().f_lineno))
            time.sleep(0.5)
    
    def language_change(self, mainPage_language_change_posXpath, mainPage_language_chinese_posXpath,
                        mainPage_language_russian_posXpath, mainPage_language_english_posXpath, language=0):
        """
        语言切换函数
        language: 0---english; 1---chinese; 2---russian
        :param mainPage_language_change_posXpath:
        :param mainPage_language_chinese_posXpath:
        :param mainPage_language_russian_posXpath:
        :param mainPage_language_english_posXpath:
        :param language:
        :return:
        """
        self.driver.find_element(By.XPATH, mainPage_language_change_posXpath).click()
        if language == 0:
            btn = self.driver.find_element(By.XPATH, mainPage_language_english_posXpath)
            self.driver.execute_script("arguments[0].click()", btn)   # 强制点击
        elif language == 1:
            btn = self.driver.find_element(By.XPATH, mainPage_language_chinese_posXpath)
            self.driver.execute_script("arguments[0].click()", btn)
        elif language == 2:
            btn = self.driver.find_element(By.XPATH, mainPage_language_russian_posXpath)
            self.driver.execute_script("arguments[0].click()", btn)
        time.sleep(1)
        element_header = self.driver.find_element(By.XPATH, "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead//tr")  # 查询table的header
        headers = element_header.find_elements(By.XPATH, "//th[@colspan='1']")  # table header
        headers_content = []
        for th in headers:
            self.driver.execute_script("arguments[0].scrollIntoView();", th)
            header_content = th.text.strip()
            if header_content != "":
                headers_content.append(header_content)
        return headers_content

    def data_limit(self,listPage_profile_profiles_editButton_posId,listPage_profile_profiles_delButton_posId):
        """校验数据是否只有查看权限"""
        # 校验当前数据是否为只能查看
        text_view = self.driver.find_element(By.ID, listPage_profile_profiles_editButton_posId).text.strip()
        print("text_view=", text_view)
        pytest_check.equal(self.driver.find_element(By.ID, listPage_profile_profiles_editButton_posId).text.strip(), "View", msg="所在行数{}".format(inspect.currentframe().f_lineno))
        # 校验删除按钮是否置灰
        text_del = self.driver.find_element(By.ID,
                                            listPage_profile_profiles_delButton_posId).get_attribute("class")
        print("text_del=", text_del)
        disabled_class = text_del.split(" ")[-1].strip()
        print("disabled_class=", disabled_class)
        pytest_check.equal(disabled_class, "is-disabled", msg="所在行数{}".format(inspect.currentframe().f_lineno))
        # 校验是否带锁
        self.driver.isElementExist("//i[@class='iconfont icon-lock']")
        assert self.driver.Exist

    def policy_create(self, action, profile_name, listPage_rule_create_button_posId, rule_input_Name_posXpath,
                      rule_action_posId, rule_source_add_posXpath, rule_button_oK_posId, rule_button_cancel_posId, rule_button_warningSaveYes_posCss,
                      application="http", rule_application_add_posXpath="", rule_application_search_posXpath="", *actionParameters):
        """若策略为Intercept时，actionParameters[0]表示为引用profile的类型： Traffic_Mirror_Profile、SSL_Decryption_Keyring、SSL_Decryption_Profile、TCP_Proxy_Profile"""
        # 点击创建按钮
        self.driver.find_element(By.ID, listPage_rule_create_button_posId).click()
        # 输入name
        policy_name = profile_name+"Rule"
        self.driver.find_element(By.XPATH, rule_input_Name_posXpath).send_keys(policy_name)
        # 选择Action
        self.driver.find_element(By.ID, rule_action_posId).click()
        # 选择source
        self.driver.find_element(By.XPATH, rule_source_add_posXpath).click()
        time.sleep(0.5)
        ## 选择IP的第一条记录
        self.driver.find_element(By.XPATH, "//div[@class='CommonListDetail list-detail']//ul[contains(@class, 'tableList')]/li[1]").click()
        # 关闭侧滑框
        self.driver.find_element(By.XPATH, "//div[contains(text(),'IP Address')]/i").click()
        # 选择Application
        application_isselected = ["Manipulation_Allow", "Manipulation_Deny", "Manipulation_Monitor", "Manipulation_Replace", "Manipulation_Hijack", "Manipulation_Insert", "Manipulation_EditElement", "Manipulation_RunScript"]
        if action in application_isselected:
            pass
        elif action =="Intercept":
            self.driver.find_element(By.XPATH, rule_application_add_posXpath).click()
            self.driver.find_element(By.XPATH, f"//div[@class='AppList list-box']//div[@class='CommonListDetail list-detail']//ul[contains(@class, 'tableList')]//span[text()='{application}']").click()
        else:
            self.driver.find_element(By.XPATH, rule_application_add_posXpath).click()
            self.driver.find_element(By.XPATH, rule_application_search_posXpath).send_keys(application)
            self.driver.find_element(By.XPATH, rule_application_search_posXpath).send_keys(Keys.ENTER)
            self.driver.find_element(By.XPATH, "//div[@class='AppList list-box']//div[@class='CommonListDetail list-detail']//ul[contains(@class, 'tableList')]/li[1]").click()
        # Action Parameters
        print("actionParameters=", actionParameters)
        if action == "Security_Deny":
            if application == "dns":
                # 勾选Override Application Deny Action
                self.driver.find_element(By.XPATH, actionParameters[0]).click()
                # 选择sub action
                self.driver.find_element(By.XPATH, actionParameters[1]).click()
                # 选择 Query Type
                self.driver.find_element(By.ID, actionParameters[2]).click()
                # 选择 Answer Type
                self.driver.find_element(By.XPATH, actionParameters[3]).click()
                self.driver.find_element(By.XPATH, actionParameters[4]).click()
                # 选择 Answer
                self.driver.find_element(By.XPATH, actionParameters[5]).click()
                self.driver.find_element(By.XPATH, actionParameters[6]).click()
                self.driver.find_element(By.XPATH, actionParameters[7]).click()
                self.driver.find_element(By.ID, actionParameters[8]).send_keys(profile_name)
                self.driver.find_element(By.ID, actionParameters[8]).send_keys(Keys.ENTER)
                if self.driver.find_element(By.XPATH, "//li[contains(@id, 'filelist_')]").get_attribute("id") == "filelist_null":
                    pytest_check.equal(self.driver.find_element(By.XPATH, "//li[contains(@id, 'filelist_')]").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                    result = "No Data"
                else:
                    self.driver.find_element(By.XPATH, "//li[@id='filelist_select0']").click()
                    result = self.driver.find_element(By.XPATH, "//li[@id='filelist_select0']").get_attribute("value")
                # 输入TTL
                self.driver.find_element(By.ID, actionParameters[9]).send_keys("300")
        elif action == "Manipulation_Deny":
            # 选择response code
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[0]).click()
            self.driver.find_element(By.XPATH, actionParameters[1]).click()
            time.sleep(1)
            # 选择 response content profile 类型
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[2]).click()
            self.driver.find_element(By.XPATH, actionParameters[3]).click()
            # 选择profile
            self.driver.find_element(By.XPATH, actionParameters[4]).click()
            self.driver.find_element(By.XPATH, actionParameters[5]).send_keys(profile_name)   #输入查询值
            self.driver.find_element(By.XPATH, actionParameters[5]).send_keys(Keys.ENTER)         #模拟回车按键
            time.sleep(1)
            if self.driver.find_element(By.XPATH, "//li[contains(@id, 'filelist_')]").get_attribute("id") == "filelist_null":
                pytest_check.equal(self.driver.find_element(By.XPATH, "//li[contains(@id, 'filelist_')]").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                result = "No Data"
            else:
                self.driver.find_element(By.XPATH, "//li[@id='filelist_select0']").click()
                result = self.driver.find_element(By.XPATH, "//li[@id='filelist_select0']").get_attribute("value")
        elif action == "Manipulation_Hijack":
            # 选择URL ---URL为必填项
            self.driver.find_element(By.XPATH, actionParameters[0]).click()
            self.driver.find_element(By.XPATH, actionParameters[1]).click()
            self.driver.find_element(By.XPATH, actionParameters[2]).click()
            self.driver.find_element(By.XPATH, "//ul[@class='row-container tableList']/li[1]").click()   #选择第一条URL
            # 选择hijack file
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[3]).click()
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)  # 输入查询值
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)  # 模拟回车按键
            if self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute("id") == "filelist_null":
                pytest_check.equal(self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                result = "No Data"
            else:
                self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").click()
                result = self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute("value")
        elif action == "Manipulation_Insert":
            # 选择URL ---URL为必填项
            self.driver.find_element(By.XPATH, actionParameters[0]).click()
            self.driver.find_element(By.XPATH, actionParameters[1]).click()
            self.driver.find_element(By.XPATH, actionParameters[2]).click()
            self.driver.find_element(By.XPATH, "//ul[@class='row-container tableList']/li[1]").click()   #选择第一条URL
            # 选择hijack file
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[3]).click()
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)  # 输入查询值
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)  # 模拟回车按键
            if self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute("id") == "filelist_null":
                pytest_check.equal(self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                result = "No Data"
            else:
                self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").click()
                result = self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute("value")
        elif action == "Manipulation_RunScript":
            pass
            # 选择URL ---URL为必填项
            self.driver.find_element(By.XPATH, actionParameters[0]).click()
            self.driver.find_element(By.XPATH, actionParameters[1]).click()
            self.driver.find_element(By.XPATH, actionParameters[2]).click()
            self.driver.find_element(By.XPATH, "//ul[@class='row-container tableList']/li[1]").click()   #选择第一条URL
            # 选择hijack file
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[3]).click()
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)  # 输入查询值
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)  # 模拟回车按键
            if self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute("id") == "filelist_null":
                pytest_check.equal(self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                result = "No Data"
            else:
                self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").click()
                result = self.driver.find_element(By.XPATH, "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute("value")
        elif action == "Intercept":
            if application == "ssl":
                if actionParameters[0] == "Traffic_Mirror_Profile":
                    # Mirror Decrypted Traffic
                    self.driver.find_element(By.XPATH, actionParameters[1]).click()
                    assert self.driver.find_element(By.XPATH, actionParameters[1]).get_attribute("class").split(" ")[-1]=="is-checked"
                    # Add VLAN ID
                    if self.driver.find_element(By.XPATH, actionParameters[2]).get_attribute("class").split(" ")[-1] != "is-checked":
                        self.driver.find_element(By.XPATH, actionParameters[2]).click()
                    # Traffic Mirror Profile
                    self.driver.find_element(By.XPATH, actionParameters[3]).click()
                    self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)
                    self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)
                    time.sleep(1)
                    profile_results = self.driver.find_elements(By.XPATH, "(//div[@class='select-search-option'])[6]/li")
                    print("len(profile_results):", len(profile_results))
                    if len(profile_results) == 1:
                        pytest_check.equal(
                            self.driver.find_element(By.XPATH, "(//div[@class='select-search-option'])[6]/li").text.strip(),
                            "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                        result = "No Data"
                    elif len(profile_results) > 1:
                        profile_results[1].click() # 获取第一条profile [0]为No Data
                        # result = self.driver.find_element(By.XPATH, "(//div[@class='select-search-option'])[6]/li[2]").get_attribute("value")
                        result = self.driver.find_element(By.XPATH,
                                                          "//label[text()='Traffic Mirror Profile']/parent::div//input").get_attribute("value")
                        print("result=", result)
                elif actionParameters[0] == "SSL_Decryption_Keyring":
                    self.driver.find_element(By.XPATH, actionParameters[1]).click()
                    self.driver.find_element(By.XPATH, actionParameters[2]).send_keys(profile_name)
                    self.driver.find_element(By.XPATH, actionParameters[2]).send_keys(Keys.ENTER)
                    time.sleep(1)
                    profile_results = self.driver.find_elements(By.XPATH,
                                                                "(//div[@class='select-search-option'])[6]/li")
                    print("len(profile_results):", len(profile_results))
                    if len(profile_results) == 1:
                        pytest_check.equal(
                            self.driver.find_element(By.XPATH,
                                                     "(//div[@class='select-search-option'])[6]/li").text.strip(),
                            "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                        result = "No Data"
                    elif len(profile_results) > 1:
                        profile_results[1].click()   # 获取第一条profile [0]为No Data
                        result = self.driver.find_element(By.XPATH, f"//label[text()='{actionParameters[3]}']/parent::div//input").get_attribute("value")
                        print("result=", result)
                elif actionParameters[0] == "SSL_Decryption_Profile":
                    self.driver.find_element(By.XPATH, actionParameters[1]).click()
                    self.driver.find_element(By.XPATH, actionParameters[2]).send_keys(profile_name)
                    self.driver.find_element(By.XPATH, actionParameters[2]).send_keys(Keys.ENTER)
                    time.sleep(1)
                    profile_results = self.driver.find_elements(By.XPATH, "(//div[@class='select-search-option'])[6]/li")
                    print("len(profile_results):", len(profile_results))
                    if len(profile_results) == 1:
                        pytest_check.equal(
                            self.driver.find_element(By.XPATH, "(//div[@class='select-search-option'])[6]/li").text.strip(),
                            "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                        result = "No Data"
                    elif len(profile_results) > 1:
                        profile_results[1].click()  # 获取第一条profile [0]为No Data
                        result = self.driver.find_element(By.XPATH,
                                                          "//label[text()='Decryption Profile']/parent::div//input").get_attribute("value")
                        print("result=", result)
                elif actionParameters[0] == "TCP_Proxy_Profile":
                    self.driver.find_element(By.XPATH, actionParameters[1]).click()
                    self.driver.find_element(By.XPATH, actionParameters[2]).send_keys(profile_name)
                    self.driver.find_element(By.XPATH, actionParameters[2]).send_keys(Keys.ENTER)
                    time.sleep(1)
                    profile_results = self.driver.find_elements(By.XPATH,
                                                                "(//div[@class='select-search-option'])[6]/li")
                    print("len(profile_results):", len(profile_results))
                    if len(profile_results) == 1:
                        pytest_check.equal(
                            self.driver.find_element(By.XPATH,
                                                     "(//div[@class='select-search-option'])[6]/li").text.strip(),
                            "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                        result = "No Data"
                    elif len(profile_results) > 1:
                        profile_results[1].click()  # 获取第一条profile [0]为No Data
                        result = self.driver.find_element(By.XPATH,
                                                          "//label[text()='TCP Proxy Profile']/parent::div//input").get_attribute(
                            "value")
                        print("result=", result)
        time.sleep(2)
        # 保存策略
        if result =="No Data":
           print("无可引用的文件,取消创建")
           self.driver.find_element(By.ID, rule_button_cancel_posId).click()
           if self.driver.find_element(By.CSS_SELECTOR, rule_button_warningSaveYes_posCss).is_displayed():
               self.driver.find_element(By.CSS_SELECTOR, rule_button_warningSaveYes_posCss).click()
           return 0
        else:
            self.driver.find_element(By.ID, rule_button_oK_posId).click()
            self.driver.find_element(By.CSS_SELECTOR, rule_button_warningSaveYes_posCss).click()
            return policy_name

    def policy_query(self, listPage_policiesSearch_selectLabel_posId, listPage_policiesSearch_dropDown_item_posXpath,
                     listPage_policiesSearch_input_itemContent_posXpath, listPage_policiesSearch_buttonSearch_posId,
                     listPage_policiesTable_tableTbody_posXpath, listPage_policiesTable_tableHeader_posXpath,**kwargs):
        """
        policies模块中从点击查询到查询到结果使用方法
        :param listPage_policiesSearch_selectLabel_posId: 查询框id
        :param listPage_policiesSearch_dropDown_item_posXpath: 下拉列表item的xpath
        :param listPage_policiesSearch_input_itemContent_posXpath: 选中item后，输入input的xpath
        :param listPage_policiesSearch_buttonSearch_posId: 查询按钮id
        :param kwargs: 需要查询的内容，来自调用函数
        """
        # 点击search查询框
        self.driver.find_element(By.ID, listPage_policiesSearch_selectLabel_posId).click()
        # 循环输入查询内容
        for key, value in kwargs.items():
            if "_" in key:
                key = key.replace("_", " ")   # 将下划线替换为空格
            dropdown_item_posXpath = listPage_policiesSearch_dropDown_item_posXpath.format(replaceName=key)
            self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()    # 点击下拉item
            input_item_posXpath = listPage_policiesSearch_input_itemContent_posXpath.format(replaceName=key)
            self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(value.strip())       # 输入查询值
            self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(Keys.ENTER)         # 模拟回车按键
        # 点击查询按钮
        element_search = self.driver.find_element(By.ID, listPage_policiesSearch_buttonSearch_posId)
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        element_tbody = self.driver.find_element(By.XPATH, listPage_policiesTable_tableTbody_posXpath)  # 找到所有的行，table的body
        element_header = self.driver.find_element(By.XPATH, listPage_policiesTable_tableHeader_posXpath)   # 查询table的header
        # 获取table header的text、th.class
        headers = element_header.find_elements(By.XPATH, "th")     # table header
        rows = element_tbody.find_elements(By.XPATH, "tr")     # table body
        if len(rows) == 0:
            print(f"没有查询到数据：查询条件：{kwargs}")
            return 0
        map_header_className = {}  # 表头名称和th.class的映射，为了从表body中取对应列的值{"ID":"33"}
        for th in headers:
            header_content = th.text.strip()
            classNames = th.get_attribute("class").split()
            for c_name in classNames:
                if "el-table" in c_name:
                    tableBodyRowClassName = c_name
            if header_content and tableBodyRowClassName:
                map_header_className[header_content] = tableBodyRowClassName
        # 从第一行查询的结果中，取出需要断言的值、name
        first_row = rows[0]
        return [first_row, map_header_className]

    def download_file( ):
        my_file = ReadData()
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': my_file._profiles_files_dowload_path(), 'safebrowsing.enabled': True}
        webdriver.ChromeOptions()
        loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir, "config", "login_logout.ini")
        loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        remote_url = loginout_parse.get("remote_url", "url")
        options.add_experimental_option('prefs', prefs)
        options.add_argument("--incognito")
        driver = MyWebDriver(
            command_executor=remote_url,
            options=options)
        driver.implicitly_wait(5)
        driver.get("http://192.168.44.72")
        driver.maximize_window()
        aut_username = loginout_parse.get("ui_account_1", "username")
        aut_pwd = loginout_parse.get("ui_account_1", "passwd")
        driver.find_element(By.NAME, loginPage_userName_posName).send_keys(aut_username)
        driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(aut_pwd)
        driver.find_element(By.ID, "login").click()
        return driver

    def cached_intermediate_certificates_driver( ):
        my_file = ReadData()
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': my_file._profiles_files_dowload_path(), 'safebrowsing.enabled': True}
        webdriver.ChromeOptions()
        loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir, "config", "login_logout.ini")
        loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        remote_url = loginout_parse.get("remote_url", "url")
        options.add_experimental_option('prefs', prefs)
        options.add_argument("--incognito")
        driver = MyWebDriver(
            command_executor=remote_url,
            options=options)
        driver.implicitly_wait(5)
        driver.get("http://192.168.44.72")
        driver.maximize_window()
        aut_username = loginout_parse.get("ui_account_1_cached", "username")
        aut_pwd = loginout_parse.get("ui_account_1_cached", "passwd")
        driver.find_element(By.NAME, loginPage_userName_posName).send_keys(aut_username)
        driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(aut_pwd)
        driver.find_element(By.ID, "login").click()
        return driver