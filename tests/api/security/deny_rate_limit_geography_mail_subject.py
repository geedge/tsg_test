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
            "rule_action_1": "deny",
            "method_1": "rate_limit",
            "bps_1": 10,
            "do_log_1": 2,
            "obj_condition_1": [
                {
                "attribute_name": "ATTR_DESTINATION_GEO_COUNTRY",
                "object_type": "geolocation",
                "object_sub_type": "geolocation",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "type": "library",
                        "continent": "Asia",
                        "geoname_id": "680501",
                        "super_administrative_area": "auto_geo_obj",
                        "administrative_area": "auto_geo_obj",
                        "country_abbr": "auto_geo_obj",
                        "country": "auto_geo_obj",
                        "location_type": "country",
                        "latitude": "0",
                        "longitude": "0",
                        "addr_type": 4,
                        "ip_address": "192.168.40.206"
                        }
                    ]
                    }
                ]
                },
                {
                "attribute_name": "ATTR_MAIL_SUBJECT",
                "object_type": "keywords",
                "object_sub_type": "keywords",
                "object_list": [
                    {
                    "add_item_list": [
                        {
                        "keyword_array": [
                            "Bestman"
                        ]
                        }
                    ]
                    }
                ]
                }
            ],
            "app_name_1": ["mail"],
            "expected_return": "timeout",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key":"mail_account","query_value":"hbn@163.com"}],
            "traffic": {
                "type": "curl",
                "command": "curl --connect-timeout 10 -m 10 --url \"smtp://192.168.40.206\" --mail-from \"hbn@163.com\" --mail-rcpt \"autotest@163.com\" -H @/opt/traffic_replay/mail_file/subjectEnglish.txt --user \"hbn@163.com:111111\" -F '=(;type=multipart/mixed' -F '=(;type=multipart/mixed' -F \"=\"Bestman\";type=text/plain\" -F \"file=@/opt/traffic_replay/mail_file/mail_test_english.txt;type=`file --mime-type \"/opt/traffic_replay/mail_file/mail_test_english.txt\"|sed 's/.*: //'`;encoder=base64\" -F '=)'"
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
        # print("verification result: ", verification_result)
        
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
        
        print("Finish test case: " + parameter["test_case_name"])
        return result
    except Exception as e:
      print("Error: ", e)
      return "Error: " + str(e)
    finally:
        name_list = []
        erase = DeleteConfig()
        erase.clear_config(token, parameter, name_list)
  
if __name__ == "__main__":
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.86",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 6,
        "is_log": 1,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/api",
        "module_name": "security",
        "test_case_name": "allow_http_fqdn"
    }
    run(parameter)