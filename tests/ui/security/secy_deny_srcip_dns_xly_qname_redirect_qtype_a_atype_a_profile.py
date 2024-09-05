# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.policy.edit_rule import EditRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.packet_generator.verification import Verification
from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import *
from support.ui_utils.profile.create_dns_records_profile import CreateProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
import support.ui_utils.env

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
        support.ui_utils.env.initiate_selenium_request()
        driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_name": "secy_deny_srcip_dns_xly_qname_redirect_qtype_a_atype_a_profile",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "secy_srcip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter['test_pc_ip'],
                            }
                        ]
                    }
                ],
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [],
                "external_port": [],
                "source_geography": [],
                "destination_geography": [],
                "sub_id": [],
                "device": [],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "dns", #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [
                    {
                        "name": "secy_fqdn",
                        "object_type": "fqdn",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "qname",
                                "item_value": "$www.facebook.com"
                            }
                        ],
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                    {
                        "type": "redirect",
                        "resolution":[
                            {
                                "qtype": "A",
                                "answer":[
                                    {
                                        "atype": "A",
                                        "answer_value_type": "Profile",
                                        "profile_name": "secy_dns_type_A",
                                        "ttl": "300-333"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "packet_capture": []
            },
            "profile": [
                {
                    "name": "secy_dns_type_A",
                    "type": "A",
                    "items": ["1.1.1.1"]
                }
            ],
            "expected_return": "1.1.1.1",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key":"server_ip", "query_value": "8.8.8.8"},
                                {"query_field_key":"decoded_as", "query_value": "DNS"},
                                {"query_field_key":"dns_qname", "query_value": "www.facebook.com"}],
            "traffic": {
                "protocol": "dns",
                "type": "nslookup",
                "command": "nslookup www.facebook.com -timeout=1 8.8.8.8"
            },
            "token": ""
        }
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        # name_list汇总
        name_list = [
            {
                "type": test_data["policy_type"],
                "name": test_data["rule_name"]
            },
            {
                "type": test_data["condition"]["source_ip"][0]['object_type'],
                "name": test_data["condition"]["source_ip"][0]['name']
            },
            {
                "type": test_data["condition"]["protocol_filed"][0]['object_type'],
                "name": test_data["condition"]["protocol_filed"][0]['name']
            },
            {
                "type":"dns_records",
                "name":test_data["profile"][0]['name']
            }
        ]
        
        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "security":
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
            test_dns_records_profile_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
                    "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_dnsRecords_posId
                },
                "create": {
                    "profileListPage_createButton_posId": listPage_profile_dnsRecords_createButton_posId,
                    "profilePage_inputName_posId": dnsRecordsProfilePage_input_Name_posId,
                    "profilePage_Type_A_posId": dnsRecordsProfilePage_radioButton_typeA_posId,
                    "dnsRecordsProfiles_input_item_posXpath": dnsRecordsProfilePage_input_addItem_posXpath,
                    "dnsRecordsProfile_save_item_posXpath": dnsRecordsProfilePage_button_saveItemByIndex_posXpath,
                    "profilePage_button_oK_posCss": dnsRecordsProfilePage_button_oK_posCss,
                    "profilePage_button_cancel_posCss": dnsRecordsProfilePage_button_cancel_posCss,
                    "profilePage_button_warningSaveYes_posCss": dnsRecordsProfilePage_button_warningSaveYes_posCss,
                    # action
                },
                "edit": {
                    "templates_button_chartEdit_posXpath": listPage_profile_dnsRecords_editButton_posId
                },
                "search": {
                    "profileListPage_searchLabel_posId": listPage_profileSearch_dnsRecords_selectLabel_posId,
                    "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_dnsRecords_dropDown_item_posXpath,
                    "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_dnsRecords_input_itemContent_posXpath,
                    "profileListPage_tableTbody_posXpath": listPage_profilTable_dnsRecords_tableTbody_posXpath
                },
                "delete": {
                    "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
                    "profileListPage_deleteButton_posId": listPage_profile_dnsRecords_delButton_posId,
                    "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_dnsRecords_button_yes_posXpath
                }
            }
            test_rule_element_position = {
                "page_jump":{
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_security_posId
                },
                "create": {
                    "policyRuleListPage_createButton_posId": securityRuleListPage_createButton_posId,
                    "policyRulePage_inputName_posXpath": securityRulePage_inputName_posXpath,
                    "policyRulePage_selectAction_posId": securityRulePage_selectDeny_posId,
                    # srcip
                    "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": securityRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": securityRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
                    "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                    "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                    "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    # qname
                    "policyRulePage_addConditionQname_posXpath": securityRulePage_addCondition_qname_posXpath,
                    "policyRulePage_addQname_posXpath": securityRulePage_addQname_posXpath,
                    "policyRulePage_searchQname_posXpath": securityRulePage_searchQname_posXpath,
                    "policyRulePage_selectQname_posXpath": securityRulePage_selectQname_posXpath,
                    "policyRulePage_closeQname_posXpath": securityRulePage_closeQname_posXpath,
                    "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                    "policyRulePage_subAction_redirect_posXpath": securityRulePage_subAction_redirect_posXpath,
                    # dns redirect
                    "policyRulePage_dnsAnswer0ValueType_posId":  securityRulePage_subAction_redirect_answer0ValueType_posId,
                    "policyRulePage_dnsAnswer0ValueTypeChoose_posXpath":  securityRulePage_subAction_redirect_answer0ValueTypeChoose_posXpath,
                    "policyRulePage_dnsAnswerType0Choose_posId": securityRulePage_subAction_redirect_dnsAnswerType0choose_posId,
                    "policyRulePage_dnsAnswerType0ChooseValue_posXpath": securityRulePage_subAction_redirect_dnsAnswerType0chooseValue_posXpath,
                    "policyRulePage_dnsAnswerValueSelectPlaceholder_posId": securityRulePage_subAction_redirect_dnsAnswerValueSelectPlaceholder_posId,
                    "policyRulePage_dnsAnswerValueNameSearch_posId": securityRulePage_subAction_redirect_dnsAnswerValueNameSearch_posId,
                    "policyRulePage_dnsAnswerValueNameSelect_posId": securityRulePage_subAction_redirect_dnsAnswerValueNameSelect_posId,
                    "policyRulePage_dnsAnswer0ATextPlaceholder_posId": securityRulePage_subAction_redirect_dnsAnswer0ATextPlaceholder_posId,
                    "policyRulePage_dnsAnswerValueTTL0_posId": securityRulePage_subAction_redirect_dnsAnswerValueTTL0_posId,
                    "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": securityRulePage_okButton_yes_posId,
                    "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath
                },
                "search": {
                    "policyRuleListPage_searchLable_posId": securityRuleListPage_searchLable_posId,
                    "policyRuleListPage_searchLable_dropDown_item_posXpath": securityRuleListPage_searchLable_dropDown_item_posXpath,
                    "policyRuleListPage_searchLable_input_itemContent_posXpath": securityRuleListPage_searchLable_input_itemContent_posXpath,
                    "policyRuleListPage_searchLable_searchButton_posId": securityRuleListPage_searchLable_searchButton_posId,
                    "policyRuleListPage_tableTbody_posXpath": securityRuleListPage_tableTbody_posXpath
                },
                "delete": {
                    "policyRuleListPage_allSelect_posXpath": securityRulelistPage_allSelect_posXpath,
                    "policyRuleListPage_deleteButton_posId": securityRuleListPage_deleteButton_posId,
                    "policyRuleListPage_okButton_warningYes_posXpath": securityRuleListpage_okButton_warningYes_posXpath,
                    "policyRuleListPage_okButton_warningNo_posXpath":securityRuleListpage_okButton_warningNo_posXpath
                }
            }
        
        # 创建object
        if "source_ip" in test_data["condition"] and len(test_data["condition"]["source_ip"]) != 0:
            ip_data = test_data["condition"]["source_ip"]
            create_ip = CreateObject(driver)
            for i in range(len(ip_data)):
                create_ip_code = create_ip.create(ip_data[i], test_ip_object_element_position)
                if create_ip_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create ip object successfully.", flush=True)
                elif create_ip_code != 200:
                    result = "Fail to create ip."
                    break
        
        # 创建protocol_filed        
        if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
            protocol_field_data = test_data["condition"]["protocol_filed"]
            create_protocol_filed = CreateObject(driver)
            for x in range(len(protocol_field_data)):
                object_type = protocol_field_data[x]['object_type']
                if object_type == 'fqdn':
                    create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_fqdn_object_element_position)
                if create_protocol_filed_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_type), flush=True)
                elif create_protocol_filed_code != 200:
                    result = "Fail to create {}.".format(object_type)
                    break

        if "profile" in test_data  and len(test_data["profile"]) != 0:
            profile_data = test_data["profile"]
            dnsRecords_profile = CreateProfile(driver,test_dns_records_profile_element_position)
            for i in range(len(profile_data)):
                create_profile_code = dnsRecords_profile.create_dns_records_profile(profile_data[i],test_dns_records_profile_element_position,test_data["profile"][i]["name"])
                if create_profile_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create traffic dns records profile successfully.", flush=True)
                elif create_profile_code != 200:
                    result = "Fail to create Dns Records Profiles profile."
                    break

        # 创建rule
        if create_profile_code == 200:
            create_rule = CreateRule(driver)
            create_rule_code = create_rule.create(test_data, test_rule_element_position)
            if create_rule_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create security rule successfully.", flush=True)
            elif create_rule_code != 200:
                result = "Fail to create security rule."
            
        # 触发流量验证
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
            if search_rule_code == 200:
                # rule_id = search_rule.get_rule_id()
                test_data["rule_id"] = rule_id
                verify = Verification()
                verification_result = verify.verification(driver, parameter, test_data, [], test_rule_element_position)
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
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete security rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete security rule."
            else:
                result = result + " In addition, fail to search security rule."
        
        # 删除object
        if delete_rule_code == 200:
            # 删除ip
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
            # 删除protocol_filed
            for q in range(len(protocol_field_data)):
                search_protocol_filed = SearchObject(driver)
                object_type = protocol_field_data[q]['object_type']
                if object_type == 'fqdn':
                    search_protocol_filed_code, first_row_checkbox_element = search_protocol_filed.search(protocol_field_data[q]["name"], test_fqdn_object_element_position)
                if search_protocol_filed_code == 200:
                    delete_protocol_filed = DeleteObject(driver)
                    if object_type == 'fqdn':
                        delete_protocol_filed_code = delete_protocol_filed.delete(test_fqdn_object_element_position, first_row_checkbox_element, True)
                    if delete_protocol_filed_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(object_type), flush=True)
                    elif delete_protocol_filed_code != 200:
                        result = result + " In addition, fail to delete {} object.".format(object_type)
                        break
                else:
                    result = result + " In addition, fail to search {} object.".format(object_type)
                    break
        #删除profile
        delete_rule_code = 200
        profile_data = test_data["profile"]
        if delete_rule_code == 200:
            for x in range(len(profile_data)):
                search_dns_records_profile = SearchProfile(driver)
                profile_return_code,first_row_checkbox_element=search_dns_records_profile.search(profile_data[x]['name'],test_dns_records_profile_element_position)
                if profile_return_code == 200:
                    delete_mirror_profile = DeleteProfile(driver)
                    delete_profile_code = delete_mirror_profile.delete(test_dns_records_profile_element_position,first_row_checkbox_element,True)
                    if delete_profile_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns records profile successfully.", flush=True)
                    elif delete_profile_code != 200:
                        result = result + " In addition, fail to delete profile."
                        break
                else:
                    result = result + " In addition, fail to search profile."
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
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.65",
        "api_server": "http://192.168.44.72",
        "test_subcriber_id": "test",
        "script_type": "ui",
        "debug_flag": "local",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "root_path": "D:/python_engine/tsg_test",
        "path": "D:/python_engine/tsg_test/tests/api",
        "module_name": "security",
        "test_case_name": "allow_positive_ip_http_not_host"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """