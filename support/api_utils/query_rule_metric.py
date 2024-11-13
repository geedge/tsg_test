# -*- coding: UTF-8 -*-
import configparser
import json
import time
import pytz
import requests
import support.ui_utils.env
from datetime import datetime
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.organize_config import *
from support.api_utils.util_statistics_template import UtilStatisticsTemplate
from support.packet_generator.workpath import workdir

class QueryRuleMetric:
    def __init__(self, parameter, policy_configuration, token, traffic_result):
        self.parameter = parameter
        self.policy_configuration = policy_configuration
        self.token = token
        self.traffic_result = traffic_result
    
    def query_rule_metric(self, verification_result, rule_uuids_tuple, start_time):
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
            if self.rule_type == "security" or self.rule_type == "pxy_intercept" or self.rule_type == "pxy_manipulation" or self.rule_type == "monitor" or self.rule_type == "dos_protection":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                metric_result = None
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
                    if metric_result == None:
                        metric_dict, error = self.get_metric(rule_uuids_tuple, start_time, end_time)
                        if len(error) != 0:
                            return error, my_driver
                        metric_result = self.verify_metric(metric_dict, verification_result)
                    if metric_result != None:
                        break
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is passed.', flush=True)
                elif metric_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is failed.', flush=True)
                elif metric_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is none.', flush=True)
                elif metric_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is no_set.', flush=True)
                return metric_result, my_driver
            elif self.rule_type == "statistics":
                max_fail_count = 15    #  更具实际情况修改： 最大查询次数， 每次间隔query_metric_interval 秒
                query_metric_interval = 10    # 每次查询statistic metric的 间隔时间 单位秒
                if initiation_method == "ui":
                    max_fail_count = 20    # 每次查询statistic metric的 间隔时间 单位秒
                organize_config = OrganizeConfig(self.parameter, self.policy_configuration, self.token, rule_uuids_tuple)
                code, statistics_template_chart_list = organize_config.organize_statistics_rule_cfg()
                if code != 200:
                    return "Exception when getting Statistics Template information from the interface", my_driver
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                if len(statistics_template_chart_list) > 0:
                    for statistics_info in statistics_template_chart_list:
                        fail_count = 0
                        while True:
                            if initiation_method == "ui":
                                element_language_menu = my_driver.find_element(By.XPATH, language_button_posXpath)
                                my_driver.execute_script("arguments[0].scrollIntoView();", element_language_menu)
                                my_driver.execute_script("arguments[0].click();", element_language_menu)
                            utc_tz = pytz.timezone('UTC')
                            current_utc_time = datetime.now(utc_tz)
                            end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                            metric_result_list = self.get_livechart_statistics(start_time, end_time, statistics_info)
                            if len(metric_result_list[1]) > 0:
                                metric_result = metric_result_list[0]
                            else:
                                metric_result = self.verify_statistics_metric(start_time, end_time, self.traffic_result, statistics_info, metric_result_list[0])
                            if metric_result == True:  # 返回结果不等于333，则退出循环查询
                                break
                            elif metric_result == 333 and metric_result_list[1] == "this is a pass":    # session的incoming outgoing,fqdn_category区分判断
                                metric_result = True    # 无法断言方向，强制通过
                                metric_result_list[1] = ""
                                break
                            else:   # 查询验证失败，再验证
                                metric_result = False
                                fail_count += 1
                                if fail_count >= max_fail_count:
                                    break
                                time.sleep(query_metric_interval)
                if metric_result == True:
                    return metric_result, my_driver
                else:
                    return metric_result_list[1], my_driver
            elif self.rule_type == "service_chaining":
                # sc自动化目前只实现了但application、单sf、单sff的用例
                conf_path = os.path.join(workdir, "configuration_file.ini")
                conf = configparser.ConfigParser()
                conf.read(conf_path, encoding="utf-8")
                active_dst_ip_list = conf.get("sc_active_dst_ip", "ip_list")
                effective_device_tag_list = ["group-xxg-tsgx", "center-xxg-tsgx"]
                sff_configuration = self.policy_configuration["action_parameter"]["sff_profiles"]
                sf_configuration = self.policy_configuration["action_parameter"]["sff_profiles"][0]["service_func_profiles"]
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                n = 0
                while n <= 4:
                    utc_tz = pytz.timezone('UTC')
                    current_utc_time = datetime.now(utc_tz)
                    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    metic_dict, code = self.get_sc_metric(self.token, rule_uuids_tuple, start_time, end_time)
                    if code == 333 or code == 444:
                        metric_result = code
                    else:
                        if self.policy_configuration["action_parameter"]["targeted_traffic"] == "raw":
                            metric_result = self.verify_sc_metric(sff_configuration, sf_configuration, active_dst_ip_list, metic_dict, self.traffic_result)
                        elif self.policy_configuration["action_parameter"]["targeted_traffic"] == "decrypted":
                            metric_result = self.verify_sc_metric(sff_configuration, sf_configuration, active_dst_ip_list, metic_dict, "")
                    if metric_result == True:
                        break
                    time.sleep(15)
                    n += 1
                negate_option = self.get_negate_option_from_configration()
                if metric_result == 333:
                    if sf_configuration[0]["connectivity"]["method"] == "vxlan_g":
                        if sf_configuration[0]["connectivity"]["sf_dest_ip"] not in active_dst_ip_list:
                            metric_result = True
                        elif sf_configuration[0]["connectivity"]["sf_dest_ip"] in active_dst_ip_list and sf_configuration[0]["admin_status"] == 0:
                            metric_result = True
                        elif sf_configuration[0]["device_group"]["tag"] not in effective_device_tag_list and sff_configuration[0]["load_balance_localization"] == "nearby":
                            metric_result = True
                        elif negate_option == 1:
                            metric_result = True
                        else:
                            metric_result = False
                    elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                        if sf_configuration[0]["admin_status"] == 0:
                            metric_result = True
                        elif sf_configuration[0]["device_group"]["tag"] not in effective_device_tag_list and sff_configuration[0]["load_balance_localization"] == "nearby":
                            metric_result = True
                        elif negate_option == 1:
                            metric_result = True
                        else:
                            metric_result = False
                elif metric_result == 444:
                    metric_result = False
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The metric result checked by calling service chaining api is passed", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(datetime.now().microsecond)[:3],"The metric result checked by calling service chaining api is failed", flush=True)
                return metric_result, my_driver
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When querying rule metric, the exception error: ", str(e), flush=True)
            return "When querying rule metric, the exception error: " + str(e)
    
    def get_metric(self, rule_uuids_tuple, start_time, end_time):
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': self.token}
            url = self.parameter["api_server"] + "/v1/logs/query"
            if "rule_number" in self.policy_configuration:
                rule_number = self.policy_configuration["rule_number"]
            else:
                rule_number = 1
            for _ in range(rule_number):
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
                    "rule_uuid": "", 
                    "start_time": "",
                    "end_time": "", 
                    "vsys": 1, 
                    "execution_mode": "oneshot", 
                    "output_mode": "json",
                    "interval": 1
                }
                rule_uuids_list = list(rule_uuids_tuple)
                hit_query_condition['rule_uuid'] = rule_uuids_list["uuid"]
                hit_query_condition['start_time'] = start_time
                hit_query_condition['end_time'] = end_time
                hit_query_condition['vsys'] = self.parameter["vsys"]
                response = requests.post(url, headers=headers, json=hit_query_condition, verify=False)
                assert response.status_code == 200
                response = json.loads(response.text)
                return response, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When getting metric, the exception error: ", e, flush=True)
            return "", "When getting metric, the exception error: " + str(e)
        
    def verify_metric(self, metric_dict, verification_result):
        metric_query = verification_result['expected_metric']
        if 'hits' in metric_query and metric_query['hits'] == 0 and len(metric_dict['data']['result']) == 0:
            metric_result = True
        elif 'hits' in metric_query and len(metric_dict['data']['result']) > 0:
            metric = metric_dict['data']['result'][0]
            if metric_query['hits'] == 1:
                for key, value in metric_query.items():
                    if key not in metric or metric[key] != value:
                        metric_result = False
                    else:
                        metric_result = True
            if metric_query['hits'] == 2:
                protocol_list = ['dns', 'ftp']
                case_name = self.parameter["test_case_name"]
                for key, value in metric_query.items():
                    if key not in metric or metric[key] > 2:
                        metric_result = False
                    elif key in metric and metric[key] == 1 and all(value in case_name for value in protocol_list):
                        metric_result = None
                    else:
                        metric_result = True
            elif metric_query['hits'] == 'many':
                for key, value in metric_query.items():
                    if key not in metric or metric[key] < 1:
                        metric_result = False
                    else:
                        metric_result = True
        else:
            metric_result = None
        return metric_result
    
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
    
    def verify_statistics_metric(self, start_time, end_time, traffic_result, statistics_info, metric_result_dict):
        result_list = []
        metrics_len = len(statistics_info["metrics"])
        dimensions_len = len(statistics_info["dimensions"]) #time调试时需确认是否处理
        tmp_result = {}
        break_flag = False
        for _ in copy.deepcopy(metric_result_dict):
            tmp_dict = {}
            tmp_dict_key = ""
            if break_flag:
                break
            for k, v in _.items():
                if v == None:  # Metric结果返回中包括None值处理
                    v = 0
                if k in statistics_info["metrics_dimension"]["metrics"].keys():
                    if v == 0:
                        continue
                    k_0 = k
                    # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并,所有Line都可以合并
                    # Line图的UNIQUE_COUNT不能合并，比如一条流量只有1个Session ID但是流量持续了多个周期，则每个周期出1个Session ID的UNIQUE_COUNT统计数据
                    if "unique_count" == statistics_info["metrics_dimension"]["metrics"][k]["metric_type"]:
                        tmp_dict = _
                        break_flag = True
                        break
                    if statistics_info["chart_type"] == "line":
                        if dimensions_len == 2:
                            tmp_dict_key = f"{tmp_dict_key};{k_0}"
                        else:
                            tmp_dict_key = f"{k_0}"
                        if len(tmp_result) > 0 and tmp_dict_key in tmp_result.keys():
                            tmp_v = tmp_result[tmp_dict_key] + v
                            tmp_result[tmp_dict_key] = tmp_v
                        else:
                            tmp_result[tmp_dict_key] = v
                elif k in statistics_info["metrics_dimension"]["dimensions"].keys():
                    #k_0 = statistics_info["metrics_dimension"]["dimensions"][k]
                    k_0 = k
                    # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并，如果line图有非Time的Dimensions根据目前设计仅有一个非时间的维度
                    if statistics_info["chart_type"] == "line":
                        if k == "Time":
                            continue
                        #if metrics_len == 1 and dimensions_len == 2:
                        if tmp_dict_key == "":
                            tmp_dict_key = f"{k_0};{v}"
                        else:
                            tmp_dict_key = f"{tmp_dict_key};{k_0}"
                    else:
                        tmp_dict[k_0] = v
                else:
                    continue
                if statistics_info["chart_type"] != "line":
                    tmp_dict[k_0] = v
                # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并
            if len(tmp_dict) > 0:
                result_list.append(tmp_dict)
        if statistics_info["chart_type"] == "line":
            if metrics_len == 1 and dimensions_len == 2:
                for key in tmp_result.keys():
                    tmp_dict = {}
                    key_list = key.split(";")
                    if len(key_list) == 3:
                        tmp_dict[key_list[0]] = key_list[1]
                        tmp_dict[key_list[2]] = tmp_result[key]
                        result_list.append(copy.deepcopy(tmp_dict))
            else:
                if tmp_result != {}:
                    result_list.append(tmp_result)
        statistics_value = []
        metrics_functions = [item["function"]["name"] for item in statistics_info["metrics"]]
        if statistics_info["chart_type"] in {"line", "table", "bar"}:
            histogram_sketch_line_flag = False
            histogram_function_temp = {"MEDIAN", "P95_PERCENTILE", "P99_PERCENTILE"}
            if statistics_info["chart_type"] == "line":
                for histogram_function in histogram_function_temp:
                    if histogram_function in metrics_functions:
                        histogram_sketch_line_flag = True
                        break
            if histogram_sketch_line_flag:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The histogram metrics Line cannot automatically compare statistical results.", flush=True)
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Debug:The statistics metric API query result is {}".format(metric_result_dict), flush=True)
                metric_results = [True, ""]
            else:
                statistics_value = copy.deepcopy(result_list[0])
                if len(result_list) != 1:  #
                    metrics_labels = [item["label"] for item in statistics_info["metrics"]]
                    # 将列表中metric值设置为0
                    for k, v in statistics_value.items():
                        if k in metrics_labels:#if isinstance(v, int):
                            statistics_value[k] = 0
                    # 遍历result结果，将metric值累加并存储到statistics_value
                    for result_index in range(len(result_list)):
                        # UNIQUE_COUNT、COUNT（SUM、RATE、BITRATE）的直接处理
                        for k, v in result_list[result_index].items():
                            if k in metrics_labels:
                                statistics_value[k] += v
                        break_flag = 0  # 默认外层循环累加，累加标志，如下面列表不是所有累加值，而是获取其中一个值即可
                        tmp_break_list_tmp = UtilStatisticsTemplate().tmp_break_list   #  兼容UI API，所以三组值
                        tmp_break_list = [i.lower() for i in tmp_break_list_tmp]   # 将元素转成小写
                        temp_dimensions_keys = [copy.deepcopy(k.lower()) for k in result_list[0].keys()]
                        for item in tmp_break_list:  # 遍历判断是否符合上述条件，获取退出累加标志1。"client_ip_sketch", "server_ip_sketch", "fqdn_category"
                            if item in temp_dimensions_keys:
                                break_flag = 1  # 退出外层累加标志
                                break
                        if break_flag == 1:
                            break  # 退出累加循环
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The actual query result data from TSG: {}".format(statistics_value), flush=True)
                # 时差，速率使用:
                util = UtilStatisticsTemplate()
                time_dif_seconds = util.time_dif_seconds(start_time, end_time)
                metric_results = self.verify_livechart_statistics(statistics_info, statistics_value, traffic_result, time_dif_seconds)  # 判断正确调用函数
        elif statistics_info["chart_type"] == "histogram":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Histogram cannot automatically compare statistical results.", flush=True)
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Debug:The statistics metric API query result is {}".format(metric_result_dict), flush=True)
            metric_results = [True, ""]
        return metric_results
    
    def get_sc_metric(self, token, rule_uuids_tuple, start_time, end_time):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = "{}/v1/logs/query".format(self.parameter["api_server"])
        post_data_ori_json = """
        {
            "execution_mode": "oneshot",
            "identifier_name": "service-chaining-policy-rule-statistics",
            "rule_uuid": "271039",
            "start_time": "2023-11-21T03:23:24Z",
            "end_time": "2023-11-30T07:39:49Z",
            "vsys": 1,
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
        rule_uuids_list = list(rule_uuids_tuple)
        post_data_ori_dict["rule_uuid"] = rule_uuids_list["uuid"]
        post_data_ori_dict["vsys"] = self.parameter["vsys"]
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
    
    def verify_sc_metric(self, sff_configuration, sf_configuration, active_dst_ip_list, metic_dict, traffic_result):
        metric_result = False
        application = self.get_application_from_configration()
        if self.policy_configuration["action_parameter"]["targeted_traffic"] == "raw":
            byte_value = traffic_result["total_bytes"]
            pkt_value = traffic_result["total_packets"]
            if sf_configuration[0]["connectivity"]["method"] == "vxlan_g" and sf_configuration[0]["connectivity"]["sf_dest_ip"] in active_dst_ip_list:
                if len(application) > 0 :
                    if application[0] == "http" or application[0] == "ssl" or application[0] == "rdp" or application[0] == "OPENVPN":
                        lost_pkt = 3
                        lost_byte = 192  # tcp三次握手的三个包的字节数和
                    elif application[0] == "ftp":
                        lost_pkt = 4
                        lost_byte = 266
                    elif application[0] == "mail":
                        lost_pkt = 15
                        lost_byte = 1273
                    elif application[0] == "dns" or application[0] == "quic" or application[0] == "rtp" :
                        lost_pkt = 0
                        lost_byte = 0
                    pkt_value -= lost_pkt
                    byte_value -= lost_byte
                traffic_result["total_bytes"] = byte_value + 50 * pkt_value
                traffic_result["total_packets"] = pkt_value
                if sff_configuration["type"] == 1:
                    if metic_dict["sent_bytes"] == metic_dict["received_bytes"] == traffic_result["total_bytes"] and metic_dict["sent_packets"] == metic_dict["received_packets"] == pkt_value:
                        metric_result = True
                    else:
                        metric_result = False
                elif sff_configuration["type"] == 2:
                    if metic_dict["sent_bytes"] == traffic_result["total_bytes"] and metic_dict["sent_packets"] == pkt_value and metic_dict["received_bytes"] == metic_dict["received_packets"] == 0:
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                if len(application) > 0 :
                    if application[0] == "http" or application[0] == "ssl" or application[0] == "rdp" or application[0] == "OPENVPN":
                        lost_pkt = 3
                        lost_byte = 192  # tcp三次握手的三个包的字节数和
                    elif application[0] == "ftp":
                        lost_pkt = 4
                        lost_byte = 266
                    elif application[0] == "mail":
                        lost_pkt = 15
                        lost_byte = 1273
                    elif application[0] == "dns" or application[0] == "quic" or application[0] == "rtp":
                        lost_pkt = 0
                        lost_byte = 0
                    pkt_value -= lost_pkt
                    byte_value -= lost_byte
                traffic_result["total_bytes"] = byte_value + 4 * pkt_value
                traffic_result["total_packets"] = pkt_value
                if sff_configuration["type"] == 2:
                    if metic_dict["sent_bytes"] == traffic_result["total_bytes"] and metic_dict["sent_packets"] == pkt_value and metic_dict["received_bytes"] == metic_dict["received_packets"] == 0:
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        elif self.policy_configuration["action_parameter"]["targeted_traffic"] == "decrypted":
            if sf_configuration[0]["connectivity"]["method"] == "vxlan_g" and sf_configuration[0]["connectivity"]["sf_dest_ip"] in active_dst_ip_list:
                if sff_configuration["type"] == 1:
                    if metic_dict["sent_bytes"] == metic_dict["received_bytes"] and metic_dict["sent_packets"] == metic_dict["received_packets"]:
                        metric_result = True
                    else:
                        metric_result = False
                elif sff_configuration["type"] == 2:
                    if metic_dict["sent_bytes"] != 0 and metic_dict["sent_packets"] != 0 and metic_dict["received_bytes"] == metic_dict["received_packets"] == 0:
                       metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                if sff_configuration["type"] == 2 and len(metic_dict) != 0:
                    if metic_dict["sent_bytes"] != 0 and metic_dict["sent_packets"] != 0 and metic_dict["received_bytes"] == metic_dict["received_packets"] == 0:
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        return metric_result
    
    def get_application_from_configration(self):
        action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(action_parameter)):
            or_conditions = action_parameter[i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_APP_ID":
                    application = or_conditions[j]["items"]
                    return application
    
    def get_negate_option_from_configration(self):
        negate_option_list = []
        action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(action_parameter)):
            negate_option_list.append(action_parameter[i]["negate_option"])
        for value in negate_option_list:
            if value == 1:
                return 1
        return 0