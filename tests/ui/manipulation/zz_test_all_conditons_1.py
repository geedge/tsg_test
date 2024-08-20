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
from support.traffic_manager.verification import Verification
from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
import support.ui_utils.env
import traceback
from support.api_utils.delete_policy import *
from support.report import *
from datetime import datetime
import concurrent
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED, ProcessPoolExecutor

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        result = ""
        
        # 脚本启动时间
        start_time = time.time()

        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "pxy_manipulation",
            "rule_name": parameter["test_case_name"],
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
                "application": [
                    {
                        "name": "http",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                    {
                        "name": "manipulation_fqdn_node",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "fqdn",
                                "item_value": "baidu.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "manipulation_url",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                "item_value": "baidu"
                            }
                        ],
                    },
                    {
                        "name": "manipulation_http_signature",
                        "object_type": "http_signature",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "request_header",
                                "item_key": "User-Agent",
                                "item_value": "TEXT",
                                "value": [
                                    "Chrome"
                                ]
                            }
                        ],
                    },
                    {
                        "name": "manipulation_res_header_http_signature",
                        "object_type": "http_signature",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "response_header",
                                "item_key": "Content-Type",
                                "item_value": "TEXT",
                                "value": [
                                    "text/html"
                                ]
                            }
                        ],
                    },
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
                            "file": "testa.html"
                        },
                    }
                ]
            },
            "expected_return": "https://www.daixiaorui.com",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key": "http_host", "query_value": "www.baidu.com"}],
            "traffic": {
                "protocol": "ssl",
                "type": "curl",
                "command": "curl --compressed -kv --connect-timeout 30 --max-time 60 --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" https://www.baidu.com"
            },
            "token": ""
        }
        test_data = parameter["test_data"]

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        # name_list汇总
        name_list = get_name_list(test_data)
        name_list.insert(0, {
                    "type": "pxy_intercept",
                    "name": "manipulation_pre_intercept",
                    })

        # 添加测试过程中涉及的template
        template_path = {}
        template_path["trex_workpath"] = "/opt/trex/v3.03"
        template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"

        # 创建object
        data_list = []
        if "condition" in test_data.keys():
            for cond_key, cond_value in (test_data["condition"].items()):
                if cond_key in manipulation_object_no_create_list:
                    continue   # 直接跳过
                if len(cond_value) != 0:  # 不为空
                    for tmp_0 in cond_value:
                        tmp_key = cond_key
                        if cond_key == "protocol_filed":
                            tmp_key = tmp_0["object_type"]
                        data_list.append({"module_type": "condition", "data_type": tmp_key, "value": tmp_0})

        # 创建profile
        prfi_code = 200
        if "action_parameter" in test_data.keys():
            for prfi_key, prfi_value in(test_data["action_parameter"]).items():
                if prfi_key in manipulation_profile_no_create_list:
                    continue  # 直接跳过
                if len(prfi_value) != 0:
                    for tmp_0 in prfi_value:
                        data_list.append({"module_type": "profile", "data_type": prfi_key, "value": tmp_0})


        result_code = concurrent_operate_object_and_profile(data_list, operation="create")

        concurrent_operate_rule(test_data, operation="create")

        # 环境初始化
        support.ui_utils.env.initiate_selenium_request()
        driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()
        create_rule_code = 200
        # 触发流量验证
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], element_position_map)
            if search_rule_code == 200:
                test_data["rule_id"] = rule_id
                verify = Verification()
                verification_result = verify.verification(driver, parameter, test_data, [], element_position_map)
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


        concurrent_operate_rule(test_data, operation="delete")

        concurrent_operate_object_and_profile(data_list, operation="delete")

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

def operate_object_and_profile(data_dict, element_position_map, operation="create"):
    # 获取当前线程和进程的信息
    thread_id = threading.get_ident()
    process_id = os.getpid()
    thread_info = f"Thread ID: {thread_id}, Process ID: {process_id}"
    module_type = data_dict["module_type"]
    data_type = data_dict["data_type"]
    data_value = data_dict["value"]
    # 环境初始化
    support.ui_utils.env.initiate_selenium_request()
    driver = support.ui_utils.env.my_driver()
    support.ui_utils.env.setup()
    try:
        if module_type == "condition":
            if operation == "create":
                create_cond = CreateObject(driver)
                result_code = create_cond.create(data_value, element_position_map)
            elif operation == "delete":
                search_cond = SearchObject(driver)
                tmp_name = data_value["name"].strip()
                search_cond_code, first_row_checkbox_element = search_cond.search(tmp_name, element_position_map)
                delete_cond = DeleteObject(driver)
                result_code = delete_cond.delete(element_position_map, first_row_checkbox_element, True)
            else:
                print("error")
        elif module_type == "profile":
            if operation == "create":
                prfi = CreateProfile(driver)
                result_code = prfi.create(data_value, element_position_map)
            elif operation == "delete":
                search_prfi = SearchProfile(driver)
                tmp_name = data_value["profile_file"]["name"].strip()
                search_prfi_code, first_row_checkbox_element = search_prfi.search(tmp_name, element_position_map)
                delete_prfi = DeleteProfile(driver)
                result_code = delete_prfi.delete(element_position_map, first_row_checkbox_element, True)
            else:
                print("error")
        else:
            print("error")
        if result_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{}, {} {} {} successfully.".format(thread_info, operation, module_type, data_type), flush=True)
        else:
            result = "{}, Fail to create {} {}.".format(thread_info, module_type, data_type)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{}, {} {} {} failed.".format(thread_info, operation, module_type, data_type), flush=True)
    finally:
        driver.quit()
    return result_code

def concurrent_operate_object_and_profile(data_list, operation="create"):
    #with concurrent.futures.ProcessPoolExecutor(max_workers=4) as p_executor_pool:
    p_executor_pool = ProcessPoolExecutor(max_workers=4)
    print(len(data_list))
    print(data_list)
    all_task = []
    for item in data_list:
        time.sleep(1)
        cond_key = item["data_type"]
        if cond_key == "protocol_filed":
            tmp_key = item["value"]["object_type"]
            element_position_map = get_element_position(tmp_key)
        else:
            element_position_map = get_element_position(cond_key)
        task_0 = p_executor_pool.submit(operate_object_and_profile, item, element_position_map, operation)
        all_task.append(task_0)

    for future0 in as_completed(all_task):
        data = future0.result()
        #print("result: ", data)
        result_code = data

    p_executor_pool.shutdown()
    return result_code

def operate_rule(data_dict, policy_type, operation="create"):
    # 获取当前线程和进程的信息
    thread_id = threading.get_ident()
    process_id = os.getpid()
    thread_info = f"Thread ID: {thread_id}, Process ID: {process_id}"
    # 环境初始化
    support.ui_utils.env.initiate_selenium_request()
    driver = support.ui_utils.env.my_driver()
    support.ui_utils.env.setup()
    try:
        if operation == "create":
            create_rule = CreateRule(driver)
            element_position_map = get_element_position(data_dict["policy_type"])
            # 添加deny quic 和 intercept
            if policy_type == "pxy_intercept":
                tmp_name_list = create_pre_policy(data_dict, driver)
            elif policy_type == "prx_manipulation":
                create_rule_code = create_rule.create(data_dict, element_position_map)
                if create_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{}, Create manipulation rule successfully.".format(thread_info), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{}, Create manipulation rule faided.".format(thread_info), flush=True)
            else:
                print("error policy type")
        elif operation == "delete":
            if policy_type == "pxy_intercept":
                # 删除提前先发的security intercept策略
                tmp_name_list = [{
                    "type": "pxy_intercept",
                    "name": "manipulation_pre_intercept",
                    }]
                delete_pre_policy(tmp_name_list, driver)
            elif policy_type == "prx_manipulation":
                search_rule = SearchRule(driver)
                element_position_map = get_element_position(data_dict["policy_type"])
                search_rule_code, first_row_checkbox_element = search_rule.search(data_dict["policy_type"], data_dict["rule_name"], element_position_map)
                if search_rule_code == 200:
                    delete_rule = DeleteRule(driver)
                    delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                    if delete_rule_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{}, Delete manipulation rule successfully.".format(thread_info), flush=True)
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{}, Delete manipulation rule failed.".format(thread_info), flush=True)
    finally:
        driver.quit()

def concurrent_operate_rule(data_list, operation="create"):
    p_executor_pool = ProcessPoolExecutor(max_workers=2)
    all_task = []
    task_0 = p_executor_pool.submit(operate_rule, data_list, "pxy_intercept", operation=operation)
    task_1 = p_executor_pool.submit(operate_rule, data_list, "prx_manipulation", operation=operation)
    all_task.append(task_0)
    all_task.append(task_1)

    for future0 in as_completed(all_task):
        data = future0.result()
        #print("result: ", data)

    p_executor_pool.shutdown()








if __name__ == '__main__':

    parameter = {
        "username": "zcw3",
        "password": "qa111111",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "ui",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "manipulation",
        "test_case_name": os.path.basename(__file__)[:-3],
        "test_data": {},
    }


    test_data = {
        "is_multi_priority": False,
        "rule_num": 1,
        "policy_type": "pxy_manipulation",
        "rule_name": parameter["test_case_name"],
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
                        "file": "testa.html"
                    },
                }
            ]
        },
        "expected_return": "https://www.daixiaorui.com,404",
        "counters": {"hits": 1},
        "log_query_param": [{"query_field_key": "http_host", "query_value": "www.baidu.com"}],
        "traffic": {
            "protocol": "ssl",
            "type": "curl",
            "command": "curl -kv --connect-timeout 30 --max-time 60 https://www.baidu.com"
        },
        "token": ""
    }



    parameter["test_data"] = test_data
    parameter = replace_paras(parameter)
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    ##pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """