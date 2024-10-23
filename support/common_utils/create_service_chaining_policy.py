# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.profile.create_sc_profile import CreateServiceFunctionForwarderProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.element_position.profile_element_position import *
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.create_policy import CreatePolicy
from support.packet_generator.verify import Verify
from support.ui_utils.element_position.map_element_position_library import get_element_position, create_pre_policy, delete_pre_policy
from support.api_utils.analyse_result import Analyse
import support.ui_utils.env
from datetime import datetime
import copy
import time
from support.ui_utils.object.generate_random_ip import *
from support.common_utils.data_translation import DataTranslation

class CreateServiceChainingPolicy:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        result = self._run(self.test_data, self.parameter)
        return result

    def _run(self, test_data, parameter):
        # 声明定义数据
        ui_result, api_result = "", ""
        self.api_name_list, self.ui_name_list = [], []
        result = {
            "ui_result": "",
            "api_result": ""
        }

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token
        self.test_data["token"] = token

        # 无需创建的condition
        service_chaining_no_create_list = ["application", "ip_protocol","sub_action_override"]
        # name_list汇总
        temp_name_list = []
        policy_name_dict = {}
        policy_name_dict["type"] = test_data["policy_type"]
        policy_name_dict["name"] = test_data["rule_name"]
        temp_name_list.append(policy_name_dict)
        for con_key, conditions in test_data["condition"].items():  
            if conditions:  # 确保conditions不为空  
                if con_key in service_chaining_no_create_list:
                    continue
                if con_key in {"source_library", "destination_library","server_fqdn_library","internal_library","external_library"}:
                    continue
                for condition in conditions:  
                    # 为每个条件项创建一个新的字典  
                    obj_name_dict = {  
                        "type": condition["object_type"],  
                        "name": condition["name"]  
                    }  
                    temp_name_list.append(obj_name_dict) 
        for sff in test_data["profile"]:
            sff_name_dict = {
                "type": "service_function_forwarder",
                "name": sff["name"]
            }
            temp_name_list.append(sff_name_dict) 
            for sf in sff["service_functions"]:
                    sf_name_dict = {
                "type": "service_function",
                "name": sf["name"]
            }
            temp_name_list.append(sf_name_dict)
        self.ui_name_list = temp_name_list
        self.api_name_list = temp_name_list

        need_initialization = False
        if len(parameter["script_type"]) == 0:
            need_initialization = True

        if parameter["script_type"] == "ui" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)

                parameter["script_type"] = "ui"

                # 环境初始化
                support.ui_utils.env.initiate_selenium_request()
                driver = support.ui_utils.env.my_driver()
                support.ui_utils.env.setup()

                # 将测试数据中的ip替换为随机ip
                if test_data["targeted_traffic"] == "raw" and (len(test_data["condition"]["source_ip"]) != 0 or len(test_data["condition"]["destination_ip"]) != 0):
                    random_ip = GenerateRandomIP(driver)
                    test_data = random_ip.generate_random_ip(test_data,run_env=parameter["env"])

                test_service_function_forwarder_profile_element_position = {
                    "page_jump":{
                        "mainPage_menu_bar_posXpath": mainPage_menu_bar_posXpath,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
                        "mainPage_profileSecondLevelMenu_posXpath": mainPage_secondLevelMenu_statisticsTemplates_posXpath,
                        "mainPage_leftMenu_posXpath": mainPage_leftMenu_posXpath,
                        "mainPage_profileFirstLevelMenu_Name": mainPage_firstLevelMenu_profiles_posName,
                        "mainPage_profileSecondLevelMenu_Name": mainPage_secondLevelMenu_serviceFunctionForwarders_posName
                    },
                    "create": {
                        "profileListPage_createButton_posXpath": listPage_profile_serviceFunctionForwarders_createButton_posXpath,
                        "profilePge_inputName_posXpath": serviceFunctionForwarders_input_Name_posXpath,
                        "profilePage_operateRadio_posXpath": serviceFunctionForwarders_radio_labelAndRadioName_posXpath,
                        "profilePage_operateUnavailabilityAction_Radio_posXpath":serviceFunctionForwarders_radio_unavailabilityAction_posXpath,
                        "profilePage_inputMiniHealthServerFunctions_posXpath":serviceFunctionForwarders_input_minHealthServiceFunctions_posXpath,
                        "profilePage_addSF_posXpath": serviceFunctionForwarders_button_serviceFunctionsAdd_posXpath,
                        "profilePage_searchSF_posXpath":serviceFunctionForwarders_rightDrawer_input_sfDrawerSearch_posXpath,
                        "profilePage_chooseSF_posXpath":serviceFunctionForwarders_rightDrawer_li_sfDrawerFirerRowItem_posXpath,
                        "profilePage_closeSFProfile_posXpath":serviceFunctionForwarders_rightDrawer_button_sfDrawerClose_posXpath,
                        "profilePage_okButton_posXpath":serviceFunctionForwarders_button_oK_posXpath,
                    },
                    "search": {
                        "profileListPage_searchLabel_posXpath": listPage_profileSearch_serviceFunctionForwarders_selectLabel_posXpath,
                        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_serviceFunctionForwarders_dropDown_item_posXpath,
                        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_serviceFunctionForwarders_input_itemContent_posXpath,
                        "profileListPage_searchButton_posXpath": listPage_profileSearch_serviceFunctions_buttonSearch_posXpath,
                        "profileListPage_tableTbody_posXpath": listPage_profilTable_serviceFunctionForwarders_tableTbody_posXpath
                    },
                    "delete": {
                        "profileListPage_allSelect_posXpath": listPage_profileBottomPage_serviceFunctionForwarders_button_allSelect_posXpath,
                        "profileListPage_deleteButton_posXpath": listPage_profile_serviceFunctionForwarders_delButton_posXpath,
                        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_serviceFunctionForwarders_button_yes_posCss
                    }
                }
                test_service_function_profile_element_position = {
                    "page_jump":{
                        "mainPage_menu_bar_posXpath": mainPage_menu_bar_posXpath,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
                        "mainPage_profileSecondLevelMenu_posXpath": mainPage_secondLevelMenu_statisticsTemplates_posXpath,
                        "mainPage_leftMenu_posXpath": mainPage_leftMenu_posXpath,
                        "mainPage_profileFirstLevelMenu_Name": mainPage_firstLevelMenu_profiles_posName,
                        "mainPage_profileSecondLevelMenu_Name": mainPage_secondLevelMenu_serviceFunctions_posName
                    },
                    "create":{
                        "profileListPage_createButton_posXpath": listPage_profile_serviceFunctions_createButton_posXpath,
                        "profileListPage_inputName_posXpath": serviceFunctions_input_Name_posXpath,
                        "profilePage_addDeviceTag_posXpath": serviceFunctions_button_deviceGroupAdd_posXpath,
                        "profilePage_selectDeviceType_posXpath": serviceFunctions_radio_selectDeviceType_posXpath,
                        "profilePage_searchDevice_inputName_posXpath": serviceFunctions_searchDevice_input_Name_posXpath,
                        "profilePage_selectDevice_posXpath": serviceFunctions_radio_selectDevice_posXpath,
                        "profilePage_closeSidePage_posXpath": serviceFunctions_button_closeSidePage_Cancel_posXpath,
                        # vxlan
                        "profilePage_Vxlan_G_posXpath": serviceFunctions_radio_connectivityXvlan_posXpath,
                        "profilePage_inputDestIP_posXpath": serviceFunctions_input_destinationIpAddress_posXpath,
                        "profilePage_operateHealthCheckRadio_posXpath": serviceFunctions_radio_healthCheck_posXpath,
                        "profilePage_inputInterval_posXpath":serviceFunctions_input_interval_posXpath,
                        "profilePage_inputRetries_posXpath": serviceFunctions_input_retries_posXpath,
                        # vlan
                        "profilePage_layer2Switch_posXpath": serviceFunctions_radio_connectivityLayer2Switch_posXpath,
                        "profilePage_intInternalVlan_posXpath": serviceFunctions_input_internalVlan_posXpath,
                        "profilePage_intExternalVlan_posXpath": serviceFunctions_input_externalVlan_posXpath,
                        "profilePage_switch_enableButton_posXpath":serviceFunctions_switch_enalbe_posXpath,
                        "profilePage_okButton_posXpath": serviceFunctions_button_oK_posXpath,
                        "profilePage_okButton_warningYes_posCss": serviceFunctions_button_warningSaveYes_posCss
                    },
                    "search": {
                        "profileListPage_searchLabel_posXpath": listPage_profileSearch_serviceFunctions_selectLabel_posXpath,
                        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_serviceFunctions_dropDown_item_posXpath,
                        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_serviceFunctions_input_itemContent_posXpath,
                        "profileListPage_searchButton_posXpath": listPage_profileSearch_serviceFunctions_buttonSearch_posXpath,
                        "profileListPage_tableTbody_posXpath": listPage_profilTable_serviceFunctions_tableTbody_posXpath
                    },
                    "delete": {
                        "profileListPage_allSelect_posXpath": listPage_profileBottomPage_serviceFunctions_button_allSelect_posXpath,
                        "profileListPage_deleteButton_posXpath": listPage_profile_serviceFunctions_delButton_posXpath,
                        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_serviceFunctions_button_yes_posCss
                    }
                }

                # 创建object
                if "condition" in test_data.keys():
                    for cond_key, cond_value in (test_data["condition"].items()):
                        if cond_key in service_chaining_no_create_list:
                            continue   # 直接跳过
                        cond_status = 0
                        cond_key_out = cond_key.replace("_", " ")
                        if len(cond_value) != 0:  # 不为空
                            cond_data = cond_value
                            create_ip = CreateObject(driver)
                            for i in range(len(cond_data)):  # 遍历创建所有condition
                                if cond_key == "protocol_filed":
                                    tmp_key = cond_data[i]["object_type"]
                                    cond_key_out = tmp_key.replace("_", " ")
                                    element_position_map = get_element_position(tmp_key)
                                else:
                                    element_position_map = get_element_position(cond_key)
                                cond_code = create_ip.create(cond_data[i], element_position_map)
                                if cond_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(cond_key_out), flush=True)
                                else:
                                    ui_result = "Fail to create {} object.".format(cond_key_out)
                                    cond_status = 1
                                    break
                        if cond_status == 1:   # 创建失败，退出遍历创建
                            break

                # 创建profile
                if "profile" in test_data and len(test_data["profile"]) != 0:
                    service_chaining_profile = CreateServiceFunctionForwarderProfile(driver)
                    create_profile_code,sc_info= service_chaining_profile.create_sff_profile(test_data,test_service_function_forwarder_profile_element_position,test_service_function_profile_element_position)
                    if create_profile_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create service function forwarder profile successfully.", flush=True)
                    elif create_profile_code != 200:
                        ui_result = "Fail to create service function forwarder profile."

                # 创建rule
                if cond_code == 200 and create_profile_code == 200:
                    if test_data["targeted_traffic"] == "decrypted":
                        element_position_map = get_element_position(test_data["policy_type"])
                        # 添加intercept
                        tmp_name_list = create_pre_policy(test_data, driver)
                        for tmp in tmp_name_list:
                            self.ui_name_list.insert(0, copy.deepcopy(tmp))
                    create_rule = CreateRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    create_rule_code = create_rule.create(test_data, element_position_map)
                    if create_rule_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create service chaining rule successfully.", flush=True)
                    elif create_rule_code != 200:
                        ui_result = "Fail to create service chaining rule."

                # 触发流量验证
                if create_rule_code == 200:
                    time.sleep(1.5)
                    search_rule = SearchRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], element_position_map)
                    if search_rule_code == 200:
                        test_data["rule_id"] = rule_id
                        policy_type = test_data["policy_type"]
                        policy_id_dict_temp = {}
                        policy_id_dict_temp[policy_type] = rule_id
                        create_policies_ids = []
                        create_policies_ids.append(policy_id_dict_temp)
                        statistics_sc_info_list = []
                        sc_info["rule_id"] = rule_id
                        statistics_sc_info_list.append(sc_info)
                        cfg_list = {}
                        cfg_list["create_policies_ids"] = create_policies_ids
                        cfg_list["statistics_sc_info_list"] = statistics_sc_info_list
                        verification = Verify()
                        verification_result = verification.verify_result(driver, parameter, test_data, cfg_list, element_position_map)
                        if len(verification_result) == 4:
                            driver = verification_result[3]
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Traffic verification failed", flush=True)

                # 分析验证结果，并返回给flask
                if len(verification_result) == 4:
                    analysis = Analyse()
                    ui_result = analysis.analyse_result(test_data["policy_type"], [], verification_result)

                # 删除rule
                if create_rule_code == 200:
                    if test_data["targeted_traffic"] == "decrypted":
                        # 删除intercept策略
                        delete_pre_policy(tmp_name_list, driver)
                    search_rule = SearchRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], element_position_map)
                    if search_rule_code == 200:
                        delete_rule = DeleteRule(driver)
                        delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                        if delete_rule_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service chaining rule successfully.", flush=True)
                        elif delete_rule_code != 200:
                            ui_result = ui_result + " In addition, fail to delete {} rule.".format(test_data["policy_type"])
                    else:
                        ui_result = ui_result + " In addition, fail to search {} rule.".format(test_data["policy_type"])

                # 删除object
                if delete_rule_code == 200 and "condition" in test_data.keys():
                    # 删除
                    for cond_key, cond_value in (test_data["condition"].items()):  # 遍历所有cond数据
                        if cond_key in service_chaining_no_create_list:
                            continue  # 直接跳过
                        cond_status = 0
                        cond_key_out = cond_key.replace("_", " ")
                        if len(cond_value) != 0:  # 不为空
                            cond_data = cond_value
                            for i in range(len(cond_data)):  # 遍历查询所有condition
                                search_cond = SearchObject(driver)
                                if cond_key == "protocol_filed":
                                    tmp_key = cond_data[i]["object_type"]
                                    cond_key_out = tmp_key.replace("_", " ")
                                    element_position_map = get_element_position(tmp_key)
                                else:
                                    element_position_map = get_element_position(cond_key)
                                search_cond_code, first_row_checkbox_element = search_cond.search(cond_data[i]["name"], element_position_map)
                                if search_cond_code == 200:
                                    delete_cond = DeleteObject(driver)
                                    delete_cond_code = delete_cond.delete(element_position_map, first_row_checkbox_element, True)
                                    if delete_cond_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(cond_key_out), flush=True)
                                        time.sleep(1)
                                    else:
                                        ui_result = ui_result + " In addition, fail to delete {} object.".format(cond_key_out)
                                        break
                                else:
                                    ui_result = ui_result + " In addition, fail to search {} object.".format(cond_key_out)
                                    break
                                # 退出遍历标志
                                if cond_status == 1:  # 失败，退出遍历创建
                                    break
                        # 退出遍历标志
                        if cond_status == 1:  # 失败，退出遍历创建
                            break
                # 删除profile
                if delete_rule_code == 200:
                    # 删除sff
                    profile_data = test_data["profile"]
                    for x in range(len(profile_data)):
                        search_sff = SearchProfile(driver)
                        search_sff_code, first_row_checkbox_element = search_sff.search(profile_data[x]["name"],test_service_function_forwarder_profile_element_position)
                        if search_sff_code == 200:
                            delete_sff = DeleteProfile(driver)
                            delete_sff_code = delete_sff.delete(test_service_function_forwarder_profile_element_position, first_row_checkbox_element, True)
                            if delete_sff_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function forwarder successfully.", flush=True)
                                # 删除sf
                                sf_data = test_data["profile"][x]["service_functions"]
                                search_sf = SearchProfile(driver)
                                for y in range(len(sf_data)):
                                    search_sf_code, first_row_checkbox_element = search_sf.search(sf_data[y]["name"],test_service_function_profile_element_position)
                                    if search_sf_code == 200:
                                        delete_sf = DeleteProfile(driver)
                                        delete_sf_code = delete_sf.delete(test_service_function_profile_element_position, first_row_checkbox_element, True)
                                        if delete_sf_code == 200:
                                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function successfully.", flush=True)
                                        else:
                                            ui_result = ui_result + " In addition, fail to delete service function profile."
                                    else:
                                        ui_result = ui_result + " In addition, fail to search service function profile."
                            else:
                                ui_result = ui_result + " In addition, fail to delete service function forwarder profile."
                        else:
                            ui_result = ui_result + " In addition, fail to search service function forwarder profile."
            except Exception as e:
                raise
            finally:
                # 清理环境
                result["ui_result"] = ui_result
                support.ui_utils.env.teardown()
            
        if parameter["script_type"] == "api" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)

                parameter["script_type"] = "api"

                # 数据转换，适配API的test_data
                translation = DataTranslation()
                test_data = translation.data_translation(parameter, test_data)
                # print(test_data)

                # 添加测试过程中涉及的template
                template_path = {}
                template_path["rule_template"] = parameter["root_path"] + "/support/api_utils/template/rule_template.json"
                template_path["object_template"] = parameter["root_path"] + "/support/api_utils/template/object_template.json"
                template_path["pre_intercept_template_path"] = parameter["root_path"] + "/support/api_utils/template/pre_intercept_template.json"
                template_path["profile_sf_template"] =  parameter["root_path"] + "/support/api_utils/template/profile_sf_template.json"
                template_path["profile_sff_template"] =  parameter["root_path"] + "/support/api_utils/template/profile_sff_template.json"

                # 创建Object、Profile、Rule
                create = CreatePolicy()
                cfg_list = create.create_policy(parameter, test_data, template_path)
                time.sleep(30)

                # 流量验证
                verification = Verify()
                verification_result = verification.verify_result("", parameter, test_data, cfg_list, "")

                # 分析验证结果，并返回给flask
                analysis = Analyse()
                api_result = analysis.analyse_result(test_data["policy_type"], cfg_list, verification_result)
            except Exception as e:
                raise
            finally:
                result["api_result"] = api_result
                # 删除配置
                delete = DeletePolicy()
                delete.delele_policy_by_uuid(token, parameter, cfg_list)

        return result

    def clean_up(self):
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.ui_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        if isinstance(self.api_name_list, list) and self.api_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)