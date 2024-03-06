# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
# from src.ui.object.ip.ipObject import IpAddress
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.traffic_replay.traffic_verification import *
from support.api_utils.analysis_result import *
import support.ui_utils.env_initialization

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
    # 脚本启动时间
    start_time = time.time()
    
    # 环境初始化
    driver = support.ui_utils.env_initialization.my_driver()
    support.ui_utils.env_initialization.setup()
    
    # 测试数据
    test_data = {
        "isMultiPriority": False,
        "ruleNum": 1,
        "policyType": "security",
        "ruleName": "security_rule_with_deny_ip_quic",
        "ruleAction": "deny",
        "ruleType": "create",
        "condition": {
            "sourceIP": [
                {
                    "name": "security_source_ip",
                    "objectType": "ip",
                    "selectType": False,
                    "negate": False,
                    "item": [
                        "1.1.1.1",
                        "1.1.1.1-1.1.1.2"
                    ]
                }
            ],
            "sourcePort": [
                {
                    "name": "security_source_port",
                    "objectType": "port",
                    "selectType": False,
                    "negate": False,
                    "item": [
                        "1000-1110",
                        "2222"
                    ]
                }
            ],
            "destinationIP": [],
            "destinationPort": [],
            "internalIP": [],
            "internalPort": [],
            "externalIP": [],
            "externalPort": [],
            "sourceGeography": [],
            "destinationGeography": [],
            "subId": [],
            "device": [],
            "tunnel": [],
            "tunnelLevel": [],
            "flag": [],
            "application": [
                {
                    "name": "http",
                    "negate": False
                }
            ],
            "serverFqdn": [
                {
                    "name": "www.baidu.com", # 需要新建，不能使用已存在的object，保证自动化的统一性，这里只是示例
                    "objectType": "fqdn",
                    "selectType": False,
                    "negate": False,
                    "plus": False,
                    "item": [
                        "*google.com"
                    ]
                }
            ],
            "protocolFiled": [
                {
                    "name": "youtube", # 需要新建，不能使用已存在的object，保证自动化的统一性，这里只是示例
                    "fieldType": "url",
                    "objectType": "url",
                    "selectType": False,
                    "negate": False,
                    "plus": False,
                    "item": [
                        "youtube.com", 
                        "google.com"
                    ]
                }
            ],
            "subActionOverride": True,
            "subAction": [
                {
                    "type": "drop",
                    "dropPacket": 1,
                    "sendTcpRst": False,
                    "sendIcmpUnreachable": True
                }
                # {
                #     "type": "rate_limit",
                #     "rateUnit": "kbps",
                #     "rateValue": 200
                # }
                # {
                #     "type": "block",
                #     "code": 404,
                #     "contentType": "TEXT",
                #     "content": "block_change_response_profile"
                # }
                # {
                #     "type": "redirect",
                #     "redirectUrl": "www.google.com"
                # }
            ],
            "packetCapture": [
                {
                    "enable": True,
                    "captureDepth": 3000
                }
            ]
        },
        "profile": [
        ],
        "expectedReturn": "POST",
        "counters_1": {"hits": 0},
        "log_query_param_1": [],
        "command": "curl -kv https://www.google.com"
    }
    
    # 添加定位库集合
    test_rule_element_position = {}
    if test_data["policyType"] == "security":
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
        test_port_object_element_position = {
            "page_jump":{
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_port_posId
            },
            "create": {
                "objectListPage_createButton_posId": portObjectListPage_createButton_posId,
                "objectListPage_dropDown_createPortButton_posId": portObjectListPage_dropDown_createButton_posId,
                "objectPage_inputName_posXpath": portObjectPage_inputName_posXpath,
                "objectPage_addItem_posId": portObjectPage_addItem_posId,
                "objectPage_inputItem_posXpath": portObjectPage_inputItem_posXpath,
                "objectPage_button_saveItem_posXpath": portObjectPage_button_saveItem_posXpath,
                "objectPage_okButton_posId": portObjectPage_okButton_posId,
                "objectPage_okButton_warningYes_posXpath": portObjectPage_okButton_warningYes_posXpath
            },
            "search": {
                "objectListPage_searchLabel_posId": portObjectListPage_searchLabel_posId,
                "objectListPage_searchLabel_selectName_posXpath": portObjectListPage_searchLabel_selectName_posXpath,
                "objectListPage_tableTbody_posXpath": portObjectListPage_tableTbody_posXpath
            },
            "delete": {
                "objectListPage_allSelect_posXpath": portObjectListPage_allSelect_posXpath,
                "objectListPage_deleteButton_posId": portObjectListPage_deleteButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": portObjectListPage_deleteButton_warningYes_posXpath
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
                "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                "policyRulePage_searchSrcIP_posXpath": securityRulePage_searchSrcIP_posXpath,
                "policyRulePage_selectSrcIP_posXpath": securityRulePage_selectSrcIP_posXpath,
                "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
                "policyRulePage_addConditionSrcPort_posXpath": securityRulePage_addCondition_srcPort_posXpath,
                "policyRulePage_addSrcPort_posXpath": securityRulePage_addSrcPort_posXpath,
                "policyRulePage_searchSrcPort_posXpath": securityRulePage_searchSrcPort_posXpath,
                "policyRulePage_selectSrcPort_posXpath": securityRulePage_selectSrcPort_posXpath,
                "policyRulePage_closeSrcPort_posXpath": securityRulePage_closeSrcPort_posXpath,
                "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                "policyRulePage_addConditionUrl_posXpath": securityRulePage_addCondition_url_posXpath,
                "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
                "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                "policyRulePage_addUrl_posXpath": securityRulePage_addUrl_posXpath,
                "policyRulePage_searchUrl_posXpath": securityRulePage_searchUrl_posXpath,
                "policyRulePage_selectUrl_posXpath": securityRulePage_selectUrl_posXpath,
                "policyRulePage_closeUrl_posXpath": securityRulePage_closeUrl_posXpath,
                "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                "policyRulePage_subAction_drop_posXpath": securityRulePage_subAction_drop_posXpath,
                "policyRulePage_subAction_drop_dropPkt_posXpath": securityRulePage_subAction_drop_dropPkt_posXpath,
                "policyRulePage_subAction_drop_sendTcpRst_posXpath": securityRulePage_subAction_drop_sendTcpRst_posXpath,
                "policyRulePage_subAction_drop_sendIcmp_posXpath": securityRulePage_subAction_drop_sendIcmp_posXpath,
                "policyRulePage_subAction_block_posXpath": securityRulePage_subAction_block_posXpath,
                "policyRulePage_subAction_block_responseCode_posXpath": securityRulePage_subAction_block_responseCode_posXpath,
                "policyRulePage_subAction_block_responseCode_change_posXpath": securityRulePage_subAction_block_responseCode_change_posXpath,
                "policyRulePage_subAction_block_responseContent_posXpath": securityRulePage_subAction_block_responseContent_posXpath,
                "policyRulePage_subAction_block_responseContent_change_posXpath": securityRulePage_subAction_block_responseContent_change_posXpath,
                "policyRulePage_subAction_block_responseContent_text_posId": securityRulePage_subAction_block_responseContent_text_posId,
                "policyRulePage_subAction_block_responseContent_clickProfile_posXpath": securityRulePage_subAction_block_responseContent_clickProfile_posXpath,
                "policyRulePage_subAction_block_responseContent_searchProfile_posXpath": securityRulePage_subAction_block_responseContent_searchProfile_posXpath,
                "policyRulePage_subAction_block_responseContent_selectProfile_posId": securityRulePage_subAction_block_responseContent_selectProfile_posId,
                "policyRulePage_packetCapture_posXpath": securityRulePage_packetCapture_posXpath,
                "policyRulePage_packetCapture_depth_posXpath": securityRulePage_packetCapture_depth_posXpath,
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
    
    # 添加测试过程中涉及的template
    template_path = {}
    template_path["trex_workpath"] = "/opt/trex/v3.03"
    template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"
    
    # 创建object
    if "sourceIP" in test_data["condition"] and len(test_data["condition"]["sourceIP"]) != 0:
        ip_data = test_data["condition"]["sourceIP"]
        create_ip = CreateObject(driver)
        for i in range(len(ip_data)):
            create_ip_code = create_ip.create(ip_data[i], test_ip_object_element_position)
            if create_ip_code != 200:
                result = "Fail to create ip object."
                break
    if "sourcePort" in test_data["condition"] and len(test_data["condition"]["sourcePort"]) != 0:
        port_data = test_data["condition"]["sourcePort"]
        create_port = CreateObject(driver)
        for j in range(len(port_data)):
            create_port_code = create_port.create(port_data[j], test_port_object_element_position)
            if create_port_code != 200:
                result = "Fail to create port object."
                break
    
    # 创建rule
    if create_ip_code == 200 and create_port_code == 200:
        create_rule = CreateRule(driver)
        create_rule_code = create_rule.create(test_data, test_rule_element_position)
        if create_rule_code != 200:
            result = "Fail to create security rule."
        
    # 触发流量验证
    if create_rule_code == 200:
        verify = TrafficVerification()
        verification_result = verify.traffic_verification(parameter, test_data, template_path, [])
        print("verification result: ", verification_result)
    
    # 分析验证结果，并返回给flask
    if len(verification_result) != 0:
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data, [], verification_result)
        print("analysis result: ", result)
    
    # 删除rule
    if create_rule_code == 200:
        search_rule = SearchRule(driver)
        search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policyType"], test_data["ruleName"], test_rule_element_position)
        if search_rule_code == 200:
            delete_rule = DeleteRule(driver)
            delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
            if delete_rule_code != 200:
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
                if delete_ip_code != 200:
                    result = result + " In addition, fail to delete ip object."
                    break
            else:
               result = result + " In addition, fail to search ip object."
               break
        # 删除port
        for y in range(len(port_data)):
            search_port = SearchObject(driver)
            search_port_code, first_row_checkbox_element = search_port.search(port_data[y]["name"], test_port_object_element_position)
            if search_port_code == 200:
                delete_port = DeleteObject(driver)
                delete_port_code = delete_port.delete(test_port_object_element_position, first_row_checkbox_element, True)
                if delete_port_code != 200:
                    result = result + " In addition, fail to delete port object."
                    break
            else:
               result = result + " In addition, fail to search port object."
               break
    
    # 清理环境
    support.ui_utils.env_initialization.teardown()
    
    # 脚本结束时间和耗时
    end_time = time.time()
    duration = end_time - start_time
    print("duration: ", duration)
    
    print("Finish test case: " + parameter["test_case_name"])
    return result

if __name__ == '__main__':
    parameter = {
      "username": "zhaokun",
      "password": "zhaokun1",
      "test_pc_ip": "192.168.64.73",
      "api_server": "http://192.168.44.72",
      "is_log": 0,
      "env": "tsgx",
      "vsys_id": 6,
      "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
      "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
      "module_name": "security",
      "test_case_name": "security_rule_with_deny_ip_quic"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """