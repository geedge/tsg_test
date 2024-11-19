# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
import pytz
from datetime import datetime
from support.ui_utils.workpath import workdir
from support.ui_utils.ui_client import UIClient
from support.api_utils.api_client import APIClient
from support.packet_generator.traffic_generator import *
from support.report_update import ReportUpdate

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        
        # 参数初始化
        result, exception_result = "", ""
        test_summary = {}
        
        # 脚本启动时间
        start_time = time.time()
        
        policy_configuration = {
            "name": os.path.splitext(os.path.basename(__file__))[0],
            "type": "security",
            "action": "allow",
            "and_conditions": [
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_GTP_PHONE_NUMBER",
                            "type": "mobile_identity",
                            "sub_type": "phone_number",
                            "name": "sec_pn",
                            "items": [
                                {
                                    "op": "add",
                                    "expr_type": "and",
                                    "expression": '^' + parameter['test_phone_number'] + '$',
                                }
                            ]
                        }
                    ]
                },
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_APP_ID",
                            "type": "application",
                            "items": ["http"]
                        }
                    ],
                },
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_HTTP_REQ_BODY",
                            "type": "keyword",
                            "name": "sec_keyword",
                            "items": [
                                {
                                    "op": "add",
                                    "expr_type": "and",
                                    "expression": "helloSecurity"
                                }
                            ]
                        }
                    ]
                }
            ],
            "is_enabled": 1,
            "log_option": "metadata",
        }
        
        traffic_generation = {
            "tool": "http", 
            "command": "curl --connect-timeout 10 -m 10 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"helloSecurity\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" http://192.168.40.206:180/go"
        }
        
        verification_result = {
            "excepted_traffic_result": "helloSecurity",
            "expected_metric": {"hits": 1},
            "expected_log": [
                {"query_field_key":"imsi", "query_value":parameter['test_imsi']},
                {"query_field_key":"phone_number", "query_value": parameter['test_phone_number']}
            ]
        }
        
        # 创建
        if parameter["initiation_method"] == "ui":
            ui_client = UIClient()
            rules_tuple, ui_error = ui_client.create_rules(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
        elif parameter["initiation_method"] == "api":
            api_client = APIClient(parameter)
            # {uuid, type}, i.e., {"12341-232-a21", "ip"}
            objects_tuple, api_error = api_client.create_objects(policy_configuration)
            if len(api_error) > 0:
                return api_error
            rules_tuple, api_error = api_client.create_rules(policy_configuration, objects_tuple, "", "")
            if len(api_error) > 0:
                return api_error

        # 等待下发配置生效
        time.sleep(3)
        
        # 类实例化
        generator = TrafficGenerator()
        
        # 获取当前时间
        utc_tz = pytz.timezone('UTC')
        current_utc_time = datetime.now(utc_tz)
        start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # 触发流量
        traffic_result = generator.run(policy_configuration, traffic_generation)
        
        # 验证流量生成器的返回值是否符合策略执行的预期
        excepted_traffic_result, error = generator.result(verification_result, traffic_result)
        if excepted_traffic_result == False:
            return error
        
        # 验证tsg的日志是否符合策略执行的预期
        if parameter["initiation_method"] == "ui":
            log_result = ui_client.query_rule_log(verification_result, rules_tuple, traffic_result)
        elif parameter["initiation_method"] == "api":
            log_result = api_client.query_rule_log(traffic_generation, verification_result, rules_tuple, start_time, traffic_result)
        if log_result == True:
            test_summary["log"] = "Pass."
        elif log_result == False:
            test_summary["log"] = "The failure reason: the returned log does not match the expected result."
        elif log_result == None:
            test_summary["log"] = "The failure reason: the returned log is empty."
        elif len(log_result) > 0:
            test_summary["log"] = log_result
            
        # 验证tsg的metric是否符合策略执行的预期
        if parameter["initiation_method"] == "ui":
            metric_result = ui_client.query_rule_metric(verification_result, traffic_result)
        elif parameter["initiation_method"] == "api":
            metric_result = api_client.query_rule_metric(verification_result, rules_tuple, start_time, traffic_result)
        if metric_result == True:
            test_summary["metric"] = "Pass."
        elif metric_result == False:
            test_summary["metric"] = "The failure reason: the returned metric does not match the expected result."
        elif metric_result == None:
            test_summary["metric"] = "The failure reason: the returned metric is empty."
        elif len(metric_result) > 0:
            test_summary["metric"] = metric_result
        
        return test_summary
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When running test case, the exception error: ", str(e), flush=True)
        return "When running test case, the exception error: " + str(e)
    finally:
        # 删除
        if parameter["initiation_method"] == "ui":
            if not rules_tuple:
                ui_client.delete_rules(parameter, policy_configuration)
        elif parameter["initiation_method"] == "api":
            if not rules_tuple:
                api_client.delete_rules(rules_tuple)
            if not objects_tuple:
                api_client.delete_objects(objects_tuple)
        
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
        
if __name__ == '__main__':
    # sc rule json example
    policy_configuration = {
        "and_conditions": [
            {
                "negate_option": False,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "object_uuids": [
                            "f5cf118e-99d4-4726-bd57-66ab1ad31a27"
                        ]
                    }
                ]
            },
            {
                "negate_option": False,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_APP_ID",
                        "type": "application",
                        "items": ["http"]
                    }
                ],
            }
        ],
        "action": "service_chaining",
        "type": "service_chaining",
        "action_parameter": {
            "targeted_traffic": "raw",
            "sff_profiles": [
				{
					"name": "sff_zk",
					"type": 1, # 1是steer，2是mirror
					"load_balance_method": "hash-int-ip",
					"load_balance_localization": "nearby",
					"failure_action": "bypass",
					"service_func_profiles": [
						{
							"name": "sf_zk",
							"admin_status": 1,
							"device_group": {
								"value": "City A",
								"tag": "device_group"
							},
							"connectivity": {
								"method": "vxlan_g",
								"dest_ip": "1.1.1.1"
							},
							"health_check": {
								"method": "bfd",
								"interval_ms": 200,
								"retires": 5
							}
						}
					]
				}
            ]
        }
    }
    # monitor rule json example
    policy_configuration = {
        "and_conditions": [
            {
                "negate_option": False,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "object_uuids": [
                            "f5cf118e-99d4-4726-bd57-66ab1ad31a27"
                        ]
                    }
                ]
            },
            {
                "negate_option": False,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_APP_ID",
                        "object_uuids": [
                            "80791b3a-e700-2cb8-8c24-6876d9faa8f8"
                        ]
                    }
                ]
            },
            {
                "negate_option": False,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_HTTP_URL",
                        "type": "url",
                        "member_type": "item",
                        "items": [
                            {
                                "op": "add",
                                "expr_type": "and",
                                "expression": "yumi.com"
                            }
                        ]
                    }
                ]
            }
        ],
        "action_parameter": {
            "traffic_mirroring": {
                "enable": 1,
                "vlanID": 1,
                "mirroring_profile": {
					"name": "mirror_zk",
					"vlan_array": [
						"5"
					]
				}
            },
            "packet_capture": {
                "enable": 1,
                "capture_depth": 2000
            }
        },
        "name": "monitor_zk",
        "log_option": "none",
        "action": "monitor",
        "type": "monitor",
        "is_enabled": 0
    }
    # rule referencing library json example
    policy_configuration = {
        "and_conditions": [
            {
                "negate_option": False,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
						"type": "library",
                        "catalog": {
							"category": "internet_service",
							"ip_entries": [
								{
									"op": "add",
									"ip": "1.1.1.1"
								}
							],
							"fqdn_entries": [
								{
									"op": "add",
									"fqdn": "google.com"
								}
							],
							"tag": {
								"category": "internet_service",
								"parent_uuid": 0, # 有parent则是对应的uuid，如"503a8672-2466-5cb4-a275-00407b8f8e21"
								"description": "",
								"tag_key": "is_zk",
								"tag_value": "is_zk",
								"icon_base64_code": "",
								"icon_position": ""
							}
						}
                    }
                ]
            }
        ],
        "action": "deny",
        "type": "security",
        "action_parameter": {
            "sub_action": "drop",
            "send_tcp_reset": 1,
            "send_icmp_unreachable": 0,
            "after_n_packets": 0,
            "packet_capture": {
                "enable": 0
            }
        },
        "name": "test_zk",
        "log_option": "metadata",
        "is_enabled": 0
    }
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "test_phone_number": "1112231231",
        "test_imsi": "110035141486424",
        "api_server": "http://192.168.44.72",
        "initiation_method": "api",
        "env": "tsgx",
        "vsys": 5,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)