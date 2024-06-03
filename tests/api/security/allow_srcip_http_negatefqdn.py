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
        # 脚本启动时间
        start_time = time.time()
        
        # 测试数据
        test_data = {
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
                    "repeat_time": 1,
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
                    "repeat_time": 1,
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
        
        # 分析验证结果，并返回给flask
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data, cfg_list, verification_result)
        if len(result) == 0:
            print("The test case is passed.")
        elif len(result) != 0:
            print("The test case is failed. The failure reason is: ", result)
      
        # 删除配置
        erase = DeleteConfig()
        erase.delele_cfg(token, parameter, cfg_list)
        
        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print("Duration of running the test case: ", duration)
            
        print("Finish test case: " + parameter["test_case_name"])
        return result
    except Exception as e:
        print("Error: ", e)
        return "Error: " + str(e)
  
if __name__ == "__main__":
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.86",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 6,
        "is_log": 0,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/api",
        "module_name": "security",
        "test_case_name": "allow_negate_fqdn"
    }
    run(parameter)