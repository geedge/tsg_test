import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.log_in import *
from support.api_utils.create_config import *
from support.traffic_replay.traffic_verification import *
from support.api_utils.delete_config import *
from support.api_utils.analysis_result import *

def run(parameter):
  try:
    print("Begin to run test case: " + parameter["test_case_name"])
    # 测试数据
    test_data = {
      "is_multi_priority": True,
      "rule_num": 2,
      "policy_type": "security",
      "rule_action_1": "deny",
      "method_1": "drop",
      "rule_action_2": "deny",
      "method_2": "drop",
      "do_log_1": 2,
      "do_log_2": 2,
      "obj_condition_1": [
        {
          "attribute_name": "ATTR_SOURCE_IP",
          "object_type": "ip",
          "object_sub_type": "ip",
          "object_list": [
            {
              "add_item_list": [
                {
                  "ip_address": "default",
                  "port_range": "0-65535"
                }
              ]
            }
          ]
        }
      ],
      "obj_condition_2": [
        {
          "attribute_name": "ATTR_SOURCE_IP",
          "object_type": "ip",
          "object_sub_type": "ip",
          "object_list": [
            {
              "add_item_list": [
                {
                  "ip_address": "default",
                  "port_range": "0-65535"
                }
              ]
            }
          ]
        }
      ],
      "app_name_1": ["ssl"],
      "app_name_2": ["ssl"],
      "expected_return": "reset",
      "counters_1": {"hits": 0},
      "counters_2": {"hits": "many"},
      "log_query_param_1": [],
      "log_query_param_2": [],
      "traffic": {
                "type": "curl",
                "command": "curl -kv --connect-timeout 10 -m 10 https://www.baidu.com"
            },
      "token": ""
    }
    
    # 添加测试过程中涉及的template
    template_path = {}
    template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
    template_path["object_template"] = parameter["path"] + "/template/object_template.json"
    
    # 获取token
    log_in = LogIn()
    pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
    token = log_in.login(parameter["username"], pwd, parameter["api_server"])
    test_data["token"] = token
    
    # 创建Object、Profile、Rule
    config = CreateConfig()
    cfg_list = config.create_cfg(parameter, test_data, template_path)
    
    # 流量验证
    verify = TrafficVerification()
    verification_result = verify.traffic_verification(parameter, test_data, cfg_list)
    print("verification result: ", verification_result)
    
    # 分析验证结果，并返回给flask
    analysis = AnalysisResult()
    result = analysis.analysis_result(test_data, cfg_list, verification_result)
    print("analysis result: ", result)
   
    # 删除配置
    erase = DeleteConfig()
    erase.delele_cfg(token, parameter, cfg_list)
    
    print("Finish test case: " + parameter["test_case_name"])
    return result
  except Exception as e:
      print("Error: ", e)
      return "Error: " + str(e)
    finally:
        erase = DeleteConfig()
        erase.clear_config(token, parameter)
    if __name__ == "__main__":
    parameter = {
      "script_type": "api",
      "username": "hebingning",
      "password": "hbn66AAA",
      "test_pc_ip": "192.168.64.73",
      "api_server": "http://192.168.44.72",
      "is_log": 1,
      "env": "tsgx",
      "vsys_id": 6,
      "root_path": "D:/python_script/tsg_test",
      "path": "D:/python_script/tsg_test/tests/api",
      "module_name": "security",
      "test_case_name": "allow_negate_fqdn"
    }
    run(parameter)