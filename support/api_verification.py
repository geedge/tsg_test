# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import requests
# import support.api_utils.get_log
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
from support.api_utils.organize_config import *
from support.get_metric_log import GetMetricLog

class APIVerification:
    def __init__(self, parameter, policy_configuration, traffic_generation, verification, configuration_manager):
        self.parameter = parameter
        self.policy_configuration = policy_configuration
        self.traffic_generation = traffic_generation
        self.verification = verification
        self.configuration_manager = configuration_manager
    
    def api_verification(self, traffic_result):
        try:
            is_log = self.parameter["is_log"]
            initiation_method = self.parameter["initiation_method"]
            if initiation_method == "ui":
                my_driver = self.configuration_manager["driver"]
            else:
                my_driver = ""
            for _, value in self.configuration_manager["rule_uuid_list"].items():
                self.rule_id = value[0]
            self.token = self.configuration_manager["token"]
            if "rule_number" in self.policy_configuration:
                self.rule_number = self.policy_configuration["rule_number"]
            else:
                self.rule_number = 1
            self.rule_type = self.policy_configuration["type"]
            
            get_metric_log = GetMetricLog(self.parameter, self.policy_configuration, self.traffic_generation, self.configuration_manager)
            if self.rule_type == "security" or self.rule_type == "pxy_intercept" or self.rule_type == "pxy_manipulation" or self.rule_type == "monitor" :
                # 获取开始时间
                utc_tz = pytz.timezone('UTC')
                current_utc_time = datetime.now(utc_tz) - timedelta(seconds=90)
                start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by api.", flush=True)
                metric_query_flag, log_query_flag = self.check_validation('metric_query', 'log_query')
                log_result, metric_result = None, None
                if int(is_log) == 1:
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
                else:
                    metric_result = "no_set"
                    log_result = "no_set"
                
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result by calling api is {}.'.format(metric_result), flush=True)
                elif metric_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result by calling api is {}.'.format(metric_result), flush=True)
                elif metric_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result by calling api is none.', flush=True)
                elif metric_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result by calling api is no_set.', flush=True)
                
                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result by calling api is {}.'.format(log_result), flush=True)
                elif log_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result by calling api is {}.'.format(log_result), flush=True)
                elif log_result == None:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result by calling api is none.', flush=True)
                elif log_result == "no_set":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result by calling api is no_set.', flush=True)
                
                return log_result, metric_result, my_driver
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "API verification Exception Error: ", str(e), flush=True)
            return "API verification Exception Error: " + str(e)
        
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
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Need verify metric.", flush=True)
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do not verify metric.", flush=True)
        if log_query_flag == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Need verify log.", flush=True)
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Do not Need verify log.", flush=True)
        return metric_query_flag, log_query_flag

    def verify_log(self, log_dict, traffic_result):
        log_query = self.verification['log_query']
        temp_log_result_list = []
        if len(log_dict) > 0 and len(log_query) > 0:
            for log in log_dict:
                for log_query_param in log_query:
                    query_field_key = log_query_param['query_field_key']
                    query_value = log_query_param['query_value']
                    exclude_fields = {
                        "packet_capture_file", "http_response_body", "http_request_body", "monitor_mirrored_pkts",
                        "monitor_mirrored_bytes", "client_port", "ssl_ech_flag", "ssl_esni_flag",
                        "attack_type", "sessions", "session_rate", "packets", "packet_rate","bytes", "bit_rate",
                        "basic_attack_type", "basic_sessions","basic_session_rate", "basic_packets", "basic_packet_rate","basic_bytes", "basic_bit_rate",
                        "rule_id","conditions"
                    }
                    if query_field_key in log and query_field_key not in exclude_fields and log[query_field_key] == query_value:
                        temp_log_result_list.append(True)
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
                    else:
                        temp_log_result_list.append(False)
                if self.rule_type == 'pxy_intercept' and len(temp_log_result_list) < len(log_query):
                    if True in temp_log_result_list:
                        log_result = True
                    else:
                        log_result = False
                elif False not in temp_log_result_list and len(log_dict) > 0:
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

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")