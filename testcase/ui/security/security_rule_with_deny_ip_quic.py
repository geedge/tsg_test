# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.ui.object.ip.ipObject import IpAddress
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
        "policyType": "security",
        "ruleName": "security_rule_with_deny_ip_quic",
        "ruleAction": "deny",
        "ruleType": "create",
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
        "application":[
            {
                "name": "http",
                "negate": False
            }
        ],
        "serverFqdn":[
            {
                "type": "fqdn",
                "name": "www.baidu.com"
            }
        ],
        "protocolFiled":[
            {
                "type": "url",
                "name": "youtube"
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
        ],
        "profile":[
        ],
        "hope_return": "POST",
        "counters_1": {"hits": 0},
        "log_query_param_1": [],
        "command": "curl -kv https://www.google.com"
    }
    
    # 根据policy type添加定位库集合
    test_rule_element_position = {}
    if test_data["policyType"] == "security":
        test_rule_element_position = {
            "page_jump":{
                    'mainPage_navigationBar_logo_posCss': mainPage_navigationBar_logo_posCss,
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
                    "policyRulePage_selectSrcIP_posXpath" :securityRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
                    "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                    "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                    "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                    "policyRulePage_addCondition_serverFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addCondition_url_posXpath": securityRulePage_addCondition_url_posXpath,
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
                    "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": securityRulePage_okButton_yes_posId,
                    "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath
            },
            "search": {
                    "policyRuleListPage_searchLable_posId": securityRuleListPage_searchLable_posId,
                    "policyRuleListPage_searchLable_dropDown_item_posXpath": securityRuleListPage_searchLable_input_itemContent_posXpath,
                    "policyRuleListPage_searchLable_input_itemContent_posXpath": securityRuleListPage_searchLable_searchButton_posId,
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
    ip_data = test_data["ip"]
    if len(ip_data) != 0:
        ip_address = IpAddress(driver)
        for i in range(len(ip_data)):
            ip_result = ip_address._create(ip_data[i])
    
    # 创建rule
    if ip_result == 200:
        security_rule = PolicyRulePublicFunc(driver)
        security_rule_result = security_rule._create(test_data, test_rule_element_position)
        
    # 触发流量验证
    if security_rule_result == 200:
        verify = TrafficVerification()
        verification_result = verify.traffic_verification(parameter, test_data, template_path, [])
        print("verification result: ", verification_result)
    
    # 分析验证结果，并返回给flask
    if len(verification_result) != 0:
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data, [], verification_result)
        print("analysis result: ", result)
    
    # 删除rule
    security_rule._search(test_data["ruleName"], test_rule_element_position)
    security_rule._delete(test_rule_element_position)
    
    # 删除ip
    for j in range(len(ip_data)):
        ip_address._search(ip_data[j]["name"])
        ip_address._delete()
    
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