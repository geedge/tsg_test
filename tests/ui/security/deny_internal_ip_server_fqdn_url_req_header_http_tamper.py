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
from support.traffic_replay.traffic_verification import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import *
import support.ui_utils.env

from support.report import *

def run(parameter):
    try:
        print("Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        result = ""
        
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
            "rule_name": "security_rule_deny_internal_ip_server_fqdn_url_req_header_http_reset",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                "internal_ip": [
                    {
                        "name": "security_internal_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter["test_pc_ip"],
                            }
                        ]
                    }
                ],
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
                        "name": "http", #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                    {
                        "name": "test_node",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "items": [
                            {
                                "item_value": "open.node.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "security_url",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                "item_value": "open.node->"
                            }
                        ],
                    },
                    {
                        "name": "security_http_signature",
                        "object_type": "http_signature",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "request_header",
                                "item_key": "User-Agent",
                                "item_value": "TEXT",
                                "value": [
                                    "curl"
                                ]
                            }
                        ],
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                    {
                        "type": "tamper"
                    }
                ],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "timed out",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key":"http_host", "query_value": "open.node.com"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv --connect-timeout 10 -m 10 http://open.node.com:180"
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
                "type": "security",
                "name": "security_rule_deny_internal_ip_server_fqdn_http_block_403_text"
            },
            {
                "type": "ip",
                "name": "security_internal_ip"
            },
            {
                "type": "fqdn",
                "name": "test_node"
            },
            {
                "type": "url",
                "name": "security_url"
            },
            {
                "type": "http_signature",
                "name": "security_http_signature"
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

            test_url_object_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_url_posId
                },
                "create": {
                    "objectListPage_createButton_posId": urlObjectListPage_createButton_posId,
                    "objectListPage_dropDown_createButton_posId": urlObjectListPage_dropDown_createButton_posId,
                    "objectPage_inputName_posXpath": urlObjectPage_inputName_posXpath,
                    "objectPage_addItem_posId": urlObjectPage_addItem_posId,
                    # item简单定位
                    "objectPage_inputItem_posXpath": urlObjectPage_inputItem_posXpath,
                    "objectPage_button_saveItem_posXpath": urlObjectPage_saveItem_posXpath,
                    "objectPage_okButton_posId": urlObjectPage_okButton_posId,
                    "objectPage_okButton_warningYes_posXpath": urlObjectPage_okButton_warningYes_posXpath
                },
                "search": {
                    "objectListPage_searchLabel_posId": urlObjectPage_searchLabel_posId,
                    "objectListPage_searchLabel_selectName_posXpath": urlObjectListPage_searchLabel_selectName_posXpath,
                    "objectListPage_tableTbody_posXpath": urlObjectPage_tableTbody_posXpath
                },
                "delete": {
                    "objectListPage_allSelect_posXpath": urlObjectPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posId": urlObjectListPage_deleteButton_posId,
                    "objectListPage_deleteButton_warningYes_posXpath": urlObjectListPage_deleteButton_warningYes_posXpath
                }
            }
            test_http_signature_object_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_httpSignature_posId
                },
                "create": {
                    "objectListPage_createButton_posId": httpSignatureObjectListPage_createButton_posId,
                    "objectListPage_dropDown_createButton_posId": httpSignatureObjectListPage_dropDown_createButton_posId,
                    "objectPage_inputName_posXpath": httpSignatureObjectPage_inputName_posXpath,
                    "objectPage_addItem_posId": httpSignatureObjectPage_addItem_posId,
                    "objectPage_item_key_dropDown_posXpath": httpSignatureObjectPage_item_key_dropDown_posXpath,
                    "objectPage_item_key_dropDown_select_posXpath": httpSignatureObjectPage_item_key_dropDown_select_posXpath,
                    "objectPage_item_value_select_posXpath": httpSignatureObjectPage_item_value_select_posXpath,
                    "objectPage_inputItem_posXpath": httpSignatureObjectPage_inputItem_posXpath,
                    "objectPage_item_value_plus_posXpath": httpSignatureObjectPage_item_value_plus_posXpath,
                    "objectPage_button_saveItem_posXpath": httpSignatureObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posId": httpSignatureObjectPage_okButton_posId,
                    "objectPage_okButton_warningYes_posXpath": httpSignatureObjectPage_okButton_warningYes_posXpath
                },
                "search": {
                    "objectListPage_searchLabel_posId": httpSignatureObjectListPage_searchLabel_posId,
                    "objectListPage_searchLabel_selectName_posXpath": httpSignatureObjectListPage_searchLabel_selectName_posXpath,
                    "objectListPage_tableTbody_posXpath": httpSignatureObjectListPage_tableTbody_posXpath
                },
                "delete": {
                    "objectListPage_allSelect_posXpath": httpSignatureObjectListPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posId": httpSignatureObjectListPage_deleteButton_posId,
                    "objectListPage_deleteButton_warningYes_posXpath": httpSignatureObjectListPage_deleteButton_warningYes_posXpath
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
                    "policyRulePage_addConditionInternalIP_posXpath": securityRulePage_addCondition_internalIP_posXpath,
                    "policyRulePage_addInternalIP_posXpath": securityRulePage_addInternalIP_posXpath,
                    "policyRulePage_searchInternalIP_posXpath": securityRulePage_searchInternalIP_posXpath,
                    "policyRulePage_selectInternalIP_posXpath": securityRulePage_selectInternalIP_posXpath,
                    "policyRulePage_closeInternalIP_posXpath": securityRulePage_closeInternalIP_posXpath,
                    "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                    "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    # fqdn
                    "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                    "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                    "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                    "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
                    # url
                    "policyRulePage_addConditionUrl_posXpath": securityRulePage_addCondition_url_posXpath,
                    "policyRulePage_addUrl_posXpath": policyRulePage_addUrl_posXpath,
                    "policyRulePage_searchUrl_posXpath": policyRulePage_searchUrl_posXpath,
                    "policyRulePage_selectUrl_posXpath": policyRulePage_selectUrl_posXpath,
                    "policyRulePage_closeUrl_posXpath": policyRulePage_closeUrl_posXpath,
                    # req header
                    "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
                    "policyRulePage_addRequestHeader_posXpath": manipulationRulePage_addRequestHeader_posXpath,
                    "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
                    "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
                    "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                    # sub action
                    "policyRulePage_subAction_tamper_posXpath": securityRulePage_subAction_tamper_posXpath,
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
        if "internal_ip" in test_data["condition"] and len(test_data["condition"]["internal_ip"]) != 0:
            ip_data = test_data["condition"]["internal_ip"]
            create_port = CreateObject(driver)
            for i in range(len(ip_data)):
                create_port_code = create_port.create(ip_data[i], test_ip_object_element_position)
                if create_port_code == 200:
                    print("Create ip object successfully.", flush=True)
                elif create_port_code != 200:
                    result = "Fail to create ip object."
                    break
        if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
            fqdn_data = test_data["condition"]["server_fqdn"]
            create_fqdn = CreateObject(driver)
            for i in range(len(fqdn_data)):
                create_fqdn_code = create_fqdn.create(fqdn_data[i], test_fqdn_object_element_position)
                if create_fqdn_code == 200:
                    print("Create fqdn object successfully.", flush=True)
                elif create_fqdn_code != 200:
                    result = "Fail to create fqdn."
                    break
        # 创建url+req header       
        if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
            protocol_field_data = test_data["condition"]["protocol_filed"]
            create_protocol_filed = CreateObject(driver)
            for x in range(len(protocol_field_data)):
                object_type = protocol_field_data[x]['object_type']
                if object_type == 'url':
                    create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_url_object_element_position)
                elif object_type == 'http_signature':
                    create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_http_signature_object_element_position)
                if create_protocol_filed_code == 200:
                    print("Create {} object successfully.".format(object_type), flush=True)
                elif create_protocol_filed_code != 200:
                    result = "Fail to create {}.".format(object_type)
                    break
        # 创建rule
        if create_port_code == 200:
            create_rule = CreateRule(driver)
            create_rule_code = create_rule.create(test_data, test_rule_element_position)
            if create_rule_code == 200:
                print("Create security rule successfully.", flush=True)
            elif create_rule_code != 200:
                result = "Fail to create security rule."
            
        # 触发流量验证
        if create_rule_code == 200:
            edit_rule = EditRule(driver)
            edit_rule_code, rule_id = edit_rule.edit(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
            if edit_rule_code == 200:
                # rule_id = search_rule.get_rule_id()
                test_data["rule_id"] = rule_id
                verify = TrafficVerification()
                verification_result = verify.traffic_verification(driver, parameter, test_data, [])
                if len(verification_result) == 4:
                    driver = verification_result[3]
                elif len(verification_result) == 5:
                    driver = verification_result[4]
        
        # 分析验证结果，并返回给flask
        if len(verification_result) != 0:
            analysis = AnalysisResult()
            result = analysis.analysis_result(test_data, [], verification_result)
            if len(result) == 0:
                print("The test case is passed.", flush=True)
            elif len(result) != 0:
                print("The test case is failed. The failure reason is: ", result, flush=True)
        
        # 删除rule
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print("Delete security rule successfully.", flush=True)
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
                        print("Delete ip object successfully.", flush=True)
                    elif delete_ip_code != 200:
                        result = result + " In addition, fail to delete ip object."
                        break
                else:
                    result = result + " In addition, fail to search ip object."
                    break
        # 删除fqdn
            for x in range(len(fqdn_data)):
                search_fqdn = SearchObject(driver)
                search_fqdn_code, first_row_checkbox_element = search_fqdn.search(fqdn_data[x]["name"], test_fqdn_object_element_position)
                if search_fqdn_code == 200:
                    delete_fqdn = DeleteObject(driver)
                    delete_fqdn_code = delete_fqdn.delete(test_fqdn_object_element_position, first_row_checkbox_element, True)
                    if delete_fqdn_code == 200:
                        print("Delete fqdn object successfully.", flush=True)
                    elif delete_fqdn_code != 200:
                        result = result + " In addition, fail to delete fqdn object."
                        break
                else:
                    result = result + " In addition, fail to search fqdn object."
                    break
        
        # 删除protocol_filed
            for q in range(len(protocol_field_data)):
                search_protocol_filed = SearchObject(driver)
                object_type = protocol_field_data[q]['object_type']
                if object_type == 'url':
                    search_protocol_filed_code, first_row_checkbox_element = search_protocol_filed.search(protocol_field_data[q]["name"], test_url_object_element_position)
                elif object_type == 'http_signature':
                    search_protocol_filed_code, first_row_checkbox_element = search_protocol_filed.search(protocol_field_data[q]["name"], test_http_signature_object_element_position)
                if search_protocol_filed_code == 200:
                    delete_protocol_filed = DeleteObject(driver)
                    if object_type == 'url':
                        delete_protocol_filed_code = delete_protocol_filed.delete(test_url_object_element_position, first_row_checkbox_element, True)
                    elif object_type == 'http_signature':
                        delete_protocol_filed_code = delete_protocol_filed.delete(test_http_signature_object_element_position, first_row_checkbox_element, True)
                    if delete_protocol_filed_code == 200:
                        print("Delete {} object successfully.".format(object_type), flush=True)
                    elif delete_protocol_filed_code != 200:
                        result = result + " In addition, fail to delete {} object.".format(object_type)
                        break
                else:
                    result = result + " In addition, fail to search {} object.".format(object_type)
                    break
        
        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print("Duration of running the test case: ", duration, flush=True)
        
        print("Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        print("Error: ", e, flush=True)
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
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.91",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 11,
        "is_log": 1,
        "root_path": "D:/python_script/tsg_test",
        "path": "D:/python_script/tsg_test/tests/ui",
        "module_name": "security",
        "test_case_name": "deny_srcip_fqdn_drop_rst_icmp"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """