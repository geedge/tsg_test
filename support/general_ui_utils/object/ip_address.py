import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.general_ui_utils.random_name import RandomName
from support.general_ui_utils.element_position.objects_element_position import *
from support.general_ui_utils.read_data import ReadData
from selenium.webdriver.remote.webelement import WebElement
from support.general_ui_utils.object.objects_public_operations import ObjectsPublicOperations
from support.general_ui_utils.profile.profiles_public_operations import ProfilesPublicOperations
from support.general_ui_utils.object.objects_public_operations import ObjectsPublicOperations, get_txt_filenames, download_files
import random

class IpAddress:
    def __init__(self, driver):
        self.my_random = RandomName()
        self.driver = driver
        # 调用profiles公共方法操作、删除、查询，
        self.objects_po = ObjectsPublicOperations(self.driver)
        self.profile_pub = ProfilesPublicOperations(self.driver)

    def ip_address_case(self, data):
        self.driver.implicitly_wait(2)
        self._create(data)
        self._modify(data)
        self._delete(data)
    
    def _column_settings_case(self):
        self._goto_subObjectPage()
        self.objects_po.Column_settings(Column=list_Column_settings_HTTP_Signatures_Description_posXpath)
    
    def _view_statistics_case(self,data):
        self._goto_subObjectPage()
        self._create(data)
        self._search(data)
        if data['Create']['model'] == '0':
            self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_ip_address_editButton_posId).click()
            self.driver.find_element(By.XPATH, "//div[@id='id']//span[text()='Elaborate']").click()
            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_OK_posXpath).click()
            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_warningSaveYes_posXpath).click()
        self.objects_po.View_statistics(edit_element=listPage_object_ip_address_editButton_posId)
        self._delete(data)

    def loading_parameter(self, data):
        self.objects_po.Modify_object(data)
        # 创建mobile_identities
        # 点击create
        self.import_status = "0"
        self.my_files = ReadData()
        self.modify_status = "0"
        self.create_name = self.objects_po.create_name
        self.random_name = self.my_random.random_name()
        self.random_item = self.my_random.random_ipv4_or_ipv6()
        self.random_number = self.my_random.random_number()
    
    def audit_log_case(self, data):
        # 进入编辑页面
        self._create(data)
        self._search(data)
        # 查询后进行编辑操作
        self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()
        self.driver.find_element(By.ID, listPage_object_ip_address_editButton_posId).click()
        # 点击audit Logs
        self.driver.find_element(By.XPATH,main_button_audit_button_posXpath).click()
        self.driver.is_exist_element(Element='//table/tbody/tr[1]') # 编辑记录第一行是否有数据
        assert self.driver.Exist,"断言存在创建记录"
        print("断言成功，存在创建记录")
        self.driver.is_exist_element(Element='//table/tbody/tr[2]')  # 编辑记录第二行是否存在编辑记录
        assert self.driver.Exist == False,"断言不存在编辑记录"
        print("断言成功，不存在编辑记录")
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_ipAddress_posId).click()
        self._delete(data)
    
    def _goto_subObjectPage(self):
        self.objects_po.licenese_Check()
        # 菜单操作 跳转到mobile_identities页面
        self.driver.find_element(By.ID, mainPage_firstLevelMenu_Objects_posId).click()
        self.driver.find_element(By.ID, mainPage_secondLevelMenu_ipAddress_posId).click()
    
    def _page_turn_case(self, data):
        self._goto_subObjectPage()
        self.objects_po.pages_turning(data)
    
    def watch_button_case(self):
        # self._create(data)
        self._goto_subObjectPage()
        self.objects_po.Watch_list()
		
    def _input_name_destination(self, data):
        if data["Create"]["model"] == "0":
                # 创建ip_address,input_name
                self.driver.find_element(By.ID, listPage_object_ip_address_create_ip_address_Button_posId).click()
                self.driver.find_element(By.XPATH, ip_addressObjectPage_input_Name_posXpath).send_keys(self.create_name)
                self.driver.find_element(By.XPATH, ip_addressObjectPage_textArea_Description_posXpath).send_keys(self.random_name)
        elif data["Create"]["model"] == "1":
            # 创建mobile_identities_Group,input_name
            self.driver.find_element(By.ID, listPage_object_ip_address_create_ip_address_Group_Button_posId).click()
            self.driver.find_element(By.XPATH, ip_addressObjectPage_textArea_Description_posXpath).send_keys(self.random_name)
            self.driver.find_element(By.XPATH,ip_addressObjectPage_input_Name_posXpath).send_keys(self.create_name)
    
    def _ip_address_object_create(self, data):
        if data["Createtype"] == "IP":
            if data['Create']['type'] == "new_object":
                self._add_item(data)
            elif data['Create']['type'] == "import_files":
                # 点击导入文件按钮
                self.driver.find_element(By.XPATH, main_button_import_files_button_posXpath).click()
                # 导入文件
                self.driver.find_element(By.XPATH, main_ObjectPage_Input_path_Import_files_posXpath).send_keys(self.my_files._obj_files_path(file_name=data["Create"]["files_name"]))
            elif data['Create']['type'] == "export_files":
                pass
        elif data["Createtype"] == 'Geography':
            # 选择Geography
            self.driver.find_element(By.ID, ip_addressObjectPage_radioButton_Geography_posId).click()
            if data['Create']['type'] == "new_object":
                for item in data['Create']['item']:
                    # 新建item
                    self.Geography = ip_addressObjectPage_radioButton_Geography_Select_Asia.replace("replace",item)
                    self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                    self.driver.find_element(By.XPATH, self.Geography).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_radioButton_Geography_Select_Asia_China).click()
            elif data['Create']['type'] == "import_files":
                pass
            elif data['Create']['type'] == "export_files":
                pass
        elif data["Createtype"] == "IP_Learnig":
            # 选择IP_Learnig
            self.driver.find_element(By.ID, ip_addressObjectPage_radioButton_IP_learning_posId).click()
            if data['Create']['type'] == "new_object":
                self._add_item(data)
            elif data['Create']['type'] == "import_files":
                pass
            elif data['Create']['type'] == "export_files":
                pass
    
    def _sub_ip_address_create(self, data):
        if data["Createtype"] == "IP":
            if data['Create']['type'] == "new_object":
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_addButton_posXpath).click()  # 添加sub_Object
                # 进入添加object界面
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_Button_posXpath).click()  # add new sub_object
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_Select_one_Button_posXpath).click()  # new mobile_Identities
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_one_inputName_posXpath).send_keys(self.random_number)  # new mobile_Identities_InputName
                # 添加sub_object信息
                self._add_item(data)
            elif data['Create']['type'] == "import_files":
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_addButton_posXpath).click()  # 添加sub_Object
                # 进入添加object界面
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_Button_posXpath).click()  # add new sub_object
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_Select_one_Button_posXpath).click()  # new mobile_Identities
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_one_inputName_posXpath).send_keys(self.random_number)  # new mobile_Identities_InputName
                # 导入文件
                # 点击导入文件按钮
                self.driver.find_element(By.XPATH, main_button_import_files_button_posXpath).click()
                # 导入文件
                self.driver.find_element(By.XPATH, main_ObjectPage_Input_path_Import_files_posXpath).send_keys(self.my_files._obj_files_path(file_name=data["Create"]["files_name"]))
                pass
            elif data['Create']['type'] == "quote":
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_addButton_posXpath).click()  # 添加sub_Object
                self.driver.find_element(By.XPATH, mainPage_ObjectSearch_buttonSearch_Item_posXpath).send_keys(data['Create']['sub_name']+Keys.ENTER)
                self.driver.find_element(By.XPATH, main_Group_sub_Object_input_frame_select_one_posXpath).click()
            elif data['Create']['type'] == "export_files":
                pass
        elif data["Createtype"] == 'Geography':
            if data['Create']['type'] == "new_object":
                # 选择Geography
                self.driver.find_element(By.ID, ip_addressObjectPage_radioButton_Geography_posId).click()
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_addButton_posXpath).click()  # 添加sub_Object
                # 进入添加object界面
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_Button_posXpath).click()  # add new sub_object
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_Select_one_Button_posXpath).click()  # new mobile_Identities
                self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_one_inputName_posXpath).send_keys(self.random_number)  # new mobile_Identities_InputName
                # 添加sub_object信息
                self._add_item(data)
            elif data['Create']['type'] == "import_files":
                pass
            elif data['Create']['type'] == "export_files":
                pass
    
    def confirm_creation(self, data):
        if data["Create"]["model"] == "0":
            #导入验证
            if data['Create']['type'] =="import_files":
                # 确认导入
                self.driver.find_element(By.XPATH, main_ObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath).click()
            # 确认创建
            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_OK_posXpath).click()
            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_warningSaveYes_posXpath).click()
            time.sleep(3)
            if self.modify_status == "0":
                self.objects_po.extract_ele()
            elif self.modify_status == "1":
                time.sleep(3)
                self.objects_po.assert_ele()
                if self.objects_po.modify_name !=None:
                    #  断言修改Name是否生效
                    assert self.objects_po.modify_name == self.objects_po.edit_table_dict['edit_after_Name'], "校验修改Name是否生效"
                else:
                    pass
        elif data["Create"]["model"] == "1":
            if self.modify_status == "0":
                if data['Create']['type'] == "quote":
                    # 确认创建
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_OK_posXpath).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_warningSaveYes_posXpath).click()
                    self.objects_po.extract_ele()
                else:
                    if data['Create']['type'] == "import_files":
                        # 确认导入
                        self.driver.find_element(By.XPATH, main_ObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath).click()
                    # 确认创建sub object
                    self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_one_OK1_Button_posXpath).click()  # 保存new_Object
                    self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath).click()  # 确认新建保存按钮
                    if self.modify_status =="1" or self.modify_status == "2":
                        # 确认创建
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_SaveYes_posXpath).click()
                        try:
                            self.driver.is_exist_element(Element=ip_addressObjectPage_button_warningSaveYes_posXpath)
                            if self.driver.Exist:
                                self.driver.find_element(By.XPATH, ip_addressObjectPage_button_warningSaveYes_posXpath).click()
                            else:
                                pass
                        except:
                            pass
                    else:
                        # 确认创建
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_OK_posXpath).click()
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_warningSaveYes_posXpath).click()
                    time.sleep(3)
                    self.objects_po.extract_ele()
        #对不规范创建Object的验证
        elif data["Create"]["model"] == "2":
            if len(data['Name'])<4:
                self.driver.find_element(By.XPATH, ip_addressObjectPage_button_OK_posXpath).click()
                self.Name_tip = self.driver.find_element(By.XPATH,main_ObjectPage_tips_Name_input_Xpath).text
                assert self.Name_tip == "The length of the name is at most 128 characters and cannot be less than 4 characters","Name字符不符合要求"
            if data['Create']['item'] == "null":
                # 确认创建
                self.driver.find_element(By.XPATH, ip_addressObjectPage_button_OK_posXpath).click()
                self.driver.find_element(By.XPATH, ip_addressObjectPage_button_warningSaveYes_posXpath).click()
                self.driver.is_exist_element(Element=main_Import_Mobile_Identity_files_error_type_posXpath)
                if self.driver.Exist:
                    self.alert_tip =self.driver.find_element(By.XPATH, main_Import_Mobile_Identity_files_error_type_posXpath).text
                    assert self.alert_tip=="INVALID REQUEST:Object's member[items/subordinate object] is mandatory."
    
    def _add_item(self, data):
        if data["Create"]["model"] == "0" :
            if data['Create']['item'] == "null":
                data['Create']['model'] ="2"
            elif data["Createtype"] == "IP":
                if self.modify_status == "0":
                    # 新建item
                    for item in data['Create']['item']:
                        self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_inputItem_posXpath).send_keys(item)
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Save_Item_posXpath).click()
                        if data['Subtype'] == "error_item":
                            self.driver.is_exist_element(Element=ip_addressObjectPage_addItem_error_tips_posXpath)
                            if self.driver.Exist:
                                self.error_item_tips = self.driver.find_element(By.XPATH, ip_addressObjectPage_addItem_error_tips_posXpath).text
                                assert self.error_item_tips == "IP format error","错误item的提示"
                                data['Create']['model'] ="2"
                        self.item_content  = item
                elif self.modify_status == "1":  #add item
                    # 新建item
                    if type(data['Create']['item_modify']['add_data']) == list:
                        for item in data['Create']['item_modify']['add_data']:
                            self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_inputItem_posXpath).send_keys(item)
                            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Save_Item_posXpath).click()
                    elif type(data['Create']['item_modify']['add_data']) == str:
                        self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_inputItem_posXpath).send_keys(data['Create']['item_modify']['add_data'])
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Save_Item_posXpath).click()
                elif self.modify_status == "2":   #modify item
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_editItem_posXpath).click()
                    description_elem = self.driver.find_element(By.XPATH, ip_addressObjectPage_button_ip_text_posXpath)
                    description_elem.clear()
                    description_elem.send_keys(data['Create']['item_modify']['modify_data'])
                    self.driver.find_element(By.XPATH, "//i[@class='operate-icon iconfont icon-save check']").click()
            elif data["Createtype"] == "Geography":
                if self.modify_status == "0":
                    # 新建item
                    self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_radioButton_Geography_Select_Asia).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_radioButton_Geography_Select_Asia_China).click()
                elif self.modify_status == "1":
                    # 添加item
                    self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                    self.Geography = ip_addressObjectPage_radioButton_Geography_Select_replace.replace("replace",data['Create']['item_modify']['add_data'])
                    self.driver.find_element(By.XPATH, self.Geography).click()
                    self.driver.find_element(By.XPATH, ip_address_Geography_list_first_ele_posXpath).click()
            elif data['Createtype'] == "IP_Learnig":
                if self.modify_status == "0":
                    # 新建IP_Learing_item
                    for item in data['Create']['item']:
                        self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_IP_learning_inputItem_posXpath).send_keys(item)
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Save_Item_posXpath).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_IP_learn_from_protocols_posXpath).click()
                    for learn_from_protocols in data['Create']['Learn From Protocols']:
                        if learn_from_protocols == "HTTP":
                            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_IP_learn_from_protocols_Select_HTTP_posXpath).click()
                        elif learn_from_protocols == "SSL":
                            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_IP_learn_from_protocols_Select_SSL_posXpath).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_IP_learn_from_protocols_up_posXpath).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Input_Aging_Times_posXpath).send_keys(data['Create']['Aging Times'])
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Input_Vote_Clients_Number_posXpath).send_keys(data['Create']['Vote Clients Number'])
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Input_Learned_IP_Limits_posXpath).send_keys(data['Create']['Learned IP Limits'])
                    self.driver.find_element(By.XPATH, '//div/span[contains(text(),"seconds")]').click()
                    if data['Subtype'] == "error_item":
                        self.driver.is_exist_element(Element=ip_addressObjectPage_addItem_error_tips_posXpath)
                        if self.driver.Exist:
                            self.error_item_tips = self.driver.find_element(By.XPATH, ip_addressObjectPage_addItem_error_tips_posXpath).text
                            assert self.error_item_tips == "Format error", "错误item的提示"
                            data['Create']['model'] = "2"
                            try:
                                assert self.driver.find_element(By.XPATH, '//form/div[4]/form/div[3]/div/div[2]').text =="It should not be 0 or empty, or exceed 2,147,483,647.","Aging Times为空断言"
                                print("Aging Times为空断言成功")
                                assert self.driver.find_element(By.XPATH, '//div/div/div[1]/div[2]/form/div[4]/form/div[4]/div/div[2]').text == "It should not be 0 or empty, or exceed 10,000.", "Vote Clients Number为空断言"
                                print("Vote Clients Number为空断言成功")
                                assert self.driver.find_element(By.XPATH, '//form/div[4]/form/div[5]/div/div[2]').text == "It should not be 0 or empty, or exceed 10,000.", "Learned IP Limits为空断言"
                                print("Learned IP Limits为空断言成功")
                            except:
                                print("Aging Times、Vote Clients Number、Learned IP Limits不为空")
                                pass
                elif self.modify_status == "1":
                    # 提取total个数，add-item后，再次提取，断言个数为+1
                    self.total_count = self.driver.find_element(By.XPATH, main_first_Item_count_posXpath).text
                    if type(data['Create']['item_modify']['add_data']) == list:
                        # 新加IP_Learing_item
                        for item in data['Create']['item_modify']['add_data']:
                            self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                            self.driver.find_element(By.XPATH, ip_addressObjectPage_IP_learning_inputItem_posXpath).send_keys(item)
                            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Save_Item_posXpath).click()
                    elif type(data['Create']['item_modify']['add_data']) == str:
                        # 新加IP_Learing_item
                        self.driver.find_element(By.ID, ip_addressObjectPage_button_addItem_posId).click()
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_IP_learning_inputItem_posXpath).send_keys(data['Create']['item_modify']['add_data'])
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_button_Save_Item_posXpath).click()
                    # 暂时只支持add_data个数为1
                    assert self.objects_po._split_assert(assert_content=self.total_count) == self.driver.find_element(By.XPATH, main_first_Item_count_posXpath).text, "断言输入后Total+1"

                elif self.modify_status == "2":  # modify item
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_editItem_posXpath).click()
                    description_elem = self.driver.find_element(By.XPATH, ip_addressObjectPage_button_ip_learing_text_posXpath)
                    description_elem.clear()
                    description_elem.send_keys(data['Create']['item_modify']['modify_data'])
                    self.driver.find_element(By.XPATH, "//i[@class='operate-icon iconfont icon-save check']").click()
            if len(data['Name'])<4:
                data['Create']['model'] ="2"
        elif data["Create"]["model"] == "1" :
            if data['Create']['item'] == "null":
                data['Create']['model'] = "2"
            elif data["Createtype"] == "IP":
                if self.modify_status == "0":
                    for item in data['Create']['item']:
                        self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_add_item_Button_posXpath).click()  # new添加itemButton
                        self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_addIP_item_inputName_posXpath).send_keys(item)  # 输入item
                        self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_add_itemIP_Save_Button_posXpath).click()  # 添加item保存
                elif self.modify_status == "1":
                    self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_edit_subObject_Button_posXpath).click()
                    if type(data['Create']['item_modify']['add_data']) == list:
                        for item in data['Create']['item_modify']['add_data']:
                            self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_add_item_Button_posXpath).click()  # new添加itemButton
                            self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_addIP_item_inputName_posXpath).send_keys(item)  # 输入item
                            self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_add_itemIP_Save_Button_posXpath).click()  # 添加item保存
                    elif type(data['Create']['item_modify']['add_data']) == str:
                        self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_add_item_Button_posXpath).click()  # new添加itemButton
                        self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_addIP_item_inputName_posXpath).send_keys(data['Create']['item_modify']['add_data'])  # 输入item
                        self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_add_itemIP_Save_Button_posXpath).click()  # 添加item保存
                elif self.modify_status == "2":
                    self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_edit_subObject_Button_posXpath).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_button_editItem_posXpath).click()
                    description_elem = self.driver.find_element(By.XPATH, ip_addressObjectPage_button_ip_text_posXpath)
                    description_elem.clear()
                    description_elem.send_keys(data['Create']['item_modify']['modify_data'])
                    self.driver.find_element(By.XPATH, "//i[@class='operate-icon iconfont icon-save check']").click()
            elif data["Createtype"] == "Geography":
                if self.modify_status == "0":
                    # 新建item
                    self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_add_new_add_item_Button_posXpath).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_radioButton_Geography_Select_Asia).click()
                    self.driver.find_element(By.XPATH, ip_addressObjectPage_radioButton_Geography_Select_Asia_China).click()
                elif self.modify_status == "1":
                    self.driver.find_element(By.XPATH, ip_address_Group_sub_Object_edit_subObject_Button_posXpath).click()
                    if type(data['Create']['item_modify']['add_data']) == list:
                        for item in data['Create']['item_modify']['add_data']:
                            # 添加item
                            self.driver.find_element(By.XPATH, ip_addressObjectPage_Group_button_addItem_posXpath).click()
                            self.Geography = ip_addressObjectPage_radioButton_Geography_Select_replace.replace("replace", item)
                            self.driver.find_element(By.XPATH, self.Geography).click()
                            self.driver.find_element(By.XPATH, ip_address_Geography_list_first_ele_posXpath).click()
                    elif type(data['Create']['item_modify']['add_data']) == str:
                        # 添加item
                        self.driver.find_element(By.XPATH, ip_addressObjectPage_Group_button_addItem_posXpath).click()
                        self.Geography = ip_addressObjectPage_radioButton_Geography_Select_replace.replace("replace",data['Create']['item_modify']['add_data'])
                        self.driver.find_element(By.XPATH, self.Geography).click()
                        self.driver.find_element(By.XPATH, ip_address_Geography_list_first_ele_posXpath).click()
            if len(data['Name']) < 4:
                data['Create']['model'] = "2"
    
    def _create(self, data):
        # 跳转到mobile_identities列表页
        self._goto_subObjectPage()
        self.loading_parameter(data)
        # 创建mobile_identities
        # 点击create
        self.driver.find_element(By.ID, listPage_object_ip_address_createButton_posId).click()
        if data["Create"]["model"] == "0":
            # 输入ip_address,input_name
            self._input_name_destination(data)
            # 添加item
            self._ip_address_object_create(data)
            #验证重复item
            if data["isRepetition"] == "1":
                self.objects_po.Duplicate_check(data)
            # 确认创建
            self.confirm_creation(data)
        elif data["Create"]["model"] == "1":
            # 输入ip_address,input_name
            self._input_name_destination(data)
            # 添加item
            self._sub_ip_address_create(data)
            # 确认创建
            self.confirm_creation(data)
            
    def _search(self, data):
        if data["Search_type"] == "ID":
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(self.objects_po.table_dict['ID'])
            self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Id_posXpath).click()
        elif data["Search_type"] == "Name":
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(
                self.objects_po.table_dict['Name'])
            self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Name_posXpath).click()
        elif data["Search_type"] == "Description":
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(
                self.objects_po.table_dict['Description'])
            self.driver.find_element(By.XPATH,listPage_objectSearch_ip_address_select_Description_posXpath).click()
        elif data["Search_type"] == "Details":
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(
                self.objects_po.table_dict['Details'])
            self.driver.find_element(By.XPATH,listPage_objectSearch_ip_address_select_Details_posXpath).click()
        elif data["Search_type"] == "subType":
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys()
            self.driver.find_element(By.XPATH,listPage_objectSearch_ip_address_select_subType_posXpath).click()
        elif data["Search_type"] == "Createby":
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys()
            self.driver.find_element(By.XPATH,listPage_objectSearch_ip_address_select_CreateBy_posXpath).click()
        elif data['Search_type'] == 'subName':
            # 删除Group下的sub mobile
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys(self.random_number)
            self.driver.find_element(By.XPATH, listPage_objectSearch_ip_address_select_Name_posXpath).click()
        else:  # 全局查询
            self.driver.find_element(By.ID, listPage_objectSearch_ip_address_selectLabel_posId).send_keys()
            self.driver.find_element(By.ID, mainPage_ObjectSearch_buttonSearch_posId).click()
        self.driver.find_element(By.ID, mainPage_ObjectSearch_buttonSearch_posId).click()
    
    def _modify(self, data):
        if self.objects_po.modify_name != None:
            self.modify_status = "1"
            self._search(data)
            # 查询后进行编辑操作
            self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_ip_address_editButton_posId).click()
            self.objects_po.clear_Name(path=ip_addressObjectPage_input_Name_posXpath)
            self.driver.find_element(By.XPATH, ip_addressObjectPage_input_Name_posXpath).send_keys(self.objects_po.modify_name)
            # 确认修改进行断言
            self.confirm_creation(data)
        if "item_modify" in data['Create']:
            self._search(data)
            self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_ip_address_editButton_posId).click()
            if data['Create']['item_modify']['type'] == "add":
                self.modify_status ="1"
                self._add_item(data)
                self.confirm_creation(data)
            if data['Create']['item_modify']['type'] == "check":
                self.driver.find_element(By.ID,mainPage_ObjectSearch_buttonSearch_Item_posId).send_keys(data['Create']['item_modify']['check_data']+Keys.ENTER)
                self.item_check_content = self.driver.find_element(By.XPATH,ip_addressObjectPage_button_addItem_first_item_posXpath).text
                assert self.item_check_content == data['Create']['item_modify']['check_data'],"断言检查item文本正确"
            if data['Create']['item_modify']['type'] == "modify":
                self.modify_status = "2"
                self._add_item(data)
                self.confirm_creation(data)
        else:
            pass
    
    def _delete(self, data, search_value=None, dele_flag=None):
        if self.modify_status == "1" and data['Create']['type'] == "0":
            self.driver.find_element(By.XPATH,listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
            self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
            self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()
            # self.Page_Tips = self.driver.find_element(By.XPATH, listPage_object_ip_address_del_after_ele_posXpath).text
            # assert self.Page_Tips == "No Data", "校验修改Name是否生效"
        elif self.modify_status == "1" and data['Create']['type'] == "1":
            self.driver.find_element(By.XPATH,listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
            self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
            self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()
            self._delete_sub(data)
            time.sleep(2)
            # self.Page_Tips = self.driver.find_element(By.XPATH, listPage_object_ip_address_del_after_ele_posXpath).text
            # assert self.Page_Tips == "No Data", "校验修改Name是否生效"
        elif data['Subtype'] =="not_delete":
            pass
        elif data['Subtype'] =="Five_layer":
            self._search(data)
            # 1、点击第二个对象 2、校验删除按钮是否置灰
            self.driver.find_element(By.XPATH, main_listPage_object_select_Second_object_posXpath).click()
            self.driver.is_exist_element(Element=listPage_object_ip_address_delButton_disable_posXpath)
            assert  self.driver.Exist,"断言删除按钮状态为置灰状态"
            self.driver.find_element(By.XPATH, main_listPage_object_select_Second_object_posXpath).click()
            self.quote_count = self.driver.find_element(By.XPATH, list_quote_content_object_HTTP_Signatures_posXpath).text
            # 3、提取引用个数 4、点击引用框，断言第一行存在引用，第二行不存在引用
            assert int(self.quote_count) == 1,"断言引用计数为1"
            self.driver.find_element(By.XPATH, list_quote_content_object_HTTP_Signatures_posXpath).click()
            self.driver.is_exist_element(Element=list_quote_first_row_object_HTTP_Signatures_posXpath)
            assert self.driver.Exist,"断言第一行引用计数存在"
            self.driver.is_exist_element(Element=list_quote_second_row_object_HTTP_Signatures_posXpath)
            assert self.driver.Exist ==False ,"断言第二行引用不存在"
            for i in range(5):
                time.sleep(1)
                self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
                self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
                self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()
        elif data['Subtype'] == "export_files":
            self._search(data)
            self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
            self.driver.find_element(By.XPATH, main_ObjectPage_Input_Import_files_button_posXpath).click() # 点击导出文件
            self.driver.find_element(By.XPATH, list_PageObject_Export_files_yes_button_posXpath).click()
            # 校验文件内容
            # 2、检验文件内容
            time.sleep(3)
            self.file_name = get_txt_filenames(path=self.my_files._obj_files_dowload_path())
            self.file_path = self.my_files._obj_files_dowload_path() + "\\" + self.file_name
            self.content = open(self.file_path, "rb").read()
            try:
                assert str(self.item_content) in str(self.content), "断言导出内容是否在txt文件中"
                os.remove(self.file_path)
                print("文件删除成功")
            except:
                print("文件不存在")
            # 3、断言成功后，删除文件
            self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
            self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()
        elif data['Create']['model'] == "2":
            pass
        else:
            self._goto_subObjectPage()
            self._search(data)
            self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
            self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
            self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()
            time.sleep(3)
            if data["Create"]["model"] == "1":
                self._delete_sub(data)
                time.sleep(3)
                # self.Page_Tips = self.driver.find_element(By.XPATH,listPage_object_ip_address_del_after_ele_posXpath).text
                # assert self.Page_Tips == "No Data", "校验修改Name是否生效"
    
    def _delete_sub(self, data):
        self._goto_subObjectPage()
        data['Search_type'] = 'subName'
        self._search(data)
        self.driver.find_element(By.XPATH, listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
        self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
        self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()

    def _repetition_item_case(self, data):
        self._create(data)
        # self._modify(data)
        if data["isRepetition"] == "1":
            self._search(data)
            for i in range(2):
                time.sleep(1)
                self.driver.find_element(By.XPATH,listPage_object_ip_address_select_First_object_posXpath).click()  # 选择第一个对象
                self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
                self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()

    def test_clear_counter(self, data):
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
        print(page_flag, selected_object_type, selected_objects_number, detail_type)
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
            self._goto_subObjectPage()  # 页面跳转
            self.driver.implicitly_wait(5)
            is_firstObjectGroup_exist = self.driver.is_exist_element_by_value(By.XPATH, acc_listPage_object_tableCheckbox_firstObjectGroup_posXpath)
            is_firstSingleObject_exist = self.driver.is_exist_element_by_value(By.XPATH,acc_listPage_object_tableCheckbox_firstSingleObject_posXpath)
            if is_firstObjectGroup_exist == False or is_firstSingleObject_exist == False:
                # 创建测试数据
                self._create(data=obj_data)
                create_data_flag = 1
            else:
                firstSingleObject = self.driver.find_element(By.XPATH, acc_listPage_object_tableCheckbox_firstSingleObject_posXpath)
                firstObjectGroup = self.driver.find_element(By.XPATH,acc_listPage_object_tableCheckbox_firstObjectGroup_posXpath)
                firstNotLocalVsysObjectOrGroup = self.driver.find_element(By.XPATH,acc_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath)

                if firstSingleObject == firstNotLocalVsysObjectOrGroup or firstObjectGroup == firstNotLocalVsysObjectOrGroup:
                    # 创建测试数据
                    self._create(data=obj_data)
                    create_data_flag = 1
                else:
                    pass

        except Exception as e:
            print(e)
        if page_flag == 0:  # 列表页
            self._pure_operate_checkbox(selected_object_type, selected_objects_number)  # 列表页选择操作
            self._verify_clear_counter(page_flag, selected_object_type, selected_objects_number, selected_data_number,
                                       detail_type)
        else:  # 详情页
            # 判断进入何种类型的Object的详情页
            self._judge_whitch_page(detail_type)
            self._verify_clear_counter(page_flag, selected_object_type, selected_objects_number, selected_data_number,detail_type)
        # 页面跳转
        self.driver.refresh()
        self._goto_subObjectPage()
        # 清除测试数据
        if create_data_flag == 1:  # 已新建数据
            self._delete(obj_data, search_value="test_ui", del_flag=1)
        elif self.create_other_vsys_data_flag == 1:  # 已创建其他Vsys数据
            # 切换Vsys至Vsys3
            vsys_name = self.loginout_parse.get("vsys3", "vsys_name")  # 登录后vsys切换为UIAutoTestVsys
            profile_pub = ProfilesPublicOperations(self.driver)
            profile_pub.change_vsys(vsys_name=vsys_name)
            # # 页面跳转
            # self._just_goto_accountsPage()
            # 清除测试数据
            self._delete(obj_data, search_value="test_ui", del_flag=1)

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
                        selected_objects_number = 1
                    elif len(local_vsys_object_checkbox_elems) == 0:
                        selected_objects_number = 1
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
                        print("i.click()")
                        selected_objects_number -= 1
                for j in local_vsys_object_checkbox_elems:
                    if selected_objects_number < 1:
                        break
                    else:
                        j.click()
                        print("j.click()")
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
            is_clear_counter_clickable = self.driver.find_element(By.XPATH,acc_ObjectDetailPage_clearCounter_posXpath).get_attribute("class")
            if detail_type != 2:  # 不是非本Vsys的详情页
                assert "not-allowed" not in is_clear_counter_clickable, "is_clear_counter_clickable = {}".format(is_clear_counter_clickable)
            else:  # 非本Vsys的详情页
                assert "not-allowed" in is_clear_counter_clickable, "is_clear_counter_clickable = {}".format(is_clear_counter_clickable)

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
            self.driver.find_element(By.ID, listPage_object_ip_address_editButton_posId).click()  # 点击edit按钮
        elif detail_type == 1:  # Object Group详情页
            # 选中第一个Object Group并进入其详情页
            self.driver.find_element(By.XPATH, acc_listPage_object_tableCheckbox_firstObjectGroup_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_ip_address_editButton_posId).click()  # 点击edit按钮

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
                    profile_pub.change_vsys(vsys_name=vsys_name)
                    self._create(data=obj_data)
                    ui_vsys_name = self.loginout_parse.get("vsys", "vsys_name")  # 切换为UIAutoTestVsys
                    profile_pub.change_vsys(vsys_name=ui_vsys_name)
                    self.create_other_vsys_data_flag = 1
            except Exception as e:
                print(e)
            # 选中第一个非本Vsys的Object Group或Object并进入其详情页
            self.driver.find_element(By.XPATH,
                                     acc_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath).click()
            self.driver.find_element(By.ID, listPage_object_ip_address_editButton_posId).click()  # 点击edit按钮
    
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

if __name__ == '__main__':
    my_files = ReadData()
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': my_files._obj_files_dowload_path()}
    options.add_experimental_option('prefs', prefs)
    a = download_files()
    # a.get("http://192.168.44.72")
    # a.maximize_window()
    # a.find_element(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[2]/div[1]/div/input").send_keys("youzhijiang")
    # a.find_element(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[2]/div[2]/div/input").send_keys("youzhijiang1")
    # a.find_element(By.ID,"login").click()
    # time.sleep(2)
    r = IpAddress(a)
    profile_pub = ProfilesPublicOperations(a)
    profile_pub.change_vsys(vsys_name='UIAutoTestVsys')
    # model=0/1 ====0:单个   1group
    # type =IMSI/Phone_Number/IMEI
    data = {
        "ids": "用例3、IP的修改添加item",
        "Name": "test-1",
        "Create": {
            "model": "0",
            "type": "new_object",
            "item": ["1.1.1.1"],
            "item_modify": {"type": "add","add_data": "192.168.2.1/24"}
        },
        "Createtype": "IP",
        "isRepetition": "False",
        "Subtype": "",
        "Search_type": "ID"
    }
    r.ip_address_case(data)