# -*- coding: UTF-8 -*-
import time
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
from support.packet_generator.verification import Verification
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import *
from support.ui_utils.switch_intf import *
import support.ui_utils.env
from support.report import *
from datetime import datetime
import configparser

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        result, exception_result = "", ""
        
        # 脚本启动时间
        start_time = time.time()
        
        # 测试数据
        ui_test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "dos_protection",
            "rule_name": "dos_protect_srcip_http_rate_srcip_d3",
            "rule_action": "protect",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "dos_srcip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter['test_pc_ip'],
                            }
                        ]
                    }
                ],
                "application": [
                    {
                        "name": "http",
                        "object_type": "application",
                        "negate": False
                    }
                ]
            },
            "obj_condition": [
                {
                    "attribute_name": "ATTR_SOURCE_IP",
                    "object_type": "ip",
                    "object_sub_type": "ip",
                    "object_list": [
                        {
                            "add_item_list": [
                                {
                                    "ip_address": "default",
                                    "port_range": "0-65535"
                                }
                            ]
                        }
                    ]
                }
            ],
            "app_name": ["http"],
            "threshold": {
                "type": "rate",
                "rate_threshold": {
                    "group_by": "source_ip",
                    "request_per_period": 1,
                    "counting_period": "10s"
                }
            },
            "mitigation": {
                "behavior": "deny",
                "timeout": "10s"
            },
            "expected_return": "",
            "counters": {"hits": 1},
            "log_query_param": [
                
            ],
            "dos_query_param": [
                
            ],
            "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "1.1.1.1",
                "clients_end_ip": "1.1.1.1",
                "servers_start_ip": "2.1.1.1",
                "servers_end_ip": "2.1.1.2",
                "m": 1,
                "d": 1,
                "yaml_name": "test",
                "pcap_name": "http"
            },
            "token": ""
        }
        
        # 获取网卡
        parse = configparser.ConfigParser()
        parse_dir = os.path.join("configuration_file.ini")
        parse.read(parse_dir, encoding="utf-8")
        api_intf = parse.get("test_pc", "api_intf")
        ui_intf = parse.get("test_pc", "ui_intf")
        
        parameter_reinitialization = False
        if parameter["script_type"] == "all":
            parameter_reinitialization = True
        
        if parameter["script_type"] == "ui" or parameter["script_type"] == "all":
            # script_type为all时，需要单独对参数进行初始化
            if parameter_reinitialization == True:
                parameter["test_pc_ip"] = parse.get("test_pc", "ip_for_ui_with_traffic")
                parameter['test_subcriber_id'] = parse.get("test_pc", "subcriber_id_for_ui_with_traffic")
                parameter['test_imsi'] = parse.get("test_pc", "imsi_for_ui_with_traffic")
                parameter['test_phone_number'] = parse.get("test_pc", "phone_number_for_ui_with_traffic")
                parameter["vsys_id"] = parse.get("vsys", "id_for_ui")
                parameter["is_log"] = parse.get("is_log", "ui")
            
            # 环境初始化
            support.ui_utils.env.initiate_selenium_request()
            driver = support.ui_utils.env.my_driver()
            support.ui_utils.env.setup()
            
            log_in = LogIn()
            pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
            token = log_in.login(parameter["username"], pwd, parameter["api_server"])
            ui_test_data["token"] = token

            # name_list汇总
            name_list = [
                {
                    "type": ui_test_data["policy_type"],
                    "name": ui_test_data["rule_name"]
                },
                {
                    "type": ui_test_data["condition"]["source_ip"][0]['object_type'],
                    "name": ui_test_data["condition"]["source_ip"][0]['name']
                }
            ]
            
            # 添加定位库集合
            test_rule_element_position = {}
            if ui_test_data["policy_type"] == "dos_protection":
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
                        "policyRulePage_selectAction_posId": securityRulePage_selectDeny_posId,
                        # srcip
                        "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                        "policyRulePage_searchSrcIP_posXpath": securityRulePage_searchSrcIP_posXpath,
                        "policyRulePage_selectSrcIP_posXpath": securityRulePage_selectSrcIP_posXpath,
                        "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
                        "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                        "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                        "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                        "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                        "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                        "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                        # fqdn
                        "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                        "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                        "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                        "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                        "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
                        # url
                        "policyRulePage_addConditionUrl_posXpath": securityRulePage_addCondition_url_posXpath,
                        "policyRulePage_addUrl_posXpath": policyRulePage_addUrl_posXpath,
                        "policyRulePage_searchUrl_posXpath": policyRulePage_searchUrl_posXpath,
                        "policyRulePage_selectUrl_posXpath": policyRulePage_selectUrl_posXpath,
                        "policyRulePage_closeUrl_posXpath": policyRulePage_closeUrl_posXpath,
                        # req header
                        "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
                        "policyRulePage_addRequestHeader_posXpath": manipulationRulePage_addRequestHeader_posXpath,
                        "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
                        "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
                        "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
                        "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                        "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                        "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                        # sub action
                        "policyRulePage_subAction_rateLimit_posXpath": securityRulePage_subAction_rateLimit_posXpath,
                        "policyRulePage_subAction_rateLimit_rate_posXpath": securityRulePage_subAction_rateLimit_rate_posXpath,
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
            if "source_ip" in ui_test_data["condition"] and len(ui_test_data["condition"]["source_ip"]) != 0:
                ip_data = ui_test_data["condition"]["source_ip"]
                create_ip = CreateObject(driver)
                for i in range(len(ip_data)):
                    create_ip_code = create_ip.create(ip_data[i], test_ip_object_element_position)
                    if create_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create ip object successfully.", flush=True)
                    elif create_ip_code != 200:
                        result = "Fail to create ip."
                        break
            
            # 创建rule
            if create_ip_code == 200:
                create_rule = CreateRule(driver)
                create_rule_code = create_rule.create(ui_test_data, test_rule_element_position)
                if create_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create security rule successfully.", flush=True)
                elif create_rule_code != 200:
                    result = "Fail to create security rule."

            # 触发流量验证
            if create_rule_code == 200:
                search_rule = SearchRule(driver)
                search_rule_code, rule_id = search_rule.get_rule_id(ui_test_data["policy_type"], ui_test_data["rule_name"], test_rule_element_position)
                if search_rule_code == 200:
                    # rule_id = search_rule.get_rule_id()
                    ui_test_data["rule_id"] = rule_id
                    verify = Verification()
                    verification_result = verify.verification(driver, parameter, ui_test_data, [], test_rule_element_position)
                    if len(verification_result) == 4:
                        driver = verification_result[3]
                    elif len(verification_result) == 5:
                        driver = verification_result[4]
            
            # 分析验证结果，并返回给flask
            if len(verification_result) != 0:
                analysis = AnalysisResult()
                result = analysis.analysis_result(ui_test_data, [], verification_result)
            
            # 删除rule
            if create_rule_code == 200:
                search_rule = SearchRule(driver)
                search_rule_code, first_row_checkbox_element = search_rule.search(ui_test_data["policy_type"], ui_test_data["rule_name"], test_rule_element_position)
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
        
        if parameter["script_type"] == "api" or parameter["script_type"] == "all":
            # script_type为all时，需要单独对参数进行初始化
            if parameter_reinitialization == True:
                parameter["test_pc_ip"] = parse.get("test_pc", "ip_for_api")
                parameter['test_subcriber_id'] = parse.get("test_pc", "subcriber_id_for_api")
                parameter["env"] = "tsgx"
                parameter["vsys_id"] = parse.get("vsys", "id_for_api")
                parameter["is_log"] = parse.get("is_log", "api")
            
            # 切换网卡，让ui网卡down，api网卡up
            switch = SwitchIntf()
            switch.switch_intf(api_intf, ui_intf)
        
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
        # 测试结束后恢复网卡状态，让ui网卡恢复默认up，api网卡恢复默认down
        parse = configparser.ConfigParser()
        parse_dir = os.path.join("configuration_file.ini")
        parse.read(parse_dir, encoding="utf-8")
        api_intf = parse.get("test_pc", "api_intf")
        ui_intf = parse.get("test_pc", "ui_intf")
        switch = SwitchIntf()
        switch.switch_intf(ui_intf, api_intf)
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
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 5,
        "is_log": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_testtests/ui",
        "module_name": "dos_protection",
        "test_case_name": "dos_protect_srcip_http_rate_srcip_d3"
    }
    run(parameter)