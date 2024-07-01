import configparser
import inspect
import os
import time
import pytest_check
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from support.ui_utils.my_web_driver import MyWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
from support.general_ui_utils.random_name import RandomName
from support.general_ui_utils.read_data import ReadData
from support.general_ui_utils.workpath import workdir
from support.general_ui_utils.element_position.objects_element_position import *
from support.general_ui_utils.element_position.profiles_element_position import *
import ipaddress

class ProfilesPublicOperations:
    def __init__(self, driver):
        self.driver = driver
        self.my_random = RandomName()

    def query(self, mainPage_profileSearch_selectLabel_posId, listPage_profileSearch_subProfiles_dropDown_item_posXpath,
              listPage_profileSearch_subProfiles_input_itemContent_posXpath, mainPage_profileSearch_buttonSearch_posId,
              listPage_profilTable_subProfiles_tableTbody_posXpath,
              listPage_profilTable_subProfiles_tableHeader_posXpath,
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
                key = key.replace("_", " ")  # 将下划线替换为空格
            dropdown_item_posXpath = listPage_profileSearch_subProfiles_dropDown_item_posXpath.format(replaceName=key)
            self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()  # 点击下拉item
            if key != "type":
                input_item_posXpath = listPage_profileSearch_subProfiles_input_itemContent_posXpath.format(
                    replaceName=key)
                self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(value.strip())  # 输入查询值
                self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(Keys.ENTER)  # 模拟回车按键
            else:
                dropdown_typeItem_posXpath = listPage_profileSearch_subProfiles_dropDown_typeItem_posXpath.format(
                    replaceName=value.split("->")[0])
                self.driver.find_element(By.XPATH, dropdown_typeItem_posXpath).click()  # 点击type的下拉item
        # 点击查询按钮
        element_search = self.driver.find_element(By.ID, mainPage_profileSearch_buttonSearch_posId)
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        element_tbody = self.driver.find_element(By.XPATH,
                                                 listPage_profilTable_subProfiles_tableTbody_posXpath)  # 找到所有的行，table的body
        element_header = self.driver.find_element(By.XPATH,
                                                  listPage_profilTable_subProfiles_tableHeader_posXpath)  # 查询table的header
        # 获取table header的text、th.class
        headers = element_header.find_elements(By.XPATH, "th")  # table header
        rows = element_tbody.find_elements(By.XPATH, "tr")  # table body
        if len(rows) == 0:
            #print(f"没有查询到数据：查询条件：{kwargs}")
            return [0, 0]
        map_header_className = {}  # 表头名称和th.class的映射，为了从表body中取对应列的值{"ID":"33"}
        for th in headers:
            self.driver.execute_script("arguments[0].scrollIntoView();", th)
            header_content = th.text.strip()
            classNames = th.get_attribute("class").split()
            for c_name in classNames:
                if "el-table" in c_name and "column" in c_name:
                    tableBodyRowClassName = c_name
            if header_content and tableBodyRowClassName:
                map_header_className[header_content] = tableBodyRowClassName
        # 从第一行查询的结果中，取出需要断言的值、name
        first_row = rows[0]
        return [first_row, map_header_className]

    def getListPageTableContents(self, el_body=listPage_profilTable_dnsRecords_tableTbody_posXpath):
        """
        获取列表页中表格行的所有数据
        :param listPage_profilTable_subProfiles_tableTbody_posXpath:
        :return:
        """
        element_tbody = self.driver.find_element(By.XPATH, el_body)  # 定位到<tbody>元素，在进一步解析
        rows = element_tbody.find_elements(By.XPATH, "tr")     #获取<tbody>下的所有<tr>行的元素
        return rows

    def getListPage_firstTableData_checkBoxClass_and_ID(self, el_body=listPage_profilTable_dnsRecords_tableTbody_posXpath, sublevel_path_model=0):
        """
        获取列表页中第一列（单元格）中选择框属性和ID值,返回dict
        :parameter sublevel_path_model  可以取值0、1、2、3。。。自定义，默认为0.因为 选择框class属性和id值子级定位在不同的模块下定位方法不一样，需要增加取法判断
        :return: dict
        """
        table_rows = self.getListPageTableContents(el_body=el_body)  # 获得到<tbody>的所有<tr>行元素集合
        id_checkbox_dict = {}
        if len(table_rows) == 0:
            print("列表页中没有数据...")
        else:  # 取出每个行数据
            for tr_s in table_rows:  # 取出每一个行
                el_first_data = tr_s.find_element(By.XPATH, "./td[1]")  # 只取第一单元格数据
                if sublevel_path_model == 0:   # 符合profiles模块下大部分子模块，除了ssl fingerprints
                    first_data_checkbox_class = el_first_data.find_element(By.XPATH, ".//div[@class='table-status-box']//label[contains(@class, 'checkbox')]").get_attribute("class")
                    first_data_id = el_first_data.find_element(By.XPATH, ".//div[@class='table-status-box']//div[contains(@class, 'table-status-item-id')]//span").text.strip()
                elif sublevel_path_model == 1:   # 适用于profiles--ssl fingerprints模块的class和id取用
                    #print(el_first_data.get_attribute('outerHTML'))
                    first_data_checkbox_class = el_first_data.find_element(By.XPATH, ".//*[contains(@class, 'el-checkbox__input')]").get_attribute("class")
                    first_data_id = el_first_data.find_element(By.XPATH, ".//*[contains(@class, 'el-checkbox__original')]").get_attribute("value")
                else:
                    print("sublevel_path_model传入的参数不准确，请检查...")
                id_checkbox_dict[first_data_id] = first_data_checkbox_class
            #print(id_checkbox_dict)
            return id_checkbox_dict

    def linkdata(self, link_list_dict, listPage_profile_dnsRecords_linkButton_posId, listPage_linkTips_dnsRecords_button_save_posXpath,
                 listPage_linkTips_dnsRecords_button_add_posXpath, listPage_linkTips_dnsRecords_button_OK_posXpath):
        """
        :param link_dict:  [{"link_dst_cluster": "42.49-User4Link", "link_dst_vsys":"Vsys2test"}]
        :param link_dst_cluster:
        :param link_dst_vsys:
        :return:
        """
        # 点击 link 按钮
        #{"link_dst_cluster": "42.49-User4Link", "link_dst_vsys":"Vsys2test"}
        #link_dst_cluster = link_dict["link_dst_cluster"]
        #link_dst_vsys = link_dict["Vsys2test"]
        self.driver.find_element(By.ID, listPage_profile_dnsRecords_linkButton_posId).click()
        link_count = len(link_list_dict)
        for link_index in range(len(link_list_dict)):
            link_dst_cluster = link_list_dict[link_index]["link_dst_cluster"]
            link_dst_vsys = link_list_dict[link_index]["link_dst_vsys"]
            # 选择cluster
            self.driver.find_element(By.XPATH, listPage_linkTips_dnsRecords_input_clusterSelect_posXpath).click()
            el_cluster_path = listPage_linkTips_dnsRecords_dropitem_clusterDrop_posXpath.format(replaceName=link_dst_cluster)
            # 下拉列表元素移动到页面显示，在执行js强制点击
            actions = ActionChains(self.driver)
            element_item = self.driver.find_element(By.XPATH, el_cluster_path)
            actions.move_to_element(element_item).perform()
            self.driver.execute_script("arguments[0].click();", element_item)
            # 选择vsys id
            self.driver.find_element(By.XPATH, listPage_linkTips_dnsRecords_input_vsysSelect_posXpath).click()
            el_vsys_path = listPage_linkTips_dnsRecords_dropitem_vsysSelect_posXpath.format(replaceName=link_dst_vsys)
            # 下拉列表元素移动到页面显示，在执行js强制点击
            element_item2 = self.driver.find_element(By.XPATH, el_vsys_path)
            actions.move_to_element(element_item2).perform()
            self.driver.execute_script("arguments[0].click();", element_item2)
            # 点击 保存
            if link_index == 0:
                self.driver.find_element(By.XPATH, listPage_linkTips_dnsRecords_button_save_posXpath).click()
            else:
                self.driver.find_element(By.XPATH, "//*[@id='clusterSave']/i").click()
            if link_index != link_count - 1:  # 不是最后一个cluster 需要添加添加按钮
                self.driver.find_element(By.XPATH, listPage_linkTips_dnsRecords_button_add_posXpath).click()
        # 点击 OK
        self.driver.find_element(By.XPATH, listPage_linkTips_dnsRecords_button_OK_posXpath).click()
        time.sleep(3)
        # 状态断言
        status_info = "color: rgb(141, 203, 75);"
        rows = self.driver.find_element(By.XPATH, listPage_profilTable_dnsRecords_tableTbody_posXpath).find_elements(By.XPATH, "./tr")
        print(len(rows))
        for row_0 in rows:
            status_style = row_0.find_element(By.XPATH, "./td[7]//i").get_attribute("style")
            print(status_style)
            pytest_check.is_in(status_info, status_style, msg="所在行数{}".format(inspect.currentframe().f_lineno))

    def select_lock_and_referenceCount(self, rows, islock=False, referenceCount=0):
        """
        筛选点击是 否有锁、引用数是否为0的数据，默认选择列表列中无锁且引用为0的数据。
        :param rows:
        :param lock: False True
        :param referenceCount: 0， 1
        :return:  0 表示有删除对象， 1表示没有删除对象
        """
        referenceCount = (referenceCount)
        return_code = 1
        for row_item in rows:  # 每一行操作
            el_td_1 = row_item.find_element(By.XPATH, "./td[1]")
            # 获取第一列元素下所有的属性
            child_class_list = []
            el_child_list = el_td_1.find_elements(By.XPATH, ".//*")
            for el_child_item in el_child_list:
                # print(el_child_item.get_attribute("class"))
                child_class_list.append(el_child_item.get_attribute("class"))
            # 如果没有 icon-lock 属性，则需要点击选择框
            child_class_list = list(set(child_class_list))  # 去重
            lock_flag = 0   # 没有锁
            refer_count = 0  # 引用为0
            click_flag = 0   # 0不点击、1点击
            for _ in child_class_list:  # 校验所有的class 中是否有 该属性
                if "icon-lock" in _:
                    lock_flag = 1  # 有锁 则变成1
                    break
                    # print(child_class_list)
            # 再次查找元素是引用是否不为0
            el_td_list = row_item.find_elements(By.XPATH, "./td")  # 每一列操作
            # 判断一下，是否存在 Reference Count 列，如果存在，则需要进一步操作
            for el_td_item in el_td_list:
                td_item_id_list = []  # 每一列存放id的属性
                td_item_childs = el_td_item.find_elements(By.XPATH, ".//*")
                for td_child in td_item_childs:
                    td_item_id_list.append(td_child.get_attribute("id"))
                td_item_id_list = list(set(td_item_id_list))  # 去重
                # print(td_item_id_list)
                refer_except = "ReferenceData-"  # ReferenceData-_DNSRecordProfile_Home_App_anonymousComponent  id中存在预期值即可
                for td_id_item in td_item_id_list:
                    if refer_except in td_id_item:  # 存在这个部分id属性即可
                        refer_counter_actual = el_td_item.find_element(By.XPATH, f".//*[@id='{td_id_item}']").text.strip()
                        print(td_id_item, ">>>", refer_counter_actual)
                        if refer_counter_actual != "0":    #
                            refer_count = 1  # 引用数不为 0

            # lock=False, referenceCount=0  # 传入参数和实际判断参数对比，确认是否点击
            if islock == False:   # 选择没有锁的
                if referenceCount == 0:   # 选择引用为0的
                    if lock_flag == 0 and refer_count == 0:
                        click_flag = 1
                else:    # 选择引用不为0的
                    if lock_flag == 0 and refer_count == 1:
                        click_flag = 1
            else:    # 选择有锁的
                if referenceCount == 0:  # 选择引用为0的
                    if lock_flag == 1 and refer_count == 0:
                        click_flag = 1
                else:  # 选择引用不为0的
                    if lock_flag == 1 and refer_count == 1:
                        click_flag = 1

            if click_flag == 1:  # 没有 icon-lock  引用为0，， 需要点击
                el_td_1.find_element(By.XPATH, ".//*[@class='el-checkbox__input']").click()
                return_code = 0
                time.sleep(0.2)
        return return_code


    def check_checkBoxClass_by_buttonAll(self, el_body=listPage_profilTable_dnsRecords_tableTbody_posXpath, el_all_btn=mainPage_profileBottomPage_button_allSelect_posXpath, sublevel_path_model=0):
        """
        点击页面底部all后，判断列表页第一列中，选择框的属性值，有is-checked属性，表明已经勾选
        :param el_body: body元素定位，大部分是上都是默认的
        :param el_all_btn: 页面底部all定位，大部分都是默认相同的
        :param sublevel_path_model: 是 getListPage_firstTableData_checkBoxClass_and_ID(self, el_body=listPage_profilTable_dnsRecords_tableTbody_posXpath, sublevel_path_model=0)
            函数的使用参数，具体取值是什么，请查看该函数定义
        :return:
        """
        id_checkbox_dict = self.getListPage_firstTableData_checkBoxClass_and_ID(el_body=el_body, sublevel_path_model=sublevel_path_model)
        print(id_checkbox_dict)
        if id_checkbox_dict == {}:
            return 0
        # 点击all前属性判断，此时无is-checked 属性
        first_data_checkbox_class_except = "is-checked"
        print("all button 点击前属性验证...")
        for k,v in id_checkbox_dict.items():
            pytest_check.is_not_in(first_data_checkbox_class_except, v, msg="所在行数{}".format(inspect.currentframe().f_lineno))

        # 点击all后，属性判断，此时有is-checked 属性
        self.driver.find_element(By.XPATH, el_all_btn).click()
        time.sleep(1)
        id_checkbox_dict = self.getListPage_firstTableData_checkBoxClass_and_ID(el_body=el_body)
        print(id_checkbox_dict)
        if id_checkbox_dict == {}:
            return 0
        print("all button 点击后属性验证...")
        for k,v in id_checkbox_dict.items():
            pytest_check.is_in(first_data_checkbox_class_except, v, msg="所在行数{}".format(inspect.currentframe().f_lineno))

        # 再点击all，取消点击后，属性判断，此时没有is-checked 属性
        self.driver.find_element(By.XPATH, el_all_btn).click()
        id_checkbox_dict = self.getListPage_firstTableData_checkBoxClass_and_ID(el_body=el_body)
        print(id_checkbox_dict)
        if id_checkbox_dict == {}:
            return 0
        # 取消all点击后判断，此时无is-checked 属性
        print("all button 取消点击后属性验证...")
        for k,v in id_checkbox_dict.items():
            pytest_check.is_not_in(first_data_checkbox_class_except, v, msg="所在行数{}".format(inspect.currentframe().f_lineno))

    def delete(self, listPage_profile_subProfiles_delButton_posId, listPage_dialogTips_subProfiles_button_yes_posCss,
               listPage_dialogTips_subProfiles_button_no_posCss):
        """
        直接删除函数，
        :param listPage_profile_subProfiles_delButton_posId: 删除按钮id
        :param listPage_dialogTips_subProfiles_button_yes_posCss: 提示删除框中yes定位css
        :param listPage_dialogTips_subProfiles_button_no_posCss: 提示删除框中no定位css
        :return:
        """
        self.driver.find_element(By.ID, listPage_profile_subProfiles_delButton_posId).click()  # 点击删除按钮
        random_yes_or_no = random.randint(0, 1)
        if random_yes_or_no == 0:  # 点击yes，删除
            self.driver.find_element(By.CSS_SELECTOR, listPage_dialogTips_subProfiles_button_yes_posCss).click()  # 直接删除
        else:
            self.driver.find_element(By.CSS_SELECTOR,
                                     listPage_dialogTips_subProfiles_button_no_posCss).click()  # 先取消，再删除
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

    def check_ip_address(self, ip_str):
        """
        判断输入的是ipv4、ipv6、非ip地址
        :return:
        """
        try:
            # 将输入的字符串解析为 IP 地址对象
            ip = ipaddress.ip_address(ip_str)
            # 检查地址类型
            if isinstance(ip, ipaddress.IPv4Address):
                print(f"{ip_str} 是一个有效的 IPv4 地址")
                return "ipv4"
            elif isinstance(ip, ipaddress.IPv6Address):
                print("{ip_str} 是一个有效的 IPv6 地址")
                return "ipv6"
        except ValueError:
            print(f"{ip_str} 不是一个有效的 IP 地址")
            return "not_ip"

    def get_name_from_data(self, data):
        """
        从用例dict中获取name，含有随机判断效果
        :param data:
        :return:
        """
        if "name" in data.keys():
            name = data["name"]
            random_name = self.my_random.random_name(source_name=name, is_none=True)
        else:
            random_name = self.my_random.random_name()
        return random_name

    def change_vsys(self, vsys_name=""):
        """
        调整vsys，vsys_name可以为空字符串，不用切换vsys。vsys_name=空时，默认切换到UIAutoTestVsys
        :param vsys_name:  vsys name, 例如：Default Vsys 、或者空。vsys_name与当前vsys一直或者为空字符串时，不要操作vsys
        :return:
        """
        current_vsys_name = self.driver.find_element(By.XPATH, mainPage_currentPage_vsysName_posXpath, find_before_wait_time=0.6, ).text.strip().lower()
        if vsys_name.lower() == current_vsys_name:
            #print(f"当前系统所在vsys：{current_vsys_name}")
            return 0
        else:  # 空为切换默认   剩下为指定切换
            if vsys_name == "":  # 空，切换到默认vsys
                config_content = configparser.ConfigParser()
                config_content_dir = os.path.join(workdir, "config", "loginout.ini")
                config_content.read(config_content_dir, encoding="utf-8")
                change_vsys_name = config_content.get("vsys", "vsys_name")
                # change_vsys_name = "UIAutoTestVsys"
                if change_vsys_name.lower() == current_vsys_name:  # 如果默认系统和当前一直，也不用点击
                    #print(f"当前系统所在vsys：{current_vsys_name}")
                    return 0
            else:  # 切换到指定vsys
                change_vsys_name = vsys_name
            #print(f"当前系统所在vsys：{current_vsys_name}，需要切换到vsys：{change_vsys_name}")
            self.driver.find_element(By.CSS_SELECTOR, mainPage_button_menu_posXCss).click()  # 点击vsys menu
            # 如果切换vsys时弹出 Leave this page?的确认弹窗，点击确认
            if self.driver.element_isExist(By.XPATH, leave_this_page_elem_Xpath, timeout=0.5):
                try:   # 上述条件判断中，会存在会存在对应的元素，但是没有提示框情况，因此异常跳过继续执行
                    self.driver.find_element(By.XPATH, leave_this_page_ok_elem_Xpath).click()
                except:
                    print("上述点击步骤存在异常，跳过继续执行...")
                    pass
            else:
                pass
            vsys_tree_name_list = self.driver.find_elements(By.XPATH, mainPage_vsysTree_vsysName_posXpath)
            flag_num = 0
            for el_vsys_item in vsys_tree_name_list:
                vsys_item_name = el_vsys_item.text.strip().lower()
                if vsys_item_name == change_vsys_name.lower():
                    flag_num = 1
                    el_vsys_item.click()
                    break
            if flag_num == 0:
                #print(f"测试用户没有vsys：{change_vsys_name}")
                raise ValueError(f"user vsys:{change_vsys_name}")

    def column_setting(self, mainPage_profileColumn_columnSetting_posId,
                       listPage_profileColumn_button_columnAll_posXpath, listPage_profileColumn_button_cancel_posId,
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
        columnAll_class = self.driver.find_element(By.XPATH,
                                                   listPage_profileColumn_button_columnAll_posXpath).get_attribute(
            "class").split()
        print("columnAll_class=", columnAll_class)
        if column_flags == 0:  # 保持当前状态
            self.driver.find_element(By.ID, listPage_profileColumn_button_cancel_posId).click()  # 点击cancel按钮
        elif column_flags == 1:  # 仅显示默认列
            if "is-checked" in columnAll_class:
                self.driver.find_element(By.XPATH,
                                         listPage_profileColumn_button_columnAll_posXpath).click()  # 取消点击列All按钮
                self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
            else:
                self.driver.find_element(By.XPATH, listPage_profileColumn_button_columnAll_posXpath).click()  # 点击列All按钮
                self.driver.find_element(By.XPATH,
                                         listPage_profileColumn_button_columnAll_posXpath).click()  # 取消点击列All按钮
                self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
        elif column_flags == 2:  # 显示所有列
            if "is-checked" in columnAll_class:
                self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
            else:
                self.driver.find_element(By.XPATH, listPage_profileColumn_button_columnAll_posXpath).click()  # 点击列All按钮
                self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
        else:
            for name in column:
                # print("name=", name)
                self.driver.find_element(By.XPATH,
                                         f"//*[@id='dropColRes-_ElementSet_{Profiles}_Home_App_anonymousComponent']//span[contains(text(),'{name}')]").click()  # 选择指定列按钮
            self.driver.find_element(By.ID, listPage_profileColumn_button_ok_posId).click()  # 点击ok按钮
        element_header = self.driver.find_element(By.XPATH,
                                                  "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead//tr")  # 查询table的header
        headers = element_header.find_elements(By.XPATH, "//th[@colspan='1']")  # table header
        # print("headers=", headers)
        # print("headers_len=", len(headers))
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
        max_page_num = self.driver.find_element(By.XPATH,
                                                f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']").find_element(
            By.XPATH, ".//li[last()]").text.strip()
        max_page_num = int(max_page_num)
        if pages > max_page_num:  # 如果传入的页数大于最大的也是，则取最大页数值
            pages = max_page_num
        for number in range(1, pages):
            self.driver.find_element(By.XPATH, "//div[@class='pagination']//button[contains(@class, 'btn-next')]").click()
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
            random_page = random.sample(range(1, pages + 1), 1)[0]
            print("random_page=", random_page)
            self.driver.find_element(By.XPATH, "//div[@class='pagination']//span[text()='Go to']//input").send_keys(Keys.CONTROL + "a")
            self.driver.find_element(By.XPATH, "//div[@class='pagination']//span[text()='Go to']//input").send_keys(Keys.BACKSPACE)
            self.driver.find_element(By.XPATH, "//div[@class='pagination']//span[text()='Go to']//input").send_keys(random_page)
            time.sleep(0.5)
            self.driver.find_element(By.XPATH, "//div[@class='pagination']//span[text()='Go to']//input").send_keys(Keys.RETURN)
            time.sleep(0.5)
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            pytest_check.equal(current_page_content, random_page,
                               msg="所在行数{}".format(inspect.currentframe().f_lineno))
            time.sleep(0.5)
        # 随机点击某页
        for _ in range(3):
            enview_pages_element = self.driver.find_elements(By.XPATH, "//ul[@class='el-pager']//li")
            enview_pages = []
            if pages < 8:
                random_page = random.sample(range(1, pages + 1), 1)[0]
                print("random_page=", random_page)
                btn = self.driver.find_element(By.XPATH, f"//li[text()='{random_page}']")
                self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
            if pages >= 8:
                for i in range(len(enview_pages_element)):
                    print("1=", enview_pages_element[i].text)
                    if enview_pages_element[i].text != "":
                        enview_pages.append(enview_pages_element[i].text)
                # print(enview_pages)
                random_page = random.sample(range(1, len(enview_pages) + 1), 1)[0]
                random_page = int(enview_pages[random_page - 1])
                btn2 = self.driver.find_element(By.XPATH, f"//li[text()='{random_page}']")
                self.driver.execute_script("arguments[0].click()", btn2)  # 强制点击
            time.sleep(0.5)
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            pytest_check.equal(current_page_content, random_page,
                               msg="所在行数{}".format(inspect.currentframe().f_lineno))
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
            self.driver.find_element(By.XPATH, "//div[@class='pagination']//button[contains(@class, 'btn-prev')]").click()
            time.sleep(0.5)
            # 当前页XPATH
            current_page = f"//*[@id='pagination-_pagination_{profiles}_Home_App_anonymousComponent']//li[contains(@class, 'active')]"
            current_page_content = int(self.driver.find_element(By.XPATH, current_page).text.strip())
            # print("current_page_content=", current_page_content)
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
            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
        elif language == 1:
            btn = self.driver.find_element(By.XPATH, mainPage_language_chinese_posXpath)
            self.driver.execute_script("arguments[0].click()", btn)
        elif language == 2:
            btn = self.driver.find_element(By.XPATH, mainPage_language_russian_posXpath)
            self.driver.execute_script("arguments[0].click()", btn)
        time.sleep(1)
        element_header = self.driver.find_element(By.XPATH,
                                                  "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead//tr")  # 查询table的header
        headers = element_header.find_elements(By.XPATH, "//th[@colspan='1']")  # table header
        # print("headers=", headers)
        # print("headers_len=", len(headers))
        headers_content = []
        for th in headers:
            self.driver.execute_script("arguments[0].scrollIntoView();", th)
            header_content = th.text.strip()
            # print("header_content=", header_content)
            if header_content != "":
                headers_content.append(header_content)
        return headers_content

    def data_limit(self, listPage_profile_profiles_editButton_posId, listPage_profile_profiles_delButton_posId):
        """校验数据是否只有查看权限"""
        # 校验当前数据是否为只能查看
        text_view = self.driver.find_element(By.ID, listPage_profile_profiles_editButton_posId).text.strip()
        print("text_view=", text_view)
        pytest_check.equal(self.driver.find_element(By.ID, listPage_profile_profiles_editButton_posId).text.strip(),
                           "View", msg="所在行数{}".format(inspect.currentframe().f_lineno))
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
                      rule_action_posId, rule_source_add_posXpath, rule_button_oK_posId, rule_button_cancel_posId,
                      rule_button_warningSaveYes_posCss,
                      application="http", rule_application_add_posXpath="", rule_application_search_posXpath="",
                      *actionParameters):
        """若策略为Intercept时，actionParameters[0]表示为引用profile的类型： Traffic_Mirror_Profile、SSL_Decryption_Keyring、SSL_Decryption_Profile、TCP_Proxy_Profile"""
        # 点击创建按钮
        self.driver.find_element(By.ID, listPage_rule_create_button_posId).click()
        # 输入name
        policy_name = profile_name + "Rule"
        self.driver.find_element(By.XPATH, rule_input_Name_posXpath).send_keys(policy_name)
        # 选择Action
        self.driver.find_element(By.ID, rule_action_posId).click()
        # 选择source
        self.driver.find_element(By.XPATH, rule_source_add_posXpath).click()
        time.sleep(0.5)
        ## 选择IP的第一条记录
        self.driver.find_element(By.XPATH,
                                 "//div[@class='CommonListDetail list-detail']//ul[contains(@class, 'tableList')]/li[1]").click()
        # 关闭侧滑框
        self.driver.find_element(By.XPATH, "//div[contains(text(),'IP Address')]/i").click()
        # 选择Application
        application_isselected = ["Manipulation_Allow", "Manipulation_Deny", "Manipulation_Monitor",
                                  "Manipulation_Replace", "Manipulation_Hijack", "Manipulation_Insert",
                                  "Manipulation_EditElement", "Manipulation_RunScript"]
        if action in application_isselected:
            pass
        elif action == "Intercept":
            self.driver.find_element(By.XPATH, rule_application_add_posXpath).click()
            self.driver.find_element(By.XPATH,
                                     f"//div[@class='AppList list-box']//div[@class='CommonListDetail list-detail']//ul[contains(@class, 'tableList')]//span[text()='{application}']").click()
        else:
            self.driver.find_element(By.XPATH, rule_application_add_posXpath).click()
            self.driver.find_element(By.XPATH, rule_application_search_posXpath).send_keys(application)
            self.driver.find_element(By.XPATH, rule_application_search_posXpath).send_keys(Keys.ENTER)
            self.driver.find_element(By.XPATH,
                                     "//div[@class='AppList list-box']//div[@class='CommonListDetail list-detail']//ul[contains(@class, 'tableList')]/li[1]").click()
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
                if self.driver.find_element(By.XPATH, "//li[contains(@id, 'filelist_')]").get_attribute(
                        "id") == "filelist_null":
                    pytest_check.equal(
                        self.driver.find_element(By.XPATH, "//li[contains(@id, 'filelist_')]").text.strip(),
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
            self.driver.find_element(By.XPATH, actionParameters[5]).send_keys(profile_name)  # 输入查询值
            self.driver.find_element(By.XPATH, actionParameters[5]).send_keys(Keys.ENTER)  # 模拟回车按键
            time.sleep(1)
            if self.driver.find_element(By.XPATH, "//li[contains(@id, 'filelist_')]").get_attribute(
                    "id") == "filelist_null":
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
            self.driver.find_element(By.XPATH, "//ul[@class='row-container tableList']/li[1]").click()  # 选择第一条URL
            # 选择hijack file
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[3]).click()
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)  # 输入查询值
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)  # 模拟回车按键
            if self.driver.find_element(By.XPATH,
                                        "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute(
                "id") == "filelist_null":
                pytest_check.equal(self.driver.find_element(By.XPATH,
                                                            "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                result = "No Data"
            else:
                self.driver.find_element(By.XPATH,
                                         "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").click()
                result = self.driver.find_element(By.XPATH,
                                                  "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute(
                    "value")
        elif action == "Manipulation_Insert":
            # 选择URL ---URL为必填项
            self.driver.find_element(By.XPATH, actionParameters[0]).click()
            self.driver.find_element(By.XPATH, actionParameters[1]).click()
            self.driver.find_element(By.XPATH, actionParameters[2]).click()
            self.driver.find_element(By.XPATH, "//ul[@class='row-container tableList']/li[1]").click()  # 选择第一条URL
            # 选择hijack file
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[3]).click()
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)  # 输入查询值
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)  # 模拟回车按键
            if self.driver.find_element(By.XPATH,
                                        "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute(
                "id") == "filelist_null":
                pytest_check.equal(self.driver.find_element(By.XPATH,
                                                            "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                result = "No Data"
            else:
                self.driver.find_element(By.XPATH,
                                         "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").click()
                result = self.driver.find_element(By.XPATH,
                                                  "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute(
                    "value")
        elif action == "Manipulation_RunScript":
            pass
            # 选择URL ---URL为必填项
            self.driver.find_element(By.XPATH, actionParameters[0]).click()
            self.driver.find_element(By.XPATH, actionParameters[1]).click()
            self.driver.find_element(By.XPATH, actionParameters[2]).click()
            self.driver.find_element(By.XPATH, "//ul[@class='row-container tableList']/li[1]").click()  # 选择第一条URL
            # 选择hijack file
            self.driver.find_element(By.CSS_SELECTOR, actionParameters[3]).click()
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)  # 输入查询值
            self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)  # 模拟回车按键
            if self.driver.find_element(By.XPATH,
                                        "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute(
                "id") == "filelist_null":
                pytest_check.equal(self.driver.find_element(By.XPATH,
                                                            "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").text.strip(),
                                   "No Data", msg="所在行数{}".format(inspect.currentframe().f_lineno))
                result = "No Data"
            else:
                self.driver.find_element(By.XPATH,
                                         "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").click()
                result = self.driver.find_element(By.XPATH,
                                                  "//body/div[contains(@class,'el-select-dropdown')]//ul//div[@class='select-search-option']/li").get_attribute(
                    "value")
        elif action == "Intercept":
            if application == "ssl":
                if actionParameters[0] == "Traffic_Mirror_Profile":
                    # Mirror Decrypted Traffic
                    self.driver.find_element(By.XPATH, actionParameters[1]).click()
                    assert self.driver.find_element(By.XPATH, actionParameters[1]).get_attribute("class").split(" ")[
                               -1] == "is-checked"
                    # Add VLAN ID
                    if self.driver.find_element(By.XPATH, actionParameters[2]).get_attribute("class").split(" ")[
                        -1] != "is-checked":
                        self.driver.find_element(By.XPATH, actionParameters[2]).click()
                    # Traffic Mirror Profile
                    self.driver.find_element(By.XPATH, actionParameters[3]).click()
                    self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(profile_name)
                    self.driver.find_element(By.XPATH, actionParameters[4]).send_keys(Keys.ENTER)
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
                        # result = self.driver.find_element(By.XPATH, "(//div[@class='select-search-option'])[6]/li[2]").get_attribute("value")
                        result = self.driver.find_element(By.XPATH,
                                                          "//label[text()='Traffic Mirror Profile']/parent::div//input").get_attribute(
                            "value")
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
                        profile_results[1].click()  # 获取第一条profile [0]为No Data
                        result = self.driver.find_element(By.XPATH,
                                                          f"//label[text()='{actionParameters[3]}']/parent::div//input").get_attribute(
                            "value")
                        print("result=", result)
                elif actionParameters[0] == "SSL_Decryption_Profile":
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
                        # result = self.driver.find_element(By.XPATH, "(//div[@class='select-search-option'])[6]/li[2]").get_attribute("value")
                        result = self.driver.find_element(By.XPATH,
                                                          "//label[text()='Decryption Profile']/parent::div//input").get_attribute(
                            "value")
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
                        # result = self.driver.find_element(By.XPATH, "(//div[@class='select-search-option'])[6]/li[2]").get_attribute("value")
                        result = self.driver.find_element(By.XPATH,
                                                          "//label[text()='TCP Proxy Profile']/parent::div//input").get_attribute(
                            "value")
                        print("result=", result)
        time.sleep(2)
        # 保存策略
        if result == "No Data":
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
                     listPage_policiesTable_tableTbody_posXpath, listPage_policiesTable_tableHeader_posXpath, **kwargs):
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
                key = key.replace("_", " ")  # 将下划线替换为空格
            dropdown_item_posXpath = listPage_policiesSearch_dropDown_item_posXpath.format(replaceName=key)
            self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()  # 点击下拉item
            input_item_posXpath = listPage_policiesSearch_input_itemContent_posXpath.format(replaceName=key)
            self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(value.strip())  # 输入查询值
            self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(Keys.ENTER)  # 模拟回车按键
        # 点击查询按钮
        element_search = self.driver.find_element(By.ID, listPage_policiesSearch_buttonSearch_posId)
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        element_tbody = self.driver.find_element(By.XPATH,
                                                 listPage_policiesTable_tableTbody_posXpath)  # 找到所有的行，table的body
        element_header = self.driver.find_element(By.XPATH,
                                                  listPage_policiesTable_tableHeader_posXpath)  # 查询table的header
        # 获取table header的text、th.class
        headers = element_header.find_elements(By.XPATH, "th")  # table header
        rows = element_tbody.find_elements(By.XPATH, "tr")  # table body
        if len(rows) == 0:
            #print(f"没有查询到数据：查询条件：{kwargs}")
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


def download_file():
    my_file = ReadData()
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': my_file._profiles_files_dowload_path(), 'safebrowsing.enabled': True}
    webdriver.ChromeOptions()
    loginout_parse = configparser.ConfigParser()
    loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
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


def cached_intermediate_certificates_driver():
    my_file = ReadData()
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': my_file._profiles_files_dowload_path(), 'safebrowsing.enabled': True}
    webdriver.ChromeOptions()
    loginout_parse = configparser.ConfigParser()
    loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
    loginout_parse.read(loginout_parse_dir, encoding="utf-8")
    remote_url = loginout_parse.get("remote_url", "url")
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--incognito")
    driver = MyWebDriver(
        command_executor=remote_url,
        options=options)
    driver.implicitly_wait(5)
    login_url = loginout_parse.get("tsg_url", "login_url")
    driver.get(login_url)
    driver.maximize_window()
    # 需要判断，遇到https不安全时，点击高级-继续登录才可以访问https-tsg
    if "https" in login_url:
        driver.isElementExist("//*[@id='details-button']")
        if driver.Exist:
            if "高级" in driver.find_element(By.XPATH, "//*[@id='details-button']").text.strip():
                driver.find_element(By.XPATH, "//*[@id='details-button']").click()
                driver.find_element(By.XPATH, "//*[@id='proceed-link']").click()
    aut_username = loginout_parse.get("ui_account_1_cached", "username")
    aut_pwd = loginout_parse.get("ui_account_1_cached", "passwd")
    driver.find_element(By.NAME, loginPage_userName_posName).send_keys(aut_username)
    driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(aut_pwd)
    driver.find_element(By.ID, "login").click()
    return driver
