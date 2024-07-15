# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.profile.create_sc_profile import CreateProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.policy.edit_rule import EditRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.element_position.profile_element_position import *
from support.traffic_replay.traffic_verification import *
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
        result = ""
        
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
            "rule_name": "raw_mirror_redispatch_bypass_vxlan_activeip_none",
            "rule_action": "service_chaining",
            "targeted_traffic": "raw",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "service_chaining_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "10.64.224.25"
                            }
                        ]
                    }
                ],
                "source_port": [],
                "destination_ip": [
                    {
                        "name": "service_chaining_destination_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "10.64.224.29"
                            }
                        ]
                    }
                ],
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
                        "name": "ssl",  
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                    {
                        "name": "baidu.com",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "items": [
                            {
                                "item_value": "baidu.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [],
                "sub_action_override": False,
                "sub_action": [],
                "packet_capture": [],
            },
            "multiProfile": True,
            "profile": [
                {
                    "name": "mirror_redispatch_bypass_vxlan_activeip_none",
                    "profile_type": "create",
                    "type": "mirroring",
                    "load_balance_method": "hash_int-ip",
                    "load_balance_localization": "global",
                    "failure_action": "Re-dispatch:Bypass:1",
                    "service_functions": [
                        {
                            "name": "vxlan_activeip_none",
                            "profile_type": "create",
                            "device_group": "Device_Group:group-xxg-tsgx",
                            "connectivity": "VXLAN-G:2.2.2.53",
                            "health_check": "none",
                            "enable": "on"
                        }
                    ]
                }
            ],
            "traffic":{
                    "type": "trex",
                    "clients_start_ip": "192.168.64.86",
                    "clients_end_ip": "192.168.64.86",
                    "servers_start_ip": "2.1.1.1",
                    "servers_end_ip": "2.1.1.2",
                    "m": 1,
                    "d": 1,
                    "yaml_name": "test_https",
                    "pcap_name": "test_https"
                },
            "expected_return":"",
            "token": ""
        }

        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "service_chaining":
            test_ip_object_element_position = {
                    "page_jump":{
                        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                        "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                        "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_ipAddress_posId
                    },
                    "create": {
                        "objectListPage_createButton_posId": ipObjectListPage_createButton_posId,
                        "objectListPage_dropDown_createButton_posId": ipObjectListPage_dropDown_createButton_posId,
                        "objectPage_inputName_posXpath": ipObjectPage_inputName_posXpath,
                        "objectPage_ipType_posId": ipObjectPage_ipType_posId,
                        "objectPage_addItem_posId": ipObjectPage_addItem_posId,
                        "objectPage_inputItem_posXpath": ipObjectPage_inputItem_posXpath,
                        "objectPage_button_saveItem_posXpath": ipObjectPage_button_saveItem_posXpath,
                        "objectPage_okButton_posId": ipObjectPage_okButton_posId,
                        "objectPage_okButton_warningYes_posXpath": ipObjectPage_okButton_warningYes_posXpath
                    },
                    "search": {
                        "objectListPage_searchLabel_posId": ipObjectListPage_searchLabel_posId,
                        "objectListPage_searchLabel_selectName_posXpath": ipObjectListPage_searchLabel_selectName_posXpath,
                        "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
                    },
                    "delete": {
                        "objectListPage_allSelect_posXpath": ipObjectListPage_allSelect_posXpath,
                        "objectListPage_deleteButton_posId": ipObjectListPage_deleteButton_posId,
                        "objectListPage_deleteButton_warningYes_posXpath": ipObjectListPage_deleteButton_warningYes_posXpath
                    }
                }
            test_fqdn_object_element_position = {
                "page_jump":{
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_fqdn_posId
                },
                "create": {
                    "objectListPage_createButton_posId": fqdnObjectListPage_createButton_posId,
                    "objectListPage_dropDown_createButton_posId": fqdnObjectListPage_dropDown_createButton_posId,
                    "objectPage_inputName_posXpath": fqdnObjectPage_inputName_posXpath,
                    "objectPage_addItem_posId": fqdnObjectPage_addItem_posId,
                    "objectPage_inputItem_posXpath": fqdnObjectPage_inputItem_posXpath,
                    "objectPage_button_saveItem_posXpath": fqdnObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posId": fqdnObjectPage_okButton_posId,
                    "objectPage_okButton_warningYes_posXpath": fqdnObjectPage_okButton_warningYes_posXpath
                },
                "search": {
                    "objectListPage_searchLabel_posId": fqdnObjectListPage_searchLabel_posId,
                    "objectListPage_searchLabel_selectName_posXpath": fqdnObjectListPage_searchLabel_selectName_posXpath,
                    "objectListPage_tableTbody_posXpath": fqdnObjectListPage_tableTbody_posXpath
                },
                "delete": {
                    "objectListPage_allSelect_posXpath": fqdnObjectListPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posId": fqdnObjectListPage_deleteButton_posId,
                    "objectListPage_deleteButton_warningYes_posXpath": fqdnObjectListPage_deleteButton_warningYes_posXpath
                }
            }
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
                    "profilePage_operateUnavailabilityAction_Radio_posXpath":serviceFunctionForwarders_radio_unavailabilityAction_posXpath,
                    "profilePage_inputMiniHealthServerFunctions_posXpath":serviceFunctionForwarders_input_minHealthServiceFunctions_posXpath,
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
                    "policyRulePage_addApplication_posXpath": serviceChainingRulePage_addApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath":serviceChainingRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_searchApplication_posXpath": serviceChainingRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": serviceChainingRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": serviceChainingRulePage_closeApplication_posXpath,
                    "policyRulePage_addCondition_posXpath": serviceChainingRulePage_addCondition_posXpath,
                    "policyRulePage_addConditionServerFqdn_posXpath": serviceChainingRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addCondition_close_posXpath": serviceChainingRulePage_addCondition_close_posXpath,
                    "policyRulePage_addServerFqdn_posXpath": serviceChainingRulePage_addServerFqdn_posXpath,
                    "policyRulePage_searchServerFqdn_posXpath": serviceChainingRulePage_searchServerFqdn_posXpath,
                    "policyRulePage_selectServerFqdn_posXpath": serviceChainingRulePage_selectServerFqdn_posXpath,
                    "policyRulePage_closeServerFqdn_posXpath": serviceChainingRulePage_closeServerFqdn_posXpath,
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
                    "name": "raw_mirror_redispatch_bypass_vxlan_activeip_none",
                },
                {
                    "type": "ip",
                    "name": "service_chaining_source_ip",
                },
                {
                    "type": "ip",
                    "name": "service_chaining_destination_ip",    
                },
                {
                    "type": "fqdn",
                    "name": "baidu.com",
                },
                {
                    "type": "service_function_forwarder",
                    "name": "mirror_redispatch_bypass_vxlan_activeip_none",
                },
                {
                    "type": "service_function",
                    "name": "vxlan_activeip_none",
                }
            ]


        # 添加测试过程中涉及的template
        template_path = {}
        template_path["trex_workpath"] = "/opt/trex/v3.03"
        template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"

        # 将测试数据中的ip替换为随机ip
        random_ip = GenerateRandomIP(driver)
        test_data = random_ip.generate_random_ip(test_data,run_env=parameter["env"])
        
        # 创建object
        for condition_key in test_data["condition"].keys():
            if condition_key == "source_ip" or condition_key == "destination_ip":
                ip_data = test_data["condition"][condition_key]
                create_ip = CreateObject(driver)
                for i in range(len(ip_data)):
                    create_ip_code = create_ip.create(ip_data[i], test_ip_object_element_position)
                    if create_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create ip object successfully.", flush=True)
                    elif create_ip_code != 200:
                        result = "Fail to create ip object."
                        break
            if condition_key == "server_fqdn":
                fqdn_data = test_data["condition"][condition_key]
                create_fqdn = CreateObject(driver)
                for i in range(len(fqdn_data)):
                    create_fqdn_code = create_fqdn.create(fqdn_data[i], test_fqdn_object_element_position)
                    if create_fqdn_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create fqdn object successfully.", flush=True)
                    elif create_fqdn_code != 200:
                        result = "Fail to create fqdn object."
                        break

        # 创建profile
        if "profile" in test_data and len(test_data["profile"]) != 0:
            profile_data = test_data["profile"]
            service_chaining_profile = CreateProfile(driver)
            for j in range(len(profile_data)):
                create_profile_code,sc_info= service_chaining_profile.create_sff_profile(profile_data[j],test_service_function_forwarder_profile_element_position,test_service_function_profile_element_position)
                if create_profile_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create service function forwarder profile successfully.", flush=True)
                elif create_profile_code != 200:
                        result = "Fail to create service chaining profile."
                        break
                sc_info["targeted_traffic"] = test_data["targeted_traffic"]
                sc_info["app_name_1"] = test_data["condition"]["application"]
        # 创建rule
        if create_ip_code == 200 and create_profile_code == 200:
            create_rule = CreateRule(driver)
            create_rule_code = create_rule.create(test_data, test_rule_element_position)
            if create_rule_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create service chaining rule successfully.", flush=True)
            elif create_rule_code != 200:
                result = "Fail to create service chaining rule."
            
        # 触发流量验证
        if create_rule_code == 200:
            edit_rule = EditRule(driver)
            edit_rule_code, rule_id = edit_rule.edit(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
            if edit_rule_code == 200:
                test_data["rule_id"] = rule_id
                verify = TrafficVerification()
                verification_result = verify.traffic_verification(driver, parameter, test_data, sc_info)
                if len(verification_result) == 4:
                    driver = verification_result[3]
                elif len(verification_result) == 5:
                    driver = verification_result[4]

        # 分析验证结果，并返回给flask
        if len(verification_result) != 0:
            analysis = AnalysisResult()
            result = analysis.analysis_result(test_data, [], verification_result)
            if len(result) == 0:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
            elif len(result) != 0:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", result, flush=True)

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

        # 删除object
        if delete_rule_code == 200:
            # 删除ip
            for condition_key in test_data["condition"].keys():
                if condition_key == "source_ip" or condition_key == "destination_ip":
                    ip_data = test_data["condition"][condition_key]
                    for x in range(len(ip_data)):
                        search_ip = SearchObject(driver)
                        search_ip_code, first_row_checkbox_element = search_ip.search(ip_data[x]["name"], test_ip_object_element_position)
                        if search_ip_code == 200:
                            delete_ip = DeleteObject(driver)
                            delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
                            if delete_ip_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip object successfully.", flush=True)
                            elif delete_ip_code != 200:
                                result = result + " In addition, fail to delete ip object."
                                break
                        else:
                            result = result + " In addition, fail to search ip object."
                            break
                if condition_key == "server_fqdn":
                    fqdn_data = test_data["condition"][condition_key]
                    for x in range(len(fqdn_data)):
                        search_fqdn = SearchObject(driver)
                        search_fqdn_code, first_row_checkbox_element = search_fqdn.search(fqdn_data[x]["name"], test_fqdn_object_element_position)
                        if search_fqdn_code == 200:
                            delete_fqdn = DeleteObject(driver)
                            delete_fqdn_code = delete_fqdn.delete(test_fqdn_object_element_position, first_row_checkbox_element, True)
                            if delete_fqdn_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn object successfully.", flush=True)
                            elif delete_fqdn_code != 200:
                                result = result + " In addition, fail to delete fqdn object."
                                break
                        else:
                            result = result + " In addition, fail to search fqdn object."
                            break

        # 删除profile
        if delete_rule_code == 200:
            # 删除sff
            for x in range(len(profile_data)):
                search_sff = SearchProfile(driver)
                search_sff_code, first_row_checkbox_element = search_sff.search(profile_data[x]["name"],test_service_function_forwarder_profile_element_position)
                if search_sff_code == 200:
                    delete_sff = DeleteProfile(driver)
                    delete_sff_code = delete_sff.delete(test_service_function_forwarder_profile_element_position, first_row_checkbox_element, True)
                    if delete_sff_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete sff successfully.", flush=True)
                        # 删除sf
                        sf_data = test_data["profile"][x]["service_functions"]
                        search_sf = SearchProfile(driver)
                        for y in range(len(sf_data)):
                            search_sf_code, first_row_checkbox_element = search_sf.search(sf_data[y]["name"],test_service_function_profile_element_position)
                            if search_sf_code == 200:
                                delete_sf = DeleteProfile(driver)
                                delete_sf_code = delete_sf.delete(test_service_function_profile_element_position, first_row_checkbox_element, True)
                                if delete_sf_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete sf successfully.", flush=True)
                                elif delete_sf_code != 200:
                                    result = result + " In addition, fail to delete sf."
                                    break
                            else:
                                result = result + " In addition, fail to search sf."
                                break
                    elif delete_sff_code != 200:
                        result = result + " In addition, fail to delete sff."
                        break
                else:
                    result = result + " In addition, fail to search sff."
                    break

            # 脚本结束时间和耗时
            end_time = time.time()
            duration = end_time - start_time
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
            
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
            return result
    except Exception as e:
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
                if False in verification_result:
                    result_flag = "Fail"
                else:
                    result_flag = "Pass"
                report_data.append(result_flag)
                report_data.append(result)
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
        "vsys_id": 11,
        "is_log": 1,
        "root_path": "C:/automation_project/tsg_test",
        "path": "C:/automation_project/tsg_test/tests/ui",
        "module_name": "service_chaining",
        "test_case_name": "none"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """