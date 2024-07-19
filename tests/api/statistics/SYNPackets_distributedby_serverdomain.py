import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.api_utils.log_in import *
from support.api_utils.create_policy import *
from support.traffic_manager.traffic_verification import *
from support.api_utils.delete_policy import *
from support.api_utils.analysis_result import *
import traceback
from support.report import *
from datetime import datetime

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        result = ""
        
        # 脚本启动时间
        start_time = time.time()
        
        # 脚本启动时间
        start_time = time.time()
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "statistics",
            "rule_action_1": "statistics",
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
                    "attribute_name": "ATTR_DESTINATION_IP",
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
                }
            ],
            "profile_condition_1": [
                {
                    "profile_type": "Statistics_Templates",
                    "name": "random_name",
                    "chart_list": [
                        {
                            "type": "table",
                            "metrics": [
                                {
                                    "source_columns": "syn_pkts",
                                    "function": "SUM"
                                }
                            ],
                            "dimensions": [
                                {
                                    "source_columns": [
                                        "server_fqdn"
                                    ],
                                    "is_drilldown": 0
                                }
                            ],
                            "order_by": None,
                            "limit": 1000,
                            "drilldown_limit": None,
                            "threshold": {
                                "in_bytes": "10",
                                "out_bytes": "10"
                            }
                        }
                    ]
                }
            ],
            "app_name_1": [],
            "expected_return": "POST",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key": "http_host", "query_value": "open.node.com"}],
            "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "192.168.64.86",
                "clients_end_ip": "192.168.64.86",
                "servers_start_ip": "2.1.1.1",
                "servers_end_ip": "2.1.1.2",
                "m": 1,
                "d": 1,
                "yaml_name": "test_https",
                "pcap_name": "test_https"
            },
            "token": ""
        }

        # 添加测试过程中涉及的template
        template_path = {}
        template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
        template_path["object_template"] = parameter["path"] + "/template/object_template.json"
        template_path["profile_statistics_template"] = parameter["path"] + "/template/profile_statistics_template.json"

        # 获取token
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token
        
        # 创建Object、Profile、Rule
        create = CreatePolicy()
        cfg_list = create.create_policy(parameter, test_data, template_path)
        
        # 流量验证
        verify = TrafficVerification()
        verification_result = verify.traffic_verification("", parameter, test_data, cfg_list)
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
        traceback.print_exc()
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
        "test_pc_ip": "192.168.64.86",
        "api_server": "http://192.168.44.72",
        "test_subcriber_id": "test68",
        "debug_flag": "local",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 6,
        "is_log": 0,
        "root_path": "C:/zcw/tsg_test",
        "path": "C:/zcw/tsg_test/tests/api",
        "module_name": "statistics",
        "test_case_name": "SYNPackets_distributedby_serverdomain"
    }
    run(parameter)