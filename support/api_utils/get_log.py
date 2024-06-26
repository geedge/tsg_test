#!/usr/bin/python3
# coding=utf-8
import copy
import time
import requests
import json
import ipaddress


class GetLog():
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

    def get_log_by_condition(self, token, rule_num, start_time, end_time, test_pc_ip, create_policies_ids, test_data,
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
                log_filter = f"subscriber_id= 'test23' AND has({log_query_rule_type},{policy_id})"
                log_condition_dict['filter'] = log_filter
            else:
                log_filter = f"client_ip={test_pc_ip} AND has({log_query_rule_type},{policy_id})"
                log_condition_dict['filter'] = log_filter
                log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={test_pc_ip}",
                                                                                    f"client_ip='{test_pc_ip}'")
            url = api_host + "/v1/log/query"
            print("Begin to query log by condition.")
            response = requests.post(url, headers=headers, json=log_condition_dict, verify=False)
            assert response.status_code == 200
            log_list = json.loads(response.text)
            log_list = log_list['data']['result']
            log_index = i + 1
            log_query_params = test_data['log_query_param_' + str(log_index)]
            print("Compare log with test data.")
            if len(log_list) > 0 and len(log_query_params) > 0:
                for log in log_list:
                    for log_query_param in log_query_params:
                        query_field_key = log_query_param['query_field_key']
                        query_value = log_query_param['query_value']
                        if query_field_key in log and log[query_field_key] == query_value:
                            log_reult = True
                        else:
                            log_reult = False
            elif len(log_list) == 0:
                log_reult = None
        return log_reult

    def get_metric(self, token, rule_num, start_time, end_time, create_policies_ids, test_data, api_host, vsys_id):
        # 请求接口查询metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/log/query"
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
            print("Begin to query metric by condition.")
            response = requests.post(url, headers=headers, json=hit_query_condition, verify=False)
            assert response.status_code == 200
            response = json.loads(response.text)
            index = i + 1
            counter = test_data['counters_' + str(index)]
            result_len = len(response['data']['result'])
            print("Compare metric with test data.")
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
                                 trex_ip_info, test_data, host_api, vsys_id, alignment_period="PT1S"):
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
        # print("statistics metric result data：")
        # print(r_dict)
        print("Get the metric information of rule id {}".format(statistics_info["rule_id"]))
        if r_dict["code"] != 200:
            print("statistics metric query failed.")
            return [333, "The statistics metric API query failed. Procedure"]
        else:  # 返回正常结果
            if r_dict["data"]["result"] == []:  # 为空
                # 对应session方式和fqdn category需要另行处理
                try:
                    metrics_columns = test_data["profile_condition_1"][0]["chart_list"][0]["metrics"][0][
                        "source_columns"].lower()
                    dimension_columns = \
                    test_data["profile_condition_1"][0]["chart_list"][0]["dimensions"][0]["source_columns"][0].lower()
                except:
                    dimension_columns = "no_dimensions"

                if dimension_columns == "no_dimensions":
                    # API和UI因数据格式不一致，所以API方式获取不到按UI方式获取
                    try:
                        metrics_columns = \
                        test_data["action_parameter"]["statistics_template"][0]["charts"][0]["metrics"][0].split(":")[0].lower()
                        dimension_columns = \
                        test_data["action_parameter"]["statistics_template"][0]["charts"][0]["dimensions"][0]
                    except Exception as e:
                        print("Error: ", e)
                        dimension_columns = "no_dimensions"
                if metrics_columns == "new_in_sessions" or metrics_columns == "new_out_sessions" or dimension_columns == "fqdn_category":
                    return [333, "passthrough"]
                else:
                    print("Do not query statistics metric result")
                return [333, "statistics metric no result was found"]
            else:  # 提取结果，并断言
                metric_result = False  # 默认
                result_list_source = r_dict["data"]["result"]
                result_list = []
                for _ in copy.deepcopy(result_list_source):  # 将key转成小写，  ***且将key中空格替换为下划线****
                    tmp_dict = {}
                    for k, v in _.items():
                        k_0 = "_".join(k.lower().split())  # 将key变为小写且使用下划线连接
                        tmp_dict[k_0] = v
                    result_list.append(tmp_dict)
                statistics_value = 0
                if statistics_info["chart_type"] == "line" or statistics_info["chart_type"] == "table" or \
                        statistics_info["chart_type"] == "bar":
                    # print(f'{statistics_info["chart_type"]}>>断言对比...')
                    histogram_sketch_line_flag = False
                    histogram_sketch_temp ={"in_latency_ms_sketch","out_latency_ms_sketch","latency_ms_sketch",
                                  "in_pkt_length_sketch","out_pkt_length_sketch","pkt_length_sketch"}
                    if statistics_info["chart_type"] == "line":
                        for histogram_sketch in histogram_sketch_temp:
                            if histogram_sketch in result_list[0].keys():
                                histogram_sketch_line_flag = True
                                break
                    if histogram_sketch_line_flag:
                        print("The histogram Metrics Line does not statistic the results.")
                        metric_results = [True, ""]
                    else:
                        # print(statistics_info)
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
                                if "client_ip_sketch".lower() in result_list[
                                    0].keys() or "server_ip_ip_sketch".lower() in result_list[
                                    0].keys() or "fqdn_category".lower() in result_list[0].keys():
                                    break
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
                        print("The actual query result data from TSG: \n{}".format(statistics_value))
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
                                          'webSketch_categories': 'WebSketch Categories',
                                          'client_ip_matched_objects': 'Client IP Matched Objects',
                                          'server_ip_matched_objects': 'Server IP Matched Objects','c2s_ttl': 'C2S TTL',
                                          's2c_ttl': 'S2C TTL',
                                          'c2s_link_id': 'C2S Link ID', 's2c_link_id': 'S2C Link ID',
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
                        for i in range(len(assert_key_list)):
                            metric_results = self.assert_livechart_statistics(statistics_info["chart_type"],
                                                                              assert_key_list[i], statistics_value,
                                                                              statistics_metircs_except,
                                                                              trex_ip_info)  # 判断正确调用函数
                            metric_result = metric_results[0]
                            if metric_result == False:
                                print("Failure on assertion, the assertion is: {}".format(assert_key_list[i]))
                                break
                elif statistics_info["chart_type"] == "histogram":
                    print("The histogram does not statistic the results.")
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
            print(f"Total number of expected results for traffic replay: \n{statistics_metircs_except}")
            failure_info_1 = f"Total expected results for traffic playback:{statistics_metircs_except}"
            statistics_metircs_except_avg = {}  # 重组预期1秒粒度结果
            for k, v in statistics_metircs_except.items():
                if "bytes" in k:
                    statistics_metircs_except_avg[k] = int((v) / 1)  # 统计平均字节数
                else:
                    statistics_metircs_except_avg[k] = int(v / 1)
            if assert_key != "session_identifier_sketch" and assert_key != "client_ip_sketch" and assert_key != "server_ip_sketch":  # 除了这几个gauge，需要打印下信息
                print(f"Average number of traffic playback in 1 second granularity: \n{statistics_metircs_except_avg}")
            failure_info_2 = f"Average number of traffic playback in 1-second granularity: {statistics_metircs_except_avg}"
            print(assert_key)
            if assert_key == "bytes":
                if statistics_value[assert_key] > (
                        statistics_metircs_except_avg["total_bytes"] - 10):  # 预期值减10，因为出现多个时间周期统计的结果实际值减小
                    print(success_result)
                    metric_result = True
            elif assert_key == "in_bytes" or assert_key == "out_bytes":# or assert_key == "incoming_bytes" or assert_key == "outgoing_bytes":
                print(assert_key)
                if (statistics_value[assert_key] > (statistics_metircs_except_avg["total_bytes_sent"] - 10)) or (
                        statistics_value[assert_key] > (statistics_metircs_except_avg["total_bytes_received"] - 10)):
                    print(success_result)
                    metric_result = True
            elif assert_key == "pkts":
                if statistics_value[assert_key] == (statistics_metircs_except_avg["total_packets"]):  # 预期值减10，因为出现多个时间周期统计的结果实际值减小
                    print(success_result)
                    metric_result = True
            elif assert_key == "in_pkts" or assert_key == "out_pkts":# or assert_key == "incoming_packets" or assert_key == "outgoing_packets":
                print(assert_key)
                if (statistics_value[assert_key] == (statistics_metircs_except_avg["total_packets_sent"])) or (
                        statistics_value[assert_key] == (statistics_metircs_except_avg["total_packets_received"])):
                    print(success_result)
                    metric_result = True
            elif assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions" or assert_key == "new_in_sessions" or assert_key == "new_out_sessions" or assert_key == "syn_pkts":# or assert_key == "new_incoming_sessions" or assert_key == "new_outgoing_sessions":
                if assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions":  # 双向流，两个方向都是一样的
                    if statistics_value[assert_key] == statistics_metircs_except_avg["total_syn_pkt"]:
                        print(success_result)
                        metric_result = True
                elif assert_key == "syn_pkts":
                    if statistics_value[assert_key] == (statistics_metircs_except_avg["total_syn_pkt"] * 2):
                        print(success_result)
                        metric_result = True
                elif assert_key == "new_in_sessions" or assert_key == "new_out_sessions":# or assert_key == "new_incoming_sessions" or assert_key == "new_outgoing_sessions":  # 区分方向
                    if statistics_value[assert_key] == statistics_metircs_except_avg["total_syn_pkt"] or \
                            statistics_value[assert_key] == 0:
                        print(success_result)
                        metric_result = True
            elif assert_key == "session_identifier_sketch" or assert_key == "client_ip_sketch" or assert_key == "server_ip_sketch":# or assert_key == "session_ids" or assert_key == "client_ips" or assert_key == "server_ips":
                statistics_metircs_except_gauge = {}
                for k, v in statistics_metircs_except.items():
                    statistics_metircs_except_gauge["session_identifier_sketch"] = statistics_metircs_except["total_syn_pkt"]
                    #statistics_metircs_except_gauge["session_ids"] = statistics_metircs_except["total_syn_pkt"]
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
                    #statistics_metircs_except_gauge["client_ips"] = unique_client_ips
                    #statistics_metircs_except_gauge["server_ips"] = unique_server_ips
                    print(f"Gauge of traffic playback in 1-second granularity: \n{statistics_metircs_except_gauge}")
                    if -3 < statistics_value[assert_key] - statistics_metircs_except_gauge[assert_key] < 3:
                        print("Statistics result normal.")
                        metric_result = True
            else:
                print(f"Key for missing assertion: {assert_key}")
                metric_result = False
        elif chart_type == "histogram":
            metric_result = True
        else:  # table bar等二维图表
            print(f"Total number of traffic replay: \n{statistics_metircs_except}")
            failure_info_1 = f"Total expected results for traffic replay:{statistics_metircs_except}"
            if assert_key == "bytes":
                # Metrics Aggregate影响核对值，临时if方式，后期优化传如Metrics Aggregate Map进行比对判断
                if statistics_value[assert_key] == statistics_metircs_except["total_bytes"] or statistics_value[
                    assert_key] == statistics_metircs_except["total_bytes"] * 8:
                    print(success_result)
                    metric_result = True
            elif assert_key == "in_bytes" or assert_key == "out_bytes":# or assert_key == "incoming_bytes" or assert_key == "outgoing_bytes":
                if (statistics_value[assert_key] == statistics_metircs_except["total_bytes_sent"]) or (
                        statistics_value[assert_key] == statistics_metircs_except["total_bytes_received"]
                        or statistics_value[assert_key] == statistics_metircs_except["total_bytes_sent"] * 8) or (
                        statistics_value[assert_key] == statistics_metircs_except["total_bytes_received"] * 8):
                    print(success_result)
                    metric_result = True
            elif assert_key == "pkts":
                if statistics_value[assert_key] == statistics_metircs_except["total_packets"]:
                    print(success_result)
                    metric_result = True
            elif assert_key == "in_pkts" or assert_key == "out_pkts":# or assert_key == "incoming_packets" or assert_key == "outgoing_packets":
                if (statistics_value[assert_key] == statistics_metircs_except["total_packets_sent"]) or (
                        statistics_value[assert_key] == statistics_metircs_except["total_packets_received"]):
                    print(success_result)
                    metric_result = True
            elif assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions" or assert_key == "new_in_sessions" or assert_key == "new_out_sessions" or assert_key == "syn_pkts":# or assert_key == "new_incoming_sessions" or assert_key == "new_outgoing_sessions":
                if assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions":  # 双向流，两个方向都是一样的
                    if statistics_value[assert_key] == statistics_metircs_except["total_syn_pkt"]:
                        print(success_result)
                        metric_result = True
                elif assert_key == "syn_pkts":
                    if statistics_value[assert_key] == (statistics_metircs_except["total_syn_pkt"] * 2):
                        print(success_result)
                        metric_result = True
                elif assert_key == "new_in_sessions" or assert_key == "new_out_sessions":# or assert_key == "new_incoming_sessions" or assert_key == "new_outgoing_sessions":  # 区分方向
                    if statistics_value[assert_key] == statistics_metircs_except["total_syn_pkt"] or statistics_value[
                        assert_key] == 0:
                        print(success_result)
                        metric_result = True
            else:
                print(f"Key for missing assertion: {assert_key}")
                failure_info_3 = f"key for missing assertions:{assert_key}"
                metric_result = False
        if metric_result == False:
            print(failure_reason)
            actual_result = "Total actual results: {statistics_value}"
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
            print("Service chaining metric query failed.")
            return 444
        else:  # 返回正常结果
            if r_dict["data"]["result"] == []:  # 为空
                print("Service chaining metric is empty.")
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
            lost_pkt = 3
            lost_byte = 192  # tcp三次握手的三个包的字节数和
            if sc_info["sf_method"] == "vxlan_g" and sc_info["sf_dest_ip"] in active_dest_ips_list:
                if sc_info["app_name_1"]:
                    pkt_value -= lost_pkt
                    byte_value -= lost_byte
                sc_expected_metric["total_bytes"] = byte_value + 50 * pkt_value
                if sc_info["type"] == 1:
                    if sc_value["sent_bytes"] == sc_value["received_bytes"] == sc_expected_metric["total_bytes"] and \
                            sc_value["sent_packets"] == sc_value["received_packets"] == pkt_value:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                elif sc_info["type"] == 2:
                    if sc_value["sent_bytes"] == sc_expected_metric["total_bytes"] and sc_value[
                        "sent_packets"] == pkt_value and sc_value["received_bytes"] == sc_value[
                        "received_packets"] == 0:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sc_info["sf_method"] == "layer2_switch":
                if sc_info["app_name_1"]:
                    pkt_value -= lost_pkt
                    byte_value -= lost_byte
                sc_expected_metric["total_bytes"] = byte_value + 4 * pkt_value
                if sc_info["type"] == 2:
                    if sc_value["sent_bytes"] == sc_expected_metric["total_bytes"] and sc_value[
                        "sent_packets"] == pkt_value and sc_value["received_bytes"] == sc_value[
                        "received_packets"] == 0:
                        print(success_result)
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
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                elif sc_info["type"] == 2:
                    if sc_value["sent_bytes"] != 0 and sc_value["sent_packets"] != 0 and sc_value["received_bytes"] == \
                            sc_value["received_packets"] == 0:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sc_info["sf_method"] == "layer2_switch":
                if sc_info["type"] == 2 and len(sc_value) != 0:
                    if sc_value["sent_bytes"] != 0 and sc_value["sent_packets"] != 0 and sc_value["received_bytes"] == \
                            sc_value["received_packets"] == 0:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        if metric_result == False:
            print(failure_reason)
        return metric_result

    def diff_ip_count(self, start_ip, end_ip):
        start_ip_obj = ipaddress.IPv4Address(start_ip)
        end_ip_obj = ipaddress.IPv4Address(end_ip)
        ip_count = int(end_ip_obj) - int(start_ip_obj) + 1
        return ip_count


if __name__ == '__main__':
    print("test")