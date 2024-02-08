import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.api.logIn import *
from src.api.createConfig import *
from src.api.trafficVerification import *
from src.api.deleteConfig import *
from src.api.analysisResult import *

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
    # 测试数据
    test_data_json = {
      "isMultiPriority": False,
      "ruleNum": 1,
      "policyType": "security",
      "rule_action_1": "allow",
      "do_log_1": 2,
      "obj_condition_1": [
        {
          "is_negate": 1,
          "attribute_name": "ATTR_SOURCE_IP",
          "objectType": "ip",
          "objectSubType": "ip",
          "objectList": [
            {
              "addItemList": [
                {
                  "ip_address": "default",
                  "port_range": "0-65535"
                }
              ]
            }
          ]
        }
      ],
      "app_name_1": ["http"],
      "expectedReturn": "POST",
      "counters_1": {"hits": 0},
      "log_query_param_1": [],
      "command": "curl -kv http://open.node.com:180"
    }
    
    # 添加测试过程中涉及的template
    template_path = {}
    template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
    template_path["object_template"] = parameter["path"] + "/template/object_template.json"
    
    # 获取token
    log_in = LogIn()
    pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
    token = log_in.login(parameter["username"], pwd, parameter["api_server"])
    parameter["token"] = token
    
    # 创建Object、Profile、Rule
    config = CreateConfig()
    cfg_list = config.create_cfg(parameter, test_data_json, template_path)
    
    # 流量验证
    verify = TrafficVerification()
    verification_result = verify.traffic_verification(parameter, test_data_json, template_path, cfg_list)
    print("verification result: ", verification_result)
    
    # 分析验证结果，并返回给flask
    analysis = AnalysisResult()
    result = analysis.analysis_result(test_data_json, cfg_list, verification_result)
    print("analysis result: ", result)
   
    # 删除配置
    erase = DeleteConfig()
    erase.delele_cfg(token, parameter, cfg_list)
    
    print("Finish test case: " + parameter["test_case_name"])
    return result

if __name__ == "__main__":
    parameter = {
      "username": "zhaokun",
      "password": "zhaokun1",
      "test_pc_ip": "192.168.64.73",
      "api_server": "http://192.168.44.72",
      "is_log": 0,
      "env": "tsgx",
      "vsys_id": 6,
      "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase",
      "module_name": "security",
      "test_case_name": "allow_negate_ip"
    }
    run(parameter)