import os
import time
import support.ui_utils.env
from datetime import datetime
from support.api_utils.log_in import *
from support.general_ui_utils.dashboard.create_dashboard import CreateDashboard
from support.general_ui_utils.dashboard.edit_dashboard import EditDashboard
from support.general_ui_utils.dashboard.delete_dashboard import DeleteDashboard
import random
from support.api_utils.delete_policy import *
from support.instance_utils.test_data_instance import TestDataInstance
from support.report import GenerateReport
from support.report_update import ReportUpdate


def run(parameter):
    global create_code, driver
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run test case: " + parameter["test_case_name"], flush=True)
        #参数初始化
        exception_result = ""
        result = {}

        #脚本启动时间
        start_time = time.time()

        #测试数据
        test_data ={
            "type":"dashboard",
            "visualization_type": "Pie",
            "data_source": "Application and Protocol Metrics",
            "select_metric_type": "single",
            "metric": {
                "single_type": [
                    {
                        "field":"Sessions",
                        "aggregate": "random",
                        "label": "verifyedit"
                    },
                    {
                        "field": "Incoming Bytes",
                        "aggregate": "BITRATE",
                        "label": "verifyedit2"
                    },
                    {
                        "field": "Outgoing Bytes",
                        "aggregate": "SUM",
                        "label": ""
                    },
                    {
                        "field": "Incoming Packets",
                        "aggregate": "SUM",
                        "label": ""
                    },
                    {
                        "field": "Outgoing Packets",
                        "aggregate": "SUM",
                        "label": ""
                    },
                    {
                        "field": "Packets Sent",
                        "aggregate": "SUM",
                        "label": ""
                    },
                    {
                        "field": "Packets Received",
                        "aggregate": "SUM",
                        "label": ""
                    },
                    {
                        "field": "Bytes Sent",
                        "aggregate": "BITRATE",
                        "label": ""
                    },
                    {
                        "field": "Bytes Received",
                        "aggregate": "SUM",
                        "label": ""
                    }

                ],
                "multiple_type": [
                    {
                        "field": ["Sessions"],
                        "aggregate": "random",
                        "label": "verifyedit2"
                    },
                    {
                        "field": ["Incoming Bytes","Outgoing Bytes"],
                        "aggregate": "random",
                        "label": ""
                    },
                    {
                        "field": ["Incoming Packets","Outgoing Packets"],
                        "aggregate": "random",
                        "label": ""
                    },
                    {
                        "field": ["Bytes Sent","Bytes Received"],
                        "aggregate": "random",
                        "label": ""
                    },
                    {
                        "field": ["Packets Sent","Packets Received"],
                        "aggregate": "random",
                        "label": ""
                    }
                ]
            },
            "multiple_dimension": "true",
            "dimensions": ["Time","App Name"],
            "sub_type": "",
            "order_by":"verifyedit2",
            "filter": [
                {
                    "field": "App Name",
                    "operator": "random",
                    "value": ["dns"]
                },
                {
                    "field": "Device Group",
                    "operator": "=",
                    "value": ["group-xxg-tsgx"]
                },
                {
                    "field": "Data Center",
                    "operator": "IN",
                    "value": ["center-xxg-tsgx","center-xxg-9140"]
                }
            ]
        }

        # 测试用例实例化
        test_data_instance = TestDataInstance(test_data, parameter)
        result = test_data_instance.create()

        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,flush=True)
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
        "username": "auto_ui_yzj",
        "password": "auto_ui_yzj",
        "test_pc_ip": "192.168.64.28",
        "test_subcriber_id": "",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 2,
        "is_log": 0,
        "root_path": "D:/PycharmProjects/tsg_test",
        "path": "D:/PycharmProjects/tsg_test/tests/ui",
        "module_name": "dashboard",
        "test_case_name": "create_table_traffic_spectrum"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """