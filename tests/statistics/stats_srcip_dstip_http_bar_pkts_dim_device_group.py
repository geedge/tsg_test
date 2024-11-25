# -*- coding: UTF-8 -*-
import os
import sys
import time
import pytz

from support.organize_config import OrganizeConfig
from support.ui_utils.element_position.map_element_position_library import replace_paras
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
        start_time = time.time()

        policy_configuration = {
            "name": parameter["test_case_name"],
            "type": "statistics",
            "action": "statistics",
            "and_conditions": [
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "name": parameter["test_case_name"].replace("_dstip", "", 1),
                            "attribute_name": "ATTR_SOURCE_IP",
                            "type": "ip",
                            "member_type": "item",
                            "items": [
                                {
                                    "op": "add",
                                    "ip": "10.64.224.31",
                                    "interval": "1-65535"
                                }
                            ]
                        }
                    ]
                },
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "name": parameter["test_case_name"].replace("_srcip", "", 1),
                            "attribute_name": "ATTR_DESTINATION_IP",
                            "type": "ip",
                            "sub_type": "ip",
                            "statistics_option": "none",
                            "member_type": "item",
                            "items": [
                                {
                                    "op": "add",
                                    "ip": "2.1.1.9",
                                    "interval": "0-65535"
                                }
                            ]
                        }
                    ]
                },
                {
                    "negate_option": 0,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_APP_ID",
                            "type": "application",
                            "items": ["http"]
                        }
                    ],
                }
            ],
            "action_parameter": {
                "template_profile": {
                    "name": parameter["test_case_name"].replace("_srcip_dstip", "", 1),
                    "uuid": "",
                    "dataview": {
                        "charts": [
                            {
                                "id": "",
                                "display": {
                                    "page_x": None,
                                    "page_y": None,
                                    "height": "",
                                    "width": "",
                                    "type": "bar",
                                    "table_type": ""
                                },
                                "uuid": "",
                                "name": "RATE(Packets Sent, Packets Received) Distributed by Device Group",
                                "threshold": {
                                    "in_bytes": 0,
                                    "out_bytes": 0
                                },
                                "query": {
                                    "dimensions": [
                                        {
                                            "source_fields": [
                                                "device_group"
                                            ],
                                            "function": {
                                                "name": "",
                                                "expression": "",
                                                "variables": [

                                                ]
                                            },
                                            "label": "Device Group",
                                            "is_drill_down": 0
                                        }
                                    ],
                                    "limit": "99",
                                    "metrics": [
                                        {
                                            "source_fields": [
                                                "sent_pkts",
                                                "received_pkts"
                                            ],
                                            "function": {
                                                "name": "SUM",
                                                "expression": "",
                                                "variables": [

                                                ]
                                            },
                                            "metric_type": "count",
                                            "metric_name": "count_1",
                                            "label": "SUM(Packets Sent, Packets Received)",
                                            "unit": "packets"
                                        }
                                    ],
                                    "order_by": "SUM(Packets Sent, Packets Received)",
                                    "source": "statistics_rule",
                                    "series_limit": ""
                                }
                            },
                            {
                                "id": "",
                                "display": {
                                    "page_x": None,
                                    "page_y": None,
                                    "height": "",
                                    "width": "",
                                    "type": "bar",
                                    "table_type": ""
                                },
                                "uuid": "",
                                "name": "SUM(Packets Sent) Distributed by Device Group",
                                "threshold": {
                                    "in_bytes": 0,
                                    "out_bytes": 0
                                },
                                "query": {
                                    "dimensions": [
                                        {
                                            "source_fields": [
                                                "device_group"
                                            ],
                                            "function": {
                                                "name": "",
                                                "expression": "",
                                                "variables": [

                                                ]
                                            },
                                            "label": "Device Group",
                                            "is_drill_down": 0
                                        }
                                    ],
                                    "limit": "50",
                                    "metrics": [
                                        {
                                            "source_fields": [
                                                "sent_pkts"
                                            ],
                                            "function": {
                                                "name": "SUM",
                                                "expression": "",
                                                "variables": [

                                                ]
                                            },
                                            "metric_type": "count",
                                            "metric_name": "count_1",
                                            "label": "SUM(Packets Sent)",
                                            "unit": "packets"
                                        }
                                    ],
                                    "order_by": "SUM(Packets Sent)",
                                    "source": "statistics_rule",
                                    "series_limit": ""
                                }
                            },
                            {
                                "id": "",
                                "display": {
                                    "page_x": None,
                                    "page_y": None,
                                    "height": "",
                                    "width": "",
                                    "type": "bar",
                                    "table_type": ""
                                },
                                "uuid": "",
                                "name": "SUM(Packets Received) Distributed by Device Group",
                                "threshold": {
                                    "in_bytes": 0,
                                    "out_bytes": 0
                                },
                                "query": {
                                    "dimensions": [
                                        {
                                            "source_fields": [
                                                "device_group"
                                            ],
                                            "function": {
                                                "name": "",
                                                "expression": "",
                                                "variables": [

                                                ]
                                            },
                                            "label": "Device Group",
                                            "is_drill_down": 0
                                        }
                                    ],
                                    "limit": 100,
                                    "metrics": [
                                        {
                                            "source_fields": [
                                                "received_pkts"
                                            ],
                                            "function": {
                                                "name": "SUM",
                                                "expression": "",
                                                "variables": [

                                                ]
                                            },
                                            "metric_type": "count",
                                            "metric_name": "count_1",
                                            "label": "SUM(Packets Received)",
                                            "unit": "packets"
                                        }
                                    ],
                                    "order_by": "SUM(Packets Received)",
                                    "source": "statistics_rule",
                                    "series_limit": ""
                                }
                            }
                        ]
                    },
                    "vsys": 1
                }
            },
            "is_enabled": 1,
            "log_option": "metadata"
        }

        traffic_generation = {
            "tool": "trex",  # or trex/http
            "clients_start_ip": "10.64.224.9",
            "clients_end_ip": "10.64.224.9",
            "servers_start_ip": "2.1.1.9",
            "servers_end_ip": "2.1.1.9",
            "m": 1,
            "d": 1,
            "yaml_name": "test",
            "pcap_name": "http_87pkts"
        }

        verification_result = {
            "excepted_traffic_result": {"total_bytes": 94679, "total_bytes_received": 93284, "total_bytes_sent": 1395, "total_packets": 87, "total_packets_received": 65, "total_packets_sent": 22, "total_syn_pkt": 1},
            "expected_query": {"hits": 1},
            "expected_log": [
                {"query_field_key": "decoded_as", "query_value": "HTTP"},
                {"query_field_key": "server_fqdn", "query_value": "www.yumi.com"}
            ]
        }
        # 创建
        if parameter["initiation_method"] == "ui":
            ui_client = UIClient()
            rules_tuple, ui_error = ui_client.create_rules(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
        elif parameter["initiation_method"] == "api":
            api_client = APIClient(parameter)

            organize_config = OrganizeConfig(parameter, policy_configuration, api_client.token, ())
            organize_config.generate_random_ip(parameter, policy_configuration, traffic_generation)

            # {uuid, type}, i.e., {"12341-232-a21", "ip"}
            objects_tuple, api_error = api_client.create_objects(policy_configuration)
            if len(api_error) > 0:
                return api_error
            # 处理Profiles
            profiles_tuple, api_error = api_client.create_profiles(policy_configuration)
            if len(api_error) > 0:
                return api_error
            rules_tuple, api_error = api_client.create_rules(policy_configuration, objects_tuple, "", profiles_tuple)
            if len(api_error) > 0:
                return api_error
        # 等待下发配置生效
        time.sleep(3)

        # 类实例化
        generator = TrafficGenerator()

        # 获取当前时间
        utc_tz = pytz.timezone('UTC')
        current_utc_time = datetime.now(utc_tz)
        traffic_start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

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
            log_result = api_client.query_rule_log(traffic_generation, verification_result, rules_tuple, traffic_start_time, traffic_result)
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
            metric_result = api_client.query_rule_metric(verification_result, rules_tuple, traffic_start_time, traffic_result)
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"DEBUG:Case:{},log_result:{},excepted_traffic_result:{},metric_result:{}".format(os.path.basename(__file__)[:-3], log_result, excepted_traffic_result, metric_result),  flush=True)
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
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "When running test case, the exception error: ", str(e), flush=True)
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
            if profiles_tuple:
                api_client.delete_profiles(profiles_tuple)

        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Finish test case: " + parameter["test_case_name"], flush=True)
    # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)

if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.73",
        "api_server": "http://192.168.44.72",
        "is_log": 0,
        "env": "tsgx",
        "vsys": 1,  # 6
        "root_path": "D:/tsgcode/tsg_test",
        "path": "tsgcode/tsg_test/testcase/ui",
        "module_name": "statistics",
        "test_case_name": os.path.basename(__file__)[:-3],
        "debug_flag": "local",
        "test_subcriber_id": "test6489",
        "initiation_method": "api",
        "policy_type": "statistics"
    }
    parameter = replace_paras(parameter)
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例:
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）:
    allure serve allure
    """