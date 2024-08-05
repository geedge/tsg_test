#!/usr/bin/python3
# coding=utf-8
import copy
import inspect
import time
import requests
import json
import ipaddress
from datetime import datetime

class GetLog:
    def get_log_schema(self, token, log_type, api_host, vsys_id):
        # 修改完成后删除注释：将下方的security_event替换成变量
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/log/schema/" + log_type + "?vsys_id=" + str(vsys_id)
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200
        log_schema = json.loads(response.text)
        log_schema = log_schema['data']['fields']
        log_schema = ",".join([field['name'] for field in log_schema])
        return log_schema

    def get_log_by_condition(self, token, rule_num, start_time, end_time, test_pc_ip, test_sub_id, create_policies_ids, test_data,
                             api_host, vsys_id, script_type):
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
        policy_type = test_data["policy_type"]
        # 多次循环
        for i in range(rule_num):
            if policy_type == 'security':
                schema_type = 'security_event'
            elif policy_type == 'pxy_intercept' or policy_type == 'pxy_manipulation':
                schema_type = 'proxy_event'
            elif policy_type == 'monitor':
                schema_type = 'monitor_event'
            policy_id = list(create_policies_ids[i].values())[0]
            fields = self.get_log_schema(token, schema_type, api_host, vsys_id)
            if policy_type == 'security':
                log_source = 'security_event'
                identifier_name = 'security-event-list'
                log_query_rule_type = 'security_rule_list'
            elif policy_type == 'pxy_intercept':
                log_source = 'session_record'
                identifier_name = 'session-record-list'
                log_query_rule_type = 'proxy_rule_list'
            elif policy_type == 'pxy_manipulation':
                log_source = 'proxy_event'
                identifier_name = 'proxy-event-manipulation-list'
                log_query_rule_type = 'proxy_rule_list'
            elif policy_type == 'monitor':
                log_source = 'monitor_event'
                identifier_name = 'monitor-event-list'
                log_query_rule_type = 'monitor_rule_list'
            elif policy_type == 'statistics':
                log_source = 'session_record'
                identifier_name = 'session-record-list'
                log_query_rule_type = 'statistics_rule_list'
            log_condition_dict['columns'] = fields
            log_condition_dict['start_time'] = start_time
            log_condition_dict['end_time'] = end_time
            log_condition_dict['vsys_id'] = vsys_id
            log_condition_dict['source'] = log_source
            log_condition_dict['identifier_name'] = identifier_name
            log_condition_dict['execution_mode'] = 'oneshot'

            # 从conditions中获取object_type判断是否存在subscriberid
            # 加script_type判断条件的原因是：ui全流程test_data中没有obj_condition_1这种形式的数据，这种数据形式是api中
            if script_type == "api" and len(test_data["obj_condition_1"]) > 0 and test_data["obj_condition_1"][0][
                "attribute_name"] == "ATTR_SUBSCRIBER_ID":
                log_filter = f"subscriber_id='{test_sub_id}' AND has({log_query_rule_type},{policy_id})"
                log_condition_dict['filter'] = log_filter
            else:
                log_filter = f"client_ip={test_pc_ip} AND has({log_query_rule_type},{policy_id})"
                log_condition_dict['filter'] = log_filter
                log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={test_pc_ip}",
                                                                                    f"client_ip='{test_pc_ip}'")
            url = api_host + "/v1/log/query"
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to query log by condition.", flush=True)
            response = requests.post(url, headers=headers, json=log_condition_dict, verify=False)
            assert response.status_code == 200
            log_list = json.loads(response.text)
            log_list = log_list['data']['result']
            log_index = i + 1
            if script_type == "ui":
                log_query_params = test_data['log_query_param']
            elif script_type == "api":
                log_query_params = test_data['log_query_param_' + str(log_index)]
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Compare log with test data.", flush=True)
            if len(log_list) > 0 and len(log_query_params) > 0:
                for log in log_list:
                    for log_query_param in log_query_params:
                        query_field_key = log_query_param['query_field_key']
                        query_value = log_query_param['query_value']
                        # 传入值与日志的值相等时验证
                        if query_field_key in log and query_field_key != "packet_capture_file" and log[query_field_key] == query_value:
                            log_reult = True
                        
                        # 验证packet capture
                        elif query_field_key == "packet_capture_file":
                            # 验证开关开启状态
                            if query_value == True:
                                # 查询结果中packet_capture_file长度大于0，走下一步骤
                                if len(log[query_field_key]) > 0:
                                    packet_capture_url = log[query_field_key]
                                    download_parameter = {'url': packet_capture_url, 'exportObj': True}
                                    url = api_host + "/v1/util/download_file" + "?vsys_id=" + str(vsys_id)
                                    response = requests.get(url, headers=headers, params=download_parameter, verify=False)
                                    if response.status_code == 200:
                                        log_reult = True
                                    else:
                                        log_reult = False
                                # 开关开启， packet_capture_file长度小于0，结果失败       
                                else:
                                    log_reult = False
                            # 验证开关关闭状态
                            elif query_value == False:
                                # 查询结果中packet_capture_file不为空，进下一步骤
                                if len(log[query_field_key]) > 0 :
                                    log_reult = False
                                else:
                                    log_reult = True
                        # 传入值不相等，而且非packet capture验证为false
                        else:
                            log_reult = False
            elif len(log_query_params) == 0:
                log_reult = True
            elif len(log_list) == 0:
                log_reult = None
        return log_reult

    def get_metric(self, token, rule_num, start_time, end_time, create_policies_ids, test_data, api_host, vsys_id, script_type):
        # 请求接口查询metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/log/query"
        metric_result = False
        for i in range(rule_num):
            policy_type = test_data["policy_type"]
            if policy_type == 'security':
                dataset_identifier_name = "security-policy-rule-statistics"
            elif policy_type == 'pxy_intercept' or policy_type == 'pxy_manipulation':
                dataset_identifier_name = "proxy-policy-rule-statistics"
            elif policy_type == 'monitor':
                dataset_identifier_name = "monitor-policy-rule-statistics"
            policy_id = list(create_policies_ids[i].values())[0]
            hit_query_condition = {"identifier_name": dataset_identifier_name, "rule_id": "", "start_time": "",
                                   "end_time": "", "vsys_id": 1, "execution_mode": "oneshot", "output_mode": "json",
                                   "interval": 1}
            hit_query_condition['rule_id'] = policy_id
            hit_query_condition['start_time'] = start_time
            hit_query_condition['end_time'] = end_time
            hit_query_condition['vsys_id'] = vsys_id
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to query metric by condition.", flush=True)
            response = requests.post(url, headers=headers, json=hit_query_condition, verify=False)
            assert response.status_code == 200
            response = json.loads(response.text)
            index = i + 1
            if script_type == "ui":
                counter = test_data['counters']
            elif script_type == "api":
                counter = test_data['counters_' + str(index)]
            result_len = len(response['data']['result'])
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Compare metric with test data.", flush=True)
            # 需要hits == 0时，则验证，验证通过metric置为true
            if 'hits' in counter and counter['hits'] == 0 and result_len == 0:
                metric_result = True
            elif 'hits' in counter and result_len > 0:
                metric = response['data']['result'][0]
                if counter['hits'] == 1:
                    for key, value in counter.items():
                        # 接口返回的统计是否与预期的一致
                        if key not in metric or metric[key] != value:
                            metric_result = False
                        else:
                            metric_result = True
                elif counter['hits'] == 'many':
                    for key, value in counter.items():
                        # 接口返回的统计是否与预期的一致
                        if key not in metric or metric[key] < 1:
                            metric_result = False
                        else:
                            metric_result = True
            else:
                metric_result = None
            return metric_result

    def get_livechart_statistics(self, token, start_time, end_time, statistics_info, statistics_metircs_except,
                                 trex_ip_info, test_data, host_api, vsys_id, script_type, alignment_period="PT1S"):
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
        url = "{}/v1/log/query".format(host_api)
        # 重组请求体数据
        post_data_ori_json = """
        {
            "execution_mode":"oneshot",
            "query_type":"real_time",
            "start_time":"2023-11-24T02:55:40Z",
            "end_time":"2023-11-24T03:00:40Z",
            "alignment_period":"PT15S",
            "sql":"",
            "filter":"",
            "template_id":1051,
            "version":1,
            "chart_id":2705,
            "vsys_id":1,
            "rule_id":274147,
            "duration":1,
            "interval":1,
            "limit":10000,
            "output_mode":"json"
        }
        """
        post_data_ori_dict = json.loads(post_data_ori_json)
        post_data_ori_dict["start_time"] = start_time
        post_data_ori_dict["end_time"] = end_time
        post_data_ori_dict["rule_id"] = statistics_info["rule_id"]
        post_data_ori_dict["template_id"] = statistics_info["template_id"]
        post_data_ori_dict["chart_id"] = statistics_info["chart_id"]
        post_data_ori_dict["version"] = statistics_info["version"]
        post_data_ori_dict["alignment_period"] = alignment_period
        post_data_ori_dict["vsys_id"] = vsys_id
        post_data_ori_dict["sql"] = statistics_info["sql"]
        response = requests.post(url, json=post_data_ori_dict, headers=headers, verify=False)
        # assert response.status_code == 200
        r_dict = response.json()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"statistics metric ：start_time:{},end_time:{},rule_id:{}".format(start_time,end_time,statistics_info["rule_id"]))
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "statistics metric result data：")
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], r_dict)
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get the metric information of rule id {}".format(post_data_ori_dict))
        if r_dict["code"] != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "statistics metric query failed.", flush=True)
            return [333, "The statistics metric API query failed."]
        else:  # 返回正常结果
            if r_dict["data"]["result"] == []:  # 为空
                # 对应session方式和fqdn category需要另行处理
                if script_type == "api":
                    metrics_columns = test_data["profile_condition_1"][0]["chart_list"][0]["metrics"][0][
                        "source_columns"].lower()
                    dimension_columns = \
                    test_data["profile_condition_1"][0]["chart_list"][0]["dimensions"][0]["source_columns"][0].lower()
                elif script_type == "ui":
                    metrics_columns = \
                    test_data["action_parameter"]["statistics_template"][0]["charts"][0]["metrics"][0].split(":")[0].lower()

                    if len(test_data["action_parameter"]["statistics_template"][0]["charts"][0]["dimensions"]) > 0:
                        dimension_columns = \
                        test_data["action_parameter"]["statistics_template"][0]["charts"][0]["dimensions"][0]
                    else:
                        dimension_columns = "No Dimensions!"
                # api返回值为空，不判断方向，直接返回重新查找
                if metrics_columns == "new_in_sessions" or metrics_columns == "new_out_sessions":# or dimension_columns == "fqdn_category":
                    return [333, "this is a pass"]
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do not query statistics metric result.", flush=True)
                return [333, "statistics metric no result was found."]
            else:  # 提取结果，并断言
                metric_result = False  # 默认
                result_list_source = r_dict["data"]["result"]
                result_list = []
                if "metrics_dimension" in statistics_info.keys(): #ui操作
                    metrics_len = len(statistics_info["metrics_dimension"]["metrics"])
                    dimensions_len = len(statistics_info["metrics_dimension"]["dimensions"])
                    tmp_result = {}
                    for _ in copy.deepcopy(result_list_source):  # 将key转成小写，  ***且将key中空格替换为下划线****
                        tmp_dict = {}
                        tmp_dict_key = ""
                        for k, v in _.items():
                            if k in statistics_info["metrics_dimension"]["metrics"].keys():
                                if v == None:  # Metric结果返回中包括None值处理
                                    v = 0
                                k_0 = statistics_info["metrics_dimension"]["metrics"][k]  # 将key变为小写且使用下划线连接
                                # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并
                                if statistics_info["chart_type"] == "line" and metrics_len == 1 and dimensions_len == 1:
                                    if tmp_dict_key == "":
                                        tmp_dict_key = f"{k_0}"
                                    else:
                                        tmp_dict_key = f"{tmp_dict_key};{k_0}"
                                    if len(tmp_result) > 0 and tmp_dict_key in tmp_result.keys():
                                        tmp_v = tmp_result[tmp_dict_key] + v
                                        tmp_result[tmp_dict_key] = tmp_v
                                    else:
                                        tmp_result[tmp_dict_key] = v
                            elif k in statistics_info["metrics_dimension"]["dimensions"].keys():
                                k_0 = statistics_info["metrics_dimension"]["dimensions"][k]
                                # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并
                                if statistics_info["chart_type"] == "line" and metrics_len == 1 and dimensions_len == 1:
                                    if tmp_dict_key == "":
                                        tmp_dict_key = f"{k_0};{v}"
                                    else:
                                        tmp_dict_key = f"{tmp_dict_key};{k_0}"
                            else:
                                continue
                                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The interface query chart results{} are inconsistent with the user-defined data{}{}".format(k,statistics_info["metrics_dimension"]["metrics"].keys(),statistics_info["metrics_dimension"]["dimensions"].keys()), flush=True)
                                #throw Exception e
                            if (statistics_info["chart_type"] == "line" and metrics_len == 1 and dimensions_len == 1) == False:
                                tmp_dict[k_0] = v
                        # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并
                        if len(tmp_dict) > 0:
                            result_list.append(tmp_dict)
                    if statistics_info["chart_type"] == "line" and metrics_len == 1 and dimensions_len == 1:
                        for key in tmp_result.keys():
                            tmp_dict = {}
                            key_list = key.split(";")
                            if len(key_list) == 3:
                                tmp_dict[key_list[0]] = key_list[1]
                                tmp_dict[key_list[2]] = tmp_result[key]
                                result_list.append(tmp_dict)
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"The Metrics results:{}.".format(result_list), flush=True)
                else:
                    for _ in copy.deepcopy(result_list_source):  # 将key转成小写，  ***且将key中空格替换为下划线****
                        tmp_dict = {}
                        for k, v in _.items():
                            k_0 = "_".join(k.lower().split())  # 将key变为小写且使用下划线连接
                            tmp_dict[k_0] = v
                        result_list.append(tmp_dict)
                statistics_value = 0
                if statistics_info["chart_type"] == "line" or statistics_info["chart_type"] == "table" or \
                        statistics_info["chart_type"] == "bar":
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f'{statistics_info["chart_type"]}>>断言对比...')
                    histogram_sketch_line_flag = False
                    histogram_sketch_temp ={"in_latency_ms_sketch","out_latency_ms_sketch","latency_ms_sketch",
                                  "in_pkt_length_sketch","out_pkt_length_sketch","pkt_length_sketch"}
                    if statistics_info["chart_type"] == "line":
                        for histogram_sketch in histogram_sketch_temp:
                            if histogram_sketch in result_list[0].keys():
                                histogram_sketch_line_flag = True
                                break
                    if histogram_sketch_line_flag:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The histogram Metrics Line does not statistic the results.", flush=True)
                        metric_results = [True, ""]
                    else:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], statistics_info)
                        statistics_value = copy.deepcopy(result_list[0])
                        # 将列表中metric值设置为0
                        for k, v in statistics_value.items():
                            if isinstance(v, int):
                                statistics_value[k] = 0
                        # 遍历result结果，将metric值累加并存储到statistics_value;因为流量单一，只能统计第一个计算值
                        tmp_list_1 = []  # 下面for..提取值使用
                        for result_index in range(len(result_list)):
                            if "session_identifier_sketch" in result_list[0].keys():  # session_identifier_sketch 需要单独处理
                                for k, v in result_list[result_index].items():
                                    if isinstance(v, int):
                                        if v != 0:
                                            tmp_list_1.append(v)  # 将不等于0的数值添加到列表中，为了计算平均数
                            else:  # 其它的取值方式
                                for k, v in result_list[result_index].items():
                                    if isinstance(v, int):
                                        statistics_value[k] += v
                                break_flag = 0     # 默认外层循环累加，累加标志
                                tmp_break_list = ["client_ip_sketch", "server_ip_sketch", "fqdn_category", "client_ip_object", "server_ip_object", "websketch_categories"]   #兼容UI API，所以三组值
                                for item in tmp_break_list:    #遍历判断是否符合上述条件，获取退出累加标志1。"client_ip_sketch", "server_ip_sketch", "fqdn_category"
                                    if item in result_list[0].keys():
                                        break_flag = 1    # 退出外层累加标志
                                        break
                                if break_flag == 1:
                                    break   # 退出累加循环
                        if "session_identifier_sketch" in result_list[0].keys() or "client_ip_sketch" in result_list[
                            0].keys() or "server_ip_sketch" in result_list[0].keys():  # session_identifier_sketch 需要单独处理
                            sum_1 = 0
                            for i in range(1, len(tmp_list_1) - 1):  # 去掉首位两个数计算平均数
                                sum_1 += tmp_list_1[i]
                            avg_1 = 0
                            if sum_1 != 0:
                                avg_1 = sum_1 / (len(tmp_list_1) - 2)
                            for k, v in result_list[0].items():  # 取得session_indentifier_sketch的值
                                if isinstance(v, int):
                                    statistics_value[k] = avg_1
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The actual query result data from TSG: \n{}".format(statistics_value))
                        # 重组需要断言使用的key列表
                        assert_key_list = []
                        dimension_list = {'time': 'Time', 'device_group': 'Device Group', 'client_ip': 'Client IP',
                                          'server_ip': 'Server IP', 'client_asn': 'Client ASN',
                                          'server_asn': 'Server ASN', 'client_country': 'Client Country',
                                          'server_country': 'Server Country',
                                          'server_fqdn': 'Server FQDN', 'server_domain': 'Server Domain',
                                          'application': 'Application',
                                          'fqdn_category': 'WebSketch Categories',
                                          'client_ip_object': 'Client IP Matched Objects',
                                          'server_ip_object': 'Server IP Matched Objects',
                                          'websketch_categories': 'WebSketch Categories',
                                          'client_ip_matched_objects': 'Client IP Matched Objects',
                                          'server_ip_matched_objects': 'Server IP Matched Objects','c2s_ttl': 'Client-to-Server TTL',
                                          's2c_ttl': 'Server-to-Client TTL',
                                          'c2s_link_id': 'Client-to-Server Link ID', 's2c_link_id': 'Server-to-Client Link ID',
                                          'client_port': 'Client Port', 'server_port': 'Server Port'}
                        for k, v in statistics_value.items():
                            # if isinstance(v, int) or isinstance(v, float):
                            #    assert_key_list.append(k)
                            # 如果dimension为端口则为int类型，所以需要过滤掉
                            if k in dimension_list.keys():
                                continue
                            else:
                                assert_key_list.append(k)
                        # 开始判断key的正确性
                        #if "statists_metric_results" in test_data.keys():
                        #    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "statists_metric_results: \n{}".format(test_data["statists_metric_results"]), flush=True)
                        for i in range(len(assert_key_list)):
                            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Determine the correctness of the Key:{}".format(str(assert_key_list)))
                            # 因目前功能端版本：tsg-os-v24.07-rc3-c3f7112只要带有非首包可命中且符合Dimensions的流量均不能全部统计*pkts和*bytes，所以需要从Test_data传入期望统计结果："statists_metric_results":[{'c2s_ttl': 64, 's2c_ttl': 40, 'in_bytes': 1140, 'out_bytes': 93218, 'bytes': 94358}]
                            # 如果有期望值就比对期望值
                            #if "statists_metric_results" in test_data.keys():
                            #    metric_results = self.expected_value_vs_statistics_metric(statistics_info["chart_type"],
                            #                                                             assert_key_list[i],
                            #                                                             statistics_value,
                            #                                                             statistics_metircs_except,
                            #                                                             trex_ip_info,
                            #                                                             test_data["statists_metric_results"])  # 判断正确调用函数
                            #else:
                            metric_results = self.assert_livechart_statistics(statistics_info["chart_type"],
                                                                              assert_key_list[i], statistics_value,
                                                                              statistics_metircs_except,
                                                                              trex_ip_info)  # 判断正确调用函数
                            metric_result = metric_results[0]
                            if metric_result == False:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Failure on assertion, the assertion is: {}".format(assert_key_list[i]), flush=True)
                                break
                            else:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "statistics metric query success.", flush=True)
                elif statistics_info["chart_type"] == "histogram":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The histogram does not statistic the results.", flush=True)
                    metric_results = [True, ""]
                return metric_results

    def assert_livechart_statistics(self, chart_type, assert_key, statistics_value, statistics_metircs_except,
                                    trex_ip_info):
        metric_result = False
        failure_reason = "Result failed."
        success_result = "Result passed."
        failure_reason_info = ""
        failure_info_1 = ""
        failure_info_2 = ""
        failure_info_3 = ""
        if chart_type == "line":
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Total number of expected results for traffic replay: \n{statistics_metircs_except}")
            failure_info_1 = f"Total expected results for traffic playback:{statistics_metircs_except}"
            statistics_metircs_except_avg = {}  # 重组预期1秒粒度结果
            for k, v in statistics_metircs_except.items():
                if "bytes" in k:
                    statistics_metircs_except_avg[k] = int((v) / 1)  # 统计平均字节数
                else:
                    statistics_metircs_except_avg[k] = int(v / 1)
            # if assert_key != "session_identifier_sketch" and assert_key != "client_ip_sketch" and assert_key != "server_ip_sketch":  # 除了这几个gauge，需要打印下信息
            #     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Average number of traffic playback in 1 second granularity: \n{statistics_metircs_except_avg}", flush=True)
            failure_info_2 = f"Average number of traffic playback in 1-second granularity: {statistics_metircs_except_avg}"
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], assert_key)
            if assert_key == "bytes":
                if statistics_value[assert_key] > (
                        statistics_metircs_except_avg["total_bytes"] - 10):  # 预期值减10，因为出现多个时间周期统计的结果实际值减小
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "in_bytes" or assert_key == "out_bytes":
               # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], assert_key)
                if (statistics_value[assert_key] > (statistics_metircs_except_avg["total_bytes_sent"] - 10)) or (
                        statistics_value[assert_key] > (statistics_metircs_except_avg["total_bytes_received"] - 10)):
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "pkts":
                if statistics_value[assert_key] >= (statistics_metircs_except_avg["total_packets"]-10) and statistics_value[assert_key] <= statistics_metircs_except_avg["total_packets"]:  # 预期值减10，因为出现多个时间周期统计的结果实际值减小
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "in_pkts" or assert_key == "out_pkts":
               # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], assert_key)
                if (statistics_value[assert_key] >= (statistics_metircs_except_avg["total_packets_sent"]-10) and statistics_value[assert_key] <= statistics_metircs_except_avg["total_packets_sent"]) or (
                        statistics_value[assert_key] >= (statistics_metircs_except_avg["total_packets_received"]-10) and statistics_value[assert_key] <= statistics_metircs_except_avg["total_packets_received"]):
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions" or assert_key == "new_in_sessions" or assert_key == "new_out_sessions" or assert_key == "syn_pkts":
                if assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions":  # 双向流，两个方向都是一样的
                    if statistics_value[assert_key] == statistics_metircs_except_avg["total_syn_pkt"]:
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                elif assert_key == "syn_pkts":
                    if statistics_value[assert_key] == (statistics_metircs_except_avg["total_syn_pkt"] * 2):
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                elif assert_key == "new_in_sessions" or assert_key == "new_out_sessions":# 区分方向
                    if statistics_value[assert_key] == statistics_metircs_except_avg["total_syn_pkt"] or \
                            statistics_value[assert_key] == 0:
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
            elif assert_key == "session_identifier_sketch" or assert_key == "client_ip_sketch" or assert_key == "server_ip_sketch":
                statistics_metircs_except_gauge = {}
                for k, v in statistics_metircs_except.items():
                    statistics_metircs_except_gauge["session_identifier_sketch"] = statistics_metircs_except["total_syn_pkt"]
                    # 计算ip个数,分析gauge的预期结果 active_sessions  unique_client_ips  unique_server_ips
                    unique_client_ips = self.diff_ip_count(trex_ip_info["clients_start"], trex_ip_info["clients_end"])
                    unique_server_ips = self.diff_ip_count(trex_ip_info["servers_start"], trex_ip_info["servers_end"])
                    sessions_count = statistics_metircs_except["total_syn_pkt"]
                    if sessions_count < unique_client_ips:
                        unique_client_ips = sessions_count
                    if sessions_count < unique_server_ips:
                        unique_server_ips = sessions_count
                    statistics_metircs_except_gauge["client_ip_sketch"] = unique_client_ips
                    statistics_metircs_except_gauge["server_ip_sketch"] = unique_server_ips
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Gauge of traffic playback in 1-second granularity: \n{statistics_metircs_except_gauge}")
                    if -3 < statistics_value[assert_key] - statistics_metircs_except_gauge[assert_key] < 3:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Statistics result normal.", flush=True)
                        metric_result = True
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Key for missing assertion: {assert_key}", flush=True)
                metric_result = False
        elif chart_type == "histogram":
            metric_result = True
        else:  # table bar等二维图表
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Total number of traffic replay: \n{statistics_metircs_except}")
            failure_info_1 = f"Total expected results for traffic replay:{statistics_metircs_except}"
            if assert_key == "bytes":
                # Metrics Aggregate影响核对值，临时if方式，后期优化传如Metrics Aggregate Map进行比对判断
                if statistics_value[assert_key] == statistics_metircs_except["total_bytes"] or statistics_value[
                    assert_key] == statistics_metircs_except["total_bytes"] * 8:
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "in_bytes" or assert_key == "out_bytes":
                if (statistics_value[assert_key] == statistics_metircs_except["total_bytes_sent"]) or (
                        statistics_value[assert_key] == statistics_metircs_except["total_bytes_received"]
                        or statistics_value[assert_key] == statistics_metircs_except["total_bytes_sent"] * 8) or (
                        statistics_value[assert_key] == statistics_metircs_except["total_bytes_received"] * 8):
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "pkts":
                if statistics_value[assert_key] == statistics_metircs_except["total_packets"]:
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "in_pkts" or assert_key == "out_pkts":
                if (statistics_value[assert_key] == statistics_metircs_except["total_packets_sent"]) or (
                        statistics_value[assert_key] == statistics_metircs_except["total_packets_received"]):
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                    metric_result = True
            elif assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions" or assert_key == "new_in_sessions" or assert_key == "new_out_sessions" or assert_key == "syn_pkts":# or assert_key == "new_incoming_sessions" or assert_key == "new_outgoing_sessions":
                if assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions":  # 双向流，两个方向都是一样的
                    if statistics_value[assert_key] == statistics_metircs_except["total_syn_pkt"]:
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                elif assert_key == "syn_pkts":
                    if statistics_value[assert_key] == (statistics_metircs_except["total_syn_pkt"] * 2):
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                elif assert_key == "new_in_sessions" or assert_key == "new_out_sessions":# 区分方向
                    if statistics_value[assert_key] == statistics_metircs_except["total_syn_pkt"] or statistics_value[
                        assert_key] == 0:
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Key for missing assertion: {assert_key}", flush=True)
                failure_info_3 = f"key for missing assertions:{assert_key}"
                metric_result = False
        if metric_result == False:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], failure_reason)
            actual_result = f"Total actual results: {statistics_value}"
            failure_reason_info = "{}{}{}.{}".format(failure_info_1, failure_info_2, failure_info_3, actual_result)
        return metric_result, failure_reason_info

    def get_sc_metric(self, token, start_time, end_time, sc_info, sc_expected_metric, active_dest_ips_list, host_api,
                      vsys_id):
        # 请求接口查询sc metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = "{}/v1/log/query".format(host_api)
        # 重组请求体数据
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
        post_data_ori_dict["rule_id"] = int(sc_info["rule_id"])
        post_data_ori_dict["vsys_id"] = vsys_id
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

    def assert_sc_metric(self, sc_info, sc_value, sc_expected_metric, active_dest_ips_list):
        metric_result = False
        failure_reason = "Result failed."
        success_result = "Result passed."
        if sc_info["targeted_traffic"] == "raw":
            byte_value = sc_expected_metric["total_bytes"]
            pkt_value = sc_expected_metric["total_packets"]
            if sc_info["sf_method"] == "vxlan_g" and sc_info["sf_dest_ip"] in active_dest_ips_list:
                if len(sc_info["app_name_1"]) > 0 :
                    if sc_info["app_name_1"][0] == "http" or sc_info["app_name_1"][0] == "ssl":
                        lost_pkt = 3
                        lost_byte = 192  # tcp三次握手的三个包的字节数和
                    elif sc_info["app_name_1"][0] == "ftp":
                        lost_pkt = 4
                        lost_byte = 266
                    elif sc_info["app_name_1"][0] == "mail":
                        lost_pkt = 15
                        lost_byte = 1273
                    pkt_value -= lost_pkt
                    byte_value -= lost_byte
                sc_expected_metric["total_bytes"] = byte_value + 50 * pkt_value
                sc_expected_metric["total_packets"] = pkt_value
                if sc_info["type"] == 1:
                    if sc_value["sent_bytes"] == sc_value["received_bytes"] == sc_expected_metric["total_bytes"] and \
                            sc_value["sent_packets"] == sc_value["received_packets"] == pkt_value:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                    else:
                        metric_result = False
                elif sc_info["type"] == 2:
                    if sc_value["sent_bytes"] == sc_expected_metric["total_bytes"] and sc_value[
                        "sent_packets"] == pkt_value and sc_value["received_bytes"] == sc_value[
                        "received_packets"] == 0:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sc_info["sf_method"] == "layer2_switch":
                if len(sc_info["app_name_1"]) > 0 :
                    if sc_info["app_name_1"][0] == "http" or sc_info["app_name_1"][0] == "ssl":
                        lost_pkt = 3
                        lost_byte = 192  # tcp三次握手的三个包的字节数和
                    elif sc_info["app_name_1"][0] == "ftp":
                        lost_pkt = 4
                        lost_byte = 266
                    elif sc_info["app_name_1"][0] == "mail":
                        lost_pkt = 15
                        lost_byte = 1273
                    pkt_value -= lost_pkt
                    byte_value -= lost_byte
                sc_expected_metric["total_bytes"] = byte_value + 4 * pkt_value
                sc_expected_metric["total_packets"] = pkt_value
                if sc_info["type"] == 2:
                    if sc_value["sent_bytes"] == sc_expected_metric["total_bytes"] and sc_value[
                        "sent_packets"] == pkt_value and sc_value["received_bytes"] == sc_value[
                        "received_packets"] == 0:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        elif sc_info["targeted_traffic"] == "decrypted":
            if sc_info["sf_method"] == "vxlan_g" and sc_info["sf_dest_ip"] in active_dest_ips_list:
                if sc_info["type"] == 1:
                    if sc_value["sent_bytes"] == sc_value["received_bytes"] and sc_value["sent_packets"] == sc_value[
                        "received_packets"]:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                    else:
                        metric_result = False
                elif sc_info["type"] == 2:
                    if sc_value["sent_bytes"] != 0 and sc_value["sent_packets"] != 0 and sc_value["received_bytes"] == \
                            sc_value["received_packets"] == 0:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sc_info["sf_method"] == "layer2_switch":
                if sc_info["type"] == 2 and len(sc_value) != 0:
                    if sc_value["sent_bytes"] != 0 and sc_value["sent_packets"] != 0 and sc_value["received_bytes"] == \
                            sc_value["received_packets"] == 0:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        # if metric_result == False:
        #     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], failure_reason)
        return metric_result

    def diff_ip_count(self, start_ip, end_ip):
        start_ip_obj = ipaddress.IPv4Address(start_ip)
        end_ip_obj = ipaddress.IPv4Address(end_ip)
        ip_count = int(end_ip_obj) - int(start_ip_obj) + 1
        return ip_count

    def expected_value_vs_statistics_metric(self, chart_type, assert_key, statistics_value, statistics_metircs_except,
                                    trex_ip_info,statists_metric_results):

        """
        statists_metric_results:Statistics Rule因Condition、Dimensions等影响无法统计到全部流量时期望的统计结果格式如下：
        "statists_metric_results":[{'c2s_ttl': 64, 's2c_ttl': 40, 'in_bytes': 1140, 'out_bytes': 93218, 'bytes': 94358}]
        """
        metric_result = False
        failure_reason_info = ""
        assert_key_in_expected = False
        assert_key_equal_expected = False
        tmp_expected = ""
        failure_reason_info = ""
        failure_info_1 = ""
        failure_info_2 = ""
        failure_info_3 = ""
        try:
            for statists_metric_result in statists_metric_results:
                if assert_key in statists_metric_result.keys():
                    assert_key_in_expected = True
                    tmp_expected = statists_metric_result[assert_key]
                    if statistics_value[assert_key] == tmp_expected:
                        #和原始流量对比需转换，暂未对比，因已经和期望值对比，此处不比较也没有影响 and statists_metric_result[assert_key] <= statistics_metircs_except["total_packets"]:
                        metric_result = True
                        assert_key_equal_expected = True
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"pass：expected_value_vs_statistics_metric",flush=True)
                        break
            if  assert_key_in_expected == False:
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Key:{assert_key} for missing expected: {statists_metric_results}", flush=True)
                failure_info_1 = f"Key:{assert_key} for missing expected: {statists_metric_results}"
                actual_result = f"Total actual results: {statistics_value}"
                failure_reason_info = "{}{}{}.{}".format(failure_info_1, failure_info_2, failure_info_3, actual_result)
                metric_result = False
            elif assert_key_equal_expected == False:
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"statistics_value[{assert_key}]:{statistics_value[assert_key]} is inconsistent with the expected value: {tmp_expected}", flush=True)
                failure_info_2 = f"statistics_value[{assert_key}]:{statistics_value[assert_key]} is inconsistent with the expected value: {tmp_expected}"
                actual_result = f"Total actual results: {statistics_value}"
                failure_reason_info = "{}{}{}.{}".format(failure_info_1, failure_info_2, failure_info_3, actual_result)
                metric_result = False
        except Exception as e:
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
            #      f"get_log.py:Exception occurred in expected_value_vs_statistics_metric:{e}")
            actual_result = f"Total actual results: {statistics_value}"
            failure_info_3 = f"get_log.py:Exception occurred in expected_value_vs_statistics_metric:{e}"
            failure_reason_info = "{}{}{}.{}".format(failure_info_1, failure_info_2, failure_info_3, actual_result)
        finally:
            return metric_result, failure_reason_info

    def get_livechart_statistics_2408(self, token, start_time, end_time, statistics_info, statistics_metircs_except,
                                 trex_ip_info, test_data, host_api, vsys_id, script_type, alignment_period="PT1S"):
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
        url = "{}/v1/log/query".format(host_api)
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
        #"order_by": "\"UNIQUE_COUNT(Server IP Object List)\" DESC",
        post_data_ori_dict = json.loads(post_data_ori_json)
        post_data_ori_dict_dsl = post_data_ori_dict["dsl"]
        post_data_ori_dict_dsl["name"] = "customized-statistics" #该值对Statistics Rule Chart查询来说是固定的所以直接赋值
        post_data_ori_dict_dsl["data_source"] = "statistics_rule" #该值对Statistics Rule Chart查询来说是固定的所以直接赋值
        post_data_ori_dict_dsl["filter"] = "vsys_id in ({}) and rule_id = {} and template_id = {} and chart_id = {} and version = {}".format(vsys_id,statistics_info["rule_id"],statistics_info["template_id"],statistics_info["chart_id"],statistics_info["version"])
        post_data_ori_dict_dsl["custom.statistics.dimensions"] = statistics_info["dimensions"]
        post_data_ori_dict_dsl["custom.statistics.metrics"] = statistics_info["metrics"]
        post_data_ori_dict_dsl["intervals"] = [f"{start_time}/{end_time}"] #如果想传入非UTC时间，携带时区也是可以的2024-07-22T17:38:30+08:00/2024-07-23T17:38:30+08:00
        post_data_ori_dict_dsl["order_by"] = "'{}' DESC".format(statistics_info["order_by"])
        post_data_ori_dict_dsl["limit"] = statistics_info["limit"]
        post_data_ori_dict["dsl"] = post_data_ori_dict_dsl
        post_data_ori_dict["vsys_id"] = vsys_id
        # 请求接口获取Metrics数据
        response = requests.post(url, json=post_data_ori_dict, headers=headers, verify=False)
        r_dict = response.json()
        # 打印获取Metrics相关开始结束时间和Rule ID信息信息，方便后面出错排查问题
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"statistics metric ：start_time:{},end_time:{},rule_id:{}".format(start_time,end_time,statistics_info["rule_id"]))
        if r_dict["code"] != 200:
            self.error_print_function(inspect.currentframe().f_code.co_name, "statistics metric query failed.")
            return [333, "The statistics metric API query failed."]
        else:  # 返回正常结果
            if r_dict["data"]["result"] == []:  # 为空
                # 对应有方向的session方式需要另行处理
                if script_type == "api":
                    metrics_columns = test_data["profile_condition_1"][0]["chart_list"][0]["metrics"][0][
                        "source_columns"].lower()
                    dimension_columns = \
                        test_data["profile_condition_1"][0]["chart_list"][0]["dimensions"][0]["source_columns"][0].lower()
                elif script_type == "ui":
                    metrics_columns = [item["source_fields"] for item in statistics_info["metrics"]]

                    if len(statistics_info["dimensions"]) > 0:
                        dimension_columns = [item["source_fields"] for item in statistics_info["dimensions"]]
                    else:
                        dimension_columns = "No Dimensions!"
                # api返回值为空，不判断方向，直接返回重新查找
                if metrics_columns in {"new_in_sessions","new_out_sessions","closed_in_sessions","closed_out_sessions"}:  # or dimension_columns == "fqdn_category":
                    return [333, "this is a pass"]
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Do not query statistics metric result.", flush=True)
                return [333, "statistics metric no result was found."]
            else:  # 提取结果，并断言
                metric_result = False  # 默认
                result_list_source = r_dict["data"]["result"]
                result_list = []
                if script_type == "ui":
                    metrics_len = len(statistics_info["metrics"])
                    dimensions_len = len(statistics_info["dimensions"]) #time调试时需确认是否处理
                    tmp_result = {}
                    for _ in copy.deepcopy(result_list_source):
                        tmp_dict = {}
                        tmp_dict_key = ""
                        for k, v in _.items():
                            if k in statistics_info["metrics_dimension"]["metrics"].keys():
                                if v == None:  # Metric结果返回中包括None值处理
                                    v = 0
                                #k_0 = statistics_info["metrics_dimension"]["metrics"][k]
                                k_0 = k
                                # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并,所有Line都可以合并
                                if statistics_info["chart_type"] == "line":# and metrics_len == 1 and dimensions_len == 1:
                                    if tmp_dict_key == "":
                                        tmp_dict_key = f"{k_0}"
                                    else:
                                        tmp_dict_key = f"{tmp_dict_key};{k_0}"
                                    if len(tmp_result) > 0 and tmp_dict_key in tmp_result.keys():
                                        tmp_v = tmp_result[tmp_dict_key] + v
                                        tmp_result[tmp_dict_key] = tmp_v
                                    else:
                                        tmp_result[tmp_dict_key] = v
                            elif k in statistics_info["metrics_dimension"]["dimensions"].keys():
                                #k_0 = statistics_info["metrics_dimension"]["dimensions"][k]
                                k_0 = k
                                # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并
                                if statistics_info["chart_type"] == "line" and metrics_len == 1 and dimensions_len == 1 and k != "__time":
                                    if tmp_dict_key == "":
                                        tmp_dict_key = f"{k_0};{v}"
                                    else:
                                        tmp_dict_key = f"{tmp_dict_key};{k_0}"
                            else:
                                continue
                                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The interface query chart results{} are inconsistent with the user-defined data{}{}".format(k,statistics_info["metrics_dimension"]["metrics"].keys(),statistics_info["metrics_dimension"]["dimensions"].keys()), flush=True)
                                # throw Exception e
                            if (statistics_info["chart_type"] == "line" and metrics_len == 1 and dimensions_len == 1) == False:
                                tmp_dict[k_0] = v
                            # 如果是Line图且为1Metrics加Dimensions则同一类型分组合并
                        if len(tmp_dict) > 0:
                            result_list.append(tmp_dict)
                        if statistics_info["chart_type"] == "line" and metrics_len == 1 and dimensions_len == 1:
                            for key in tmp_result.keys():
                                tmp_dict = {}
                                key_list = key.split(";")
                                if len(key_list) == 3:
                                    tmp_dict[key_list[0]] = key_list[1]
                                    tmp_dict[key_list[2]] = tmp_result[key]
                                    result_list.append(tmp_dict)
                else:#api如果使用统一处理方法,API需从Statistics Template API获取数据重新组织和UI一样
                    for _ in copy.deepcopy(result_list_source):  # 将key转成小写，  ***且将key中空格替换为下划线****
                        tmp_dict = {}
                        for k, v in _.items():
                            k_0 = "_".join(k.lower().split())  # 将key变为小写且使用下划线连接
                            tmp_dict[k_0] = v
                        result_list.append(tmp_dict)
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
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"The histogram Metrics Line cannot automatically compare statistical results.", flush=True)
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
                            #tmp_list_1 = []  # 下面for..提取值使用
                            #metrics_columns = [item["source_fields"] for item in statistics_info["metrics"]]
                            #metrics_fields = [item["source_fields"] for item in statistics_info["metrics"]]
                            #dimensions_columns = [item["source_fields"] for item in statistics_info["dimensions"]]
                            #dimensions_fields = [item["source_fields"] for item in statistics_info["dimensions"]]
                            for result_index in range(len(result_list)):
                                # UNIQUE_COUNT、COUNT（SUM、RATE、BITRATE）的直接处理
                                key_tmp = ""
                                for k, v in result_list[result_index].items():
                                    if k in metrics_labels:
                                        statistics_value[k] += v
                                break_flag = 0  # 默认外层循环累加，累加标志，如下面列表不是所有累加值，而是获取其中一个值即可
                                tmp_break_list = ["client_ip_sketch", "server_ip_sketch", "fqdn_category",
                                                  "client_ip_object", "server_ip_object",
                                                  "websketch_categories"]  # 兼容UI API，所以三组值
                                for item in tmp_break_list:  # 遍历判断是否符合上述条件，获取退出累加标志1。"client_ip_sketch", "server_ip_sketch", "fqdn_category"
                                    if item in result_list[0].keys():
                                        break_flag = 1  # 退出外层累加标志
                                        break
                                if break_flag == 1:
                                    break  # 退出累加循环
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"The actual query result data from TSG: \n{}".format(statistics_value))
                        metric_results = self.assert_livechart_statistics_2408(statistics_info, statistics_value, statistics_metircs_except)  # 判断正确调用函数
                elif statistics_info["chart_type"] == "histogram":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Histogram cannot automatically compare statistical results.", flush=True)
                    metric_results = [True, ""]
                return metric_results
    def assert_livechart_statistics_2408(self, statistics_info, statistics_value, statistics_metircs_except):
        chart_type = statistics_info["chart_type"]
        metric_result = False
        failure_reason = "Result failed."
        success_result = "Result passed."
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
                    failure_info_1 = f"Total expected results for traffic replay:{statistics_metircs_except}"
                    match chart_type:
                        case "line":
                            metric_result,failure_info_2 = self.metric_value_verification(assert_key, statistics_metircs_except)
                        case "histogram":
                            metric_result = True
                        case _:
                            metric_result,failure_info_2 = self.metric_value_verification(assert_key,statistics_metircs_except)
                    """
                    if chart_type == "line":
                        metric_result, failure_info_2 = self.metric_value_verification(k, metrics_info[k], v, statistics_metircs_except)
                    elif chart_type == "histogram":
                        metric_result = True
                    else:
                        metric_result, failure_info_2 = self.metric_value_verification(k, metrics_info[k], v, statistics_metircs_except)
                else:
                    continue
                if metric_result == False:
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], failure_reason)
                    actual_result = f"Total actual results: {statistics_value}"
                    failure_reason_info = "{}{}{}.{}".format(failure_info_1, failure_info_2, failure_info_3, actual_result)
                    break
            return metric_result, failure_reason_info
        except Exception as e:
            exception_result = str(e)
            self.error_print_function(inspect.currentframe().f_code.co_name, f"response.status_code:{e}")
            return metric_result, failure_info_2
    def metric_value_verification(self, assert_key, metric_info,stats_value, test_traffic_statistics):
        #metric_info:[{'function': {'name': 'UNIQUE_COUNT'}, 'label': 'UNIQUECOUNT(Client IP)', 'metric_name': 'unique_count_1', 'metric_type': 'unique_count', 'source_fields': ['client_ip']}]
        function_name = metric_info["function"]["name"]
        source_fields_tmp = metric_info["source_fields"]
        metric_result = False
        """
        match function_name:
            case "SUM":
                metric_result, failure_info_2 = self.metric_count_value_verification(source_fields_tmp,stats_value, 1,test_traffic_statistics)
            case "RATE":
                metric_result, failure_info_2= self.metric_count_value_verification(source_fields_tmp,stats_value, 1,test_traffic_statistics)
            case "BITRATE":
                metric_result, failure_info_2 = self.metric_count_value_verification(source_fields_tmp,stats_value, 8, test_traffic_statistics)
            case "UNIQUE_COUNT":
                metric_result, failure_info_2 = self.metric_unique_count_value_verification(source_fields_tmp, stats_value, 1,test_traffic_statistics)
            case _:
                failure_info_2 = f"Invalid function name: {function_name}"
        """
        try:
            if function_name == "SUM":
                metric_result, failure_info_2 = self.metric_count_value_verification(source_fields_tmp,stats_value, 1,test_traffic_statistics)
            elif function_name == "RATE":
                metric_result, failure_info_2= self.metric_count_value_verification(source_fields_tmp,stats_value, 1,test_traffic_statistics)
            elif function_name == "BITRATE":
                metric_result, failure_info_2 = self.metric_count_value_verification(source_fields_tmp,stats_value, 8, test_traffic_statistics)
            elif function_name == "UNIQUE_COUNT":
                metric_result, failure_info_2 = self.metric_unique_count_value_verification(source_fields_tmp,stats_value, 1,test_traffic_statistics)
            elif function_name == "HISTOGRAM":
                metric_result, failure_info_2 = self.metric_histogram_value_verification(source_fields_tmp,stats_value, 1,test_traffic_statistics)
            else:
                failure_info_2 = f"Invalid function name: {function_name}"
            return metric_result,failure_info_2
        except Exception as e:
            exception_result = str(e)
            self.error_print_function(inspect.currentframe().f_code.co_name, f"response.status_code:{e}")
            return metric_result, failure_info_2

    def metric_count_value_verification(self,source_fields, stats_value, rate_coefficient,test_traffic_statistics):
        failure_info_2 = ""
        metric_result = False
        """
        match len(source_fields):
            case 1:
                # * Bytes处理逻辑sent_bytes、received_bytes、in_bytes、out_bytes、syn_bytes
                if source_fields[0] in {"in_bytes", "out_bytes"} and (stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient or stats_value == test_traffic_statistics["total_bytes_received"] * rate_coefficient):
                    metric_result = True
                elif source_fields[0] == "sent_bytes" and stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient:
                    metric_result = True
                elif source_fields[0] == "received_bytes" and stats_value == test_traffic_statistics["total_bytes_received"] * rate_coefficient:
                    metric_result = True
                # * Packets处理逻辑sent_pkts、received_bytes、in_pkts、out_pkts、syn_pkts
                elif source_fields[0] in {"in_pkts", "out_pkts"} and (stats_value == test_traffic_statistics["total_packets_sent"]  or stats_value == test_traffic_statistics["total_packets_received"]):
                    metric_result = True
                elif source_fields[0] == "sent_pkts" and stats_value == test_traffic_statistics["total_packets_sent"]:
                    metric_result = True
                elif source_fields[0] == "received_pkts" and stats_value == test_traffic_statistics["total_packets_received"]:
                    metric_result = True
                elif source_fields[0] == "syn_pkts" and stats_value == test_traffic_statistics["total_syn_pkt"] * 2:
                    metric_result = True
                # * Sessions处理逻辑new_in_sessions、new_out_sessions、closed_in_sessions、closed_out_sessions
                elif source_fields[0] in {"new_in_sessions", "new_out_sessions","closed_in_sessions","closed_out_sessions"} and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                # * Flows处理逻辑new_c2s_flows、new_s2c_flows
                elif source_fields[0] in {"new_c2s_flows", "new_s2c_flows"} and stats_value == test_traffic_statistics["total_packets_sent"]:
                    metric_result = True
                #elif source_fields[0] == "received_pkts" and stats_value == test_traffic_statistics["total_packets_received"]:
                #    metric_result = True
                #elif source_fields[0] == "syn_pkts" and stats_value == test_traffic_statistics["total_syn_pkt"] * 2:
                #    metric_result = True
                # * Fragments处理逻辑：c2s_ip_fragments、s2c_ip_fragments,to do
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            case 2:
                # * Bytes处理逻辑sent_bytes、received_bytes、in_bytes、out_bytes、syn_bytes
                if "in_bytes" in source_fields and "out_bytes" in source_fields and stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient:
                    metric_result = True
                elif "sent_bytes" in source_fields and "received_bytes" in source_fields and stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient:
                    metric_result = True
                # * Packets处理逻辑sent_pkts、received_bytes、in_pkts、out_pkts、syn_pkts
                elif "in_pkts" in source_fields and "out_pkts" in source_fields and stats_value == test_traffic_statistics["total_packets"]:
                    metric_result = True
                elif "sent_pkts" in source_fields and "received_pkts" in source_fields and stats_value == test_traffic_statistics["total_packets"]:
                    metric_result = True
                # * Sessions处理逻辑new_in_sessions、new_out_sessions、closed_in_sessions、closed_out_sessions
                elif (("new_in_sessions" in source_fields and "new_out_sessions" in source_fields) or ("closed_in_sessions" in source_fields and "closed_out_sessions" in source_fields)) and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                # * Flows处理逻辑new_c2s_flows、new_s2c_flows
                elif "new_c2s_flows" in source_fields and "new_s2c_flows" in source_fields and stats_value == test_traffic_statistics["total_packets_sent"]*2:
                    metric_result = True
                # * Fragments处理逻辑：c2s_ip_fragments、s2c_ip_fragments,to do
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            case 3:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            case 4:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            case _:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
        """
        try:
            if len(source_fields) == 1:
                # * Bytes处理逻辑sent_bytes、received_bytes、in_bytes、out_bytes、syn_bytes
                if source_fields[0] in {"in_bytes", "out_bytes"} and (stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient or stats_value == test_traffic_statistics["total_bytes_received"] * rate_coefficient):
                    metric_result = True
                elif source_fields[0] == "sent_bytes" and stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient:
                    metric_result = True
                elif source_fields[0] == "received_bytes" and stats_value == test_traffic_statistics["total_bytes_received"] * rate_coefficient:
                    metric_result = True
                # * Packets处理逻辑sent_pkts、received_bytes、in_pkts、out_pkts、syn_pkts
                elif source_fields[0] in {"in_pkts", "out_pkts"} and (stats_value == test_traffic_statistics["total_packets_sent"]  or stats_value == test_traffic_statistics["total_packets_received"]):
                    metric_result = True
                elif source_fields[0] == "sent_pkts" and stats_value == test_traffic_statistics["total_packets_sent"]:
                    metric_result = True
                elif source_fields[0] == "received_pkts" and stats_value == test_traffic_statistics["total_packets_received"]:
                    metric_result = True
                elif source_fields[0] == "syn_pkts" and stats_value == test_traffic_statistics["total_syn_pkt"] * 2:
                    metric_result = True
                # * Sessions处理逻辑new_in_sessions、new_out_sessions、closed_in_sessions、closed_out_sessions
                elif source_fields[0] in {"new_in_sessions", "new_out_sessions","closed_in_sessions","closed_out_sessions"} and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                # * Flows处理逻辑new_c2s_flows、new_s2c_flows
                elif source_fields[0] in {"new_c2s_flows", "new_s2c_flows"} and stats_value == test_traffic_statistics["total_packets_sent"]:
                    metric_result = True
                #elif source_fields[0] == "received_pkts" and stats_value == test_traffic_statistics["total_packets_received"]:
                #    metric_result = True
                #elif source_fields[0] == "syn_pkts" and stats_value == test_traffic_statistics["total_syn_pkt"] * 2:
                #    metric_result = True
                # * Fragments处理逻辑：c2s_ip_fragments、s2c_ip_fragments,to do
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 2:
                # * Bytes处理逻辑sent_bytes、received_bytes、in_bytes、out_bytes、syn_bytes
                if "in_bytes" in source_fields and "out_bytes" in source_fields and stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient:
                    metric_result = True
                elif "sent_bytes" in source_fields and "received_bytes" in source_fields and stats_value == test_traffic_statistics["total_bytes_sent"] * rate_coefficient:
                    metric_result = True
                # * Packets处理逻辑sent_pkts、received_bytes、in_pkts、out_pkts、syn_pkts
                elif "in_pkts" in source_fields and "out_pkts" in source_fields and stats_value == test_traffic_statistics["total_packets"]:
                    metric_result = True
                elif "sent_pkts" in source_fields and "received_pkts" in source_fields and stats_value == test_traffic_statistics["total_packets"]:
                    metric_result = True
                # * Sessions处理逻辑new_in_sessions、new_out_sessions、closed_in_sessions、closed_out_sessions
                elif (("new_in_sessions" in source_fields and "new_out_sessions" in source_fields) or ("closed_in_sessions" in source_fields and "closed_out_sessions" in source_fields)) and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                # * Flows处理逻辑new_c2s_flows、new_s2c_flows
                elif "new_c2s_flows" in source_fields and "new_s2c_flows" in source_fields and stats_value == test_traffic_statistics["total_packets_sent"]*2:
                    metric_result = True
                # * Fragments处理逻辑：c2s_ip_fragments、s2c_ip_fragments,to do
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 3:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            elif len(source_fields) == 4:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            else:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            return metric_result,failure_info_2
        except Exception as e:
            exception_result = str(e)
            self.error_print_function(inspect.currentframe().f_code.co_name, f"response.status_code:{e}")
            return metric_result, failure_info_2

    def metric_unique_count_value_verification(self,source_fields, stats_value, rate_coefficient,test_traffic_statistics):
        failure_info_2 = ""
        metric_result = False
        all_metrics = {'client_ip_object_list':'Client IP Object List','server_ip_object_list':'Server IP Object List',
                                      'client_ip': 'Client IP','server_ip': 'Server IP',
                                      'in_bytes': 'Incoming Bytes', 'out_bytes': 'Outgoing Bytes',
                                      'bytes': 'Bytes', 'new_c2s_flows': 'New Client-to-Server Flows',
                                      'new_s2c_flows': 'New Server-to-Client Flows', 'sessions': 'Sessions',
                                      'new_in_sessions': 'New Incoming Sessions',
                                      'new_out_sessions': 'New Outgoing Sessions',
                                      'new_unestablished_sessions': 'New Unestablished Sessions',
                                      'in_pkts': 'Incoming Packets',
                                      'out_pkts': 'Outgoing Packets',
                                      'pkts': 'Packets',
                                      'syn_pkts': 'SYN Packets',
                                      'c2s_ip_fragments': 'Client-to-Server IP Fragments',
                                      's2c_ip_fragments': 'Server-to-Client IP Fragments',
                                      'ip_fragments': 'IP Fragments',
                                      'session_identifier_sketch': 'Session IDs', 'client_ip_sketch': 'Client IPs',
                                      'server_ip_sketch': 'Server IPs', 'in_latency_ms_sketch': 'Incoming Latency',
                                      'out_latency_ms_sketch': 'Outgoing Latency', 'latency_ms_sketch': 'Latency',
                                      'in_pkt_length_sketch': 'Incoming Packet Length',
                                      'out_pkt_length_sketch': 'Outgoing Packet Length',
                                      'pkt_length_sketch': 'Packet Length'
                                      }
        """
        match len(source_fields):
            case 1:
                if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            case 2:
                if source_fields[0] in all_metrics and source_fields[1] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            case 3:
                if source_fields[0] in all_metrics and source_fields[1] in all_metrics  and source_fields[2] in all_metrics and source_fields[3] in all_metrics  and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            case 4:
                if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            case _:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
        """
        try:
            if len(source_fields) == 1:
                if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 2:
                if source_fields[0] in all_metrics and source_fields[1] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 3:
                if source_fields[0] in all_metrics and source_fields[1] in all_metrics  and source_fields[2] in all_metrics and source_fields[3] in all_metrics  and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 4:
                if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            else:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            return metric_result,failure_info_2
        except Exception as e:
            exception_result = str(e)
            self.error_print_function(inspect.currentframe().f_code.co_name, f"response.status_code:{e}")
            return metric_result, failure_info_2

    def metric_histogram_value_verification(self,source_fields, stats_value, rate_coefficient,test_traffic_statistics):
        # 待重构
        failure_info_2 = ""
        metric_result = False
        all_metrics = {'client_ip_object_list':'Client IP Object List','server_ip_object_list':'Server IP Object List',
                                      'client_ip': 'Client IP','server_ip': 'Server IP',
                                      'in_bytes': 'Incoming Bytes', 'out_bytes': 'Outgoing Bytes',
                                      'bytes': 'Bytes', 'new_c2s_flows': 'New Client-to-Server Flows',
                                      'new_s2c_flows': 'New Server-to-Client Flows', 'sessions': 'Sessions',
                                      'new_in_sessions': 'New Incoming Sessions',
                                      'new_out_sessions': 'New Outgoing Sessions',
                                      'new_unestablished_sessions': 'New Unestablished Sessions',
                                      'in_pkts': 'Incoming Packets',
                                      'out_pkts': 'Outgoing Packets',
                                      'pkts': 'Packets',
                                      'syn_pkts': 'SYN Packets',
                                      'c2s_ip_fragments': 'Client-to-Server IP Fragments',
                                      's2c_ip_fragments': 'Server-to-Client IP Fragments',
                                      'ip_fragments': 'IP Fragments',
                                      'session_identifier_sketch': 'Session IDs', 'client_ip_sketch': 'Client IPs',
                                      'server_ip_sketch': 'Server IPs', 'in_latency_ms_sketch': 'Incoming Latency',
                                      'out_latency_ms_sketch': 'Outgoing Latency', 'latency_ms_sketch': 'Latency',
                                      'in_pkt_length_sketch': 'Incoming Packet Length',
                                      'out_pkt_length_sketch': 'Outgoing Packet Length',
                                      'pkt_length_sketch': 'Packet Length'
                                      }
        """
                match len(source_fields):
                    case 1:
                        if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                            metric_result = True
                        else:
                            failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                    case 2:
                        if source_fields[0] in all_metrics and source_fields[1] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                            metric_result = True
                        else:
                            failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                    case 3:
                        if source_fields[0] in all_metrics and source_fields[1] in all_metrics  and source_fields[2] in all_metrics and source_fields[3] in all_metrics  and stats_value == test_traffic_statistics["total_syn_pkt"]:
                            metric_result = True
                        else:
                            failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                    case 4:
                        if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                            metric_result = True
                        else:
                            failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                    case _:
                        failure_info_2 = f"Meaningless source fields definition: {source_fields}"
                """
        try:
            if len(source_fields) == 1:
                if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 2:
                if source_fields[0] in all_metrics and source_fields[1] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 3:
                if source_fields[0] in all_metrics and source_fields[1] in all_metrics and source_fields[2] in all_metrics and source_fields[3] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            elif len(source_fields) == 4:
                if source_fields[0] in all_metrics and stats_value == test_traffic_statistics["total_syn_pkt"]:
                    metric_result = True
                else:
                    failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            else:
                failure_info_2 = f"Meaningless source fields definition: {source_fields}"
            return metric_result, failure_info_2
        except Exception as e:
            exception_result = str(e)
            self.error_print_function(inspect.currentframe().f_code.co_name, f"response.status_code:{e}")
            return metric_result, failure_info_2
    def error_print_function(self,function,error):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Class:{self.__class__.__name__},Function:{function}Error: {error}", flush=True)

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")