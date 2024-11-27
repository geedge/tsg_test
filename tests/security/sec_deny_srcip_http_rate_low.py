# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from datetime import datetime
from support.report_update import ReportUpdate
from support.common_utils.create_policy import CreatePolicy

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        exception_result = ""
        result = {}
        
        # 脚本启动时间
        script_start_time = time.time()
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_name": "sec_deny_srcip_http_rate_low",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "sec_srcip",
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
                        "name": "http", #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [
                    {
                        "type": "rate_limit",
                        "rate_value": "0.1",
                    }
                ],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "timed out",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key":"http_host", "query_value": "open.node.com"}],
            "traffic": {
                "protocol": "http",
                "type": "curl",
                "command": "curl -kv --connect-timeout 10 -m 10 http://open.node.com:180"
            },
            "token": ""
        }
        # 测试用例实例化
        create = CreatePolicy(test_data, parameter)
        result = create.create_policy()
        
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        if isinstance(create, CreatePolicy):
            create.clean_up()
        # 统计脚本用时
        script_end_time = time.time()
        duration = script_end_time - script_start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
            
if __name__ == '__main__':
    # ui
    # parameter = {
    #     "username": "hebingning",
    #     "password": "hbn66AAA",
    #     "test_pc_ip": "192.168.64.65",
    #     "test_subcriber_id": "test6776",
    #     "api_server": "http://192.168.44.72",
    #     "debug_flag": "local",
    #     "script_type": "ui",
    #     "env": "tsgx",
    #     "vsys_id": 1,
    #     "is_log": 1,
    #     "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
    #     "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
    #     "module_name": "security",
    #     "test_case_name": "deny_srcip_fqdn_drop_rst_icmp"
    # }
    # run(parameter)
    # api
    from support.ui_utils.element_position.map_element_position_library import replace_paras
    from support.ui_utils.workpath import workdir

    parameter = {
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "api",  # api  ui  空字符串
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/tests/api",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    run(parameter)

# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from datetime import datetime
from support.report_update import ReportUpdate
from support.common_utils.create_policy import CreatePolicy

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        exception_result = ""
        result = {}
        
        # 脚本启动时间
        script_start_time = time.time()
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_name": "sec_deny_srcip_http_pre_url_alert_200_profile",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "sec_srcip",
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
                        "name": "http", #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [
                    {
                        "name": "sec_url",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                "item_value": "open.node*"
                            }
                        ],
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                    {
                        "type": "alert",
                        "code": 200,
                        "content_type": "Profile",
                        "content": "sec_respage"
                    }
                ],
                "packet_capture": []
            },
            "action_parameter": {
                "response_page": [
                    {
                        "profile_type": "response_page",
                        "response_code": 200,
                        "response_content_type": "Profile",
                        "profile_file": {
                            "name": "sec_respage",
                            "model": "create",
                            "file": "response_testa.html"
                        },
                    }
                ]
            },
            "profile": [],
            "expected_return": "200",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key":"http_host", "query_value": "open.node.com"},
                                {"query_field_key":"http_url", "query_value": "open.node.com:180/"},
                                {"query_field_key": "decoded_as", "query_value": "HTTP"},
                                {"query_field_key":"security_action","query_value":"deny"}],
            "traffic": {
                "protocol": "http",
                "type": "wget",
                "command": "wget -q --debug http://open.node.com:180"
            },
            "token": ""
        }
        # 测试用例实例化
        create = CreatePolicy(test_data, parameter)
        result = create.create_policy()
        
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        if isinstance(create, CreatePolicy):
            create.clean_up()
        # 统计脚本用时
        script_end_time = time.time()
        duration = script_end_time - script_start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
            
if __name__ == '__main__':
    # ui
    # parameter = {
    #     "username": "hebingning",
    #     "password": "hbn66AAA",
    #     "test_pc_ip": "192.168.64.65",
    #     "test_subcriber_id": "test6776",
    #     "api_server": "http://192.168.44.72",
    #     "debug_flag": "local",
    #     "script_type": "ui",
    #     "env": "tsgx",
    #     "vsys_id": 1,
    #     "is_log": 1,
    #     "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
    #     "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
    #     "module_name": "security",
    #     "test_case_name": "deny_srcip_fqdn_drop_rst_icmp"
    # }
    # run(parameter)
    # api
    from support.ui_utils.element_position.map_element_position_library import replace_paras
    from support.ui_utils.workpath import workdir

    parameter = {
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "api",  # api  ui  空字符串
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/tests/api",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    run(parameter)

# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
import pytz
from datetime import datetime
from support.ui_utils.workpath import workdir
from support.ui_utils.ui_client import UIClient
from support.api_utils.api_client import APIClient
from support.packet_generator.traffic_generator import *
from support.report_update import ReportUpdate

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        
        # 参数初始化
        result, exception_result = "", ""
        test_summary = {}
        
        # 脚本启动时间
        script_start_time = time.time()
        
        policy_configuration = {
            "name": os.path.splitext(os.path.basename(__file__))[0],
            "type": "security",
            "action": "deny",
            "and_conditions": [
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_SOURCE_IP",
                            "type": "ip",
                            "sub_type": "ip",
                            "name": "sec_srcip",
                            "items": [
                                {
                                    "op": "add",
                                    "ip": parameter['test_pc_ip'],
                                    "interval": "0-65535"
                                }
                            ]
                        }
                    ]
                },
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_APP_ID",
                            "type": "application",
                            "items": ["http"]
                        }
                    ],
                },
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_HTTP_URL",
                            "name": "sec_url",
                            "type": "url",
                            "statistics_option": "none",
                            "member_type": "item",
                            "items": [
                                {
                                    "op": "add",
                                    "expr_type": "and",
                                    "expression": "^open.node"
                                }
                            ]
                        }
                    ]
                }
            ],
            "action_parameter": {
                "sub_action": "drop",
                "packet_capture": {
                    "enable": 0
                },
                "send_tcp_reset": 1,
                "send_icmp_unreachable": 0,
                "after_n_packets": 0
            },
            "is_enabled": 1,
            "log_option": "metadata",
        }
        
        traffic_generation = {
            "tool": "http", # or trex/http
            "command": "wget -q --debug http://open.node.com:180"
        }
        
        verification_result = {
            "excepted_traffic_result": "200",
            "expected_metric": {"hits": 1},
            "expected_log": [
                {"query_field_key":"http_host", "query_value": "open.node.com"},
                {"query_field_key":"http_url", "query_value": "open.node.com:180/"},
                {"query_field_key": "decoded_as", "query_value": "HTTP"},
                {"query_field_key":"security_action","query_value":"deny"}
            ]
        }
        
        # 创建
        if parameter["initiation_method"] == "ui":
            ui_client = UIClient()
            objects_tuple, ui_error = ui_client.create_objects(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
            rules_tuple, ui_error = ui_client.create_rules(policy_configuration, objects_tuple)
            if len(ui_error) > 0:
                return ui_error
        elif parameter["initiation_method"] == "api":
            api_client = APIClient(parameter)
            # {uuid, type}, i.e., {"12341-232-a21", "ip"}
            objects_tuple, api_error = api_client.create_objects(policy_configuration)
            if len(api_error) > 0:
                return api_error
            rules_tuple, api_error = api_client.create_rules(policy_configuration, objects_tuple, "", "")
            if len(api_error) > 0:
                return api_error

        # 等待下发配置生效
        time.sleep(3)
        
        # 类实例化
        generator = TrafficGenerator()
        
        # 获取当前时间
        utc_tz = pytz.timezone('UTC')
        current_utc_time = datetime.now(utc_tz)
        start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # 触发流量
        traffic_result = generator.run(policy_configuration, traffic_generation)
        
        # 验证流量生成器的返回值是否符合策略执行的预期
        excepted_traffic_result, error = generator.result(verification_result, traffic_result)
        if excepted_traffic_result == False:
            return error
        
        # 验证tsg的日志是否符合策略执行的预期
        if parameter["initiation_method"] == "ui":
            log_result = ui_client.query_rule_log(verification_result, rules_tuple, traffic_result)
        elif parameter["initiation_method"] == "api":
            log_result = api_client.query_rule_log(traffic_generation, verification_result, rules_tuple, start_time, traffic_result)
        if log_result == True:
            test_summary["log"] = "Pass."
        elif log_result == False:
            test_summary["log"] = "The failure reason: the returned log does not match the expected result."
        elif log_result == None:
            test_summary["log"] = "The failure reason: the returned log is empty."
        elif len(log_result) > 0:
            test_summary["log"] = log_result
            
        # 验证tsg的metric是否符合策略执行的预期
        if parameter["initiation_method"] == "ui":
            metric_result = ui_client.query_rule_metric(verification_result, traffic_result)
        elif parameter["initiation_method"] == "api":
            metric_result = api_client.query_rule_metric(verification_result, rules_tuple, start_time, traffic_result)
        if metric_result == True:
            test_summary["metric"] = "Pass."
        elif metric_result == False:
            test_summary["metric"] = "The failure reason: the returned metric does not match the expected result."
        elif metric_result == None:
            test_summary["metric"] = "The failure reason: the returned metric is empty."
        elif len(metric_result) > 0:
            test_summary["metric"] = metric_result
        
        return test_summary
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When running test case, the exception error: ", str(e), flush=True)
        return "When running test case, the exception error: " + str(e)
    finally:
        # 删除
        if parameter["initiation_method"] == "ui":
            if rules_tuple:
                ui_client.delete_rules(parameter, policy_configuration)
        elif parameter["initiation_method"] == "api":
            if rules_tuple:
                api_client.delete_rules(rules_tuple)
            if objects_tuple:
                api_client.delete_objects(objects_tuple)
        
        # 统计脚本用时
        script_end_time = time.time()
        duration = script_end_time - script_start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
        
if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "initiation_method": "api",
        "env": "tsgx",
        "vsys": 5,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)