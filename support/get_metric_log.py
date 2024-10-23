#!/usr/bin/python3
# coding=utf-8
import requests
import json
from datetime import datetime

class GetMetricLog:
    def __init__(self, parameter, policy_configuration, traffic_generation, configuration_manager):
        self.parameter = parameter
        self.policy_configuration = policy_configuration
        self.rule_type = self.policy_configuration["type"]
        if "rule_number" in policy_configuration:
            self.rule_number = policy_configuration["rule_number"]
        else:
            self.rule_number = 1
        self.traffic_generation = traffic_generation
        self.configuration_manager = configuration_manager
        for _, value in self.configuration_manager["rule_uuid_list"].items():
            self.rule_id = value[0]
    
    def get_log(self, token, start_time, end_time):
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            log_condition = {
                "page_no": 1,
                "page_size": 20,
                "source": "security_event",
                "columns": None,
                "start_time": "",
                "end_time": "",
                "filter": "",
                "vsys_id": 1
            }
            log_condition_dict = json.loads(json.dumps(log_condition))
            attribute_name_list = self.statistic_attr_name()
            for i in range(self.rule_number):
                if self.rule_type == 'security':
                    schema_type = 'security_event'
                elif self.rule_type == 'pxy_intercept':
                    schema_type = 'session_record'
                elif self.rule_type == 'pxy_manipulation':
                    schema_type = 'proxy_event'
                elif self.rule_type == 'monitor':
                    schema_type = 'monitor_event'
                elif self.rule_type == 'dos_protection':
                    schema_type = 'dos_event'
                fields = self.get_log_schema(token, schema_type, self.parameter["api_server"], self.parameter["vsys_id"])
                log_condition_dict['columns'] = fields
                
                if self.rule_type == 'security':
                    log_source = 'security_event'
                    identifier_name = 'security-event-list'
                    log_query_rule_type = 'security_rule_list'
                elif self.rule_type == 'pxy_intercept':
                    log_source = 'session_record'
                    identifier_name = 'session-record-list'
                    log_query_rule_type = 'proxy_rule_list'
                elif self.rule_type == 'pxy_manipulation':
                    log_source = 'proxy_event'
                    identifier_name = 'proxy-event-manipulation-list'
                    log_query_rule_type = 'proxy_rule_list'
                elif self.rule_type == 'monitor':
                    log_source = 'monitor_event'
                    identifier_name = 'monitor-event-list'
                    log_query_rule_type = 'monitor_rule_list'
                elif self.rule_type == 'statistics':
                    log_source = 'session_record'
                    identifier_name = 'session-record-list'
                    log_query_rule_type = 'statistics_rule_list'
                elif self.rule_type == "dos_protection":
                    log_source = "dos_event"
                    identifier_name = "dos-event-list"
                log_condition_dict['source'] = log_source
                log_condition_dict['identifier_name'] = identifier_name
                
                log_condition_dict['start_time'] = start_time
                log_condition_dict['end_time'] = end_time
                log_condition_dict['vsys_id'] = self.parameter["vsys_id"]
                log_condition_dict['execution_mode'] = 'oneshot'
                
                # 当attribute_name_list大于1？？
                if len(attribute_name_list) == 1:
                    if self.rule_type == "dos_protection":
                        attack_type = "Custom Network Attack"
                        log_condition_dict['filter'] = f"destination_ip='{self.traffic_generation['servers_start_ip']}'AND attack_type='{attack_type}'"
                    else:
                        if self.policy_configuration["and_conditions"][0]["or_conditions"][0]["attribute_name"] == "ATTR_SUBSCRIBER_ID":
                            log_filter = f"subscriber_id='{self.parameter["test_subcriber_id"]}' AND has({log_query_rule_type}, {self.rule_id})"
                            log_condition_dict['filter'] = log_filter
                        else:
                            log_filter = f"client_ip={self.parameter["test_pc_ip"]} AND has({log_query_rule_type}, {self.rule_id})"
                            log_condition_dict['filter'] = log_filter
                            log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={self.parameter["test_pc_ip"]}", f"client_ip='{self.parameter["test_pc_ip"]}'")
                
                url = self.parameter["api_server"] + "/v1/log/query"
                response = requests.post(url, headers=headers, json=log_condition_dict, verify=False)
                assert response.status_code == 200
                log_list = json.loads(response.text)
                log_list = log_list['data']['result']
                return log_list, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log exception error: ", e, flush=True)
            return "", "Get log exception error: " + str(e)

    def get_log_schema(self, token, schema_type, api_host, vsys_id):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/log/schema/" + schema_type + "?vsys_id=" + str(vsys_id)
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200
        log_schema = json.loads(response.text)
        log_schema = log_schema['data']['fields']
        log_schema = ",".join([field['name'] for field in log_schema])
        return log_schema

    def get_metric(self, token, start_time, end_time):
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = self.parameter["api_server"] + "/v1/log/query"
            for i in range(self.rule_number):
                if self.rule_type == 'security':
                    dataset_identifier_name = "security-policy-rule-statistics"
                elif self.rule_type == 'pxy_intercept' or self.rule_type == 'pxy_manipulation':
                    dataset_identifier_name = "proxy-policy-rule-statistics"
                elif self.rule_type == 'monitor':
                    dataset_identifier_name = "monitor-policy-rule-statistics"
                elif self.rule_type == 'dos_protection':
                    dataset_identifier_name = "dos-protection-rule-statistics"
                hit_query_condition = {
                    "identifier_name": dataset_identifier_name, 
                    "rule_id": "", 
                    "start_time": "",
                    "end_time": "", 
                    "vsys_id": 1, 
                    "execution_mode": "oneshot", 
                    "output_mode": "json",
                    "interval": 1
                }
                hit_query_condition['rule_id'] = self.rule_id
                hit_query_condition['start_time'] = start_time
                hit_query_condition['end_time'] = end_time
                hit_query_condition['vsys_id'] = self.parameter["vsys_id"]
                response = requests.post(url, headers=headers, json=hit_query_condition, verify=False)
                assert response.status_code == 200
                response = json.loads(response.text)
                return response, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get metric exception error: ", e, flush=True)
            return "", "Get metric exception error: " + str(e)

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

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")