#!/usr/bin/python3
# coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import requests
import json
import subprocess
import createObject
import createRule
import delConfig
import getApplicationId
import getLog
import createProfile
import time
import report
import random
import traceback
import fnmatch
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from traffic_replay.traffic_replay import TrafficReplay

class Verify():
    def __init__(self):
        self.password = ""
        self.token = ""
        self.table_data = []
        self.all_cases_count = 0
        self.excuted_cases_count = 0
        self.pass_cases_count = 0
        self.fail_cases_count = 0
        self.res_time_result = True

    def encryptPwd(self, pwd, api_host):
        url = api_host + "/v1/user/encryptpwd"
        pwJson = {"password": ""}
        pwJson["password"] = pwd
        response = requests.get(url, params=pwJson)
        data = json.loads(response.text)
        self.password = data["data"]["encryptpwd"]
        return self.password

    def login(self, user, api_host):
        url = api_host + "/v1/user/login"
        loginJson = {"username": "", "password": ""}
        loginJson["username"] = user
        loginJson["password"] = self.password
        response = requests.post(url, json=loginJson)
        jsonData = json.loads(response.text)
        self.token = jsonData["data"]["token"]
        return self.token

    def start_verify(self, parameter, config, template_path):
    # def start_verify(self, user, password, test_pc_ip, api_host, is_log, path_dict, run_env, vsys_id, debug_json=""):
        """
        :param user:
        :param password:
        :param test_pc_ip:
        :param api_host:
        :param is_log:
        :param path_dict:   路径字典，需要使用路径参数，在此变量中
        :param run_env:
        :param debug_json:
        :return:
        """
        user = parameter["username"]
        password = parameter["password"]
        test_pc_ip = parameter["test_pc_ip"]
        api_host = parameter["api_host"]
        is_log = parameter["is_log"]
        path_dict = template_path
        run_env = parameter["env"]
        vsys_id = parameter["vsys_id"]
        self.encryptPwd(password, api_host)
        self.login(user, api_host)
        self.table_data.append(["Name", "Result", "Failure Reason"])
        try:
            self.create_ip_ids = []
            self.create_subid_ip_ids = []
            self.create_fqdn_ids = []
            self.create_url_ids = []
            self.create_flag_ids = []
            self.create_keywords_ids = []
            self.create_account_ids = []
            self.create_http_signature_ids = []
            self.create_policies_ids = []
            self.statistics_info_list = []
            if ("need_to_verify" in config):
                has_verify_flag = 1
            else:
                has_verify_flag = 0
            # 下发配置
            self.dispatch_config(config, api_host, test_pc_ip, path_dict, has_verify_flag, vsys_id, run_env=run_env)
            # 如果不存在need_to_verify或need_to_verify为true，表示需要进行验证且出报告
            if has_verify_flag == 0 or config["need_to_verify"] == True:
                # 流量验证、构造流量、日志验证
                result_list = self.verify_result(config, test_pc_ip, is_log, self.statistics_info_list, api_host, vsys_id, path_dict)
                cmd_result = result_list[0]
                log_result = result_list[1]
                metric_result = result_list[2]
                if len(result_list) == 4:
                    statistics_failure_reason = result_list[3]     # statistic错误原因
            else:
                cmd_result, log_result, metric_result = True, True, True    
            # 删除配置
            erase = delConfig.Erase()
            erase.del_config(self.token, self.create_policies_ids, self.create_ip_ids, self.create_subid_ip_ids, self.create_fqdn_ids, self.create_url_ids, self.create_flag_ids, self.create_keywords_ids, self.create_account_ids, self.create_http_signature_ids, self.create_profile_ids, api_host, vsys_id)
            # 生成报告的数据
            self.excuted_cases_count += 1
            report_data = []
            report_data.append(parameter["test_case_name"])
            if cmd_result == False or log_result == False or metric_result == False:
                result = "Fail"
                self.fail_cases_count += 1
            else:
                result = "PASS"
                self.pass_cases_count += 1
            report_data.append(result)
            failure_reason = ""
            if config["policyType"] == "statistics":
                failure_reason = statistics_failure_reason
            elif config["policyType"] == "service_chaining":
                if cmd_result == False or log_result == False or metric_result == False:
                    failure_reason = failure_reason + "The verification result of metrics is failed, the failure reason is: the metrics do not match the expectation value."
            elif config["policyType"] == "tsg_security":
                if cmd_result == False and log_result == True and metric_result == True and self.res_time_result == True:
                    failure_reason = failure_reason + "The verification result of policy effect is failed, the failure reason is: the contents returned by the command do not contain the expected value."
                elif cmd_result == False and log_result == True and metric_result == True and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification result of policy effect and create time are failed, the failure reason is: the contents returned by the command do not contain the expected value, the create time is over 60s"
                elif cmd_result == False and log_result == False and metric_result == True and self.res_time_result == True:
                    failure_reason = failure_reason + "The verification results of policy effect and logs are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs."
                elif cmd_result == False and log_result == False and metric_result == True and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification results of policy effect, logs and create time are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs, the create time is over 60s"
                elif cmd_result == False and log_result == True and metric_result == False and self.res_time_result == True:
                    failure_reason = failure_reason + "The verification results of policy effect and metrics are failed, the failure reasons are: the contents returned by the command did not contain the expected value; the metrics do not match the expectation value."
                elif cmd_result == False and log_result == True and metric_result == False and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification results of policy effect, metrics and create time are failed, the failure reasons are: the contents returned by the command did not contain the expected value; the metrics do not match the expectation value, the create time is over 60s"
                elif cmd_result == True and log_result == False and metric_result == True and self.res_time_result == True:
                    failure_reason = failure_reason + "The verification result of logs is failed, the failure reason is: the expected value is not queried in the logs."
                elif cmd_result == True and log_result == False and metric_result == True and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification result of logs and create time are failed, the failure reasons are: the expected value is not queried in the logs, the create time is over 60s"
                elif cmd_result == True and log_result == True and metric_result == False and self.res_time_result == True:
                    failure_reason = failure_reason + "The verification result of metrics is failed, the failure reason is: the metrics do not match the expectation value."
                elif cmd_result == True and log_result == True and metric_result == False and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification result of metrics and create time are failed, the failure reasos are: the metrics do not match the expectation value, the create time is over 60s"
                elif cmd_result == True and log_result == True and metric_result == True and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification result of create time is failed, the failure reason is: the create time is over 60s."
                elif cmd_result == True and log_result == False and metric_result == False and self.res_time_result == True:
                    failure_reason = failure_reason + "The verification results of logs and metrics are failed, the failure reasons are: the expected value is not queried in the logs; the metrics do not match the expectation value."
                elif cmd_result == True and log_result == False and metric_result == False and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification results of logs, metrics and create time are failed, the failure reasons are: the expected value is not queried in the logs; the metrics do not match the expectation value, the create time is over 60s"
                elif cmd_result == False and log_result == False and metric_result == False and self.res_time_result == True:
                    failure_reason = failure_reason + "The verification results of effect, logs and metrics are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs; the metrics do not match the expectation value."
                elif cmd_result == False and log_result == False and metric_result == False and self.res_time_result == False:
                    failure_reason = failure_reason + "The verification results of effect, logs, metrics  and create time are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs; the metrics do not match the expectation value, the create time is over 60s"
            report_data.append(failure_reason)
            self.table_data.append(report_data)
            return failure_reason
        except Exception as e:
            print(e)
            traceback.print_exc()

    def dispatch_config(self, condition, api_host, test_pc_ip, path_dict, has_verify_flag, vsys_id, run_env="tsgx"):
        # 按key-value进行策略、对象的新增
        isMultiPriority = condition['isMultiPriority']
        if isMultiPriority:
            self.rule_num = condition['ruleNum']
        else:
            self.rule_num = 1
        self.create_profile_ids = []
        self.policy_statistics_template_chart_info = []   # 用于statistics 查询使用
        self.policy_sc_sff_sf_info = [] # 组合policy和profile信息
        temp_profile_list = []  # 共组合使用
        # statistics和sc需要随机ip
        if condition["policyType"] == "statistics" or (condition["policyType"] == "service_chaining" and condition["targeted_traffic"] == "raw"):
            condition = self.generate_random_ip(condition, run_env=run_env)
        for i in range(self.rule_num):
            # 第i次循环，创建第i组object、profile和rule
            create_number = i + 1
            obj_condition = condition['obj_condition_'+str(create_number)]
            # 创建object
            object_info = createObject.CreateObject()
            obj_template = path_dict["obj_template"]
            res_time_result, source_list, dst_list, filter_list, flag_list, ip_ids, subid_ids, fqdn_ids, url_ids, flag_ids, keywords_ids, account_ids, http_signature_ids = object_info.create_condition(self.token, obj_condition, obj_template, api_host, test_pc_ip, vsys_id)
            self.res_time_result = res_time_result
            # 如果need_to_verify为true或has_verify_flag为0，表示需要验证功能，如果need_to_verify为false，则不需要验证，直接退出
            if has_verify_flag == 1 and condition["need_to_verify"] == False:
                break
            # print(res_time_result)
            if len(ip_ids) > 0:
                self.create_ip_ids.extend(ip_ids)
            if len(subid_ids) > 0:
                self.create_subid_ip_ids.extend(subid_ids)
            if len(fqdn_ids) > 0:
                self.create_fqdn_ids.extend(fqdn_ids)
            if len(url_ids) > 0:
                self.create_url_ids.extend(url_ids)
            if len(flag_ids) > 0:
                self.create_flag_ids.extend(flag_ids)
            if len(keywords_ids) > 0:
                self.create_keywords_ids.extend(keywords_ids)
            if len(account_ids) > 0:
                self.create_account_ids.extend(account_ids)
            if len(http_signature_ids) > 0:
                self.create_http_signature_ids.extend(http_signature_ids)
            # 创建profile
            profile_condition_key = "profile_condition_{}".format(create_number)
            if (profile_condition_key in condition.keys()) and len(condition[profile_condition_key]) > 0:    # 含有profile_condition_ key 并且非空
                profile_info = createProfile.CreateProfile()
                profile_condition_values = condition[profile_condition_key]
                for profile_data in profile_condition_values:
                    # create_profile_ids_dict用于删除和metric查询使用
                    create_profile_ids_dict = profile_info.create_profile_by_template(path_dict, profile_data, self.token, api_host, vsys_id)
                    #print(create_profile_ids_dict)
                    self.create_profile_ids.append(create_profile_ids_dict)
                    if condition["policyType"] == "statistics" or condition["policyType"] == "service_chaining":
                        temp_profile_list.append(create_profile_ids_dict)
            # 创建rule
            rule_info = createRule.CreatePolicyRule()
            policy_id_list = rule_info.create_rule_by_template(self.token, source_list, dst_list, filter_list, flag_list, condition, create_number, path_dict, api_host, vsys_id, create_profile_ids=self.create_profile_ids)
            self.policy_id = list(policy_id_list[0].values())[0]
            if len(self.create_profile_ids) > i:     # 含有profile profile ，提取profile id等相关信息
                if condition["policyType"] == "statistics":
                    temp_info = {}
                    temp_info["policy_id"] = list(policy_id_list[i].values())[i]
                    temp_info["profile_info"] = temp_profile_list     # 来自上面常见porfile数据
                    self.policy_statistics_template_chart_info.append(temp_info)
                    if len(self.policy_statistics_template_chart_info) > 0:
                        for chart in self.policy_statistics_template_chart_info[0]["profile_info"][0]["template_info"]:
                            statistics_info = {}
                            statistics_info["rule_id"] = self.policy_statistics_template_chart_info[0]["policy_id"]
                            statistics_info["template_id"] = chart["template_id"]
                            statistics_info["chart_id"] = chart["chart_id"]
                            statistics_info["chart_type"] = chart["chart_type"]
                            statistics_info["version"] = chart["version"]
                            statistics_info["sql"] = chart["sql"]
                            self.statistics_info_list.append(statistics_info)
                elif condition["policyType"] == "service_chaining":
                    sc_sff_sf_info = {}
                    sc_sff_sf_info["policy_id"] = list(policy_id_list[i].values())[i]
                    sc_sff_sf_info["sff_info"] = temp_profile_list
                    self.policy_sc_sff_sf_info.append(sc_sff_sf_info)
                    if len(self.policy_sc_sff_sf_info) > 0:
                        for sff in self.policy_sc_sff_sf_info[0]["sff_info"]:
                            sc_info = {}
                            sc_info["rule_id"] = self.policy_sc_sff_sf_info[0]["policy_id"]
                            sc_info["targeted_traffic"] = condition["targeted_traffic"]
                            sc_info["app_name_1"] = condition["app_name_1"]
                            sc_info["sff_id"] = sff["id"]
                            sc_info["type"] = sff["sff_info"]["type"]
                            sc_info["sf_id"] = sff["sff_info"]["sf_info"][0]["id"]
                            if sff["sff_info"]["sf_info"][0]["connectivity"]["method"] == "vxlan_g":
                                sc_info["sf_method"] = sff["sff_info"]["sf_info"][0]["connectivity"]["method"]
                                sc_info["sf_dest_ip"] = sff["sff_info"]["sf_info"][0]["connectivity"]["dest_ip"]
                                sc_info["health_check_method"] = sff["sff_info"]["sf_info"][0]["health_check"]["method"]
                            else:
                                sc_info["sf_method"] = sff["sff_info"]["sf_info"][0]["connectivity"]["method"]
                                sc_info["health_check_method"] = "none"
                            self.statistics_info_list.append(sc_info)
            if len(policy_id_list) > 0:
                self.create_policies_ids.extend(policy_id_list)

    def is_debug_case_file(self, folder_path, debug_json):
        debug_json_abspath = os.path.join(folder_path, debug_json)
        if os.path.exists(debug_json_abspath):
            debug_flag = 1
            file_path = debug_json_abspath
            return debug_flag, file_path
        else:
            # raise Exception("debug单个json文件不存在：{}".format(debug_json_abspath))
            print("debug单个json文件不存在：{}".format(debug_json_abspath))
            return -1, ""

    def verify_result(self, condition, test_pc_ip, is_log, statistics_info_list, api_host, vsys_id, path_dict):
        # 判断，如果condition中包含名为command的key，则读取command来执行，否则执行默认的
        policy_type = condition["policyType"]
        log = getLog.GetLog()
        if policy_type == "tsg_security" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor":
            # 获取开始时间
            now = datetime.utcnow()
            start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            # 等待时间，等待策略生效
            time.sleep(30)
            # 触发流量
            command = condition['command']
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
            output, error = p.communicate()
            output = output + error
            # cmd_return = output.decode(errors='ignore')
            cmd_return = output
            print(output)
            hope_return = condition['hope_return']
            # 获取结束时间
            now = datetime.utcnow()
            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            cmd_result = self.is_in(cmd_return, hope_return)
            loop_num = condition['ruleNum']
            is_counters, is_log_query = self.is_verify(condition, loop_num, 'counters', 'log_query_param')
            if is_log == 1:
                if is_log_query == 1:
                    # 考虑到有5分钟后才出日志的情况，循环5次
                    for _ in range(5):
                        now = datetime.utcnow()
                        end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                        # 等待产生日志
                        time.sleep(30)
                        log_result = log.get_log_by_condition(self.token, self.rule_num, start_time, end_time, test_pc_ip, self.create_policies_ids, condition, api_host, vsys_id)
                        if log_result == True:
                            break
                elif is_log_query == 0:
                    # 此时代表不需要进行logs模块的校验，可能为security shunt动作或statistics，sc策略等
                    log_result = True
                if is_counters == 1:
                    for _ in range(5):
                        now = datetime.utcnow()
                        end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                        time.sleep(30)
                        metric_result = log.get_metric(self.token, self.rule_num, start_time, end_time, self.create_policies_ids, condition, api_host, vsys_id)
                        if log_result == True:
                            break
                elif is_counters == 0:
                    metric_result = True
            else:
                metric_result = True
                log_result = True
            return cmd_result, log_result, metric_result
        elif policy_type == "statistics":      # statistics 使用trex流量回放验证
            # 获取开始时间
            #time.sleep(1)
            #print(55)
            #return 1, 1, 1, "调试"
            time.sleep(5)
            now = datetime.utcnow()
            start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            print("trex，回放流量方法")
            # 解析trex使用参数， 解析client server ip
            for ip_item in condition["obj_condition_1"]:
                if "ATTR_SOURCE_ADDR" in ip_item.values():
                    if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                        clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                        clients_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                    else:
                        clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                        clients_end = clients_start
                if "ATTR_DESTINATION_ADDR" in ip_item.values():
                    if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                        servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                        servers_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                    else:
                        servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                        servers_end = servers_start
            # 解析trex 命令行参数，-m -d
            if "trex" in condition.keys():
                m = condition["trex"]["m"]
                d = condition["trex"]["d"]
                yaml_name = condition["trex"]["yaml_name"].strip()
                pcap_name = condition["trex"]["pcap_name"].strip()
            else:
                print("trex参数使用默认值：")
                m = 1
                d = 1
                yaml_name = "http_50.yaml"
                pcap_name = "http_get_347pkts.pcap"
            # 执行trex命令前，策略验证，查看下发策略是否生效

            ######## 不要删除
            verify_policy_break_count = 0
            while True:      # 多次策略验证
                verify_attribute_dict = {"src_ip": clients_start, "dst_ip": servers_start}
                print(verify_attribute_dict)
                hit_policy_list = self.verify_policy(condition, verify_attribute_dict, self.token, api_host, vsys_id)
                if self.policy_id in hit_policy_list:   # 策略生效，验证通过，跳出验证
                    break
                if verify_policy_break_count > 6:    # 预计验证10分钟，仍然不生效，则结束执行，报异常。
                    # 直接调用清空策略方法
                    print("测试不生效，结束测试：策略id：{}".format(self.policy_id))
                    return False, False, False
                verify_policy_break_count += 1
                time.sleep(20)
                print("间隔{}秒，第{}次策略验证结果：策略验证失败，策略没有生效，{}策略id：{} ...".format(20*verify_policy_break_count, verify_policy_break_count, condition["policyType"], self.policy_id))
            time.sleep(5)     # 策略验证通过后，延迟五秒启动流量回放

            # 执行回放命令
            traffic_replay = TrafficReplay(path_dict)
            statistics_metircs = traffic_replay.trex_playback(yaml_name, pcap_name, m=m, d=d, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
            time.sleep(50)
            now = datetime.utcnow()
            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            cmd_return = hope_return = condition['hope_return']
            # 断言判断
            trex_ip_info = {}
            trex_ip_info["clients_start"] = clients_start
            trex_ip_info["clients_end"] = clients_end
            trex_ip_info["servers_start"] = servers_start
            trex_ip_info["servers_end"] = servers_end
            if len(statistics_info_list) > 0:  # 非空
                for statistics_info in statistics_info_list:
                    n = 1    #自增变量
                    fail_count = 1   #失败重试变量
                    while n < 3:
                        now = datetime.utcnow()
                        end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')   # 重新获取结束时间
                        metric_results = log.get_livechart_statistics(self.token, start_time, end_time, statistics_info, statistics_metircs, trex_ip_info, api_host, vsys_id)
                        metric_result = metric_results[0]
                        if metric_result == True:  # 返回结果不等于333，则退出循环查询
                            break
                        elif metric_result == False:  # 查询验证失败时，再查询验证一次
                            if fail_count > 2:
                                break
                            fail_count += 1
                        time.sleep(60)
                        n += 1
                if  metric_results[0] == 333:     # API 查询失败时变量赋值
                    metric_result = False
            return metric_result, metric_result, metric_result, metric_results[1]    # 匹配其它策略模式
        elif policy_type == "service_chaining":
            active_dest_ips_list = ["2.2.2.53", "2.2.2.56", "2.2.2.57"] # vxlan时判断dest_ip是否在bfd探测为active的ip里
            if condition["targeted_traffic"] == "raw":
                # 获取开始时间
                time.sleep(5)
                now = datetime.utcnow()
                start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                print("trex，回放流量方法")
                # 解析trex使用参数， 解析client server ip
                for ip_item in condition["obj_condition_1"]:
                    if "ATTR_SOURCE_ADDR" in ip_item.values():
                        if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                            clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                            clients_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                        else:
                            clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                            clients_end = clients_start
                    if "ATTR_DESTINATION_ADDR" in ip_item.values():
                        if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                            servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                            servers_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                        else:
                            servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                            servers_end = servers_start
                # 解析trex 命令行参数，-m -d
                if "trex" in condition.keys():
                    m = condition["trex"]["m"]
                    d = condition["trex"]["d"]
                    yaml_name = condition["trex"]["yaml_name"].strip()
                    pcap_name = condition["trex"]["pcap_name"].strip()
                else:
                    print("trex参数使用默认值：")
                    m = 1
                    d = 1
                    yaml_name = "http_50.yaml"
                    pcap_name = "http_get_347pkts.pcap"
                # 执行回放命令
                traffic_replay = TrafficReplay(path_dict)
                sc_metircs = traffic_replay.trex_playback(yaml_name, pcap_name, m=m, d=d, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
                time.sleep(20)
                now = datetime.utcnow()
                end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                cmd_return = hope_return = condition["hope_return"]
                # 断言判断
                if len(statistics_info_list) > 0:   # 非空
                    for statistics_info in statistics_info_list:
                        n = 0    #自增变量
                        fail_count = 0   #失败重试变量
                        while n <= 4:
                            now = datetime.utcnow()
                            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')   # 重新获取结束时间
                            metric_result = log.get_sc_metric(self.token, start_time, end_time, statistics_info, sc_metircs, active_dest_ips_list, api_host)
                            if metric_result == True:  # 返回结果不等于333，则退出循环查询
                                break
                            elif metric_result == False or metric_result == 333:  # 查询验证失败时，再查询验证两次
                                if fail_count >= 2:
                                    break
                                fail_count += 1
                            time.sleep(60)
                            n += 1
                    if metric_result == 333:
                        if statistics_info["sf_method"] == "vxlan_g" and statistics_info["sf_dest_ip"] not in active_dest_ips_list:
                            metric_result = True
                        else:
                            metric_result = False
                    elif metric_result == 444:
                        metric_result = False
                cmd_result = metric_result
            elif condition["targeted_traffic"] == "decrypted":
                # 获取开始时间
                now = datetime.utcnow()
                start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                # 等待时间，等待策略生效
                time.sleep(sleep_time)
                # 触发流量
                command = condition['command']
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, _ = p.communicate()
                cmd_return = output.decode()
                hope_return = condition['hope_return']
                # 获取结束时间
                now = datetime.utcnow()
                end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                cmd_result = self.is_in(cmd_return, hope_return)
                if len(statistics_info_list) > 0:  # 非空
                    for statistics_info in statistics_info_list:
                        n = 0  # 自增变量
                        fail_count = 0  # 失败重试变量
                        while n <= 6:
                            now = datetime.utcnow()
                            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')  # 重新获取结束时间
                            metric_result = log.get_sc_metric(self.token, start_time, end_time, statistics_info,"", active_dest_ips_list, api_host)
                            if metric_result == True:  # 返回结果不等于333，则退出循环查询
                                break
                            elif metric_result == False or metric_result == 333:  # 查询验证失败时，再查询验证两次
                                if fail_count >= 2:
                                    break
                                fail_count += 1
                            time.sleep(60)
                            n += 1
                    if metric_result == 333:
                        if statistics_info["sf_method"] == "vxlan_g" and statistics_info["sf_dest_ip"] not in active_dest_ips_list:
                            metric_result = True
                        else:
                            metric_result = False
                    elif metric_result == 444:
                        metric_result = False
            return cmd_result, metric_result, metric_result

    def is_verify(self, condition, loop_num, counters, log_query_param):
        # 判断传入了验证日志、metric相关的参数
        is_counters = 0
        is_log_query = 0
        for i in range(loop_num):
            index = i + 1
            counters_data = condition[counters + '_' + str(index)]
            if counters_data != {}:
                is_counters = 1
                break
        for i in range(loop_num):
            index = i + 1
            log_query_param_data = condition[log_query_param + '_' + str(index)]
            if len(log_query_param_data) > 0:
                is_log_query = 1
                break
        return is_counters, is_log_query

    def generate_random_ip(self, config, run_env="tsgx"):
        # statistics中将ip改为随机
        if "obj_condition_1" in config.keys():
            for obj in config["obj_condition_1"]:
                if obj["protocolField"] == "ATTR_SOURCE_ADDR" or obj["protocolField"] == "ATTR_DESTINATION_ADDR":
                    src_ip = obj["objectList"][0]["addItemList"][0]["ip_address"]
                    if "-" not in src_ip and "/" not in src_ip:
                        src_ip_list = src_ip.split(".")
                        src_ip_list[2] = str(random.randint(200, 250))
                        src_ip_list[3] = str(random.randint(100, 250))
                        if run_env == "7400":
                            src_ip_list[0] = "10"
                            src_ip_list[1] = "50"
                        elif run_env == "9140":
                            src_ip_list[0] = "172"
                            src_ip_list[1] = "56"
                        elif run_env == "tsgx":
                            src_ip_list[0] = "10"
                            src_ip_list[1] = "64"
                        new_src_ip = ".".join(src_ip_list)
                        obj["objectList"][0]["addItemList"][0]["ip_address"] = new_src_ip
                    elif "-" in src_ip and "/" not in src_ip:
                        two_ip_list = src_ip.split("-")
                        ip_list_1 = two_ip_list[0].split(".")
                        ip_list_2 = two_ip_list[1].split(".")
                        ip_list_1[2] = str(random.randint(200, 250))
                        ip_list_1[3] = str(random.randint(1, 50))
                        ip_list_2[2] = ip_list_1[2]
                        ip_list_2[3] = str(int(ip_list_1[3]) + 200)
                        new_ip_1 = ".".join(ip_list_1)
                        new_ip_2 = ".".join(ip_list_2)
                        if run_env == "7400":
                            ip_list_1[0] = "10"
                            ip_list_1[1] = "50"
                            ip_list_2[0] = "10"
                            ip_list_2[1] = "50"
                        elif run_env == "9140":
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
                        new_two_ip = "-".join(new_two_ip_list)
                        obj["objectList"][0]["addItemList"][0]["ip_address"] = new_two_ip
        return config

    def is_in(self, full_str, sub_str):
        sub_str = sub_str.split(',')
        # 遍历sub_str中的每个单词，并检查该单词是否在full_str中
        cmd_result = all(word in full_str for word in sub_str)
        return cmd_result # 返回：True or False

    def verify_policy(self, condition, verify_attribute_dict, token, host_api, vsys_id):
        """
        :param condition:
        :param verify_attribute_dict:    {key:value}形式的验证条件，只支持ip
        :param token:
        :param host_api:
        :param vsys_id:
        :return:
        """
        # 简单策略验证策略是否生效，验证ip+http
        #print("策略验证api需要适配新版，目前还没有")
        verify_list_json = """
            {"verify_list":[{"type":"statistics","vsys_id":1,"verify_session":{"attributes":[{"attribute_type":"ip","attribute_name":"source","attribute_value":{"ip":"10.64.133.200","port":1000,"table_name":"","addrType":4,"protocol":"6"}},{"attribute_type":"ip","attribute_name":"destination","attribute_value":{"ip":"10.64.156.173","port":80,"table_name":"","addrType":4,"protocol":"6"}},{"attribute_type":"numeric","attribute_name":"app_id","attribute_value":{"numeric":67}}]}}],"vsys_id":1}            """
        url = "{}/v1/policy/rule/verify_policy".format(host_api)
        headers = {"Content-Type": "application/json", "Authorization": token}
        verify_list_dict = json.loads(verify_list_json)
        # 重组type
        verify_list_dict["verify_list"][0]["type"] = condition["policyType"]
        # 重组 src ip
        if "src_ip" in verify_attribute_dict.keys():
            verify_list_dict["verify_list"][0]["verify_session"]["attributes"][0]["attribute_value"]["ip"] = verify_attribute_dict["src_ip"]
        # 重组 dst_ip
        if "dst_ip" in verify_attribute_dict.keys():
            verify_list_dict["verify_list"][0]["verify_session"]["attributes"][1]["attribute_value"]["ip"] = verify_attribute_dict["dst_ip"]
        # 重组 vsys_id
        verify_list_dict["verify_list"][0]["vsys_id"] = vsys_id
        verify_list_dict["vsys_id"] = vsys_id
        # 重组查询 application
        if condition["app_name_1"] != []:
            #print(str(condition["app_name_1"]))
            app_list = getApplicationId.get_app_id(str(condition["app_name_1"]), host_api)
            #print(app_list)
            verify_list_dict["verify_list"][0]["verify_session"]["attributes"][2]["attribute_value"]["numeric"] = app_list[0]
        #print(verify_list_dict)
        response = requests.post(url, json=verify_list_dict, headers=headers)
        r_dict = response.json()
        #print(json.dumps(r_dict))
        hit_policy_list = []
        if "hit_policy_list" in r_dict["data"].keys():
            for policy_id in r_dict["data"]["hit_policy_list"]:
                hit_policy_list.append(policy_id["id"])
        return hit_policy_list

    # 遍历文件夹，查看有多少个用例
    def find_json_files(self, directory):
        for _, _, files in os.walk(directory):
            for file in files:
                if fnmatch.fnmatch(file, '*.json'):
                    self.all_cases_count += 1

    # 计算当前已执行和未执行用例的数量，生成报告
    def build_report(self):
        unexcuted_cases_count = self.all_cases_count - self.excuted_cases_count
        pie_table_data = [
            [self.all_cases_count, self.pass_cases_count, self.fail_cases_count, unexcuted_cases_count]
        ]
        pass_cases_ratio = self.pass_cases_count/self.all_cases_count*100
        fail_cases_ratio = self.fail_cases_count/self.all_cases_count*100
        unexcuted_cases_ratio = 100.00-pass_cases_ratio-fail_cases_ratio
        pass_cases_ratio = format(pass_cases_ratio, '.2f')
        fail_cases_ratio = format(fail_cases_ratio, '.2f')
        unexcuted_cases_ratio = format(unexcuted_cases_ratio, '.2f')
        pie_data = [pass_cases_ratio, fail_cases_ratio, unexcuted_cases_ratio]
        # table_data是每个case的执行明细，pie_data是pass、fail、unexecuted百分比，pie_table_data是all、pass、fail、unexecuted用例数
        new_report = report.GenerateReport()
        new_report.generate_report(self.table_data, pie_data, pie_table_data, project_path)

if __name__ == "__main__":
    username = "hebingning"
    password = "hbn66AAA"
    test_pc_ip = "192.168.64.76"
    path_dict = {}
    env = "tsgx"
    is_log = 0
    sleep_time = 30
    vsys_id = 6
    api_host = "http://192.168.44.72"
    project_path = "D:/python_script/tsg_policy_api"
    # project_path = "D:/Document/Project-TSG/Code/git/tsg_policy_api"
    # project_path = "/tmp/pycharm_project_800"
    trex_workpath = "/opt/trex/v3.03"   # trex项目工作目录
    traffic_playback_workpath = f"{project_path}/traffic_replay"
    rule_template = f"{project_path}/data/template/rule_template.json"
    obj_template = f"{project_path}/data/template/object_template.json"
    profile_statistics_template = f"{project_path}/data/template/profile_statistics_template.json"
    profile_sff_template = f"{project_path}/data/template/profile_sff_template.json"
    profile_sf_template = f"{project_path}/data/template/profile_sf_template.json"
    pre_deny_quic_template = f"{project_path}/data/template/pre_deny_quic_template.json"
    pre_intercept_template = f"{project_path}/data/template/pre_intercept_template.json"
    profile_dns_record_template = f"{project_path}/data/template/profile_dns_record_template.json"
    temp_folder_path = f"{project_path}/data/case_data"
    profiles_hijack_file_path = f"{project_path}/data/upload_file/Create-hijack-Files-test-5.png"
    profiles_insert_profile_path = f"{project_path}/data/upload_file/Create-Insert-Script-test1.js"
    profiles_run_script_path = f"{project_path}/data/upload_file/run_script_hijack.lua"
    profiles_deny_path = f"{project_path}/data/upload_file/Response-Pages_1.html"
    url_file = f"{project_path}/data/upload_file/url.txt"
    fqdn_file = f"{project_path}/data/upload_file/fqdn.txt"
    path_dict["project_path"] = project_path
    path_dict["rule_template"] = rule_template
    path_dict["pre_deny_quic_template_path"] = pre_deny_quic_template
    path_dict["pre_intercept_template_path"] = pre_intercept_template
    path_dict["obj_template"] = obj_template
    path_dict["profile_statistics_template"] = profile_statistics_template
    path_dict["profile_sf_template"] = profile_sf_template
    path_dict["profile_sff_template"] = profile_sff_template
    path_dict["profiles_hijack_file_path"] = profiles_hijack_file_path
    path_dict["profiles_insert_profile_path"] = profiles_insert_profile_path
    path_dict["profiles_run_script_path"] = profiles_run_script_path
    path_dict["profiles_deny_path"] = profiles_deny_path
    path_dict["profile_dns_record_template"] = profile_dns_record_template
    path_dict["trex_workpath"] = trex_workpath
    path_dict["traffic_playback_workpath"] = traffic_playback_workpath
    folder_list = os.listdir(temp_folder_path)
    print("数据源包含的文件夹列表：", folder_list)
    # num1 = len(folder_list)
    # num2 = []
    # for i in range(num1):
    #     temp_path = temp_folder_path +'/' +folder_list[i]
    #     files2 = os.listdir(temp_path)
    #     num2.append(len(files2))
    # json_data = dict(zip(folder_list, num2))
    # for key,value in json_data.items():
    #     print('{key}包含文件数：{value}'.format(key = key, value = value))
    verify_res = Verify()
    verify_res.find_json_files(temp_folder_path)
    for j in range(len(folder_list)):
        folder_path = temp_folder_path + '/' + folder_list[j]
        path_dict["folder_path"] = folder_path
        verify_res.start_verify(username, password, test_pc_ip, api_host, is_log, path_dict, env, vsys_id)
        # verify_res.start_verify(username, password, test_pc_ip, api_host, is_log, path_dict, env, vsys_id, debug_json="security_deny_create_50w_fqdn.json")
    verify_res.build_report()
