# -*- coding: UTF-8 -*-
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from support.general_ui_utils.object.tunnel import Tunnel
import support.ui_utils.env_initialization


def run(parameter):
    try:
        print("Begin to run test case: " + parameter["test_case_name"])
        # 脚本启动时间
        start_time = time.time()

        # 环境初始化
        support.ui_utils.env_initialization.initiate_selenium_request()
        driver = support.ui_utils.env_initialization.my_driver()
        support.ui_utils.env_initialization.setup()

        # 测试数据
        test_data = {
            "ids":"Tunnel的增删改查:IP",
            "Search_type":"ID",
           "type": "GRE"
        }

        t = Tunnel(driver)
        t.tunnel_case(test_data)
        result = ""

        # 清理环境
        support.ui_utils.env_initialization.teardown()

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print("Duration of running the test case: ", duration)

        print("Finish test case: " + parameter["test_case_name"])
        return result
    except Exception as e:
        print("Error: ", e)
        return "Error: " + str(e)


if __name__ == '__main__':
    parameter = {
        "username": "lotus",
        "password": "lotus2023",
        "test_pc_ip": "192.168.38.138",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 0,
        "is_log": 0,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
        "module_name": "object",
        "sub_module_name": "",
        "test_case_name": "crud_gre_type_tunnel.py"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """