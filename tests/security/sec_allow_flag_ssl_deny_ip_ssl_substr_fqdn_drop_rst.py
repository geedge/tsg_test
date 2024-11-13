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
                "attribute_name": "ATTR_FLAG",
                "object_type": "flag",
                "object_sub_type": "flag",
                "object_list": [
                {
                    "add_item_list": [
                    {
                        "flag": 8,
                        "mask": 8
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
                        "ip_address": parameter["test_pc_ip"],
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
      
if __name__ == "__main__":
    parameter = {
      "script_type": "api",
      "username": "hebingning",
      "password": "hbn66AAA",
      "test_pc_ip": "192.168.64.88",
      "test_subcriber_id": "test6488",
      "api_server": "http://192.168.44.72",
      "is_log": 0,
      "env": "tsgx",
      "vsys_id": 6,
      "root_path": "D:/python_script/tsg_test",
      "path": "D:/python_script/tsg_test/tests/api",
      "module_name": "security",
      "test_case_name": "allow_negate_fqdn"
    }
    run(parameter)