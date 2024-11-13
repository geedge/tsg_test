# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from datetime import datetime
from support.ui_utils.workpath import workdir
from support.ui_utils.common.ui_client import UIClient
from support.api_utils.api_client_old import APIClient
# from support.api_utils.api_client_2410 import APIClient
from support.analyse_result_backup import Analyse
from support.cmdb_collector_backup import CMDBCollector
# from support.packet_generator.verify import Verify
from support.verify import Verify
# from support.packet_generator.traffic_generator import *
from support.traffic_generator import *
from support.report_update import ReportUpdate

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        
        # 参数初始化
        result, exception_result = "", ""
        configuration_manager = {}
        
        # 脚本启动时间
        start_time = time.time()
        
        policy_configuration = {
            "name": "automation_test_zk",
            "type": "security",
            "action": "deny",
            "and_conditions": [
                {
                    "negate_option": 0,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_SOURCE_IP",
                            "type": "ip",
                            "sub_type": "ip",
                            "name": "sec_srcip",
                            "items": [
                                {
                                    "op": "add",
                                    "ip": parameter["test_pc_ip"],
                                    "interval": "0-65535"
                                }
                            ]
                        }
                    ]
                },
                {
                    "negate_option": 0,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_APP_ID",
                            "type": "application",
                            "items": ["http"]
                        }
                    ],
                }
            ],
            "action_parameter": {
                "sub_action": "drop",
                "packet_capture": {
                    "enable": 0
                },
                "send_tcp_reset": 1,
                "send_icmp_unreachable": 0,
                "after_n_packets": 1
            },
            "is_enabled": 1,
            "log_event": True
        }
        
        traffic_generation = {
            "tool": "http", # or trex/http
            "command": "curl -kv --connect-timeout 10 -m 10 http://open.node.com:180"
        }
        
        verification_result = {
            "expected_result": "reset",
            "metric_query": {"hits": 1},
            "log_query": [
                {"query_field_key":"http_host", "query_value": "open.node.com"}
            ]
        }
        
        # 创建
        cmdb_collector = CMDBCollector()
        if parameter["initiation_method"] == "ui":
            ui_client = UIClient()
            configuration_manager, error = ui_client.create_rule(parameter, policy_configuration)
            if len(error) > 0:
                return error
        elif parameter["initiation_method"] == "api":
            api_client = APIClient(parameter)
            configuration_manager["token"] = api_client.token
            object_uuid, object_error = api_client.create_objects(policy_configuration)
            print(json.dumps(object_uuid))
            if len(object_error) > 0:
                return object_error
            # configuration_manager["object_uuid_list"] = cmdb_collector.collect(object_uuid)
            rule_uuid, rule_error = api_client.create_rules(policy_configuration, object_uuid)
            print(json.dumps(rule_uuid))
            if len(rule_error) > 0:
                return rule_error
            # configuration_manager["rule_uuid_list"] = cmdb_collector.collect(rule_uuid)

        # 触发流量
        time.sleep(3)
        generator = TrafficGenerator()
        traffic_result = generator.generate_traffic(policy_configuration, traffic_generation)
        
        verification = Verify()
        # 验证流量生成器的返回值是否符合策略执行的预期
        excepted_traffic_result, error = verification.verify_traffic_result(verification_result, traffic_result)
        if excepted_traffic_result == False:
            return error
        
        # 验证tsg的日志和metric是否符合策略执行的预期
        excepted_metric_log_result = verification.verify_metric_log(parameter, policy_configuration, traffic_generation, verification_result, configuration_manager, traffic_result)
        if len(excepted_metric_log_result) != 3:
            return excepted_metric_log_result

        # 分析结果
        analyse = Analyse()
        result = analyse.analyse_result(policy_configuration["type"], excepted_metric_log_result)
        
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception Error: ", str(e), flush=True)
        return "Exception Error: " + str(e)
    finally:
        # 删除
        cmdb_collector.cleanup(parameter, api_client.token, configuration_manager)
        
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
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "debug": "local",
        "initiation_method": "api",
        "env": "tsgx",
        "vsys": 5,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)