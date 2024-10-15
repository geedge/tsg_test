# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import traceback
from datetime import datetime
from support.instance_utils.case_instance_generator import CaseInstanceGenerator
from support.report_update import ReportUpdate
from support.ui_utils.object.generate_random_ip import *

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
            "policy_type": "service_chaining",
            "rule_name": "sc_raw_dstip_dstport_range_steer_bypass_vxlan_activeip_bfd",
            "rule_action": "service_chaining",
            "targeted_traffic": "raw",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
                "source_port": [],
                "destination_ip": [
                    {
                        "name": "service_chaining_destination_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "10.64.225.22"
                            }
                        ]
                    }
               ],
                "destination_port": [{
                        "name": "sc_ui_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "port",
                                "item_value": "443-443",
                            },
                        ]
                    }
                ],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [],
                "external_port": [],
                "geography": [],
                "sub_id": [],
                "device": [],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [],
                "server_fqdn": [],
                "protocol_filed": [],
                "sub_action_override": False,
                "sub_action": [],
                "packet_capture": [],
            },
            "multiProfile": True,
            "profile": [
                {
                    "name": "steer_bypass_vxlan_activeip_bfd",
                    "profile_type": "create",
                    "type": "steering",
                    "load_balance_method": "hash_int-ip",
                    "load_balance_localization": "nearby",
                    "failure_action": "Bypass",
                    "service_functions": [
                        {
                            "name": "vxlan_activeip_bfd",
                            "profile_type": "create",
                            "device_group": "Device_Group:group-xxg-tsgx",
                            "connectivity": "VXLAN-G:2.2.2.53",
                            "health_check": "BFD:200:5",
                            "enable": "on"
                        }
                    ]
                }
            ],
            "log_query_param": [{"query_field_key": "sc_rsp_raw", "query_value": ""},
                                {"query_field_key": "sent_pkts", "query_value": ""},
                                {"query_field_key": "received_pkts", "query_value": ""},
                                {"query_field_key": "sent_bytes", "query_value": ""},
                                {"query_field_key": "received_bytes", "query_value": ""},
                                {"query_field_key": "server_port", "query_value": "443"}],
            "traffic":{
                    "protocol": "",
                    "type": "trex",
                    "clients_start_ip": "10.64.225.22",
                    "clients_end_ip": "10.64.225.22",
                    "servers_start_ip": "10.64.226.22",
                    "servers_end_ip": "10.64.226.22",
                    "m": 1,
                    "d": 1,
                    "yaml_name": "test",
                    "pcap_name": "test_https"
                },
            "expected_return":"",
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
            case_instance_generator.delete_data()
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)

    
if __name__ == '__main__':
    parameter = {
        "username": "lytest",
        "password": "123456ly",
        "test_pc_ip": "192.168.50.88",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "root_path": "C:/automation_project/tsg_test",
        "path": "C:/automation_project/tsg_test/tests/ui",
        "module_name": "service_chaining",
        "test_case_name": "sc_raw_dstip_dstport_range_steer_bypass_vxlan_activeip_bfd"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """