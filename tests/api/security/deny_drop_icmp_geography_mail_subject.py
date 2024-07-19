import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.log_in import *
from support.api_utils.create_policy import *
import time
from support.traffic_manager.verification import Verification
from support.api_utils.delete_policy import *
from support.api_utils.analysis_result import *
from support.report import *
from datetime import datetime

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        result, exception_result = "", ""
        
        # 脚本启动时间
        start_time = time.time()
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_action_1": "deny",
            "method_1": "drop",
            "do_log_1": 2,
            "send_tcp_reset_1": 0,
            "send_icmp_unreachable_1": 1,
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
                        "geoname_id": "971420",
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
            "log_query_param_1": [{"query_field_key":"mail_subject","query_value":"Bestman"}],
            "traffic": {
                "protocol": "mail",
                "type": "curl",
                "command": "curl -kv --connect-timeout 25 -m 25 --url 'smtp://192.168.40.206' --mail-from 'hbn@163.com'  --mail-rcpt 'autotest@163.com'  --upload-file '/app/support/traffic_manager/mail_file/subjectEnglish.txt'   --user 'hbn@163.com:111111'"
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
        create = CreatePolicy()
        cfg_list = create.create_policy(parameter, test_data, template_path)
        
        # 流量验证
        verify = Verification()
        verification_result = verify.verification("", parameter, test_data, cfg_list, "")
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "verification result: ", verification_result, flush=True)
        
        # 分析验证结果，并返回给flask
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data, cfg_list, verification_result)
        if len(result) == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
        elif len(result) != 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", result, flush=True)
    
        # 删除配置
        delete = DeletePolicy()
        delete.delele_policy_by_cfg(token, parameter, cfg_list)
        
        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        name_list = []
        delete = DeletePolicy()
        delete.delete_policy_by_name(token, parameter, name_list)
        # 生成csv报告
        file_path = parameter["root_path"] + "/report/{}_report.csv".format(parameter["script_type"])
        if os.path.exists(file_path) and os.path.isfile(file_path):  
            if result is not None and result != "" and len(result) != 0:
                report_data = []
                report_data.append(parameter["test_case_name"])
                if False in verification_result:
                    result_flag = "Fail"
                else:
                    result_flag = "Pass"
                report_data.append(result_flag)
                report_data.append(result)
                new_report = GenerateReport()
                new_report.insert_data(parameter, report_data)
      
if __name__ == "__main__":
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.88",
        "test_subcriber_id": "test6488",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 6,
        "is_log": 1,
        "root_path": "D:/python_script/tsg_test",
        "path": "D:/python_script/tsg_test/tests/api",
        "module_name": "security",
        "test_case_name": "allow_http_fqdn"
    }
    run(parameter)