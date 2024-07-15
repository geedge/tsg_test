# 标准库导入
import configparser
import os
import random
import time
import re

# 第三方库导入
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 本地库导入
from support.general_ui_utils.workpath import workdir
from support.general_ui_utils.random_name import RandomName
from support.general_ui_utils.read_data import ReadData
from support.general_ui_utils.element_position.objects_element_position import *
from support.general_ui_utils.element_position.ln_objects_element_positionMERGELAST import *
from support.general_ui_utils.element_position.policies_element_position import *
from support.general_ui_utils.object.objects_public_operations import (
    ObjectsPublicOperations,
    get_txt_filenames,
    download_files,
)
from support.general_ui_utils.profile.profiles_public_operations import ProfilesPublicOperations

class Tunnel:
    def __init__(self, driver):
        self.driver = driver
        self.my_files = ReadData()
        self.objects_po=ObjectsPublicOperations(self.driver)
        self.my_random = RandomName()
        self.random_item = self.my_random.random_tunnel()
        self.export_number = 0
        self.loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
        self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        self.profile_pub = ProfilesPublicOperations(self.driver)
        # try:
        #     element = self.driver.find_element(By.XPATH, '//*[@class="iconfont icon-Delete_X"]')
        #     element.click()
        # except NoSuchElementException:
        #     pass

#screenshot_on_failure是一个装饰器，可以在方法执行失败时自动截图
    def tunnel_case(self, data):#接受一个data的参数，类型为字典
        self.driver.implicitly_wait(10)
        self._create(data)
        self._modify(data)
        self._delete(data)
    def tunnel_column_settings_case(self):
        self.driver.implicitly_wait(10)
        self._goto_subObjectPage()
        self.objects_po.Column_settings(Column=listPage_object_tunnel_type_Button_posXpath)
        self.objects_po.Column_ele_ex(Column_text=self.objects_po.Column_text)
        assert self.objects_po.result

    def  name_length_limit(self,data):
        self._create(data)

    def input_verify(self,data):
        # 调用消除右上提示弹窗
       # self.objects_po.dismiss_right_top_tips(mainPage_rightTopTips_closeButton_posXpath)
        # 跳转到Tunnel列表页
        self._goto_subObjectPage()
        # Create Tunnel Object
        self.driver.find_element(By.ID, listPage_object_Tunnels_createButton_posId).click()  # 点击Create
        # name最大长度限制
        self.error_length_name = "tst"
        error_item = "12334"

        self.driver.find_element(By.XPATH, Tunnel_ObjectPage_InputName_posXpath).send_keys(self.error_length_name)  # 输入超长名字
        # self.driver.find_element(By.XPATH, Tunnel_ObjectPage_inputItem_posXpath).send_keys(error_item)  #
        # self.driver.find_element(By.XPATH, TunnelsObjectPage_textArea_Description_posXpath).send_keys("")  # 不添加描述

        #点击页面其他区域
        self.driver.find_element(By.XPATH, Tunnel_ObjectPage_inputItem_posXpath).click() #

        name_error_message=self.driver.find_element(By.XPATH,'//form/div[1]/div/div[2]').text #输入不足四个字符时的提示信息
        name_actual_message='The length of the name is at most 32 characters and cannot be less than 4 characters'
        assert name_actual_message ==  name_error_message.strip() # 校验输入name不足四个字符时的提示信息
        # endpoint_error_message = self.driver.find_element(By.XPATH, '//form/div[4]/div[1]/div/div[2]').text  #
        # endpoint_actual_message = 'Format error'
        # assert endpoint_actual_message == endpoint_error_message.strip()  # 校验
        # des_error_message = self.driver.find_element(By.XPATH,'//form/div[4]/div[2]/div/div[3]').text #
        # des_actual_message = 'Cannot be empty'
        # assert des_actual_message == des_error_message.strip()  #

    def _goto_subObjectPage(self):
        # 菜单操作 跳转到Tunnel页面
        #self.driver.refresh()
        self.driver.find_element(By.ID, mainPage_firstLevelMenu_Objects_posId).click()
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_Tunnel_posId).click()

    def pop_export_part(self):
        self.driver.find_element(By.XPATH, listPage_object_Tunnels_exportButton_posXPATH).click()
        self.driver.find_element(By.XPATH, tunnel_export_pop_window_master_select_button_xpath).click()  # 取消选中导出
        self.driver.find_element(By.XPATH, tunnel_export_pop_window_first_checkbox_button_xpath).click()  # 选择第一个
        self.export_total_str = self.driver.find_element(By.XPATH,tunnel_export_pop_window_export_num_button_xpath).text #定位到导出个数的按钮
        self.export_total = re.search(r'\d+', self.export_total_str)  # 正则表达式返回匹配的数字对象
        if self.export_total:
            self.export_number = int(self.export_total.group())  # group()方法返回正则表达式匹配的字符串
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.export_number)

        self.driver.find_element(By.XPATH, listPage_object_urls_exportPopYes_posXpath).click() #确认导出
    def pop_cancel_export_num(self):
        self.driver.find_element(By.XPATH, listPage_object_Tunnels_exportButton_posXPATH).click()
        self.driver.find_element(By.XPATH, tunnel_export_pop_window_master_select_button_xpath).click()#取消选中导出
        self.driver.is_exist_element(Element=listPage_object_urls_exportPopYes_posXpath)
        assert self.driver.is_exist, "断言导出按钮是否置灰不展示"
        self.driver.find_element(By.XPATH,tunnel_export_pop_no).click()
        self.driver.refresh()

    def _export_objects(self):
        self.driver.find_element(By.XPATH, listPage_object_Tunnels_exportButton_posXPATH).click()
        time.sleep(3)
        self.export_total_str = self.driver.find_element(By.XPATH,tunnel_export_pop_window_export_num_button_xpath).text
        self.driver.find_element(By.XPATH, listPage_object_urls_exportPopYes_posXpath).click()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 11111)
        self.export_total =re.search(r'\d+',self.export_total_str)  #正则表达式返回匹配的数字对象
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.export_total_str)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 2222)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.export_total)
        if self.export_total:
            self.export_number = int(self.export_total.group())#group()方法返回正则表达式匹配的字符串
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.export_number)

    def _export_objects_and_verify(self,data):
        self._create(data)#新建,新建后就是查询到该条数据的状态
        self.driver.find_element(By.XPATH, listPage_object_Tunnels_select_First_object_posXpath).click()#选中第一行
        self._export_objects()#选中并导出文件
        time.sleep(3)
        self.file_name = get_txt_filenames(path=self.my_files._obj_files_dowload_path())
        self.file_path = self.my_files._obj_files_dowload_path() + "\\" + self.file_name
        self.content = open(self.file_path,"rb").read()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "self.content |||self.random_item".format(self.content, self.random_item))
        try:
            # assert str(data['Items'][0]) in str(self.content), "断言导出内容是否在txt文件中"
            assert str(self.random_item) in str(self.content), "断言导出内容是否在txt文件中"
            os.remove(self.file_path)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "文件删除成功")
        except FileNotFoundError:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "文件不存在")
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "发生异常:", e)
        self._delete(data)

    def export_multi_condition_test(self,data):
        self.create_tunnel(data)  # 新建,新建后就是查询到该条数据的状态
        if data["SubType"] == "cancel_export":
            #1、单个Object导出取消选中目标数据
            self.driver.find_element(By.XPATH, listPage_object_Tunnels_select_First_object_posXpath).click()
            self.pop_cancel_export_num()
            self.create_tunnel(data)
            # 2、多个Object导出取消选中目标数据(2个)
            self.driver.find_element(By.XPATH, listPage_object_Tunnels_select_First_object_posXpath).click()
            self.driver.find_element(By.XPATH, listPage_object_Tunnels_select_second_object_posXpath).click()
            self.pop_cancel_export_num()
            self._delete(data)
        elif data["SubType"] == "multi_export":
            self.create_tunnel(data)
            self.driver.find_element(By.XPATH, listPage_object_Tunnels_select_First_object_posXpath).click()
            self.driver.find_element(By.XPATH, listPage_object_Tunnels_select_second_object_posXpath).click()
            if data["multi_type"] == "all":#4、多选导出所有数据，校验行数
                self._export_objects()
                assert self.export_number == 2,"断言多选全部导出是否符合预期"
                self._delete(data)
            else:#3、多选导出第一个数据
                self.pop_export_part()
                assert self.export_number == 1,"断言单选导出数据是否符合预期"
                time.sleep(1)
                self.driver.refresh()
                self._delete(data)
        self.driver.refresh()
        self._delete(data)


    def _verify_audit_logs(self,data):
        self._create(data) #新建后已经查询了
        self.select_first_row_data_and_edit(data)
        #Audit Logs校验
        self.driver.find_element(By.XPATH, url_ObjectDetailPage_auditLogs_posXpath).click()
        self.driver.is_exist_element(Element='//table/tbody/tr')
        assert self.driver.is_exist == True, "断言新建object是否存在创建日志"
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "断言成功，存在创建记录，测试 === Success")
        self.driver.is_exist_element(Element='(//table/tbody/tr)[2]')
        assert self.driver.is_exist == False, "断言新建object是否存在编辑日志"
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "断言成功，不存在编辑记录，测试 === Success")
        self.driver.find_element(By.XPATH,acc_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath).click()  # 勾选第一行log CheckBox
        self.driver.find_element(By.XPATH,acc_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath).click()  # 点击compare 按钮
        try:
            operation = self.driver.find_element(By.XPATH,acc_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath).text
            assert operation == "Create", "最新一条audit log 非 Create log！！！！"
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "校验成功，获取到 Create log")
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], e)
            raise
        self._modify(data)
        self.select_first_row_data_and_edit(data)
        self.driver.find_element(By.XPATH, url_ObjectDetailPage_auditLogs_posXpath).click()
        self.driver.is_exist_element(Element='//table/tbody/tr')
        assert self.driver.is_exist, "断言新建object是否存在创建日志"
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "断言成功，存在创建记录，测试 === Success")
        self.driver.is_exist_element(Element='(//table/tbody/tr)[2]')
        assert self.driver.is_exist, "断言新建object是否存在编辑日志"
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "断言成功，存在编辑记录，测试 === Success")
        self.driver.find_element(By.XPATH,acc_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath).click()  # 勾选第一行log CheckBox
        self.driver.find_element(By.XPATH,acc_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath).click()  # 点击compare 按钮
        try:
            operation = self.driver.find_element(By.XPATH,acc_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath).text
            assert operation == "Edit", "最新一条audit log 非 Edit log！！！！"
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "校验成功，获取到 Edit log")
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], e)
            raise

        #删除该元素
        self._delete(data)

    def select_first_row_data_and_edit(self,data):
        # self._goto_subObjectPage()
        # self._search(data)
        #查询后编辑
        self.driver.find_element(By.XPATH, listPage_object_Tunnels_select_First_object_posXpath).click()
        self.driver.find_element(By.ID, listPage_object_Tunnels_editButton_posId).click()  # edit按钮

    def _verify_not_checkbox_export(self,data):
        # 调用消除右上提示弹窗
       #self.objects_po.dismiss_right_top_tips(mainPage_rightTopTips_closeButton_posXpath)
        self._goto_subObjectPage()
        #未选中导出
        #self.driver.find_element(By.XPATH,listPage_objectSearch_Tunnels_AllButton_posxpath).click()
        self.driver.find_element(By.XPATH, listPage_object_Tunnels_exportButton_posXPATH).click()
        self.driver.find_element(By.XPATH, listPage_object_urls_exportPopYes_posXpath).click()
        time.sleep(3)
        # #文件有多少行
        # self.file_name = get_txt_filenames(path=self.my_files._obj_files_dowload_path())
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.file_name)
        # self.file_path = self.my_files._obj_files_dowload_path() + "\\" + self.file_name
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.file_path)
        # with open(self.file_path, "rb") as file:
        #     self.lines = file.readlines()
        # self.num_lines = len(self.lines)-1
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.num_lines)
        # #实际有多少行
        # total_str = self.driver.find_element(By.XPATH,listPage_objectSearch_Tunnels_Total_posxpath).text
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], total_str)
        # total_result = total_str.split(":")[1].strip()
        # assert total_result == str(self.num_lines),  "判断在不选择All的情况下是否将全文Object导出"
        # os.remove(self.file_path)
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "文件删除成功")
        self. _calculate_export_all_objects_quantity()

    def _calculate_export_all_objects_quantity(self):
        self.file_name = get_txt_filenames(path=self.my_files._obj_files_dowload_path())
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.file_name)
        self.file_path = self.my_files._obj_files_dowload_path() + "\\" + self.file_name
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.file_path)
        with open(self.file_path, "rb") as file:
            self.lines = file.readlines()
        self.num_lines = len(self.lines) - 1
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.num_lines)
        # 实际有多少行
        total_str = self.driver.find_element(By.XPATH, listPage_objectSearch_Tunnels_Total_posxpath).text
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], total_str)
        total_result = total_str.split(":")[1].strip()
        assert total_result == str(self.num_lines), "判断在不选择All的情况下是否将全文Object导出"
        os.remove(self.file_path)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "文件删除成功")

    def _delete_quoted_object(self,data):
        self.create_tunnel(data)
        self.new_security_policy_tunnel(data)
        # 调用消除右上提示弹窗
        self._goto_subObjectPage()
        #first_quoted_tunnel_elem_posXpath = '(//*[@class="obj-charts-btn pro-port cursorPointer textCenter" and text() != 0])[1]/parent::div/parent::div/parent::td'
        self.driver.find_element(By.XPATH,listPage_object_Tunnels_select_First_object_posXpath).click()
        del_button_elem = listPage_object_Tunnels_delButton_posId
        del_button_elem_clickable = self.objects_po.is_element_clickable(del_button_elem,"ID")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "当前元素是否可点击".format(del_button_elem_clickable))
        assert del_button_elem_clickable == False,"删除按钮不可点击"
        self.objects_po._del_policy(data)
        self._delete(data)

    def _list_check(self):
        # 调用消除右上提示弹窗
        #self.objects_po.dismiss_right_top_tips(mainPage_rightTopTips_closeButton_posXpath)
        self._goto_subObjectPage()
        #选中All后，除create外其余置灰 ;翻页、创建操作后清除选中状态；列表所有数据前均增加复选框
        #一、All按钮选中所有复选框，所选数据存在无权操作数据时除Create按扭外其余按钮置灰
        #self.driver.find_element(By.ID,mainPage_secondLevelMenu_Tunnel_posId).click()
        self.unauthorized_operation()
        #二、切换页面（翻页、创建、导入等）后清除选中状态
        self.driver.find_element(By.ID,mainPage_secondLevelMenu_Tunnel_posId).click()
        self.clear_selection()
    def unauthorized_operation(self):
        self.driver.find_element(By.XPATH,listPage_objectSearch_Tunnels_AllButton_posxpath).click()
        # 1、导出按钮置灰
        try:
            self.driver.is_exist_element(Element=listPage_object_Tunnels_exportButton_posXPATH) # 导出按钮置灰
            assert self.driver.is_exist,"导出按钮置灰"
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "导出按钮置灰，测试 == Success")
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "导出按钮置灰，测试 == Fail")
        # 2、编辑按钮置灰
        try:
            self.driver.is_exist_element(Element=listPage_object_Tunnels_editButton_posXPATH) # 编辑按钮置灰
            assert self.driver.is_exist,"编辑按钮置灰"
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "编辑按钮置灰，测试 == Success")
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "编辑按钮置灰，测试 == Fail")
        # 3、删除按钮置灰
        try:
            self.driver.is_exist_element(Element=listPage_object_Tunnels_delButton_posXPATH) # 删除按钮置灰
            assert self.driver.is_exist,"删除按钮置灰"
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "删除按钮置灰，测试 == Success")
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "删除按钮置灰，测试 == Fail")

    def clear_selection(self):
        try:
            self.driver.find_element(By.XPATH,listPage_objectSearch_Tunnels_AllButton_posxpath).click() # 选择all
            time.sleep(5)
            self.driver.refresh()#刷新
            self.driver.is_exist_element(Element=mobileIdentitiesObjectPage_selete_Mobile_Identity_Button_posXpath)
            time.sleep(5)
            assert self.driver.is_exist,"刷新导致元素不勾选"
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "刷新后元素不勾选，测试 == Success")
            time.sleep(5)
            self.driver.find_element(By.XPATH, listPage_objectSearch_Tunnels_AllButton_posxpath).click()  # 选择all
            self.driver.find_element(By.XPATH,'//*[@id="pagination-_pagination_Objects_tunnel_Home_App_anonymousComponent"]/div[1]/button[2]').click() # 第二页
            self.driver.is_exist_element(Element=mobileIdentitiesObjectPage_selete_Mobile_Identity_Button_posXpath)
            time.sleep(5)
            assert self.driver.is_exist,"翻页导致元素不勾选"
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "翻页后元素不勾选，测试 == Success")
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "翻页后元素不勾选，测试 == Fail")
    def _search(self, data):
        self._goto_subObjectPage()
        if data["Search_type"] == "ID":
            self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_selectLabel_posId).send_keys(self.table_dict['ID'])
            self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_select_Id_posId).click()
        elif data["Search_type"] == "Name":
            self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_selectLabel_posId).send_keys(self.table_dict['Name'])
            self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_select_Name_posId).click()
        elif data["Search_type"] == "IP":
            self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_selectLabel_posId).send_keys(self.table_dict['Endpoint A'])
            self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_select_IP_posId).click()
        else:  # 全局查询
            self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_selectLabel_posId).send_keys(self.table_dict['Name'])
            self.driver.find_element(By.XPATH, listPage_objectSearch_Tunnels_select_all_xpath).click()
        self.driver.find_element(By.ID, listPage_objectSearch_Tunnels_buttonSearch_posId).click()

    def _create(self, data):
        # 调用消除右上提示弹窗
        #self.objects_po.dismiss_right_top_tips(mainPage_rightTopTips_closeButton_posXpath)
        # 跳转到Tunnel列表页
        self._goto_subObjectPage()
        # 创建Tunnel
        self.random_name = self.my_random.random_name()
        self.random_number = self.my_random.random_number()
        self.over_limit_name = "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttes"
        #Create Tunnel Object
        self.driver.find_element(By.ID, listPage_object_Tunnels_createButton_posId).click()#点击Create
        self.driver.find_element(By.XPATH, object_page_ln_select_brief_statistics).click()  # 选择statistics
        #name最大长度限制
        self.driver.find_element(By.XPATH, Tunnel_ObjectPage_InputName_posXpath).send_keys(self.over_limit_name)#输入超长名字
        assert "32/32" == self.driver.find_element(By.XPATH, Tunnel_ObjectPage_NameLength_posXpath).text #校验是否超过32个自动过滤
        self.objects_po.clear_Name(path=Tunnel_ObjectPage_InputName_posXpath)#清除name
        ###################################################旧版本……需要注释
        #重新输入name
        # self.driver.find_element(By.XPATH, Tunnel_ObjectPage_InputName_posXpath).send_keys(self.random_name)#输入名字
        # self.driver.find_element(By.XPATH, Tunnel_ObjectPage_inputItem_posXpath).send_keys(self.random_item)#输入item内容
        # self.driver.find_element(By.ID,Tunnel_ObjectPage_ChangeColor_posid).click()#Color select buuton
        # self.driver.find_element(By.ID,Tunnel_ObjectPage_YellowColor_posid).click()#switch yellow color
        # self.driver.find_element(By.XPATH, TunnelsObjectPage_textArea_Description_posXpath).send_keys(self.random_name)  # 添加描述
        # self.driver.find_element(By.XPATH, Tunnel_AddEndpoint_posXpath).click()  # 添加item按钮
        # self.driver.find_element(By.XPATH, Tunnel_ObjectPage_inputItem2_posXpath).send_keys(self.random_item)  # 输入item内容2
        # self.driver.find_element(By.XPATH, TunnelsObjectPage_textArea_Description2_posXpath).send_keys(self.random_name)  # 添加描述2
        ###################################################旧版本……需要注释
        #1.输入Name
        self.driver.find_element(By.XPATH, Tunnel_ObjectPage_InputName_posXpath).send_keys(self.random_name)
        #2.选择Type
        if data["type"] == "IP":
            self.driver.find_element(By.ID, Tunnel_Edit_Page_Type).click()
            self.driver.find_element(By.XPATH, Tunnel_Type_IP)
        elif data["type"] == "GRE":
            self.driver.find_element(By.ID,Tunnel_Edit_Page_Type).click()
            self.driver.find_element(By.XPATH,Tunnel_Type_GRE)
        else:
            pass
        #3.添加endpoint
        self.driver.find_element(By.XPATH, Tunnel_add_item_button).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_first).click()
        self.driver.find_element(By.XPATH, tunnel_add_endpoint_b).click()
        self.driver.find_element(By.XPATH, tunnel_add_item_2).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, tunnel_ip_list_fourth).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_close).click()
        #4.添加Description
        self.driver.find_element(By.XPATH,tunnel_page_description).send_keys(self.random_name)

        #确认保存
        self.driver.find_element(By.ID, TunnelsObjectPage_button_SaveYes_posId).click()
        self.driver.find_element(By.CSS_SELECTOR, TunnelsObjectPage_button_warningSaveYes_posSelector).click()
        #数据提取
        time.sleep(3)
        #通过Name查询，查看内容是否和新建时一致
        self.extract_ele_tunnel()## 提取ID、Name、Description、Detail
        self.search_by_name={"Search_type": "Name"}
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.search_by_name)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], data)
        self._search(self.search_by_name)
        now_name = self.driver.find_element(By.XPATH, '//table/tbody/tr[1]/td[3]/div//span').text
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "self.random_name[:32]:", self.random_name[:32])
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "now_name:", now_name)
        assert self.random_name[:32] == now_name, "Comparison equal"

    def create_tunnel(self,data):
        #使用create_tunnel时需要data传递Name
        # 调用消除右上提示弹窗
        # self.objects_po.dismiss_right_top_tips(mainPage_rightTopTips_closeButton_posXpath)
        # 跳转到Tunnel列表页
        self._goto_subObjectPage()
        # 创建Tunnel
        self.random_name = self.my_random.random_name()
        self.driver.find_element(By.ID, listPage_object_Tunnels_createButton_posId).click()  # 点击Create

        # 1.输入Name
        self.driver.find_element(By.XPATH, Tunnel_ObjectPage_InputName_posXpath).send_keys(self.random_name)
        # 2.选择Type
        if data["type"] == "IP":
            self.driver.find_element(By.ID, Tunnel_Edit_Page_Type).click()
            self.driver.find_element(By.XPATH, Tunnel_Type_IP)
        elif data["type"] == "GRE":
            self.driver.find_element(By.ID, Tunnel_Edit_Page_Type).click()
            self.driver.find_element(By.XPATH, Tunnel_Type_GRE)
        else:
            pass
        # 3.添加endpoint
        self.driver.find_element(By.XPATH, Tunnel_add_item_button).click()

        ##endpoint A中新建ip object
        self.driver.find_element(By.XPATH, tunnel_ip_list_add_button).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_select_ip).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_add).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_input).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_input).send_keys("2.2.2.3")
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_save).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_name).send_keys("2.2.2.3")
        self.driver.find_element(By.XPATH, tunnel_slide_ip_ok).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_confirm_ok).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_close).click()

        ##endpoint B中新建ip object group
        self.driver.find_element(By.XPATH, tunnel_add_endpoint_b).click()
        self.driver.find_element(By.XPATH, tunnel_add_item_2).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_add_button).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_select_ip_group).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_name).send_keys("new_group_test")
        self.driver.find_element(By.XPATH, tunnel_ip_group_add_subobject).click()
        self.driver.find_element(By.XPATH, tunnel_ip_group_first_row).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_ok).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_confirm_ok).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_close).click()

        # 确认保存
        self.driver.find_element(By.ID, TunnelsObjectPage_button_SaveYes_posId).click()
        self.driver.find_element(By.CSS_SELECTOR, TunnelsObjectPage_button_warningSaveYes_posSelector).click()

        self.extract_ele_tunnel()  ## 提取ID、Name、Description、Detail


    def delete_created_ip_bymself(self,data):
        #self.driver.find_element(By.ID, mainPage_firstLevelMenu_Objects_posId).click()
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_ipAddress_posId).click()
        # 1.刪除ip object group
        if "isDeleteGroup" in data and data["isDeleteGroup"] == "True":
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys("new_group_test")
            self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Name_posXpath).click()
            self.driver.find_element(By.ID, mainPage_ObjectSearch_buttonSearch_posId).click()
            # 尝试定位第一个对象，如果找到则执行删除操作
            try:
                first_object = self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath)
                if first_object:
                    first_object.click()  # 选择第一个对象
                    self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
                    self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()
            except NoSuchElementException:
                # 如果没有找到元素，打印消息并跳过删除操作
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "未找到第一个对象，跳过删除操作")
        else:
            pass

        #2.刪除ip object
        self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys("2.2.2.3")
        self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Name_posXpath).click()
        self.driver.find_element(By.ID, mainPage_ObjectSearch_buttonSearch_posId).click()

        self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
        self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
        self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()



    def item_search_verify(self, data):
        self._goto_subObjectPage()
        # 创建Tunnel
        self.random_name = self.my_random.random_name()
        self.driver.find_element(By.ID, listPage_object_Tunnels_createButton_posId).click()  # 点击Create

        # 1.输入Name
        self.driver.find_element(By.XPATH, Tunnel_ObjectPage_InputName_posXpath).send_keys(self.random_name)
        # 3.添加endpoint
        self.driver.find_element(By.XPATH, Tunnel_add_item_button).click()

        ##新建ip object
        self.driver.find_element(By.XPATH, tunnel_ip_list_add_button).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_select_ip).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_add).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_input).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_input).send_keys("2.2.2.3")
        self.driver.find_element(By.XPATH, tunnel_slide_ip_item_save).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_name).send_keys("2.2.2.3")
        self.driver.find_element(By.XPATH, tunnel_slide_ip_ok).click()
        self.driver.find_element(By.XPATH, tunnel_slide_ip_confirm_ok).click()
        self.driver.find_element(By.XPATH, tunnel_ip_list_close).click()

        # 校验item_search的功能
        self.driver.find_element(By.XPATH, tunnel_item_search_frame).send_keys("2.2.2.3" + Keys.ENTER)
        find_content1 = self.driver.find_element(By.XPATH, tunnel_first_row_item).text
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], find_content1)
        assert find_content1 == '2.2.2.3', f"Expected '2.2.2.3', but got '{find_content1}'"

        self.objects_po.clear_Name(path=tunnel_item_search_frame)  # 清除name
        self.driver.find_element(By.XPATH, tunnel_item_search_frame).send_keys("1.1" + Keys.ENTER)

        try:
            find_content2 = self.driver.find_element(By.XPATH, tunnel_first_row_item).text
        except NoSuchElementException:
            find_content2 = "null"
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "what0"+find_content2)
        assert find_content2 == '', f"Expected '', but got '{find_content2}'"

        self.driver.find_element(By.XPATH,'//*[@id="Cancel-_tunnelAdd_Home_App_anonymousComponent"]/span').click()#Cancel
        self.driver.find_element(By.XPATH,'//*[@class="el-button el-button--default el-button--small el-button--primary operation-confirm-Leave"]').click()



    def _modify(self, data):
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_Tunnel_posId).click()
        data["Search_type"]="ID"
        self._search(data)
        self.random_name = self.my_random.random_name()  # 重新生成一个random_name
        self.random_item = self.my_random.random_tunnel() #重新生成的endpoint
        #查询后EditName
        self.driver.find_element(By.XPATH,listPage_object_Tunnels_select_First_object_posXpath).click()#第一行数据前的复选框
        self.driver.find_element(By.ID,listPage_object_Tunnels_editButton_posId ).click()#edit按钮
        self.objects_po.clear_Name(path=Tunnel_ObjectPage_InputName_posXpath)#清除name
        self.driver.find_element(By.XPATH,Tunnel_ObjectPage_InputName_posXpath).send_keys(self.random_name)#重新输入name
        self.driver.find_element(By.ID,TunnelsObjectPage_button_SaveYes_posId).click()
        self.driver.find_element(By.CSS_SELECTOR, TunnelsObjectPage_button_warningSaveYes_posSelector).click()
        #断言修改name是否生效
        #断言修改后的数据是否保持一致
        time.sleep(3)
        self.assert_ele_tunnel()
        assert  self.random_name[:32] == self.edit_table_dict['Name'],"校验修改Name是否生效"

    def _delete(self,data):
        self._goto_subObjectPage()
        self._search(data)
        self.driver.find_element(By.XPATH,listPage_object_Tunnels_select_First_object_posXpath).click()#选择第一个对象
        #确认删除
        self.driver.find_element(By.ID,listPage_object_Tunnels_delButton_posId).click()
        self.driver.find_element(By.XPATH,listPage_object_Tunnels_del_yes_Button_posXpath).click()

        time.sleep(3)

    def extract_ele_tunnel(self):
        self.driver.is_exist_element(
            Element='((//div[@class!="itemDetails cursor"]//table[@class="el-table__body"])[1]//tr)[1]')  # 查看第一行是否存在数据
        if self.driver.is_exist:
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
        # ID
        self.key11 = self.driver.find_element(By.XPATH, list_first_row_first_column_posXpath).text
        self.value12 = self.driver.find_element(By.XPATH, list_second_row_first_column_posXpath).text
        # Vsy_ID
        self.key12 = self.driver.find_element(By.XPATH, list_first_row_second_column_posXpath).text
        self.value22 = self.driver.find_element(By.XPATH, list_second_row_second_column_posXpath).text
        # Name
        self.key13 = self.driver.find_element(By.XPATH, list_first_row_third_column_posXpath).text
        self.value23 = self.driver.find_element(By.XPATH, '//table/tbody/tr[1]/td[3]/div//span').text
        #Endpoint A:单个ip
        self.key14= self.driver.find_element(By.XPATH, list_first_row_fifth_column_posXpath).text
        self.value24 = self.driver.find_element(By.XPATH,
                                                '(//*[@id="multilineItemDetails-_MultilineTableCell_ElTableBody_ElTable_Objects_tunnel_Home_App_anonymousComponent"]/div/span/div/div/div)[2]').text
        #字典
        self.table_dict = {self.key11: self.value12, self.key12: self.value22, self.key13: self.value23,self.key14:self.value24}
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.table_dict)

        # 修改tunnel后元素===》断言

    def assert_ele_tunnel(self):
        # ID
        self.key11 = self.driver.find_element(By.XPATH, list_first_row_first_column_posXpath).text
        self.value12 = self.driver.find_element(By.XPATH, list_second_row_first_column_posXpath).text
        # Vsy_ID
        self.key12 = self.driver.find_element(By.XPATH, list_first_row_second_column_posXpath).text
        self.value22 = self.driver.find_element(By.XPATH, list_second_row_second_column_posXpath).text
        # Name
        self.key13 = self.driver.find_element(By.XPATH, list_first_row_third_column_posXpath).text
        self.value23 = self.driver.find_element(By.XPATH, '//table/tbody/tr[1]/td[3]/div//span').text
        # 字典
        self.edit_table_dict = {self.key11: self.value12, self.key12: self.value22, self.key13: self.value23}
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.edit_table_dict)

    def new_security_policy_tunnel(self, data):
        # 跳转到安全策略创建页面
        self.driver.find_element(By.ID, mainPage_firstLevelMenu_Policy_posId).click()
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_Security_posId).click()
        # 添加tunnel
        self.driver.find_element(By.XPATH, security_create_Button_posXpath).click()
        self.driver.find_element(By.XPATH, security_create_Name_input_frame_PosXpath).send_keys(data["Name"])

        self.driver.find_element(By.XPATH, security_policy_add_condition_button_by_xpath).click() #选择Condition按钮
        self.driver.find_element(By.XPATH, security_create_add_tunnel_button_click_PosXpath).click() #选择tunnel
        time.sleep(2)
        self.driver.find_element(By.XPATH,security_add_tunnel_button).click() #添加tunnel
        # self.driver.find_element(By.XPATH, security_search_tunnel_frame_click_PosXpath).send_keys(
        #     self.random_name + Keys.ENTER)
        # 如tunnel存在则创建
        time.sleep(3)
        self.driver.is_exist_element(Element=security_first_tunnel_inlist_click_PosXpath) #直接选择第一个最新的，不用搜索
        if self.driver.is_exist:  # 如果存在，就进行创建
            assert self.driver.is_exist == True
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], '正常找到Object，正常进行引用创建')

            self.driver.find_element(By.XPATH, security_first_tunnel_inlist_click_PosXpath).click()
            self.driver.find_element(By.XPATH, security_create_ok_click_posXpath).click()
            self.driver.find_element(By.XPATH, security_create_Warn_ok_click_posXpath).click()
        else:  # 不存在就跳过
            assert self.driver.is_exist == False  # 未找到元素
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], '未找到Object，无法进行引用创建')
            pass

    def _vsys_case(self,data):
        # for step,operation in self.vsys_operate.items():
        # #items()返回包含字典所有键值对的元组列表
        #     self.step =step #将key赋值给step
        #
        #     # split()函数返回列表，value赋值给operation
        #     self.setp_operation = operation.split(">")
        #     self.vsys = self.setp_operation[0]
        #     self.operation = self.setp_operation[1]
        #
        #     self.objects_po.Switch_vsys(vsys_id=self.vsys)
        #     self.tunnel_vsys_operate(operate=self.operation,data=data)
        #
        # self.clear_create_(data)
        if "vsys_operate" in data.keys():
            self.vsys_opearte = data["vsys_operate"]   #{"step1": "Tvsys1->create", "step2": "Tvsys3->search"}
            self.vsys2="null"
            for i in range(1,len(self.vsys_opearte.keys())+1):
                self.step = "step" + str(i)  #step1
                self.step_operation = self.vsys_opearte[self.step].split("->")   #[Tvsys1,create]
                if i==1:
                    self.vsys1 = self.step_operation[0]    #Tvsys1
                    self.operation1 = self.step_operation[1]   #create
                    self.objects_po.Switch_vsys(vsys_id=self.vsys1)
                elif i==2:
                    self.vsys2 = self.step_operation[0]  #Tvsys3
                    self.operation2 = self.step_operation[1]  #search
                    if self.vsys1 == self.vsys2:
                        if self.operation2 == "security_quote":
                            data["delete_mode"] = "security"
                        # elif self.operation2 == "intercept_quote":
                        #     data["delete_mode"] = "intercept"
                    else:
                        self.objects_po.Switch_vsys(vsys_id=self.vsys2)
                    self.objects_po.compare_vsys(vsys1=self.vsys1,vsys2=self.vsys2)  # self._query = 0
                self.tunnel_vsys_operate(operate=self.step_operation[1],data=data)   #Tvsys1 create
        self._clear_tunnel_vsys_create(data)

    def tunnel_vsys_operate(self,operate,data):
        if operate == "create":
            self._create(data)
        elif operate == "search":
            self._search(data)
        elif operate == "security_quote":
            self.new_security_policy_tunnel(data)
        else:
            pass

    def _clear_tunnel_vsys_create(self,data):
        if self.operation1 == "create":
            if self.operation2 == "security_quote" and data["delete_mode"] == "security":
                self.objects_po.Switch_vsys(vsys_id=self.vsys2)
                self.objects_po._del_policy(data)
                self._delete(data)
            # elif self.operation2 == "intercept_quote" and data["delete_mode"] == "intercept":
            #     self.objects_po.Switch_vsys(vsys_id=self.vsys2)
            #     self.objects_po._del_policy(data)
            #     self._delete(data)
            else:
                self.objects_po.Switch_vsys(vsys_id=self.vsys1)
                self._delete(data)
                pass

    def test_ClearCounter(self,data):
        """
                测试点：
                    # 列表页
                        ##单选Object
                        ##多选Object
                        ##多选Object 和Object Group
                        ##单选非本Vsys Object
                    # 详情页
                        ##Object详情页
                        ##Object Group详情页
                        ##非本Vsys的Object详情页
                :return:
                """
        # 于data中获取数据
        page_flag, selected_object_type, selected_objects_number, detail_type, selected_data_number = data["page_flag"], \
            data["selected_object_type"], data["selected_objects"], data["detail_type"], data["selected_data"]
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], page_flag, selected_object_type, selected_objects_number, detail_type)
        obj_data = {"Model": "create",
                    "Type": 1,
                    "Name": "test_ui 4 Clear Counter",
                    "Items": [],
                    "Description": "",
                    "Subordinate Objects": {
                        "subName": "",
                        "subItems": [
                            "[random]->"
                        ],
                        "subDescription": ""
                    }, }
        # 判断当前页是否有符合条件的测试数据
        create_data_flag = 0
        try:
            self._just_goto_tunnelPage()  # 页面跳转
            self.driver.implicitly_wait(5)
            #is_firstObjectGroup_exist = self.driver.is_exist_element_by_value(By.XPATH,acc_listPage_object_tableCheckbox_firstObjectGroup_posXpath)
            is_firstSingleObject_exist = self.driver.is_exist_element_by_value(By.XPATH,acc_listPage_object_tableCheckbox_firstSingleObject_posXpath)
            #if is_firstObjectGroup_exist == False or is_firstSingleObject_exist == False:
            if is_firstSingleObject_exist == False:
                # 创建测试数据
                self._create(data)
                create_data_flag = 1
            else:
                # firstSingleObject = self.driver.find_element(By.XPATH,acc_listPage_object_tableCheckbox_firstSingleObject_posXpath)
                # #firstObjectGroup = self.driver.find_element(By.XPATH, acc_listPage_object_tableCheckbox_firstObjectGroup_posXpath)
                # #firstNotLocalVsysObjectOrGroup = self.driver.find_element(By.XPATH,acc_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath)
                #
                # if firstSingleObject == firstNotLocalVsysObjectOrGroup or firstObjectGroup == firstNotLocalVsysObjectOrGroup:
                #     # 创建测试数据
                #     self._create(data)
                #     create_data_flag = 1
                # else:
                #     pass
                pass

        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], e)
        if page_flag == 0:  # 列表页
            self._pure_operate_checkbox(selected_object_type, selected_objects_number)  # 列表页选择操作
            self._verify_clear_counter(page_flag, selected_object_type, selected_objects_number, selected_data_number,
                                       detail_type)
        else:  # 详情页
            # 判断进入何种类型的Object的详情页
            self._judge_whitch_page(detail_type)
            self._verify_clear_counter(page_flag, selected_object_type, selected_objects_number, selected_data_number,
                                       detail_type)
        # 页面跳转
        self.driver.refresh()
        self._just_goto_tunnelPage()
        # 清除测试数据
        if create_data_flag == 1:  # 已新建数据
            self._del(obj_data, search_value="test_ui", del_flag=1)
        elif self.create_other_vsys_data_flag == 1:  # 已创建其他Vsys数据
            # 切换Vsys至Vsys3
            vsys_name = self.loginout_parse.get("vsys3", "vsys_name")  # 登录后vsys切换为UIAutoTestVsys
            profile_pub = ProfilesPublicOperations(self.driver)
            profile_pub.change_vsys(vsys_name=vsys_name)
            # # 页面跳转
            # self._just_goto_accountsPage()
            # 清除测试数据
            self._del(obj_data, search_value="test_ui", del_flag=1)

    def _just_goto_tunnelPage(self):
        self.driver.find_element(By.ID, mainPage_firstLevelMenu_Objects_posId).click()
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_Tunnel_posId).click()

    def _judge_whitch_page(self, detail_type):
        """
         #判断进入何种类型的Object的详情页
        :param detail_type:
        :return:
        """
        self.create_other_vsys_data_flag = 0
        if detail_type == 0:  # Object详情页
            # 选中第一个Object并进入其详情页
            self.driver.find_element(By.XPATH, acc_listPage_object_tableCheckbox_firstSingleObject_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_Tunnels_editButton_posId).click()  # 点击edit按钮
        elif detail_type == 1:  # Object Group详情页
            # 选中第一个Object Group并进入其详情页
            self.driver.find_element(By.XPATH, acc_listPage_object_tableCheckbox_firstObjectGroup_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_Tunnels_editButton_posId).click()  # 点击edit按钮

        else:  # etail_type=2--非本Vsys的Object详情页
            # 判断当前页有无非本Vsys的对象
            is_firstNotLocalVsys_exist = self.driver.is_exist_element_by_value(By.XPATH,
                                                                     acc_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath)
            try:
                if is_firstNotLocalVsys_exist == True:
                    pass
                else:
                    # 创建测试数据
                    obj_data = {"Model": "create",
                                "Type": 1,
                                "Name": "test_ui 4 Clear Counter",
                                "Items": [],
                                "Description": "",
                                "Subordinate Objects": {
                                    "subName": "",
                                    "subItems": [
                                        "[random]->"
                                    ],
                                    "subDescription": ""
                                }, }
                    # 切换Vsys至Vsys3
                    vsys_name = self.loginout_parse.get("vsys3", "vsys_name")  #
                    # profile_pub = ProfilesPublicOperations(driver)
                    self.profile_pub.change_vsys(vsys_name=vsys_name)
                    self._create(data=obj_data)
                    ui_vsys_name = self.loginout_parse.get("vsys", "vsys_name")  # 切换为UIAutoTestVsys
                    self.profile_pub.change_vsys(vsys_name=ui_vsys_name)
                    self.create_other_vsys_data_flag = 1
            except Exception as e:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], e)
            # 选中第一个非本Vsys的Object Group或Object并进入其详情页
            self.driver.find_element(By.XPATH,
                                     acc_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_Tunnels_editButton_posId).click()  # 点击edit按钮

    def _pure_operate_checkbox(self, selected_object_type, selected_objects_number):
        """

        :param selected_object_type: 上层传入，
            selected items Type=0选中对象，
            selected items Type=1则选中对象组,
            selected items Type=2则选中对象和对象组，
            selected items Type=3则任意非本Vsys的对象",
        :return:
        """
        self.verify_selected_objects_number0 = 0
        self.create_other_vsys_data_flag = 0
        if selected_object_type == 0:  # 选中对象
            object_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                              acc_listPage_object_tableCheckbox_singleObject_posXpaths)  # 定位所有single object对应的CheckBox
            object_not_local_vsys_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                                             acc_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths)  # 列表页中不是本Vsys的对象或对象组的CheckBox
            # 处理object_checkbox_elems，将不是本Vsys的checkbox元素剔除
            local_vsys_object_checkbox_elems = self._operate_webelmet_group(object_checkbox_elems,
                                                                            object_not_local_vsys_checkbox_elems)
            if selected_objects_number == 0:  # 选中个数为0
                self.verify_selected_objects_number0 = 1
            else:  # 选中头selected_objects 个对象
                if selected_objects_number == -1:  # 选中个数为随机
                    if len(local_vsys_object_checkbox_elems) == 1:
                        self.random_selected_objects_number = 1
                    # elif len(local_vsys_object_checkbox_elems) == 0:
                    #     selected_objects_number = 1
                    else:
                        self.random_selected_objects_number = random.randint(1, len(local_vsys_object_checkbox_elems))
                    selected_objects_number = self.random_selected_objects_number
                else:  # 采用用例中的数值
                    selected_objects_number = selected_objects_number
                for i in local_vsys_object_checkbox_elems:
                    if selected_objects_number < 1:
                        break
                    else:
                        i.click()
                        selected_objects_number -= 1

        elif selected_object_type == 1:  # 1则选中对象组
            # 定位对象组
            object_group_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                                    acc_listPage_object_tableCheckbox_objectGroup_posXpaths)
            object_not_local_vsys_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                                             acc_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths)  # 列表页中不是本Vsys的对象或对象组的CheckBox
            # 处理object_checkbox_elems，将不是本Vsys的checkbox元素剔除
            local_vsys_object_group_checkbox_elems = self._operate_webelmet_group(object_group_checkbox_elems,
                                                                                  object_not_local_vsys_checkbox_elems)
            if selected_objects_number == 0:  # 选中个数为0
                self.verify_selected_objects_number0 = 1
                # pass
            else:  # 选中头selected_objects 个对象
                if selected_objects_number == -1:  # 选中个数为随机
                    self.random_selected_objects_number = random.randint(1, len(local_vsys_object_group_checkbox_elems))
                    selected_objects_number = self.random_selected_objects_number
                else:  # 选中个数为确切值
                    if selected_objects_number > len(local_vsys_object_group_checkbox_elems):  # 用例中参数大于实际页面展示的数目
                        selected_objects_number = len(local_vsys_object_group_checkbox_elems)
                    else:  # 采用用例中的数值
                        selected_objects_number = selected_objects_number
                for i in local_vsys_object_group_checkbox_elems:
                    if selected_objects_number < 1:
                        break
                    else:
                        i.click()
                        selected_objects_number -= 1

        elif selected_object_type == 2:  # 2则选中对象和对象组
            # 定位所有single object对应的CheckBox
            object_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                              acc_listPage_object_tableCheckbox_singleObject_posXpaths)
            # 定位对象组
            object_group_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                                    acc_listPage_object_tableCheckbox_objectGroup_posXpaths)
            object_not_local_vsys_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                                             acc_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths)  # 列表页中不是本Vsys的对象或对象组的CheckBox
            # 处理object_checkbox_elems，将不是本Vsys的checkbox元素剔除
            local_vsys_object_checkbox_elems = self._operate_webelmet_group(object_checkbox_elems,
                                                                            object_not_local_vsys_checkbox_elems)
            local_vsys_object_group_checkbox_elems = self._operate_webelmet_group(object_group_checkbox_elems,
                                                                                  object_not_local_vsys_checkbox_elems)

            if selected_objects_number == 0:  # 选中个数为0
                # pass
                self.verify_selected_objects_number0 = 1

            else:  # 选中头selected_objects 个对象
                if selected_objects_number == -1:  # 选中个数为随机
                    self.random_selected_objects_number = random.randint(1,
                                                                         len(local_vsys_object_group_checkbox_elems) + len(
                                                                             local_vsys_object_checkbox_elems))
                    selected_objects_number = self.random_selected_objects_number
                else:  # 选中个数为确切值
                    if selected_objects_number > len(local_vsys_object_group_checkbox_elems) + len(
                            local_vsys_object_checkbox_elems):  # 用例中参数大于实际页面展示的数目
                        selected_objects_number = len(local_vsys_object_group_checkbox_elems) + len(
                            local_vsys_object_checkbox_elems)
                    else:  # 采用用例中的数值
                        selected_objects_number = selected_objects_number
                for i in local_vsys_object_group_checkbox_elems:
                    if selected_objects_number == 1:  # 剩余一个，用于勾选单独对象
                        break
                    else:
                        i.click()
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "i.click()")
                        selected_objects_number -= 1
                for j in local_vsys_object_checkbox_elems:
                    if selected_objects_number < 1:
                        break
                    else:
                        j.click()
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "j.click()")
                        selected_objects_number -= 1

        else:  # 3则任意非本Vsys的对象
            object_not_local_vsys_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                                             acc_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths)  # 列表页中不是本Vsys的对象或对象组的CheckBox
            if len(object_not_local_vsys_checkbox_elems) == 0:
                # 无则新建测试数据
                # 创建测试数据
                obj_data = {"Model": "create",
                            "Type": 1,
                            "Name": "test_ui 4 Clear Counter",
                            "Items": [],
                            "Description": "",
                            "Subordinate Objects": {
                                "subName": "",
                                "subItems": [
                                    "[random]->"
                                ],
                                "subDescription": ""
                            }, }
                # 切换Vsys
                # 切换Vsys至Vsys3
                vsys_name = self.loginout_parse.get("vsys3", "vsys_name")  # 登录后vsys切换为UIAutoTestVsys
                profile_pub = ProfilesPublicOperations(a)
                profile_pub.change_vsys(vsys_name=vsys_name)
                self._create(data=obj_data)
                self.create_other_vsys_data_flag = 1
            if selected_objects_number == 0:  # 选中个数为0
                # pass
                self.verify_selected_objects_number0 = 1
            else:  # 选中头selected_objects 个对象
                if selected_objects_number == -1:  # 选中个数为随机
                    self.random_selected_objects_number = random.randint(1, len(object_not_local_vsys_checkbox_elems))
                    selected_objects_number = self.random_selected_objects_number
                else:  # 采用用例中的数值
                    selected_objects_number = selected_objects_number
                for i in object_not_local_vsys_checkbox_elems:
                    if selected_objects_number < 1:
                        break
                    else:
                        i.click()
                        selected_objects_number -= 1



    def _verify_clear_counter(self, page_flag, selected_object_type, selected_objects_number, selected_data_number,
                              detail_type):
        """
        page_flag =0时默认已勾选元素，page_flag =1默认已进入Object 详情页
        :param page_flag:
        :return:
        """

        if page_flag == 0:  # 列表页操作与验证
            if selected_object_type != 3:  # 不是选择非本Vsys的数据
                # 点击Clear Counter按钮
                self.driver.find_element(By.XPATH, listPage_object_pages_clearCounter_button_poxXpath).click()
                if self.verify_selected_objects_number0 == 1:  # 未选择任何数据
                    error_message_elem_isExist = self.driver.is_exist_element_by_value(By.XPATH,
                                                                             '//div[@role="alert" and contains(@class,"el-message el-message--error")]')
                    assert error_message_elem_isExist == True, "校验失败！无错误提示"
                else:
                    # 处理二次确认弹窗
                    clickable_flag = self._select_objects_secondSelect(selected_objects_number, selected_data_number)
                    if clickable_flag == 1:  # 确认弹窗中的确认按钮可点击
                        try:
                            is_disabled = self.driver.find_element(By.XPATH,
                                                                   acc_listPage_object_clearCounterPopYes_posXpath).get_attribute(
                                "disabled")
                        except:
                            is_disabled = None
                            pass
                        assert is_disabled == None, "校验失败！此时按钮不可点击"
                    else:  # 确认弹窗中的确认按钮不可点击
                        try:
                            is_disabled = self.driver.find_element(By.XPATH,
                                                                   acc_listPage_object_clearCounterPopYes_posXpath).get_attribute(
                                "disabled")
                        except:
                            is_disabled = None
                            pass
                        assert is_disabled == 'disabled', "校验失败！此时按钮可点击"

            else:  # 校验非本Vsys的数据
                # is_clear_counter_clickable = self.objects_po.is_element_clickable(
                #     listPage_object_pages_clearCounter_button_poxXpath, "XPATH")
                is_clear_counter_clickable = self.driver.find_element(By.XPATH,
                                                                      listPage_object_pages_clearCounter_button_poxXpath).get_attribute(
                    "class")
                assert "notAllowed" in is_clear_counter_clickable, "is_clear_counter_clickable ={}".format(
                    is_clear_counter_clickable)
        else:  # page_flag =1:  #详情页操作与验证
            # Clear Counter按钮
            is_clear_counter_clickable = self.driver.find_element(By.XPATH,
                                                                  acc_ObjectDetailPage_clearCounter_posXpath).get_attribute(
                "class")
            if detail_type != 2:  # 不是非本Vsys的详情页
                assert "not-allowed" not in is_clear_counter_clickable, "is_clear_counter_clickable = {}".format(
                    is_clear_counter_clickable)
            else:  # 非本Vsys的详情页
                assert "not-allowed" in is_clear_counter_clickable, "is_clear_counter_clickable = {}".format(
                    is_clear_counter_clickable)



    def _select_objects_secondSelect(self, selected_objects_number, selected_data_number):
        """
        处理列表页选择的二次确认弹窗
        :param selected_data_number: 二次弹窗中要选择的数目
        :param selected_object_type: 选择的类型
        :return:
        """

        # 处理二次确认弹窗
        self.driver.find_element(By.XPATH,
                                 acc_listPage_object_exportPopSelectAll_posXpath).click()  # 点击全选按钮，取消默认全选
        data_checkbox_elems = self.driver.find_elements(By.XPATH,
                                                        acc_listPage_object_exportPopCheckbox_posXpaths)  # 导出弹窗数据CheckBox
        if selected_data_number != 0:
            if selected_data_number > 0:
                selected_data_number = selected_data_number
            elif selected_data_number == -1:  # 随机数值
                selected_data_number = random.randint(1, self.random_selected_objects_number)
            clickable_flag = 1
            for i in data_checkbox_elems:
                if selected_data_number < 1:
                    break
                else:
                    i.click()
                    selected_data_number -= 1
        else:  # selected_data_number = 0确认弹窗中不选择数据
            clickable_flag = 0
        return clickable_flag


    def _operate_webelmet_group(self, group1, group2):
        """
        处理WebElemet Group(将1中的2元素排除掉)
        :param group1:
        :param group2:
        :return:
        """
        # 将group 转换为set 便于排除处理
        set_group1 = set(group1)
        set_group2 = set(group2)
        # 使用集合差集来排除 elements_group2 中的元素
        filtered_set = set_group1 - set_group2
        # 将结果转换回列表
        filtered_elements = list(filtered_set)
        return filtered_elements

    def _View_statistics_case(self, data):
        self._create(data)
        self._search(data)
        self.objects_po.View_statistics(edit_element=listPage_object_Tunnels_editButton_posId)
        self._delete(data)



if __name__ == '__main__':
    my_files = ReadData()
    options =webdriver.ChromeOptions()
    prefs = {'download.default_directory':my_files._obj_files_dowload_path()}
    options.add_experimental_option('prefs', prefs)
    a = download_files()
    r = Tunnel(a)
    profile_pub = ProfilesPublicOperations(a)
    profile_pub.change_vsys(vsys_name="UIAutoTestVsys")
    data ={
                "ids": "非本Vsys的Object详情页",
                "page_flag": 1,
                "selected_object_type": 0,
                "selected_objects": -1,
                "selected_data": -1,
                "detail_type": 2
    }
    r.test_ClearCounter(data)
    a.quit()

