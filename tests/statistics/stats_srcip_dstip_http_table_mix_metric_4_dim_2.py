# -*- coding: UTF-8 -*-
import time
import os
import sys

from support.ui_utils.element_position.map_element_position_library import replace_paras

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import traceback
from datetime import datetime
from support.instance_utils.case_instance_generator import CaseInstanceGenerator
from support.report_update import ReportUpdate

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
            "policy_type": "statistics",
            "rule_name": parameter["test_case_name"],
            "rule_action": "statistics",
            "rule_type": "create",
            "debug_flag": "local",
            "test_subcriber_id": "test6489",
            "script_type": "ui",
            "condition": {
                "source_ip": [
                    {
                        "name": parameter["test_case_name"].replace("_dstip", "", 1),
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "10.64.38.240",
                            },
                        ]
                    }
                ],
                "source_port": [],
                "destination_ip": [
                    {
                        "name": parameter["test_case_name"].replace("_srcip", "", 1),
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "2.1.1.3",
                            },
                        ]
                    }
                ],
                "destination_port": [],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [],
                "external_port": [],
                "source_geography": [],
                "destination_geography": [],
                "sub_id": [],
                "device": [],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "http",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                ],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [
                ],
                "packet_capture": []
            },
            "action_parameter": {
                "statistics_template": [{
                    "name": parameter["test_case_name"].replace("_srcip_dstip", "", 1),
                    "profile_type": "statistics_template",
                    "charts": [
                        {
                            "chart_name": "UNIQUECOUNT(Client IP Object List,
                            "visualization_type": "Table",
                            "metrics": [
                                "sent_bytes+received_bytes:SUM:SUM Bytes Sent Bytes Received",
                                "sent_pkts+received_pkts:SUM:SUM Packets Sent Packets Received",
                                "new_c2s_flows+new_s2c_flows:SUM:SUM New Double Flows",
                                "new_in_sessions+new_out_sessions:SUM:SUM New Sessions"
                            ],
                            "dimensions": [
                                "server_fqdn",
                                "app"
                            ],
                            "order_by": "SUM New Sessions",
                            "row_limit": "20",
                            "min_in_size": "0",
                            "min_out_size": "0"
                        }
                    ]
                }]
            },
            "expected_return": "reset",
            "counters": {"hits": 1},
            "log_query_param": [{"query_field_key": "server_fqdn", "query_value": "www.yumi.com"}],
            "traffic": {
                "protocol": "",
                "type": "trex",
                "clients_start_ip": "10.64.38.240",
                "clients_end_ip": "10.64.38.240",
                "servers_start_ip": "2.1.1.31",
                "servers_end_ip": "2.1.1.31",
                "m": 1,
                "d": 1,
                "yaml_name": "test",
                "pcap_name": "http_87pkts"
            },
            # "traffic": {
            #     "type": "trex",
            #     "clients_start_ip": "192.168.64.86",
            #     "clients_end_ip": "192.168.64.86",
            #     "servers_start_ip": "2.1.1.1",
            #     "servers_end_ip": "2.1.1.2",
            #     "m": 1,
            #     "d": 1,
            #     "yaml_name": "test",
            #     "pcap_name": "test_https"
            # },
            # "traffic": {
            #     "type": "nslookup",
            #     "command": "nslookup www.facebook.com"
            # },
            # "traffic": {
            #     "type": "wget",
            #     "command": "wget -q -O- http://open.node.com:180"
            # },
            "token": ""
        }
        # 测试用例实例化
        case_instance_generator = CaseInstanceGenerator(test_data, parameter)
        result = case_instance_generator.run()

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Finish test case: " + parameter["test_case_name"], flush=True)
        return result

    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,
              flush=True)
        traceback.print_exc()
        return "Error: " + str(e)
    finally:
        # 清理环境
        if isinstance(case_instance_generator, CaseInstanceGenerator):
            case_instance_generator.delete_data()
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)


if __name__ == '__main__':
    """56个Fields，其中3个不支持Unique_count,其他的按类别8个一组创建Test
    client_ip_object_list
    server_ip_object_list
    server_fqdn
    server_domain
    fqdn_category_list
    http_host
    app
    app_category
     client_ip	
     client_country	
     server_ip	
     server_country
     client_asn
     server_asn
     client_port
     server_port
    device_group	
    sled_ip 
    decoded_as
    c2s_ttl
    s2c_ttl
    c2s_link_id
    s2c_link_id
    session_id	
     direction  	 
     in_latency_ms	
     out_latency_ms	
     tcp_handshake_latency_ms
     subscriber_id
     duration_ms
     syn_pkts
     tcp_rtt_ms
    sent_bytes	
    received_bytes		
    sent_pkts	
    received_pkts
    in_bytes	 
    out_bytes	 
    in_pkts	 
    out_pkts 
     new_c2s_flows	 
     new_s2c_flows	 
     new_in_sessions	 
     new_out_sessions
     closed_in_sessions
     closed_out_sessions
     c2s_ip_fragments 
     s2c_ip_fragments
    ssl_ja3_hash
    ssl_sni	
    ssl_handshake_latency_ms
    dtls_handshake_latency_ms
    flags
    in_pkt_length_distribution	 	 
    out_pkt_length_distribution	 	 
    pkt_length_distribution	
    """
    parameter = {
        "username": "AutomationTestAccount",
        "password": "1qaz@WSX",
        "test_pc_ip": "192.168.64.38",
        "api_server": "http://192.168.44.72",
        "is_log": 0,
        "env": "tsgx",
        "vsys_id": 5,  # 5
        "root_path": "D:/tsgcode/tsg_test",
        "path": "tsgcode/tsg_test/testcase/ui",
        "module_name": "statistics",
        "test_case_name": os.path.basename(__file__)[:-3],
        "debug_flag": "local",
        "test_subcriber_id": "test6438",
        "script_type": "ui",
        "policy_type": "statistics"
   }
    parameter = replace_paras(parameter)
    run(parameter)

    """
    # 在测试文件的当前路径执行如下命令执行测试用例:
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）:
    allure serve allure
    """