# # -*- coding: UTF-8 -*-
# import time
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
# from datetime import datetime
# from support.report_update import ReportUpdate
# from support.common_utils.create_policy import CreatePolicy

# def run(parameter):
#     try:
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
#         # 参数初始化
#         exception_result = ""
#         result = {}
        
#         # 脚本启动时间
#         script_start_time = time.time()
        
#         # 测试数据
#         test_data = {
#             "is_multi_priority": False,
#             "rule_num": 1,
#             "policy_type": "security",
#             "rule_name": os.path.splitext(os.path.basename(__file__))[0],
#             "rule_action": "deny",
#             "rule_type": "create",
#             "condition": {
#                 "source_ip": [
#                     {
#                         "name": "sec_srcip",
#                         "object_type": "ip",
#                         "select_type": False,
#                         "negate": False,
#                         "item": [
#                             {
#                                 "item_operation": "add",
#                                 "item_type": "ipv4",
#                                 "item_value": parameter['test_pc_ip'],
#                             }
#                         ]
#                     }
#                 ],
#                 "source_port": [],
#                 "destination_ip": [],
#                 "destination_port": [],
#                 "internal_ip": [],
#                 "internal_port": [],
#                 "external_ip": [],
#                 "external_port": [],
#                 "source_geography": [],
#                 "destination_geography": [],
#                 "sub_id": [],
#                 "device": [],
#                 "tunnel": [],
#                 "tunnel_level": [],
#                 "flag": [],
#                 "application": [
#                     {
#                         "name": "common_server_fqdn", #
#                         "object_type": "application",
#                         "negate": False
#                     }
#                 ],
#                 "server_fqdn": [],
#                 "protocol_filed": [],
#                 "sub_action_override": False,
#                 "sub_action": [],
#                 "packet_capture": []
#             },
#             "profile": [],
#             "expected_return": "reset",
#             "counters": {"hits": 1},
#             "log_query_param": [{"query_field_key":"server_fqdn","query_value":"open.node.com"}],
#             "traffic": {
#                 "protocol": "http",
#                 "type": "curl",
#                 "command": "curl --connect-timeout 5 -m 5 -kv http://open.node.com:180"
#             },
#             "token": ""
#         }
#         # 测试用例实例化
#         create = CreatePolicy(test_data, parameter)
#         result = create.create_policy()
        
#         return result
#     except Exception as e:
#         exception_result = str(e)
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
#         return "Error: " + str(e)
#     finally:
#         # 清理环境并删除配置
#         if isinstance(create, CreatePolicy):
#             create.clean_up()
#         # 统计脚本用时
#         script_end_time = time.time()
#         duration = script_end_time - script_start_time
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
#         # 生成csv报告
#         update = ReportUpdate()
#         update.write_result(parameter, result, exception_result)
            
# if __name__ == '__main__':
#     # ui
#     # parameter = {
#     #     "username": "hebingning",
#     #     "password": "hbn66AAA",
#     #     "test_pc_ip": "192.168.64.65",
#     #     "test_subcriber_id": "test6776",
#     #     "api_server": "http://192.168.44.72",
#     #     "debug_flag": "local",
#     #     "script_type": "ui",
#     #     "env": "tsgx",
#     #     "vsys_id": 1,
#     #     "is_log": 1,
#     #     "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
#     #     "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
#     #     "module_name": "security",
#     #     "test_case_name": "deny_srcip_fqdn_drop_rst_icmp"
#     # }
#     # run(parameter)
#     # api
#     from support.ui_utils.element_position.map_element_position_library import replace_paras
#     from support.ui_utils.workpath import workdir

#     parameter = {
#         "username": "hebingning",
#         "password": "hbn66AAA",
#         "test_pc_ip": "192.168.64.93",
#         "test_subcriber_id": "test6491",
#         "api_server": "http://192.168.44.72",
#         "debug_flag": "local",
#         "script_type": "api",  # api  ui  空字符串
#         "is_log": 1,
#         "env": "tsgx",
#         "vsys_id": 1,
#         "root_path": workdir,
#         "path": workdir + "/tests/api",
#         "module_name": "security",
#         "test_case_name": os.path.basename(__file__)[:-3]
#     }
#     parameter = replace_paras(parameter)
#     run(parameter)

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
        script_start_time = time.time()
        
        policy_configuration = {
            "name": os.path.splitext(os.path.basename(__file__))[0],
            "type": "security",
            "action": "allow",
            "and_conditions": [
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_APP_ID",
                            "type": "application",
                            "sub_type": "application",
                            "application": {
                                "app_name": "udp_payload_c2s_first_data_len",
                                "app_longname": "udp_payload_c2s_first_data_len",
                                "app_properties": {
                                    "tcp_timeout": 0,
                                    "udp_timeout": 0,
                                    "action_parameter": {
                                        "sub_action": "drop",
                                        "after_n_packets": 0,
                                        "send_tcp_reset": 1,
                                        "send_icmp_unreachable": 1
                                    },
                                    "continue_scanning": 0,
                                    "category": "business-systems",
                                    "subcategory": "auth-service",
                                    "content": "voice-call",
                                    "risk": 1,
                                    "characteristics": "evasive"
                                },
                                "app_surrogates": [
                                    {
                                        "group_by": "session",
                                        "ordered_match": "no",
                                        "signature_sequence": [
                                            {
                                                "exclude": 0,
                                                "signature":{
                                                    "name": "udp_payload_c2s_first_data_len",
                                                    "is_enabled": True,
                                                    "and_conditions": [
                                                        {
                                                            "negate_option": False,
                                                            "or_conditions": [
                                                                {
                                                                    "attribute_name": "ATTR_UDP_PAYLOAD_C2S_FIRST_DATA_LEN",
                                                                    "type": "interval",
                                                                    "name": "sec_interval",
                                                                    "items": [
                                                                        {
                                                                            "op": "add",
                                                                            "interval": "1-31",
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]

                            },

                        }
                    ]
                }
            ],
            "is_enabled": 1,
            "log_option": "metadata",
        }
        
        traffic_generation = {
            "tool": "dns", 
            "command": "nslookup www.baidu.com"
        }
        
        verification_result = {
            "excepted_traffic_result": "baidu",
            "expected_metric": {"hits": 2},
            "expected_log": [
                {"query_field_key":"server_ip", "query_value": "8.8.8.8"},
                {"query_field_key":"decoded_as", "query_value": "DNS"}
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
            if rules_tuple:
                ui_client.delete_rules(parameter, policy_configuration)
        elif parameter["initiation_method"] == "api":
            if rules_tuple:
                api_client.delete_rules(rules_tuple)
            if objects_tuple:
                api_client.delete_objects(objects_tuple)
        
        # 统计脚本用时
        script_end_time = time.time()
        duration = script_end_time - script_start_time
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
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "initiation_method": "api",
        "env": "tsgx",
        "vsys": 1,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)