# import os
import sys
import time
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.profile.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
import re
import random
import copy
from datetime import datetime 

class CreateProfile():
    def __init__(self, driver):
        self.driver = driver
    def create_sff_profile(self, data, sff_profile_element_position,sf_profile_element_position):
        sc_info = {}
        page_jump_element_position = sff_profile_element_position["page_jump"]
        create_element_position = sff_profile_element_position["create"]
        try:
            # 新建sf
            if "service_functions" in data.keys():   # 判断是否需要创建sf
                service_functions = data["service_functions"]
                sf_name_list,sc_info= self.get_sf_info(service_functions,sf_profile_element_position,sc_info)
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_profile_page(page_jump_element_position)
            # 点击create
            self.driver.find_element(By.ID, create_element_position["profileListPage_createButton_posId"]).click()
            # 输入name
            sff_name = data["name"]
            self.driver.find_element(By.ID, create_element_position["profilePge_inputName_posId"]).send_keys(sff_name)
            #页面除name外其他选项的操作
            sc_info= self.operate_sff_page(data,sc_info,sf_name_list,sff_profile_element_position)
            # 确认创建
            self.driver.find_element(By.CSS_SELECTOR, create_element_position["profilePge_okButton_posXCss"]).click()
            self.driver.find_element(By.CSS_SELECTOR, create_element_position["profilePge_okButton_warningYes_posXpath"]).click()
            return 200,sc_info
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            return 400
    def operate_sff_page(self, data,sc_info,sf_name_list,sff_profile_element_position):
        create_element_position = sff_profile_element_position["create"]
        """
        除name的其它选项操作，共创建、修改逻辑调用
        :param data:
        :param operation_type: create modify。创建 修改时调用
        :return:
        """
        # 重组定位使用
        label_dict = {'type': 'Type', 'load_balance_method': 'Load Balance Method', 'load_balance_localization': 'Load Balance Localization',
                       'failure_action': 'Failure Action', "unavailability_action": "Unavailability Action"}
        radio_name_dict = {'steering': 'Steering', 'mirroring': 'Mirroring', 'hash_int-ip': 'Hash Int-IP', 'hash_ext-ip': 'Hash Ext-IP',
                           'hash_int-ip_and_ext-ip': 'Hash Int-IP and Ext-IP', 'hash_innermost_int-ip': 'Hash Innermost Int-IP',
                           'nearby': 'Nearby', 'global': 'Global', 'bypass': 'Bypass', 're-dispatch': 'Re-dispatch', 'block': 'Block'}
        # Type 操作
        sff_type = self.format_from_data_lower_and_underline(data, key="type")  
        if sff_type == "steering":
            sc_info["type"] = 1
        elif sff_type == "mirroring":
            sc_info["type"] = 2
        self.sff_operate_radio(create_element_position, key="type", value=sff_type, label_dict=label_dict, radio_name_dict=radio_name_dict)
        # Load Balance Method 操作
        load_balance_method = self.format_from_data_lower_and_underline(data, key="load_balance_method")
        self.sff_operate_radio(create_element_position, key="load_balance_method", value=load_balance_method, label_dict=label_dict, radio_name_dict=radio_name_dict)
        # Load Balance Localization操作
        load_balance_localization = self.format_from_data_lower_and_underline(data, key="load_balance_localization")
        self.sff_operate_radio(create_element_position, key="load_balance_localization", value=load_balance_localization, label_dict=label_dict, radio_name_dict=radio_name_dict)
        # Failure Action 操作
        failure_action = self.format_from_data_lower_and_underline(data, key="failure_action")
        failure_action_list = failure_action.split(":")
        failure_action = failure_action_list[0]
        self.sff_operate_radio(create_element_position, key="failure_action", value=failure_action, label_dict=label_dict, radio_name_dict=radio_name_dict)     #点击 Failure Action 操作
        if "re-dispatch" in failure_action_list:
            # Unavailability Action 点击操作
            replaceLabel_unavailability_action = label_dict["unavailability_action"]
            replaceRadioName_unavailability_action = radio_name_dict[failure_action_list[1]]
            ep_unavailability_action = create_element_position["profilePage_operateUnavailabilityAction_Radio_posXpath"].format(replaceLabel=replaceLabel_unavailability_action, replaceRadioName=replaceRadioName_unavailability_action)
            self.driver.find_element(By.XPATH,ep_unavailability_action).click()   #点击 Unavailability Action
            if "bypass" in failure_action_list:   # bypass 下的输入框操作 Minimum Health Service Functions
                data_minHealthServiceFunctions = failure_action_list[-1]
                self.operate_input(data_input=data_minHealthServiceFunctions, ep_input=create_element_position["profilePage_inputMiniHealthServerFunctions_posXpath"])   # 输入 Minimum Health Service Functions
        #添加SF的操作
        self.driver.find_element(By.XPATH,create_element_position["profilePage_addSF_posXpath"]).click()
        for name in sf_name_list:
            self.driver.find_element(By.XPATH,create_element_position["profilePage_searchSF_posXpath"]).send_keys(name)
            self.driver.find_element(By.XPATH,create_element_position["profilePage_searchSF_posXpath"]).send_keys(Keys.ENTER)
            time.sleep(1.5)
            self.driver.find_element(By.XPATH,create_element_position["profilePage_chooseSF_posXpath"].format(replaceValue=name)).click()
        self.driver.find_element(By.XPATH,create_element_position["profilePage_closeSFProfile_posXpath"]).click()
        return sc_info

    def sff_operate_radio(self,create_element_position,key="", value="", label_dict=None, radio_name_dict=None):
        """Type  Load Balance Method  Load Balance Localization  Failure Action  单选按钮操作
        适合
        :param key:
        :param value:
        :param label_dict: 为字典类型{}
        :param radio_name_dict:为字典类型{}
        :return:
        """
        # 替换元素定位中的值，组织元素定位
        replaceLabel_type = label_dict[key]
        replaceRadioName_type = radio_name_dict[value]
        ep_radio_type = create_element_position["profilePage_operateRadio_posXpath"].format(replaceLabel=replaceLabel_type, replaceRadioName=replaceRadioName_type)
        # type点选按钮操作
        self.driver.find_element(By.XPATH,ep_radio_type).click()

    def format_lower_and_underline(self, str_a: str):
        """
        将字符串替换为小写，所有空格替换为一个下划线   A  b   C    a_b_c
        """
        str_a = str_a.lower()
        str_b = re.sub(r"\s+", "_", str_a)
        return str_b

    def format_from_data_lower_and_underline(self, data, key=""):
        value = data[key]
        value = self.format_lower_and_underline(value)
        return value  

    def get_sf_info(self, service_functions,sf_profile_element_position,sc_info):
        """
        可以创建多个sf对象
        :param service_functions:    sf所需数据列表
        :return:   [sf_name_id_dict, sf_id_data_dict]  例如： [{"name1":"1", "name2":"2"}, {"1":{sf1}, "2":{sf2}}]
        """
        sf_name_list = []    #sf的name的列表
        for sf in range(len(service_functions)):
            try:
                serviceFunctions_name,sc_info= self.create_sf_profile(service_functions[sf],sf_profile_element_position,sc_info)
                sf_name_list.append(serviceFunctions_name)
            except:   # 给一次概率一样的机会
                serviceFunctions_name = self.create_sf_profile(service_functions[sf],sf_profile_element_position,sc_info)
        return sf_name_list,sc_info
    
    def create_sf_profile(self,data, profile_element_position, sc_info):
        page_jump_element_position = profile_element_position["page_jump"]
        create_element_position = profile_element_position["create"]
        #页面跳转
        page_jump = PageJump(self.driver)
        page_jump.jump_sub_profile_page(page_jump_element_position)
        #点击create
        self.driver.find_element(By.ID,create_element_position["profileListPage_createButton_posId"]).click()
        #在打开页面操作：输入name
        sf_name = data["name"]
        self.driver.find_element(By.ID,create_element_position["profileListPage_inputName_posId"]).send_keys(sf_name)
        #页面其它选项操作
        result_info = self.operate_sf_page(data,create_element_position,sc_info)
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, create_element_position["profilePage_okButton_posCss"]).click()
        self.driver.find_element(By.CSS_SELECTOR, create_element_position["profilePage_okButton_warningYes_posCss"]).click()
        time.sleep(2)
        return sf_name,result_info
    
    def operate_sf_page(self,data,create_element_position,sc_info):
        # Device Group 操作
        device_group = self.format_from_data_lower_and_underline(data, key="device_group")
        device_group_list = device_group.split(":")
        #替换元素定位中的值，组织元素定位
        effective_devices_group_dict = {"device_group": "Select Device Group", "data_center": "Select Data Center"}
        effective_devices_name_dict = {'group-xxg-tsgxsfcos': 'group-xxg-tsgxSfcOs', 'group-xxg-7400': 'group-xxg-7400', 'group-xxg-9140': 'group-xxg-9140', 'group-xxg-tsgx': 'group-xxg-tsgx',
                                        'center-xxg-7400': 'center-xxg-7400', 'center-xxg-9140': 'center-xxg-9140', 'center-xxg-tsgx': 'center-xxg-tsgx', 'center_02': 'Center 02', 'city_a': 'City A',
                                        'group_华严3楼':'GROUP 华严3楼', 'group_华严4楼':'GROUP 华严4楼', 'center_华严3楼':'Center 华严3楼', 'center_华严4楼':'Center 华严4楼'}
        replaceGroup = effective_devices_group_dict[device_group_list[0]]
        replaceDeviceName = effective_devices_name_dict[device_group_list[-1]]
        ep_dropdown_item = create_element_position["profilePage_operateDeviceRadio_posXpath"].format(replaceGroup=replaceGroup, replaceDeviceName=replaceDeviceName)
        #点击添加框
        self.driver.find_element(By.XPATH, create_element_position["profilePage_addDeviceTag_posXpath"]).click()
        #点击侧滑里列表中按钮
        self.driver.find_element(By.XPATH, ep_dropdown_item).click()
        self.driver.find_element(By.XPATH, create_element_position["profilePage_effectiveDevicesDrawerOk_posXpath"]).click()
        # Connectivity选择操作
        connectivity = self.format_from_data_lower_and_underline(data, key="connectivity")
        data_internal_vlan = data_external_vlan = ""
        connectivity_list = connectivity.split(":")
        if "layer" in connectivity:   # Layer 2 Switch 定位
            sc_info["sf_method"] = "layer2_switch"
            self.driver.find_element(By.XPATH,create_element_position["profilePage_layer2Switch_posXpath"]).click()
            data_internal_vlan = connectivity_list[1]
            if data_internal_vlan == "random":   #随机生成
                data_internal_vlan = random.randint(2048, 4000)
                self.driver.find_element(By.XPATH,create_element_position["profilePage_intInternalVlan_posXpath"]).send_keys(data_internal_vlan)
            data_external_vlan = connectivity_list[2]
            if data_external_vlan == "random":   #随机生成
                data_external_vlan = random.randint(2048, 4000)
                self.driver.find_element(By.XPATH,create_element_position["profilePage_intExternalVlan_posXpath"]).send_keys(data_external_vlan)
        else:     # vxlan定位
            sc_info["sf_method"] = "vxlan_g"
            self.driver.find_element(By.XPATH,create_element_position["profilePage_Vxlan_G_posXpath"]).click()
            sf_dest_ip = connectivity_list[1]
            sc_info["sf_dest_ip"] = sf_dest_ip
            self.operate_input(sf_dest_ip,create_element_position["profilePage_inputDestIP_posXpath"],True)
        # Health Check 操作
        health_check = self.format_from_data_lower_and_underline(data, key="health_check")
        # 组织元素定位
        health_check_radio_index_dict = {'none': 0, 'in-band_bfd': 1, 'bfd': 2, 'http': 3}
        health_item = health_check.split(":")[0]
        replaceIndex = health_check_radio_index_dict[health_item]
        # 点击health check单选按钮
        self.driver.find_element(By.XPATH,create_element_position["profilePage_operateHealthCheckRadio_posXpath"].format(replaceIndex=replaceIndex)).click()
        if health_check.startswith("bfd:"):
            health_check_list = health_check.split(":")
            data_interval = health_check_list[1]
            data_retries = health_check_list[2]
            # 输入input操作
            self.operate_input(data_interval,create_element_position["profilePage_inputInterval_posXpath"],True)
            self.operate_input(data_retries,create_element_position["profilePage_inputRetries_posXpath"],True)
        if data["enable"] == "off":
            self.driver.find_element(By.XPATH,create_element_position["profilePage_switch_enableButton_posXpath"]).click()
            sc_info["admin_status"] = 0
        else:
            sc_info["admin_status"] = 1
        return sc_info
    def operate_input(self, data_input="", ep_input="", is_clear=True):
        """
        页面中输入框类型操作
        :param input_data: input 输入值
        :param ep_input: 输入框元素定位
        :param is_clear: 输入前是否情况数据，默认是：True  False
        :return:
        """
        if is_clear:     # 清楚原有数据
            self.driver.find_element(By.XPATH, ep_input).clear()
        self.driver.find_element(By.XPATH, ep_input).send_keys(data_input)

    def operate_drawer_box(self, ep_dropdown_input="", ep_dropdown_item=""):
        """
        侧滑选择点击操作
        :param ep_dropdown_input:   下拉菜单输入框定位
        :param ep_dropdown_item:     下拉菜单列表选项定位
        :return:
        """
        #点击添加框
        self.driver.find_element(By.XPATH, ep_dropdown_input).click()
        #点击侧滑里列表中按钮
        self.driver.find_element(By.XPATH, ep_dropdown_item).click()
        self.driver.find_element(By.XPATH, serviceFunctions_button_effectiveDevicesDrawerOk_posXpath).click()        