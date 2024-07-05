import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.log_in import *
from support.api_utils.create_config import *
from support.traffic_replay.traffic_verification import *
from support.api_utils.delete_config import *
from support.api_utils.analysis_result import *
from support.report import *

def run(parameter):
    try:
        print("Begin to run test case: " + parameter["test_case_name"])
        # 参数初始化
        result = ""
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "ruleNum": 1,
            "policy_type": "service_chaining",
            "rule_action_1": "service_chaining",
            "targeted_traffic": "decrypted",
            "do_log_1": 2,
            "obj_condition_1":[
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
                                }
                            ]
                        }
                    ]
                },
                {
                    "attribute_name": "ATTR_SERVER_FQDN",
                    "object_type": "fqdn",
                    "object_sub_type": "fqdn",
                    "repeat_time": 1,
                    "object_list": [
                        {
                            "add_item_list": [
                                {
                                    "keyword_array": [
                                        "*vip.com"
                                    ]
                                }
                            ]
                        }
                ]
                }
            ],   
            "profile_condition_1":[
                {
                    "profile_type": "service_function_forwarder",
                    "name": "test_sc_api_steer_block_vxlan_notip_bfd",
                    "type": "1",
                    "load_balance_method": "hash-ext-ip",
                    "load_balance_localization": "nearby",
                    "failure_action": "block",
                    "return_data": 1,
                    "op_action": "add",
                    "sf_condition":[
                        {
                            "profile_type": "service_function",
                            "name": "test_sc_api_vxlan_notip_bfd",
                            "profile_id":None,
                            "device_group":{
                                "tag":"device_group",
                                "value":"group-xxg-tsgx"
                            },
                            "admin_status":1,
                            "connectivity":{
                                "method":"vxlan_g",
                                "dest_ip":"6.6.6.16"
                            },
                            "health_check":{
                                "method":"bfd",
                                "interval_ms": 200,
                                "retires": 5
                            },
                            "is_valid":1,
                            "vsys_id":1
                        }
                    ]
                }               
            ],
            "app_name_1": ["ssl"],
            "expected_return":"Empty,reply",
            "traffic":{
                "type": "curl",
                "command": "curl --connect-timeout 10 --max-time 30 -kv https://www.vip.com"
            },
        }
        
        # 添加测试过程中涉及的template
        template_path = {}
        template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
        template_path["object_template"] = parameter["path"] + "/template/object_template.json"
        template_path["profile_sf_template"] = parameter["path"] + "/template/profile_sf_template.json"
        template_path["profile_sff_template"] = parameter["path"] + "/template/profile_sff_template.json"
        template_path["pre_deny_quic_template_path"] = parameter["path"] + "/template/pre_deny_quic_template.json"
        template_path["pre_intercept_template_path"] = parameter["path"] + "/template/pre_intercept_template.json"
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
        verification_result = verify.traffic_verification("", parameter, test_data, cfg_list)
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
        "username": "lytest",
        "password": "123456ly",
        "test_pc_ip": "192.168.64.86",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 6,
        "is_log": 0,
        "root_path": "C:/Users/17310/Desktop/test/tsg_test",
        "path": "C:/Users/17310/Desktop/test/tsg_test/tests/api",
        "module_name": "service_chaining",
        "test_case_name": "decrypted_filter_steer_block_vxlan_notip_bfd"
    }
    run(parameter)