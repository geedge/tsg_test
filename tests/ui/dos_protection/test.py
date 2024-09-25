import os
import sys
import time
from datetime import datetime, timedelta
import pytz
from support.api_utils.log_in import LogIn

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import support.api_utils.get_log
import support.api_utils.policy_verify
import support.ui_utils.env

def main():
    # 已知参数
    parameter = {
        "username": "lina2024",
        "password": "lina2024",
        "test_pc_ip": "192.168.64.96",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
        "module_name": "dos_protection",
        "test_case_name": "dos_protect_srcip_http_rate_srcip_d3"
    }

    # 其他参数
    rule_num = 1
    # 获取开始时间
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.now(utc_tz) - timedelta(seconds=72000)
    start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    #获取结束时间
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.now(utc_tz)
    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    test_data = {
        'is_multi_priority': False,
        'rule_num': 1,
        'policy_type': 'dos_protection',
        'rule_name': 'dos_protect_srcip_http_rate_srcip_d3',
        'rule_action': 'protect',
        'rule_type': 'create',
        'do_log': 2,
        'condition': {
            'source_ip': [
                {
                    'name': 'dos_srcip',
                    'object_type': 'ip',
                    'select_type': False,
                    'negate': False,
                    'item': [
                        {
                            'item_operation': 'add',
                            'item_type': 'ipv4',
                            'item_value': '10.64.6.162'
                        }
                    ]
                }
            ],
            'application': [
                {
                    'name': 'http',
                    'object_type': 'application',
                    'negate': False
                }
            ]
        },
        'threshold': {
            'type': 'rate',
            'rate_threshold': {
                'group_by': 'source_ip',
                'request_per_period': 1,
                'counting_period': '1min'
            }
        },
        'mitigation': {
            'behavior': 'deny',
            'timeout': '2min'
        },
        'expected_return': '',
        'counters': {
            'hits': 'many'
        },
        "log_query_param": [
                {"query_field_key": "basic_attack_type", "query_value": "tcp_syn_flood"},
                {"query_field_key": "basic_sessions", "query_value": 2},
                {"query_field_key": "basic_session_rate", "query_value": ""},
                {"query_field_key": "basic_packets", "query_value": ""},
                {"query_field_key": "basic_packet_rate", "query_value": ""},
                {"query_field_key": "basic_bytes", "query_value": ""},
                {"query_field_key": "basic_bit_rate", "query_value": ""},
                {"query_field_key": "attack_type", "query_value": "custom_network_attack"},
                {"query_field_key": "sessions", "query_value": 2},
                {"query_field_key": "packets", "query_value": ""},
                {"query_field_key": "bytes", "query_value": ""},
                {"query_field_key": "bit_rate", "query_value": ""},
                {"query_field_key": "packet_rate", "query_value": ""},
                {"query_field_key": "session_rate", "query_value": ""},
            ],
        'traffic': {
            'protocol': '',
            'type': 'trex',
            'clients_start_ip': '10.64.6.162',
            'clients_end_ip': '10.64.6.162',
            'servers_start_ip': '2.1.1.4',
            'servers_end_ip': '2.1.1.4',
            'm': 1,
            'd': 5,
            'yaml_name': 'test',
            'pcap_name': 'http'
        },
        'token': '0c9d2f30-f1e9-4e12-9d26-26c330deefa4&27&',
        'rule_id': '142685'
    }

    log_in = LogIn()
    pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
    token = log_in.login(parameter["username"], pwd, parameter["api_server"])
    test_data["token"] = token

    api_server = parameter["api_server"]
    vsys_id = parameter["vsys_id"]
    script_type = parameter["script_type"]
    create_policies_ids = [{'dos_protection': test_data['rule_id']}]
    # 调用 GetLog 的 get_log_by_condition 函数
    log = support.api_utils.get_log.GetLog()

    output = '{"total_bytes": 435032, "total_bytes_received": 400868, "total_bytes_sent": 34164, "total_packets": 388, "total_packets_received": 300, "total_packets_sent": 88, "total_syn_pkt": 4}'  # 示例的输出
    log_result = log.get_log_by_condition(
        token,
        rule_num,
        start_time,
        end_time,
        parameter["test_pc_ip"],
        parameter["test_subcriber_id"],
        create_policies_ids,
        test_data,
        api_server,
        vsys_id,
        script_type,
        output
    )

    # 打印 log_result 结果
    print("log_result:", log_result)


if __name__ == "__main__":
    main()


# # 打印所有参数
#         print(f"token: {token}")
#         print(f"rule_num: {rule_num}")
#         print(f"start_time: {start_time}")
#         print(f"end_time: {end_time}")
#         print(f"test_pc_ip: {test_pc_ip}")
#         print(f"test_sub_id: {test_sub_id}")
#         print(f"create_policies_ids: {create_policies_ids}")
#         print(f"test_data: {test_data}")
#         print(f"api_server: {api_host}")
#         print(f"vsys_id: {vsys_id}")
#         print(f"script_type: {script_type}")
#         print(f"output: {output}")
#         headers = {'Content-Type': 'application/json', 'Authorization': token}

