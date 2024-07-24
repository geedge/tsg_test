# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import support.api_utils.get_log
import support.api_utils.policy_verify
import support.ui_utils.env
import subprocess
import configparser
import json
import platform
import pytz
import support.traffic_manager.trex_replay as trex_replay
from support.traffic_manager.workpath import workdir
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from support.traffic_manager.traffic_replay import TrafficReplay

class ApiVerification():
    def api_verification(self, driver, parameter, test_data, traffic_result, cfg_list):
        my_driver = driver
        api_server = parameter["api_server"]
        script_type = parameter["script_type"]
        is_log = parameter["is_log"]
        test_pc_ip = parameter["test_pc_ip"]
        test_sub_id = parameter["test_subcriber_id"]
        vsys_id = parameter["vsys_id"]
        debug_flag = ""
        if "debug_flag" in parameter.keys():
            debug_flag = parameter["debug_flag"]
        token = test_data["token"]
        policy_type = test_data["policy_type"]
        isMultiPriority = test_data["is_multi_priority"]

        if isMultiPriority:
            rule_num = test_data["rule_num"]
        else:
            rule_num = 1
        
        if script_type == "ui":
            if policy_type == "service_chaining":
                statistics_sc_info_list = []
                cfg_list["rule_id"] = test_data["rule_id"]
                statistics_sc_info_list.append(cfg_list)
            elif policy_type == "statistics":
                statistics_sc_info_list = cfg_list["statistics_sc_info_list"]
                #cfg_list["rule_id"] = test_data["rule_id"]
                #statistics_sc_info_list.append(cfg_list)
            temp_list = {}
            temp_list[policy_type] = test_data["rule_id"]
            create_policies_ids = []
            create_policies_ids.append(temp_list)
        elif script_type == "api":
            if len(cfg_list) != 0:
                create_policies_ids = cfg_list["create_policies_ids"]
                statistics_sc_info_list = cfg_list["statistics_sc_info_list"]
        policy_id_list = []
        for i in range(len(create_policies_ids)):
            policy_id_list.append(list(create_policies_ids[i].values())[0])
        # 判断，如果condition中包含名为command的key，则读取command来执行，否则执行默认的
        
        log = support.api_utils.get_log.GetLog()
        
        if policy_type == "security" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor":
            # 获取开始时间
            utc_tz = pytz.timezone('UTC')
            current_utc_time = datetime.now(utc_tz) - timedelta(seconds=30)
            start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            print(start_time)
            
            # 等待时间，等待策略生效
            time.sleep(10)
            
            # 触发流量
            # if debug_flag == "local":
            #     temp_data = json.dumps(test_data["traffic"])
            #     output = self.call_traffic_server(temp_data, script_type, debug_flag)
            # else:
            #     output = self.call_traffic_server(test_data["traffic"], script_type, debug_flag)
            output = traffic_result
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
            cmd_return = output
            
            expected_return = test_data["expected_return"]
            cmd_result = self.is_in(cmd_return, expected_return, debug_flag)
            
            loop_num = test_data["rule_num"]
            is_counters, is_log_query = self.is_verify(script_type, test_data, loop_num, 'counters', 'log_query_param')
            
            log_result, metric_result = None, None
            if int(is_log) == 1:
                if is_log_query == 1 or is_counters == 1:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of 'is_log' is 1. Ready to get log and metric now.", flush=True)
                    for i in range(50):
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log and metric for the {} time.".format(i+1), flush=True)
                        if i == 10 and script_type == "ui" and driver:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Operate the browser to prevent timeout close.", flush=True)
                            support.ui_utils.env.teardown()
                            support.ui_utils.env.initiate_selenium_request()
                            my_driver = support.ui_utils.env.my_driver()
                            support.ui_utils.env.setup()
                        utc_tz = pytz.timezone('UTC')
                        current_utc_time = datetime.now(utc_tz)
                        end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        time.sleep(7)
                        if is_log_query == 1 and log_result == None:
                            log_result = log.get_log_by_condition(token, rule_num, start_time, end_time, test_pc_ip, test_sub_id, create_policies_ids, test_data, api_server, vsys_id, script_type)
                        if is_log_query == 0:
                            log_result = "no_set"
                        if is_counters == 1 and metric_result == None:
                            metric_result = log.get_metric(token, rule_num, start_time, end_time, create_policies_ids, test_data, api_server, vsys_id, script_type)
                        if is_counters == 0:
                            log_result = "no_set"
                        if log_result != None and metric_result != None:
                            break
            else:
                metric_result = "no_set"
                log_result = "no_set"
            
            if metric_result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "metric_result" is {}. The mean is: the metrics match the expected value from test data.'.format(metric_result), flush=True)
            elif metric_result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "metric_result" is {}. The mean is: the metrics do not match the expected value from test data.'.format(metric_result), flush=True)
            elif metric_result == None:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "metric_result" is none. The mean is: do not get metrics.', flush=True)
            elif metric_result == "no_set":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "metric_result" is no_set. The mean is: no need to get metrics.', flush=True)
            
            if log_result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "log_result" is {}. The mean is: the logs result match the expected value from test data.'.format(log_result), flush=True)
            elif log_result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "log_result" is {}. The mean is: the logs result do not match the expected value from test data.'.format(log_result), flush=True)
            elif log_result == None:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "log_result" is none. The mean is: do not get logs.', flush=True)
            elif log_result == "no_set":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "log_result" is no_set. The mean is: no need to get logs.', flush=True)
            
            return cmd_result, log_result, metric_result, my_driver
        elif policy_type == "statistics":      # statistics 使用trex流量回放验证
            # 获取开始时间
            time.sleep(5)
            utc_tz = pytz.timezone('UTC')
            current_utc_time = datetime.now(utc_tz)
            # 将时间向前推迟 8 分钟，因为trex流量先发送。
            new_time = current_utc_time - timedelta(seconds=30)
            start_time = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],'start_time', flush=True)
            # 解析trex使用参数， 解析client server ip
            # if script_type == "ui":
                # if "source_ip" in test_data["condition"].keys():
                #     source_ip = test_data["condition"]["source_ip"]
                #     for ip_item in source_ip:
                #         if "-" in ip_item["item"][0]["item_value"]:
                #             clients_start = ip_item["item"][0]["item_value"].split("-")[0]
                #             clients_end = ip_item["item"][0]["item_value"].split("-")[-1]
                #         else:
                #             clients_start = ip_item["item"][0]["item_value"]
                #             clients_end = clients_start
                # if "destination_ip" in test_data["condition"].keys():
                #     destination_ip = test_data["condition"]["destination_ip"]
                #     for ip_item in destination_ip:
                #         if "-" in ip_item["item"][0]["item_value"]:
                #             servers_start = ip_item["item"][0]["item_value"].split("-")[0]
                #             servers_end = ip_item["item"][0]["item_value"].split("-")[-1]
                #         else:
                #             servers_start = ip_item["item"][0]["item_value"]
                #             servers_end = servers_start
            if script_type == "api":
                # for ip_item in test_data["obj_condition_1"]:
                #     if "ATTR_SOURCE_IP" in ip_item.values():
                #         if "-" in ip_item["object_list"][0]["add_item_list"][0]["ip_address"]:
                #             clients_start = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[0]
                #             clients_end = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[-1]
                #         else:
                #             clients_start = ip_item["object_list"][0]["add_item_list"][0]["ip_address"]
                #             clients_end = clients_start
                #     if "ATTR_DESTINATION_IP" in ip_item.values():
                #         if "-" in ip_item["object_list"][0]["add_item_list"][0]["ip_address"]:
                #             servers_start = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[0]
                #             servers_end = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[-1]
                #         else:
                #             servers_start = ip_item["object_list"][0]["add_item_list"][0]["ip_address"]
                #             servers_end = servers_start
                verify_policy_break_count = 0
                for i in range(len(policy_id_list)):
                    while True:      # 多次策略验证
                        policy_id = policy_id_list[i]
                        verify_attribute_dict = {"src_ip": test_data["traffic"]["clients_start_ip"], "dst_ip": test_data["traffic"]["servers_start_ip"]}
                        policy_verify = support.api_utils.policy_verify.PolicyVerify()
                        hit_policy_list = policy_verify.policy_verify(test_data, verify_attribute_dict, token, api_server, vsys_id)
                        if policy_id in hit_policy_list:   # 策略生效，验证通过，跳出验证
                            break
                        if verify_policy_break_count > 40:    # 预计验证200秒，仍然不生效，则结束执行，报异常。
                            # 直接调用清空策略方法
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Invalid test, end test. Policy id: {}".format(policy_id), flush=True)
                            return False, False, False, "The policy verification fail."
                        verify_policy_break_count += 1
                        time.sleep(5)
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Interval {} second, result of the {} policy verification: policy verification fail, no effect of policy, {}policy id:{} ...".format(20*verify_policy_break_count, verify_policy_break_count, test_data["policy_type"], policy_id), flush=True)
            time.sleep(5)     # 策略验证通过后，延迟五秒启动流量回放
            # 执行回放命令
            # 将原数据中使用的ip替换为随机生成ip
            # test_data["traffic"]["clients_start_ip"] = clients_start
            # test_data["traffic"]["clients_end_ip"] = clients_end
            # test_data["traffic"]["servers_start_ip"] = servers_start
            # test_data["traffic"]["servers_end_ip"] = servers_end
            # if debug_flag == "local":
            #     temp_data = json.dumps(test_data["traffic"])
            #     statistics_result = self.call_traffic_server(temp_data, script_type, debug_flag)
            #     statistics_metircs = statistics_result["result"]
            # else:
            #     statistics_metircs = self.call_traffic_server(test_data["traffic"], script_type, debug_flag)
            statistics_metircs = traffic_result
            time.sleep(50)
            if script_type == "ui":
                # 点击 语言快捷切换按钮
                element_language_menu = my_driver.find_element(By.XPATH, language_button_posXpath)
                # 移动元素到页面，在执行点击
                my_driver.execute_script("arguments[0].scrollIntoView();", element_language_menu)
                my_driver.execute_script("arguments[0].click();", element_language_menu)
            utc_tz = pytz.timezone('UTC')
            current_utc_time = datetime.now(utc_tz)
            end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            cmd_return = expected_return = test_data["expected_return"]
            # 断言判断
            trex_ip_info = {}
            trex_ip_info["clients_start"] = test_data["traffic"]["clients_start_ip"]
            trex_ip_info["clients_end"] = test_data["traffic"]["clients_end_ip"]
            trex_ip_info["servers_start"] = test_data["traffic"]["servers_start_ip"]
            trex_ip_info["servers_end"] = test_data["traffic"]["servers_end_ip"]
            if len(statistics_sc_info_list) > 0:  # 非空
                for statistics_info in statistics_sc_info_list:
                    n = 1    #自增变量
                    fail_count = 1   #失败重试变量
                    while n < 20:
                        time.sleep(7)
                        if script_type == "ui":
                            # 点击 语言快捷切换按钮
                            element_language_menu = my_driver.find_element(By.XPATH, language_button_posXpath)
                            # 移动元素到页面，再执行点击
                            my_driver.execute_script("arguments[0].scrollIntoView();", element_language_menu)
                            my_driver.execute_script("arguments[0].click();", element_language_menu)
                        utc_tz = pytz.timezone('UTC')
                        current_utc_time = datetime.now(utc_tz)
                        end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        metric_results = log.get_livechart_statistics(token, start_time, end_time, statistics_info, statistics_metircs, trex_ip_info, test_data, api_server, vsys_id, script_type)
                        metric_result = metric_results[0]
                        if metric_result == True:  # 返回结果不等于333，则退出循环查询
                            break
                        elif metric_result == False:  # 查询验证失败时，再查询验证一次
                            if fail_count > 10:
                                break
                            fail_count += 1
                        elif  metric_results[0] == 333 and metric_results[1] == "this is a pass":    # session的incoming outgoing,fqdn_category区分判断
                            break
                        n += 1
                if  metric_results[0] == 333:     # API 查询失败时变量赋值
                    metric_result = False
                    if metric_results[1] == "this is a pass":     # incoming或者outgoing的session方向
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The direction of incoming or outgoing session is different from the actual flow direction, or the data is empty when fqdn_category is the dimension.")
                        metric_results[1] = ""
                        metric_result = True
            return metric_result, metric_result, metric_result, metric_results[1], my_driver    # 匹配其它策略模式
        elif policy_type == "service_chaining":
            active_dest_ips_list = ["2.2.2.53", "2.2.2.56", "2.2.2.57"] # vxlan时判断dest_ip是否在bfd探测为active的ip里
            if test_data["targeted_traffic"] == "raw":
                # 获取开始时间
                time.sleep(5)
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=30)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                # 解析trex使用参数， 解析client server ip
                # if script_type == "api":
                #     for ip_item in test_data["obj_condition_1"]:
                #         if "ATTR_SOURCE_IP" in ip_item.values():
                #             if "-" in ip_item["object_list"][0]["add_item_list"][0]["ip_address"]:
                #                 test_data["traffic"]["clients_start_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[0]
                #                 test_data["traffic"]["clients_end_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[-1]
                #             else:
                #                 test_data["traffic"]["clients_start_ip"] = test_data["traffic"]["clients_end_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"]
                #         if "ATTR_DESTINATION_IP" in ip_item.values():
                #             if "-" in ip_item["object_list"][0]["add_item_list"][0]["ip_address"]:
                #                 test_data["traffic"]["servers_start_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[0]
                #                 test_data["traffic"]["servers_end_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"].split("-")[-1]
                #             else:
                #                 test_data["traffic"]["servers_start_ip"] = test_data["traffic"]["servers_end_ip"] = ip_item["object_list"][0]["add_item_list"][0]["ip_address"]
                # elif script_type == "ui":
                #     for source_ip in test_data["condition"]["source_ip"]:
                #         if "-" in source_ip["item"][0]["item_value"]:
                #             test_data["traffic"]["clients_start_ip"] = source_ip["item"][0]["item_value"].split("-")[0]
                #             test_data["traffic"]["clients_end_ip"] = source_ip["item"][0]["item_value"].split("-")[-1]
                #         else:
                #             test_data["traffic"]["clients_start_ip"] = test_data["traffic"]["clients_end_ip"] = source_ip["item"][0]["item_value"]
                #     for dest_ip in test_data["condition"]["destination_ip"]:
                #         if "-" in dest_ip["item"][0]["item_value"]:
                #             test_data["traffic"]["servers_start_ip"] = dest_ip["item"][0]["item_value"].split("-")[0]
                #             test_data["traffic"]["servers_end_ip"] = dest_ip["item"][0]["item_value"].split("-")[-1]
                #         else:
                #             test_data["traffic"]["servers_start_ip"] = test_data["traffic"]["servers_end_ip"] = dest_ip["item"][0]["item_value"]
                # 执行回放命令
                # if debug_flag == "local":
                #     temp_data = json.dumps(test_data["traffic"])
                #     sc_result = self.call_traffic_server(temp_data, script_type, debug_flag)
                #     sc_metircs = sc_result["result"]
                # else:
                #     sc_metircs = self.call_traffic_server(test_data["traffic"], script_type, debug_flag)
                sc_metircs = traffic_result
                time.sleep(20)
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz)
                end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                cmd_return = expected_return = test_data["expected_return"]
                # 断言判断
                if len(statistics_sc_info_list) > 0:   # 非空
                    for sc_info in statistics_sc_info_list:
                        n = 0    #自增变量
                        fail_count = 0   #失败重试变量
                        while n <= 4:
                            utc_tz = pytz.timezone('UTC')
                            current_utc_time = datetime.now(utc_tz)
                            end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                            metric_result = log.get_sc_metric(token, start_time, end_time, sc_info, sc_metircs, active_dest_ips_list, api_server, vsys_id)
                            if metric_result == True:  # 返回结果不等于333，则退出循环查询
                                break
                            elif metric_result == False:  # 查询验证失败时，再查询验证两次
                                if fail_count >= 2:
                                    break
                                fail_count += 1
                            time.sleep(15)
                            n += 1
                    if metric_result == 333:
                        if sc_info["sf_method"] == "vxlan_g":
                            if sc_info["sf_dest_ip"] not in active_dest_ips_list:
                                metric_result = True
                            elif sc_info["sf_dest_ip"] in active_dest_ips_list and sc_info["admin_status"] == 0:
                                metric_result = True
                            else:
                                metric_result = False
                        elif sc_info["sf_method"] == "layer2_switch":
                            if sc_info["admin_status"] == 0:
                                metric_result = True
                            else:
                                metric_result = False
                    elif metric_result == 444:
                        metric_result = False
                cmd_result = metric_result
            elif test_data["targeted_traffic"] == "decrypted":
                # 获取开始时间
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=30)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                # 等待时间，等待策略生效
                time.sleep(10)
                # 触发流量
                # if debug_flag == "local":
                #     temp_data = json.dumps(test_data["traffic"])
                #     output = self.call_traffic_server(temp_data, script_type, debug_flag)
                # else:
                #     output = self.call_traffic_server(test_data["traffic"], script_type, debug_flag)
                output = traffic_result
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                cmd_return = output
                expected_return = test_data["expected_return"]
                # 获取结束时间
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz)
                end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                cmd_result = self.is_in(cmd_return, expected_return, debug_flag)
                if len(statistics_sc_info_list) > 0:  # 非空
                    for sc_info in statistics_sc_info_list:
                        n = 0  # 自增变量
                        fail_count = 0  # 失败重试变量
                        while n <= 4:
                            utc_tz = pytz.timezone('UTC')
                            current_utc_time = datetime.now(utc_tz)
                            end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                            metric_result = log.get_sc_metric(token, start_time, end_time, sc_info,"", active_dest_ips_list, api_server, vsys_id)
                            if metric_result == True:  # 返回结果不等于333，则退出循环查询
                                break
                            elif metric_result == False:  # 查询验证失败时，再查询验证两次
                                if fail_count >= 2:
                                    break
                                fail_count += 1
                            time.sleep(15)
                            n += 1
                    if metric_result == 333:
                        if sc_info["sf_method"] == "vxlan_g":
                            if sc_info["sf_dest_ip"] not in active_dest_ips_list:
                                metric_result = True
                            elif sc_info["sf_dest_ip"] in active_dest_ips_list and sc_info["admin_status"] == 0:
                                metric_result = True
                            else:
                                metric_result = False
                        elif sc_info["sf_method"] == "layer2_switch":
                            if sc_info["admin_status"] == 0:
                                metric_result = True
                            else:
                                metric_result = False
                    elif metric_result == 444:
                        metric_result = False
            return cmd_result, metric_result, metric_result, my_driver
        elif policy_type == "shaping":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added.")
            return True, True, True

    def is_in(self, full_str, sub_str, debug_flag):
        if debug_flag == "local":
            temp = full_str["result"]
        else:
            temp = full_str
        sub_str = sub_str.split(',')
        # 遍历sub_str中的每个单词，并检查该单词是否在full_str中
        cmd_result = all(word in temp for word in sub_str)
        if cmd_result == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "cmd_result" is {}. The mean is: the expected value is in the returned value from test data.'.format(cmd_result), flush=True)
        elif cmd_result == False:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of "cmd_result" is {}. The mean is: the expected value is not in the returned value from test data.'.format(cmd_result), flush=True)
        return cmd_result # 返回：True or False

    def is_verify(self, script_type, test_data, loop_num, counters, log_query_param):
        # 判断传入了验证日志、metric相关的参数
        is_counters = 0
        is_log_query = 0
        for i in range(loop_num):
            index = i + 1
            if script_type == "ui":
                counters_data = test_data[counters]
            elif script_type == "api":
                counters_data = test_data[counters + '_' + str(index)]
            if counters_data != {}:
                is_counters = 1
                break
        for i in range(loop_num):
            index = i + 1
            if script_type == "ui":
                log_query_param_data = test_data[log_query_param]
            elif script_type == "api":
                log_query_param_data = test_data[log_query_param + '_' + str(index)]
            if len(log_query_param_data) > 0:
                is_log_query = 1
                break
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of 'is_counters' is", is_counters, flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of 'is_log_query' is", is_log_query, flush=True)
        return is_counters, is_log_query
    
    def call_traffic_server(self, data, script_type, debug_flag):
        if debug_flag == "local":
            parse = configparser.ConfigParser()
            parse_dir = os.path.join(workdir, "configuration_file.ini")
            parse.read(parse_dir, encoding="utf-8")
            if script_type == "api":
                traffic_server = parse.get("traffic_server", "api_server_url")
            elif script_type == "ui":
                traffic_server = parse.get("traffic_server", "ui_server_url")
            port = parse.get("traffic_port", "server_port")
            url = traffic_server + ":" + port + "/v1/traffic"
            headers = {"Content-Type": "application/json"}
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send traffic for effect verification.", flush=True)
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], url, data)
            response = requests.post(url, data=data, headers=headers)
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], response.text)
            if response.status_code == 200:
                try:
                    jsonData = json.loads(response.text)
                except:    # json解析失败，直接返回json原文
                    jsonData = {}
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "json loads failed:", flush=True)
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{} {} \n{}".format(url, data, response.text), flush=True)
                    jsonData["result"] = response.text
            return jsonData
        else:
            type = data.get("type")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send traffic for effect verification.", flush=True)
            if type == "curl" or type == "wget" or type == "nslookup":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Execute {} operation.".format(type), flush=True)
                command = data.get("command")
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Excute Command: {}".format(command), flush=True)
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
                output, error = p.communicate()
                cmd_result = output + error
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Excute result: {}".format(cmd_result), flush=True)
            elif type == "trex":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Execute {} operation.".format(type), flush=True)
                pcap_name = data.get("pcap_name") + ".pcap"
                yaml_name = data.get("yaml_name") + ".yaml"
                m = data.get("m")
                d = data.get("d")
                clients_start_ip = data.get("clients_start_ip")
                clients_end_ip = data.get("clients_end_ip")
                servers_start_ip = data.get("servers_start_ip")
                servers_end_ip = data.get("servers_end_ip")
                path_dict = {
                    "trex_workpath": "/opt/trex/v3.05",
                    "traffic_playback_workpath": "/opt/tsg_test/support/traffic_replay"
                }
                path = "/opt/trex"
                entries = os.listdir(path)  
                dir_names = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
                if len(dir_names) == 1:
                    join_trex_workpath = "/opt/trex/{}".format(dir_names[0])
                    path_dict["trex_workpath"] = join_trex_workpath
                parse = configparser.ConfigParser()
                parse_dir = os.path.join(workdir, "configuration_file.ini")
                parse.read(parse_dir, encoding="utf-8")
                path_dict["traffic_playback_workpath"] = parse.get("traffic_playback", "traffic_playback_workpath")
                tr = trex_replay.TrafficReplay(path_dict)
                cmd_result = tr.trex_playback(yaml_name, pcap_name, m, d, clients_start_ip, clients_end_ip, servers_start_ip, servers_end_ip)
            return cmd_result

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")