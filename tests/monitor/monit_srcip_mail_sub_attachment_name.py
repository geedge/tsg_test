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
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Begin to run test case: " + parameter["test_case_name"], flush=True)

        # 参数初始化
        result, exception_result = "", ""
        test_summary = {}

        # 脚本启动时间
        start_time = time.time()

        policy_configuration = {
            "and_conditions": [
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_SOURCE_IP",
                            "type": "ip",
                            "sub_type": "ip",
                            "name": "monitor_source_ip",
                            "items": [
                                {
                                    "op": "add",
                                    "ip": "10.64.224.7",
                                    "interval": "0-65535"
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
                            "items": ["mail"]
                        }
                    ]
                },
                {
                    "negate_option": False,
                    "or_conditions": [
                        {
                            "attribute_name": "ATTR_MAIL_ATT_NAME",
                            "type": "keyword",
                            "member_type": "item",
                            "name": "monitor_mail_att_name",
                            "items": [
                                {
                                    "op": "add",
                                    "expr_type": "and",
                                    "expression": "test"
                                }
                            ]
                        }
                    ]
                }
            ],
            "action_parameter": {
                "packet_capture": {
                    "enable": 0
                },
                "traffic_mirroring": {
                    "enable": 0
                }
            },
            "name": os.path.splitext(os.path.basename(__file__))[0],
            "log_option": "metadata",
            "action": "monitor",
            "type": "monitor",
            "is_enabled": 1
        }

        traffic_generation = {
            "tool": "trex",  # or trex/http
            "clients_start_ip": "10.64.224.3",
            "clients_end_ip": "10.64.224.3",
            "servers_start_ip": "2.1.1.3",
            "servers_end_ip": "2.1.1.3",
            "m": 1,
            "d": 1,
            "yaml_name": "test",
            "pcap_name": "mail_imap"
        }

        verification_result = {
            "excepted_traffic_result":  "trex",
            "expected_metric": {"hits": 1},
            "expected_log": [
                {"query_field_key": "mail_attachment_name", "query_value": "test1214.txt"},
                {"query_field_key": "decoded_as", "query_value": "MAIL"}
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
            log_result = api_client.query_rule_log(traffic_generation, verification_result, rules_tuple, start_time,
                                                   traffic_result)
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
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "When running test case, the exception error: ", str(e), flush=True)
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
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
              "Finish test case: " + parameter["test_case_name"], flush=True)

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
        "initiation_method": "api",
        "env": "tsgx",
        "vsys": 5,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "monitor",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)
