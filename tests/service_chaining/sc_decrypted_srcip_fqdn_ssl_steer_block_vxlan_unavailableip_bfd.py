# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
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
            "rule_name": "sc_decrypted_srcip_fqdn_ssl_steer_block_vxlan_unavailableip_bfd",
            "rule_action": "service_chaining",
            "targeted_traffic": "decrypted",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "service_chaining_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter["test_pc_ip"]
                            }
                        ]
                    }
                ],
                "source_port": [],
                "destination_port": [],
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
                "application": [
                    {
                        "name": "ssl",  
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
                                "item_value": "$www.facebook.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [],
                "sub_action_override": False,
                "sub_action": [],
                "packet_capture": [],
            },
            "multiProfile": True,
            "profile": [
                {
                    "name": "steer_block_vxlan_unavailableip_bfd",
                    "profile_type": "create",
                    "type": "steering",
                    "load_balance_method": "hash_int-ip",
                    "load_balance_localization": "nearby",
                    "failure_action": "Block",
                    "service_functions": [
                        {
                            "name": "vxlan_unavailableip_bfd",
                            "profile_type": "create",
                            "device_group": "Device_Group:group-xxg-tsgx",
                            "connectivity": "VXLAN-G:3.3.3.52",
                            "health_check": "BFD:10:255",
                            "enable": "on"
                        }
                    ]
                }
            ],
            "log_query_param": [{"query_field_key": "sc_rsp_decrypted", "query_value": ""}],
            "traffic":{
                "protocol": "ssl",
                "type": "curl",
                "command": "curl --connect-timeout 10 --max-time 30 -kv https://www.facebook.com"
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
        "test_pc_ip": "192.168.64.91",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 11,
        "is_log": 1,
        "root_path": "C:/automation_project/tsg_test",
        "path": "C:/automation_project/tsg_test/tests/ui",
        "module_name": "service_chaining",
        "test_case_name": "sc_decrypted_srcip_fqdn_ssl_steer_block_vxlan_unavailableip_bfd"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """