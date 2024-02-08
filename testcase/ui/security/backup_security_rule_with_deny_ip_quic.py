# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.ui.object.ip.ipObject import IpAddress
from src.ui.policy.backup_security.securityRule import SecurityRule
from src.api.trafficVerification import *
from src.api.analysisResult import *
import src.ui.envInitialization

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
    # 脚本启动时间
    start_time = time.time()
    
    # 环境初始化
    driver = src.ui.envInitialization.my_driver()
    src.ui.envInitialization.setup()
    
    # 测试数据
    test_data_json = {
        "isMultiPriority": False,
        "ruleNum": 1,
        "policyType": "security",
        "ruleName": "security_rule_with_deny_ip_quic",
        "ruleType": "create",
        "ip":[
            {
                "name": "security_source_ip",
                "objectType": "create",
                "item": [
                    "1.1.1.1",
                    "1.1.1.1-1.1.1.2"
                ]
            }
        ],
        "application":[
            {
                "name": "quic"
            }
        ],
        "profile":[
        ],
        "hope_return": "POST",
        "counters_1": {"hits": 0},
        "log_query_param_1": [],
        "command": "curl -kv https://www.google.com"
    }
    
    # 添加测试过程中涉及的template
    template_path = {}
    template_path["trex_workpath"] = "/opt/trex/v3.03"
    template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"
    
    # 创建ip
    ip_data = test_data_json["ip"]
    ip_address = IpAddress(driver)
    for i in range(len(ip_data)):
        ip_result = ip_address._create(ip_data[i])
    
    # 创建rule
    if ip_result == 200:
        security_rule = SecurityRule(driver)
        security_rule_result = security_rule._create(test_data_json)
        
    # 触发流量验证
    if security_rule_result == 200:
        verify = TrafficVerification()
        verification_result = verify.traffic_verification(parameter, test_data_json, template_path, [])
        print("verification result: ", verification_result)
    
    # 分析验证结果，并返回给flask
    if len(verification_result) != 0:
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data_json, [], verification_result)
        print("analysis result: ", result)
    
    # 删除rule
    security_rule._search(test_data_json["ruleName"])
    security_rule._delete()
    
    # 删除ip
    for j in range(len(ip_data)):
        ip_address._search(ip_data[j]["name"])
        ip_address._delete()
    
    # 清理环境
    src.ui.envInitialization.teardown()
    
    # 脚本结束时间和耗时
    end_time = time.time()
    duration = end_time - start_time
    print("duration: ", duration)
    
    print("Finish test case: " + parameter["test_case_name"])
    return result

if __name__ == '__main__':
    parameter = {
      "username": "zhaokun",
      "password": "zhaokun1",
      "test_pc_ip": "192.168.64.73",
      "api_server": "http://192.168.44.72",
      "is_log": 0,
      "env": "tsgx",
      "vsys_id": 6,
      "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
      "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
      "module_name": "security",
      "test_case_name": "security_rule_with_deny_ip_quic"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """