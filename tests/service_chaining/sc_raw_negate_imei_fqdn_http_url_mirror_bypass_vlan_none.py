# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import traceback
from datetime import datetime
from support.common_utils.create_policy import CreatePolicy
from support.report_update import ReportUpdate

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
            "policy_type": "service_chaining",
            "rule_name": "sc_raw_negate_imei_fqdn_http_url_mirror_bypass_vlan_none",
            "rule_action": "service_chaining",
            "targeted_traffic": "raw",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [],
                "external_port": [],
                "geography": [],
                "sub_id": [],
                "device": [
                    {
                        "name": "service_chaining_imei",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": True,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "imei",
                                "item_value": "$1234567802",
                            }
                        ]
                    }
                ],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "http",  
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                    {
                        "name": "service_chaining_fqdn",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_value": "ct.cn",
                            }
                        ]
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "service_chaining_url",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                "item_value": "ct.cn/"
                            }
                        ],
                    },
                ],
                "sub_action_override": False,
                "sub_action": [],
                "packet_capture": [],
            },
            "multiProfile": True,
            "profile": [
                {
                    "name": "mirror_bypass_vlan_none",
                    "profile_type": "create",
                    "type": "mirroring",
                    "load_balance_method": "hash_int-ip",
                    "load_balance_localization": "nearby",
                    "failure_action": "Bypass",
                    "service_functions": [
                        {
                            "name": "vlan_none",
                            "profile_type": "create",
                            "device_group": "Device_Group:group-xxg-tsgx",
                            "connectivity": "Layer_2_Switch:random:random",
                            "health_check": "none",
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
                                {"query_field_key": "subscriber_id", "query_value": "test2425"},
                                {"query_field_key": "imei", "query_value": "1234567802"},
                                {"query_field_key": "imsi", "query_value": "43458960458"},
                                {"query_field_key": "apn", "query_value": "www.lyrawautotest.com"},
                                {"query_field_key": "phone_number", "query_value": "12345678902"}],
            "traffic":{
                    "protocol": "",
                    "type": "trex",
                    "clients_start_ip": "10.64.224.25",
                    "clients_end_ip": "10.64.224.25",
                    "servers_start_ip": "10.64.224.29",
                    "servers_end_ip": "10.64.224.29",
                    "m": 1,
                    "d": 1,
                    "yaml_name": "test",
                    "pcap_name": "http_get_347pkts"
                },
            "expected_return":"",
            "token": ""
        }

        # 测试用例实例化
        create = CreatePolicy(test_data, parameter)
        result = create.create_policy()
        
        # 脚本结束时间和耗时
        script_end_time = time.time()
        duration = script_end_time - script_start_time
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
        if isinstance(create, CreatePolicy):
            create.clean_up()
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
    
if __name__ == '__main__':
    parameter = {
        "username": "lytest",
        "password": "123456ly",
        "test_pc_ip": "192.168.50.88",
        "test_subcriber_id": "test2425",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "root_path": "C:/automation_project/tsg_test",
        "path": "C:/automation_project/tsg_test/tests/ui",
        "module_name": "service_chaining",
        "test_case_name": "sc_raw_negate_imei_fqdn_http_url_mirror_bypass_vlan_none"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """