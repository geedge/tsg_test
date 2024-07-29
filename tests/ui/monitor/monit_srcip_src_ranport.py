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
            "rule_name": "monitor_rule_source_range_port",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "monitor_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter['test_pc_ip'],
                            },
                        ]
                    }
                ],
                "source_port": [
                    {
                        "name": "monitor_src_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "port",
                                "item_value": "1-65535",
                            },
                        ]
                    }
                ],
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
                "application": [],
                "server_fqdn": [
                ],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [
                ],
                "packet_capture": []
            },
            "is_mirror":"on",
            "profile": [],
            "expected_return": "baidu",
            "counters": {"hits": "many"},
            "log_query_param": [{"query_field_key": "ssl_sni", "query_value": "www.baidu.com"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv https://www.baidu.com"
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
                "name": "monitor_rule_source_range_port"
            },
            {
                "type": "port",
                "name": "monitor_src_port"
            }
        ]

        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "monitor":
            test_port_object_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_port_posId
                },
                "create": {
                    "objectListPage_createButton_posId": portObjectListPage_createButton_posId,
                    "objectListPage_dropDown_createButton_posId": portObjectListPage_dropDown_createButton_posId,
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
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_monitor_posId
                },
                "create": {
                    "policyRuleListPage_createButton_posId": monitorRuleListPage_createButton_posId,
                    "policyRulePage_inputName_posXpath": monitorRulePage_inputName_posXpath,
              
                    ###src_port
                    "policyRulePage_addConditionSrcPort_posXpath": monitorRulePage_addCondition_srcPort_posXpath,
                    "policyRulePage_addSrcPort_posXpath": monitorRulePage_addSrcPort_posXpath,
                    "policyRulePage_searchSrcPort_posXpath": monitorRulePage_searchSrcPort_posXpath,
                    "policyRulePage_selectSrcPort_posXpath": monitorRulePage_selectSrcPort_posXpath,
                    "policyRulePage_closeSrcPort_posXpath": monitorRulePage_closeSrcPort_posXpath,
                    ###src_port
                    "policyRulePage_searchApplication_posXpath": monitorRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": monitorRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": monitorRulePage_closeApplication_posXpath,
                    "policyRulePage_addCondition_posXpath": monitorRulePage_addCondition_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": monitorRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addApplication_posXpath": monitorRulePage_addApplication_posXpath,
                    "policyRulePage_addCondition_close_posXpath": monitorRulePage_addCondition_close_posXpath,
                   #other button
                    "policyRulePage_enable_posXpath": monitorRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": monitorRulePage_okButton_posId,
                    "policyRulePage_okButton_warningYes_posXpath": monitorRulePage_okButton_warningYes_posXpath,
                    # profile
                    "policyRulePage_mirrorTrafficButton_posXpath": monitorRulePage_mirrorTrafficButton_posXpath,
                    "policyRulePage_addVLANIDButton_posXpath": monitorRulePage_addVLANIDButton_posXpath,
                    "policyRulePage_firstSelectMirrorProfile_posXpath": monitorRulePage_firstSelectMirrorProfile_posXpath,
                    "policyRulePage_searchMirrorProfile_posXpath": monitorRulePage_searchMirrorProfile_posXpath,
                    "policyRulePage_selectMirrorProfile_posXpath": monitorRulePage_selectMirrorProfile_posXpath,
                    # 添加ip
                    "policyRulePage_addSrcIP_posXpath": monitorRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": monitorRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": monitorRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": monitorRulePage_closeSrcIP_posXpath,
                },
                "search": {
                    "policyRuleListPage_searchLable_posId": monitorRuleListPage_searchLable_posId,
                    "policyRuleListPage_searchLable_dropDown_item_posXpath": monitorRuleListPage_searchLable_dropDown_item_posXpath,
                    "policyRuleListPage_searchLable_input_itemContent_posXpath": monitorRuleListPage_searchLable_input_itemContent_posXpath,
                    "policyRuleListPage_searchLable_searchButton_posId": monitorRuleListPage_searchLable_searchButton_posId,
                    "policyRuleListPage_tableTbody_posXpath": monitorRuleListPage_tableTbody_posXpath
                },
                "delete": {
                    "policyRuleListPage_allSelect_posXpath": monitorRulelistPage_allSelect_posXpath,
                    "policyRuleListPage_deleteButton_posId": monitorRuleListPage_deleteButton_posId,
                    "policyRuleListPage_okButton_warningYes_posXpath": monitorRuleListpage_okButton_warningYes_posXpath,
                    "policyRuleListPage_okButton_warningNo_posXpath": monitorRuleListpage_okButton_warningNo_posXpath
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
                    result = "Fail to create ip object."
                    break

        #创建port
        if "source_port" in test_data["condition"] and len(test_data["condition"]["source_port"]) != 0:
            port_data =test_data["condition"]["source_port"]
            create_port = CreateObject(driver)
            for i in range(len(port_data)):
                create_port_code =create_port.create(port_data[i],test_port_object_element_position)
                if create_port_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create ip object successfully.", flush=True)
                elif create_port_code != 200:
                    result = "Fail to create ip object."
                    break

        # 创建rule
        if create_port_code == 200:
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
            for x in range(len(ip_data)):
                search_ip = SearchObject(driver)
                search_ip_code, first_row_checkbox_element = search_ip.search(ip_data[x]["name"],
                                                                              test_ip_object_element_position)
                if search_ip_code == 200:
                    delete_port = DeleteObject(driver)
                    delete_ip_code = delete_port.delete(test_ip_object_element_position,
                                                        first_row_checkbox_element, True)
                    if delete_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip object successfully.", flush=True)
                    elif delete_ip_code != 200:
                        result = result + " In addition, fail to delete ip object."
                        break
                else:
                    result = result + " In addition, fail to search ip object."
                    break
            # 删除port
            for x in range(len(port_data)):
                search_ip = SearchObject(driver)
                search_ip_code, first_row_checkbox_element = search_ip.search(port_data[x]["name"],
                                                                              test_port_object_element_position)
                if search_ip_code == 200:
                    delete_port = DeleteObject(driver)
                    delete_ip_code = delete_port.delete(test_port_object_element_position,
                                                        first_row_checkbox_element, True)
                    if delete_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip object successfully.", flush=True)
                    elif delete_ip_code != 200:
                        result = result + " In addition, fail to delete ip object."
                        break
                else:
                    result = result + " In addition, fail to search ip object."
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