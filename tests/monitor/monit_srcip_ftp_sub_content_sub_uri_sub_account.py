import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.instance_utils.instance_test_data import InstanceTestData
from support.report_update import ReportUpdate
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime


def run(parameter):
    try:
        case_instance_generator = None
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        exception_result = ""
        result = {}

        # 脚本启动时间
        start_time = time.time()

        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "monitor",
            "rule_name": "monitor_rule_ftp_uri_content_account",
            "rule_action": "monitor",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "monitor_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": parameter['test_pc_ip'],
                            },
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
                        "name": "ftp",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [
                    {
                        "name": "monitor_ftp_uri",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                #"item_value": "english->"
                                "item_value":"$ftp://192.168.40.206/autoFtp/english_big.txt"
                            }
                        ],
                    },
                    {
                        "name": "monitor_keywords_ftp_content",
                        "object_type": "keywords",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ftp_content",
                                "item_value": "TEXT",
                                "value": [
                                    "autotest*"
                                ]
                            }
                        ],
                    },
                    {
                        "name": "monitor_ftp_account",
                        "object_type": "account",
                        "select_type": False,
                        "item_operation": "add",
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "ftp_account",
                                "item_value": "ftpuser"
                            }
                        ],
                    }
                ],
                #"sub_action_override": True,
                "sub_action": [],
                "packet_capture": []
            },
            "is_mirror": "off",
            "expected_return": "auto",
            "counters": {"hits":  1},
            "log_query_param": [{"query_field_key": "ftp_account", "query_value": "ftpuser"},
                                {"query_field_key": "ftp_url","query_value": "ftp://192.168.40.206/autoFtp/english_big.txt"}
                                ],
            "traffic": {
                "protocol": "ftp",
                "type": "curl",
                "command": "curl -m 20 ftp://192.168.40.206/autoFtp/english_big.txt -u ftpuser:111111"
            },
            "token": ""
        }

        # 测试用例实例化
        instantiation = InstanceTestData(test_data, parameter)
        result = instantiation.create()

        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,
              flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        if isinstance(instantiation, InstanceTestData):
            instantiation.clean_up()
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)


if __name__ == '__main__':
    parameter = {
        "username": "guoqiuya",
        "password": "Guoqiuya123@@",
        "test_pc_ip": "192.168.64.96",
        "test_subcriber_id": "test490",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "is_log": 1,
        "env": "tsgx",
        "script_type": "api",
        "vsys_id": 1,
        "root_path": "C:/Users/guoqiuya/Desktop/code/test_924/tsg_test",
        "path": "C:/Users/guoqiuya/Desktop/code/test_924/tsg_test/tests/ui",
        "module_name": "monitor",
        "test_case_name": "monitor_rule_mail_mirror_on"
    }
    parameter = replace_paras(parameter)
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """