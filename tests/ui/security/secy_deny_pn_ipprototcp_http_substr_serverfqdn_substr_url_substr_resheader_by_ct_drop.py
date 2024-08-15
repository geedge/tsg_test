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
from support.traffic_manager.verification import Verification
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import *
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
            "rule_name": "secy_deny_pn_ipprototcp_http_substr_serverfqdn_substr_url_substr_resheader_by_ct_drop",
            "rule_action": "deny",
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
                "source_geography": [],
                "destination_geography": [],
                "sub_id": [],
                "device": [
                    {
                        "name": "secy_pn",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "phone_number",
                                "item_value": '$' + parameter['test_phone_number'],
                            }
                        ]
                    }
                ],
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
                "ip_protocol":[
                    "TCP"
                ],
                "server_fqdn": [
                    {
                        "name": "secy_fqdn",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "fqdn",
                                "item_value": "open.node.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "secy_url",
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
                        "name": "secy_http_sig",
                        "object_type": "http_signature",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "response_header",
                                "item_key": "Content-Type",
                                "item_value": "TEXT",
                                "value": [
                                    "text/html"
                                ]
                            }
                        ],
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                    {
                        "type": "drop",
                        "send_tcp_rst": False,
                        "drop_packet": 0,
                        "send_icmp_unreachable": True
                    }
                ],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "timed out",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key":"imsi", "query_value":parameter['test_imsi']},
            {"query_field_key":"phone_number", "query_value": parameter['test_phone_number']},
            {"query_field_key": "ip_protocol", "query_value": "tcp"}],
            "traffic": {
                "protocol": "http",
                "type": "curl",
                "command": 'curl --connect-timeout 10 -m 10 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"helloSecurity\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" http://open.node.com:180/go'
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
                "name": "secy_deny_pn_ipprototcp_http_substr_serverfqdn_substr_url_substr_resheader_by_ct_drop"
            },
            {
                "type": "mobile_identity",
                "name": "secy_pn"
            },
            {
                "type": "fqdn",
                "name": "secy_fqdn"
            },
            {
                "type": "url",
                "name": "secy_url"
            },
            {
                "type": "http_signature",
                "name": "secy_http_sig"
            }
        ]
        
        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "security":
            test_phone_number_object_element_position = {
                "page_jump":{
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_mobileIdentify_posId
                },
                "create": {
                    "objectListPage_createButton_posId": mobile_identitiesObjectListPage_createButton_posId,
                    "objectListPage_dropDown_createButton_posId": mobile_identitiesObjectListPage_dropDown_createButton_posId,
                    "objectPage_inputName_posXpath": mobile_identitiesObjectPage_inputName_posXpath,
                    "objectPage_phnoeNumberType_posId": phoneNumberObjectPage_phoneNumberType_posId,
                    "objectPage_addItem_posId": phoneNumberObjectPage_addItem_posId,
                    "objectPage_inputItem_posXpath": phoneNumberObjectPage_inputItem_posXpath,
                    "objectPage_button_saveItem_posXpath": phoneNumberObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posId": phoneNumberObjectPage_okButton_posId,
                    "objectPage_okButton_warningYes_posXpath": phoneNumberObjectPage_okButton_warningYes_posXpath
                },
                "search": {
                    "objectListPage_searchLabel_posId": imsiObjectListPage_searchLabel_posId,
                    "objectListPage_searchLabel_selectName_posXpath": imsiObjectListPage_searchLabel_selectName_posXpath,
                    "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
                },
                "delete": {
                    "objectListPage_allSelect_posXpath": imsiObjectListPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posId": imsiObjectListPage_deleteButton_posId,
                    "objectListPage_deleteButton_warningYes_posXpath": imsiObjectListPage_deleteButton_warningYes_posXpath
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
                    "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                    "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                    "policyRulePage_addConditionImsi_posXpath": securityRulePage_addCondition_imsi_posXpath,
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    "policyRulePage_addImsi_posXpath": securityRulePage_addImsi_posXpath,
                    "policyRulePage_choosePhoneNumber_posXpath": securityRulePage_choosePhoneNumber_posXpath,
                    "policyRulePage_searchImsi_posXpath": policyRulePage_searchImsi_posXpath,
                    "policyRulePage_selectImsi_posXpath": policyRulePage_selectImsi_posXpath,
                    "policyRulePage_closeImsi_posXpath": policyRulePage_closeImsi_posXpath,
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
                    # res header
                    "policyRulePage_addConditionResponseHeader_posXpath": securityRulePage_addCondition_responseHeader_posXpath,
                    "policyRulePage_addResponseHeader_posXpath": manipulationRulePage_addResponseHeader_posXpath,
                    "policyRulePage_searchResponseHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
                    "policyRulePage_selectResponseHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
                    "policyRulePage_closeResponseHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
                    # ip protocol
                    "policyRulePage_addConditionIpProtocol_posXpath": policyRulePage_addCondition_IpProtocol_posXpath,
                    "policyRulePage_addIpProtocol_posXpath": policyRulePage_addIpProtocol_posXpath,
                    "policyRulePage_searchIpProtocol_posXpath": policyRulePage_searchIpProtocol_posXpath,
                    "policyRulePage_selectIpProtocol_posXpath": policyRulePage_selectIpProtocol_posXpath,
                    "policyRulePage_closeIpProtocol_posXpath": policyRulePage_closeIpProtocol_posXpath,
                    # 关闭add condition
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                    "policyRulePage_subAction_drop_posXpath": securityRulePage_subAction_drop_posXpath,
                    "policyRulePage_subAction_drop_dropPkt_posXpath": securityRulePage_subAction_drop_dropPkt_posXpath,
                    "policyRulePage_subAction_drop_sendTcpRst_posXpath": securityRulePage_subAction_drop_sendTcpRst_posXpath,
                    "policyRulePage_subAction_drop_sendIcmp_posXpath": securityRulePage_subAction_drop_sendIcmp_posXpath,
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
        
        # 创建phone number
        if "device" in test_data["condition"] and len(test_data["condition"]["device"]) != 0:
            device_data = test_data["condition"]["device"]
            create_device = CreateObject(driver)
            for i in range(len(device_data)):
                object_sub_type = device_data[i]['item'][0]['item_type']
                if object_sub_type == 'phone_number':
                    create_device_code = create_device.create(device_data[i], test_phone_number_object_element_position)
                if create_device_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_sub_type), flush=True)
                elif create_device_code != 200:
                    result = "Fail to create {} object.".format(object_sub_type)
                    break
        if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
            fqdn_data = test_data["condition"]["server_fqdn"]
            create_fqdn = CreateObject(driver)
            for i in range(len(fqdn_data)):
                create_fqdn_code = create_fqdn.create(fqdn_data[i], test_fqdn_object_element_position)
                if create_fqdn_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create fqdn object successfully.", flush=True)
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
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_type), flush=True)
                elif create_protocol_filed_code != 200:
                    result = "Fail to create {}.".format(object_type)
                    break
        # 创建rule
        if create_device_code == 200:
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
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete security rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete security rule."
            else:
                result = result + " In addition, fail to search security rule."
        
        # 删除object
        if delete_rule_code == 200:
            # 删除device相关的object
            for y in range(len(device_data)):
                search_device = SearchObject(driver)
                object_sub_type = device_data[i]['item'][0]['item_type']
                if object_sub_type == 'phone_number':
                    search_device_code, first_row_checkbox_element = search_device.search(device_data[y]["name"], test_phone_number_object_element_position)
                if search_device_code == 200:
                    delete_device = DeleteObject(driver)
                    if object_sub_type == 'phone_number':
                        delete_device_code = delete_device.delete(test_phone_number_object_element_position, first_row_checkbox_element, True)
                    if delete_device_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(object_sub_type), flush=True)
                    elif delete_device_code != 200:
                        result = result + " In addition, fail to delete {} object.".format(object_sub_type)
                        break
                else:
                    result = result + " In addition, fail to search {} object.".format(object_sub_type)
            # 删除fqdn
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
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(object_type), flush=True)
                    elif delete_protocol_filed_code != 200:
                        result = result + " In addition, fail to delete {} object.".format(object_type)
                        break
                else:
                    result = result + " In addition, fail to search {} object.".format(object_type)
                    break
                # 脚本结束时间和耗时
        
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
        "test_pc_ip": "192.168.64.91",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
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