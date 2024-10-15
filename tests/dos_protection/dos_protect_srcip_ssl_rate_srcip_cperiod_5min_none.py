# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from datetime import datetime
from support.report_update import ReportUpdate
from support.instance_utils.case_instance_generator import CaseInstanceGenerator

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        exception_result = ""
        result = {}
        
        # 脚本启动时间
        start_time = time.time()
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "dos_protection",
            "rule_name": os.path.splitext(os.path.basename(__file__))[0],
            "rule_action": "protect",
            "rule_type": "create",
            "do_log" : 2,
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
                        "name": "ssl",
                        "object_type": "application",
                        "negate": False
                    }
                ]
            },
            "threshold": {
                "type": "rate",
                "rate_threshold": {
                    "group_by": "source_ip",
                    "request_per_period": 1,
                    "counting_period": "5min"
                }
            },
            "mitigation": {
                "behavior": "deny",
                "timeout": "10s"
            },
            "expected_return": "",
            "counters": {"hits": "many"},
            "log_query_param": [
                {"query_field_key": "attack_type", "query_value": "custom_network_attack"},
                {"query_field_key": "sessions", "query_value": ""},
                {"query_field_key": "packets", "query_value": ""},
                {"query_field_key": "bytes", "query_value": ""},
                {"query_field_key": "bit_rate", "query_value": ""},
                {"query_field_key": "packet_rate", "query_value": ""},
                {"query_field_key": "session_rate", "query_value": ""},

                {"query_field_key": "rule_id", "query_value": ""},
                {"query_field_key": "conditions", "query_value": ""},
                {"query_field_key": "source_ip_list", "query_value": ""},
                {"query_field_key": "source_country_list", "query_value": "Private Network"},
                {"query_field_key": "destination_ip", "query_value": ""},
                {"query_field_key": "destination_country", "query_value": "US"},
            ],
            "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "1.1.1.1",
                "clients_end_ip": "1.1.1.1",
                "servers_start_ip": "2.1.2.32",
                "servers_end_ip": "2.1.2.32",
                "m": 2,
                "d": 5,
                "yaml_name": "test",
                "pcap_name": "ssl_tls13"
            },
            "token": ""
        }
        
        # 测试用例实例化
        case_instance_generator = CaseInstanceGenerator(test_data, parameter)
        result = case_instance_generator.create()
        
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        if isinstance(case_instance_generator, CaseInstanceGenerator):
            case_instance_generator.delete_data()
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
            
if __name__ == '__main__':
    parameter = {
        "username": "lina2024",
        "password": "lina2024",
        "test_pc_ip": "192.168.64.96",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "E:/tsg_test",
        "path": "E:/tsg_test/tests/ui",
        "module_name": "dos_protection",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)