import os
import sys
from support.instance_utils.case_instance_generator import CaseInstanceGenerator
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
                        "name": "monit_mail_account_by_account",
                        "object_type": "account",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "mail_account",
                                "item_value": "hbn*->"
                            }
                        ],
                    }
                ],
            },
            "expected_return": "Ok",
            "counters": {"hits": 1},
            "log_query_param": [
                {"query_field_key": "decoded_as", "query_value": "MAIL"},
                {"query_field_key": "mail_account", "query_value": "hbn@163.com"}
            ],
            "traffic": {
                "protocol": "mail",
                "type": "curl",
                "command": "curl -kv --connect-timeout 25 -m 25 --url 'smtp://192.168.40.206' --mail-from 'hbn@163.com'  --mail-rcpt 'autotest@163.com'  --upload-file '/app/support/packet_generator/mail_file/subjectEnglish.txt' --user 'hbn@163.com:111111'"
            },
            "token": ""
        }

        # 测试用例实例化
        case_instance_generator = CaseInstanceGenerator(test_data, parameter)
        result = case_instance_generator.run()

        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,
              flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        case_instance_generator.delete_data()
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
        "script_type": "api",
        "vsys_id": 1,
        "root_path": "C:/Users/guoqiuya/Desktop/code/test_924/tsg_test",
        "path": "C:/Users/guoqiuya/Desktop/code/test_924/tsg_test/tests/ui",
        "module_name": "manipulation",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """