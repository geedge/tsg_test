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
            self.rule_uuid = value[0]
    
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
                fields = self.get_log_schema(token, schema_type, self.parameter["api_server"], self.parameter["vsys"])
                log_condition_dict['columns'] = fields
                log_condition_dict['source'] = log_source
                log_condition_dict['identifier_name'] = identifier_name
                
                log_condition_dict['start_time'] = start_time
                log_condition_dict['end_time'] = end_time
                log_condition_dict['vsys_id'] = self.parameter["vsys"]
                # ========24.10 begin========
                # log_condition_dict['vsys'] = self.parameter["vsys"]
                # ========24.10 end==========
                log_condition_dict['execution_mode'] = 'oneshot'
                
                # 当attribute_name_list大于1？？
                if len(attribute_name_list) == 1:
                    if self.rule_type == "dos_protection":
                        attack_type = "Custom Network Attack"
                        log_condition_dict['filter'] = f"destination_ip='{self.traffic_generation['servers_start_ip']}'AND attack_type='{attack_type}'"
                    else:
                        if self.policy_configuration["and_conditions"][0]["or_conditions"][0]["attribute_name"] == "ATTR_SUBSCRIBER_ID":
                            log_filter = f"subscriber_id='{self.parameter["test_subcriber_id"]}' AND has({log_query_rule_type}, {self.rule_uuid})"
                            log_condition_dict['filter'] = log_filter
                        else:
                            log_filter = f"client_ip={self.parameter["test_pc_ip"]} AND has({log_query_rule_type}, {self.rule_uuid})"
                            log_condition_dict['filter'] = log_filter
                            log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={self.parameter["test_pc_ip"]}", f"client_ip='{self.parameter["test_pc_ip"]}'")
                
                url = self.parameter["api_server"] + "/v1/log/query"
                # ========24.10 begin========
                # url = self.parameter["api_server"] + "/v1/logs/query"
                # ========24.10 end==========
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
        # ========24.10 begin========
        # url = api_host + "/v1/logs/schema/" + schema_type
        # vsys = {"vsys": vsys_id}
        # response = requests.get(url, headers=headers, params=vsys, verify=False)
        # ========24.10 end==========
        assert response.status_code == 200
        log_schema = json.loads(response.text)
        log_schema = log_schema['data']['fields']
        log_schema = ",".join([field['name'] for field in log_schema])
        return log_schema

    def get_metric(self, token, start_time, end_time):
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = self.parameter["api_server"] + "/v1/log/query"
            # ========24.10 begin========
            # url = self.parameter["api_server"] + "/v1/logs/query"
            # ========24.10 end==========
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
                hit_query_condition['rule_id'] = self.rule_uuid
                # ========24.10 begin========
                # hit_query_condition['rule_uuid'] = self.rule_uuid
                # ========24.10 end==========
                hit_query_condition['start_time'] = start_time
                hit_query_condition['end_time'] = end_time
                hit_query_condition['vsys_id'] = self.parameter["vsys"]
                # ========24.10 begin========
                # hit_query_condition['vsys'] = self.parameter["vsys"]
                # ========24.10 end==========
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
    
    def get_sc_metric(self, token, start_time, end_time, sc_expected_metric, active_dest_ips_list):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = "{}/v1/log/query".format(self.parameter["api_server"])
        # ========24.10 begin========
        # url = "{}/v1/logs/query".format(self.parameter["api_server"])
        # ========24.10 end==========
        post_data_ori_json = """
        {
            "execution_mode": "oneshot",
            "identifier_name": "service-chaining-policy-rule-statistics",
            "rule_id": "271039",
            "start_time": "2023-11-21T03:23:24Z",
            "end_time": "2023-11-30T07:39:49Z",
            "vsys_id": 1,
            "interval": 1,
            "duration":1,
            "limit": 10000,
            "output_mode": "json"
        }
        """
        # 重组请求体数据
        post_data_ori_dict = json.loads(post_data_ori_json)
        post_data_ori_dict["identifier_name"] = "service-chaining-policy-rule-statistics"
        post_data_ori_dict["start_time"] = start_time
        post_data_ori_dict["end_time"] = end_time
        post_data_ori_dict["rule_id"] = self.rule_uuid
        post_data_ori_dict["vsys_id"] = self.parameter["vsys"]
        # ========24.10 begin========
        # post_data_ori_dict["rule_uuid"] = self.rule_uuid
        # post_data_ori_dict["vsys"] = self.parameter["vsys"]
        # ========24.10 end==========
        response = requests.post(url, json=post_data_ori_dict, headers=headers, verify=False)
        r_dict = response.json()
        if r_dict["code"] != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Service chaining metric query failed.", flush=True)
            return 444
        else:  # 返回正常结果
            if r_dict["data"]["result"] == []:  # 为空
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Service chaining metric is empty.", flush=True)
                return 333
            else:  # metric不为空时，验证返回结果
                metric_result = False  # 默认
                result_list = r_dict["data"]["result"]
                sc_value = copy.deepcopy(result_list[0])
                metric_result = self.assert_sc_metric(sc_info, sc_value, sc_expected_metric, active_dest_ips_list)
        return metric_result

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")