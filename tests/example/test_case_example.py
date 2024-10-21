# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from datetime import datetime
from support.ui_utils.workpath import workdir
from support.ui_utils.common.ui_client import UIClient
from support.api_utils.api_client import APIClient
from support.analyse_result import Analyse
from support.cmdb_collector import CMDBCollector
from support.packet_generator.verify import Verify
from support.packet_generator.traffic_generator import *
from support.report_update import ReportUpdate

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        
        # 参数初始化
        result, exception_result = "", ""
        configuration_manager = {
            "object_uuid_list": [],
            "rule_uuid_list": []
        }
        
        # 脚本启动时间
        start_time = time.time()
        
        policy_configuration = {
            "name": "automation_test_zk",
            "type": "security",
            "action": "deny",
            "source": [
                {
                    "attribute_name": "ATTR_SOURCE_IP",
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
            "application": {
                "attribute_name": "ATTR_APP_ID",
                "negate_option": False,
                "objects": [
                    {
                        "object_type": "application",
                        "name": "http"
                    }
                ],
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

        # 创建
        cmdb_collector = CMDBCollector()
        if parameter["initiation_method"] == "ui":
            ui_client = UIClient()
            configured_policy = ui_client.create_rule(parameter, policy_configuration)
        elif parameter["initiation_method"] == "api":
            api_client = APIClient()
            object_uuid = api_client.create_object(parameter, policy_configuration)
            configuration_manager["object_uuid_list"] = cmdb_collector.collect(object_uuid)
            rule_uuid = api_client.create_rule(object_uuid)
            configuration_manager["rule_uuid_list"] = cmdb_collector.collect(rule_uuid)
        
        if len(configured_policy["result"]) != 0:
            result = configured_policy["result"]
            return result

        # 触发流量
        generator = TrafficGenerator()
        traffic_result = generator.generate_traffic(traffic_generation)
        
        # 验证流量生成器的返回值是否符合策略执行的预期
        verify = Verify()
        verification_result = verify.verify_result(parameter, verification, configured_policy, traffic_result)
        
        # 验证tsg的日志和metric是否符合策略执行的预期
        
        
        if len(verification_result) != 4:
            result = verification_result
            return result

        # 分析结果
        analyse = Analyse()
        result = analyse.analyse_result(verification_result)
        
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception Error: ", e, flush=True)
        return "Exception Error: " + str(e)
    finally:
        # 删除
        cmdb_collector.cleanup(parameter, configured_policy["token"], configuration_manager)
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
        "initiation_method": "api",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)