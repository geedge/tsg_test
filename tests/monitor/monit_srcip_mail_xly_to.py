import os
import sys
from support.instance_utils.test_data_instance import TestDataInstance
from support.report_update import ReportUpdate

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime


def run(parameter):
    try:
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
            "rule_name": os.path.splitext(os.path.basename(__file__))[0],
            "rule_action": "monitor",
            "rule_type": "create",
            "is_mirror": "off",
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
                                "item_value": parameter["test_pc_ip"],
                            },
                        ]
                    }
                ],
                "application": [
                    {
                        "name": "mail",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "monitor_mail_to",
                        "object_type": "account",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "to",
                                "item_value": "$autotest@163.com"
                            }
                        ],
                    }
                ],
            },
            "expected_return": "Email sent successfully",
            "counters": {"hits": 1},
            "log_query_param": [
                {"query_field_key": "decoded_as", "query_value": "MAIL"},
                {"query_field_key": "mail_to", "query_value": "autotest@163.com"}
            ],
            # "traffic": {
            #     "protocol": "mail",
            #     "type": "curl",
            #     "command": "curl -kv --connect-timeout 25 -m 25 --url 'smtp://192.168.40.206' --mail-from 'hbn@163.com'  --mail-rcpt 'autotest@163.com'  --upload-file '/app/support/packet_generator/mail_file/subjectEnglish.txt' --user 'hbn@163.com:111111'"
            # },
            "traffic": {
                "protocol": "mail",
                "type": "curl",  # client/curl
                "mail_type": "smtp",  # gmail or smtp or smtp_ssl
                "mail_server": "192.168.40.206",  # gmail: smtp.gmail.com
                "mail_port": 25,  # gmail：465（用于SSL）、587（用于启动TLS）。smtp默认：25
                "mail_timeout": 20,
                "sender": "hbn@163.com",
                "password": "111111",
                "receiver": "autotest@163.com",
                "subject": "Bestman",
                "body": "123",
                # "attach": "/app/support/packet_generator/mail_file/subjectEnglish.txt"
                "attach": "/opt/traffic_replay/mail_file/subjectEnglish.txt"
            },
            "token": ""
        }

        # 测试用例实例化
        test_data_instance = TestDataInstance(test_data, parameter)
        result = test_data_instance.create()

        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,
              flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        if isinstance(test_data_instance, TestDataInstance):
            test_data_instance.clean_up()
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
        "test_pc_ip": "192.168.64.105",
        "test_subcriber_id": "test490",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "is_log": 1,
        "env": "tsgx",
        "script_type": "ui",
        "vsys_id": 1,
        "root_path": "C:/Users/guoqiuya/Desktop/code/test_924/tsg_test",
        "path": "C:/Users/guoqiuya/Desktop/code/test_924/tsg_test/tests/ui",
        "module_name": "monitor",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """