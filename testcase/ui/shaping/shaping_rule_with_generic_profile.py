# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.ui.object.ip.ipObject import IpAddress
from src.ui.profile.shaping.shapingProfile import ShapingProfile
from src.ui.policy.policyRulePublicFunc import PolicyRulePublicFunc
from src.ui.element_position.policyElementPosition import *
from src.api.trafficVerification import *
from src.api.analysisResult import *
import src.ui.envInitialization

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
    # 脚本启动时间
    start_time = time.time()
    
    # 环境初始化
    driver = src.ui.envInitialization.my_driver()
    src.ui.envInitialization.setup()
    
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
        "ip":[
            {
                "name": "security_source_ip",
                "objectType": "create",
                "negate": False,
                "item": [
                    "1.1.1.1",
                    "1.1.1.1-1.1.1.2"
                ]
            }
        ],
        "application":[],
        "serverFqdn":[],
        "protocolFiled":[],
        "subAction": [],
        "profile": [
            {
                "name": "shaping_generic_profile",
                "profileType": "create",
                "type": "generic",
                "argument": "",
                "unit": "bps->",
                "incoming": "2000->",
                "outgoing": "500->"
            }
        ]
    }
    
    # 根据policy type添加定位库集合
    test_rule_element_position = {}
    if test_data["policyType"] == "shaping":
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
                    "policyRulePage_selectAction_posId": shapingRulePage_addCondition_srcIP_posXpath,
                    "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": shapingRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": shapingRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": shapingRulePage_closeSrcIP_posXpath,
                    "policyRulePage_priority_posId": shapingRulePage_priority_posId,
                    "policyRulePage_fairFactor_posId": shapingRulePage_fairFactor_posId,
                    "policyRulePage_addProfile_posXpath": shapingRulePage_addProfile_posXpath,
                    "policyRulePage_searchProfile_posXpath": shapingRulePage_searchProfile_posXpath,
                    "policyRulePage_selectProfile_posXpath": shapingRulePage_selectProfile_posXpath,
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
    ip_data = test_data["ip"]
    ip_address = IpAddress(driver)
    for i in range(len(ip_data)):
        ip_result = ip_address._create(ip_data[i])
    
    # 创建profile
    profile_data = test_data["profile"]
    shaping_profile = ShapingProfile(driver)
    for j in range(len(profile_data)):
        shaping_profile_result = shaping_profile._create(profile_data[j])
    
    # 创建rule
    if ip_result == 200 and shaping_profile_result == 200:
        shaping_rule = PolicyRulePublicFunc(driver)
        shaping_rule_result = shaping_rule._create(test_data, test_rule_element_position)
        
    # 触发流量验证
    if shaping_rule_result == 200:
        verify = TrafficVerification()
        verification_result = verify.traffic_verification(parameter, test_data, template_path, [])
        print("verification result: ", verification_result)
    
    # 分析验证结果，并返回给flask
    if len(verification_result) != 0:
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data, [], verification_result)
        print("analysis result: ", result)
    
    # 删除rule
    shaping_rule._search(test_data["ruleName"], test_rule_element_position)
    shaping_rule._delete(test_rule_element_position)
    
    # 删除ip
    for x in range(len(ip_data)):
        ip_address._search(ip_data[x]["name"])
        ip_address._delete()
    
    # 删除profile
    for y in range(len(profile_data)):
        shaping_profile._search(profile_data, Name=profile_data[y]["name"])
        shaping_profile._delete()
    
    # 清理环境
    src.ui.envInitialization.teardown()
    
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