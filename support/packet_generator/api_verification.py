# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import requests
import support.api_utils.get_log
import support.api_utils.policy_verify
import support.ui_utils.env
import subprocess
import configparser
import json
import platform
import pytz
import support.packet_generator.trex_replay as trex_replay
from support.packet_generator.workpath import workdir
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.api_utils.organize_config import *

class ApiVerification:
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
        is_multi_priority = test_data["is_multi_priority"]

        if is_multi_priority:
            rule_num = test_data["rule_num"]
        else:
            rule_num = 1
        
        if cfg_list == None:
            temp_list = {}
            temp_list[policy_type] = test_data["rule_id"]
            create_policies_ids = []
            create_policies_ids.append(temp_list)
        elif len(cfg_list) == 0:
            if policy_type == "service_chaining":
                cfg_list["rule_id"] = test_data["rule_id"]
                statistics_sc_info_list = []
                statistics_sc_info_list.append(cfg_list)
            temp_list = {}
            temp_list[policy_type] = test_data["rule_id"]
            create_policies_ids = []
            create_policies_ids.append(temp_list)
        elif len(cfg_list) != 0:
            create_policies_ids = cfg_list["create_policies_ids"]
            statistics_sc_info_list = cfg_list["statistics_sc_info_list"]
        policy_id_list = []
        for i in range(len(create_policies_ids)):
            policy_id_list.append(list(create_policies_ids[i].values())[0])
        
        log = support.api_utils.get_log.GetLog()
        if policy_type == "security" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor" :
            #如果是通过trex回放，需要替换src ip
            if test_data["policy_type"] == "monitor" and test_data["traffic"]["type"] == "trex":
                test_pc_ip = test_data["condition"]["source_ip"][0]["item"][0]["item_value"]
            # 获取开始时间
            utc_tz = pytz.timezone('UTC')
            current_utc_time = datetime.now(utc_tz) - timedelta(seconds=90)
            start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            output = traffic_result
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
            cmd_return = output
            
            expected_return = test_data["expected_return"]
            cmd_result = self.is_in(cmd_return, expected_return, debug_flag)
            
            loop_num = test_data["rule_num"]
            is_counters, is_log_query = self.is_verify(script_type, test_data, loop_num, 'counters', 'log_query_param')
            
            log_result, metric_result = None, None
            if int(is_log) == 1:
                if is_log_query == True or is_counters == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of parameter 'is_log' is True.", flush=True)
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Ready to get log and metric by api.", flush=True)
                    query_time = 70
                    if test_data["traffic"]["protocol"] == "mail":
                        query_time = 90
                    for i in range(int(query_time)):
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log and metric for the {} time.".format(i+1), flush=True)
                        if i == 30 and script_type == "ui" and driver:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Operate the browser to prevent timeout close.", flush=True)
                            support.ui_utils.env.teardown()
                            support.ui_utils.env.initiate_selenium_request()
                            my_driver = support.ui_utils.env.my_driver()
                            support.ui_utils.env.setup()
                        utc_tz = pytz.timezone('UTC')
                        current_utc_time = datetime.now(utc_tz)
                        end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        time.sleep(7)
                        if is_log_query == True and log_result == None:
                            log_result = log.get_log_by_condition(token, rule_num, start_time, end_time, test_pc_ip, test_sub_id, create_policies_ids, test_data, api_server, vsys_id, script_type,output)
                        if is_log_query == False:
                            log_result = "no_set"
                        if is_counters == True and metric_result == None:
                            metric_result = log.get_metric(token, rule_num, start_time, end_time, create_policies_ids, test_data, api_server, vsys_id, script_type)
                        if is_counters == False:
                            log_result = "no_set"
                        if log_result == False:
                            print("log_result....{}".format(log_result))
                            if i < 3:   # 允许失败3次，重新请求数据断言
                                log_result = None
                        if metric_result == False:
                            print("metric_result....{}".format(metric_result))
                            if i < 3:   # 允许失败3次，重新请求数据断言
                                metric_result = None
                        if log_result != None and metric_result != None:
                            break
            else:
                metric_result = "no_set"
                log_result = "no_set"
            
            if metric_result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is {}.'.format(metric_result), flush=True)
            elif metric_result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is {}.'.format(metric_result), flush=True)
            elif metric_result == None:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is none.', flush=True)
            elif metric_result == "no_set":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is no_set.', flush=True)
            
            if log_result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is {}.'.format(log_result), flush=True)
            elif log_result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is {}.'.format(log_result), flush=True)
            elif log_result == None:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is none.', flush=True)
            elif log_result == "no_set":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is no_set.', flush=True)
            
            return cmd_result, log_result, metric_result, my_driver
        elif policy_type == "statistics":      # statistics 数据校验
            # 获取开始时间
            utc_tz = pytz.timezone('UTC')
            current_utc_time = datetime.now(utc_tz)
            # 将时间向前推迟 180 秒，因为trex流量先发送。
            new_time = current_utc_time - timedelta(seconds=30)
            start_time = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            statistics_metircs_expect = traffic_result
            time.sleep(10)
            max_fail_count = 15    #  更具实际情况修改： 最大查询次数， 每次间隔search_interval_time 秒
            search_interval_time = 10    # 每次查询statistic metric的 间隔时间 单位秒
            if script_type == "ui":
                max_fail_count = 20    # 每次查询statistic metric的 间隔时间 单位秒
                #time.sleep(60)
            utc_tz = pytz.timezone('UTC')
            cmd_return = expected_return = test_data["expected_return"]
            code, statistics_template_chart_list = OrganizeConfig().organize_statistics_rule_cfg(parameter, test_data)
            if code != 200:
                return False, False, False, "Exception when getting Statistics Template information from the interface", my_driver  # 匹配其它策略模式
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'DEBUG：The expect result: {}'.format(statistics_metircs_expect), flush=True)
            if len(statistics_template_chart_list) > 0:  # 非空
                for statistics_info in statistics_template_chart_list:
                    fail_count = 0   #自增变量
                    while True:    # max_fail_count最大查询测试
                        if script_type == "ui":
                            # 点击 语言快捷切换按钮
                            element_language_menu = my_driver.find_element(By.XPATH, language_button_posXpath)
                            # 移动元素到页面，再执行点击
                            my_driver.execute_script("arguments[0].scrollIntoView();", element_language_menu)
                            my_driver.execute_script("arguments[0].click();", element_language_menu)
                        utc_tz = pytz.timezone('UTC')
                        current_utc_time = datetime.now(utc_tz)
                        end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        metric_results = log.get_livechart_statistics(token, start_time, end_time, statistics_info, statistics_metircs_expect, api_server, vsys_id)
                        metric_result = metric_results[0]
                        if metric_result == True:  # 返回结果不等于333，则退出循环查询
                            break
                        elif metric_result == 333 and metric_results[1] == "this is a pass":    # session的incoming outgoing,fqdn_category区分判断
                            metric_result = True    # 无法断言方向，强制通过
                            metric_results[1] = ""
                            break
                        else:   # 查询验证失败，再验证
                            metric_result = False
                            fail_count += 1
                            if fail_count >= max_fail_count:
                                break
                            time.sleep(search_interval_time)
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'DEBUG：Traffic Metric Verify Result:{}'.format(metric_result), flush=True)
            return metric_result, metric_result, metric_result, metric_results[1], my_driver    # 匹配其它策略模式
        elif policy_type == "service_chaining":
            #从配置文件中获取active ip list
            conf_path = os.path.join(workdir,"configuration_file.ini")
            conf = configparser.ConfigParser()
            conf.read(conf_path, encoding="utf-8")
            active_dest_ips_list = conf.get("sc_active_dst_ip","ip_list")
            effective_device_tag = ["group-xxg-tsgx","center-xxg-tsgx"]
            if test_data["targeted_traffic"] == "raw":
                # 获取开始时间
                time.sleep(30)
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=60)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
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
                            metric_result = log.get_sc_metric(token, start_time, end_time, sc_info, traffic_result, active_dest_ips_list, api_server, vsys_id)
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
                            elif sc_info["device_tag"] not in effective_device_tag and sc_info["load_balance_localization"] == "nearby":
                                metric_result = True
                            elif sc_info["is_negate"] == 1:
                                metric_result = True
                            else:
                                metric_result = False
                        elif sc_info["sf_method"] == "layer2_switch":
                            if sc_info["admin_status"] == 0:
                                metric_result = True
                            elif sc_info["device_tag"] not in effective_device_tag and sc_info["load_balance_localization"] == "nearby":
                                metric_result = True
                            elif sc_info["is_negate"] == 1:
                                metric_result = True
                            else:
                                metric_result = False
                    elif metric_result == 444:
                        metric_result = False
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The verification of service chaining api is passed", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(datetime.now().microsecond)[:3],"The verification of service chaining api is failed", flush=True)
                cmd_result = metric_result
            elif test_data["targeted_traffic"] == "decrypted":
                # 获取开始时间
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=30)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                # 等待时间，等待策略生效
                time.sleep(10)
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
                            elif sc_info["device_tag"] not in effective_device_tag and sc_info["load_balance_localization"] == "nearby":
                                metric_result = True
                            elif sc_info["is_negate"] == 1:
                                metric_result = True
                            else:
                                metric_result = False
                        elif sc_info["sf_method"] == "layer2_switch":
                            if sc_info["admin_status"] == 0:
                                metric_result = True
                            elif sc_info["device_tag"] not in effective_device_tag and sc_info["load_balance_localization"] == "nearby":
                                metric_result = True
                            elif sc_info["is_negate"] == 1:
                                metric_result = True
                            else:
                                metric_result = False
                    elif metric_result == 444:
                        metric_result = False
            return metric_result, cmd_result, metric_result, my_driver
        elif policy_type == "dos_protection":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
            output = traffic_result
            # 获取开始时间
            utc_tz = pytz.timezone('UTC')
            current_utc_time = datetime.now(utc_tz) - timedelta(seconds=90)
            start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            loop_num = test_data["rule_num"]
            is_counters, is_log_query = self.is_verify(script_type, test_data, loop_num, 'counters', 'log_query_param')
            
            log_result, metric_result = None, None
            if int(is_log) == 1:
                if is_log_query == True or is_counters == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of parameter 'is_log' is True.", flush=True)
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Ready to get log and metric by api.", flush=True)
                    for i in range(150):
                        if i in {30,60,90} and script_type == "ui" and driver:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Operate the browser to prevent timeout close.", flush=True)
                            support.ui_utils.env.teardown()
                            support.ui_utils.env.initiate_selenium_request()
                            my_driver = support.ui_utils.env.my_driver()
                            support.ui_utils.env.setup()
                        utc_tz = pytz.timezone('UTC')
                        current_utc_time = datetime.now(utc_tz)
                        end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        time.sleep(7)
                        if is_log_query == True and log_result == None:
                            log_result = log.get_log_by_condition(token, rule_num, start_time, end_time, test_pc_ip, test_sub_id, create_policies_ids, test_data, api_server, vsys_id, script_type,output)
                        if is_log_query == False:
                            log_result = "no_set"
                        if is_counters == True and metric_result == None:
                            metric_result = log.get_metric(token, rule_num, start_time, end_time, create_policies_ids, test_data, api_server, vsys_id, script_type)
                        if is_counters == False:
                            log_result = "no_set"
                        if log_result != None and metric_result != None:
                            break
            else:
                metric_result = "no_set"
                log_result = "no_set"
            
            if metric_result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is {}.'.format(metric_result), flush=True)
            elif metric_result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is {}.'.format(metric_result), flush=True)
            elif metric_result == None:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is none.', flush=True)
            elif metric_result == "no_set":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "metric_result" by calling api is no_set.', flush=True)
            
            if log_result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is {}.'.format(log_result), flush=True)
            elif log_result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is {}.'.format(log_result), flush=True)
            elif log_result == None:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is none.', flush=True)
            elif log_result == "no_set":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "log_result" by calling api is no_set.', flush=True)
            
            return True, log_result, metric_result, my_driver
        elif policy_type == "shaping":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added.")
            return True, True, True

    def is_in(self, full_str, sub_str, debug_flag):
        if sub_str == "trex":  #故若干
            cmd_result = True
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "cmd_result" is {}.'.format(cmd_result), flush=True)
            return cmd_result
        if debug_flag == "local":
            temp = full_str["result"]
        else:
            temp = full_str
        sub_str = sub_str.split(',')
        # 遍历sub_str中的每个单词，并检查该单词是否在full_str中
        cmd_result = all(word in temp for word in sub_str)
        if cmd_result == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "cmd_result" is {}.'.format(cmd_result), flush=True)
        elif cmd_result == False:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The value of parameter "cmd_result" is {}.'.format(cmd_result), flush=True)
        return cmd_result # 返回：True or False

    def is_verify(self, script_type, test_data, loop_num, counters, log_query_param):
        # 判断传入了验证日志、metric相关的参数
        is_counters = False
        is_log_query = False
        for i in range(loop_num):
            index = i + 1
            temp_counters = counters + '_' + str(index)
            if temp_counters in test_data.keys():
                counters_data = test_data[counters + '_' + str(index)]
            else:
                counters_data = test_data[counters]
            if counters_data != {}:
                is_counters = True
                break
        for i in range(loop_num):
            index = i + 1
            temp_log_query_param = log_query_param + '_' + str(index)
            if temp_log_query_param in test_data.keys():
                log_query_param_data = test_data[log_query_param + '_' + str(index)]
            else:
                log_query_param_data = test_data[log_query_param]
            if len(log_query_param_data) > 0:
                is_log_query = True
                break
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of parameter 'is_counters' is {}.".format(is_counters), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of parameter 'is_log_query' is {}.".format(is_log_query), flush=True)
        return is_counters, is_log_query
    
    def call_traffic_server(self, data, script_type, debug_flag):
        if debug_flag == "local":
            parse = configparser.ConfigParser()
            parse_dir = os.path.join(workdir, "configuration_file.ini")
            parse.read(parse_dir, encoding="utf-8")
            traffic_server = parse.get("traffic_server", "url")
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
    """
    log = support.api_utils.get_log.GetLog()
    token = "f4339216-6164-42fd-98f0-48f5cecf7154&41&"
    start_time, end_time = "2024-07-29T09:22:42Z","2024-08-02T09:22:42Z"
    statistics_info = {'rule_id': '281993', 'template_id': 43, 'chart_id': 121, 'chart_type': 'table', 'version': 1, 'sql': ' SELECT client_ip as "Client IP" ,sum(in_bytes) as "incoming bytes" ,sum(out_bytes) as "outgoing bytes" ,RATE(bytes, ${duration}, ${interval}) * 8 as "all bytes"  FROM statistics_rule WHERE  __time  >= \'${start_time}\' AND __time < \'${end_time}\'  AND ( ${filter} )  AND rule_id = ${rule_id} AND template_id = ${template_id} AND chart_id = ${chart_id} AND version = ${version} GROUP BY client_ip ORDER BY  "all bytes" desc LIMIT 100', 'metrics_dimension': {'metrics': {'incoming bytes': 'in_bytes', 'outgoing bytes': 'out_bytes', 'all bytes': 'bytes'}, 'dimensions': {'Client IP': 'client_ip'}}}
    statistics_metircs = {'clients_end': '10.64.21.202', 'clients_start': '10.64.21.202', 'servers_end': '2.1.1.3', 'servers_start': '2.1.1.3'}
    trex_ip_info = {'clients_end': '10.64.21.202', 'clients_start': '10.64.21.202', 'servers_end': '2.1.1.3', 'servers_start': '2.1.1.3'}
    test_data =test_data = {'is_multi_priority': False, 'rule_num': 1, 'policy_type': 'statistics', 'rule_name': 'stats_srcip_dstip_mail_imap_table_all_bytes_dim_client_ip', 'rule_action': 'statistics', 'rule_type': 'create', 'debug_flag': 'local', 'test_subcriber_id': 'test6489', 'script_type': 'ui', 'condition': {'source_ip': [{'name': 'stats_srcip_mail_imap_table_all_bytes_dim_client_ip', 'object_type': 'ip', 'select_type': False, 'negate': False, 'item': [{'item_operation': 'add', 'item_type': 'ipv4', 'item_value': '10.64.21.202'}]}], 'source_port': [], 'destination_ip': [{'name': 'stats_dstip_mail_imap_table_all_bytes_dim_client_ip', 'object_type': 'ip', 'select_type': False, 'negate': False, 'item': [{'item_operation': 'add', 'item_type': 'ipv4', 'item_value': '2.1.1.3'}]}], 'destination_port': [], 'internal_ip': [], 'internal_port': [], 'external_ip': [], 'external_port': [], 'source_geography': [], 'destination_geography': [], 'sub_id': [], 'device': [], 'tunnel': [], 'tunnel_level': [], 'flag': [], 'application': [{'name': 'mail', 'object_type': 'application', 'negate': False}], 'server_fqdn': [], 'protocol_filed': [], 'sub_action_override': True, 'sub_action': [], 'packet_capture': []}, 'action_parameter': {'statistics_template': [{'name': 'stats_mail_imap_table_all_bytes_dim_client_ip', 'profile_type': 'statistics_template', 'charts': [{'chart_name': 'stats_mail_imap_table_all_bytes_dim_client_ip', 'visualization_type': 'Table', 'metrics': ['in_bytes:SUM:incoming bytes', 'out_bytes:SUM:outgoing bytes', 'bytes:BITRATE:all bytes'], 'dimensions': ['client_ip'], 'order_by': 'all bytes', 'row_limit': '100', 'min_in_size': '0', 'max_out_size': '0'}]}]}, 'expected_return': 'reset', 'counters': {'hits': 1}, 'log_query_param': [{'query_field_key': 'app', 'query_value': 'imap'}], 'traffic': {'protocol': '', 'type': 'trex', 'clients_start_ip': '10.64.21.202', 'clients_end_ip': '10.64.21.202', 'servers_start_ip': '2.1.1.3', 'servers_end_ip': '2.1.1.3', 'm': 1, 'd': 1, 'yaml_name': 'test_https', 'pcap_name': 'mail_imap'}, 'statists_metric_results': [{'client_ip': '10.64.5.193', 'in_bytes': 17247, 'out_bytes': 1157083, 'bytes': 9394640}], 'token': 'f4339216-6164-42fd-98f0-48f5cecf7154&41&', 'rule_id': '281993'}
    script_type = "ui"
    vsys_id = 1
    api_server = "http://192.168.44.72"
    metric_results = log.get_livechart_statistics_2408(token, start_time, end_time, statistics_info, statistics_metircs,
                                                  trex_ip_info, test_data, api_server, vsys_id, script_type)
    """
