# -*- coding: UTF-8 -*-
import os
import random
import sys

from support.api_utils.organize_config import OrganizeConfig

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
from support.packet_generator.verification import Verification
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
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Begin to run test case: " + parameter["test_case_name"], flush=True)
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
            "rule_name": os.path.splitext(os.path.basename(__file__))[0],
            "rule_action": "allow",
            "rule_type": "create",
            "is_mirror": "on",
            "mirror_type": "mail",
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
                                "item_value": "10.64.101.2",
                            },
                        ]
                    }
                ],
                "application": [
                    {
                        "name": "mail",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "monit_mail_from_by_account",
                        "object_type": "account",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "mail_from",
                                "item_value": " zhangchengwei&@geedge&networks.com"
                            }
                        ],
                    }
                ],
            },
            "profile": [

                        {
                            "name":"profile1",
                            "vlan_count": random.randint(3, 66)

                            #vlan的范围：应该是在3-66
                        }
             ],
            "expected_return": "trex",
            "counters": {"hits": 1},
            "log_query_param": [
                {"query_field_key": "decoded_as", "query_value": "MAIL"},
                {"query_field_key": "monitor_mirrored_pkts", "query_value": 3748},
                {"query_field_key": "monitor_mirrored_bytes", "query_value": 4623316}
            ],
            "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "10.64.224.3",
                "clients_end_ip": "10.64.224.3",
                "servers_start_ip": "2.1.1.3",
                "servers_end_ip": "2.1.1.3",
                "m": 1,
                "d": 1,
                "yaml_name": "test",
                "pcap_name": "mail_imap"
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
                "type": test_data["condition"]["source_ip"][0]['object_type'],
                "name": test_data["condition"]["source_ip"][0]['name']
            },
            {
                "type": test_data["condition"]["protocol_filed"][0]['object_type'],
                "name": test_data["condition"]["protocol_filed"][0]['name']
            }

        ]

        organize_config = OrganizeConfig()
        test_data = organize_config.generate_random_ip(test_data, parameter)

        # 创建object
        if "condition" in test_data.keys():
            for cond_key, cond_value in (test_data["condition"].items()):
                cond_status = 0
                if cond_key == "application":
                    continue  # 直接跳过
                cond_key_out = cond_key.replace("_", " ")
                if len(cond_value) != 0:  # 不为空
                    cond_data = cond_value
                    create_ip = CreateObject(driver)
                    for i in range(len(cond_data)):  # 遍历创建所有condition
                        if cond_key == "protocol_filed":
                            tmp_key = cond_data[i]["object_type"]
                            cond_key_out = tmp_key.replace("_", " ")
                            element_position_map = get_element_position(tmp_key)
                        else:
                            element_position_map = get_element_position(cond_key)
                        cond_code = create_ip.create(cond_data[i], element_position_map)
                        if cond_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                  "Create {} object successfully.".format(cond_key_out), flush=True)
                        else:
                            result = "Fail to create {} object.".format(cond_key_out)
                            cond_status = 1
                            break
                if cond_status == 1:  # 创建失败，退出遍历创建
                    break

        # 创建profile
        prfi_code = 200
        if "profile" in test_data.keys():
            profile_data = test_data["profile"]
            element_position_map = get_profile_element_position("monitor_profile")
            create_monitor_profile = CreateMonitorProfile(driver, element_position_map)
            for i in range(len(profile_data)):
                create_monitor_profile_code = create_monitor_profile.create_monitor_profile(profile_data[i],
                                                                                            test_monitor_profile_element_position,
                                                                                            test_data["profile"][i][
                                                                                                "name"])
                if create_monitor_profile_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Create traffic mirroring profile successfully.", flush=True)
                elif create_monitor_profile_code != 200:
                    result = "Fail to create Traffic Mirroring Profiles profile."
                    break

        # 创建rule
        if cond_code == 200 and prfi_code == 200:
            create_rule = CreateRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            create_rule_code = create_rule.create(test_data, element_position_map)
            if create_rule_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Create {} rule successfully.".format(test_data["policy_type"], flush=True))
            elif create_rule_code != 200:
                result = "Fail to create {} rule.".format(test_data["policy_type"])

        # 触发流量验证
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"],
                                                                element_position_map)
            if search_rule_code == 200:
                test_data["rule_id"] = rule_id
                verify = Verification()
                verification_result = verify.verification(driver, parameter, test_data, [], element_position_map)
                if len(verification_result) == 4:
                    driver = verification_result[3]
                elif len(verification_result) == 5:
                    driver = verification_result[4]
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Traffic verification failed", flush=True)

        # 分析验证结果，并返回给flask
        if len(verification_result) != 0:
            analysis = AnalysisResult()
            result = analysis.analysis_result(test_data, [], verification_result)
            # if len(result) == 0:
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
            # elif len(result) != 0:
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", result, flush=True)

        # 删除rule
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"],
                                                                              test_data["rule_name"],
                                                                              element_position_map)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Delete manipulation rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete {} rule.".format(test_data["policy_type"])
            else:
                result = result + " In addition, fail to search {} rule.".format(test_data["policy_type"])

        # 删除object
        if delete_rule_code == 200 and "condition" in test_data.keys():
            # 删除
            for cond_key, cond_value in (test_data["condition"].items()):  # 遍历所有cond数据
                if cond_key == "application":
                    continue  # 直接跳过
                cond_status = 0
                cond_key_out = cond_key.replace("_", " ")
                if len(cond_value) != 0:  # 不为空
                    cond_data = cond_value
                    for i in range(len(cond_data)):  # 遍历查询所有condition
                        search_cond = SearchObject(driver)
                        if cond_key == "protocol_filed":
                            tmp_key = cond_data[i]["object_type"]
                            cond_key_out = tmp_key.replace("_", " ")
                            element_position_map = get_element_position(tmp_key)
                        else:
                            element_position_map = get_element_position(cond_key)
                        search_cond_code, first_row_checkbox_element = search_cond.search(cond_data[i]["name"],
                                                                                          element_position_map)
                        if search_cond_code == 200:
                            delete_cond = DeleteObject(driver)
                            delete_cond_code = delete_cond.delete(element_position_map, first_row_checkbox_element,
                                                                  True)
                            if delete_cond_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                      "Delete {} object successfully.".format(cond_key_out), flush=True)
                            else:
                                result = result + " In addition, fail to delete {} object.".format(cond_key_out)
                                break
                        else:
                            result = result + " In addition, fail to search {} object.".format(cond_key_out)
                            break
                        # 退出遍历标志
                        if cond_status == 1:  # 失败，退出遍历创建
                            break
                # 退出遍历标志
                if cond_status == 1:  # 失败，退出遍历创建
                    break

        # 删除profile
        if delete_rule_code == 200 and "profile" in test_data.keys():
            # 删除
            if delete_rule_code == 200:
                for x in range(len(profile_data)):
                    search_mirror_profile = SearchProfile(driver)
                    profile_return_code, first_row_checkbox_element = search_mirror_profile.search(
                        profile_data[x]['name'], test_monitor_profile_element_position)
                    if profile_return_code == 200:
                        delete_mirror_profile = DeleteProfile(driver)
                        delete_profile_code = delete_mirror_profile.delete(test_monitor_profile_element_position,
                                                                           first_row_checkbox_element, True)
                        if delete_profile_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                  "Delete monitor profile successfully.", flush=True)
                        elif delete_profile_code != 200:
                            result = result + " In addition, fail to delete profile."
                            break
                    else:
                        result = result + " In addition, fail to search profile."
                        break
        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,
              flush=True)
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
        "test_pc_ip": "192.168.64.96",
        "test_subcriber_id": "test490",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "is_log": 1,
        "env": "tsgx",
        "script_type": "ui",
        "vsys_id": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "monitor",
        "test_case_name": "monitor_rule_mail_mirror_on"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """