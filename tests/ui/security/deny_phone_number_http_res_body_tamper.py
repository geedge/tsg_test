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
            "rule_name": "security_rule_deny_phone_number_http_res_body_tamper",
            "rule_action": "allow",
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
                        "name": "security_phone_number",
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
                "server_fqdn": [],
                "protocol_filed": [
                    {
                        "name": "security_keywords_response_body",
                        "object_type": "keywords",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "response_body",
                                "item_value": "TEXT",
                                "value": [
                                    "test_resbody"
                                ]
                            }
                        ],
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                    {
                        "type": "tamper"
                    }
                ],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "timed out",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key":"imsi", "query_value": "110035141486424"}],
            "traffic": {
                "protocol": "http",
                "type": "curl",
                "command": "curl --connect-timeout 10 -m 10 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"helloSecurity\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" http://192.168.40.206:180/go"
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
                "name": "security_rule_deny_phone_number_http_res_body_tamper"
            },
            {
                "type": "mobile_identity",
                "name": "security_phone_number"
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
            test_keywords_object_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_keywords_posId
                },
                "create": {
                    "objectListPage_createButton_posId": keywordsObjectListPage_createButton_posId,
                    "objectListPage_dropDown_createButton_posId": keywordsObjectListPage_dropDown_createButton_posId,
                    "objectPage_inputName_posXpath": keywordsObjectPage_inputName_posXpath,
                    "objectPage_addItem_posId": keywordsObjectPage_addItem_posId,
                    "objectPage_item_value_select_posXpath": keywordsObjectPage_item_value_select_posXpath,
                    "objectPage_inputItem_posXpath": keywordsObjectPage_inputItem_posXpath,
                    "objectPage_item_value_plus_posXpath": keywordsObjectPage_item_value_plus_posXpath,
                    "objectPage_button_saveItem_posXpath": keywordsObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posId": keywordsObjectPage_okButton_posId,
                    "objectPage_okButton_warningYes_posXpath": keywordsObjectPage_okButton_warningYes_posXpath
                },
                "search": {
                    "objectListPage_searchLabel_posId": keywordsObjectListPage_searchLabel_posId,
                    "objectListPage_searchLabel_selectName_posXpath": keywordsObjectListPage_searchLabel_selectName_posXpath,
                    "objectListPage_tableTbody_posXpath": keywordsObjectListPage_tableTbody_posXpath
                },
                "delete": {
                    "objectListPage_allSelect_posXpath": keywordsObjectListPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posId": keywordsObjectListPage_deleteButton_posId,
                    "objectListPage_deleteButton_warningYes_posXpath": keywordsObjectListPage_deleteButton_warningYes_posXpath
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
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    # response body
                    "policyRulePage_addConditionResponseBody_posXpath": securityRulePage_addCondition_responseBody_posXpath,
                    "policyRulePage_addResponseBody_posXpath": manipulationRulePage_addResponseBody_posXpath,
                    "policyRulePage_searchResponseBody_posXpath": securityRulePage_searchRequestHeader_posXpath,
                    "policyRulePage_selectResponseBody_posXpath": securityRulePage_selectRequestHeader_posXpath,
                    "policyRulePage_closeResponseBody_posXpath": securityRulePage_closeRequestHeader_posXpath,
                    # sub action
                    "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                    "policyRulePage_subAction_tamper_posXpath": securityRulePage_subAction_tamper_posXpath,
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
        # 创建keywords      
        if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
            protocol_field_data = test_data["condition"]["protocol_filed"]
            create_protocol_filed = CreateObject(driver)
            for x in range(len(protocol_field_data)):
                object_type = protocol_field_data[x]['object_type']
                if object_type == 'keywords':
                    create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_keywords_object_element_position)
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
            for q in range(len(protocol_field_data)):
                search_protocol_filed = SearchObject(driver)
                object_type = protocol_field_data[q]['object_type']
                if object_type == 'keywords':
                    search_protocol_filed_code, first_row_checkbox_element = search_protocol_filed.search(protocol_field_data[q]["name"], test_keywords_object_element_position)
                if search_protocol_filed_code == 200:
                    delete_protocol_filed = DeleteObject(driver)
                    if object_type == 'keywords':
                        delete_protocol_filed_code = delete_protocol_filed.delete(test_keywords_object_element_position, first_row_checkbox_element, True)
                    if delete_protocol_filed_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(object_type), flush=True)
                    elif delete_protocol_filed_code != 200:
                        result = result + " In addition, fail to delete {} object.".format(object_type)
                        break
                else:
                    result = result + " In addition, fail to search {} object.".format(object_type)
                    break
        
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
        "test_pc_ip": "192.168.64.91",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 11,
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