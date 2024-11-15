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
    def __init__(self, parameter, policy_configuration, token, rule_uuids_tuple):
        self.api_server = parameter["api_server"]
        self.vsys = parameter["vsys"]
        self.policy_configuration = policy_configuration
        self.token = token
        rule_uuids_list = list(rule_uuids_tuple)
        self.rule_uuid = rule_uuids_list["uuid"]
    
    def organize_statistics_rule_cfg(self):
        # 变量初始化
        statistics_sc_info_list = []
        code, policy_info = self.get_policy_info(self.rule_uuid, self.policy_configuration["type"])
        if code != 200:
            return 400, statistics_sc_info_list
        if self.policy_configuration["type"] == "statistics":
            try:
                # 从Statistics Rule定义信息中获取流量验证所需数据格式
                for policy in policy_info:
                    user_region = policy["action_parameter"]
                    if user_region != {}:
                        template_id = user_region["template_profile"]
                        code, template_info = self.get_template_info(template_id, "statistics_template")
                        if code != 200:
                            return 400, statistics_sc_info_list
                        # 目前TSG仅支持一条Statistics Rule选择一条Template，如果支持多条需重写
                        for template in template_info:
                            for chart in template["dataview"]["charts"]:
                                statistics_info = {}
                                statistics_info["rule_id"] = self.rule_uuid
                                statistics_info["template_id"] = template_id
                                statistics_info["chart_id"] = chart["uuid"]
                                statistics_info["chart_type"] = chart["display"]["type"]
                                statistics_info["version"] = chart["version"]
                                if chart["display"]["type"] != "histogram" and chart["query"]["dimensions"] != []:
                                    code, query_dimensions = self.query_dimensions_from_chart_dimensions(chart["query"]["dimensions"])
                                    if code != 200:
                                        return 400, statistics_sc_info_list
                                    statistics_info["dimensions"] = query_dimensions
                                else:
                                    statistics_info["dimensions"] = chart["query"]["dimensions"]
                                code, query_metrics = self.query_metrics_from_chart_metrics(chart["query"]["metrics"])
                                if code != 200:
                                    return 400, statistics_sc_info_list
                                statistics_info["metrics"] = query_metrics
                                if "order_by" in chart["query"].keys():
                                    statistics_info["order_by"] = chart["query"]["order_by"]
                                #if chart["display"]["type"] == "histogram":
                                #    statistics_info.pop("order_by")
                                statistics_info["topk"] = ""
                                if "series_limit" in chart["query"].keys():
                                    code, topk_dimensions_tmp = self.query_topk_dimensions_from_chart_dimensions(chart["query"]["dimensions"], chart["query"]["series_limit"], chart["query"]["metrics"][0]["label"])
                                    if code != 200:
                                        return 400, statistics_sc_info_list
                                    statistics_info["topk"] = topk_dimensions_tmp
                                elif "limit" in chart["query"].keys() and chart["query"]["limit"] != 65535:
                                    statistics_info["limit"] = chart["query"]["limit"]
                                self.statistics_template_metrics_dimension_list(statistics_info)
                                statistics_sc_info_list.append(copy.deepcopy(statistics_info))
            except Exception as e:
                #traceback.print_exc()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Analyze the Template data anomaly of Statistics Rule{}".format(e))
                return 400, statistics_sc_info_list
        return 200, statistics_sc_info_list

    def query_metrics_from_chart_metrics(self, metrics_list):
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
        metrics_result = []
        try:
            for metric in metrics_list:
                metric_temp_dict = json.loads(metric_temp_json)
                metric_temp_dict["function"]["name"] = metric["function"]["name"]
                metric_temp_dict["source_fields"] = metric["source_fields"]
                metric_temp_dict["metric_name"] = metric["metric_name"]
                metric_temp_dict["metric_type"] = metric["metric_type"]
                metric_temp_dict["label"] = metric["label"]
                metrics_result.append(metric_temp_dict)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Analyze the abnormal metrics data of Template Chart. except{}".format(e))
            return 400, metrics_result
        return 200, metrics_result

    def query_dimensions_from_chart_dimensions(self, dimensions_list):
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
        dimensions_result = []
        try:
            for dimension in dimensions_list:
                dimension_temp_dict = json.loads(dimension_temp_json)
                dimension_temp_dict["dimension_name"] = dimension["source_fields"][0]
                dimension_temp_dict["label"] = dimension["label"]
                dimension_temp_dict["function"]["name"] = dimension["function"]["name"]
                dimension_temp_dict["source_fields"] = dimension["source_fields"]
                dimensions_result.append(dimension_temp_dict)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Analyze the abnormal dimesions data of Template Chart. except{}".format(e))
            return 400, dimensions_result
        return 200, dimensions_result

    def query_topk_dimensions_from_chart_dimensions(self, dimensions_list, series_limit, metric):
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
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Analyze the abnormal TOPK dimesions data of Template Chart. except{}".format(e))
            return 400, dimension_temp_dict
        return 200, dimension_temp_dict
    
    def statistics_template_metrics_dimension_list(self, statistics_info):
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
    
    # ？？
    def generate_random_ip(self, parameter, policy_configuration, traffic_generation):
        vsys_id = parameter["vsys"]
        run_env = parameter["env"]
        # Statistics中将IP改为随机
        # 是否产生Traffic随机IP标识
        traffic_radom_ip_flag = False
        # 如果是Trex流量则标识为True
        if "trex" == traffic_generation["tool"]:
            traffic_radom_ip_flag = True
        sub_id_flag = False
        if "sub_id" in policy_configuration["name"] or "_imsi_" in policy_configuration["name"] or "_imei_" in policy_configuration["name"] or "_phone_number_" in policy_configuration["name"] or "_apn_" in policy_configuration["name"]:
            sub_id_flag = True
        for i in range(len(policy_configuration["and_conditions"])):
            or_conditions = policy_configuration["and_conditions"][i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_SOURCE_IP":
                    traffic_radom_ip_flag = False
                    src_ip = or_conditions[j]["items"][0]["ip"]
                    traffic_replace_ip = 0
                    if "default" in src_ip:
                        src_ip = "10.64.77.11"
                        traffic_replace_ip = 1
                    if "-" not in src_ip and "/" not in src_ip:
                        src_ip_list = src_ip.split(".")
                        if str(vsys_id) == "1":  # 根据vsys id，确认IP范围
                            if sub_id_flag == True:
                                src_ip_list[2] = str(25)
                            else:
                                src_ip_list[2] = str(random.randint(1, 25))
                        elif str(vsys_id) == "5":  # 根据vsys id，确认IP范围
                            if sub_id_flag == True:
                                src_ip_list[2] = str(255)
                            else:
                                src_ip_list[2] = str(random.randint(224, 255))
                        if sub_id_flag == True:
                            src_ip_list[3] = str(251)
                        else:
                            src_ip_list[3] = str(random.randint(100, 249))
                        if run_env == "9140":
                            src_ip_list[0] = "172"
                            src_ip_list[1] = "56"
                        elif run_env == "tsgx":
                            src_ip_list[0] = "10"
                            src_ip_list[1] = "64"
                        new_src_ip = ".".join(src_ip_list)
                        start_ip = new_src_ip
                        end_ip = new_src_ip
                        policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"] = new_src_ip
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
                        end_ip = new_ip_2
                        new_two_ip = "-".join(new_two_ip_list)
                        policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"] = new_two_ip
                    else:
                        start_ip = end_ip = "1.1.1.1"
                    # 更改替换traffic{}中ip地址，暂时替换为clients_start_ip = clients_end_ip， servers_start_ip = servers_end_ip
                    traffic_generation["clients_start_ip"] = start_ip
                    traffic_generation["clients_end_ip"] = end_ip
        if traffic_radom_ip_flag:
            src_ip = "10.64.77.11"
            src_ip_list = src_ip.split(".")
            if str(vsys_id) == "1":  # 根据vsys id，确认IP范围
                if sub_id_flag == True:
                    src_ip_list[2] = str(25)
                else:
                    src_ip_list[2] = str(random.randint(1, 25))
            elif str(vsys_id) == "5":  # 根据vsys id，确认IP范围
                if sub_id_flag == True:
                    src_ip_list[2] = str(255)
                else:
                    src_ip_list[2] = str(random.randint(224, 255))
            if sub_id_flag == True:
                src_ip_list[3] = str(251)
            else:
                src_ip_list[3] = str(random.randint(100, 249))
            if run_env == "9140":
                src_ip_list[0] = "172"
                src_ip_list[1] = "56"
            elif run_env == "tsgx":
                src_ip_list[0] = "10"
                src_ip_list[1] = "64"
            new_src_ip = ".".join(src_ip_list)
            traffic_generation["clients_start_ip"] = new_src_ip
            traffic_generation["clients_end_ip"] = new_src_ip
        # 如果无Source、estination IP,而包含Internal、External IP
        # 集成测试环境Trex的External IP为Source IP故逻辑如下：如果是其他测试环境需要根据具体环境调整逻辑
        for i in range(len(policy_configuration["and_conditions"])):
            or_conditions = policy_configuration["and_conditions"][i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_EXTERNAL_IP":
                    if "-" in policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"]:
                        policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"] = "{}-{}".format(traffic_generation["clients_start_ip"], traffic_generation["clients_end_ip"])
                    elif "/" in policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"]:
                        policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"] = "{}/{}".format(traffic_generation["clients_start_ip"], 32)
                    else:
                        policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"] = traffic_generation["clients_start_ip"]
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Setrandom ip for statistics rule.", flush=True)
        return policy_configuration, traffic_generation

    # ？？
    def generate_random_dos_src_ip(self, parameter, policy_configuration, traffic_generation):
        vsys_id = parameter["vsys"]
        run_env = parameter["env"]
        for i in range(len(policy_configuration["and_conditions"])):
            or_conditions = policy_configuration["and_conditions"][i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_SOURCE_IP":
                    src_ip = or_conditions[j]["items"][0]["ip"]
                    if "default" in src_ip:
                        src_ip = "10.64.77.11"
                    if "-" not in src_ip and "/" not in src_ip:
                        src_ip_list = src_ip.split(".")
                        if str(vsys_id) == "1":  # 根据vsys id，确认IP范围
                            src_ip_list[2] = str(random.randint(1, 25))
                        elif str(vsys_id) == "5":  # 根据vsys id，确认IP范围
                            src_ip_list[2] = str(random.randint(224, 255))
                        src_ip_list[3] = str(random.randint(56, 99))
                        if run_env == "9140":
                            src_ip_list[0] = "172"
                            src_ip_list[1] = "56"
                        elif run_env == "tsgx":
                            src_ip_list[0] = "10"
                            src_ip_list[1] = "64"
                        new_src_ip = ".".join(src_ip_list)
                        start_ip = new_src_ip
                        end_ip = new_src_ip
                        policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"] = new_src_ip
                    elif "-" in src_ip and "/" not in src_ip:
                        two_ip_list = src_ip.split("-")
                        ip_list_1 = two_ip_list[0].split(".")
                        ip_list_2 = two_ip_list[1].split(".")
                        if str(vsys_id) == "1":  # 根据vsys id，确认IP范围
                            ip_list_1[2] = str(random.randint(1, 25))
                        elif str(vsys_id) == "5":  # 根据vsys id，确认IP范围
                            ip_list_1[2] = str(random.randint(224, 255))
                        else:
                            ip_list_1[3] = str(random.randint(56,99))
                        ip_list_2[2] = ip_list_1[2]
                        ip_list_2[3] = str(int(ip_list_1[3]) + 1)
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
                        end_ip = new_ip_2
                        new_two_ip = "-".join(new_two_ip_list)
                        policy_configuration["and_conditions"][i]["or_conditions"][j]["items"][0]["ip"] = new_two_ip
                    else:
                        start_ip = end_ip = "1.1.1.1"
                    traffic_generation["clients_start_ip"] = start_ip
                    traffic_generation["clients_end_ip"] = end_ip
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Set random ip for dos rule.", flush=True)
        return policy_configuration, traffic_generation

    # ？？
    def generate_unique_dos_dst_ip(self, traffic_generation):
        # 处理 server_start_ip 和 server_end_ip 的情况
        dst_ip = traffic_generation["servers_start_ip"]
        # 只对没有 "-" 或 "/" 的 IP 进行处理
        if "-" not in dst_ip and "/" not in dst_ip:
            # 将 IP 分割为四部分
            src_ip_list = dst_ip.split(".")
            # 随机生成新 IP 的部分
            src_ip_list[0] = "6"  # 第一部分固定为 "6"
            src_ip_list[1] = str(random.randint(0, 255))  # 第二部分随机生成 0-255
            src_ip_list[2] = str(random.randint(1, 223))  # 第三部分随机生成 1-223，避免保留地址
            src_ip_list[3] = str(random.randint(0, 255))  # 第四部分随机生成 0-255
            # 重新组合为新的 IP 地址
            new_src_ip = ".".join(src_ip_list)
            # 将新生成的 IP 替换到 traffic 中
            traffic_generation["servers_start_ip"] = new_src_ip
            traffic_generation["servers_end_ip"] = new_src_ip
        # 输出日志，记录生成的唯一 IP
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Set unique dst ip for dos rule.", flush=True)
        return traffic_generation

    def get_policy_info(self, rule_uuid, rule_type):
        try:
            # 请求接口查询metric
            if rule_type == "statistics":
                new_rule_type = "statistics-rules"
            headers = {'Content-Type': 'application/json', 'Authorization': self.token}
            url = (self.api_server + f"/v1/policies/{new_rule_type}?vsys={new_rule_type}&page_size=20&page_no=1&uuid={rule_uuid}&is_enabled=")
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code != 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception when getting Statistics Rule information from the interface. except{}".format(e))
                return 400, []
            response = json.loads(response.text)
            result = response['data']['list']
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception when getting Statistics Rule information from the interface. except{}".format(e))
            return 400, []
        return 200, result
    
    def get_template_info(self, template_id, template_type):
        try:
            # 请求接口查询metric
            headers = {'Content-Type': 'application/json', 'Authorization': self.token}
            # 获取单个Template
            #url = (api_host + f"/v1/policy/profile/statistics_template/{template_id}?page_size=-1&vsys_id={vsys_id}")
            # 获取一批Template
            url = (self.api_server + f"/v1/profiles/statistics-templates?page_size=20&page_no=1&uuid={template_id}&vsys={str(self.vsys)}")
            response = requests.get(url, headers=headers, verify=False)
            assert response.status_code == 200
            response = json.loads(response.text)
            result = response['data']['list']
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception when getting Statistics Rule information from the interface. except{}".format(e))
            return 400, result
        return 200, result

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
    # print(list1)
    # print(list1["Client IPs"])
    # print(list1["Client IPs"]["function"]["name"])
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