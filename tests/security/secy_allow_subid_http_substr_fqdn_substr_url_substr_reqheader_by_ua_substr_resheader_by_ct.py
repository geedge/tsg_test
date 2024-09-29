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
        result, exception_result = "", ""
        
        # 脚本启动时间
        start_time = time.time()
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_action_1": "allow",
            "do_log_1": 2,
            "obj_condition_1": [
                {
                "attribute_name": "ATTR_SUBSCRIBER_ID",
                "object_type": "subscriberid",
                "object_sub_type": "subscriberid",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "default"
                        ]
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
                            "open.node.com"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_HTTP_URL",
                "object_type": "url",
                "object_sub_type": "url",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "open.node.com"
                        ]
                        }
                    ]
                    }
                ]
                },
                    {
                "attribute_name": "ATTR_HTTP_REQ_HDR",
                "object_type": "http_signature",
                "object_sub_type": "http_signature",
                "object_list": [
                    {
                    "context_name" : "User-Agent",
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "Wget"
                        ]
                        }
                    ]
                    }
                ]
                },
                    {
                "attribute_name": "ATTR_HTTP_RES_HDR",
                "object_type": "http_signature",
                "object_sub_type": "http_signature",
                "object_list": [
                    {
                    "context_name" : "Content-Type",
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "text/html"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_HTTP_REQ_BODY",
                "object_type": "keywords",
                "object_sub_type": "keywords",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "requestbodysubstring"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_HTTP_RES_BODY",
                "object_type": "keywords",
                "object_sub_type": "keywords",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "responsebodysubstring"
                        ]
                        }
                    ]
                    }
                ]
                }
            ],
            "application_1": ["http"],
            "expected_return": "open.node.com",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key":"http_host","query_value":"open.node.com"}],
            "traffic": {
                "protocol": "http",
                "type": "curl",
                "command": "curl --connect-timeout 5 -m 10 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"requestbodysubstring\\\",\\\"setcook\\\":\\\"asdf\\\",\\\"contenttype\\\": \\\"charset\\\",\\\"responsebody\\\": \\\"responsebodysubstring\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" http://open.node.com:180/go"
            },
            "token": ""
        }
        
        # 测试用例实例化
        case_instance_generator = CaseInstanceGenerator(test_data, parameter)
        result = case_instance_generator.run()
        
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        case_instance_generator.delete_data()
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
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.86",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 6,
        "is_log": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/api",
        "module_name": "security",
        "test_case_name": "allow_http_fqdn"
    }
    run(parameter)