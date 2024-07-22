# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.delete_policy import *
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.policy.edit_rule import EditRule
from support.traffic_manager.verification import Verification
from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
import support.ui_utils.env
import traceback

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
            "policy_type": "monitor",
            "rule_name": "monitor_tcp_protocol",
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
                "device": [],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "http",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                    {
                        "name": "test_example",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "items": [
                            {
                                "item_value": "*example.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [
                ],
                "packet_capture": [],
                "ip_protocol":[
                    "TCP"
                ]
            },
            "is_mirror":"on",
            "profile": [],
            "expected_return": "Example Domain",
            "counters": {"hits": "many"},
            "log_query_param": [{"query_field_key": "http_host", "query_value": "www.example.com"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv http://www.example.com"
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
                "type": "monitor",
                "name": "monitor_tcp_protocol"
            },
            {
                "type": "fqdn",
                "name": "test_example"
            }
        ]

        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "monitor":
            test_fqdn_object_element_position = {
                "page_jump": {
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
            test_rule_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_monitor_posId
                },
                "create": {
                    "policyRuleListPage_createButton_posId": monitorRuleListPage_createButton_posId,
                    "policyRulePage_inputName_posXpath": securityRulePage_inputName_posXpath,
                    "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                    "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                    "policyRulePage_subAction_drop_posXpath": securityRulePage_subAction_drop_posXpath,
                    "policyRulePage_subAction_drop_dropPkt_posXpath": securityRulePage_subAction_drop_dropPkt_posXpath,
                    "policyRulePage_subAction_drop_sendTcpRst_posXpath": securityRulePage_subAction_drop_sendTcpRst_posXpath,
                    "policyRulePage_subAction_drop_sendIcmp_posXpath": securityRulePage_subAction_drop_sendIcmp_posXpath,
                    "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": monitorRulePage_okButton_posId,
                    "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath,
                    # profile
                    "policyRulePage_mirrorTrafficButton_posXpath": monitorRulePage_mirrorTrafficButton_posXpath,
                    "policyRulePage_addVLANIDButton_posXpath": monitorRulePage_addVLANIDButton_posXpath,
                    "policyRulePage_firstSelectMirrorProfile_posXpath": monitorRulePage_firstSelectMirrorProfile_posXpath,
                    "policyRulePage_searchMirrorProfile_posXpath": monitorRulePage_searchMirrorProfile_posXpath,
                    "policyRulePage_selectMirrorProfile_posXpath": monitorRulePage_selectMirrorProfile_posXpath,
                    # 添加ip
                    "policyRulePage_addConditionIpProtocol_posXpath": policyRulePage_addCondition_IpProtocol_posXpath,
                    "policyRulePage_addIpProtocol_posXpath": policyRulePage_addIpProtocol_posXpath,
                    "policyRulePage_searchIpProtocol_posXpath": policyRulePage_searchIpProtocol_posXpath,
                    "policyRulePage_selectIpProtocol_posXpath": policyRulePage_selectIpProtocol_posXpath,
                    "policyRulePage_closeIpProtocol_posXpath": policyRulePage_closeIpProtocol_posXpath,
                    # 添加Server FQDN
                    "policyRulePage_addConditionServerFqdn_posXpath": policyRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addCondition_close_posXpath": policyRulePage_addCondition_close_posXpath,
                    "policyRulePage_addServerFqdn_posXpath": policyRulePage_addServerFqdn_posXpath,
                    "policyRulePage_searchServerFqdn_posXpath": policyRulePage_searchServerFqdn_posXpath,
                    "policyRulePage_selectServerFqdn_posXpath": policyRulePage_selectServerFqdn_posXpath,
                    "policyRulePage_closeServerFqdn_posXpath": policyRulePage_closeServerFqdn_posXpath,
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
                    "policyRuleListPage_deleteButton_posId": monitorRuleListPage_deleteButton_posId,
                    "policyRuleListPage_okButton_warningYes_posXpath": securityRuleListpage_okButton_warningYes_posXpath,
                    "policyRuleListPage_okButton_warningNo_posXpath": securityRuleListpage_okButton_warningNo_posXpath
                }
            }

        # 创建Server FQDN
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


        # 创建rule
        if create_fqdn_code == 200:
            create_rule = CreateRule(driver)
            create_rule_code = create_rule.create(test_data, test_rule_element_position)
            if create_rule_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create monitor rule successfully.", flush=True)
            elif create_rule_code != 200:
                result = "Fail to create monitor rule."

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
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"],
                                                                              test_data["rule_name"],
                                                                              test_rule_element_position)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete monitor rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete monitor rule."
            else:
                result = result + " In addition, fail to search monitor rule."

        # 删除object
        if delete_rule_code == 200:
            # 删除ip
            for x in range(len(fqdn_data)):
                search_fqdn = SearchObject(driver)
                search_fqdn_code, first_row_checkbox_element = search_fqdn.search(fqdn_data[x]["name"],
                                                                                  test_fqdn_object_element_position)
                if search_fqdn_code == 200:
                    delete_fqdn = DeleteObject(driver)
                    delete_fqdn_code = delete_fqdn.delete(test_fqdn_object_element_position, first_row_checkbox_element,
                                                          True)
                    if delete_fqdn_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn object successfully.", flush=True)
                    elif delete_fqdn_code != 200:
                        result = result + " In addition, fail to delete fqdn object."
                        break
                else:
                    result = result + " In addition, fail to search fqdn object."
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
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.96",
        "test_subcriber_id": "test490",
        "api_server": "http://192.168.44.72",
        "debug_flag" : "local",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "monitor",
        "test_case_name": "source_range_port",
        "script_type": "ui",
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """