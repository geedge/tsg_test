#!/usr/bin/python3
# coding=utf-8
import copy
import time
import requests
import json
import ipaddress

class GetLog():    
    def get_log_schema(self, token, log_type, api_host):
        # 修改完成后删除注释：将下方的security_event替换成变量
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/log/schema/" + log_type
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        log_schema = json.loads(response.text)
        log_schema = log_schema['data']['fields']
        log_schema = ",".join([field['name'] for field in log_schema])
        return log_schema
    
    def get_log_by_condition(self, token, ruleNum, start_time, end_time, test_pc_ip, create_policies_ids, condition, api_host, vsys_id):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        log_condition = {
            "page_no": 1,
            "page_size": 20,
            "source": "security_event",
            "fields": None,
            "start_time": "",
            "end_time": "",
            "filter": "",
            "vsys_id": 1
        }
        log_condition_dict = json.loads(json.dumps(log_condition))
        # 多次循环
        for i in range(ruleNum):
            policy_id = list(create_policies_ids[i].values())[0]
            fields = self.get_log_schema(token, "security_event", api_host)
            log_condition_dict['fields'] = fields
            log_condition_dict['start_time'] = start_time
            log_condition_dict['end_time'] = end_time
            log_condition_dict['vsys_id'] = vsys_id
            log_condition_dict['log_type'] = 'security_event'
            # 从conditions中获取object_type判断是否存在subscriberid
            if condition["obj_condition_1"][0]["protocolField"] == "ATTR_SUBSCRIBER_ID":
                log_filter = f"subscriber_id= 'test23' AND has(security_rule_list,{policy_id})"
                log_condition_dict['filter'] = log_filter
            else:
                log_filter = f"client_ip={test_pc_ip} AND has(security_rule_list,{policy_id})"
                log_condition_dict['filter'] = log_filter
                log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={test_pc_ip}", f"client_ip='{test_pc_ip}'")
            url = api_host + "/v1/log/query"
            # print(json.dumps(log_condition_dict))
            response = requests.post(url, headers=headers, json=log_condition_dict)
            assert response.status_code == 200
            log_list = json.loads(response.text)
            # print(log_list)
            log_list = log_list['data']['list']
            log_index = i + 1
            log_query_params = condition['log_query_param_'+str(log_index)]
            if len(log_list) > 0 and len(log_query_params) > 0:
                for log in log_list:
                    for log_query_param in log_query_params:
                        print(log)
                        query_field_key = log_query_param['query_field_key']
                        query_value = log_query_param['query_value']
                        if query_field_key in log and log[query_field_key] == query_value:
                            log_reult = True
                        else:
                            log_reult = False
            elif len(log_list) == 0 and len(log_query_params) > 0:
                log_reult = False
            elif len(log_list) == 0 and len(log_query_params) == 0:
                # 此时代表不需要进行logs模块的校验，可能为security shunt动作或statistics，sc策略等
                log_reult = True
            # 当日志中出现false时，就跳出此循环，多次true才可以将result置为true
            if log_reult == False:
                break
        return log_reult

    def get_metric(self, token, ruleNum, start_time, end_time, create_policies_ids, condition, api_host, vsys_id):
        #请求接口查询metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/metric/query"
        for i in range(ruleNum):
            policy_type = condition['policyType']
            if policy_type == 'tsg_security':
                dataset_identifier_name = "security-policy-rule-statistics"
            elif policy_type == 'pxy_intercept' or policy_type == 'pxy_manipulation':
                dataset_identifier_name = "proxy-policy-rule-statistics"
            policy_id = list(create_policies_ids[i].values())[0]
            hit_query_condition = {"identifier_name":dataset_identifier_name,"rule_id":"","start":"","end":"","vsys_id":1,"exec_mode": "oneshot"}
            hit_query_condition['rule_id'] = f"{policy_id}"
            hit_query_condition['start'] = start_time
            hit_query_condition['end'] = end_time
            hit_query_condition['vsys_id'] = vsys_id
            print(json.dumps(hit_query_condition))
            response = requests.post(url, headers=headers, json=hit_query_condition)
            assert response.status_code == 200
            response = json.loads(response.text)
            index = i + 1
            counter = condition['counters_'+str(index)]
            result_len = len(response['data']['result'])
            # 需要hits == 0时，则验证，验证通过metric置为true
            if 'hits' in counter and counter['hits'] == 0 and result_len == 0:
                metric_result = True
            elif 'hits' in counter and counter['hits'] == 'many' and result_len > 0:
                metric = response['data']['result'][0]
                hits = metric['hits']
                if hits > 0:
                    metric_result = True
                else:
                    metric_result = False
            # 接口有返回值时，对接口的返回内容进行验证
            elif result_len > 0:
                metric = response['data']['result'][0]
                for key,value in counter.items():
                    # 接口返回的统计是否与预期的一致
                    if key not in metric or metric[key] != value:
                        metric_result = False
                    else:
                        metric_result = True
            else:
                metric_result = False
            return metric_result

    def get_livechart_statistics(self, token, start_time, end_time, statistics_info, statistics_metircs_except, trex_ip_info, host_api, vsys_id, time_granularity="PT15S", alignment_period="PT15S"):
        """
        :param token:
        :param start_time:
        :param end_time:
        :param statistics_info:
        :param condition:
        :return:
        """
        # 请求接口查询statistics metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = "{}/v1/metric/query".format(host_api)
        # 重组请求体数据
        post_data_ori_json = """
        {
            "exec_mode":"oneshot",
            "query_type":"real_time",
            "start":"2023-11-24T02:55:40Z",
            "end":"2023-11-24T03:00:40Z",
            "alignment_period":"PT15S",
            "sql":"",
            "filter":"1=1",
            "template_id":1051,
            "version":1,
            "chart_id":2705,
            "vsys_id":1,
            "rule_id":274147
        }
        """
        post_data_ori_dict = json.loads(post_data_ori_json)
        if statistics_info["chart_type"] == "table" or statistics_info["chart_type"]  == "bar":
            dataset_identifier_name = "statistics-rule-table-or-bar-chart-template"
        elif statistics_info["chart_type"]  == "line":
            dataset_identifier_name = "statistics-rule-line-chart-template"
        else:            #  = histogram
            dataset_identifier_name = "statistics-rule-histogram-chart-template"
        post_data_ori_dict["dataset_identifier_name"] = dataset_identifier_name
        post_data_ori_dict["start"] = start_time
        post_data_ori_dict["end"] = end_time
        post_data_ori_dict["rule_id"] = statistics_info["rule_id"]
        post_data_ori_dict["template_id"] = statistics_info["template_id"]
        post_data_ori_dict["chart_id"] = statistics_info["chart_id"]
        post_data_ori_dict["version"] = statistics_info["version"]
        #post_data_ori_dict["time_granularity"] = time_granularity
        post_data_ori_dict["alignment_period"] = alignment_period
        post_data_ori_dict["vsys_id"] = vsys_id
        post_data_ori_dict["sql"] =statistics_info["sql"]
        # print("statistics metric请求体数据：")
        # print(post_data_ori_dict)
        response = requests.post(url, json=post_data_ori_dict, headers=headers)
        #assert response.status_code == 200
        r_dict = response.json()
        print("statistics metric结果数据：")
        print(r_dict)
        if r_dict["code"] != 200:
            print("statistics metric 查询失败")
            return [333, "The statistics metric API query failed. Procedure"]
        else:    # 返回正常结果
            if r_dict["data"]["result"] == []:   # 为空
                print("########statistics metric 没有查询到结果###############")
                return [333, "statistics metric No result was found"]
            else:     # 提取结果，并断言
                metric_result = False  # 默认
                result_list_source = r_dict["data"]["result"]
                #print(result_list_source)
                result_list = []
                for _ in copy.deepcopy(result_list_source):    # 将key转成小写
                    result_list.append({k.lower():v for k, v in _.items()})
                #print(result_list)
                statistics_value = 0
                if statistics_info["chart_type"] == "line" or statistics_info["chart_type"] == "table" or statistics_info["chart_type"] == "bar":
                    print(f'{statistics_info["chart_type"]}断言对比...')
                    print(statistics_info)
                    statistics_value = copy.deepcopy(result_list[0])
                    # 将列表中metric值设置为0
                    for k, v in statistics_value.items():
                        if isinstance(v, int):
                            statistics_value[k] = 0
                    # 遍历result结果，将metric值累加并存储到statistics_value
                    for result_index in range(len(result_list)):
                        for k, v in result_list[result_index].items():
                            if isinstance(v, int):
                                statistics_value[k] += v
                    print("TSG实际查询到的结果数据：\n{}".format(statistics_value))
                    # 重组需要断言使用的key列表
                    assert_key_list = []
                    for k, v in statistics_value.items():
                        if isinstance(v, int):
                            assert_key_list.append(k)
                    # 开始判断key的正确性
                    for i in range(len(assert_key_list)):
                        metric_results = self.assert_livechart_statistics(statistics_info["chart_type"], assert_key_list[i], statistics_value, statistics_metircs_except, trex_ip_info)  # 判断正确调用函数
                        metric_result = metric_results[0]
                        if metric_result == False:
                            print("断言时失败：断言内容为：{}".format(assert_key_list[i]))
                            break
                elif statistics_info["chart_type"] == "histogram":
                    print("histogram图表暂不统计结果")
                    pass
                return metric_results

    def assert_livechart_statistics(self, chart_type, assert_key, statistics_value, statistics_metircs_except, trex_ip_info):
        metric_result = False
        failure_reason = "<<<<<<<<<< 结果失败 >>>>>>>>>>"
        success_result = "<<<<<<<<<< 结果通过 >>>>>>>>>>"
        failure_reason_info = ""
        failure_info_1 = ""
        failure_info_2= ""
        failure_info_3 = ""
        if chart_type == "line":
            print(f"流量回放预期结果总数：\n{statistics_metircs_except}")
            failure_info_1 = f"Total expected results for traffic playback:{statistics_metircs_except}"
            statistics_metircs_except_avg = {}     # 重组预期15秒粒度结果
            for k, v in statistics_metircs_except.items():
                if "bytes" in k:
                    statistics_metircs_except_avg[k] = int((v) / 15)    # 统计平均字节数
                else:
                    statistics_metircs_except_avg[k] = int(v / 15)
            print(f"流量回放结果按15秒粒度平均数：\n{statistics_metircs_except_avg}")
            failure_info_2 = f"Average number of traffic playback results by 15-second granularity:{statistics_metircs_except_avg}"
            print(assert_key)
            if assert_key == "bytes":
                if statistics_value[assert_key] == statistics_metircs_except_avg["total_bytes"]:
                    print(success_result)
                    metric_result = True
            elif assert_key == "in_bytes" or assert_key == "out_bytes":
                print(assert_key)
                if (statistics_value[assert_key] == statistics_metircs_except_avg["total_bytes_sent"]) or (statistics_value[assert_key] == statistics_metircs_except_avg["total_bytes_received"]):
                    print(33)
                    print(success_result)
                    metric_result = True
            elif assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions" or assert_key == "new_in_sessions" or assert_key == "new_out_sessions" or assert_key == "syn_pkts":
                if assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions":  # 双向流，两个方向都是一样的
                    if statistics_value[assert_key] == statistics_metircs_except_avg["total_syn_pkt"]:
                        print(success_result)
                        metric_result = True
                elif assert_key == "syn_pkts":
                    if statistics_value[assert_key] == (statistics_metircs_except_avg["total_syn_pkt"] * 2):
                        print(success_result)
                        metric_result = True
                elif assert_key == "new_in_sessions" or assert_key == "new_out_sessions":  # 区分方向
                    if statistics_value[assert_key] == statistics_metircs_except_avg["total_syn_pkt"] or statistics_value[assert_key] == 0:
                        print(success_result)
                        metric_result = True

            elif assert_key == "session_identifier_sketch" or assert_key == "client_ip_sketch" or assert_key == "server_ip_sketch":
                statistics_metircs_except_gauge = {}
                for k, v in statistics_metircs_except.items():
                    statistics_metircs_except_gauge["session_identifier_sketch"] = statistics_metircs_except["total_syn_pkt"] * 15
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
                    print(f"流量回放结果按15秒粒度的Gauge：\n{statistics_metircs_except_gauge}")
                    if statistics_value[assert_key] == statistics_metircs_except_gauge[assert_key]:
                        print("<<<<<<<<<<statistics 结果正常>>>>>>>>>>")
                        metric_result = True
            else:
                print(f"遗漏断言的key：{assert_key}")
                metric_result = False
        elif chart_type == "histogram":
            pass
        else:    # table bar等二维图表
            print(f"流量回放结果总数：\n{statistics_metircs_except}")
            failure_info_1 = f"Total expected results for traffic playback:{statistics_metircs_except}"
            if assert_key == "bytes":
                if statistics_value[assert_key] == statistics_metircs_except["total_bytes"]:
                    print(success_result)
                    metric_result = True
            elif assert_key == "in_bytes" or assert_key == "out_bytes":
                if (statistics_value[assert_key] == statistics_metircs_except["total_bytes_sent"]) or (statistics_value[assert_key] == statistics_metircs_except["total_bytes_received"]):
                    print(success_result)
                    metric_result = True
            elif assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions" or assert_key == "new_in_sessions" or assert_key == "new_out_sessions" or assert_key == "syn_pkts":
                if assert_key == "new_c2s_flows" or assert_key == "new_s2c_flows" or assert_key == "sessions":    # 双向流，两个方向都是一样的
                    if statistics_value[assert_key] == statistics_metircs_except["total_syn_pkt"]:
                        print(success_result)
                        metric_result = True
                elif assert_key == "syn_pkts":
                    if statistics_value[assert_key] == (statistics_metircs_except["total_syn_pkt"] * 2):
                        print(success_result)
                        metric_result = True
                elif assert_key == "new_in_sessions" or assert_key == "new_out_sessions":    # 区分方向
                    if statistics_value[assert_key] == statistics_metircs_except["total_syn_pkt"] or statistics_value[assert_key] == 0:
                        print(success_result)
                        metric_result = True
            else:
                print(f"遗漏断言的key：{assert_key}")
                failure_info_3 = f"key for missing assertions:{assert_key}"
                metric_result = False
        if metric_result == False:
            print(failure_reason)
            failure_reason_info = "{}{}{}".format(failure_info_1, failure_info_2, failure_info_3)
        return metric_result, failure_reason_info

    def get_sc_metric(self, token, start_time, end_time, sc_info, sc_expected_metric, active_dest_ips_list, host_api):
        # 请求接口查询sc metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = "{}/v1/metric/query".format(host_api)
        # 重组请求体数据
        post_data_ori_json = """
        {
            "identifier_name": "service-chaining-policy-rule-statistics",
            "rule_id": "271039",
            "start": "2023-11-21T03:23:24Z",
            "end": "2023-11-30T07:39:49Z",
            "vsys_id": 1
        }
        """
        # 重组请求体数据
        post_data_ori_dict = json.loads(post_data_ori_json)
        post_data_ori_dict["identifier_name"] = "service-chaining-policy-rule-statistics"
        post_data_ori_dict["start"] = start_time
        post_data_ori_dict["end"] = end_time
        post_data_ori_dict["rule_id"] = sc_info["rule_id"]
        # print("sc metric请求体数据：")
        # print(post_data_ori_dict)
        response = requests.post(url, json=post_data_ori_dict, headers=headers)
        r_dict = response.json()
        print("sc metric结果数据：")
        # print(r_dict)
        if r_dict["code"] != 200:
            print("service chaining metric query failed")
            return 444
        else:    # 返回正常结果
            if r_dict["data"]["result"] == None:   # 为空
                print("########service chaining metric is empty###############")
                return 333
            else:   #metric不为空时，验证返回结果
                metric_result = False  # 默认
                result_list = r_dict["data"]["result"]
                sc_value = copy.deepcopy(result_list[0])
                metric_result = self.assert_sc_metric(sc_info, sc_value, sc_expected_metric, active_dest_ips_list)
        # print(str(metric_result))
        return metric_result

    def assert_sc_metric(self, sc_info, sc_value, sc_expected_metric,active_dest_ips_list):
        metric_result = False
        failure_reason = "<<<<<<<<<<sc 结果失败>>>>>>>>>>"
        success_result = "<<<<<<<<<<sc 结果正常>>>>>>>>>>"
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
                    if sc_value["sent_bytes"] == sc_value["received_bytes"] == sc_expected_metric["total_bytes"] and sc_value["sent_packets"] == sc_value["received_packets"] == pkt_value:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                elif sc_info["type"] == 2:
                    if sc_value["sent_bytes"] == sc_expected_metric["total_bytes"] and sc_value["sent_packets"] == pkt_value and sc_value["received_bytes"] == sc_value["received_packets"] == 0:
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
                    if sc_value["sent_bytes"] == sc_expected_metric["total_bytes"] and sc_value["sent_packets"] == pkt_value and sc_value["received_bytes"] == sc_value["received_packets"] == 0:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
        elif sc_info["targeted_traffic"] == "decrypted":
            if sc_info["sf_method"] == "vxlan_g" and sc_info["sf_dest_ip"] in active_dest_ips_list:
                if sc_info["type"] == 1:
                    if sc_value["sent_bytes"] == sc_value["received_bytes"] and sc_value["sent_packets"] == sc_value["received_packets"]:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                elif sc_info["type"] == 2:
                    if sc_value["sent_bytes"] != 0 and sc_value["sent_packets"] != 0 and sc_value["received_bytes"] == sc_value["received_packets"] == 0:
                        print(success_result)
                        metric_result = True
                    else:
                        metric_result = False
                else:
                    metric_result = False
            elif sc_info["sf_method"] == "layer2_switch":
                if sc_info["type"] == 2 and len(sc_value) != 0:
                    if sc_value["sent_bytes"] != 0 and sc_value["sent_packets"] != 0 and sc_value["received_bytes"] == sc_value["received_packets"] == 0:
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