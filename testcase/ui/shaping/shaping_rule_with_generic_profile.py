# -*- coding: UTF-8 -*-
import time
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.ui.profile.shaping.shapingProfile import ShapingProfile
from src.ui.object.ip.ipObject import IpAddress
from src.ui.policy.shaping.shapingRuleWithGeneric import ShapingRuleWithGeneric
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
      "policyType": "shaping"
    }
    ip_data = {
        "ids": "创建ip object用例",
        "name": "shaping_source_ip",
        "model": "create",
        "type": "new_ip_object",
        "item": [
            "1.1.1.1",
            "1.1.1.1-1.1.1.2"
        ],
        "createtype": "ip",
        "subtype": "",
        "search_type": "id"
    }
    profile_data = {
        "ids": "创建generic bps用例",
        "name": "shaping_generic_profile",
        "model": "create",
        "type": "generic",
        "argument": "",
        "unit": "bps->",
        "incoming": "2000->",
        "outgoing": "500->"
    }
    rule_data = {
        "ids": "创建shaping rule用例",
        "name": "shaping_rule_with_generic_profile",
        "model": "create",
        "type": "new_shaping_rule"
    }
    
    # 添加测试过程中涉及的template
    template_path = {}
    template_path["trex_workpath"] = "/opt/trex/v3.03"
    template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"
    
    # 创建ip
    ip_address = IpAddress(driver)
    ip_result = ip_address._create(ip_data)
    
    # 创建profile
    shaping_profile = ShapingProfile(driver)
    shaping_profile_result = shaping_profile._create(profile_data)
    
    # 创建rule
    if ip_result == 200 and shaping_profile_result == 200:
        shaping_rule = ShapingRuleWithGeneric(driver)
        shaping_rule_result = shaping_rule._create(ip_data["name"], profile_data["name"], rule_data["name"])
        
    # 触发流量验证
    if shaping_rule_result == 200:
        verify = TrafficVerification()
        verification_result = verify.traffic_verification(parameter, test_data_json, template_path, [])
    
    # 分析验证结果，并返回给flask
    if len(verification_result) != 0:
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data_json, [], verification_result)
    
    # 删除rule
    shaping_rule._search(rule_data["name"])
    shaping_rule._delete()
    
    # 删除ip
    ip_address._search(ip_data["name"])
    ip_address._delete()
    
    # 删除profile
    shaping_profile._search(profile_data, Name=profile_data["name"])
    shaping_profile._delete()
    
    # 清理环境
    src.ui.envInitialization.teardown()
    
    # 脚本结束时间和耗时
    end_time = time.time()
    duration = end_time - start_time
    print("用时：", duration)
    
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
      "module_name": "shaping",
      "test_case_name": "shaping_rule_with_generic_profile"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """