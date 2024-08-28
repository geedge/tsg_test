import os
import time
import support.ui_utils.env
from datetime import datetime
from support.api_utils.log_in import *
from support.general_ui_utils.dashboard.create_dashboard import CreateDashboard

import random

from support.common.report import GenerateReport


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run test case: " + parameter["test_case_name"], flush=True)
        #参数初始化
        result,exception_result = "",""

        #脚本启动时间
        start_time = time.time()

        # 环境初始化
        support.ui_utils.env.initiate_selenium_request()
        driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()

        #测试数据
        test_data =  {
            "ids": "Dimensions多个添加错误校验",
            "visualization_type": ["Bar","Pie"],
            "data_source": "Service Chaining Rule Hits",
              "metric": {
                  "single_type": [
                      {
                          "field": "Bytes Sent",
                          "aggregate": "random",
                          "label": "verifyedit"
                      }
                  ]
              },
              "dimensions": ["Time", "Rule","Service Function Forwarder Profile ID","Service Function Profile ID","Device Group", "Data Center"],
              "order_by": "",
              "filter": "",
              "isallowdimensions": "0",
              "sub_type": "error_dimensions"

        }

        select_metric_type = ["single", "multiple"]
        multiple_dimension = ["true", "false"]
        # 随机metric与dimension格式
        metric_type = random.choice(select_metric_type)
        multiple_dimension = random.choice(multiple_dimension)
        visualization_type = random.choice(test_data["visualization_type"])

        #创建Dashboard-Chart
        create_dashboard = CreateDashboard(driver)
        create_code = create_dashboard.create(test_data, visualization_type, "single", "true")
        if create_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"More dimension error hint right", flush=True)
        else:
            result = "Fail to create chart"

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Duration of running the test case: ", "{:.3f}".format(duration), flush=True)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,flush=True)
        return "Error: " + str(e)
    finally:
        #清理环境
        support.ui_utils.env.teardown()
        file_path = parameter["root_path"] + "/report/{}_report.csv".format(parameter["script_type"])
        if os.path.exists(file_path) and os.path.isfile(file_path):
            if result is not None and result != "" and len(result) != 0:
                report_data = []
                report_data.append(parameter["test_case_name"])
                result_flag = "Fail"
                report_data.append(result_flag)
                report_data.append(result)
            elif exception_result is not None and exception_result != "" and len(exception_result) != 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Fail"
                report_data.append(result_flag)
                report_data.append(exception_result)
            elif result == "" and len(result) == 0 and exception_result == "" and len(exception_result) == 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Pass"
                report_data.append(result_flag)
                report_data.append("")
            new_report = GenerateReport()
            new_report.insert_data(parameter, report_data)

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
        "module_name": "",
        "test_case_name": "create_table_traffic_spectrum"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """