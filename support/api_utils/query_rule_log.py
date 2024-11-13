# -*- coding: UTF-8 -*-
import json
import time
import pytz
import requests
import support.ui_utils.env
from datetime import datetime
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *

class QueryRuleLog:
    def __init__(self, parameter, policy_configuration, token, traffic_result):
        self.parameter = parameter
        self.policy_configuration = policy_configuration
        self.token = token
        self.traffic_result = traffic_result
    
    def query_rule_log(self, verification_result, rule_uuids_tuple, start_time):
        try:
            initiation_method = self.parameter["initiation_method"]
            if initiation_method == "ui":
                support.ui_utils.env.teardown()
                support.ui_utils.env.initiate_selenium_request()
                my_driver = support.ui_utils.env.my_driver()
                support.ui_utils.env.setup()
            else:
                my_driver = ""
            self.rule_type = self.policy_configuration["type"]
            if self.rule_type == "dos_protection":
                temp_list = [30, 60, 90]
            else:
                temp_list = [25, 55, 85]
            if self.rule_type == "security" or self.rule_type == "pxy_intercept" or self.rule_type == "pxy_manipulation" or self.rule_type == "monitor" :
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                log_result = None
                for i in range(int(90)):
                    if i in temp_list and initiation_method == "ui":
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do the browser keepalive.", flush=True)
                        element_language_menu = my_driver.find_element(By.XPATH, language_button_posXpath)
                        my_driver.execute_script("arguments[0].scrollIntoView();", element_language_menu)
                        my_driver.execute_script("arguments[0].click();", element_language_menu)
                    utc_tz = pytz.timezone('UTC')
                    current_utc_time = datetime.now(utc_tz)
                    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    time.sleep(7)
                    if log_result == None:
                        log_dict, error = self.get_log(verification_result, rule_uuids_tuple, start_time, end_time)
                        if len(error) != 0:
                            return error, my_driver
                        if self.rule_type == "dos_protection":
                            log_result = self.verify_dos_log(log_dict, verification_result)
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
                return log_result, my_driver
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When querying rule log, the exception error: ", str(e), flush=True)
            return "When querying rule log, the exception error: " + str(e)
        
    def get_log(self, verification_result, rule_uuids_tuple, start_time, end_time):
        try:
            rule_uuids_list = list(rule_uuids_tuple)
            rule_uuid = rule_uuids_list["uuid"]
            headers = {'Content-Type': 'application/json', 'Authorization': self.token}
            log_condition = {
                "page_no": 1,
                "page_size": 20,
                "source": "security_event",
                "columns": None,
                "start_time": "",
                "end_time": "",
                "filter": "",
                "vsys": 1
            }
            log_condition_dict = json.loads(json.dumps(log_condition))
            attribute_name_list = self.statistic_attr_name()
            if "rule_number" in self.policy_configuration:
                rule_number = self.policy_configuration["rule_number"]
            else:
                rule_number = 1
            for _ in range(rule_number):
                if self.rule_type == 'security':
                    schema_type = log_source = 'security_event'
                    identifier_name = 'security-event-list'
                    log_query_rule_type = 'security_rule_list'
                elif self.rule_type == 'pxy_intercept':
                    schema_type = log_source = 'session_record'
                    identifier_name = 'session-record-list'
                    log_query_rule_type = 'proxy_rule_list'
                elif self.rule_type == 'pxy_manipulation':
                    schema_type = log_source = 'proxy_event'
                    identifier_name = 'proxy-event-manipulation-list'
                    log_query_rule_type = 'proxy_rule_list'
                elif self.rule_type == 'monitor':
                    schema_type = log_source = 'monitor_event'
                    identifier_name = 'monitor-event-list'
                    log_query_rule_type = 'monitor_rule_list'
                elif self.rule_type == 'statistics':
                    schema_type = log_source = 'session_record'
                    identifier_name = 'session-record-list'
                    log_query_rule_type = 'statistics_rule_list'
                elif self.rule_type == "dos_protection":
                    schema_type = log_source = "dos_event"
                    identifier_name = "dos-event-list"
                fields = self.get_log_schema(self.token, schema_type, self.parameter["api_server"], self.parameter["vsys"])
                log_condition_dict['columns'] = fields
                log_condition_dict['source'] = log_source
                log_condition_dict['identifier_name'] = identifier_name
                
                log_condition_dict['start_time'] = start_time
                log_condition_dict['end_time'] = end_time
                log_condition_dict['vsys'] = self.parameter["vsys"]
                log_condition_dict['execution_mode'] = 'oneshot'
                
                # 当attribute_name_list大于1？？
                if len(attribute_name_list) == 1:
                    if self.rule_type == "dos_protection":
                        attack_type = "Custom Network Attack"
                        for i in range(len(verification_result)):
                            if verification_result[i]["query_field_key"] == "destination_ip":
                                destination_ip = verification_result[i]["query_value"]
                                log_condition_dict['filter'] = f"destination_ip='{destination_ip}'AND attack_type='{attack_type}'"
                                break
                    else:
                        if self.policy_configuration["and_conditions"][0]["or_conditions"][0]["attribute_name"] == "ATTR_SUBSCRIBER_ID":
                            log_filter = f"subscriber_id='{self.parameter["test_subcriber_id"]}' AND has({log_query_rule_type}, {rule_uuid})"
                            log_condition_dict['filter'] = log_filter
                        else:
                            log_filter = f"client_ip={self.parameter["test_pc_ip"]} AND has({log_query_rule_type}, {rule_uuid})"
                            log_condition_dict['filter'] = log_filter
                            log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={self.parameter["test_pc_ip"]}", f"client_ip='{self.parameter["test_pc_ip"]}'")
                
                url = self.parameter["api_server"] + "/v1/logs/query"
                response = requests.post(url, headers=headers, json=log_condition_dict, verify=False)
                assert response.status_code == 200
                log_list = json.loads(response.text)
                log_list = log_list['data']['result']
                return log_list, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log exception error: ", e, flush=True)
            return "", "Get log exception error: " + str(e)
    
    def statistic_attr_name(self):
        attribute_name_list = []
        if "and_conditions" in self.policy_configuration:
            and_conditions = self.policy_configuration["and_conditions"]
            for i in range(len(and_conditions)):
                or_conditions = and_conditions[i]["or_conditions"]
                for j in range(len(or_conditions)):
                    if or_conditions[j]["attribute_name"] != "ATTR_APP_ID":
                        attribute_name_list.append(or_conditions[j]["attribute_name"])
        return attribute_name_list
    
    def get_log_schema(self, token, schema_type, api_host, vsys):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/logs/schema/" + schema_type
        vsys = {"vsys": vsys}
        response = requests.get(url, headers=headers, params=vsys, verify=False)
        assert response.status_code == 200
        log_schema = json.loads(response.text)
        log_schema = log_schema['data']['fields']
        log_schema = ",".join([field['name'] for field in log_schema])
        return log_schema
    
    def verify_log(self, log_dict, verification_result):
        log_query = verification_result['expected_log']
        temp_log_result_list = []
        if len(log_dict) > 0 and len(log_query) > 0:
            for log in log_dict:
                for log_query_param in log_query:
                    query_field_key = log_query_param["query_field_key"]
                    query_value = log_query_param["query_value"]
                    exclude_fields = {
                        "packet_capture_file", "http_response_body", "http_request_body", "monitor_mirrored_pkts",
                        "monitor_mirrored_bytes", "client_port", "ssl_ech_flag", "ssl_esni_flag",
                        "attack_type", "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate",
                        "basic_attack_type", "basic_sessions", "basic_session_rate", "basic_packets", "basic_packet_rate", "basic_bytes", "basic_bit_rate",
                        "rule_id", "conditions"
                    }
                    if query_field_key in log and query_field_key not in exclude_fields and log[query_field_key] == query_value:
                        temp_log_result_list.append(True)
                    elif query_field_key in {"packet_capture_file", "http_response_body", "http_request_body"}:
                        if query_value == True:
                            # 查询结果中packet_capture_file长度大于0，走下一步骤
                            if len(log[query_field_key]) > 0:
                                packet_capture_url = log[query_field_key]
                                download_parameter = {"url": packet_capture_url, "exportObj": True}
                                url = self.parameter["api_server"] + "/v1/util/download_file" + "?vsys_id=" + str(self.parameter["vsys"])
                                headers = {"Content-Type": "application/json", "Authorization": self.token}
                                response = requests.get(url, headers=headers, params=download_parameter, verify=False)
                                if response.status_code == 200:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                            # 开关开启， packet_capture_file长度小于0，结果失败       
                            else:
                                temp_log_result_list.append(False)
                        # 验证开关关闭状态
                        elif query_value == False:
                            # 查询结果中packet_capture_file不为空，进下一步骤
                            if len(log[query_field_key]) > 0 :
                                temp_log_result_list.append(False)
                            else:
                                temp_log_result_list.append(True)
                    elif query_field_key in {"monitor_mirrored_pkts", "monitor_mirrored_bytes"}:
                        actual_bytes_value = self.traffic_result["total_bytes"]
                        actual_pkts_value = self.traffic_result["total_packets"]
                        mirror_bytes_value = 0
                        mirror_pkts_value = 0
                        application = self.get_application_from_configration()[0]
                        enable = self.policy_configuration["action_parameter"]["traffic_mirroring"]["enable"]
                        if enable == 1:
                            if application in {"ftp", "http", "https", "ssl"}:
                                if application in {"ftp", "http", "https", "ssl"}:
                                    protocol_filed = self.get_protocol_filed_from_configration()
                                    if len("protocol_filed") > 0:
                                        # 合并处理 "items" 和 "item" 的逻辑
                                        item_list = protocol_filed.get("items") or protocol_filed.get("item")
                                        if item_list and len(item_list) > 0:
                                            item_type = item_list[0].get("item_type")
                                            if item_type in ["san", "cn"]:
                                                mirror_bytes_value = actual_bytes_value - 4619
                                                mirror_pkts_value = actual_pkts_value - 9
                                            elif item_type == "response_header":
                                                mirror_bytes_value = actual_bytes_value - 381
                                                mirror_pkts_value = actual_pkts_value - 5
                                            elif item_type == "ftp_account":
                                                mirror_bytes_value = actual_bytes_value - 266
                                                mirror_pkts_value = actual_pkts_value - 4
                                            else:
                                                # 其他protocol field的情况，如ftp account
                                                mirror_bytes_value = actual_bytes_value - 192
                                                mirror_pkts_value = actual_pkts_value - 3
                                        else:
                                            #处理其他情况（如 ssl ech、esni、ssl sni）
                                            mirror_bytes_value = actual_bytes_value - 192
                                            mirror_pkts_value = actual_pkts_value - 3
                                    else:
                                        # 处理没有 protocol_filed 的情况
                                        mirror_bytes_value = actual_bytes_value - 192
                                        mirror_pkts_value = actual_pkts_value - 3
                                if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            elif application == "mail":
                                protocol_filed = self.get_protocol_filed_from_configration()
                                if len("protocol_filed") > 0:
                                    # 如果有 "items" 列表，并且列表不为空
                                    if "items" in protocol_filed and protocol_filed["items"]:
                                        item_type = protocol_filed["items"][0].get("item_type", "")
                                        # if item_type in ["mail_from", "mail_to"]:
                                        if item_type in ["mail_from", "to"]:
                                            mirror_bytes_value = actual_bytes_value - 19578
                                            mirror_pkts_value = actual_pkts_value - 158
                                        else:  # 如果有 "items"，但不符合特定类型时的默认行为
                                            mirror_bytes_value = actual_bytes_value - 967
                                            mirror_pkts_value = actual_pkts_value - 9
                                    # 如果有 "item" 列表，并且列表不为空
                                    elif "item" in protocol_filed and protocol_filed["item"]:
                                        item_type = protocol_filed["item"][0].get("item_type", "")
                                        if item_type in ["mail_attachment_content","mail_attachment_name"]:
                                            mirror_bytes_value = actual_bytes_value - 34554
                                            mirror_pkts_value = actual_pkts_value - 170
                                        elif item_type == "mail_subject":
                                            mirror_bytes_value = actual_bytes_value - 19578
                                            mirror_pkts_value = actual_pkts_value - 158
                                        elif item_type == "mail_content":
                                            mirror_bytes_value = actual_bytes_value - 21092
                                            mirror_pkts_value = actual_pkts_value - 159
                                        else:  # 如果有 "item"，但不符合特定类型时的默认行为
                                            mirror_bytes_value = actual_bytes_value - 967
                                            mirror_pkts_value = actual_pkts_value - 9
                                    # 如果既没有 "items" 也没有 "item"，使用默认的镜像转发处理
                                    else:
                                        mirror_bytes_value = actual_bytes_value - 967
                                        mirror_pkts_value = actual_pkts_value - 9
                                else:
                                    mirror_bytes_value = actual_bytes_value - 967
                                    mirror_pkts_value = actual_pkts_value - 9
                                if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            elif application in {"", "quic", "dns"}:
                                mirror_bytes_value = actual_bytes_value
                                mirror_pkts_value = actual_pkts_value
                                if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            else:
                                temp_log_result_list.append(False)
                            # 统一处理逻辑
                        if enable == 1 and application in {"ftp", "http", "ssl", "dns", "quic", "", "mail"}:
                            if query_field_key == "monitor_mirrored_pkts" and log[query_field_key] == mirror_pkts_value:
                                temp_log_result_list.append(True)
                                # 更新 test_data["log_query"] 中相应的 query_value
                                for log_query_param in log_query:
                                    if log_query_param["query_field_key"] == "monitor_mirrored_pkts":
                                        log_query_param["query_value"] = mirror_pkts_value  # 将值修改为5
                            elif query_field_key == "monitor_mirrored_bytes" and log[query_field_key] == mirror_bytes_value:
                                temp_log_result_list.append(True)
                                # 更新 test_data["log_query"] 中相应的 query_value
                                for log_query_param in log_query:
                                    if log_query_param["query_field_key"] == "monitor_mirrored_bytes":
                                        log_query_param["query_value"] = mirror_bytes_value  # 将值修改为5
                            else:
                                temp_log_result_list.append(False)
                    elif query_field_key in {"client_port"}:
                        start, end = map(int, query_value.split('-'))
                        if start <= log[query_field_key] <= end:
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
                        except_value = query_value     # 断言的预期值
                        if query_field_key == "proxy_passthrough_reason":
                            if except_value in {"EV Certificate", "Certificate Transparency", "Protocol Errors", "Mutual Authentication", "Certificate Not Installed", "Certificate Pinning"}:
                                if actual_value in {""}:  # 证书动态放行会产生两条日志，其中一条大概率是拦截的日志，则跳过断言
                                    continue
                                elif actual_value == except_value:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                            else:
                                if actual_value == except_value:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                        elif query_field_key == "proxy_intercept_status":  # proxy_intercept_status的值需要转换
                            if except_value == "passthrough":      # proxy_intercept_status， 0=passthrough, 1=intercept
                                except_value = 0
                            else:
                                except_value = 1
                            if except_value == 0:
                                if actual_value == 1:
                                    continue
                                elif actual_value == except_value:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                            else:
                                if actual_value == except_value:
                                    temp_log_result_list.append(True)
                                else:
                                    temp_log_result_list.append(False)
                    else:
                        temp_log_result_list.append(False)
                if self.rule_type == 'pxy_intercept' and len(temp_log_result_list) < len(log_query):
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
        action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(action_parameter)):
            or_conditions = action_parameter[i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_APP_ID":
                    application = or_conditions[j]["items"]
                    return application
    
    def get_protocol_filed_from_configration(self):
        # rule中只有一个protocol_filed
        action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(action_parameter)):
            or_conditions = action_parameter[i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_HTTP_URL":
                    return "ATTR_HTTP_URL"
                elif or_conditions[j]["attribute_name"] == "ATTR_HTTP_REQ_HDR":
                    print("to be added...")
                    
    def verify_dos_log(self, log_dict, verification_result):
        print("need to modify func logic...")