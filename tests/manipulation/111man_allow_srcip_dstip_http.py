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
import traceback


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)

        # 参数初始化
        result, exception_result = "", ""
        test_summary = {}

        # 脚本启动时间
        script_start_time = time.time()

        policy_configuration = {
            "name": parameter["test_case_name"],
            "type": "proxy_manipulation",
            "action": "allow",
            "and_conditions": [
            {
                "negate_option": False,
                "or_conditions": [
                {
                    "attribute_name": "ATTR_SOURCE_IP",
                    "type": "ip",
                    "sub_type": "ip",
                    "statistics_option": "none",
                    "member_type": "item",
                    "name": "manipulation_source_ip",
                    "items": [
                    {
                        "op": "add",
                        "ip": parameter["test_pc_ip"],
                        "interval": "0-65535"
                    }]
                }]
            },
            {
                "negate_option": False,
                "or_conditions": [
                {
                    "attribute_name": "ATTR_DESTINATION_IP",
                    "type": "ip",
                    "sub_type": "ip",
                    "statistics_option": "none",
                    "member_type": "item",
                    "name": "manipulation_destination_ip",
                    "items": [
                    {
                        "op": "add",
                        "ip": "192.168.40.206",
                        "interval": "0-65535"
                    }]
                }]
            },
            {
                "negate_option": False,
                "or_conditions": [
                {
                    "attribute_name": "ATTR_APP_ID",
                    "type": "application",
                    "items": ["http"]
                }]
            }],
            "is_enabled": 1,
            "log_option": "metadata",
            "action_parameter": {
                "sub_action": "block",
                "manipulation_block": "warning_page",
                "code": 403,
                "html_profile": {
                    "name": "test",
                    "format": "html",
                    "file_path": "Response-Pages_1.html"
                }
        }
        }

        traffic_generation = {
            "tool": "ssl", # or trex/http
            "command": "curl --connect-timeout 30 -m 60 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"test_request_body\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" https://open.node.com:1443/go"
        }

        verification_result = {
            "excepted_traffic_result": "test_resbody",
            "expected_metric": {"hits": 1},
            "expected_log": [
                {"query_field_key": "http_host", "query_value": "open.node.com"},
                {"query_field_key": "decoded_as", "query_value": "HTTP"}
            ]
        }

        # 创建
        objects_tuple, profiles_tuple,  libraries_tuple, rules_tuple = None, None, None, None
        if parameter["initiation_method"] == "ui":
            ui_client = UIClient(parameter)
            """
            ui_error = ui_client.create_objects(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
            objects_tuple, ui_error = ui_client.get_objects_uuid(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
            """
            ui_error = ui_client.create_profiles(policy_configuration)
            if len(ui_error )> 0:
                return ui_error
            profiles_tuple, ui_error = ui_client.get_profiles_uuid(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
            """
            ui_error = ui_client.create_rules(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
            rules_tuple, ui_error = ui_client.get_rules_uuid(policy_configuration)
            if len(ui_error) > 0:
                return ui_error
            """
        elif parameter["initiation_method"] == "api":
            api_client = APIClient(parameter)
            # {uuid, type}, i.e., {"12341-232-a21", "ip"}
            objects_tuple, api_error = api_client.create_objects(policy_configuration)
            if len(api_error) > 0:
                return api_error
            profiles_tuple, api_error = api_client.create_profiles(policy_configuration)
            if len(api_error) > 0:
                return api_error
            libraries_tuple, api_error = api_client.create_libraries(policy_configuration)
            if len(api_error) > 0:
                return api_error
            rules_tuple, api_error = api_client.create_rules(policy_configuration, objects_tuple, libraries_tuple, profiles_tuple)
            if len(api_error) > 0:
                return api_error

        # 等待下发配置生效
        time.sleep(3)
        return 0
        """
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

        # 提取Manipulation_rules用于查询
        tmp_rules_list = []
        for i in range(len(rules_tuple)):
            if rules_tuple[i]["type"] == "proxy_manipulation":
                tmp_rules_list.append(rules_tuple[i])
        tmp_rules_tuple = tuple(tmp_rules_list)

        # 验证tsg的日志是否符合策略执行的预期
        if parameter["initiation_method"] == "ui":
            log_result = ui_client.query_rule_log(verification_result, tmp_rules_tuple, traffic_result)
        elif parameter["initiation_method"] == "api":
            log_result = api_client.query_rule_log(traffic_generation, verification_result, tmp_rules_tuple, start_time, traffic_result)
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
            metric_result = api_client.query_rule_metric(verification_result, tmp_rules_tuple, start_time, traffic_result)
        if metric_result == True:
            test_summary["metric"] = "Pass."
        elif metric_result == False:
            test_summary["metric"] = "The failure reason: the returned metric does not match the expected result."
        elif metric_result == None:
            test_summary["metric"] = "The failure reason: the returned metric is empty."
        elif len(metric_result) > 0:
            test_summary["metric"] = metric_result

        return test_summary
        """
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When running test case, the exception error: ", str(e), flush=True)
        raise
        return "When running test case, the exception error: " + str(e)
    finally:
        # 删除
        if parameter["initiation_method"] == "ui":
            if rules_tuple:
                ui_client.delete_rules(rules_tuple)
            if objects_tuple:
                ui_client.delete_objects(objects_tuple)
            if profiles_tuple:
                ui_client.delete_profiles(profiles_tuple)
        elif parameter["initiation_method"] == "api":
            if rules_tuple:
                api_client.delete_rules(rules_tuple)
            if profiles_tuple:
                api_client.delete_profiles(profiles_tuple)
            if libraries_tuple:
                api_client.delete_libraries(libraries_tuple)
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
    from support.ui_utils.element_position.map_element_position_library import replace_paras

    parameter = {
        "username": "zcw3",
        "password": "qa111111",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "initiation_method": "api",  # api  ui  空字符串
        "env": "tsgx",
        "vsys": 1,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "manipulation",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    run(parameter)


    sc_action = {"action_parameter": {
        "targeted_traffic": "raw",
        "sff_profiles": [
            {
                "name": "autotest",
                "type": 2,
                "load_balance_method": "hash-int-ip",
                "load_balance_localization": "nearby",
                "failure_action": "bypass",
                "service_func_profiles": [
                    {
                        "name": "autotest",
                        "admin_status": 1,
                        "device_group": {
                            "value": "center-xxg-9140",
                            "tag": "data_center"
                        },
                        "connectivity": {
                            "method": "layer2_switch",
                            "int_vlan_tag": "4090",
                            "ext_vlan_tag": "4091",
                            "dest_ip": "110"
                        },
                        "health_check": {
                            "method": "none",
                            "interval_ms": 200,
                            "retires": 5
                        }
                    }
                ]
            }
        ]
    }}
    Monitor_action = {"action_parameter": {
        "traffic_mirroring": {
            "enable": 1,
            "vlanID": 1,
            "mirroring_profile": {"name": "autotest", "vlan_array": ["65", "66"]}
        },
        "packet_capture": {
            "enable": 0
        }
    }
    }
    html_profile_action = {
        "action_parameter": {
            "sub_action": "block",
            "manipulation_block": "warning_page",
            "code": 403,
            "html_profile": {
                "name": "test",
                "format": "html",
                "file_path": "Response-Pages_1.html"
            }
        }
    }
    replace_rule_action = {
        "action_parameter": {
            "sub_action": "replace_file",
            "replacement_file": {
                "name": "test",
                "file_path": "hijack_png_1.png",
                "content_name": "hijack.png",
                "content_type": "application / vnd.android.package - archive"
            }
        }
    }
    insert_css_rule_action = {
        "action_parameter": {
            "sub_action": "inject_css",
            "css_file": {
                "name": "automanipulation_insert_profile",
                "file_path": "insert_css_1.css"
            }
        }
    }
    insert_js_rule_action = {
        "action_parameter": {
            "sub_action": "inject_javascript",
            "injection_section": "html_body",
            "js_file": {
                "name": "manipulation_insert_profile",
                "file_path": "insert_js_1.js"
            }
        }
    }
    lua_rule_action = {
        "action_parameter": {
            "lua_script": {
                "name": "test",
                "file_path": "run_script_replace_reqbody.lua",
                "max_exec_time": 100
            }
        }
    }
    intercept_rule_action = {
        "action_parameter": {
            "keyring_for_trusted": {
                "name": "autotestTrust",
                "public_file": "tango_ca_v3_trust_ca.cer",
                "private_file": "tango_ca_v3_trust_ca.key",
                "reissue_expiry_hour": 24,
                "keyring_type": "root",
                "public_key_algo": "rsa2048",
                "include_root": 1
            },
            "keyring_for_untrusted": {
                "name": "autotestUNTrust",
                "public_file": "tango_ca_v3_untrust_ca.cer",
                "private_file": "tango_ca_v3_untrust_ca.key",
                "reissue_expiry_hour": 24,
                "keyring_type": "root",
                "public_key_algo": "rsa1024",
                "include_root": 0
            },
            "tcp_option_profile": {"name": "autotest", "tcp_passthrough": 1, "bypass_duplicated_packet": 0,
                                   "client_side_conn_param": {"tcp_maxseg": {"enable": 1, "maxseg": 1460}, "nodelay": 0,
                                                              "ttl": 70, "keep_alive": {"enable": 1, "tcp_keepcnt": 222,
                                                                                        "tcp_keepidle": 7200,
                                                                                        "tcp_keepintvl": 75},
                                                              "user_timeout": {"enable": 1, "timeout_ms": 5000}},
                                   "server_side_conn_param": {"tcp_maxseg": {"enable": 1, "maxseg": 1460}, "nodelay": 0,
                                                              "ttl": 75, "keep_alive": {"enable": 1, "tcp_keepcnt": 200,
                                                                                        "tcp_keepidle": 7000,
                                                                                        "tcp_keepintvl": 69},
                                                              "user_timeout": {"enable": 1, "timeout_ms": 5000}}},
            "decryption_profile": {
                "name": "autotest",
                "decryption": {
                    "certificate_checks": {
                        "approach": {
                            "cn": 1, "issuer": 1, "self-signed": 1, "expiration": 1
                        },
                        "fail_action": "fail-close"
                    },
                    "dynamic_bypass": {
                        "ev_cert": 0,
                        "cert_transparency": 0,
                        "mutual_authentication": 1,
                        "protocol_errors": 1,
                        "cert_pinning": 1,
                        "trusted_root_cert_is_not_installed_on_client": 0
                    },
                    "protocol_version": {
                        "mirror_client": 1,
                        "allow_http2": 1,
                        "min": "tls12",
                        "max": "tls13"
                    }
                }
            },
            "traffic_mirroring": {
                "enable": 1,
                "vlanID": 1,
                "mirroring_profile": {
                    "name": "autotest",
                    "vlan_array": ["65", "66"]
                }
            }
        }
    }
    dns_record_action = {
        "action_parameter": {
            "sub_action": "redirect",
            "resolution": [{"qtype": "A", "answer": [
                {"atype": "A", "record_profile": {"name": "test", "type": "A", "description": "test",
                                                  "values": [{"value": "192.168.1.2"}, {"value": "192.168.1.1"}]},
                 "selected_num": 1,
                 "ttl": {"min": 300, "max": 300}}]}, {"qtype": "AAAA", "answer": [
                {"atype": "AAAA", "record_profile": {"name": "test", "type": "AAAA", "description": "test",
                                                     "values": [{"value": "11::8847"}, {"value": "11::8848"}]},
                 "selected_num": 1,
                 "ttl": {"min": 300, "max": 300}}]}],
            "packet_capture": {"enable": 0}, "send_icmp_unreachable": 0, "send_tcp_reset": 0}
    }
    shaping_action = {
        "action_parameter": {
            "fair_factor": 1,
            "priority": 5,
            "profile_chain": [{"name": "test", "type": "generic", "type_argument": "none",
                               "limits": [{"direction": "incoming", "bandwidth": 50000},
                                          {"direction": "outgoing", "bandwidth": 100000}],
                               "aqm_options": {"algorithm": "blue"}}],
            "dscp_marking": {
                "enabled": 0
            }
        }
    }