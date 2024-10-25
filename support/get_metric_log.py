#!/usr/bin/python3
# coding=utf-8
import copy
import requests
import json
from datetime import datetime
from support.api_utils.util_statistics_template import UtilStatisticsTemplate

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
            # ========24.10 begin========
            # log_condition = {
            #     "page_no": 1,
            #     "page_size": 20,
            #     "source": "security_event",
            #     "columns": None,
            #     "start_time": "",
            #     "end_time": "",
            #     "filter": "",
            #     "vsys": 1
            # }
            # ========24.10 end==========
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

    def get_log_schema(self, token, schema_type, api_host, vsys):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/log/schema/" + schema_type + "?vsys_id=" + str(vsys)
        response = requests.get(url, headers=headers, verify=False)
        # ========24.10 begin========
        # url = api_host + "/v1/logs/schema/" + schema_type
        # vsys = {"vsys": vsys}
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
                # ========24.10 begin========
                # hit_query_condition = {
                #     "identifier_name": dataset_identifier_name, 
                #     "rule_uuid": "", 
                #     "start_time": "",
                #     "end_time": "", 
                #     "vsys": 1, 
                #     "execution_mode": "oneshot", 
                #     "output_mode": "json",
                #     "interval": 1
                # }
                # ========24.10 end==========
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
    
    def get_sc_metric(self, token, start_time, end_time):
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
        # ========24.10 begin========
        # post_data_ori_json = """
        # {
        #     "execution_mode": "oneshot",
        #     "identifier_name": "service-chaining-policy-rule-statistics",
        #     "rule_uuid": "271039",
        #     "start_time": "2023-11-21T03:23:24Z",
        #     "end_time": "2023-11-30T07:39:49Z",
        #     "vsys": 1,
        #     "interval": 1,
        #     "duration":1,
        #     "limit": 10000,
        #     "output_mode": "json"
        # }
        # """
        # ========24.10 end==========
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
            return "", 444
        else:  # 返回正常结果
            if r_dict["data"]["result"] == []:  # 为空
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Service chaining metric is empty.", flush=True)
                return "", 333
            else:  # metric不为空时，验证返回结果
                result_list = r_dict["data"]["result"]
                sc_value = copy.deepcopy(result_list[0])
                return sc_value, ""

    def get_livechart_statistics(self, token, start_time, end_time, statistics_info):
        """
        :param token:
        :param start_time:
        :param end_time:
        :param statistics_info:
        :param test_data:
        :return:
        """
        # 请求接口查询statistics metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = "{}/v1/log/query".format(self.parameter["api_server"])
        # 24.08重组请求体dsl结构数据,文档见https://docs.geedge.net/display/TSG/DSL+Examples
        post_data_ori_json = """
        {
            "dsl": {
                "name": "customized-statistics",
                "data_source": "statistics_rule",
                "filter": "vsys_id in (1) and rule_id = 282009 and template_id = 3015 and chart_id = 3026 and version = 4",
                "custom.statistics.dimensions": [
                    {
                        "metric_name": "client_country",
                        "label": "Client Country"
                    }
                ],
                "custom.statistics.metrics": [
                    {
                        "function": {
                            "name": "UNIQUE_COUNT"
                        },
                        "metric_type": "unique_count",
                        "metric_name": "unique_count_1",
                        "label": "UNIQUE_COUNT(Server IP Object List)"
                    }
                ],
                "intervals": [
                    "2024-08-01 11:39:42/2024-08-01 11:44:42"
                ],
                "order_by": "UNIQUE_COUNT(Server IP Object List) DESC",
                "limit": 20,
                "execution_mode": "oneshot"
            },
            "vsys_id": 1
        }
        """
        post_data_ori_dict = json.loads(post_data_ori_json)
        post_data_ori_dict_dsl = post_data_ori_dict["dsl"]
        post_data_ori_dict_dsl["name"] = "customized-statistics" #该值对Statistics Rule Chart查询来说是固定的所以直接赋值
        post_data_ori_dict_dsl["data_source"] = "statistics_rule" #该值对Statistics Rule Chart查询来说是固定的所以直接赋值
        post_data_ori_dict_dsl["filter"] = "vsys_id in ({}) and rule_id = {} and template_id = {} and chart_id = {} and version = {}".format(self.parameter["vsys"], statistics_info["rule_id"], statistics_info["template_id"], statistics_info["chart_id"], statistics_info["version"])
        post_data_ori_dict_dsl["custom.statistics.dimensions"] = statistics_info["dimensions"]
        if statistics_info["chart_type"] == "bar":
            variables_tmp = UtilStatisticsTemplate().time_dif_seconds(start_time,end_time)
            metrics_tmp = []
            for metric in statistics_info["metrics"]:
                if metric["function"]["name"] in ["RATE", "BITRATE"]:
                    function_tmp = {
                        "name": metric["function"]["name"],
                        "variables": [
                            variables_tmp
                        ]
                    }
                    metric["function"] = copy.deepcopy(function_tmp)
                metrics_tmp.append(metric)
            post_data_ori_dict_dsl["custom.statistics.metrics"] = statistics_info["metrics"]
        else:
            post_data_ori_dict_dsl["custom.statistics.metrics"] = statistics_info["metrics"]
        post_data_ori_dict_dsl["intervals"] = [f"{start_time}/{end_time}"]
        if statistics_info["topk"] != "" and statistics_info["topk"] != None:
            post_data_ori_dict_dsl["custom.statistics.subquery.topk"] = statistics_info["topk"]
        if "order_by" in statistics_info.keys():
            post_data_ori_dict_dsl["order_by"] = "'{}' DESC".format(statistics_info["order_by"])
        else:
            post_data_ori_dict_dsl.pop("order_by")  # 不存在，暂时删除key
        if "limit" in statistics_info.keys():
            post_data_ori_dict_dsl["limit"] = statistics_info["limit"]
        else:
            post_data_ori_dict_dsl.pop("limit")  # 不存在，暂时删除key
        post_data_ori_dict["dsl"] = post_data_ori_dict_dsl
        post_data_ori_dict["vsys_id"] = self.parameter["vsys"]
        # 请求接口获取Metrics数据
        response = requests.post(url, json=post_data_ori_dict, headers=headers, verify=False)
        r_dict = response.json()
        # 打印获取Metrics相关开始结束时间和Rule ID信息信息，方便后面出错排查问题
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "statistics metric:start_time:{}, end_time:{}, rule_id:{}, template_id:{}, chart_id:{}, version:{}".format(start_time, end_time, statistics_info["rule_id"], statistics_info["template_id"], statistics_info["chart_id"], statistics_info["version"]))
        if r_dict["code"] != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],  "Exception when getting Metrics data from the interface.")
            return [False, "The statistics metric API query failed."]
        else:  # 返回正常结果
            if r_dict["data"]["result"] == []:  # 为空
                # 对应有方向的session的单一Metrics方式需要另行处理
                tmp_in_out_list = UtilStatisticsTemplate().tmp_in_out_list
                # api返回值为空，不判断方向，直接返回重新查找
                if len(statistics_info["metrics"]) == 1:
                    if len(statistics_info["metrics"][0]["source_fields"]) == 1 and statistics_info["metrics"][0]["source_fields"][0] in tmp_in_out_list:
                        return [333, "this is a pass"]
                return [False, "statistics metric no result was found."]
            else:
                return [r_dict["data"]["result"], ""]

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")