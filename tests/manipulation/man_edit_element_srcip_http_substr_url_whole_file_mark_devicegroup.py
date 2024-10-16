# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import traceback
from datetime import datetime
from support.instance_utils.test_data_instance import TestDataInstance
from support.report_update import ReportUpdate


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
            "policy_type": "pxy_manipulation",
            "rule_name": parameter["test_case_name"],
            "rule_action": "edit_element",
            "effective_devices": ["group-xxg-tsgx"],
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "manipulation_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter["test_pc_ip"],
                            },
                        ]
                    }
                ],
                "internal_ip": [
                    {
                        "name": "manipulation_internal_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter["test_pc_ip"],
                            }
                        ]
                    }
                ],
                "application": [
                    {
                        "name": "http",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "manipulation_url",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                "item_value": "192.168"
                            }
                        ],
                    },
                ],
            },
            "action_parameter": {
                "edit_element_parameter": [
                    {
                        "profile_type": "edit_element",
                        "search_scope": "whole_file",
                        "start_indicator": "test_keywork",
                        "contained_keyword": "test_request_body",
                        "distance_from_anchor": "1",
                        "treatment": "mark"
                    }
                ]
            },
            "expected_return": "need_filter",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key": "http_host", "query_value": "192.168.40.206"}, {"query_field_key": "decoded_as", "query_value": "HTTP"}],
            "traffic": {
                "protocol": "ssl",
                "type": "curl",
                "command": "curl --connect-timeout 30 -m 60 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"test_request_body\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" https://192.168.40.206:1443/go"
            },
            "token": ""
        }

        # 测试用例实例化
        test_data_instance = TestDataInstance(test_data, parameter)
        result = test_data_instance.create()

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        traceback.print_exc()
        return "Error: " + str(e)
    finally:
        # 清理环境
        if isinstance(test_data_instance, TestDataInstance):
            test_data_instance.clean_up()
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)


if __name__ == '__main__':
    from support.ui_utils.element_position.map_element_position_library import replace_paras
    from support.ui_utils.workpath import workdir

    parameter = {
        "username": "zcw3",
        "password": "qa111111",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "api",  # api  ui  空字符串
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/testcase/ui",
        "module_name": "manipulation",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    run(parameter)
    