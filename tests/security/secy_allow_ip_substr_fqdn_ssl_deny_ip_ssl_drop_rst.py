# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
            "is_multi_priority": True,
            "rule_num": 2,
            "policy_type": "security",
            "rule_action_1": "allow",
            "rule_action_2": "deny",
            "method_2": "drop",
            "do_log_1": 2,
            "do_log_2": 2,
            "obj_condition_1": [
            {
                "attribute_name": "ATTR_SOURCE_IP",
                "object_type": "ip",
                "object_sub_type": "ip",
                "object_list": [
                {
                    "add_item_list": [
                    {
                        "ip_address": "default",
                        "port_range": "0-65535"
                    }
                    ]
                }
                ]
            },
            {
                "attribute_name": "ATTR_SERVER_FQDN",
                "object_type": "fqdn",
                "object_sub_type": "fqdn",
                "object_list": [
                {
                    "add_item_list": [
                    {
                        "keyword_array": [
                        "www.baidu.com"
                        ]
                    }
                    ]
                }
                ]
            }
            ],
            "obj_condition_2": [
            {
                "attribute_name": "ATTR_SOURCE_IP",
                "object_type": "ip",
                "object_sub_type": "ip",
                "object_list": [
                {
                    "add_item_list": [
                    {
                        "ip_address": "default",
                        "port_range": "0-65535"
                    }
                    ]
                }
                ]
            }
            ],
            "application_1": ["ssl"],
            "application_2": ["ssl"],
            "expected_return": "百度一下",
            "counters_1": {"hits": 1},
            "counters_2": {"hits": 0},
            "log_query_param_1": [{"query_field_key":"ssl_sni","query_value":"www.baidu.com"}],
            "log_query_param_2": [],
            "traffic": {
                    "protocol": "ssl",
                    "type": "curl",
                    "command": "curl -kv --connect-timeout 10 -m 10 https://www.baidu.com"
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
            case_instance_generator.clean_up()
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