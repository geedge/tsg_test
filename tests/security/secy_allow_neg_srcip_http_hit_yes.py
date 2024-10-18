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
        start_time = time.time()
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_name": os.path.splitext(os.path.basename(__file__))[0],
            "rule_action": "allow",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "secy_srcip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": True,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "1.1.1.1",
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
                "sub_action": [],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "POST",
            "counters": {"hits": "many"},
            "log_query_param": [
                {"query_field_key": "decoded_as", "query_value": "HTTP"}
            ],
            "traffic": {
                "protocol": "http",
                "type": "curl",
                "command": "curl -kv http://open.node.com:180"
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
        end_time = time.time()
        duration = end_time - start_time
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