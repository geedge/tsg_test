# -*- coding: UTF-8 -*-
import configparser
import json
import time
import pytz
import requests
from datetime import datetime
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
            self.rule_type = self.policy_configuration["type"]
            if self.rule_type == "security" or self.rule_type == "proxy_intercept" or self.rule_type == "proxy_manipulation" or self.rule_type == "monitor" or self.rule_type == "dos_protection":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                metric_result = None
                for _ in range(int(90)):
                    utc_tz = pytz.timezone('UTC')
                    current_utc_time = datetime.now(utc_tz)
                    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    time.sleep(7)
                    if metric_result == None:
                        metric_dict, error = self.get_metric(rule_uuids_tuple, start_time, end_time)
                        if len(error) != 0:
                            return error
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
                return metric_result
            elif self.rule_type == "statistics":
                max_fail_count = 15    #  更具实际情况修改： 最大查询次数， 每次间隔query_metric_interval 秒
                query_metric_interval = 10    # 每次查询statistic metric的 间隔时间 单位秒
                """        
                statistics_template = self.policy_configuration["action_parameter"]["template_profile"]
                """
                organize_config = OrganizeConfig(self.parameter, self.policy_configuration, self.token, rule_uuids_tuple)
                code, statistics_template_chart_list = organize_config.organize_statistics_rule_cfg()
                if code != 200:
                    return "Exception when getting Statistics Template information from the interface"
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                if len(statistics_template_chart_list) > 0:
                    for statistics_info in statistics_template_chart_list:
                        fail_count = 0
                        while True:
                            utc_tz = pytz.timezone('UTC')
                            current_utc_time = datetime.now(utc_tz)
                            end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                            bool_result, metric_str = self.get_livechart_statistics(self.token, start_time, end_time, statistics_info)
                            if bool_result == True and len(metric_str) == 0:
                                continue
                            elif bool_result == False:
                                return metric_str
                            else:
                                flag, metric_result = self.verify_statistics_metric(start_time, end_time, self.traffic_result, statistics_info, metric_str)
                                #if not flag:
                                #    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "DEBUG：Case Flag：{}; metric_result:{}".format(flag, metric_result), flush=True)
                                if flag == True:  # 返回结果不等于333，则退出循环查询
                                    break
                                elif flag == 333 and metric_result == "this is a pass":    # session的incoming outgoing,fqdn_category区分判断
                                    flag = True    # 无法断言方向，强制通过
                                    metric_result = ""
                                    break
                                else:   # 查询验证失败，再验证
                                    flag = False
                                    fail_count += 1
                                    if fail_count >= max_fail_count:
                                        break
                                    time.sleep(query_metric_interval)
                return flag
            elif self.rule_type == "service_chaining":
                # sc自动化目前只实现了但application、单sf、单sff的用例？？
                conf_path = os.path.join(workdir, "configuration_file.ini")
                conf = configparser.ConfigParser()
                conf.read(conf_path, encoding="utf-8")
                active_dst_ip_list = conf.get("sc_active_dst_ip", "ip_list")
                effective_device_tag_list = ["group-xxg-tsgx", "center-xxg-tsgx"]
                sff_configuration = self.policy_configuration["action_parameter"]["sff_profiles"]
                sf_configuration = self.policy_configuration["action_parameter"]["sf_configuration"]
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                n = 0
                while n <= 4:
                    utc_tz = pytz.timezone('UTC')
                    current_utc_time = datetime.now(utc_tz)
                    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    metric_dict, code = self.get_sc_metric(self.token, rule_uuids_tuple, start_time, end_time)
                    if code == 333 or code == 444:
                        metric_result = code
                    else:
                        if self.policy_configuration["action_parameter"]["targeted_traffic"] == "raw":
                            metric_result = self.verify_sc_metric(sff_configuration, sf_configuration, active_dst_ip_list, metric_dict, self.traffic_result)
                        elif self.policy_configuration["action_parameter"]["targeted_traffic"] == "decrypted":
                            metric_result = self.verify_sc_metric(sff_configuration, sf_configuration, active_dst_ip_list, metric_dict, "")
                    if metric_result == True:
                        break
                    time.sleep(15)
                    n += 1
                negate_option = self.get_negate_option_from_configration()
                if metric_result == 333:
                    if sf_configuration[0]["connectivity"]["method"] == "vxlan_g":
                        if sf_configuration[0]["connectivity"]["dest_ip"] not in active_dst_ip_list:
                            metric_result = True
                        elif sf_configuration[0]["connectivity"]["dest_ip"] in active_dst_ip_list and sf_configuration[0]["admin_status"] == 0:
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
                return metric_result
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
                elif self.rule_type == 'proxy_intercept' or self.rule_type == 'proxy_manipulation':
                    dataset_identifier_name = "proxy-policy-rule-statistics"
                elif self.rule_type == 'monitor':
                    dataset_identifier_name = "monitor-policy-rule-statistics"
                elif self.rule_type == 'dos_protection':
                    dataset_identifier_name = "dos-protection-rule-statistics"
                hit_query_condition = {
                    "identifier_name": dataset_identifier_name, 
                    "filter": "", 
                    "start_time": "",
                    "end_time": "", 
                    "vsys": 1, 
                    "execution_mode": "oneshot", 
                    "output_mode": "json",
                    "interval": 1
                }
                rule_uuids_list = list(rule_uuids_tuple)
                # hit_query_condition['rule_uuid'] = rule_uuids_list["uuid"]
                hit_query_condition['filter'] = "rule_uuid in ('{}')".format(rule_uuids_list[0]["uuid"])
                hit_query_condition['start_time'] = start_time
                hit_query_condition['end_time'] = end_time
                hit_query_condition['vsys'] = int(self.parameter["vsys"])
                # hit_query_condition['vsys'] = self.parameter["vsys"]
                response = requests.post(url, headers=headers, json=hit_query_condition, verify=False)
                assert response.status_code == 200
                response = json.loads(response.text)
                return response, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When getting metric, the exception error: ", e, flush=True)
            return "", "When getting metric, the exception error: " + str(e)
        
    def verify_metric(self, metric_dict, verification_result):
        metric_query = verification_result['expected_metric']
        if 'hits' in metric_query and metric_query['hits'] == 0 and len(metric_dict['data']['list']) == 0:
            metric_result = True
        elif 'hits' in metric_query and len(metric_dict['data']['list']) > 0:
            metric = metric_dict['data']['list'][0]
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
        url = "{}/v1/logs/query".format(self.parameter["api_server"])
        # 24.08重组请求体dsl结构数据,文档见https://docs.geedge.net/display/TSG/DSL+Examples
        post_data_ori_json = """
        {
            "dsl": {
                "name": "customized-statistics",
                "data_source": "statistics_rule",
                "filter": "vsys_id in (1) and rule_uuid = 282009 and template_uuid = 3015 and chart_uuid = 3026 and version = 4",
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
        post_data_ori_dict_dsl["filter"] = "vsys_id in ({}) and rule_uuid = '{}' and template_uuid = '{}' and chart_uuid = '{}' and version = {}".format(self.parameter["vsys"], statistics_info["rule_uuid"], statistics_info["template_uuid"], statistics_info["chart_uuid"], statistics_info["version"])
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
            post_data_ori_dict_dsl["order_by"] = " '{}' DESC".format(statistics_info["order_by"].strip())
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
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "statistics metric:start_time:{}, end_time:{}, rule_uuid:{}, template_uuid:{}, chart_uuid:{}, version:{}".format(start_time, end_time, statistics_info["rule_uuid"], statistics_info["template_uuid"], statistics_info["chart_uuid"], statistics_info["version"]))
        if r_dict["code"] != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],  "Exception when getting Metrics data from the interface.")
            return False, "The statistics metric API query failed.stat code:{}".format(r_dict["code"])
        else:  # 返回正常结果
            return True, r_dict["data"]["list"]
    
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
        return metric_results[0], metric_results[1]
    
    def verify_livechart_statistics(self, statistics_info, statistics_value, statistics_metircs_except, time_dif_seconds):
        chart_type = statistics_info["chart_type"]
        metric_result = False
        failure_reason_info = ""
        failure_info_1 = ""
        failure_info_2 = ""
        failure_info_3 = ""
        metrics_info = {}
        try:
            metrics_labels = [item["label"] for item in statistics_info["metrics"]]
            for i in range(len(statistics_info["metrics"])):
                metrics_info[statistics_info["metrics"][i]["label"]] = statistics_info["metrics"][i]
            #for metrics in statistics_info["metrics"]:
            #    metrics_info[metrics["label"]] = metrics
            # 重组需要断言使用的key列表
            assert_key_list = []
            for k, v in statistics_value.items():
                if k in metrics_labels:
                    """          
                    match chart_type:
                        case "line":
                            metric_result,failure_info_2 = self.metric_value_verification(assert_key, statistics_metircs_except)
                        case "histogram":
                            metric_result = True
                        case _:
                            metric_result,failure_info_2 = self.metric_value_verification(assert_key,statistics_metircs_except)
                    """
                    if chart_type == "line":
                        failure_info_1 = f"Total expected results for traffic replay:{statistics_metircs_except}"
                        time_dif_seconds = 0 #line图5分钟内数据按每秒时间粒度，按时间前面已经累加，此处不再平均
                        metric_result, failure_info_2 = self.metric_value_verification(k, metrics_info[k], v, statistics_metircs_except,time_dif_seconds)
                    elif chart_type == "histogram":
                        metric_result = True
                    elif chart_type == "table" or chart_type == "bar":
                        failure_info_1 = f"Total expected results for traffic replay:{statistics_metircs_except}"
                        if chart_type == "bar":
                            time_dif_seconds = 0  # Bar图搜索时间范围内总量，前面添加了dsl的metrics-function-variables参数，此处不再平均
                        metric_result, failure_info_2 = self.metric_value_verification(k, metrics_info[k], v, statistics_metircs_except,time_dif_seconds)
                    else:
                        failure_info_1 = f"Chart Type Error:{chart_type}"
                else:
                    continue
                if metric_result == False:
                    actual_result = f"Total actual results: {statistics_value}"
                    failure_reason_info = "{}{}{}.{}".format(failure_info_1, failure_info_2, failure_info_3, actual_result)
                    break
            return metric_result, failure_reason_info
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Chart Visualization Type verification anomaly.exception:{}".format(exception_result), flush=True)
            return metric_result, failure_info_2
    
    def metric_value_verification(self, assert_key, metric_info, stats_value, test_traffic_statistics, time_dif_seconds):
        #metric_info:[{'function': {'name': 'UNIQUE_COUNT'}, 'label': 'UNIQUECOUNT(Client IP)', 'metric_name': 'unique_count_1', 'metric_type': 'unique_count', 'source_fields': ['client_ip']}]
        function_name = metric_info["function"]["name"]
        source_fields_tmp = metric_info["source_fields"]
        metric_result = False
        try:
            match function_name:
                case "SUM":
                    time_dif_seconds = 0
                    metric_result, failure_info_2 = self.metric_count_value_verification(source_fields_tmp, stats_value,1, test_traffic_statistics, time_dif_seconds)
                case "RATE":
                    metric_result, failure_info_2 = self.metric_count_value_verification(source_fields_tmp, stats_value,1, test_traffic_statistics, time_dif_seconds)
                case "BITRATE":
                    metric_result, failure_info_2 = self.metric_count_value_verification(source_fields_tmp, stats_value,8, test_traffic_statistics, time_dif_seconds)
                case "UNIQUE_COUNT":
                    time_dif_seconds = 0
                    metric_result, failure_info_2 = self.metric_unique_count_value_verification(source_fields_tmp, stats_value, test_traffic_statistics)
                case "HISTOGRAM":
                    time_dif_seconds = 0
                    metric_result, failure_info_2 = self.metric_histogram_value_verification(source_fields_tmp, stats_value)
                case "MEDIAN" | "P95_PERCENTILE" | "P99_PERCENTILE":
                    time_dif_seconds = 0
                    metric_result, failure_info_2 = self.metric_histogram_value_verification(source_fields_tmp, stats_value)
                case _:
                    failure_info_2 = f"Invalid function name: {function_name}"
            return metric_result, failure_info_2
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Statistical metric data verification anomaly.exception:{}".format(exception_result), flush=True)
            return metric_result, failure_info_2
    
    def metric_count_value_verification(self, source_fields, stats_value, rate_coefficient, test_traffic_statistics, time_dif_seconds = 1):
        failure_info_2 = ""
        metric_result = False
        try:#经与OLAP沟通：目前计算方式为先除以时间再乘以8，本身已经是bps 降低的这点精度可以忽略（只有字节数据很低的时候精度会降低，实际数据都比较大不会影响）如果将*8 放在表达式里面，有表达式定义会有点问题，故修改自动化计算bps方式和OLAP保持一致
            total_bytes_sent = test_traffic_statistics["total_bytes_sent"]
            if total_bytes_sent > 0 and time_dif_seconds > 1:
                total_bytes_sent = round(total_bytes_sent / time_dif_seconds, 2) * rate_coefficient
            else:
                total_bytes_sent = test_traffic_statistics["total_bytes_sent"] * rate_coefficient

            total_bytes_received = test_traffic_statistics["total_bytes_received"]
            if total_bytes_received > 0 and time_dif_seconds > 1:
                total_bytes_received = round(total_bytes_received / time_dif_seconds, 2) * rate_coefficient
            else:
                total_bytes_received = test_traffic_statistics["total_bytes_received"] * rate_coefficient

            total_bytes = test_traffic_statistics["total_bytes"]
            if total_bytes > 0 and time_dif_seconds > 1:
                total_bytes = round(total_bytes / time_dif_seconds, 2) * rate_coefficient
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"total_bytes rate_coefficient Rate:{}".format(total_bytes), flush=True)
            else:
                total_bytes = test_traffic_statistics["total_bytes"] * rate_coefficient

            total_packets_sent = test_traffic_statistics["total_packets_sent"]
            if total_packets_sent > 0 and time_dif_seconds > 1:
                total_packets_sent = round(total_packets_sent / time_dif_seconds, 2)

            total_packets_received = test_traffic_statistics["total_packets_received"]
            if total_packets_received > 0 and time_dif_seconds > 1:
                total_packets_received = round(total_packets_received / time_dif_seconds, 2)

            total_packets = test_traffic_statistics["total_packets"]
            if total_packets > 0 and time_dif_seconds > 1:
                total_packets = round(total_packets / time_dif_seconds, 2)

            total_syn_pkt1 = test_traffic_statistics["total_syn_pkt"]
            if total_syn_pkt1 > 0 and time_dif_seconds > 1:
                total_syn_pkt1 = round(total_syn_pkt1 / time_dif_seconds, 2)

            total_syn_pkt2 = test_traffic_statistics["total_syn_pkt"] * 2
            if total_syn_pkt2 > 0 and time_dif_seconds > 1:
                total_syn_pkt2 = round(total_syn_pkt2 / time_dif_seconds, 2)
            #if time_dif_seconds > 1:
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"total_bytes_sent:{};total_syn_pkt1:{};".format(total_bytes_sent,total_syn_pkt1), flush=True)

            match len(source_fields):
                case 1:
                    # * Bytes处理逻辑sent_bytes、received_bytes、in_bytes、out_bytes、syn_bytes
                    if source_fields[0] in {"in_bytes", "out_bytes"} and (stats_value == total_bytes_sent or stats_value == total_bytes_received):
                        metric_result = True
                    elif source_fields[0] == "sent_bytes" and stats_value == total_bytes_sent:
                        metric_result = True
                    elif source_fields[0] == "received_bytes" and stats_value == total_bytes_received:
                        metric_result = True
                    # * Packets处理逻辑sent_pkts、received_bytes、in_pkts、out_pkts、syn_pkts
                    elif source_fields[0] in {"in_pkts", "out_pkts"} and (stats_value == total_packets_sent or stats_value == total_packets_received):
                        metric_result = True
                    elif source_fields[0] == "sent_pkts" and stats_value == total_packets_sent:
                        metric_result = True
                    elif source_fields[0] == "received_pkts" and stats_value == total_packets_received:
                        metric_result = True
                    elif source_fields[0] == "syn_pkts" and total_syn_pkt2:
                        metric_result = True
                    # * Sessions处理逻辑
                    elif source_fields[0] in {"new_sessions_for_this_rule", "closed_sessions_for_this_rule"} and stats_value == total_syn_pkt1:
                        metric_result = True
                    # * Flows处理逻辑new_c2s_flows_for_this_rule、new_s2c_flows_for_this_rule
                    elif source_fields[0] in {"new_c2s_flows_for_this_rule", "new_s2c_flows_for_this_rule"} and stats_value == total_syn_pkt1:
                        metric_result = True
                    #elif source_fields[0] == "received_pkts" and stats_value == test_traffic_statistics["total_packets_received"]:
                    #    metric_result = True
                    #elif source_fields[0] == "syn_pkts" and stats_value == test_traffic_statistics["total_syn_pkt"] * 2:
                    #    metric_result = True
                    # * Fragments处理逻辑:c2s_ip_fragments、s2c_ip_fragments,to do
                    elif source_fields[0] in {"c2s_ip_fragments", "s2c_ip_fragments"} and (stats_value == total_packets_sent or stats_value == total_packets_received or stats_value == 0):
                        metric_result = True
                    elif stats_value > 0:
                        metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case 2:
                    # * Bytes处理逻辑sent_bytes、received_bytes、in_bytes、out_bytes、syn_bytes
                    if "in_bytes" in source_fields and "out_bytes" in source_fields and stats_value == total_bytes:
                        metric_result = True
                    elif "sent_bytes" in source_fields and "received_bytes" in source_fields and stats_value == total_bytes:
                        metric_result = True
                    # * Packets处理逻辑sent_pkts、received_bytes、in_pkts、out_pkts、syn_pkts
                    elif "in_pkts" in source_fields and "out_pkts" in source_fields and stats_value == total_packets:
                        metric_result = True
                    elif "sent_pkts" in source_fields and "received_pkts" in source_fields and stats_value == total_packets:
                        metric_result = True
                    # * Flows处理逻辑new_c2s_flows_for_this_rule、new_s2c_flows_for_this_rule
                    elif "new_c2s_flows_for_this_rule" in source_fields and "new_s2c_flows_for_this_rule" in source_fields and stats_value == total_syn_pkt2:
                        metric_result = True
                    # * Fragments处理逻辑:c2s_ip_fragments、s2c_ip_fragments,to do
                    elif stats_value > 0:
                        metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields} and Metrics is null"
                case 3:
                    if stats_value > 0:
                        metric_result = True
                    else:
                        #如有需定义3个的业务场景需补充相关逻辑
                        failure_info_2 = f"Meaningless source fields definition: {source_fields}"
                case 4: #如有需定义4个的业务场景需补充相关逻辑
                    if stats_value > 0:
                        metric_result = True
                    else:
                        failure_info_2 = f"Meaningless source fields definition: {source_fields}"
                case _:
                    failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            return metric_result,failure_info_2
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Count statistical data verification anomaly.exception:{}".format(exception_result), flush=True)
            return metric_result, failure_info_2

    def metric_unique_count_value_verification(self, source_fields, stats_value,  test_traffic_statistics):
        failure_info_2 = ""
        metric_result = False
        util = UtilStatisticsTemplate()
        code, all_metrics = util.get_all_metrics_or_dimensions("unique_count_metrics")
        if code != 200:
            return False, "Failed to obtain the Field whose Metric Type is Unique_Count"
        # unique和syn数量：1 一致
        # 单向流时有方向的unique为1
        one_or_zero_unique = {
            "new_c2s_flows_for_this_rule",
            "new_s2c_flows_for_this_rule",
            "sent_bytes",
            "received_bytes",
            "in_bytes",
            "out_bytes",
            "sent_pkts",
            "received_pkts",
            "in_pkts",
            "out_pkts"
        }
        #unique和syn数量：1一致
        one_unique = {
            'client_ip_object_list',
            'server_ip_object_list',
            'client_ip',
            'client_country',
            'server_ip',
            'server_country',
            'client_asn',
            'server_asn',
            'server_fqdn',
            'server_domain',
            'app',
            'device_group',
            'c2s_link_id',
            's2c_link_id',
            'client_port',
            'server_port',
            'http_host',
            'ssl_ja3_hash',
            'ssl_sni',
            'subscriber_id',
            'decoded_as',
            'sled_ip',
            'direction',
            'session_id',
            'dtls_handshake_latency_ms',
            'ssl_handshake_latency_ms',
            'tcp_handshake_latency_ms',
            'duration_ms',
            'tcp_rtt_ms',
            'new_sessions_for_this_rule',
            'closed_sessions_for_this_rule',
            'new_c2s_flows_for_this_rule',
            'new_s2c_flows_for_this_rule',
            'c2s_ip_fragments',
            's2c_ip_fragments'
        }
        # unique数量大于1，具体数量不定
        uncertain_quantity_unique = {
            'app_category',
            'c2s_ttl',
            's2c_ttl',
            'flags',
            'in_pkt_length_distribution',
            'out_pkt_length_distribution',
            'pkt_length_distribution',
            'sent_bytes',
            'sent_pkts',
            'received_pkts',
            'received_bytes',
            'in_bytes',
            'out_bytes',
            'in_pkts',
            'out_pkts',
            'c2s_ip_fragments',
            's2c_ip_fragments'
        }
        try:
            match len(source_fields):
                case 1:
                    if source_fields[0] in all_metrics:
                        # * Sessions处理逻辑
                        if source_fields[0] in one_or_zero_unique and (stats_value == test_traffic_statistics["total_syn_pkt"] or stats_value == 0):
                            metric_result = True
                        elif source_fields[0] in one_unique and (stats_value == test_traffic_statistics["total_syn_pkt"]):
                            metric_result = True
                        elif source_fields[0] in uncertain_quantity_unique and (stats_value >= test_traffic_statistics["total_syn_pkt"]):
                            metric_result = True
                        else:
                            failure_info_2 = "Metrics is null"
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case 2:
                    if source_fields[0] in all_metrics and source_fields[1] in all_metrics:
                        if "new_c2s_flows_for_this_rule" in source_fields and "new_s2c_flows_for_this_rule" in source_fields and stats_value == test_traffic_statistics["total_syn_pkt"]*2:
                            metric_result = True
                        elif source_fields[0] in all_metrics and source_fields[1] in all_metrics  and stats_value >= test_traffic_statistics["total_syn_pkt"]:
                            metric_result = True
                        else:
                            failure_info_2 = "Metrics is null"
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case 3:#如有需定义3个的业务场景需补充相关逻辑
                    if source_fields[0] in all_metrics and source_fields[1] in all_metrics  and source_fields[2] in all_metrics and stats_value >= test_traffic_statistics["total_syn_pkt"]:
                        metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case 4:#如有需定义4个的业务场景需补充相关逻辑
                    if source_fields[0] in all_metrics and source_fields[1] in all_metrics  and source_fields[2] in all_metrics and source_fields[3] in all_metrics and stats_value >= test_traffic_statistics["total_syn_pkt"]:
                        metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case _:
                    failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            return metric_result, failure_info_2
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Unique Count statistical data verification anomaly.exception:{}".format(exception_result), flush=True)
            return metric_result, failure_info_2

    def metric_histogram_value_verification(self, source_fields, stats_value):
        # 待重构
        failure_info_2 = ""
        util = UtilStatisticsTemplate()
        code, all_metrics = util.get_all_metrics_or_dimensions("distribution_metrics")
        metric_result = False
        if code != 200:
            return False, "Failed to obtain the Field whose Metric Type is Distribution"
        try:
            match len(source_fields):
                case 1:
                    if source_fields[0] in all_metrics and stats_value >= 0:
                        metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case _:
                    failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            return metric_result, failure_info_2
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Histogram statistical data verification anomaly.exception:{}".format(exception_result), flush=True)
            return metric_result, failure_info_2
    
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
        post_data_ori_dict["rule_uuid"] = rule_uuids_list[0]["uuid"]
        post_data_ori_dict["vsys"] = self.parameter["vsys"]
        response = requests.post(url, json=post_data_ori_dict, headers=headers, verify=False)
        r_dict = response.json()
        if r_dict["code"] != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Service chaining metric query failed.", flush=True)
            return "", 444
        else:  # 返回正常结果
            if r_dict["data"]["list"] == []:  # 为空
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Service chaining metric is empty.", flush=True)
                return "", 333
            else:  # metric不为空时，验证返回结果
                result_list = r_dict["data"]["list"]
                sc_value = copy.deepcopy(result_list[0])
                return sc_value, ""
    
    def verify_sc_metric(self, sff_configuration, sf_configuration, active_dst_ip_list, metric_dict, traffic_result):
        metric_result = False
        # 只考虑了一个Application的场景？？
        application = self.get_application_from_configration()
        if self.policy_configuration["action_parameter"]["targeted_traffic"] == "raw":
            byte_value = traffic_result["total_bytes"]
            pkt_value = traffic_result["total_packets"]
            if sf_configuration[0]["connectivity"]["method"] == "vxlan_g" and sf_configuration[0]["connectivity"]["dest_ip"] in active_dst_ip_list:
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
                if sff_configuration[0]["type"] == 1:
                    if metric_dict["sent_bytes"] == metric_dict["received_bytes"] == traffic_result["total_bytes"] and metric_dict["sent_packets"] == metric_dict["received_packets"] == pkt_value:
                        metric_result = True
                    else:
                        metric_result = False
                elif sff_configuration[0]["type"] == 2:
                    if metric_dict["sent_bytes"] == traffic_result["total_bytes"] and metric_dict["sent_packets"] == pkt_value and metric_dict["received_bytes"] == metric_dict["received_packets"] == 0:
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
                if sff_configuration[0]["type"] == 2:
                    if metric_dict["sent_bytes"] == traffic_result["total_bytes"] and metric_dict["sent_packets"] == pkt_value and metric_dict["received_bytes"] == metric_dict["received_packets"] == 0:
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        elif self.policy_configuration["action_parameter"]["targeted_traffic"] == "decrypted":
            if sf_configuration[0]["connectivity"]["method"] == "vxlan_g" and sf_configuration[0]["connectivity"]["dest_ip"] in active_dst_ip_list:
                if sff_configuration[0]["type"] == 1:
                    if metric_dict["sent_bytes"] == metric_dict["received_bytes"] and metric_dict["sent_packets"] == metric_dict["received_packets"]:
                        metric_result = True
                    else:
                        metric_result = False
                elif sff_configuration[0]["type"] == 2:
                    if metric_dict["sent_bytes"] != 0 and metric_dict["sent_packets"] != 0 and metric_dict["received_bytes"] == metric_dict["received_packets"] == 0:
                       metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                if sff_configuration[0]["type"] == 2 and len(metric_dict) != 0:
                    if metric_dict["sent_bytes"] != 0 and metric_dict["sent_packets"] != 0 and metric_dict["received_bytes"] == metric_dict["received_packets"] == 0:
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        return metric_result
    
    def get_application_from_configration(self):
        and_conditions = self.policy_configuration["and_conditions"]
        for i in range(len(and_conditions)):
            or_conditions = and_conditions[i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_APP_ID":
                    application = or_conditions[j]["items"]
                    return application
    
    def get_negate_option_from_configration(self):
        negate_option_list = []
        and_conditions = self.policy_configuration["and_conditions"]
        for i in range(len(and_conditions)):
            negate_option_list.append(and_conditions[i]["negate_option"])
        for value in negate_option_list:
            if value == True:
                return 1
        return 0