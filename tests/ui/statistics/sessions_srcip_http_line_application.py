# -*- coding: UTF-8 -*-
import os
import sys

from support.api_utils.organize_config import OrganizeConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.profile.create_statistics_template import CreateStatisticsTemplate
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile

from support.ui_utils.policy.edit_rule import EditRule
from support.traffic_manager.verification import Verification

from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
import support.ui_utils.env
from support.api_utils.delete_policy import *
import traceback

from support.report import *
from datetime import datetime

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
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
            "policy_type": "statistics",
            "rule_name": "sessions_with_src_ip_http_line_application",
            "rule_action": "statistics",
            "rule_type": "create",
            "debug_flag": "local",
        "test_subcriber_id": "test6489",
        "script_type": "ui",
            "condition": {
                "source_ip": [
                    {
                        "name": "statistics_all_sessions_line_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "10.64.224.28",
                            },
                        ]
                    }
                ],
                "source_port": [],
                "destination_ip": [
                    {
                        "name": "statistics_all_sessions_line_destination_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "2.1.1.28",
                            },
                        ]
                    }],
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
                ],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [
                ],
                "packet_capture": []
            },
            "action_parameter": {
                "statistics_template": [{
                    "name": "Auto Sessions Line Application",
                    "profile_type": "statistics_template",
                    "charts": [
                        {
                          "chart_name": "default name",
                          "visualization_type": "Line",
                          "metrics": [
                            "sessions:RATE:sessions"
                          ],
                          "dimensions": ["application"],
                          "order_by": "sessions",
                          "row_limit": "15",
                          "min_in_size": "1",
                          "max_out_size": "1"
                        }
                      ]
                }]
            },
            "expected_return": "reset",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key": "server_fqdn", "query_value": "www.yumi.com"}],
            "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "10.64.224.28",
                "clients_end_ip": "10.64.224.28",
                "servers_start_ip": "2.1.1.28",
                "servers_end_ip": "2.1.1.28",
                "m": 1,
                "d": 1,
                "yaml_name": "test_https",
                "pcap_name": "http_87pkts"
            },
            # "traffic": {
            #     "type": "trex",
            #     "clients_start_ip": "192.168.64.86",
            #     "clients_end_ip": "192.168.64.86",
            #     "servers_start_ip": "2.1.1.1",
            #     "servers_end_ip": "2.1.1.2",
            #     "m": 1,
            #     "d": 1,
            #     "yaml_name": "test_https",
            #     "pcap_name": "test_https"
            # },
            # "traffic": {
            #     "type": "nslookup",
            #     "command": "nslookup www.facebook.com"
            # },
            # "traffic": {
            #     "type": "wget",
            #     "command": "wget -q -O- http://open.node.com:180"
            # },
            "token": ""
        }
        # name_list汇总
        name_list = [
            {
                "type": "statistics",
                "name": "sessions_with_src_ip_http_line_application",
            },
            {
                "type": "ip",
                "name": "statistics_all_sessions_line_source_ip",
            },{
                "type": "ip",
                "name": "statistics_all_sessions_line_destination_ip",
            },
            {
                "type": "statistics_template",
                "name": "Auto Sessions Line Application",
            },
        ]
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token
        # 添加测试过程中涉及的template
        template_path = {}
        template_path["trex_workpath"] = "/opt/trex/v3.03"
        template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"

                # 创建object
        # Statistics Rule使用随机IP
        organize_config = OrganizeConfig()
        test_data = organize_config.generate_random_ip(test_data, parameter)
        for cond_key, cond_value in (test_data["condition"].items()):
            cond_status = 0
            if cond_key == "application" or cond_key == "sub_action_override":
                continue   # 直接跳过
            if len(cond_value) != 0:  # 不为空
                cond_data = cond_value
                create_ip = CreateObject(driver)
                for i in range(len(cond_data)):  # 遍历创建所有condition
                    element_position_map = get_element_position(cond_key)
                    cond_code = create_ip.create(cond_data[i], element_position_map)
                    if cond_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(cond_key), flush=True)
                    else:
                        result = "Fail to create {} object.".format(cond_key)
                        cond_status = 1
                        break
            if cond_status == 1:   # 创建失败，退出遍历创建
                break

        # 创建Statistics Template
        create_statistics_template_code = 0
        if cond_code == 200:
            profile = test_data["action_parameter"]
            statistics_templates = profile["statistics_template"]
            for statistics_template in statistics_templates:
                cond_status = 0
                #create_statistics_template = CreateProfile(driver)
                create_statistics_template = CreateStatisticsTemplate(driver)
                element_position_map = get_profile_element_position("statistics_template")
                cond_code = create_statistics_template.create(statistics_template, element_position_map)
                create_statistics_template_code = cond_code
                if cond_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} Profile successfully.".format("statistics_template"), flush=True)
                else:
                    result = "Fail to create {} Profile.".format("statistics_template")
                    cond_status = 1
                    break
                if cond_status == 1:   # 创建失败，退出遍历创建
                    break

        # 创建rule
        create_rule_code = 0
        delete_rule_code = 0
        if cond_code == 200:
            create_rule = CreateRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            create_rule_code = create_rule.create(test_data, element_position_map)
            if create_rule_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(test_data["policy_type"], flush=True))
            elif create_rule_code != 200:
                result = "Fail to create {} rule.".format(test_data["policy_type"])


        # 触发流量验证
        if create_rule_code == 200:

            search_rule = SearchRule(driver)
            search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], element_position_map)
            if search_rule_code == 200:
                test_data["rule_id"] = rule_id
                config = OrganizeConfig()
                cfg_list = config.organize_cfg(parameter, test_data, template_path)
                verify = Verification()
                verification_result = verify.verification(driver, parameter, test_data, cfg_list, element_position_map)

            # 编辑修改使用
            #search_rule = SearchRule(driver)
            #element_position_map = get_element_position(test_data["policy_type"])
            #edit_rule_code, rule_id = edit_rule.edit(test_data["policy_type"], test_data["rule_name"], element_position_map)
            #if search_rule_code == 200:
                # rule_id = search_rule.get_rule_id()
               # test_data["rule_id"] = rule_id


        # 分析验证结果，并返回给flask
        if len(verification_result) != 0:
            analysis = AnalysisResult()
            result = analysis.analysis_result(test_data, [], verification_result)
            if len(result) == 0:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
            elif len(result) != 0:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", result, flush=True)

        # 避免报错：stale element not found
        time.sleep(5)

        # 删除rule
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], element_position_map)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete Statistics rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete {} rule.".format(test_data["policy_type"])
            else:
                result = result + " In addition, fail to search {} rule.".format(test_data["policy_type"])

        # 删除Statistics Tesmplate
        if create_statistics_template_code == 200 and delete_rule_code == 200:
            for prfi_key, prfi_value in (test_data["action_parameter"].items()):  # 遍历所有cond数据
                prfi_status = 0
                prfi_key_out = prfi_key.replace("_", " ")
                if len(prfi_value) != 0:  # 不为空
                    for i in range(len(prfi_value)):  # 遍历查询所有profile
                        search_prfi = SearchProfile(driver)
                        element_position_map = get_element_position(prfi_key)
                        prfi_name = prfi_value[i]["name"].strip()
                        search_prfi_code, first_row_checkbox_element = search_prfi.search(prfi_name,
                                                                                          element_position_map)
                        if search_prfi_code == 200:
                            delete_prfi = DeleteProfile(driver)
                            delete_prfi_code = delete_prfi.delete(element_position_map, first_row_checkbox_element)
                            if delete_prfi_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} profile successfully.".format(prfi_key_out), flush=True)
                            else:
                                result = result + " In addition, fail to delete {} profile.".format(prfi_key_out)
                                break
                        else:
                            result = result + " In addition, fail to search {} profile.".format(prfi_key_out)
                            break
                        # 退出遍历标志
                        if prfi_status == 1:  # 失败，退出遍历创建
                            break
                # 退出遍历标志
                if prfi_status == 1:  # 失败，退出遍历创建
                    break
        # 删除object
        if delete_rule_code == 200:
            # 删除
            for cond_key, cond_value in (test_data["condition"].items()):  # 遍历所有cond数据
                if cond_key == "application" or cond_key == "sub_action_override":
                    continue  # 直接跳过
                cond_status = 0
                if len(cond_value) != 0:  # 不为空
                    cond_data = cond_value
                    for i in range(len(cond_data)):  # 遍历查询所有condition
                        search_cond = SearchObject(driver)
                        element_position_map = get_element_position(cond_key)
                        search_cond_code, first_row_checkbox_element = search_cond.search(cond_value[i]["name"], element_position_map)
                        if search_cond_code == 200:
                            delete_cond = DeleteObject(driver)
                            delete_cond_code = delete_cond.delete(element_position_map, first_row_checkbox_element, True)
                            if delete_cond_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(cond_key), flush=True)
                            else:
                                result = result + " In addition, fail to delete {} object.".format(cond_key)
                                break
                        else:
                            result = result + " In addition, fail to search {} object.".format(cond_key)
                            break
                        # 退出遍历标志
                        if cond_status == 1:  # 失败，退出遍历创建
                            break
                # 退出遍历标志
                if cond_status == 1:  # 失败，退出遍历创建
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
        traceback.print_exc()
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
        "test_pc_ip": "192.168.64.73",
        "api_server": "http://192.168.44.72",
        "is_log": 0,
        "env": "tsgx",
        "vsys_id": 11,#6
        "root_path": "D:/tsgcode/tsg_test",
        "path": "tsgcode/tsg_test/testcase/ui",
        "module_name": "statistics",
        "test_case_name": "sessions_with_src_ip_http_line_application",
        "debug_flag": "local",
        "test_subcriber_id": "test6489",
        "script_type": "ui",
        "policy_type": "statistics"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """