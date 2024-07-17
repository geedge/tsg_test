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
from support.traffic_manager.api_verification import *
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
            "rule_name": "security_rule_allow_external_ip_mail",
            "rule_action": "allow",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [
                    {
                        "name": "security_external_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "192.168.40.206",
                            }
                        ]
                    }
                ],
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
                        "name": "mail", #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "Ok",
            "counters": {"hits": "many"},
            "log_query_param": [{"query_field_key":"decoded_as", "query_value": "MAIL"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv --connect-timeout 25 -m 25 --url 'smtp://192.168.40.206' --mail-from 'hbn@163.com'  --mail-rcpt 'autotest@163.com'  --upload-file '/app/support/traffic_replay/mail_file/subjectEnglish.txt' --user 'hbn@163.com:111111'"
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
                "name": "security_rule_allow_external_ip_ftp"
            },
            {
                "type": "ip",
                "name": "security_external_ip"
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
                    "policyRulePage_selectAction_posId": securityRulePage_selectAllow_posId,
                    "policyRulePage_addConditionExternalIP_posXpath": securityRulePage_addCondition_externalIP_posXpath,
                    "policyRulePage_addExternalIP_posXpath": securityRulePage_addExternalIP_posXpath,
                    "policyRulePage_searchExternalIP_posXpath": securityRulePage_searchExternalIP_posXpath,
                    "policyRulePage_selectExternalIP_posXpath": securityRulePage_selectExternalIP_posXpath,
                    "policyRulePage_closeExternalIP_posXpath": securityRulePage_closeExternalIP_posXpath,
                    "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                    "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                    "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                    "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                    "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                    "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
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
        
        # 创建object
        if "external_ip" in test_data["condition"] and len(test_data["condition"]["external_ip"]) != 0:
            ip_data = test_data["condition"]["external_ip"]
            create_port = CreateObject(driver)
            for i in range(len(ip_data)):
                create_port_code = create_port.create(ip_data[i], test_ip_object_element_position)
                if create_port_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create ip object successfully.", flush=True)
                elif create_port_code != 200:
                    result = "Fail to create ip."
                    break
        
        # 创建rule
        if create_port_code == 200:
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
                verify = ApiVerification()
                verification_result = verify.api_verification(driver, parameter, test_data, [])
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
        
                # 脚本结束时间和耗时
        
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
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.88",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 10,
        "is_log": 0,
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