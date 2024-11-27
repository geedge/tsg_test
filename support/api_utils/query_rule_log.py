# -*- coding: UTF-8 -*-
import json
import time
import pytz
import requests
from datetime import datetime
from support.ui_utils.element_position.policy_element_position import *

class QueryRuleLog:
    def __init__(self, parameter, policy_configuration, token, traffic_result):
        self.parameter = parameter
        self.policy_configuration = policy_configuration
        self.token = token
        self.traffic_result = traffic_result

    def query_rule_log(self, traffic_generation, verification_result, rule_uuids_tuple, start_time):
        try:
            self.rule_type = self.policy_configuration["type"]
            if self.rule_type == "security" or self.rule_type == "proxy_intercept" or self.rule_type == "proxy_manipulation" or self.rule_type == "monitor" or self.rule_type == "statistics" or self.rule_type == "service_chaining":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                log_result = None
                for _ in range(int(90)):
                    time.sleep(10)
                    utc_tz = pytz.timezone('UTC')
                    current_utc_time = datetime.now(utc_tz)
                    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    if log_result == None:
                        log_dict, error = self.get_log(traffic_generation, rule_uuids_tuple, start_time, end_time)
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "DEBGU:start_time:{},end_time:{};log_dict:{}, error:{}".format(start_time, end_time, log_dict, error), flush=True)
                        if len(error) != 0:
                            return error
                        elif len(log_dict) == 0:
                            continue
                        if self.rule_type == "dos_protection":
                            log_result = self.verify_dos_log(log_dict, verification_result, start_time, end_time)
                        else:
                            log_result = self.verify_log(log_dict, verification_result)
                    if log_result != None:
                        break
                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is passed.', flush=True)
                elif log_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is failed.', flush=True)
                elif log_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is none.', flush=True)
                elif log_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is no_set.', flush=True)
                return log_result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When querying rule log, the exception error: ", str(e), flush=True)
            return "When querying rule log, the exception error: " + str(e)

    def get_log(self, traffic_generation, rule_uuids_tuple, start_time, end_time):
        try:
            self.traffic_generation = traffic_generation
            rule_uuids_list = list(rule_uuids_tuple)
            rule_uuid = rule_uuids_list[0]["uuid"]
            headers = {'Content-Type': 'application/json', 'Authorization': self.token}
            dsl_dict = {"dsl": "", "vsys": 1}
            log_condition = {
                "name": "log-query",
                "limit": 20,
                "data_source": "",
                "fields": "",
                "intervals": []
            }
            log_condition_dict = json.loads(json.dumps(log_condition))
            if "rule_number" in self.policy_configuration:
                rule_number = self.policy_configuration["rule_number"]
            else:
                rule_number = 1
            for _ in range(rule_number):
                if self.rule_type == 'security':
                    schema_type = log_source = 'security_event'
                    log_query_rule_type = 'security_rule_uuid_list'
                elif self.rule_type == 'proxy_intercept':
                    schema_type = log_source = 'session_record'
                    log_query_rule_type = 'proxy_rule_uuid_list'
                elif self.rule_type == 'proxy_manipulation':
                    schema_type = log_source = 'proxy_event'
                    log_query_rule_type = 'proxy_rule_uuid_list'
                elif self.rule_type == 'monitor':
                    schema_type = log_source = 'monitor_event'
                    log_query_rule_type = 'monitor_rule_uuid_list'
                elif self.rule_type == 'statistics':
                    schema_type = log_source = 'session_record'
                    log_query_rule_type = 'statistics_rule_uuid_list'
                elif self.rule_type == "dos_protection":
                    schema_type = log_source = "dos_event"
                elif self.rule_type == "service_chaining":
                    schema_type = log_source = 'session_record'
                    log_query_rule_type = 'sc_rule_uuid_list'
                fields = self.get_log_schema(self.token, schema_type, self.parameter["api_server"], self.parameter["vsys"])
                log_condition_dict['fields'] = fields
                log_condition_dict['data_source'] = log_source
                log_condition_dict["intervals"].append(start_time + '/' + end_time)
                log_condition_dict['vsys'] = self.parameter["vsys"]
                if self.is_attribute_name_exsit("ATTR_SUBSCRIBER_ID") == True:
                    log_filter = f"vsys_id in ({int(self.parameter['vsys'])}) AND subscriber_id='{self.parameter['test_subcriber_id']}' AND has({log_query_rule_type}, '{rule_uuid}')"
                    log_condition_dict['filter'] = log_filter
                else:
                    if self.traffic_generation["tool"] == "trex":
                        if self.rule_type == "dos_protection":
                            attack_type = "Custom Network Attack"
                            log_condition_dict['filter'] = f"destination_ip='{traffic_generation['servers_start_ip']}'AND attack_type='{attack_type}'"
                        else:
                            log_filter = f"vsys_id in ({int(self.parameter['vsys'])}) AND client_ip={traffic_generation['clients_start_ip']} AND has({log_query_rule_type}, '{rule_uuid}')"
                            log_condition_dict['filter'] = log_filter
                            log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={traffic_generation['clients_start_ip']}",f"client_ip='{traffic_generation['clients_start_ip']}'")
                    else:
                        # log_filter = f"client_ip={self.parameter['test_pc_ip']} AND has({log_query_rule_type}, '{rule_uuid}')"
                        log_filter = f"vsys_id in ({int(self.parameter['vsys'])}) AND client_ip={self.parameter['test_pc_ip']} AND has({log_query_rule_type}, '{rule_uuid}')"
                        log_condition_dict['filter'] = log_filter
                        log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={self.parameter['test_pc_ip']}", f"client_ip='{self.parameter['test_pc_ip']}'")
                dsl_dict["dsl"] = log_condition_dict
                dsl_dict['vsys'] = int(self.parameter["vsys"])
                url = self.parameter["api_server"] + "/v1/logs/query"
                response = requests.post(url, headers=headers, json=dsl_dict, verify=False)
                job_dict = json.loads(response.text)
                job_id = job_dict['data']['job']['job_id']
                """
                {"execution_mode":"oneshot","query_jobs":[{"id":"e9df1ca8-e270-427d-9baf-3c0e8fb13813","is_saved_query":0,"with_result":false}],"vsys":5}
                {
                    "code": 200,
                    "msg": "Success",
                    "data": [{
                        "reason": null,
                        "start_time": "2024-11-27T02:27:21Z",
                        "is_done": true,
                        "job_id": "e9df1ca8-e270-427d-9baf-3c0e8fb13813",
                        "is_canceled": false,
                        "done_progress": 1,
                        "end_time": "2024-11-27T02:27:21Z",
                        "links": {
                            "status": "/v1/query/job/e9df1ca8-e270-427d-9baf-3c0e8fb13813",
                            "count": "/v1/query/job/e9df1ca8-e270-427d-9baf-3c0e8fb13813/count",
                            "list": "/v1/query/job/e9df1ca8-e270-427d-9baf-3c0e8fb13813/list",
                            "timeline": "/v1/query/job/e9df1ca8-e270-427d-9baf-3c0e8fb13813/timeline"
                        },
                        "is_failed": false
                    }],
                    "success": true
                }
                query_job_dict = {
                    "query_jobs": [{"id": job_id, "is_saved_query":0, "with_result":False}],
                    "vsys": int(self.parameter["vsys"]), "limit": 20, "offset": 0
                }
                response = requests.post(url, headers=headers, json=query_job_dict, verify=False)
                if response.status_code == 200:
                    query_job_dict = json.loads(response.text)
                    is_done = query_job_dict['data'][0]['is_done']
                    is_failed = query_job_dict['data'][0]['is_failed']
                    reason = query_job_dict['data'][0]["reason"]
                if is_done and not is_failed:
                    query_list_dict = {
                        "query_jobs":[{"id": job_id,"query_option":"list"}],
                        "vsys":int(self.parameter["vsys"]),"limit":20,"offset":0
                    }
                    response = requests.post(url, headers=headers, json=query_list_dict, verify=False)
                    assert response.status_code == 200
                    log_list = json.loads(response.text)
                    log_list = log_list['data']['list']
                    return log_list, ""
                elif is_done and is_failed:
                    return "", reason
                else:
                    return [], ""                
                """
                query_list_dict = {
                    "query_jobs":[{"id": job_id,"query_option":"list"}],
                    "vsys":int(self.parameter["vsys"]),"limit":20,"offset":0
                }
                time.sleep(2)
                response = requests.post(url, headers=headers, json=query_list_dict, verify=False)
                assert response.status_code == 200
                log_list = json.loads(response.text)
                log_list = log_list['data']['list']
                return log_list, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When getting log, the exception error: ", e, flush=True)
            return "", "When getting log, the exception error: " + str(e)

    def is_attribute_name_exsit(self, attribute_name):
        if "and_conditions" in self.policy_configuration:
            and_conditions = self.policy_configuration["and_conditions"]
            for i in range(len(and_conditions)):
                or_conditions = and_conditions[i]["or_conditions"]
                for j in range(len(or_conditions)):
                    if or_conditions[j]["attribute_name"] == attribute_name:
                        return True
        return False

    def get_log_schema(self, token, schema_type, api_host, vsys):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/logs/schema/" + schema_type
        vsys = {"vsys": vsys}
        response = requests.get(url, headers=headers, params=vsys, verify=False)
        assert response.status_code == 200
        log_schema = json.loads(response.text)
        log_schema = log_schema['data']['fields']
        log_schema = [field['name'] for field in log_schema]
        return log_schema

    def verify_log(self, log_dict, verification_result):
        log_query = verification_result['expected_log']
        temp_log_result_list = []
        if len(log_dict) > 0 and len(log_query) > 0:
            for log in log_dict:
                for log_query_param in log_query:
                    query_field_key = log_query_param["query_field_key"]
                    query_value = log_query_param["query_value"]
                    exclude_fields = [
                        "packet_capture_file", "http_response_body", "http_request_body", "monitor_mirrored_pkts",
                        "monitor_mirrored_bytes", "client_port", "ssl_ech_flag", "ssl_esni_flag",
                        "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate", "rule_uuid", "conditions"
                    ]
                    dos_verification_fields = [
                        "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate", "rule_uuid", "source_ip", "destination_ip"
                    ]
                    if query_field_key in log and query_field_key not in (exclude_fields, dos_verification_fields) and log[query_field_key] == query_value:
                        temp_log_result_list.append(True)
                    elif query_field_key in {"packet_capture_file", "http_response_body", "http_request_body"}:
                        # 为true时，表示支持下载；为false时，表示不支持下载
                        if query_value == True:
                            if len(log[query_field_key]) > 0:
                                packet_capture_url = log[query_field_key]
                                download_parameter = {"url": packet_capture_url, "exportObj": True}
                                url = self.parameter["api_server"] + "/v1/util/download-file" + "?vsys_id=" + str(self.parameter["vsys"])
                                headers = {"Content-Type": "application/json", "Authorization": self.token}
                                response = requests.get(url, headers=headers, params=download_parameter, verify=False)
                                if response.status_code == 200:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                            else:
                                temp_log_result_list.append(False)
                        elif query_value == False:
                            if len(log[query_field_key]) > 0 :
                                temp_log_result_list.append(False)
                            else:
                                temp_log_result_list.append(True)
                    elif query_field_key in {"monitor_mirrored_pkts", "monitor_mirrored_bytes"}:
                        actual_bytes_value = self.traffic_result['total_bytes']
                        actual_pkts_value = self.traffic_result["total_packets"]
                        mirror_bytes_value = 0
                        mirror_pkts_value = 0
                        application = self.get_application_from_configration()
                        enable = self.policy_configuration["action_parameter"]["traffic_mirroring"]["enable"]
                        if enable == 1:
                            attribute_name_list = self.get_attribute_name_from_configration()
                            # 根据不同的协议，对mirror相关参数进行赋值
                            if self.is_exist_in_list(application, ["ftp", "http", "https", "ssl"]):
                                if len(attribute_name_list) > 0:
                                    if self.is_exist_in_list(attribute_name_list, ["ATTR_SSL_CN", "ATTR_SSL_SAN"]):
                                        mirror_bytes_value = actual_bytes_value - 4619
                                        mirror_pkts_value = actual_pkts_value - 9
                                    elif self.is_exist_in_list(attribute_name_list, ["ATTR_HTTP_RES_HDR"]):
                                        mirror_bytes_value = actual_bytes_value - 381
                                        mirror_pkts_value = actual_pkts_value - 5
                                    elif self.is_exist_in_list(attribute_name_list, ["ATTR_FTP_ACCOUNT"]):
                                        mirror_bytes_value = actual_bytes_value - 266
                                        mirror_pkts_value = actual_pkts_value - 4
                                    else:
                                        mirror_bytes_value = actual_bytes_value - 192
                                        mirror_pkts_value = actual_pkts_value - 3
                                else:
                                    mirror_bytes_value = actual_bytes_value - 192
                                    mirror_pkts_value = actual_pkts_value - 3
                                # if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                if "mirroring_profile" in self.policy_configuration["action_parameter"]["traffic_mirroring"]:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            elif self.is_exist_in_list(application, ["mail"]):
                                if len(attribute_name_list) > 0:
                                    if self.is_exist_in_list(attribute_name_list, ["ATTR_MAIL_FROM", "ATTR_MAIL_TO"]):
                                        mirror_bytes_value = actual_bytes_value - 19578
                                        mirror_pkts_value = actual_pkts_value - 158
                                    elif self.is_exist_in_list(attribute_name_list, ["ATTR_MAIL_ATT_CONTENT", "ATTR_MAIL_ATT_NAME"]):
                                        mirror_bytes_value = actual_bytes_value - 34554
                                        mirror_pkts_value = actual_pkts_value - 170
                                    elif self.is_exist_in_list(attribute_name_list, ["ATTR_MAIL_SUBJECT"]):
                                        mirror_bytes_value = actual_bytes_value - 19578
                                        mirror_pkts_value = actual_pkts_value - 158
                                    elif self.is_exist_in_list(attribute_name_list, ["ATTR_MAIL_CONTENT"]):
                                        mirror_bytes_value = actual_bytes_value - 21092
                                        mirror_pkts_value = actual_pkts_value - 159
                                    else:
                                        mirror_bytes_value = actual_bytes_value - 967
                                        mirror_pkts_value = actual_pkts_value - 9
                                else:
                                    mirror_bytes_value = actual_bytes_value - 967
                                    mirror_pkts_value = actual_pkts_value - 9
                                # if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                if "mirroring_profile" in self.policy_configuration["action_parameter"]["traffic_mirroring"]:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            elif self.is_exist_in_list(application, ["", "quic", "dns"]):
                                mirror_bytes_value = actual_bytes_value
                                mirror_pkts_value = actual_pkts_value
                                if "mirroring_profile" in self.policy_configuration["action_parameter"]["traffic_mirroring"]:
                                # if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            # 讲上述mirror的值赋值给对应的verification_result的expected_log
                            if self.is_exist_in_list(application, ["ftp", "http", "ssl", "dns", "quic", "", "mail"]):
                                if query_field_key == "monitor_mirrored_pkts" and log[query_field_key] == mirror_pkts_value:
                                    temp_log_result_list.append(True)
                                    for log_query_param in log_query:
                                        if log_query_param["query_field_key"] == "monitor_mirrored_pkts":
                                            log_query_param["query_value"] = mirror_pkts_value
                                elif query_field_key == "monitor_mirrored_bytes" and log[query_field_key] == mirror_bytes_value:
                                    temp_log_result_list.append(True)
                                    for log_query_param in log_query:
                                        if log_query_param["query_field_key"] == "monitor_mirrored_bytes":
                                            log_query_param["query_value"] = mirror_bytes_value
                                else:
                                    temp_log_result_list.append(False)
                    elif query_field_key in {"client_port"}:
                        if "_" in query_value:
                            start, end = map(int, query_value.split('-'))
                            if start <= log[query_field_key] <= end:
                                temp_log_result_list.append(True)
                            else:
                                temp_log_result_list.append(False)
                        else:
                            if log[query_field_key] == query_value:
                                temp_log_result_list.append(True)
                            else:
                                temp_log_result_list.append(False)
                    elif query_field_key in {"ssl_ech_flag", "ssl_esni_flag"}:
                        if query_value == "True":
                            query_value = 1
                        elif query_value == "False":
                            query_value = 0
                        if log[query_field_key] == query_value:
                            temp_log_result_list.append(True)
                        else:
                            temp_log_result_list.append(False)
                    elif query_field_key in {"proxy_pinning_status", "proxy_intercept_status", "proxy_passthrough_reason"}:
                        actual_value = log[query_field_key]   # 日志查询到的值
                        expected_value = query_value     # 断言的预期值
                        if query_field_key == "proxy_passthrough_reason":
                            if expected_value in {"EV Certificate", "Certificate Transparency", "Protocol Errors", "Mutual Authentication", "Certificate Not Installed", "Certificate Pinning"} and actual_value in {""}:
                                # 证书动态放行会产生两条日志，其中一条大概率是拦截的日志，则跳过断言
                                continue
                            else:
                                if actual_value == expected_value:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                        elif query_field_key == "proxy_intercept_status":  # proxy_intercept_status的值需要转换
                            if expected_value == "passthrough":      # proxy_intercept_status， 0=passthrough, 1=intercept
                                expected_value = 0
                            else:
                                expected_value = 1
                            if expected_value == 0 and actual_value == 1:
                                continue
                            else:
                                if actual_value == expected_value:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                    elif query_field_key in {"sc_rsp_raw_uuid_list", "sc_rsp_decrypted_uuid_list"}:
                        query_value = self.policy_configuration["action_parameter"]["sff_profiles"]
                        if query_value == log_dict[query_field_key]:
                            temp_log_result_list.append(True)
                        else:
                            temp_log_result_list.append(False)
                    elif query_field_key in {"sent_pkts", "received_pkts", "sent_bytes", "received_bytes"}:
                        if query_field_key == "sent_pkts":
                            query_value = self.traffic_result["total_packets_sent"]
                        elif query_field_key == "received_pkts":
                            query_value = self.traffic_result["total_packets_received"]
                        elif query_field_key == "sent_bytes":
                            query_value = self.traffic_result["total_bytes_sent"]
                        elif query_field_key == "received_bytes":
                            query_value = self.traffic_result["total_bytes_received"]
                        if query_value == log_dict[query_field_key]:
                            temp_log_result_list.append(True)
                        else:
                            temp_log_result_list.append(False)

                    else:
                        temp_log_result_list.append(False)
                if self.rule_type == 'proxy_intercept' and len(temp_log_result_list) < len(log_query):
                    if True in temp_log_result_list:
                        log_result = True
                    else:
                        log_result = False
                elif False not in temp_log_result_list:
                    log_result = True
                else:
                    log_result = False
        elif len(log_dict) == 0 and len(log_query) > 0:
            log_result = None
        elif len(log_query) == 0:
            log_result = True
        return log_result

    def get_application_from_configration(self):
        and_conditions = self.policy_configuration["and_conditions"]
        # action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(and_conditions)):
            or_conditions = and_conditions[i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_APP_ID":
                    application = or_conditions[j]["items"]
                    return application

    def is_exist_in_list(self, application, actual_application_list):
        application_set = set(actual_application_list)
        for element in application:
            if element not in application_set:
                return False
        return True

    def get_attribute_name_from_configration(self):
        attribute_name_list = []
        # 只收集Protocol Filed相关的Attribute Name，所以需要根据实际情况补充exclude_list？？
        exclude_list = ["ATTR_SOURCE_IP", "ATTR_DESTINATION_IP", "ATTR_APP_ID"]
        and_conditions = self.policy_configuration["and_conditions"]
        for i in range(len(and_conditions)):
            or_conditions = and_conditions[i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] not in exclude_list:
                    attribute_name_list.append(or_conditions[j]["attribute_name"])
        return attribute_name_list
                    
    def verify_dos_log(self, log_dict, verification_result, start_time, end_time):
        self.verification_result = verification_result
        log_query = verification_result['expected_log']
        temp_log_result_list = []
        if len(log_dict) > 0 and len(log_query) > 0:
            count = -1
            for log in log_dict:
                count += 1
                for log_query_param in log_query:
                    query_field_key = log_query_param["query_field_key"]
                    # query_value = log_query_param["query_value"]
                    dos_verification_fields = [
                        "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate", "rule_uuid", "source_ip", "destination_ip"
                    ]
                    if query_field_key in dos_verification_fields:
                        temp_log_result_list = self.verify_value_from_dos_event(log, query_field_key, count, start_time, end_time)
                if len(temp_log_result_list) < len(log_query):
                    if True in temp_log_result_list:
                        log_result = True
                    else:
                        log_result = False
                elif False not in temp_log_result_list:
                    log_result = True
                else:
                    log_result = False
        elif len(log_dict) == 0 and len(log_query) > 0:
            log_result = None
        elif len(log_query) == 0:
            log_result = True
        return log_result

    def verify_value_from_dos_event(self, log, query_field_key, count, start_time, end_time):
        session_number, total_packets, total_bytes = self.get_value_from_session_record(start_time, end_time)
        if self.policy_configuration["action_parameter"]["mitigation"]["behavior"] == "deny":
            expected_session_number = session_number
        elif self.policy_configuration["action_parameter"]["mitigation"]["behavior"] == "none" and log["sessions"] < session_number:
            expected_session_number = log["sessions"]
        else:
            # log_result_list.append(False)
            # expected_session_number = -1
            return [False]
        log_result_list = []
        time_diff = log["end_time"] - log["start_time"]
        expected_packets_count = expected_session_number * total_packets
        expected_bytes_count = expected_session_number * total_bytes
        if query_field_key == "sessions":
            if expected_session_number == log[query_field_key]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log[query_field_key]  # count，第几次循环，则给log_query_param中的第几次-1的数赋值
            else:
                log_result_list.append(False)
        elif query_field_key == "packets":
            if expected_packets_count == log[query_field_key]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log[query_field_key]
            else:
                log_result_list.append(False)
        elif query_field_key == "bytes": #大于0且是个整数
            if log[query_field_key] > 0 and expected_bytes_count == log[query_field_key]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log[query_field_key]
            else:
                log_result_list.append(False)
        elif query_field_key == "bit_rate":
            bits_rate_value = (log["bytes"] * 8) / time_diff
            if bits_rate_value == log[query_field_key]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log[query_field_key]
            else:
                log_result_list.append(False)
        elif query_field_key == "session_rate":
            session_rate = expected_session_number / time_diff
            if session_rate == log[query_field_key]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log[query_field_key]
            else:
                log_result_list.append(False)
        elif query_field_key == "packet_rate":
            packet_rate = expected_packets_count / time_diff
            if packet_rate == log[query_field_key]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log[query_field_key]
            else:
                log_result_list.append(False)
        elif query_field_key in ["basic_attack_type", "basic_sessions","basic_session_rate", "basic_packets", "basic_packet_rate","basic_bytes", "basic_bit_rate"]:
            log_result_list.append(True)
        elif query_field_key == "rule_uuid":
            if len(log["rule_uuid"]) > 0:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log["rule_uuid"]
            else:
                log_result_list.append(False)
        elif query_field_key == "source_ip" :
            if self.traffic_generation["clients_start_ip"] == log ["source_ip"]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log["source_ip"]
            else:
                log_result_list.append(False)
        elif query_field_key == "destination_ip":
            if self.traffic_generation["servers_start_ip"] == log[query_field_key]:
                log_result_list.append(True)
                self.verification_result["expected_log"][count]["query_value"] = log[query_field_key]
            else:
                log_result_list.append(False)
        else:
            log_result_list.append(False)
        return log_result_list

    def get_value_from_session_record(self, start_time, end_time):
        headers = {'Content-Type': 'application/json', 'Authorization': self.token}
        log_condition = {
            "page_no": 1,
            "page_size": 20,
            "source": "session_record",
            "columns": None,
            "start_time": "",
            "end_time": "",
            "filter": "",
            "vsys": 1
        }
        schema_type = "session_record"
        log_condition_dict = json.loads(json.dumps(log_condition))
        fields = self.get_log_schema(self.token, schema_type, self.parameter["api_server"], self.parameter["vsys"])
        log_condition_dict['columns'] = fields
        log_condition_dict['start_time'] = start_time
        log_condition_dict['end_time'] = end_time
        log_condition_dict['vsys'] = self.parameter["vsys"]
        log_condition_dict['source'] = "session_record"
        log_condition_dict['identifier_name'] = "session-record-list"
        log_condition_dict['execution_mode'] = 'oneshot'
        if self.policy_configuration["action_parameter"]["mitigation"]['behavior']== "none":
            log_condition_dict['filter'] = f"server_ip='{self.traffic_generation['servers_start_ip']}'"
        elif self.policy_configuration["action_parameter"]["mitigation"]['behavior'] == "deny":
            json_str = json.dumps(self.policy_configuration)
            if self.is_attribute_name_exsit("ATTR_APP_ID") and "dns" in json_str:
                log_condition_dict['filter'] = f"server_ip='{self.traffic_generation['servers_start_ip']}'AND received_pkts in (0)"
            else:
                log_condition_dict['filter'] = f"server_ip='{self.traffic_generation['servers_start_ip']}'AND received_pkts in (0,1)"
        url = self.parameter["api_server"] + "/v1/logs/query".format(self.parameter["vsys"])
        response = requests.post(url, headers=headers, json=log_condition_dict, verify=False)
        assert response.status_code == 200
        log_list = json.loads(response.text)
        log_list = log_list['data']['list']
        log_entry= log_list[0]
        received_pkts = log_entry['received_pkts']
        sent_pkts = log_entry['sent_pkts']
        total_packets = received_pkts + sent_pkts
        received_bytes = log_entry['received_bytes']
        sent_bytes = log_entry['sent_bytes']
        total_bytes = received_bytes + sent_bytes
        session_number = len(log_list)
        return session_number, total_packets, total_bytes
