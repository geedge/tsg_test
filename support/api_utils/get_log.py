#!/usr/bin/python3
# coding=utf-8
import copy
import inspect
import requests
import json
import ipaddress
from datetime import datetime
from support.api_utils.util_statistics_template import UtilStatisticsTemplate

class GetLog:
    def get_log_schema(self, token, log_type, api_host, vsys_id):
        # 修改完成后删除注释:将下方的security_event替换成变量
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/logs/schema/" + log_type
        vsys = {"vsys": vsys_id}
        response = requests.get(url, headers=headers, params=vsys, verify=False)
        assert response.status_code == 200
        log_schema = json.loads(response.text)
        log_schema = log_schema['data']['fields']
        log_schema = ",".join([field['name'] for field in log_schema])
        return log_schema

    def get_log_by_condition(self, token, rule_num, start_time, end_time, test_pc_ip, test_sub_id, create_policies_ids, test_data, api_host, vsys_id, script_type, output):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        log_condition = {
            "page_no": 1,
            "page_size": 20,
            "source": "security_event",
            "columns": None,
            "start_time": "",
            "end_time": "",
            "filter": "",
            "vsys": 1
        }
        log_condition_dict = json.loads(json.dumps(log_condition))
        policy_type = test_data["policy_type"]
        # 多次循环
        for i in range(rule_num):
            if policy_type == 'security':
                schema_type = 'security_event'
            elif policy_type == 'pxy_intercept':
                schema_type = 'session_record'
            elif policy_type == 'pxy_manipulation':
                schema_type = 'proxy_event'
            elif policy_type == 'monitor':
                schema_type = 'monitor_event'
            elif policy_type == 'dos_protection':
                schema_type = 'dos_event'
            policy_id = list(create_policies_ids[i].values())[0]
            fields = self.get_log_schema(token, schema_type, api_host, vsys_id)
            if policy_type == 'security':
                log_source = 'security_event'
                identifier_name = 'security-event-list'
                log_query_rule_type = 'security_rule_uuid_list'
            elif policy_type == 'pxy_intercept':
                log_source = 'session_record'
                identifier_name = 'session-record-list'
                log_query_rule_type = 'proxy_rule_list'
            elif policy_type == 'pxy_manipulation':
                log_source = 'proxy_event'
                identifier_name = 'proxy-event-manipulation-list'
                log_query_rule_type = 'proxy_rule_uuid_list'
            elif policy_type == 'monitor':
                log_source = 'monitor_event'
                identifier_name = 'monitor-event-list'
                log_query_rule_type = 'monitor_rule_uuid_list'
            elif policy_type == 'statistics':
                log_source = 'session_record'
                identifier_name = 'session-record-list'
                log_query_rule_type = 'statistics_rule_uuid_list'
            elif policy_type == "dos_protection":
                log_source = "dos_event"
                identifier_name = "dos-event-list"
            log_condition_dict['columns'] = fields
            log_condition_dict['start_time'] = start_time
            log_condition_dict['end_time'] = end_time
            log_condition_dict['vsys'] = vsys_id
            log_condition_dict['source'] = log_source
            log_condition_dict['identifier_name'] = identifier_name
            log_condition_dict['execution_mode'] = 'oneshot'
            # 从conditions中获取object_type判断是否存在subscriberid
            if "obj_condition_1" in test_data.keys():
                    temp_obj_condition = test_data["obj_condition_1"]
            elif "obj_condition" in test_data.keys():
                temp_obj_condition = test_data["obj_condition"]
            if policy_type == "dos_protection":
                attack_type = "Custom Network Attack"
                log_condition_dict['filter'] = f"destination_ip='{test_data['traffic']['servers_start_ip']}'AND attack_type='{attack_type}'"
            else:
                if script_type == "api" and len(temp_obj_condition) > 0 and temp_obj_condition[0]["attribute_name"] == "ATTR_SUBSCRIBER_ID":
                    log_filter = f"subscriber_id='{test_sub_id}' AND has({log_query_rule_type},'{policy_id}')"
                    log_condition_dict['filter'] = log_filter
                else:
                    log_filter = f"client_ip={test_pc_ip} AND has({log_query_rule_type}, '{policy_id}')"
                    log_condition_dict['filter'] = log_filter
                    log_condition_dict['filter'] = log_condition_dict['filter'].replace(f"client_ip={test_pc_ip}", f"client_ip='{test_pc_ip}'")
            url = api_host + "/v1/logs/query"
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to query log by condition.", flush=True)
            response = requests.post(url, headers=headers, json=log_condition_dict, verify=False)
            assert response.status_code == 200
            log_list = json.loads(response.text)
            log_list = log_list['data']['list']
            log_index = i + 1
            temp_log_query_param = 'log_query_param_' + str(log_index)
            if temp_log_query_param in test_data.keys():
                log_query_params = test_data[temp_log_query_param]
            else:
                log_query_params = test_data['log_query_param']
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Compare log with test data.", flush=True)
            temp_log_result_list = []
            if len(log_list) > 0 and len(log_query_params) > 0:
                time = -1
                for log in log_list:
                    for log_query_param in log_query_params:
                        time += 1
                        query_field_key = log_query_param['query_field_key']
                        query_value = log_query_param['query_value']
                        # 传入值与日志的值相等时验证
                        exclude_fields = {
                            "packet_capture_file", "http_response_body", "http_request_body", "monitor_mirrored_pkts",
                            "monitor_mirrored_bytes", "client_port", "ssl_ech_flag", "ssl_esni_flag",
                            "attack_type", "sessions", "session_rate", "packets", "packet_rate","bytes", "bit_rate",
                            "basic_attack_type", "basic_sessions","basic_session_rate", "basic_packets", "basic_packet_rate","basic_bytes", "basic_bit_rate",
                            "rule_id","conditions"
                        }
                        dos_verify_fields = {
                            "attack_type", "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate",
                            "basic_attack_type", "basic_sessions", "basic_session_rate", "basic_packets","basic_packet_rate", "basic_bytes", "basic_bit_rate",
                            "rule_id","conditions","source_ip_list","destination_ip"
                        }
                        # 优化后的条件判断
                        if query_field_key in log and query_field_key not in exclude_fields and log[query_field_key] == query_value:
                            temp_log_result_list.append(True)
                        # 验证packet capture
                        elif query_field_key in {"packet_capture_file", "http_response_body", "http_request_body"}:
                            # 验证开关开启状态
                            if query_value == True:
                                # 查询结果中packet_capture_file长度大于0，走下一步骤
                                if len(log[query_field_key]) > 0:
                                    packet_capture_url = log[query_field_key]
                                    download_parameter = {'url': packet_capture_url, 'exportObj': True}
                                    url = api_host + "/v1/util/download_file" + "?vsys_id=" + str(vsys_id)
                                    response = requests.get(url, headers=headers, params=download_parameter, verify=False)
                                    if response.status_code == 200:
                                        temp_log_result_list.append(True)
                                    else:
                                        temp_log_result_list.append(False)
                                # 开关开启， packet_capture_file长度小于0，结果失败       
                                else:
                                    temp_log_result_list.append(False)
                            # 验证开关关闭状态
                            elif query_value == False:
                                # 查询结果中packet_capture_file不为空，进下一步骤
                                if len(log[query_field_key]) > 0 :
                                    temp_log_result_list.append(False)
                                else:
                                    temp_log_result_list.append(True)
                        # monitor 验证 "monitor_mirrored_pkts","monitor_mirrored_bytes"
                        elif query_field_key in {"monitor_mirrored_pkts", "monitor_mirrored_bytes"}:
                            actual_bytes_value = output["total_bytes"]
                            actual_pkts_value = output["total_packets"]
                            mirror_bytes_value = 0
                            mirror_pkts_value = 0
                            if "mirror_type" in test_data:
                                if test_data["mirror_type"] in {"ftp", "http", "https", "ssl"}:
                                # ftp:packets28 bytes1926; mail p:1095 1175407
                                    if test_data["mirror_type"] in {"ftp", "http", "https", "ssl"}:
                                        if "protocol_filed" in test_data["condition"]:
                                            protocol_filed = test_data["condition"]["protocol_filed"][0]

                                            # 合并处理 "items" 和 "item" 的逻辑
                                            item_list = protocol_filed.get("items") or protocol_filed.get("item")

                                            if item_list and len(item_list) > 0:
                                                item_type = item_list[0].get("item_type")

                                                if item_type in ["san", "cn"]:
                                                    mirror_bytes_value = actual_bytes_value - 4619
                                                    mirror_pkts_value = actual_pkts_value - 9
                                                elif item_type == "response_header":
                                                    mirror_bytes_value = actual_bytes_value - 381
                                                    mirror_pkts_value = actual_pkts_value - 5
                                                elif item_type == "ftp_account":
                                                    mirror_bytes_value = actual_bytes_value - 266
                                                    mirror_pkts_value = actual_pkts_value - 4
                                                else:
                                                    # 其他protocol field的情况，如ftp account
                                                    mirror_bytes_value = actual_bytes_value - 192
                                                    mirror_pkts_value = actual_pkts_value - 3
                                            else:
                                                #处理其他情况（如 ssl ech、esni、ssl sni）
                                                mirror_bytes_value = actual_bytes_value - 192
                                                mirror_pkts_value = actual_pkts_value - 3
                                        else:
                                            # 处理没有 protocol_filed 的情况
                                            mirror_bytes_value = actual_bytes_value - 192
                                            mirror_pkts_value = actual_pkts_value - 3

                                    if "profile" in test_data and test_data["profile"] != "":
                                        vlan_count = test_data['profile'][0]['vlan_count']
                                        num_vlans = vlan_count
                                        mirror_bytes_value *= num_vlans
                                        mirror_pkts_value *= num_vlans
                                elif test_data["mirror_type"] == "mail":
                                    if "protocol_filed" in test_data["condition"]:
                                        protocol_filed = test_data["condition"]["protocol_filed"][0]

                                        # 如果有 "items" 列表，并且列表不为空
                                        if "items" in protocol_filed and protocol_filed["items"]:
                                            item_type = protocol_filed["items"][0].get("item_type", "")
                                            # if item_type in ["mail_from", "mail_to"]:
                                            if item_type in ["mail_from", "to"]:
                                                mirror_bytes_value = actual_bytes_value - 19578
                                                mirror_pkts_value = actual_pkts_value - 158
                                            else:  # 如果有 "items"，但不符合特定类型时的默认行为
                                                mirror_bytes_value = actual_bytes_value - 967
                                                mirror_pkts_value = actual_pkts_value - 9

                                        # 如果有 "item" 列表，并且列表不为空
                                        elif "item" in protocol_filed and protocol_filed["item"]:
                                            item_type = protocol_filed["item"][0].get("item_type", "")
                                            if item_type in ["mail_attachment_content","mail_attachment_name"]:
                                                mirror_bytes_value = actual_bytes_value - 34554
                                                mirror_pkts_value = actual_pkts_value - 170
                                            elif item_type == "mail_subject":
                                                mirror_bytes_value = actual_bytes_value - 19578
                                                mirror_pkts_value = actual_pkts_value - 158
                                            elif item_type == "mail_content":
                                                mirror_bytes_value = actual_bytes_value - 21092
                                                mirror_pkts_value = actual_pkts_value - 159
                                            else:  # 如果有 "item"，但不符合特定类型时的默认行为
                                                mirror_bytes_value = actual_bytes_value - 967
                                                mirror_pkts_value = actual_pkts_value - 9

                                        # 如果既没有 "items" 也没有 "item"，使用默认的镜像转发处理
                                        else:
                                            mirror_bytes_value = actual_bytes_value - 967
                                            mirror_pkts_value = actual_pkts_value - 9
                                    else:
                                        mirror_bytes_value = actual_bytes_value - 967
                                        mirror_pkts_value = actual_pkts_value - 9
                                    if "profile" in test_data and test_data["profile"] != "":
                                        vlan_count = test_data['profile'][0]['vlan_count']
                                        num_vlans = vlan_count
                                        mirror_bytes_value *= num_vlans
                                        mirror_pkts_value *= num_vlans
                                elif test_data["mirror_type"] in  {"","quic","dns"}:
                                    mirror_bytes_value = actual_bytes_value
                                    mirror_pkts_value = actual_pkts_value
                                    if "profile" in test_data and test_data["profile"] != "":
                                        vlan_count = test_data['profile'][0]['vlan_count']
                                        num_vlans = vlan_count
                                        mirror_bytes_value *= num_vlans
                                        mirror_pkts_value *= num_vlans
                                else:
                                    temp_log_result_list.append(False)
                                # 统一处理逻辑
                            if "mirror_type" in test_data and test_data["mirror_type"] in {"ftp", "http", "ssl", "dns", "quic", "", "mail"}:
                                if query_field_key == "monitor_mirrored_pkts" and log[query_field_key] == mirror_pkts_value:
                                    temp_log_result_list.append(True)
                                    # 更新 test_data["log_query_param"] 中相应的 query_value
                                    for log_query_param in test_data["log_query_param"]:
                                        if log_query_param["query_field_key"] == "monitor_mirrored_pkts":
                                            log_query_param["query_value"] = mirror_pkts_value  # 将值修改为5
                                elif query_field_key == "monitor_mirrored_bytes" and log[query_field_key] == mirror_bytes_value:
                                    temp_log_result_list.append(True)
                                    # 更新 test_data["log_query_param"] 中相应的 query_value
                                    for log_query_param in test_data["log_query_param"]:
                                        if log_query_param["query_field_key"] == "monitor_mirrored_bytes":
                                            log_query_param["query_value"] = mirror_bytes_value  # 将值修改为5
                                else:
                                    temp_log_result_list.append(False)
                        # 验证范围类型的client port
                        elif query_field_key in {"client_port"}:
                            start, end = map(int, query_value.split('-'))
                            if start <= log[query_field_key] <= end:
                                temp_log_result_list.append(True)
                            else:
                                temp_log_result_list.append(False)
                        #验证ssl_ech_flag和ssl_esni_flag
                        elif query_field_key in {"ssl_ech_flag","ssl_esni_flag"}:
                            # 将 "True" 替换为 1，将 "False" 替换为 0
                            if query_value == "True":
                                query_value = 1
                            elif query_value == "False":
                                query_value = 0

                            if log[query_field_key] == query_value:
                                temp_log_result_list.append(True)
                            else:
                                temp_log_result_list.append(False)
                        elif query_field_key in dos_verify_fields:
                            temp_log_result_list= self.get_dos_temp_log_result_full_process(log,query_field_key,query_value,temp_log_result_list,test_data,token,api_host,start_time,end_time,vsys_id,time,output,policy_id)
                        elif query_field_key in {"proxy_pinning_status", "proxy_intercept_status", "proxy_passthrough_reason"}:
                            actual_value = log[query_field_key]   # 日志查询到的值
                            except_value = query_value     # 断言的预期值
                            if query_field_key == "proxy_passthrough_reason":
                                if except_value in {"EV Certificate", "Certificate Transparency", "Protocol Errors", "Mutual Authentication", "Certificate Not Installed", "Certificate Pinning"}:
                                    if actual_value in {""}:  # 证书动态放行会产生两条日志，其中一条大概率是拦截的日志，则跳过断言
                                        continue
                                    elif actual_value == except_value:
                                        temp_log_result_list.append(True)
                                    else:
                                        temp_log_result_list.append(False)
                                else:
                                    if actual_value == except_value:
                                        temp_log_result_list.append(True)
                                    else:
                                        temp_log_result_list.append(False)
                            elif query_field_key == "proxy_intercept_status":  # proxy_intercept_status的值需要转换
                                if except_value == "passthrough":      # proxy_intercept_status， 0=passthrough, 1=intercept
                                    except_value = 0
                                else:
                                    except_value = 1
                                if except_value == 0:
                                    if actual_value == 1:
                                        continue
                                    elif actual_value == except_value:
                                        temp_log_result_list.append(True)
                                    else:
                                        temp_log_result_list.append(False)
                                else:
                                    if actual_value == except_value:
                                        temp_log_result_list.append(True)
                                    else:
                                        temp_log_result_list.append(False)
                        else:
                            temp_log_result_list.append(False)
                    if policy_type == 'pxy_intercept' and len(temp_log_result_list) < len(log_query_params):
                         # 动态passthrough
                        if True in temp_log_result_list:
                            log_result = True
                        else:
                            log_result = False
                    elif False not in temp_log_result_list and len(log_list) > 0:
                        log_result = True
                    # elif len(log_list) == 0 and len(log_query_params) == 0 and False not in temp_log_result_list:
                    #     log_result = True
                    else:
                        log_result = False
                        return log_result
            elif len(log_list) == 0 and len(log_query_params) > 0:
                log_result = None
            elif len(log_query_params) == 0:
                log_result = True
            # if False not in temp_log_result_list and len(log_list) > 0:
            #     log_result = True
            # elif len(log_list) == 0 and len(log_query_params) > 0:
            #     log_result = None
            # elif len(log_list) == 0 and len(log_query_params) == 0 and False not in temp_log_result_list:
            #     log_result = True
            # else:
            #     log_result = False
        return log_result


    def get_dos_temp_log_result_full_process(self,log,query_field_key,query_value,temp_log_result_list,test_data,token,api_host,start_time,end_time,vsys_id,time,output,policy_id):
        #1.Get the time difference to calculate the session_rate、bit_rate and packet_rate
        start_time_value = log["start_time"]
        end_time_value = log["end_time"]
        time_difference = end_time_value - start_time_value

        #2.For mitigation deny:get the session count after execute the mitigation behavior;For mitigation none:get full session counts
        query_session_count,total_packets,total_bytes= self.get_session_value_in_session_records(token, api_host, start_time, end_time, vsys_id, test_data)
        if test_data["mitigation"]["behavior"] == "deny":
            exp_sessions_count = query_session_count
        elif test_data["mitigation"]["behavior"] == "none" and log["sessions"] < query_session_count:
            exp_sessions_count = log["sessions"]
        else:
            temp_log_result_list.append(False)
            exp_sessions_count = -1
        #3.In the Custom Network Attack in DoS Events.
        # For mitigaiton deny,if condition has an app,one session with four packets;if condition only have ip,one session with one packet
        # For mitigation none,one session with full packets.

        #To verify the log query param
        temp_log_result_list =  self.validate_dos_values(log, query_field_key, query_value, temp_log_result_list, time_difference,exp_sessions_count,total_packets,total_bytes, test_data, time,policy_id)
        return temp_log_result_list
    def get_session_value_in_session_records(self, token,  api_host, start_time, end_time, v_id, test_data):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        log_condition = {
            "page_no": 1,
            "page_size": 20,
            "source": "session_record",
            "columns": None,
            "start_time": "",
            "end_time": "",
            "filter": "",
            "vsys": 1
        }
        schema_type = "session_record"
        log_condition_dict = json.loads(json.dumps(log_condition))
        fields = self.get_log_schema(token, schema_type, api_host, v_id)
        log_condition_dict['columns'] = fields
        log_condition_dict['start_time'] = start_time
        log_condition_dict['end_time'] = end_time
        log_condition_dict['vsys'] = v_id
        log_condition_dict['source'] = "session_record"
        log_condition_dict['identifier_name'] = "session-record-list"
        log_condition_dict['execution_mode'] = 'oneshot'
        #log_condition_dict['filter'] = f"server_ip='{test_data['traffic']['servers_start_ip']}'AND received_pkts=1"
        if test_data["mitigation"]['behavior']== "none":
            log_condition_dict['filter'] = f"server_ip='{test_data['traffic']['servers_start_ip']}'"
        elif test_data["mitigation"]['behavior'] == "deny":
            if "application" in test_data["condition"]  and test_data["condition"]["application"] and test_data["condition"]["application"][0]["name"] == "dns":
                log_condition_dict['filter'] = f"server_ip='{test_data['traffic']['servers_start_ip']}'AND received_pkts in (0)"
            else:
                log_condition_dict['filter'] = f"server_ip='{test_data['traffic']['servers_start_ip']}'AND received_pkts in (0,1)"
        url = api_host + "/v1/logs/query".format(v_id)
        response = requests.post(url, headers=headers, json=log_condition_dict, verify=False)
        assert response.status_code == 200
        log_list = json.loads(response.text)
        log_list = log_list['data']['list']
        log_entry= log_list[0]
        # 获取 received_pkts 和 sent_pkts
        received_pkts = log_entry['received_pkts']
        sent_pkts = log_entry['sent_pkts']
        # 计算总和
        total_packets = received_pkts + sent_pkts
        # 获取 received_bytes 和 sent_bytes
        received_bytes = log_entry['received_bytes']
        sent_bytes = log_entry['sent_bytes']
        # 计算总和
        total_bytes = received_bytes + sent_bytes

        dos_deny_sessions_count = len(log_list)
        return dos_deny_sessions_count,total_packets,total_bytes


    def validate_dos_values(self, log, query_field_key, query_value, temp_log_result_list, time_difference,exp_sessions_count,total_packets ,total_bytes,test_data, time,policy_id):
        #三种情况：
        #① deny:src ip+application
        #② deny:src ip
        #③ none:
        exp_packets_count = exp_sessions_count * total_packets
        exp_bytes_count = exp_sessions_count * total_bytes
        #字段的验证:Bytes验证是否大于0、为负数;不再验证具体的值，不同用例回放数据包不同，Bytes无固定值
        if query_field_key == "attack_type":
            if query_value.replace("_", " ") == log[query_field_key].lower():
                temp_log_result_list.append(True)
            else:
                temp_log_result_list.append(False)

        elif query_field_key == "sessions":
            if exp_sessions_count == log[query_field_key]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log[query_field_key]  # time,第几次循环，则给log_query_param中的第几次-1的数赋值
            else:
                temp_log_result_list.append(False)
            # 其余值比较：基于sessions计算出的值和接口返回的值比较
        elif query_field_key == "packets":
            if exp_packets_count == log[query_field_key]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log[query_field_key]
            else:
                temp_log_result_list.append(False)

        elif query_field_key == "bytes": #大于0且是个整数
            if log[query_field_key] > 0 and exp_bytes_count == log[query_field_key]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log[query_field_key]
            else:
                temp_log_result_list.append(False)

        elif query_field_key == "bit_rate":
            bits_rate_value = int((log["bytes"] * 8) / time_difference)

            if bits_rate_value == log[query_field_key]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log[query_field_key]
            else:
                temp_log_result_list.append(False)

        elif query_field_key == "session_rate":
            session_rate = exp_sessions_count / time_difference

            if int(session_rate) == log[query_field_key]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log[query_field_key]
            else:
                temp_log_result_list.append(False)

        elif query_field_key == "packet_rate":
            packet_rate = exp_packets_count / time_difference
            if int(packet_rate) == log[query_field_key]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log[query_field_key]
            else:
                temp_log_result_list.append(False)
        elif query_field_key in ["basic_attack_type", "basic_sessions","basic_session_rate", "basic_packets", "basic_packet_rate","basic_bytes", "basic_bit_rate"]:
            temp_log_result_list.append(True)
        elif query_field_key == "rule_id":
            # 不改变用例，通过逻辑取到查询结果中的rule_uuid用于对比
            if policy_id == log["rule_uuid"]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log["rule_uuid"]
            else:
                temp_log_result_list.append(False)
        # 与开发确认，24.10 版本中conditions指标取消，且无对应的替换字段
        # elif query_field_key == "conditions":
        #     if f"DoS Protection [{policy_id}]" == log [query_field_key]:
        #         temp_log_result_list.append(True)
        #         test_data["log_query_param"][time]["query_value"] = log[query_field_key]
        #     else:
        #         temp_log_result_list.append(False)
        
        # 24.10 版本，source_ip_list替换为source_ip
        elif query_field_key == "source_ip_list" :
            if test_data["traffic"]["clients_start_ip"] == log ["source_ip"]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log["source_ip"]
            else:
                temp_log_result_list.append(False)
        elif query_field_key == "destination_ip":
            if test_data["traffic"]["servers_start_ip"] == log[query_field_key]:
                temp_log_result_list.append(True)
                test_data["log_query_param"][time]["query_value"] = log[query_field_key]
            else:
                temp_log_result_list.append(False)
        else:
            temp_log_result_list.append(False)

        return temp_log_result_list

    def get_metric(self, token, rule_num, start_time, end_time, create_policies_ids, test_data, api_host, vsys_id, script_type):
        # 请求接口查询metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = api_host + "/v1/logs/query"
        metric_result = False
        for i in range(rule_num):
            policy_type = test_data["policy_type"]
            if policy_type == 'security':
                dataset_identifier_name = "security-policy-rule-statistics"
            elif policy_type == 'pxy_intercept' or policy_type == 'pxy_manipulation':
                dataset_identifier_name = "proxy-policy-rule-statistics"
            elif policy_type == 'monitor':
                dataset_identifier_name = "monitor-policy-rule-statistics"
            elif policy_type == 'dos_protection':
                dataset_identifier_name = "dos-protection-rule-statistics"
            policy_id = list(create_policies_ids[i].values())[0]
            hit_query_condition = {"identifier_name": dataset_identifier_name, "rule_uuid": "", "start_time": "",
                                   "end_time": "", "vsys": 1, "execution_mode": "oneshot", "output_mode": "json",
                                   "interval": 1}
            hit_query_condition['rule_uuid'] = policy_id
            hit_query_condition['start_time'] = start_time
            hit_query_condition['end_time'] = end_time
            hit_query_condition['vsys'] = vsys_id
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to query metric by condition.", flush=True)
            response = requests.post(url, headers=headers, json=hit_query_condition, verify=False)
            assert response.status_code == 200
            response = json.loads(response.text)
            index = i + 1
            temp_counters = 'counters_' + str(index)
            if temp_counters in test_data.keys():
                counter = test_data[temp_counters]
            else:
                counter = test_data['counters']
            result_len = len(response['data']['list'])
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Compare metric with test data.", flush=True)
            # 需要hits == 0时，则验证，验证通过metric置为true
            if 'hits' in counter and counter['hits'] == 0 and result_len == 0:
                metric_result = True
            elif 'hits' in counter and result_len > 0:
                metric = response['data']['list'][0]
                if counter['hits'] == 1:
                    for key, value in counter.items():
                        # 接口返回的统计是否与预期的一致
                        if key not in metric or metric[key] != value:
                            metric_result = False
                        else:
                            metric_result = True
                if counter['hits'] == 2:
                    for key, value in counter.items():
                        # 接口返回的统计是否与预期的一致
                        if key not in metric or metric[key] > 2:
                            metric_result = False
                        elif key in metric and metric[key] == 1 and (test_data['traffic']['protocol'] in ['dns', 'ftp']):
                            metric_result = None
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

    def get_sc_metric(self, token, start_time, end_time, sc_info, sc_expected_metric, active_dest_ips_list, host_api, vsys_id):
        # 请求接口查询sc metric
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = "{}/v1/logs/query".format(host_api)
        # 重组请求体数据
        post_data_ori_json = """
        {
            "execution_mode": "oneshot",
            "identifier_name": "service-chaining-policy-rule-statistics",
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
        # post_data_ori_dict["rule_id"] = int(sc_info["rule_id"])
        post_data_ori_dict["rule_uuid"] = sc_info["rule_id"]
        post_data_ori_dict["vsys"] = vsys_id
        response = requests.post(url, json=post_data_ori_dict, headers=headers, verify=False)
        r_dict = response.json()
        if r_dict["code"] != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Service chaining metric query failed.", flush=True)
            return 444
        else:  # 返回正常结果
            if r_dict["data"]["list"] == []:  # 为空
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Service chaining metric is empty.", flush=True)
                return 333
            else:  # metric不为空时，验证返回结果
                metric_result = False  # 默认
                result_list = r_dict["data"]["list"]
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
                if len(sc_info["application"]) > 0 :
                    if sc_info["application"][0] == "http" or sc_info["application"][0] == "ssl" or \
                        sc_info["application"][0] == "rdp" or sc_info["application"][0] == "OPENVPN":
                        lost_pkt = 3
                        lost_byte = 192  # tcp三次握手的三个包的字节数和
                    elif sc_info["application"][0] == "ftp":
                        lost_pkt = 4
                        lost_byte = 266
                    elif sc_info["application"][0] == "mail":
                        lost_pkt = 15
                        lost_byte = 1273
                    elif sc_info["application"][0] == "dns" or sc_info["application"][0] == "quic" or \
                                sc_info["application"][0] == "rtp" :
                        lost_pkt = 0
                        lost_byte = 0
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
                if len(sc_info["application"]) > 0 :
                    if sc_info["application"][0] == "http" or sc_info["application"][0] == "ssl" or \
                        sc_info["application"][0] == "rdp" or sc_info["application"][0] == "OPENVPN":
                        lost_pkt = 3
                        lost_byte = 192  # tcp三次握手的三个包的字节数和
                    elif sc_info["application"][0] == "ftp":
                        lost_pkt = 4
                        lost_byte = 266
                    elif sc_info["application"][0] == "mail":
                        lost_pkt = 15
                        lost_byte = 1273
                    elif sc_info["application"][0] == "dns" or sc_info["application"][0] == "quic" or \
                        sc_info["application"][0] == "rtp":
                        lost_pkt = 0
                        lost_byte = 0
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

    def get_livechart_statistics(self, token, start_time, end_time, statistics_info, statistics_metircs_except, host_api, vsys_id):
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
        url = "{}/v1/logs/query".format(host_api)
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
        post_data_ori_dict_dsl["filter"] = "vsys_id in ({}) and rule_uuid = {} and template_uuid = {} and chart_uuid = {} and version = {}".format(vsys_id,statistics_info["rule_id"],statistics_info["template_id"],statistics_info["chart_id"],statistics_info["version"])
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
        post_data_ori_dict["vsys"] = vsys_id
        # 请求接口获取Metrics数据
        response = requests.post(url, json=post_data_ori_dict, headers=headers, verify=False)
        r_dict = response.json()
        # 打印获取Metrics相关开始结束时间和Rule ID信息信息，方便后面出错排查问题
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "statistics metric:start_time:{}, end_time:{}, rule_id:{}, template_id:{}, chart_id:{}, version:{}".format(start_time, end_time, statistics_info["rule_id"], statistics_info["template_id"], statistics_info["chart_id"], statistics_info["version"]))
        if r_dict["code"] != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],  "Exception when getting Metrics data from the interface.")
            return [False, "The statistics metric API query failed."]
        else:  # 返回正常结果
            if r_dict["data"]["list"] == []:  # 为空
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Debug:The statistics metric API query result is []")
                # 对应有方向的session的单一Metrics方式需要另行处理
                tmp_in_out_list = UtilStatisticsTemplate().tmp_in_out_list
                # api返回值为空，不判断方向，直接返回重新查找
                if len(statistics_info["metrics"]) == 1:
                    #for item in statistics_info["metrics"]:
                    if len(statistics_info["metrics"][0]["source_fields"]) == 1 and statistics_info["metrics"][0]["source_fields"][0] in tmp_in_out_list:
                        return [333, "this is a pass"]
                return [False, "statistics metric no result was found."]
            else:  # 提取结果，并断言
                result_list_from_api = r_dict["data"]["list"]
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Debug:The statistics metric API query result is {}".format(result_list_from_api))
                #print(result_list_from_api)
                result_list = []
                metrics_len = len(statistics_info["metrics"])
                dimensions_len = len(statistics_info["dimensions"]) #time调试时需确认是否处理
                tmp_result = {}
                break_flag = False
                for _ in copy.deepcopy(result_list_from_api):
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
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Debug:The statistics metric API query result is {}".format(result_list_from_api), flush=True)
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
                        metric_results = self.assert_livechart_statistics(statistics_info, statistics_value, statistics_metircs_except, time_dif_seconds)  # 判断正确调用函数
                elif statistics_info["chart_type"] == "histogram":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Histogram cannot automatically compare statistical results.", flush=True)
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Debug:The statistics metric API query result is {}".format(result_list_from_api), flush=True)
                    metric_results = [True, ""]
                return metric_results
    
    def assert_livechart_statistics(self, statistics_info, statistics_value, statistics_metircs_except, time_dif_seconds):
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
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], failure_reason)
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
                    # * Sessions处理逻辑new_in_sessions、new_out_sessions、closed_in_sessions、closed_out_sessions
                    elif source_fields[0] in {"new_in_sessions", "new_out_sessions", "closed_in_sessions", "closed_out_sessions"} and (stats_value == total_syn_pkt1 or stats_value == 0):
                        metric_result = True
                    # * Flows处理逻辑new_c2s_flows、new_s2c_flows
                    elif source_fields[0] in {"new_c2s_flows", "new_s2c_flows"} and stats_value == total_syn_pkt1:
                        metric_result = True
                    #elif source_fields[0] == "received_pkts" and stats_value == test_traffic_statistics["total_packets_received"]:
                    #    metric_result = True
                    #elif source_fields[0] == "syn_pkts" and stats_value == test_traffic_statistics["total_syn_pkt"] * 2:
                    #    metric_result = True
                    # * Fragments处理逻辑:c2s_ip_fragments、s2c_ip_fragments,to do
                    elif source_fields[0] in {"c2s_ip_fragments", "s2c_ip_fragments"} and (stats_value == total_packets_sent or stats_value == total_packets_received or stats_value == 0):
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
                    # * Sessions处理逻辑new_in_sessions、new_out_sessions、closed_in_sessions、closed_out_sessions
                    elif (("new_in_sessions" in source_fields and "new_out_sessions" in source_fields) or ("closed_in_sessions" in source_fields and "closed_out_sessions" in source_fields)) and stats_value == total_syn_pkt1:
                        metric_result = True
                    # * Flows处理逻辑new_c2s_flows、new_s2c_flows
                    elif "new_c2s_flows" in source_fields and "new_s2c_flows" in source_fields and stats_value == total_syn_pkt2:
                        metric_result = True
                    # * Fragments处理逻辑:c2s_ip_fragments、s2c_ip_fragments,to do
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case 3: #如有需定义3个的业务场景需补充相关逻辑
                    failure_info_2 = f"Meaningless source fields definition: {source_fields}"
                case 4: #如有需定义4个的业务场景需补充相关逻辑
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
        """        
        'in_pkt_length_distribution': 'Incoming Packet Length',
        'out_pkt_length_distribution': 'Outgoing Packet Length',
        'pkt_length_distribution': 'Packet Length',        
        """
        # unique和syn数量：1一致
        one_or_zero_unique = {"new_in_sessions", "new_out_sessions", "closed_in_sessions","closed_out_sessions","syn_pkts"
            'new_in_sessions',
            'new_out_sessions',
            'closed_in_sessions',
            'closed_out_sessions',
            'syn_pkts',
            'in_latency_ms',
            'out_latency_ms'
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
            'in_latency_ms',
            'out_latency_ms',
            'dtls_handshake_latency_ms',
            'ssl_handshake_latency_ms',
            'tcp_handshake_latency_ms',
            'duration_ms',
            'tcp_rtt_ms',
            'new_c2s_flows',
            'new_s2c_flows',
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
                        # * Sessions处理逻辑new_in_sessions、new_out_sessions、closed_in_sessions、closed_out_sessions
                        if source_fields[0] in one_or_zero_unique and (stats_value == test_traffic_statistics["total_syn_pkt"] or stats_value == 0):
                            metric_result = True
                        elif source_fields[0] in one_unique and (stats_value == test_traffic_statistics["total_syn_pkt"]):
                            metric_result = True
                        elif source_fields[0] in uncertain_quantity_unique and (stats_value >= test_traffic_statistics["total_syn_pkt"]):
                            metric_result = True
                        elif stats_value >= 1:
                            metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case 2:
                    if source_fields[0] in all_metrics and source_fields[1] in all_metrics:
                        if (("new_in_sessions" in source_fields and "new_out_sessions" in source_fields) or ("closed_in_sessions" in source_fields and "closed_out_sessions" in source_fields)) and (stats_value == test_traffic_statistics["total_syn_pkt"]):
                            metric_result = True
                        # * Flows处理逻辑new_c2s_flows、new_s2c_flows
                        elif "new_c2s_flows" in source_fields and "new_s2c_flows" in source_fields and stats_value == test_traffic_statistics["total_syn_pkt"]*2:
                            metric_result = True
                        elif stats_value >= test_traffic_statistics["total_syn_pkt"]:
                            metric_result = True
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

    def metric_percentile_value_verification(self, source_fields):
        # 待重构
        metric_result = False
        failure_info_2 = ""
        util = UtilStatisticsTemplate()
        code, all_metrics = util.get_all_metrics_or_dimensions("distribution_metrics")
        if code != 200:
            return False, "Failed to obtain the Field whose Metric Type is Distribution"
        try:
            match len(source_fields):
                case 1:
                    if source_fields[0] in all_metrics:
                        metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
                case _:
                    if source_fields[0] in all_metrics:
                        metric_result = True
                    else:
                        failure_info_2 = f"Automatic statistics fields are not implemented: {source_fields}"
            return metric_result, failure_info_2
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                  "Histogram statistical data verification anomaly.exception:{}".format(exception_result),
                  flush=True)
            return metric_result, failure_info_2

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")