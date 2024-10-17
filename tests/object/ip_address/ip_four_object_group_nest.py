# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from datetime import datetime
from support.report_update import ReportUpdate
from support.instance_utils.instance_test_data import InstanceTestData


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run test case: " + parameter["test_case_name"], flush=True)
        #参数初始化
        result,exception_result = "",""

        #脚本启动时间
        start_time = time.time()

        #测试数据
        test_data =  {
            "type": "objects",
            "case_type": "group",
            "name": "create_ip_four_group_nest",
            "object_type": "ip",
            "sub_object": 4,
            "object_operation":{
                "create": [
                    {
                        "item_operation": "quote",
                        "item_type": "",
                        "item_value": "create_ip_four_group_nest"
                    },
                    {
                        "item_operation": "quote",
                        "item_type": "",
                        "item_value": "create_ip_four_group_nest"
                    },
                    {
                        "item_operation": "quote",
                        "item_type": "",
                        "item_value": "create_ip_four_group_nest"
                    },
                    {
                        "item_operation": "quote",
                        "item_type": "",
                        "item_value": "create_ip_four_group_nest"
                    }
                ]
            },
            "search": {
                "is_fuzzy": False,
                "type": "name"
            },
            "statistics": "",  # random
            "audit_log": False  # system
        }

        # 测试用例实例化
        instantiation = InstanceTestData(test_data, parameter)
        result = instantiation.create()

    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        if isinstance(instantiation, InstanceTestData):
            instantiation.clean_up()
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Finish test case: " + parameter["test_case_name"], flush=True)
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
        "module_name": "",
        "test_case_name": "create_ip_four_group_nest"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """