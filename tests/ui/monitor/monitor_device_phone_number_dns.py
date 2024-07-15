# -*- coding: UTF-8 -*-
import time
import os
import sys
import os
import sys

from support.api_utils.delete_policy import *
from support.ui_utils.profile.search_profile import SearchProfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.policy.edit_rule import EditRule
from support.traffic_replay.traffic_verification import *
from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.ui_utils.profile.create_monitor_profile import CreateProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
import support.ui_utils.env
import traceback

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
            "policy_type": "monitor",
            "rule_name": "monitor_phone_number_dns",
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
                        "name": "monitor_phone_number",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "phone_number",
                                "item_value": "$523335886424",
                            }
                        ]
                    }
                ],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "dns",  #
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
            "is_mirror": "on",
            "profile": [],
            "expected_return": "skype",
            "counters_1": {"hits": "many"},
            "log_query_param_1": [{"query_field_key": "decoded_as", "query_value": "DNS"}],
            "traffic": {
                "type": "nslookup",
                "command": "nslookup www.skype.com -timeout=1 8.8.8.8"
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
                "type": test_data["policy_type"],
                "name": test_data["rule_name"]
            },
            {
                "type": test_data["condition"]["device"][0]['object_type'],
                "name": test_data["condition"]["device"][0]['name']
            }

        ]

        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "monitor":
            test_phone_number_object_element_position = {
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
                    "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": securityRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": securityRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
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
                    "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                    "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": monitorRulePage_okButton_posId,
                    "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath,
                    # profile
                    "policyRulePage_mirrorTrafficButton_posXpath": monitorRulePage_mirrorTrafficButton_posXpath,
                    "policyRulePage_addVLANIDButton_posXpath": monitorRulePage_addVLANIDButton_posXpath,
                    "policyRulePage_firstSelectMirrorProfile_posXpath": monitorRulePage_firstSelectMirrorProfile_posXpath,
                    "policyRulePage_searchMirrorProfile_posXpath": monitorRulePage_searchMirrorProfile_posXpath,
                    "policyRulePage_selectMirrorProfile_posXpath": monitorRulePage_selectMirrorProfile_posXpath,
                    "policyRulePage_saveProile_ok_posXpath": monitorRulePage_saveProile_ok_posXpath,
                    "policyRulePage_saveProile_warningYes_posXpath": monitorRulePage_saveProile_warningYes_posXpath,
                    # add imsi
                    "policyRulePage_addConditionImsi_posXpath": securityRulePage_addCondition_imsi_posXpath,
                    "policyRulePage_addImsi_posXpath": securityRulePage_addImsi_posXpath,
                    "policyRulePage_searchImsi_posXpath": policyRulePage_searchImsi_posXpath,
                    "policyRulePage_selectImsi_posXpath": policyRulePage_selectImsi_posXpath,
                    "policyRulePage_closeImsi_posXpath": policyRulePage_closeImsi_posXpath,
                    # phone number
                    "policyRulePage_choosePhoneNumber_posXpath": securityRulePage_choosePhoneNumber_posXpath,
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
        # 创建object
        if "device" in test_data["condition"] and len(test_data["condition"]["device"]) != 0:
            device_data = test_data["condition"]["device"]
            create_device = CreateObject(driver)
            for i in range(len(device_data)):
                object_sub_type = device_data[i]['item'][0]['item_type']
                if object_sub_type == 'phone_number':
                    create_device_code = create_device.create(device_data[i], test_phone_number_object_element_position)
                if create_device_code == 200:
                    print("Create {} object successfully.".format(object_sub_type), flush=True)
                elif create_device_code != 200:
                    result = "Fail to create {} object.".format(object_sub_type)
                    break

        # 创建rule
        if create_device_code == 200:
            create_rule = CreateRule(driver)
            create_rule_code = create_rule.create(test_data, test_rule_element_position)
            if create_rule_code == 200:
                print("Create monitor rule successfully.", flush=True)
            elif create_rule_code != 200:
                result = "Fail to create monitor rule."
        # 触发流量验证
        if create_rule_code == 200:
            edit_rule = EditRule(driver)
            edit_rule_code, rule_id = edit_rule.edit(test_data["policy_type"], test_data["rule_name"],
                                                     test_rule_element_position)
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
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"],
                                                                              test_data["rule_name"],
                                                                              test_rule_element_position)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print("Delete monitor rule successfully.", flush=True)
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
                if object_sub_type == 'phone_number':
                    search_device_code, first_row_checkbox_element = search_device.search(device_data[y]["name"],
                                                                                          test_phone_number_object_element_position)
                if search_device_code == 200:
                    delete_device = DeleteObject(driver)
                    if object_sub_type == 'phone_number':
                        delete_device_code = delete_device.delete(test_phone_number_object_element_position,
                                                                  first_row_checkbox_element, True)
                    if delete_device_code == 200:
                        print("Delete {} object successfully.".format(object_sub_type), flush=True)
                    elif delete_device_code != 200:
                        result = result + " In addition, fail to delete {} object.".format(object_sub_type)
                        break
                else:
                    result = result + " In addition, fail to search {} object.".format(object_sub_type)
                # 脚本结束时间和耗时

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print("Duration of running the test case: ", "{:.3f}".format(duration), flush=True)

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
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.91",
        "api_server": "http://192.168.44.72",
        "is_log": 0,
        "env": "tsgx",
        "script_type": "ui",
        "vsys_id": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "monitor",
        "test_case_name": "monitor_phone_number_dns"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """