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
            "name": parameter["test_case_name"],
            "type": "proxy_manipulation",
            "action": "deny",
            "and_conditions": [
            {
                "negate_option": False,
                "or_conditions": [
                {
                    "attribute_name": "ATTR_SOURCE_IP",
                    "name": "manipulation_source_ip",
                    "type": "ip",
                    "sub_type": "ip",
                    "statistics_option": "none",
                    "member_type": "item",
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
                    "attribute_name": "ATTR_APP_ID",
                    "type": "application",
                    "items": ["http"]
                }]
            },
            {
                "negate_option": False,
                "or_conditions": [
                {
                    "attribute_name": "ATTR_HTTP_REQ_HDR",
                    "name": "manipulation_http_reqheader",
                    "type": "keyword",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                    {
                        "op": "add",
                        "expr_type": "and",
                        "expression": "Wget&Windows&Win64&AppleWebKit&KHTML&Gecko&Chrome"
                    }]
                }]
            }],
            "is_enabled": 1,
            "log_option": "metadata",
            "action_parameter":
            {
                "sub_action": "block",
                "manipulation_block": "warning_page",
                "code": 403,
                "message": "test_response_code"
            }
        }

        traffic_generation = {
            "tool": "ssl",  # or trex/http
            "command": "curl --connect-timeout 30 -m 60 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"test_request_body\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" https://open.node.com:1443/go"
        }

        verification_result = {
            "excepted_traffic_result": "test_response_code",
            "expected_metric": {"hits": 1},
            "expected_log": [
                {"query_field_key": "http_host", "query_value": "open.node.com"},
                {"query_field_key": "http_user_agent", "query_value": "Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
            ]
        }

        # 创建
        objects_tuple, profiles_tuple,  libraries_tuple, rules_tuple = None, None, None, None
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

        # 类实例化
        generator = TrafficGenerator()

        # 获取当前时间
        utc_tz = pytz.timezone('UTC')
        current_utc_time = datetime.now(utc_tz)
        traffic_start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

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
            log_result = api_client.query_rule_log(traffic_generation, verification_result, tmp_rules_tuple, traffic_start_time, traffic_result)
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
            metric_result = api_client.query_rule_metric(verification_result, tmp_rules_tuple, traffic_start_time, traffic_result)
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
