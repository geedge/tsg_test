# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.profile.create_sc_profile import CreateServiceFunctionForwarderProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.policy.edit_rule import EditRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.element_position.profile_element_position import *
from support.packet_generator.verification import Verification
from support.api_utils.analysis_result import *
import support.ui_utils.env
from support.api_utils.log_in import *
from support.api_utils.delete_policy import *
from support.ui_utils.object.generate_random_ip import *
from support.report import *
from datetime import datetime

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        result, exception_result = "", ""
        
        # 脚本启动时间
        start_time = time.time()

        # 环境初始化
        driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()

        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "service_chaining",
            "rule_name": "sc_raw_rtp_mirror_bypass_vlan_none",
            "rule_action": "service_chaining",
            "targeted_traffic": "raw",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [],
                "external_port": [],
                "geography": [],
                "sub_id": [],
                "device": [],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "rtp",  
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [],
                "sub_action_override": False,
                "sub_action": [],
                "packet_capture": [],
            },
            "multiProfile": True,
            "profile": [
                {
                    "name": "mirror_bypass_vlan_none",
                    "profile_type": "create",
                    "type": "mirroring",
                    "load_balance_method": "hash_int-ip",
                    "load_balance_localization": "nearby",
                    "failure_action": "Bypass",
                    "service_functions": [
                        {
                            "name": "vlan_none",
                            "profile_type": "create",
                            "device_group": "Device_Group:group-xxg-tsgx",
                            "connectivity": "Layer_2_Switch:random:random",
                            "health_check": "none",
                            "enable": "on"
                        }
                    ]
                }
            ],
            "log_query_param": [{"query_field_key": "sc_rsp_raw", "query_value": ""}],
            "traffic":{
                    "protocol": "",
                    "type": "trex",
                    "clients_start_ip": "10.64.225.22",
                    "clients_end_ip": "10.64.225.22",
                    "servers_start_ip": "10.64.226.22",
                    "servers_end_ip": "10.64.226.22",
                    "m": 1,
                    "d": 1,
                    "yaml_name": "test",
                    "pcap_name": "rtp"
                },
            "expected_return":"",
            "token": ""
        }

        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "service_chaining":
            test_service_function_forwarder_profile_element_position = {
                "page_jump":{
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
                    "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_serviceFunctionForwarders_posId
                },
                "create": {
                    "profileListPage_createButton_posId": listPage_profile_serviceFunctionForwarders_createButton_posId,
                    "profilePge_inputName_posId": serviceFunctionForwarders_input_Name_posId,
                    "profilePage_operateRadio_posXpath": serviceFunctionForwarders_radio_labelAndRadioName_posXpath,
                    "profilePage_addSF_posXpath": serviceFunctionForwarders_button_serviceFunctionsAdd_posXpath,
                    "profilePage_searchSF_posXpath":serviceFunctionForwarders_rightDrawer_input_sfDrawerSearch_posXpath,
                    "profilePage_chooseSF_posXpath":serviceFunctionForwarders_rightDrawer_li_sfDrawerFirerRowItem_posXpath,
                    "profilePage_closeSFProfile_posXpath":serviceFunctionForwarders_rightDrawer_button_sfDrawerClose_posXpath,
                    "profilePge_okButton_posXCss":serviceFunctionForwarders_button_oK_posCss,
                    "profilePge_okButton_warningYes_posXpath":serviceFunctionForwarders_button_warningSaveYes_posCss
                },
                "search": {
                    "profileListPage_searchLabel_posId": listPage_profileSearch_serviceFunctionForwarders_selectLabel_posId,
                    "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_serviceFunctionForwarders_dropDown_item_posXpath,
                    "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_serviceFunctionForwarders_input_itemContent_posXpath,
                    "profileListPage_tableTbody_posXpath": listPage_profilTable_serviceFunctionForwarders_tableTbody_posXpath
                },
                "delete": {
                    "profileListPage_allSelect_posXpath": listPage_profileBottomPage_serviceFunctionForwarders_button_allSelect_posXpath,
                    "profileListPage_deleteButton_posId": listPage_profile_serviceFunctionForwarders_delButton_posId,
                    "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_serviceFunctionForwarders_button_yes_posCss
                }
            }
            test_service_function_profile_element_position = {
                "page_jump":{
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
                    "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_serviceFunctions_posId
                },
                "create":{
                    "profileListPage_createButton_posId":listPage_profile_serviceFunctions_createButton_posId,
                    "profileListPage_inputName_posId":serviceFunctions_input_Name_posId,
                    "profilePage_operateDeviceRadio_posXpath":serviceFunctions_radio_selectDevice_posXpath,
                    "profilePage_addDeviceTag_posXpath": serviceFunctions_button_deviceGroupAdd_posXpath,
                    "profilePage_effectiveDevicesDrawerOk_posXpath": serviceFunctions_button_effectiveDevicesDrawerOk_posXpath,
                    "profilePage_intInternalVlan_posXpath": serviceFunctions_input_internalVlan_posXpath,
                    "profilePage_intExternalVlan_posXpath": serviceFunctions_input_externalVlan_posXpath,
				    "profilePage_layer2Switch_posXpath": serviceFunctions_radio_connectivityLayer2Switch_posXpath,
                    "profilePage_Vxlan_G_posXpath": serviceFunctions_radio_connectivityXvlan_posXpath,
                    "profilePage_inputDestIP_posXpath": serviceFunctions_input_destinationIpAddress_posXpath,
                    "profilePage_operateHealthCheckRadio_posXpath": serviceFunctions_radio_healthCheck_posXpath,
                    "profilePage_inputInterval_posXpath":serviceFunctions_input_interval_posXpath,
                    "profilePage_inputRetries_posXpath": serviceFunctions_input_retries_posXpath,
                    "profilePage_okButton_posCss": serviceFunctions_button_oK_posCss,
                    "profilePage_okButton_warningYes_posCss": serviceFunctions_button_warningSaveYes_posCss
                },
                "search": {
                    "profileListPage_searchLabel_posId": listPage_profileSearch_serviceFunctions_selectLabel_posId,
                    "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_serviceFunctions_dropDown_item_posXpath,
                    "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_serviceFunctions_input_itemContent_posXpath,
                    "profileListPage_tableTbody_posXpath": listPage_profilTable_serviceFunctions_tableTbody_posXpath
                },
                "delete": {
                    "profileListPage_allSelect_posXpath": listPage_profileBottomPage_serviceFunctions_button_allSelect_posXpath,
                    "profileListPage_deleteButton_posId": listPage_profile_serviceFunctions_delButton_posId,
                    "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_serviceFunctions_button_yes_posCss
                }
            }
            test_rule_element_position = {
                "page_jump":{
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_servicechaining_posId
                },
                "create": {
                    "policyRuleListPage_createButton_posId":serviceChainingRuleListPage_createButton_posId,
                    "policyRulePage_inputName_posXpath": serviceChainingRulePage_inputName_posXpath,
                    "policyRulePage_chooseTargetedTraffic_posXpath": serviceChainingRulePage_decryptedTrafficButton_posXpath,
                    "policyRulePage_addSrcIP_posXpath": serviceChainingRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": serviceChainingRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": serviceChainingRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": serviceChainingRulePage_closeSrcIP_posXpath,
                    "policyRulePage_addDstIP_posXpath": serviceChainingRulePage_addDstIP_posXpath,
                    "policyRulePage_searchDstIP_posXpath": serviceChainingRulePage_searchDstIP_posXpath,
                    "policyRulePage_selectDstIP_posXpath": serviceChainingRulePage_selectDstIP_posXpath,
                    "policyRulePage_closeDstIP_posXpath": serviceChainingRulePage_closeDstIP_posXpath,
                    "policyRulePage_addCondition_posXpath": policyRulePage_addCondition_posXpath,
                    "policyRulePage_addCondition_close_posXpath": policyRulePage_addCondition_close_posXpath,
                    "policyRulePage_addApplication_posXpath": serviceChainingRulePage_addApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath":serviceChainingRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_searchApplication_posXpath": serviceChainingRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": serviceChainingRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": serviceChainingRulePage_closeApplication_posXpath,
                    "policyRulePage_addSFFProfile_posId": serviceChainingRulePage_addSFFProfile_posId,
                    "policyRulePage_searchSFFProfile_posXpath":serviceChainingRulePage_searchSFFProfile_posXpath,
                    "policyRulePage_selectSFFProfile_posXpath":serviceChainingRulePage_selectSFFProfile_posXpath,
                    "policyRulePage_closeSFFProfile_posXpath":serviceChainingRulePage_closeSFFProfile_posXpath,
                    "policyRulePage_enable_posXpath": serviceChainingRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": serviceChainingRulePage_okButton_posId,
                    "policyRulePage_okButton_warningYes_posXpath": serviceChainingRulePage_warningYes_posXpath
                },
                "search": {
                    "policyRuleListPage_searchLable_posId": serviceChainingRuleListPage_searchLable_posId,
                    "policyRuleListPage_searchLable_dropDown_item_posXpath": serviceChainingRuleListPage_searchLable_dropDown_item_posXpath,
                    "policyRuleListPage_searchLable_input_itemContent_posXpath": serviceChainingRuleListPage_searchLable_input_itemContent_posXpath,
                    "policyRuleListPage_searchLable_searchButton_posId": serviceChainingRuleListPage_searchLable_searchButton_posId,
                    "policyRuleListPage_tableTbody_posXpath": serviceChainingRuleListPage_tableTbody_posXpath
                },
                "delete": {
                    "policyRuleListPage_allSelect_posXpath": securityRulelistPage_allSelect_posXpath,
                    "policyRuleListPage_deleteButton_posId": serviceChainingRuleListPage_deleteButton_posId,
                    "policyRuleListPage_okButton_warningYes_posXpath": serviceChainingRuleListPage_warningYes_posXpath
                }
            }

            log_in = LogIn()
            pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
            token = log_in.login(parameter["username"], pwd, parameter["api_server"])
            test_data["token"] = token

        # name_list汇总
            name_list = [
                {
                    "type": "service_chaining",
                    "name": "sc_raw_rtp_mirror_bypass_vlan_none",
                },
                {
                    "type": "service_function_forwarder",
                    "name": "mirror_bypass_vlan_none",
                },
                {
                    "type": "service_function",
                    "name": "vlan_none",
                }
            ]

        # 创建profile
        if "profile" in test_data and len(test_data["profile"]) != 0:
            service_chaining_profile = CreateServiceFunctionForwarderProfile(driver)
            create_profile_code,sc_info= service_chaining_profile.create_sff_profile(test_data,test_service_function_forwarder_profile_element_position,test_service_function_profile_element_position)
            if create_profile_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create service function forwarder profile successfully.", flush=True)
            elif create_profile_code != 200:
                result = "Fail to create service chaining profile."

        # 创建rule
        if create_profile_code == 200:
            create_rule = CreateRule(driver)
            create_rule_code = create_rule.create(test_data, test_rule_element_position)
            if create_rule_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create service chaining rule successfully.", flush=True)
            elif create_rule_code != 200:
                result = "Fail to create service chaining rule."
            
        # 触发流量验证
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
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
                verify = Verification()
                verification_result = verify.verification(driver, parameter, test_data, cfg_list, test_rule_element_position)
                if len(verification_result) == 4:
                    driver = verification_result[3]
                elif len(verification_result) == 5:
                    driver = verification_result[4]

        # 分析验证结果，并返回给flask
        if len(verification_result) != 0:
            analysis = AnalysisResult()
            result = analysis.analysis_result(test_data, [], verification_result)
            # if len(result) == 0:
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
            # elif len(result) != 0:
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", result, flush=True)

        # 删除rule
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service chaining rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete service chaining rule."
                else:
                    result = result + " In addition, fail to search service chaining rule."

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
                                elif delete_sf_code != 200:
                                    result = result + " In addition, fail to delete service function."
                                    break
                            else:
                                result = result + " In addition, fail to search service function."
                                break
                    elif delete_sff_code != 200:
                        result = result + " In addition, fail to delete service function forwarder."
                        break
                else:
                    result = result + " In addition, fail to search service function forwarder."
                    break

            # 脚本结束时间和耗时
            end_time = time.time()
            duration = end_time - start_time
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
            
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
            return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境
        support.ui_utils.env.teardown()
        # 删除配置
        delete = DeletePolicy()
        delete.delete_policy_by_name(token, parameter, name_list)
        # 生成csv报告
        file_path = parameter["root_path"] + "/report/{}_report.csv".format(parameter["script_type"])
        if os.path.exists(file_path) and os.path.isfile(file_path):  
            if result is not None and result != "" and len(result) != 0:
                report_data = []
                report_data.append(parameter["test_case_name"])
                result_flag = "Fail"
                report_data.append(result_flag)
                report_data.append(result)
            elif exception_result is not None and exception_result != "" and len(exception_result) != 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Fail"
                report_data.append(result_flag)
                report_data.append(exception_result)
            elif result == "" and len(result) == 0 and exception_result == "" and len(exception_result) == 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Pass"
                report_data.append(result_flag)
                report_data.append("")
            new_report = GenerateReport()
            new_report.insert_data(parameter, report_data)
    
if __name__ == '__main__':
    parameter = {
        "username": "lytest",
        "password": "123456ly",
        "test_pc_ip": "192.168.50.88",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 5,
        "is_log": 1,
        "root_path": "C:/automation_project/tsg_test",
        "path": "C:/automation_project/tsg_test/tests/ui",
        "module_name": "service_chaining",
        "test_case_name": "sc_raw_rtp_mirror_bypass_vlan_none"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """