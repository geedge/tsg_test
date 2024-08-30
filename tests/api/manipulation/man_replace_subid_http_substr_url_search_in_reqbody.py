import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.log_in import *
from support.api_utils.create_policy import *
import time
from support.packet_generator.verification import Verification
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
            "policy_type": "pxy_manipulation",
            "rule_action_1": "replace",
            "user_region": [
                {
                    "search_in": "http_req_body",
                    "regexEnable": 1,
                    "regex_enable": 0,
                    "find": "Artificial",
                    "replace_with": "helloTomorrow",
                }
            ],
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
                            "*node.com:180/go"
                        ]
                        }
                    ]
                    }
                ]
                }
            ],
            "application_1": ["http"],
            "expected_return": "helloTomorrow",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key":"http_host","query_value":"open.node.com"}],
            "traffic": {
                "protocol": "http",
                "type": "curl",
                "command": "curl --connect-timeout 5 -m 10 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"Artificial\\\",\\\"setcook\\\":\\\"asdf\\\",\\\"contenttype\\\": \\\"charset\\\",\\\"responsebody\\\": \\\"responsebodysubstring\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" http://open.node.com:180/go"
            },
            "token": ""
        }
        
        # 添加测试过程中涉及的template
        template_path = {}
        template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
        template_path["object_template"] = parameter["path"] + "/template/object_template.json"
        template_path["pre_intercept_template_path"] = parameter["path"] + "/template/pre_intercept_template.json"
        
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
        
        # 分析验证结果，并返回给flask
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data, cfg_list, verification_result)
        # if len(result) == 0:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
        # elif len(result) != 0:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", result, flush=True)
      
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
        exception_result = str(e)
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
                result_flag = "Fail"
                report_data.append(result_flag)
                report_data.append(result)
            elif exception_result is not None and exception_result != "" and len(exception_result) != 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Fail"
                report_data.append(result_flag)
                report_data.append(exception_result)
            elif result == "" and len(result) == 0 and exception_result == "" and len(exception_result) == 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Pass"
                report_data.append(result_flag)
                report_data.append("")
            new_report = GenerateReport()
            new_report.insert_data(parameter, report_data)
          
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
        "test_case_name": "deny_alert_200_text_negative_ip_http_not_host"
    }
    run(parameter)