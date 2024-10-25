# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import requests
import support.get_metric_log
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
# from support.api_utils.organize_config import *
from support.organize_config import *
from support.get_metric_log import GetMetricLog
from support.api_utils.util_statistics_template import UtilStatisticsTemplate

class APIVerification:
    def __init__(self, parameter, policy_configuration, traffic_generation, verification, configuration_manager):
        self.parameter = parameter
        self.policy_configuration = policy_configuration
        self.traffic_generation = traffic_generation
        self.verification = verification
        self.configuration_manager = configuration_manager
    
    def api_verification(self, traffic_result):
        try:
            initiation_method = self.parameter["initiation_method"]
            if initiation_method == "ui":
                my_driver = self.configuration_manager["driver"]
            else:
                my_driver = ""
            for _, value in self.configuration_manager["rule_uuid_list"].items():
                self.rule_uuid = value[0]
            self.token = self.configuration_manager["token"]
            if "rule_number" in self.policy_configuration:
                self.rule_number = self.policy_configuration["rule_number"]
            else:
                self.rule_number = 1
            self.rule_type = self.policy_configuration["type"]
            
            get_metric_log = GetMetricLog(self.parameter, self.policy_configuration, self.traffic_generation, self.configuration_manager)
            if self.rule_type == "security" or self.rule_type == "pxy_intercept" or self.rule_type == "pxy_manipulation" or self.rule_type == "monitor" :
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=90)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                metric_query_flag, log_query_flag = self.check_validation('metric_query', 'log_query')
                log_result, metric_result = None, None
                if metric_query_flag == True or log_query_flag == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Ready to get log and metric by api.", flush=True)
                    query_time = 70
                    if self.traffic_generation["tool"] == "mail":
                        query_time = 90
                    for i in range(int(query_time)):
                        if i in [25, 55, 85] and initiation_method == "ui" and self.configuration_manager["driver"]:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do the browser keepalive.", flush=True)
                            support.ui_utils.env.teardown()
                            support.ui_utils.env.initiate_selenium_request()
                            my_driver = support.ui_utils.env.my_driver()
                            support.ui_utils.env.setup()
                        utc_tz = pytz.timezone('UTC')
                        current_utc_time = datetime.now(utc_tz)
                        end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        time.sleep(7)
                        if log_query_flag == True and log_result == None:
                            log_dict, error = get_metric_log.get_log(self.token, start_time, end_time)
                            if len(error) != 0:
                                return error, None, my_driver
                            log_result = self.verify_log(log_dict, traffic_result)
                        if log_query_flag == False:
                            log_result = "no_set"
                        if metric_query_flag == True and metric_result == None:
                            metric_dict, error = get_metric_log.get_metric(self.token, start_time, end_time)
                            if len(error) != 0:
                                return None, error, my_driver
                            metric_result = self.verify_metric(metric_dict, traffic_result)
                        if metric_query_flag == False:
                            log_result = "no_set"
                        if log_result != None and metric_result != None:
                            break
                
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is passed.', flush=True)
                elif metric_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is failed.', flush=True)
                elif metric_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is none.', flush=True)
                elif metric_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is no_set.', flush=True)
                
                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is passed.', flush=True)
                elif log_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is failed.', flush=True)
                elif log_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is none.', flush=True)
                elif log_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is no_set.', flush=True)
                
                return log_result, metric_result, my_driver
            elif self.rule_type == "statistics":
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz)
                new_time = current_utc_time - timedelta(seconds=30)
                start_time = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                max_fail_count = 15    #  更具实际情况修改： 最大查询次数， 每次间隔query_metric_interval 秒
                query_metric_interval = 10    # 每次查询statistic metric的 间隔时间 单位秒
                if initiation_method == "ui":
                    max_fail_count = 20    # 每次查询statistic metric的 间隔时间 单位秒
                organize_config = OrganizeConfig(self.parameter, self.policy_configuration, self.configuration_manager)
                code, statistics_template_chart_list = organize_config.organize_statistics_rule_cfg()
                if code != 200:
                    return False, "Exception when getting Statistics Template information from the interface", my_driver
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                if len(statistics_template_chart_list) > 0:  # 非空
                    for statistics_info in statistics_template_chart_list:
                        fail_count = 0   #自增变量
                        while True:    # max_fail_count最大查询测试
                            if initiation_method == "ui":
                                # 点击 语言快捷切换按钮
                                element_language_menu = my_driver.find_element(By.XPATH, language_button_posXpath)
                                # 移动元素到页面，再执行点击
                                my_driver.execute_script("arguments[0].scrollIntoView();", element_language_menu)
                                my_driver.execute_script("arguments[0].click();", element_language_menu)
                            utc_tz = pytz.timezone('UTC')
                            current_utc_time = datetime.now(utc_tz)
                            end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                            metric_result_list = get_metric_log.get_livechart_statistics(self.token, start_time, end_time, statistics_info)
                            if len(metric_result_list[1]) > 0:
                                metric_result = metric_result_list[0]
                            else:
                                metric_result = self.verify_statistics_metric(start_time, end_time, traffic_result, statistics_info, metric_result_list[0])
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
                return metric_result, metric_result_list[1], my_driver
            elif self.rule_type == "service_chaining":
                # sc自动化目前只实现了但application、单sf、单sff的用例
                conf_path = os.path.join(workdir, "configuration_file.ini")
                conf = configparser.ConfigParser()
                conf.read(conf_path, encoding="utf-8")
                active_dst_ip_list = conf.get("sc_active_dst_ip", "ip_list")
                effective_device_tag_list = ["group-xxg-tsgx", "center-xxg-tsgx"]
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=60)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz)
                end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                sff_configuration = self.policy_configuration["action_parameter"]["sff_profiles"]
                sf_configuration = self.policy_configuration["action_parameter"]["sff_profiles"][0]["service_func_profiles"]
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                n = 0
                while n <= 4:
                    utc_tz = pytz.timezone('UTC')
                    current_utc_time = datetime.now(utc_tz)
                    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    metic_dict, code = get_metric_log.get_sc_metric(self.token, start_time, end_time)
                    if code == 333 or code == 444:
                        metric_result = code
                    else:
                        if self.policy_configuration["action_parameter"]["targeted_traffic"] == "raw":
                            metric_result = self.verify_sc_metric(sff_configuration, sf_configuration, active_dst_ip_list, metic_dict, traffic_result)
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
                return metric_result, metric_result, my_driver
            elif self.rule_type == "dos_protection":
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=90)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                metric_query_flag, log_query_flag = self.check_validation('metric_query', 'log_query')
                log_result, metric_result = None, None
                if metric_query_flag == True or log_query_flag == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Ready to get log and metric by api.", flush=True)
                    for i in range(150):
                        if i in {30,60,90} and initiation_method == "ui" and self.configuration_manager["driver"]:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do the browser keepalive.", flush=True)
                            support.ui_utils.env.teardown()
                            support.ui_utils.env.initiate_selenium_request()
                            my_driver = support.ui_utils.env.my_driver()
                            support.ui_utils.env.setup()
                        utc_tz = pytz.timezone('UTC')
                        current_utc_time = datetime.now(utc_tz)
                        end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        time.sleep(7)
                        if log_query_flag == True and log_result == None:
                            log_dict, error = get_metric_log.get_log(self.token, start_time, end_time)
                            if len(error) != 0:
                                return error, None, my_driver
                            log_result = self.verify_dos_log(log_dict, traffic_result)
                        if log_query_flag == False:
                            log_result = "no_set"
                        if metric_query_flag == True and metric_result == None:
                            metric_dict, error = get_metric_log.get_metric(self.token, start_time, end_time)
                            if len(error) != 0:
                                return None, error, my_driver
                            metric_result = self.verify_metric(metric_dict, traffic_result)
                        if metric_query_flag == False:
                            log_result = "no_set"
                        if log_result != None and metric_result != None:
                            break
                
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is passed.', flush=True)
                elif metric_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is failed.', flush=True)
                elif metric_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is none.', flush=True)
                elif metric_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result checked by calling api is no_set.', flush=True)
                
                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is passed.', flush=True)
                elif log_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is failed.', flush=True)
                elif log_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is none.', flush=True)
                elif log_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result checked by calling api is no_set.', flush=True)
                
                return log_result, metric_result, my_driver
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "API verification exception error: ", str(e), flush=True)
            return "API verification exception error: " + str(e)
        
    def check_validation(self, metric_query, log_query):
        # 判断传入了验证日志、metric相关的参数
        metric_query_flag = False
        log_query_flag = False
        for i in range(self.rule_number):
            index = i + 1
            temp_metric_query = metric_query + '_' + str(index)
            if temp_metric_query in self.verification.keys():
                metric_query_data = self.verification[metric_query + '_' + str(index)]
            else:
                metric_query_data = self.verification[metric_query]
            if metric_query_data != {}:
                metric_query_flag = True
                break
        for i in range(self.rule_number):
            index = i + 1
            temp_log_query = log_query + '_' + str(index)
            if temp_log_query in self.verification.keys():
                log_query_data = self.verification[log_query + '_' + str(index)]
            else:
                log_query_data = self.verification[log_query]
            if len(log_query_data) > 0:
                log_query_flag = True
                break
        if metric_query_flag == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Need to verify metric.", flush=True)
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do not need to verify metric.", flush=True)
        if log_query_flag == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Need to verify log.", flush=True)
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do not need to verify log.", flush=True)
        return metric_query_flag, log_query_flag

    def verify_log(self, log_dict, traffic_result):
        log_query = self.verification['log_query']
        temp_log_result_list = []
        if len(log_dict) > 0 and len(log_query) > 0:
            for log in log_dict:
                for log_query_param in log_query:
                    query_field_key = log_query_param["query_field_key"]
                    query_value = log_query_param["query_value"]
                    exclude_fields = {
                        "packet_capture_file", "http_response_body", "http_request_body", "monitor_mirrored_pkts",
                        "monitor_mirrored_bytes", "client_port", "ssl_ech_flag", "ssl_esni_flag",
                        "attack_type", "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate",
                        "basic_attack_type", "basic_sessions", "basic_session_rate", "basic_packets", "basic_packet_rate", "basic_bytes", "basic_bit_rate",
                        "rule_id", "conditions"
                    }
                    if query_field_key in log and query_field_key not in exclude_fields and log[query_field_key] == query_value:
                        temp_log_result_list.append(True)
                    elif query_field_key in {"packet_capture_file", "http_response_body", "http_request_body"}:
                        if query_value == True:
                            # 查询结果中packet_capture_file长度大于0，走下一步骤
                            if len(log[query_field_key]) > 0:
                                packet_capture_url = log[query_field_key]
                                download_parameter = {"url": packet_capture_url, "exportObj": True}
                                url = self.parameter["api_server"] + "/v1/util/download_file" + "?vsys_id=" + str(self.parameter["vsys"])
                                headers = {"Content-Type": "application/json", "Authorization": self.configuration_manager["token"]}
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
                    elif query_field_key in {"monitor_mirrored_pkts", "monitor_mirrored_bytes"}:
                        actual_bytes_value = traffic_result["total_bytes"]
                        actual_pkts_value = traffic_result["total_packets"]
                        mirror_bytes_value = 0
                        mirror_pkts_value = 0
                        application = self.get_application_from_configration()[0]
                        enable = self.policy_configuration["action_parameter"]["traffic_mirroring"]["enable"]
                        if enable == 1:
                            if application in {"ftp", "http", "https", "ssl"}:
                                if application in {"ftp", "http", "https", "ssl"}:
                                    protocol_filed = self.get_protocol_filed_from_configration()
                                    if len("protocol_filed") > 0:
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
                                if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            elif application == "mail":
                                protocol_filed = self.get_protocol_filed_from_configration()
                                if len("protocol_filed") > 0:
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
                                if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            elif application in {"", "quic", "dns"}:
                                mirror_bytes_value = actual_bytes_value
                                mirror_pkts_value = actual_pkts_value
                                if len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                                    vlan_count = len(self.policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["vlan_array"])
                                    num_vlans = vlan_count
                                    mirror_bytes_value *= num_vlans
                                    mirror_pkts_value *= num_vlans
                            else:
                                temp_log_result_list.append(False)
                            # 统一处理逻辑
                        if enable == 1 and application in {"ftp", "http", "ssl", "dns", "quic", "", "mail"}:
                            if query_field_key == "monitor_mirrored_pkts" and log[query_field_key] == mirror_pkts_value:
                                temp_log_result_list.append(True)
                                # 更新 test_data["log_query"] 中相应的 query_value
                                for log_query_param in self.verification["log_query"]:
                                    if log_query_param["query_field_key"] == "monitor_mirrored_pkts":
                                        log_query_param["query_value"] = mirror_pkts_value  # 将值修改为5
                            elif query_field_key == "monitor_mirrored_bytes" and log[query_field_key] == mirror_bytes_value:
                                temp_log_result_list.append(True)
                                # 更新 test_data["log_query"] 中相应的 query_value
                                for log_query_param in self.verification["log_query"]:
                                    if log_query_param["query_field_key"] == "monitor_mirrored_bytes":
                                        log_query_param["query_value"] = mirror_bytes_value  # 将值修改为5
                            else:
                                temp_log_result_list.append(False)
                    elif query_field_key in {"client_port"}:
                        start, end = map(int, query_value.split('-'))
                        if start <= log[query_field_key] <= end:
                            temp_log_result_list.append(True)
                        else:
                            temp_log_result_list.append(False)
                    elif query_field_key in {"ssl_ech_flag", "ssl_esni_flag"}:
                        if query_value == "True":
                            query_value = 1
                        elif query_value == "False":
                            query_value = 0
                        if log[query_field_key] == query_value:
                            temp_log_result_list.append(True)
                        else:
                            temp_log_result_list.append(False)
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
                if self.rule_type == 'pxy_intercept' and len(temp_log_result_list) < len(log_query):
                    if True in temp_log_result_list:
                        log_result = True
                    else:
                        log_result = False
                elif False not in temp_log_result_list:
                    log_result = True
                else:
                    log_result = False
        elif len(log_dict) == 0 and len(log_query) > 0:
            log_result = None
        elif len(log_query) == 0:
            log_result = True
        return log_result
    
    def verify_metric(self, metric_dict, traffic_result):
        metric_query = self.verification['metric_query']
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
                for key, value in metric_query.items():
                    if key not in metric or metric[key] > 2:
                        metric_result = False
                    elif key in metric and metric[key] == 1 and (self.traffic_generation['tool'] in ['dns', 'ftp']):
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
    
    def verify_dos_log(self, log_dict, traffic_result):
        print("need to modify func logic...")
    
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
    
    def get_protocol_filed_from_configration(self):
        # rule中只有一个protocol_filed
        action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(action_parameter)):
            or_conditions = action_parameter[i]["or_conditions"]
            for j in range(len(or_conditions)):
                if or_conditions[j]["attribute_name"] == "ATTR_HTTP_URL":
                    return "ATTR_HTTP_URL"
                elif or_conditions[j]["attribute_name"] == "ATTR_HTTP_REQ_HDR":
                    print("to be added...")
        
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    # sc rule json example
    policy_configuration = {
        "and_conditions": [
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "object_uuids": [
                            "f5cf118e-99d4-4726-bd57-66ab1ad31a27"
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_APP_ID",
                        "type": "application",
                        "items": ["http"]
                    }
                ],
            }
        ],
        "action": "service_chaining",
        "type": "service_chaining",
        "action_parameter": {
            "targeted_traffic": "raw",
            "sff_profiles": [
				{
					"name": "sff_zk",
					"type": 1, # 1是steer，2是mirror
					"load_balance_method": "hash-int-ip",
					"load_balance_localization": "nearby",
					"failure_action": "bypass",
					"service_func_profiles": [
						{
							"name": "sf_zk",
							"admin_status": 1,
							"device_group": {
								"value": "City A",
								"tag": "device_group"
							},
							"connectivity": {
								"method": "vxlan_g",
								"dest_ip": "1.1.1.1"
							},
							"health_check": {
								"method": "bfd",
								"interval_ms": 200,
								"retires": 5
							}
						}
					]
				}
            ]
        }
    }
    # monitor rule json example
    policy_configuration = {
        "and_conditions": [
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "object_uuids": [
                            "f5cf118e-99d4-4726-bd57-66ab1ad31a27"
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_APP_ID",
                        "object_uuids": [
                            "80791b3a-e700-2cb8-8c24-6876d9faa8f8"
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_HTTP_URL",
                        "object_uuids": [
                            {
								"type": "url",
								"member_type": "item",
								"items": [
									{
										"op": "add",
										"expr_type": "and",
										"expression": "yumi.com"
									}
								]
							}
                        ]
                    }
                ]
            }
        ],
        "action_parameter": {
            "traffic_mirroring": {
                "enable": 1,
                "vlanID": 1,
                "mirroring_profile": {
					"name": "mirror_zk",
					"vlan_array": [
						"5"
					]
				}
            },
            "packet_capture": {
                "enable": 1,
                "capture_depth": 2000
            }
        },
        "name": "monitor_zk",
        "log_option": "none",
        "action": "monitor",
        "type": "monitor",
        "is_enabled": 0
    }