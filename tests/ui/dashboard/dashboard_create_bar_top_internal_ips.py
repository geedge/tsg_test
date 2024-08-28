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
from support.report import GenerateReport


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
            "visualization_type": ["Table","Bar"],
            "data_source": "Top Internal IPs",
            "select_metric_type": "single",
            "metric": {
                "single_type": [
                    {
                        "field": "Sessions",
                        "aggregate": "random",
                        "label": "verifyedit"
                    },
                    {
                        "field": "Bytes",
                        "aggregate": "RATE",
                        "label": "verifyedit2"
                    },
                    {
                        "field": "Incoming Bytes",
                        "aggregate": "BITRATE",
                        "label": ""
                    },
                    {
                        "field": "Outgoing Bytes",
                        "aggregate": "SUM",
                        "label": ""
                    },
                    {
                        "field": "Packets",
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
                    }
                ],
                "multiple_type": [
                    {
                        "field": ["Incoming Bytes","Outgoing Bytes"],
                        "aggregate": "random",
                        "label": "verifyedit2"
                    },
                    {
                        "field": ["Incoming Packets","Outgoing Packets"],
                        "aggregate": "RATE",
                        "label": ""
                    }
                ]
            },
            "multiple_dimension": "true",
            "dimensions": ["Time", "Internal IP"],
            "isallowdimensions": "0",
            "sub_type": "",
            "order_by":"verifyedit2",
            "filter": [
                {
                    "field": "Rank",
                    "operator": "=",
                    "value": ["Sessions"]
                },
                {
                    "field": "Device Group",
                    "operator": "=",
                    "value": ["group-xxg-tsgx"]
                },
                {
                    "field": "Data Center",
                    "operator": "=",
                    "value": ["center-xxg-tsgx"]
                }
            ]
        }
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        name_list = [
            {
                "name": "New Dashboard",
                "type": "dashboard",
            }
        ]

        select_metric_type = ["single", "multiple"]
        multiple_dimension = ["true", "false"]
        #随机metric与dimension格式
        metric_type = random.choice(select_metric_type)
        multiple_dimension = "false"

        #创建Dashboard-Chart
        create_dashboard = CreateDashboard(driver)
        create_code = create_dashboard.create(test_data,"Bar",metric_type,multiple_dimension)
        if create_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create chart successfully.", flush=True)
        else:
            result = "Fail to create chart"
        #新建chart输入数据校验
        create_verify_code = create_dashboard.create_chart_data_verify(test_data,"Bar",metric_type,multiple_dimension)
        if create_verify_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create chart data verify successfully.", flush=True)
        else:
            result = "Fail to chart data verify"

        #修改metric与dimension格式
        if metric_type == "single":
            metric_type = "multiple"
        else: metric_type = "single"

        #编辑操作
        edit_dashboard = EditDashboard(driver)
        edit_dashboard_code = edit_dashboard.edit(test_data,"Bar",metric_type,multiple_dimension)
        if edit_dashboard_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit chart successfully.", flush=True)
        else:
            result = "Fail to Edit chart"
        #修改内容数据校验
        edit_verify_code = edit_dashboard.modify_data_verify(test_data,"Bar")
        if edit_verify_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit chart verify successfully.", flush=True)
        else:
            result = "Fail to Edit chart verify"

        #删除dashboard
        delete_dashboard = DeleteDashboard(driver)
        delete_dashboard_code = delete_dashboard.delete()
        if delete_dashboard_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Delete chart successfully.", flush=True)
        else:
            result = "Fail to Delete chart"
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
        delete = DeletePolicy()
        delete.delete_policy_by_name(token, parameter, name_list)
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