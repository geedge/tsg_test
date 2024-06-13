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
            "policy_type": "pxy_manipulation",
            "rule_action_1": "deny",
            "code_1": 403,
            "do_log_1": 2,
            "obj_condition_1": [
            {
                "attribute_name": "ATTR_SUBSCRIBER_ID",
                "object_type": "subscriberid",
                "object_sub_type": "subscriberid",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "default"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_HTTP_URL",
                "object_type": "url",
                "object_sub_type": "url",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "example.com"
                        ]
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
                            "example.com"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_HTTP_REQ_HDR",
                "object_type": "http_signature",
                "object_sub_type": "http_signature",
                "object_list": [
                    {
                    "context_name" : "User-Agent",
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "Mozilla/5.0"
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_HTTP_RES_HDR",
                "object_type": "http_signature",
                "object_sub_type": "http_signature",
                "object_list": [
                    {
                    "context_name" : "Content-Type",
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "text/html"
                        ]
                        }
                    ]
                    }
                ]
                }
            ],
            "profile_condition_1": [
                {
                "profile_type": "response_page",
                "format": "html",
                "name": "auto_test_obj",
                "return_data": 1
                }
            ],
            "app_name_1": ["http"],
            "expected_return": "403",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key":"http_host","query_value":"www.example.com"}],
            "traffic": {
                "type": "wget",
                "command": "wget --debug  -q -O- --user-agent \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36\" https://www.example.com/"
            },
            "token": ""
        }
        
        # 添加测试过程中涉及的template
        template_path = {}
        template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
        template_path["object_template"] = parameter["path"] + "/template/object_template.json"
        template_path["pre_intercept_template_path"] = parameter["path"] + "/template/pre_intercept_template.json"

        # 添加测试过程中涉及的response pages
        template_path["profiles_deny_path"] = parameter["path"] + "/profile_used_to_create_rule/Response-Pages_1.html"
        
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
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.86",
        "api_server": "http://192.168.44.72",
        "test_subcriber_id": "test6473",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 6,
        "is_log": 0,
        "root_path": "D:/python_script/tsg_test",
        "path": "D:/python_script/tsg_test/tests/api",
        "module_name": "security",
        "test_case_name": "deny_alert_200_text_negative_ip_http_not_host"
    }
    run(parameter)