# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.profile.create_profile import CreateProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.policy.edit_rule import EditRule
from support.traffic_manager.traffic_verification import *
from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
import support.ui_utils.env
import traceback
from support.api_utils.delete_policy import *

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
            "policy_type": "pxy_manipulation",
            "rule_name": "deny_srcip_dstport_responseProfile",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "manipulation_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter["test_pc_ip"],
                            },
                        ]
                    }
                ],
                "destination_port": [
                    {
                        "name": "manipulation_destination_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "port",
                                "item_value": "443",
                            },
                        ]
                    }
                ],
                "application": [
                    {
                        "name": "http",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
            },
            "action_parameter": {
                "response_page": [
                    {
                        "profile_type": "response_page",
                        "response_code": 404,
                        "response_content_type": "Profile",
                        "profile_file": {
                            "name": "manipulation_profile_page",
                            "model": "create",
                            "file": "testa.html->"
                        },
                    }
                ]
            },
            "expected_return": "https://www.daixiaorui.com",
            "counters": {"hits": 2},
            "log_query_param": [{"query_field_key": "http_host", "query_value": "www.baidu.com"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv --connect-timeout 30 --max-time 60 https://www.baidu.com"
            },
            "token": ""
        }

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        # name_list汇总
        name_list = get_name_list(test_data)

        # 添加测试过程中涉及的template
        template_path = {}
        template_path["trex_workpath"] = "/opt/trex/v3.03"
        template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"

        # 创建object
        if "condition" in test_data.keys():
            for cond_key, cond_value in (test_data["condition"].items()):
                if cond_key in manipulation_object_no_create_list:
                    continue   # 直接跳过
                cond_status = 0
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
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(cond_key_out), flush=True)
                        else:
                            result = "Fail to create {} object.".format(cond_key_out)
                            cond_status = 1
                            break
                if cond_status == 1:   # 创建失败，退出遍历创建
                    break

        # 创建profile
        prfi_code = 200
        if "action_parameter" in test_data.keys():
            for prfi_key, prfi_value in(test_data["action_parameter"]).items():
                if prfi_key in manipulation_profile_no_create_list:
                    continue  # 直接跳过
                prfi_status = 0
                prfi_key_out = prfi_key.replace("_", " ")
                if len(prfi_value) != 0:   # 需要创建profile数据
                    prfi_data = prfi_value
                    prfi = CreateProfile(driver)
                    for i in range(len(prfi_data)): # 遍历创建所有 profile
                        element_position_map = get_element_position(prfi_key)
                        prfi_code = prfi.create(prfi_data[i], element_position_map)
                        if prfi_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(prfi_key_out), flush=True)
                        else:
                            result = "Fail to create {} profile.".format(prfi_key_out)
                            prfi_status = 1
                            break
                if prfi_status == 1:  # 创建失败，退出遍历创建
                    break

        # 创建rule
        if cond_code == 200 and prfi_code == 200:
            create_rule = CreateRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            # 添加deny quic 和 intercept
            tmp_name_list = create_pre_policy(test_data, driver)
            for tmp in tmp_name_list:
                name_list.insert(0, copy.deepcopy(tmp))
            create_rule_code = create_rule.create(test_data, element_position_map)
            if create_rule_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create manipulation rule successfully.", flush=True)
            elif create_rule_code != 200:
                result = "Fail to create manipulation rule."

        # 触发流量验证
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], element_position_map)
            if search_rule_code == 200:
                test_data["rule_id"] = rule_id
                verify = TrafficVerification()
                verification_result = verify.traffic_verification(driver, parameter, test_data, [])
                if len(verification_result) == 4:
                    driver = verification_result[3]
                elif len(verification_result) == 5:
                    driver = verification_result[4]
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Traffic verification failed", flush=True)

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
            # 删除提前先发的security intercept策略
            delete_pre_policy(tmp_name_list, driver)
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], element_position_map)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete manipulation rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete {} rule.".format(test_data["policy_type"])
            else:
                result = result + " In addition, fail to search {} rule.".format(test_data["policy_type"])

        # 删除object
        if delete_rule_code == 200 and "condition" in test_data.keys():
            # 删除
            for cond_key, cond_value in (test_data["condition"].items()):  # 遍历所有cond数据
                if cond_key in manipulation_object_no_create_list:
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
                        search_cond_code, first_row_checkbox_element = search_cond.search(cond_data[i]["name"], element_position_map)
                        if search_cond_code == 200:
                            delete_cond = DeleteObject(driver)
                            delete_cond_code = delete_cond.delete(element_position_map, first_row_checkbox_element, True)
                            if delete_cond_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(cond_key_out), flush=True)
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
        if delete_rule_code == 200 and "action_parameter" in test_data.keys():
            # 删除
            for prfi_key, prfi_value in (test_data["action_parameter"].items()):  # 遍历所有cond数据
                if prfi_key in manipulation_profile_no_create_list:
                    continue  # 直接跳过
                prfi_status = 0
                prfi_key_out = prfi_key.replace("_", " ")
                if len(prfi_value) != 0:  # 不为空
                    for i in range(len(prfi_value)):  # 遍历查询所有profile
                        search_prfi = SearchProfile(driver)
                        element_position_map = get_element_position(prfi_key)
                        prfi_name = prfi_value[i]["profile_file"]["name"].strip()
                        search_prfi_code, first_row_checkbox_element = search_prfi.search(prfi_name, element_position_map)
                        if search_prfi_code == 200:
                            delete_prfi = DeleteProfile(driver)
                            delete_prfi_code = delete_prfi.delete(element_position_map, first_row_checkbox_element, True)
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

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        traceback.print_exc()
        return "Error: " + str(e)
    finally:
        # 清理环境
        support.ui_utils.env.teardown()
        # 删除配置
        delete = DeletePolicy()
        #delete.delete_policy_by_name(token, parameter, name_list)
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
        "username": "zcw3",
        "password": "qa111111",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "ui",
        "is_log": 0,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "manipulation",
        "test_case_name": "deny_srcip_dstport_responseProfile"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """