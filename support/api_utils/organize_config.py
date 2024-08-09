import copy
import os
import sys
import inspect
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import random
import requests
import json
from datetime import datetime
import traceback

class OrganizeConfig:
    def organize_statistics_rule_cfg(self, parameter, test_data):
        # 变量初始化
        api_server = parameter["api_server"]
        run_env = parameter["env"]
        vsys_id = parameter["vsys_id"]
        token = test_data["token"]
        policy_define = self.get_policy_define(token, test_data["rule_id"], test_data["policy_type"], api_server, vsys_id)
        statistics_sc_info_list = []
        if test_data["policy_type"] == "statistics":
            try:
                # 从Statistics Rule定义信息中获取流量验证所需数据格式
                for policy in policy_define:
                    user_region = policy["user_region"]
                    if user_region != {}:
                        template_id = user_region["template_id"]
                        template_define = self.get_template_define(token, template_id, "statistics_template",api_server, vsys_id)
                        # 目前TSG仅支持一条Statistics Rule选择一条Template，如果支持多条需重写
                        template_number = 0
                        for template in template_define:
                            template_temp = []
                            #    chart_number = 0
                            for chart in template["dataview"]["charts"]:
                                #24.08及以后版本
                                statistics_info = {}
                                statistics_info["rule_id"] = test_data["rule_id"]
                                statistics_info["template_id"] = template_id
                                statistics_info["chart_id"] = chart["id"]
                                statistics_info["chart_type"] = chart["display"]["type"]
                                statistics_info["version"] = chart["version"]
                                #24.08及以后版本
                                #code,metrics_tmp = self.chart_metrics_to_query_metrics(chart["query"]["metrics"])
                                if chart["display"]["type"] != "Histogram" and chart["query"]["dimensions"] != []:
                                    statistics_info["dimensions"] = self.chart_dimensions_to_query_dimensions(chart["query"]["dimensions"])
                                else:
                                    statistics_info["dimensions"] = chart["query"]["dimensions"]
                                statistics_info["metrics"] = self.chart_metrics_to_query_metrics(chart["query"]["metrics"])
                                if "order_by" in chart["query"].keys():
                                    statistics_info["order_by"] = chart["query"]["order_by"]
                                if chart["display"]["type"] == "Histogram":
                                    statistics_info.pop("order_by")
                                statistics_info["topk"] = ""
                                if "series_limit" in chart["query"].keys():
                                    topk_dimensions_tmp = self.chart_topk_dimensions_to_query_topk_dimensions(
                                        chart["query"]["dimensions"], chart["query"]["series_limit"],
                                        chart["query"]["metrics"][0]["label"])
                                    statistics_info["topk"] = topk_dimensions_tmp
                                elif "limit" in chart["query"].keys() and chart["query"]["limit"] != 65535:
                                    statistics_info["limit"] = chart["query"]["limit"]
                                self.statistics_template_metrics_dimension_list_2408(statistics_info)
                                statistics_sc_info_list.append(copy.deepcopy(statistics_info))
            except Exception as e:
                traceback.print_exc()
                #self.error_print_function(inspect.currentframe().f_code.co_name,"Failed to parse Dimensions!")
        return statistics_sc_info_list

    def chart_metrics_to_query_metrics(self,metrics_list):
        metric_temp_json = """
        {
            "function": {
                "name": "UNIQUE_COUNT"
            },
            "source_fields": [
                "sent_bytes",
                "received_bytes"
            ],
            "metric_name": "unique_count_1",
            "metric_type": "unique_count",
            "label": "Client IPs"
        }       
        """
        try:
            metrics_result = []
            for metric in metrics_list:
                metric_temp_dict = json.loads(metric_temp_json)
                metric_temp_dict["function"]["name"] = metric["function"]["name"]
                metric_temp_dict["source_fields"] = metric["source_fields"]
                metric_temp_dict["metric_name"] = metric["metric_name"]
                metric_temp_dict["metric_type"] = metric["metric_type"]
                metric_temp_dict["label"] = metric["label"]
                metrics_result.append(metric_temp_dict)
            return metrics_result
        except Exception as e:
            self.error_print_function(inspect.currentframe().f_code.co_name, "Failed to parse Dimensions!")
            raise "Failed to parse Metrics!".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3])

    def chart_dimensions_to_query_dimensions(self,dimensions_list):
        dimension_temp_json = """
        {
            "dimension_name": "client_ip",
            "label": "Client IPs",
            "function": {
                "name": ""
            },
            "source_fields": [
                "sent_bytes",
                "received_bytes"
            ]
        }       
        """
        try:
            dimensions_result = []
            for dimension in dimensions_list:
                dimension_temp_dict = json.loads(dimension_temp_json)
                dimension_temp_dict["dimension_name"] = dimension["source_fields"][0]
                dimension_temp_dict["label"] = dimension["label"]
                dimension_temp_dict["function"]["name"] = dimension["function"]["name"]
                dimension_temp_dict["source_fields"] = dimension["source_fields"]
                dimensions_result.append(dimension_temp_dict)
        except Exception as e:
            self.error_print_function(inspect.currentframe().f_code.co_name, "Failed to parse Dimensions!")
            raise "Failed to parse Dimensions!".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(datetime.now().microsecond)[:3])
        return dimensions_result

    def chart_topk_dimensions_to_query_topk_dimensions(self, dimensions_list, series_limit, metric):
        dimension_temp_json = """
        {
            "dimensions": [
                "Client IP"
            ],
            "metric": "Bytes",
            "limit": 10
        }   
        """
        dimension_temp_dict = {}
        try:
            for dimension in dimensions_list:
                dimension_temp_dict = json.loads(dimension_temp_json)
                if dimension["source_fields"][0] != "__time":
                    dimension_temp_dict["dimensions"][0] = dimension["label"]
                    dimension_temp_dict["metric"] = metric
                    dimension_temp_dict["limit"] = series_limit
                    break
        except Exception as e:
            self.error_print_function(inspect.currentframe().f_code.co_name, "Failed to parse TOPK Dimensions!")
            raise "Failed to parse TOPK Dimensions!".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                            str(datetime.now().microsecond)[:3])
        return dimension_temp_dict
    def statistics_template_metrics_dimension_list_2408(self,statistics_info):
        chart_dict = {"metrics": {}, "dimensions": {}}
        if statistics_info["chart_type"] != "histogram" and statistics_info["dimensions"] != []:
            dimensions_list = {}
            for i in range(len(statistics_info["dimensions"])):
                dimensions_list[statistics_info["dimensions"][i]["label"]] = statistics_info["dimensions"][i]
            chart_dict["dimensions"] = dimensions_list
        if statistics_info["metrics"] != []:
            metrics_list = {}
            for i in range(len(statistics_info["metrics"])):
                metrics_list[statistics_info["metrics"][i]["label"]] = statistics_info["metrics"][i]
            chart_dict["metrics"] = metrics_list
        statistics_info["metrics_dimension"] = chart_dict
        return statistics_info
    def generate_random_ip(self, config, parameter):
        vsys_id = parameter["vsys_id"]
        run_env = parameter["env"]
        # statistics中将ip改为随机
        if "condition" in config.keys():
            for obj in config["condition"]:
                if "source_ip" == obj:# or "destination_ip" in obj:
                    src_ip = config["condition"]["source_ip"][0]["item"][0]["item_value"]
                    traffic_replace_ip = 0
                    if "default" in src_ip:
                        src_ip = "10.64.77.11"
                        traffic_replace_ip = 1
                    if "-" not in src_ip and "/" not in src_ip:
                        src_ip_list = src_ip.split(".")
                        if str(vsys_id) == "1":  # 根据vsys id，确认IP范围
                            src_ip_list[2] = str(random.randint(1, 25))
                        elif str(vsys_id) == "5":  # 根据vsys id，确认IP范围
                            src_ip_list[2] = str(random.randint(224, 224))
                        src_ip_list[3] = str(random.randint(100, 250))
                        if run_env == "9140":
                            src_ip_list[0] = "172"
                            src_ip_list[1] = "56"
                        elif run_env == "tsgx":
                            src_ip_list[0] = "10"
                            src_ip_list[1] = "64"
                        new_src_ip = ".".join(src_ip_list)
                        start_ip = new_src_ip
                        stop_ip = new_src_ip
                        config["condition"][obj][0]["item"][0]["item_value"] = new_src_ip
                    elif "-" in src_ip and "/" not in src_ip:
                        two_ip_list = src_ip.split("-")
                        ip_list_1 = two_ip_list[0].split(".")
                        ip_list_2 = two_ip_list[1].split(".")
                        if str(vsys_id) == "1":  # 根据vsys id，确认IP范围
                            ip_list_1[2] = str(random.randint(1, 25))
                        elif str(vsys_id) == "5":  # 根据vsys id，确认IP范围
                            ip_list_1[2] = str(random.randint(224, 224))
                        else:
                            ip_list_1[3] = str(random.randint(1, 50))
                        ip_list_2[2] = ip_list_1[2]
                        ip_list_2[3] = str(int(ip_list_1[3]) + 200)
                        new_ip_1 = ".".join(ip_list_1)
                        new_ip_2 = ".".join(ip_list_2)
                        if run_env == "9140":
                            ip_list_1[0] = "172"
                            ip_list_1[1] = "56"
                            ip_list_2[0] = "172"
                            ip_list_2[1] = "56"
                        elif run_env == "tsgx":
                            ip_list_1[0] = "10"
                            ip_list_1[1] = "64"
                            ip_list_2[0] = "10"
                            ip_list_2[1] = "64"
                        new_two_ip_list = []
                        new_two_ip_list.append(new_ip_1)
                        new_two_ip_list.append(new_ip_2)
                        start_ip = new_ip_1
                        stop_ip = new_ip_2
                        new_two_ip = "-".join(new_two_ip_list)
                        config["condition"][obj][0]["item"][0]["item_value"] = new_two_ip
                    else:
                        start_ip = stop_ip = "1.1.1.1"
                        self.error_print_function(inspect.currentframe().f_code.co_name, "Setrandom ip error.")
                    # 更改替换traffic{}中ip地址，暂时替换为clients_start_ip = clients_end_ip， servers_start_ip = servers_end_ip
                    if obj == "source_ip":# and traffic_replace_ip == 1:
                        config["traffic"]["clients_start_ip"] = start_ip
                        config["traffic"]["clients_end_ip"] = stop_ip
                    #elif obj == "destination_ip":# and traffic_replace_ip == 1:
                    #    config["traffic"]["servers_start_ip"] = start_ip
                    #    config["traffic"]["servers_end_ip"] = stop_ip
                    else:
                        self.error_print_function(inspect.currentframe().f_code.co_name, "Setrandom ip error.")
                        pass
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Setrandom ip for statistics rule.", flush=True)
        return config

    def get_policy_define(self, token, rule_id, rule_type, api_host, vsys_id):
        try:
            # 请求接口查询metric
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = api_host + "/v1/policy/rule"
            # ?page_size=20&page_no=1&ids=849138&type=statistics&is_enabled=&with_sub_vsys=1&page_location=0&location_id=&location_key=&vsys_id=1
            query_condition = {"page_size": 20, "page_no": 1, "ids": rule_id, "type": rule_type,
                            "is_enabled": "True", "with_sub_vsys": 1, "page_location": "oneshot", "location_key": "json",
                            "vsys_id": vsys_id}
            #https://192.168.44.3/v1/policy/rule?page_size=20&page_no=1&type=statistics&name=&is_enabled=&with_sub_vsys=1&user_tag_ids=&last_modified_by=&created_by=&page_location=0&location_id=&location_key=&vsys_id=
            url = (api_host + f"/v1/policy/rule?page_size=20&page_no=1&ids={rule_id}&type={rule_type}&is_enabled=&with_sub_vsys=1&page_location=0&location_id=&location_key=&vsys_id={vsys_id}")
            #url = (api_host + f"/v1/policy/rule/{rule_id}?vsys_id={str(vsys_id)}")
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code != 200:
                self.error_print_function(inspect.currentframe().f_code.co_name, f"response.status_code:{response.status_code}")
            response = json.loads(response.text)
            result = response['data']['rules']
            return result
        except AssertionError as e:
            self.error_print_function(inspect.currentframe().f_code.co_name, e)
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def get_template_define(self, token, template_id, template_type, api_host, vsys_id):
        try:
            # 请求接口查询metric
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            # 获取单个Template
            #url = (api_host + f"/v1/policy/profile/statistics_template/{template_id}?page_size=-1&vsys_id={vsys_id}")
            # 获取一批Template
            url = (api_host + f"/v1/policy/profile/statistics_template?page_size=20&page_no=1&ids={template_id}&vsys_id={str(vsys_id)}")
            response = requests.get(url, headers=headers, verify=False)
            assert response.status_code == 200
            response = json.loads(response.text)
            result = response['data']['statistics_templates']
            return result
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def error_print_function(self, function, error):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Class:{self.__class__.__name__},Function:{function}Error: {error}", flush=True)

if __name__ == "__main__":

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test1 = {"Client IPs1":{
        "function": {
            "name": "UNIQUE_COUNT"
        },
        "metric_name": "unique_count_1",
        "metric_type": "unique_count",
        "label": "Client IPs1"
    },"Client IPs":{
        "source_fields": [
            "sent_bytes",
            "received_bytes"
        ],
        "function": {
            "name": "COUNT"
        },
        "metric_name": "unique_count_1",
        "metric_type": "unique_count",
        "label": "Client IPs"
    }}
    test = [{
        "function": {
            "name": "UNIQUE_COUNT"
        },
        "metric_name": "unique_count_1",
        "metric_type": "unique_count",
        "label": "Client IPs1"
    }, {
        "function": {
            "name": "COUNT"
        },
        "metric_name": "unique_count_1",
        "metric_type": "unique_count",
        "label": "Client IPs"
    }]
    list1 = {}
    for t in test:
        list1[t["label"]] = t
    print(list1)
    print(list1["Client IPs"])
    print(list1["Client IPs"]["function"]["name"])
    #metrics_labels = [{item["label"]:item} for item in test],
    #if "Client IPs" in metrics_labels:
    #    print(metrics_labels["Client IPs"])
    """
    import copy

    original = {'c D': 3, 'a C': 1, 'b F': 2}
    deep_copied = copy.deepcopy(original)

    # 打印 original 和 deep_copied 的键
    print("Original keys:", list(original.keys()))  # 输出: ['c', 'a', 'b']
    print("Deep copied keys:", list(deep_copied.keys()))  # 输出: ['c', 'a', 'b']

    # 手动排序键
    sorted_keys = sorted(deep_copied.keys())
    print("Sorted keys:", sorted_keys)  # 输出: ['a', 'b', 'c']
    """