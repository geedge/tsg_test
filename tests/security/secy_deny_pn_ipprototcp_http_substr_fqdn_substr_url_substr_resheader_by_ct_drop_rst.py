# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from datetime import datetime
from support.report_update import ReportUpdate
from support.instance_utils.case_instance_generator import CaseInstanceGenerator

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        exception_result = ""
        result = {}
        
        # 脚本启动时间
        start_time = time.time()
        
        # 测试数据
        test_data = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_name": "secy_deny_pn_ipprototcp_http_substr_serverfqdn_substr_url_substr_resheader_by_ct_drop_rst",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [],
                "external_port": [],
                "source_geography": [],
                "destination_geography": [],
                "sub_id": [],
                "device": [
                    {
                        "name": "secy_pn",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "phone_number",
                                "item_value": '$' + parameter['test_phone_number'],
                            }
                        ]
                    }
                ],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "http", #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "ip_protocol":[
                    "TCP"
                ],
                "server_fqdn": [
                    {
                        "name": "secy_fqdn",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "fqdn",
                                "item_value": "open.node.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "secy_url",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                "item_value": "open.node"
                            }
                        ],
                    },
                    {
                        "name": "secy_http_sig",
                        "object_type": "http_signature",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "response_header",
                                "item_key": "Content-Type",
                                "item_value": "TEXT",
                                "value": [
                                    "text/html"
                                ]
                            }
                        ],
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                    {
                        "type": "drop",
                        "send_tcp_rst": True,
                        "drop_packet": 0,
                        "send_icmp_unreachable": False
                    }
                ],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "timed out",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key":"imsi", "query_value":parameter['test_imsi']},
            {"query_field_key":"phone_number", "query_value": parameter['test_phone_number']},
            {"query_field_key": "ip_protocol", "query_value": "tcp"}],
            "traffic": {
                "protocol": "http",
                "type": "curl",
                "command": "curl --connect-timeout 10 -m 10 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"helloSecurity\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" http://open.node.com:180/go"
            },
            "token": ""
        }
        # 测试用例实例化
        case_instance_generator = CaseInstanceGenerator(test_data, parameter)
        result = case_instance_generator.run()
        
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        case_instance_generator.delete_data()
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
            
if __name__ == '__main__':
    # ui
    # parameter = {
    #     "username": "hebingning",
    #     "password": "hbn66AAA",
    #     "test_pc_ip": "192.168.64.65",
    #     "test_subcriber_id": "test6776",
    #     "api_server": "http://192.168.44.72",
    #     "debug_flag": "local",
    #     "script_type": "ui",
    #     "env": "tsgx",
    #     "vsys_id": 1,
    #     "is_log": 1,
    #     "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
    #     "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
    #     "module_name": "security",
    #     "test_case_name": "deny_srcip_fqdn_drop_rst_icmp"
    # }
    # run(parameter)
    # api
    from support.ui_utils.element_position.map_element_position_library import replace_paras
    from support.ui_utils.workpath import workdir

    parameter = {
        "username": "hebingning",
        "password": "hbn66AAA",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "api",  # api  ui  空字符串
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/tests/api",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    run(parameter)