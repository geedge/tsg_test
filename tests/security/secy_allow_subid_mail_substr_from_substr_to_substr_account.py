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
                "attribute_name": "ATTR_MAIL_FROM",
                "object_type": "account",
                "object_sub_type": "account",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "hbn@163.com"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_MAIL_TO",
                "object_type": "account",
                "object_sub_type": "account",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "autotest@163.com"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_MAIL_ACCOUNT",
                "object_type": "account",
                "object_sub_type": "account",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "hbn@163.com"
                        ]
                        }
                    ]
                    }
                ]
                }
            ],
            "application_1": ["mail"],
            "expected_return": "Email sent successfully",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key":"mail_account","query_value":"hbn@163.com"}],
            "traffic": {
                "protocol": "mail",
                "type": "client", # client/curl
                "mail_type": "smtp", # gmail or smtp or smtp_ssl
                "mail_server": "192.168.40.206", # gmail: smtp.gmail.com
                "mail_port": 25, # gmail：465（用于SSL）、587（用于启动TLS）。smtp默认：25
                "mail_timeout": 20,
                "sender": "hbn@163.com",
                "password": "111111",
                "receiver": "autotest@163.com",
                "subject": "Bestman",
                "body": "123",
                "attach": "/app/support/packet_generator/mail_file/subjectEnglish.txt"
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