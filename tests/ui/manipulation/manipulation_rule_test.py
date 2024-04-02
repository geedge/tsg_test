# -*- coding: UTF-8 -*-
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
print(__file__)
print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.policy.manipulation_pub import ManipulationPub
from support.traffic_replay.traffic_verification import *
from support.api_utils.analysis_result import *
import support.ui_utils.env_initialization
import traceback


def run(parameter):
    try:
        print("Begin to run test case: " + parameter["test_case_name"])
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "manipulation",
            "rule_name": "security_rule_with_deny_ip_quic",
            "rule_action": "allow",
            "rule_type": "create",
            "condition": {
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                # "internal_ip": [
                #     {
                #         "name": "security_internal_ip",
                #         "object_type": "ip",
                #         "select_type": False,
                #         "negate": False,
                #         "item": [
                #             "1.1.1.1",
                #             "1.1.1.1-1.1.1.2"
                #         ]
                #     }
                # ],
                "internal_ip_group": [
                    {
                        "name": "security_src_ip_group",
                        "object_type": "ip_group",
                        "select_type": True,
                        "negate": False,
                        "group_subordinate": [
                            {
                                "name": "security_include_1_src_ip",
                                "object_type": "ip",
                                "negate": False,
                                "item": [
                                    "1.1.1.1",
                                    "1.1.1.1-1.1.1.2"
                                ]
                            },
                            {
                                "name": "security_include_2_src_ip",
                                "object_type": "ip",
                                "negate": False,
                                "item": [
                                    "2.1.1.1",
                                    "2.1.1.1-2.1.1.2"
                                ]
                            }
                        ],
                        "group_exclude": [
                            {
                                "name": "security_exclude_src_ip",
                                "object_type": "ip",
                                "negate": False,
                                "item": [
                                    "3.1.1.1",
                                    "3.1.1.1-3.1.1.2"
                                ]
                            }
                        ]
                    }
                ],
                "internal_port": [
                    {
                        "name": "security_internal_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            "1000-1110",
                            "2222"
                        ]
                    }
                ],
                "external_ip": [
                    {
                        "name": "security_external_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            "11.1.1.1",
                            "11.1.1.1-11.1.1.2"
                        ]
                    }
                ],
                "external_port": [],
                "source_geography": [],
                "destination_geography": [],
                "sub_id": [],
                "device": [
                    # {
                    #     "name": "security_mobile_phone_number",
                    #     "object_type": "phone_number",
                    #     "select_type": False,
                    #     "negate": False,
                    #     "plus": True,
                    #     "item": [
                    #         "test",
                    #         "test11"
                    #     ]
                    # }
                ],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [
                    # {
                    #     "name": "security_flag",
                    #     "object_type": "flag",
                    #     "select_type": False,
                    #     "negate": False,
                    #     "item": [
                    #         {
                    #             "flag_type": "asymmetric",
                    #             "flag_num": 1,
                    #             "flag_status": "True"
                    #         },
                    #         {
                    #             "flag_type": "Bidirectional",
                    #             "flag_num": 16,
                    #             "flag_status": "True"
                    #         },
                    #     ]
                    # }
                ],
                "application": [
                    {
                        "name": "http",
                        "object_type": "application",
                        "negate": False
                    }
                    # {
                    #     "name": "http_group",
                    #     "object_type": "application_group",
                    #     "negate": False
                    # }
                ],
                "server_fqdn": [
                    # {
                    #     "name": "www.baidu.com",  # 需要新建，不能使用已存在的object，保证自动化的统一性，这里只是示例
                    #     "object_type": "fqdn",
                    #     "select_type": False,
                    #     "negate": False,
                    #     "plus": False,
                    #     "item": [
                    #         "*google.com"
                    #     ]
                    # }
                ],
                "protocol_field": [
                    # {
                    #     "name": "security_url", # 需要新建，不能使用已存在的object，保证自动化的统一性，这里只是示例
                    #     "field_type": "url", # Protocol Field独有字段
                    #     "object_type": "url",
                    #     "select_type": False,
                    #     "negate": False,
                    #     "plus": False,
                    #     "item": [
                    #         "youtube.com",
                    #         "google.com"
                    #     ]
                    # },
                    {
                        "name": "security_request_header",
                        "field_type": "request_header",
                        "object_type": "http_signature",
                        "select_type": False,
                        "negate": False,
                        "plus": True,
                        "item": [
                            {
                                "item_key": "Set-Cookie",
                                "item_value": "TEXT",
                                "value": ["test", "test11"]
                            },
                            {
                                "item_key": "Content-Type",
                                "item_value": "HEX",
                                "value": ["123"]
                            }
                        ]
                    },
                    # {
                    #     "name": "security_keyword",
                    #     "field_type": "keyword",
                    #     "object_type": "keyword",
                    #     "select_type": False,
                    #     "negate": False,
                    #     "plus": True,
                    #     "item": [
                    #         {
                    #             "item_value": "TEXT",
                    #             "value": ["test", "test11"]
                    #         },
                    #         {
                    #             "item_value": "HEX",
                    #             "value": ["123"]
                    #         }
                    #     ]
                    # }
                ],
            },
            "action_parameter":{
                "profile":{}
            },
            "expected_return": "POST",
            "counters_1": {"hits": 0},
            "log_query_param_1": [],
            "command": "curl -kv https://www.google.com"
        }
        # 脚本启动时间
        start_time = time.time()
        # 实例ManipulationPub类(包含了rule创建-流量验证-销毁的全部方法)
        mp = ManipulationPub(test_data)
        # 环境初始化
        driver = mp.initiate_selenium_setup()
        # 创建object
        condition_code = mp.create_condition()
        # 创建rule
        create_rule_code = mp.create_rule()
        # 触发流量和验证
        mp.verification_and_analysis(parameter)
        # 删除rule
        mp.delete_rule()
        # 删除condition
        mp.delete_condition()
    except Exception as e:
        # 当捕获到异常时，执行相应的中断处理
        print("Exception type:", type(e).__name__)
        traceback.print_exc()  # 打印异常的完整堆栈跟踪
    finally:
        # 清理环境
        mp.selenium_teardown()
        print(2233)
        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        duration = round(duration, 2)
        print("duration: {}秒".format(duration))
        print("Finish test case: " + parameter["test_case_name"])
        return 200


if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.73",
        "api_server": "http://192.168.44.72",
        "is_log": 0,
        "env": "tsgx",
        "vsys_id": 6,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "security",
        "test_case_name": "security_rule_with_deny_ip_quic"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """