# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from support.general_ui_utils.object.tunnel import Tunnel
import support.ui_utils.env

def run(parameter):
    try:
        print("Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        result = ""
        
        # 脚本启动时间
        start_time = time.time()

        # 环境初始化
        support.ui_utils.env.initiate_selenium_request()
        driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()

        # 测试数据
        test_data = {
            "ids": "Tunnel的增删改查:IP",
            "Search_type": "ID",
            "type": "IP"
        }

        t = Tunnel(driver)
        t.tunnel_case(test_data)
        result = ""

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print("Duration of running the test case: ", "{:.3f}".format(duration), flush=True)

        print("Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        print("Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境
        support.ui_utils.env.teardown()

if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.86",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 0,
        "is_log": 0,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
        "module_name": "object",
        "sub_module_name": "ip_address",
        "test_case_name": "crud_ip_type_tunnel"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """