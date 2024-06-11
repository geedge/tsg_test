# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from support.general_ui_utils.object.ip_address import IpAddress
from support.ui_utils.element_position.object_element_position import *
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
            "ids": "用例1、IP的增删改查",
            "Name": "test_zk_1",
            "Create": {
                "model": "0",
                "type": "new_object",
                "item": 
                    [
                        "1.1.1.1",
                        "1.1.1.1-1.1.1.1",
                        "192.168.2.1/24",
                        "1:1:1::1/24",
                        "1:1:1::1-1:1:1::1",
                        "94E5:E27A::6041"
                    ]
            },
            "Createtype": "IP",
            "isRepetition": "",
            "Subtype": "",
            "Search_type": "ID"
        }
        
        ipaddress = IpAddress(driver)
        ipaddress.ip_address_case(test_data)
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
        "test_case_name": "temp_create_ip"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """