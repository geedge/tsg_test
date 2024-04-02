import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.log_in import *
from support.api_utils.create_config import *
from support.traffic_replay.traffic_verification import *
from support.api_utils.delete_config import *
from support.api_utils.analysis_result import *
from support.app_utils.call_airtest import *

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
          "is_negate": 1,
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
      "counters_1": {"hits": 0},
      "log_query_param_1": [],
      "command": "curl -kv http://open.node.com:180"
    }
    
    call_airtest = CallAirtest(parameter["app_full_name"])
    call_airtest.start_airtest()
    device_id = call_airtest.getDeviceId()

    # 获取token
    log_in = LogIn()
    pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
    token = log_in.login(parameter["username"], pwd, parameter["api_server"])
    parameter["token"] = token
    
    # 创建Object、Profile、Rule
    config = CreateConfig()
    template_path = {}
    cfg_list = config.create_cfg(parameter, test_data_json, template_path)
    
    result = call_airtest.run_airtest_script(device_id, parameter["app_name"])
    if result == 0:
        call_airtest.stop_airtest()
    elif result != 0:
        call_airtest.verifyResult()
        # 分析验证结果，并返回给flask
        analysis = AnalysisResult()
        verification_result = [True, True, True]
        result = analysis.analysis_result(test_data_json, cfg_list, verification_result)
        print("analysis result: ", result)
   
    # 删除配置
    erase = DeleteConfig()
    erase.delele_cfg(token, parameter, cfg_list)
            
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
      "test_case_name": "security_rule_with_deny_ip_quic",
      "app_name": "taobao",
      "app_full_name": "com.taobao.taobao",
    }
    run(parameter)