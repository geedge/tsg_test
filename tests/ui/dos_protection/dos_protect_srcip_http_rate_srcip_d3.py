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
from support.api_utils.create_policy import CreatePolicy
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import DeletePolicy
import support.ui_utils.env
from support.common.report import *
from datetime import datetime
from support.common.data_translation import DataTranslation
from support.common.generate_csv import GenerateCSV
from support.common.case_generator import CaseGenerator

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
            "rule_name": "dos_protect_srcip_http_rate_srcip_d3",
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
                        "name": "http",
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
                    "counting_period": "10s"
                }
            },
            "mitigation": {
                "behavior": "deny",
                "timeout": "10s"
            },
            "expected_return": "",
            "counters": {"hits": "many"},
            "log_counter": 1,
            "log_query_param": [
                {
                    "query_field_key": "attack_type",
                    "query_value": "custom_network_attack"
                },
                {
                    "query_field_key": "sessions",
                    "query_value": 2
                },
                {
                    "query_field_key": "session_rate",
                    "query_value": 0
                },
                {
                    "query_field_key": "packets",
                    "query_value": 8
                },
                {
                    "query_field_key": "packet_rate",
                    "query_value": 1
                },
                {
                    "query_field_key": "bytes",
                    "query_value": 1376
                },
                {
                    "query_field_key": "bit_rate",
                    "query_value": "1.83 K"
                }
            ],
            "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "1.1.1.1",
                "clients_end_ip": "1.1.1.1",
                "servers_start_ip": "2.1.1.1",
                "servers_end_ip": "2.1.1.2",
                "m": 1,
                "d": 5,
                "yaml_name": "test",
                "pcap_name": "http"
            },
            "token": ""
        }
        
        # 生成测试用例
        case_generator = CaseGenerator(test_data, parameter)
        result = case_generator.run()
        
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
        case_generator.delete_data()
        # 生成csv报告
        generate = GenerateCSV()
        generate.generate_csv(parameter, result, exception_result)
            
if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 5,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/api",
        "module_name": "dos_protection",
        "test_case_name": "dos_protect_srcip_http_rate_srcip_d3"
    }
    run(parameter)