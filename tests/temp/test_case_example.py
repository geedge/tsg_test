# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from datetime import datetime
from support.report_update import ReportUpdate
from support.common_utils.create_policy import CreatePolicy
from support.packet_generator.verify import Verify
from support.packet_generator.trigger_traffic import *
from support.api_utils.analyse_result import Analyse
from support.ui_utils.workpath import workdir
from support.common_utils.delete_security_policy_example import DeleteSecurityPolicy

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        
        # 参数初始化
        result = {}
        exception_result, driver = "", ""
        
        # 脚本启动时间
        start_time = time.time()
        
        policy_configuration = {
            "name": "automation_test_zk",
            "type": "security",
            "action": "deny",
            "source": [
                {
                    "negate_option": False,
                    "objects": [
                        {
                            "object_type": "ip",
                            "object_sub_type": "ip",
                            "name": "secy_srcip",
                            "items": [
                                {
                                    "op": "add",
                                    "ip": "1.1.1.1",
                                    "interval": "0-65535"
                                }
                            ]
                        }
                    ]
                }
            ],
            "destination": [
                {
                    "negate_option": False,
                    "objects": [
                        {
                            "object_type": "fqdn",
                            "object_sub_type": "fqdn",
                            "name": "secy_fqdn",
                            "items": [
                                {
                                    "op": "add",
                                    "expr_type":"and",
                                    "expression": "^example.com"
                                }
                            ]
                        }
                    ]
                }
            ],
            "application": {
                "objects": [
                    {
                        "object_type": "application",
                        "name": "http"
                    }
                ],
                "negate_option": False
            },
            "action_parameter": {
                "method": "block",
                "packet_capture": {
                    "enable": 0
                    # "capture_depth": 2000
                },
                "code": 403,
                "profile": {
                    "format": "html",
                    "name": "secy_respage",
                    "content_name": workdir + "/support/ui_utils/profile/profile_file/testa.html",
                },
                "message": "html_profile"
            },
            "is_enabled": True
        }
        traffic_generation = {
            "tool": "curl", # or trex/http
            "command": "curl -kv --connect-timeout 10 -m 10 http://www.example.com/"
        }
        verification = {
            "expected_result": "Example Domain",
            "metric_query": {"hits": 2},
            "log_query": [
                {"query_field_key":"server_fqdn", "query_value": "www.example.com"}
            ]
        }
        
        # initiation_method = "ui" # or api
        # if (interface_type == "ui"):
        #     configured_policy = #
        # else if(interface_type == "api"):
        #     configured_policy = #
        # else 
        #     return error
        
        # generate_traffic("json")
        
        # if(interface_type == "ui"):
            
        # loop_number = 1
        # if len(parameter["script_type"]) == 0: # 修改script_type
        #     loop_number = 2 # 修改loop_number
        # for i in range(loop_number):
        
        # 环境初始化
        if parameter["initiation_method"] == "ui":
            support.ui_utils.env.initiate_selenium_request()
            driver = support.ui_utils.env.my_driver()
            support.ui_utils.env.setup()
            
        # 创建
        create = CreatePolicy(policy_configuration, parameter, driver)
        configured_policy = create.create_policy()
        
        if len(configured_policy["result"]) == 0:
            # 触发流量
            sender = SendTraffic()
            traffic_result = sender.send_traffic(parameter, traffic_generation)
            
            # 验证
            verify = Verify()
            verification_result = verify.verify_result(parameter, verification, configured_policy, traffic_result)
            
            if len(verification_result) == 4:
                # 分析结果
                analysis = Analyse()
                result["result"] = analysis.analyse_result(policy_configuration["type"], configured_policy, verification_result)
                
                # 删除
                delete = DeleteSecurityPolicy()
                deleted_policy = delete.delete_security_policy(parameter, test_data, configured_policy)
                if len(deleted_policy["result"]) > 0:
                    result["result"] = result["result"] + deleted_policy["result"]
            else:
                result = verification_result
        else:
            result = configured_policy
            
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception Error: ", e, flush=True)
        return "Exception Error: " + str(e)
    finally:
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
            
if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.86",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/tests/api",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)