# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
# from src.ui.object.ip.ipObject import IpAddress
from support.ui_utils.object.createObject import CreateObject
from support.ui_utils.object.searchObject import SearchObject
from support.ui_utils.object.deleteObject import DeleteObject
from support.ui_utils.profile.shaping.shapingProfile import ShapingProfile
from support.ui_utils.policy.createRule import CreateRule
from support.ui_utils.policy.searchRule import SearchRule
from support.ui_utils.policy.deleteRule import DeleteRule
from support.ui_utils.element_position.policyElementPosition import *
from support.ui_utils.element_position.objectElementPosition import *
from support.api_utils.trafficVerification import *
from support.api_utils.analysisResult import *
import support.ui_utils.envInitialization

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
    # 脚本启动时间
    start_time = time.time()
    
    # 环境初始化
    driver = support.ui_utils.envInitialization.my_driver()
    support.ui_utils.envInitialization.setup()
    
    # 测试数据
    test_data = {
        "isMultiPriority": False,
        "ruleNum": 1,
        "policyType": "shaping",
        "ruleName": "shaping_rule_with_generic_profile",
        "ruleAction": "shaping",
        "ruleType": "create",
        "rulePriority": 6,
        "ruleFairFactor": 2,
        "condition": {
            "sourceIP": [
                {
                    "name": "shaping_source_ip",
                    "objectType": "ip",
                    "negate": False,
                    "item": [
                        "1.1.1.1",
                        "1.1.1.1-1.1.1.2"
                    ]
                }
            ],
            "sourcePort": [],
            "destinationIP": [],
            "destinationPort": [],
            "internalIP": [],
            "internalPort": [],
            "externalIP": [],
            "externalPort": [],
            "geography": [],
            "subId": [],
            "device": [],
            "tunnel": [],
            "tunnelLevel": [],
            "flag": [],
            "application": [],
            "serverFqdn": [],
            "protocolFiled": [],
            "subActionOverride": False,
            "subAction": [],
            "packetCapture": [],
        },
        "multiProfile": True,
        "profile": [
            {
                "name": "shaping_generic_profile",
                "profileType": "create",
                "type": "generic",
                "argument": "",
                "unit": "Mbps->",
                "incoming": "10->",
                "outgoing": "1->"
            },
            {
                "name": "shaping_generic_2_profile",
                "profileType": "create",
                "type": "generic",
                "argument": "",
                "unit": "bps->",
                "incoming": "2000->",
                "outgoing": "500->"
            }
        ]
    }
    
    # 添加定位库集合
    test_rule_element_position = {}
    if test_data["policyType"] == "shaping":
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
                "objectListPage_dropDown_createIpButton_posId": ipObjectListPage_dropDown_createIpButton_posId,
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
        test_rule_element_position = {
            "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_shaping_posId
            },
            "create": {
                    "policyRuleListPage_createButton_posId": shapingRuleListPage_createButton_posId,
                    "policyRulePage_inputName_posXpath": shapingRulePage_inputName_posXpath,
                    "policyRulePage_addSrcIP_posXpath": shapingRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": shapingRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": shapingRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": shapingRulePage_closeSrcIP_posXpath,
                    "policyRulePage_priority_posId": shapingRulePage_priority_posId,
                    "policyRulePage_fairFactor_posId": shapingRulePage_fairFactor_posId,
                    "policyRulePage_addProfile_posXpath": shapingRulePage_addProfile_posXpath,
                    "policyRulePage_searchProfile_posXpath": shapingRulePage_searchProfile_posXpath,
                    "policyRulePage_selectProfile_posXpath": shapingRulePage_selectProfile_posXpath,
                    "policyRulePage_closeProfile_posXpath": shapingRulePage_closeProfile_posXpath,
                    "policyRulePage_addProfile_plus_posXpath": shapingRulePage_addProfile_plus_posXpath,
                    "policyRulePage_enable_posXpath": shapingRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": shapingRulePage_okButton_yes_posId,
                    "policyRulePage_okButton_warningYes_posXpath": shapingRulePage_okButton_warningYes_posXpath
            },
            "search": {
                    "policyRuleListPage_searchLable_posId": shapingRuleListPage_searchLable_posId,
                    "policyRuleListPage_searchLable_dropDown_item_posXpath": shapingRuleListPage_searchLable_dropDown_item_posXpath,
                    "policyRuleListPage_searchLable_input_itemContent_posXpath": shapingRuleListPage_searchLable_input_itemContent_posXpath,
                    "policyRuleListPage_searchLable_searchButton_posId": shapingRuleListPage_searchLable_searchButton_posId,
                    "policyRuleListPage_tableTbody_posXpath": shapingRuleListPage_tableTbody_posXpath
            },
            "delete": {
                    "policyRuleListPage_allSelect_posXpath": shapingRuleListpage_allButton_posXpath,
                    "policyRuleListPage_deleteButton_posId": shapingRuleListpage_deleteButton_posId,
                    "policyRuleListPage_okButton_warningYes_posXpath": shapingRuleListpage_okButton_warningYes_posXpath,
                    "policyRuleListPage_okButton_warningNo_posXpath": shapingRuleListpage_okButton_warningNo_posXpath
            }
        }
        
    # 添加测试过程中涉及的template
    template_path = {}
    template_path["trex_workpath"] = "/opt/trex/v3.03"
    template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"
    
    # 创建object
    if "sourceIP" in test_data["condition"] and len(ip_data) != 0:
        ip_data = test_data["condition"]["sourceIP"]
        create_ip = CreateObject(driver)
        for i in range(len(ip_data)):
            create_ip_code = create_ip.create(ip_data[i], test_ip_object_element_position)
            if create_ip_code != 200:
                result = "Fail to create ip object."
                break
    
    # 创建profile
    profile_data = test_data["profile"]
    shaping_profile = ShapingProfile(driver)
    for j in range(len(profile_data)):
        create_profile_code = shaping_profile.create(profile_data[j])
        if create_profile_code != 200:
                result = "Fail to create shaping profile."
                break
    
    # 创建rule
    if create_ip_code == 200 and create_profile_code == 200:
        create_rule = CreateRule(driver)
        create_rule_code = create_rule.create(test_data, test_rule_element_position)
        if create_rule_code != 200:
            result = "Fail to create shaping rule."
        
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
            delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, False)
            if delete_rule_code != 200:
                result = result + " In addition, fail to delete shaping rule."
        else:
            result = result + " In addition, fail to search shaping rule."
    
    # 删除condition
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
        # 删除profile
        for y in range(len(profile_data)):
            shaping_profile.search(profile_data, Name=profile_data[y]["name"])
            shaping_profile.delete()
    
    # 清理环境
    support.ui_utils.envInitialization.teardown()
    
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
      "module_name": "shaping",
      "test_case_name": "shaping_rule_with_generic_profile"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """