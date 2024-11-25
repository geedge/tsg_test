import time
from support.api_utils.log_in import *
from support.report_update import ReportUpdate
from support.ui_utils.ui_client import UIClient


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run test case: " + parameter["test_case_name"], flush=True)

        # 参数初始化
        result, exception_result = "", ""
        test_summary = {}

        # 脚本启动时间
        start_time = time.time()

        #测试数据
        object_configuration =  {
            "or_conditions": [
                {
                    "name": "test",
                    "type": "apn",
                    "member_type": "item",
                    "statistics_option": "",  # random
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "acdcd$"
                        }
                    ]
                }
            ],
            "search": {
                "is_fuzzy": False,
                "type": "uuid"
            },

            "audit_log": False  # system
        }

        # 创建
        ui_client = UIClient()
        objects_tuple, ui_error = ui_client.create_objects(object_configuration)
        if len(ui_error) > 0:
            return ui_error
        objects_list = list(objects_tuple)
        if len(objects_list) > 0 and len(objects_list[0]["uuid"]) > 0:
            return ""

    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"When running test case, the exception error: ", str(e), flush=True)
        return "When running test case, the exception error: " + str(e)

    finally:
        # 删除
        if parameter["initiation_method"] == "ui":
            if objects_tuple is not None:
                ui_client.delete_objects(parameter, objects_tuple, object_configuration["search"])
        # elif parameter["initiation_method"] == "api":
        #     if not objects_tuple:
        #         api_client.delete_rules(rules_tuple)
        #     if not objects_tuple:
        #         api_client.delete_objects(objects_tuple)

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
        "initiation_method": "ui",
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