# -*- coding: UTF-8 -*-
import time
import os
import sys

from support.ui_utils.element_position.map_element_position_library import replace_paras

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import traceback
from datetime import datetime
from support.instance_utils.case_instance_generator import CaseInstanceGenerator
from support.report_update import ReportUpdate


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        exception_result = ""
        result = {}

        # 脚本启动时间
        start_time = time.time()

        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "statistics",
            "rule_name": parameter["test_case_name"],
            "rule_action": "statistics",
            "rule_type": "create",
            "debug_flag": "local",
            "test_subcriber_id": "test6489",
            "script_type": "ui",
            "condition": {
                "source_ip": [
                    {
                        "name": parameter["test_case_name"].replace("_dstip", "", 1),
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "10.64.224.31",
                            },
                        ]
                    }
                ],
                "source_port": [],
                "destination_ip": [
                    {
                        "name": parameter["test_case_name"].replace("_srcip", "", 1),
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "2.1.1.3",
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
                        "name": "ssl",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [
                ],
                "packet_capture": []
            },
            "action_parameter": {
                "statistics_template": [{
                    "name": parameter["test_case_name"].replace("_srcip_dstip", "", 1),
                    "profile_type": "statistics_template",
                    "charts": [
                        {
                          "chart_name": parameter["test_case_name"].replace("_srcip_dstip", "", 1),
                          "visualization_type": "Bar",
                          "metrics": [
                              "syn_pkts:RATE:SYN Packets RATE"
                          ],
                          "dimensions": [
                            "ssl_sni"
                          ],
                          "order_by": "SYN Packets RATE",
                          "row_limit": "100",
                          "min_in_size": "0",
                          "min_out_size": "0"
                        }
                      ]
                }]
            },
            "expected_return": "reset",
            "counters": {"hits": 1},
            "log_query_param": [
                {"query_field_key": "ssl_sni", "query_value": "www.bbc.com"}
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
                "pcap_name": "ssl_tls13"
            },
            "statists_metric_results": [#如果Bytes Aggregate为:BITRATE则Bytes*8
                {"client_ip": "10.64.14.213", "in_bytes": 13209, "out_bytes": 454788, "bytes": 3743976}
            ],
            # "traffic": {
            #     "type": "trex",
            #     "clients_start_ip": "192.168.64.86",
            #     "clients_end_ip": "192.168.64.86",
            #     "servers_start_ip": "2.1.1.1",
            #     "servers_end_ip": "2.1.1.2",
            #     "m": 1,
            #     "d": 1,
            #     "yaml_name": "test",
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
        # 测试用例实例化
        case_instance_generator = CaseInstanceGenerator(test_data, parameter)
        result = case_instance_generator.create()

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
        if isinstance(case_instance_generator, CaseInstanceGenerator):
            case_instance_generator.clean_up()
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)

if __name__ == '__main__':
    parameter = {

        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.73",
        "api_server": "http://192.168.44.72",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,  # 6
        "root_path": "D:/tsgcode/tsg_test",
        "path": "tsgcode/tsg_test/testcase/ui",
        "module_name": "statistics",
        "test_case_name": os.path.basename(__file__)[:-3],
        "debug_flag": "local",
        "test_subcriber_id": "test6489",
        "script_type": "ui",
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