
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
            "is_multi_priority": True,
            "rule_num": 2,
            "policy_type": "security",
            "rule_action_1": "shunt",
            "rule_action_2": "allow",
            "do_log_1": 0,
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
            },
            {
                "attribute_name": "ATTR_FLAG",
                "object_type": "flag",
                "object_sub_type": "flag",
                "object_list": [
                {
                    "add_item_list": [
                    {
                        "flag": 8,
                        "mask": 8
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
            "app_name_1": [],
            "app_name_2": [],
            "expected_return": "百度一下",
            "counters_1": {"hits": "many"},
            "counters_2": {"hits": 0},
            "log_query_param_1": [],
            "log_query_param_2": [],
            "traffic": {
                    "protocol": "ssl",
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