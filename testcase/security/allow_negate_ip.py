import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.api_common.verify import *

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
    # 测试数据
    test_case_json = {
      "isMultiPriority": False,
      "ruleNum": 1,
      "policyType": "tsg_security",
      "rule_action_1": "allow",
      "do_log_1": 2,
      "obj_condition_1": [
        {
          "not_flag": 1,
          "protocolField": "ATTR_SOURCE_ADDR",
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
      "hope_return": "POST",
      "counters_1": {"hits": 0},
      "log_query_param_1": [],
      "command": "curl -kv http://open.node.com:180"
    }
    # 测试过程中涉及的template
    template_path = {}
    template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
    template_path["obj_template"] = parameter["path"] + "/template/object_template.json"
    verify_res = Verify()
    result = verify_res.start_verify(parameter, test_case_json, template_path)
    return result

if __name__ == "__main__":
    parameter = {
      "username": "zhaokun",
      "password": "zhaokun1",
      "test_pc_ip": "192.168.64.73",
      "api_host": "http://192.168.44.72",
      "is_log": 0,
      "env": "tsgx",
      "vsys_id": 6,
      "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase",
      "module_name": "security",
      "test_case_name": "allow_negate_ip"
    }
    run(parameter)