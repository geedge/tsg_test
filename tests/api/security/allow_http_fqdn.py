import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.log_in import *
from support.api_utils.create_config import *
from support.traffic_replay.traffic_verification import *
from support.api_utils.delete_config import *
from support.api_utils.analysis_result import *

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
    # 测试数据
    test_data_json = {
      "is_multi_priority": False,
      "rule_num": 1,
      "policy_type": "security",
      "rule_action_1": "allow",
      "do_log_1": 2,
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
        },
        {
          "attribute_name": "ATTR_SERVER_FQDN",
          "object_type": "fqdn",
          "object_sub_type": "fqdn",
          "object_list": [
            {
              "add_item_list": [
                {
                  "keyword_array": [
                    "open.node.com"
                  ]
                }
              ]
            }
          ]
        }
      ],
      "app_name_1": ["http"],
      "expected_return": "POST",
      "counters_1": {"hits": 1},
      "log_query_param_1": [{"query_field_key":"http_host","query_value":"open.node.com"}],
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
    verification_result = verify.traffic_verification(parameter, test_data_json, cfg_list)
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
      "script_type": "api",
      "username": "hebingning",
      "password": "hbn66AAA",
      "test_pc_ip": "192.168.64.76",
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