# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.delete_policy import *
from support.ui_utils.profile.search_profile import SearchProfile
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
from support.ui_utils.profile.create_monitor_profile import CreateMonitorProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
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
            "rule_name": "monitor_imsi_ftp",
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
                        "name": "monitor_imsi",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "imsi",
                                "item_value": '$' + parameter['test_imsi'],
                            }
                        ]
                    }
                ],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "ftp",  #
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
            "is_mirror": "off",
            "profile": [],
            "expected_return": "auto",
            "counters": {"hits": 1},
            "log_query_param": [
                                {"query_field_key": "imsi", "query_value": parameter['test_imsi']}
                            ],
            "traffic": {
                "protocol": "ftp",
                "type": "curl",
                "command": "curl -m 20 ftp://192.168.40.206/autoFtp/english_big.txt -u ftpuser:111111"
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
                "name": "monitor_imsi_ftp"
            },
            {
                "type": "mobile_identity",
                "name": "monitor_imsi"
            }

        ]

        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "monitor":
            test_imsi_object_element_position = {
                "page_jump": {
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
                    "objectPage_imsiType_posId": imsiObjectPage_imsiType_posId,
                    "objectPage_addItem_posId": imsiObjectPage_addItem_posId,
                    "objectPage_inputItem_posXpath": imsiObjectPage_inputItem_posXpath,
                    "objectPage_button_saveItem_posXpath": imsiObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posId": imsiObjectPage_okButton_posId,
                    "objectPage_okButton_warningYes_posXpath": imsiObjectPage_okButton_warningYes_posXpath
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
                    "policyRulePage_addSrcIP_posXpath": monitorRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": monitorRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": monitorRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": monitorRulePage_closeSrcIP_posXpath,
                    "policyRulePage_addApplication_posXpath": monitorRulePage_addApplication_posXpath,
                    "policyRulePage_searchApplication_posXpath": monitorRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": monitorRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": monitorRulePage_closeApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": monitorRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addCondition_posXpath": monitorRulePage_addCondition_posXpath,
                    "policyRulePage_addConditionServerFqdn_posXpath": monitorRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addCondition_close_posXpath": monitorRulePage_addCondition_close_posXpath,
                    "policyRulePage_addServerFqdn_posXpath": monitorRulePage_addServerFqdn_posXpath,
                    "policyRulePage_searchServerFqdn_posXpath": monitorRulePage_searchServerFqdn_posXpath,
                    "policyRulePage_selectServerFqdn_posXpath": monitorRulePage_selectServerFqdn_posXpath,
                   "policyRulePage_closeServerFqdn_posXpath": monitorRulePage_closeServerFqdn_posXpath,
                    "policyRulePage_enable_posXpath": monitorRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": monitorRulePage_okButton_posId,
                    "policyRulePage_okButton_warningYes_posXpath": monitorRulePage_okButton_warningYes_posXpath,
                    # profile
                    "policyRulePage_mirrorTrafficButton_posXpath": monitorRulePage_mirrorTrafficButton_posXpath,
                    "policyRulePage_addVLANIDButton_posXpath": monitorRulePage_addVLANIDButton_posXpath,
                    "policyRulePage_firstSelectMirrorProfile_posXpath": monitorRulePage_firstSelectMirrorProfile_posXpath,
                    "policyRulePage_searchMirrorProfile_posXpath": monitorRulePage_searchMirrorProfile_posXpath,
                    "policyRulePage_selectMirrorProfile_posXpath": monitorRulePage_selectMirrorProfile_posXpath,
                    "policyRulePage_saveProile_ok_posXpath": monitorRulePage_saveProile_ok_posXpath,
                    "policyRulePage_saveProile_warningYes_posXpath": monitorRulePage_saveProile_warningYes_posXpath,
                    # add imsi
                    "policyRulePage_addConditionImsi_posXpath": monitorRulePage_addCondition_imsi_posXpath,
                    "policyRulePage_addImsi_posXpath": monitorRulePage_addImsi_posXpath,
                    "policyRulePage_searchImsi_posXpath": policyRulePage_searchImsi_posXpath,
                    "policyRulePage_selectImsi_posXpath": policyRulePage_selectImsi_posXpath,
                    "policyRulePage_closeImsi_posXpath": policyRulePage_closeImsi_posXpath,
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
        if "device" in test_data["condition"] and len(test_data["condition"]["device"]) != 0:
            device_data = test_data["condition"]["device"]
            create_device = CreateObject(driver)
            for i in range(len(device_data)):
                object_sub_type = device_data[i]['item'][0]['item_type']
                if object_sub_type == 'imsi':
                    create_device_code = create_device.create(device_data[i], test_imsi_object_element_position)
                if create_device_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_sub_type), flush=True)
                elif create_device_code != 200:
                    result = "Fail to create {} object.".format(object_sub_type)
                    break

        # 创建rule
        if create_device_code == 200:
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
            # 删除device相关的object
            for y in range(len(device_data)):
                search_device = SearchObject(driver)
                object_sub_type = device_data[i]['item'][0]['item_type']
                if object_sub_type == 'imsi':
                    search_device_code, first_row_checkbox_element = search_device.search(device_data[y]["name"],
                                                                                          test_imsi_object_element_position)
                if search_device_code == 200:
                    delete_device = DeleteObject(driver)
                    if object_sub_type == 'imsi':
                        delete_device_code = delete_device.delete(test_imsi_object_element_position,
                                                                  first_row_checkbox_element, True)
                    if delete_device_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(object_sub_type), flush=True)
                    elif delete_device_code != 200:
                        result = result + " In addition, fail to delete {} object.".format(object_sub_type)
                        break
                else:
                    result = result + " In addition, fail to search {} object.".format(object_sub_type)
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
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.9",
        "test_subcriber_id": "test490",
        "api_server": "http://192.168.44.72",
        "debug_flag" : "local",
        "is_log": 1,
        "env": "tsgx",
        "script_type": "ui",
        "vsys_id": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "monitor",
        "test_case_name": "monitor_imsi_ftp"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """