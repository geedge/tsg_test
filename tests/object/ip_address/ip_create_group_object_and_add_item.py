import time
import pytest
import os
from datetime import datetime
import support.ui_utils.env
from datetime import datetime

from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.log_in import *
from support.general_ui_utils.object.create_objects import CreateObjects
from support.general_ui_utils.object.edit_objects import EditObjects
from support.general_ui_utils.object.search_objects import SearchObjects
from support.general_ui_utils.object.delete_objects import DeleteObjects
from support.general_ui_utils.element_position.object_element_position import *
from support.common_utils.create_policy import CreatePolicy
from support.report_update import ReportUpdate


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
            "name": "create_ip_group_and_add_item",
            "object_type": "ip",
            "sub_object": 2,
            "object_operation":{
                "create": [
                    {
                        "item_operation": "add",
                        "item_type": "",
                        "item_value": ["1.1.1.1"]
                    }
                ],
                "edit":[
                    {
                        "item_operation": "add",
                        "item_type": "",
                        "item_value": ["1.1.1.1-1.1.1.1"]
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
        create = CreatePolicy(test_data, parameter)
        result = create.create_policy()

    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        if isinstance(create, CreatePolicy):
            create.clean_up()
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
        "test_case_name": "create_table_traffic_spectrum"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """