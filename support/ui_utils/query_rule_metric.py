# -*- coding: UTF-8 -*-
import configparser
import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.policies.edit_rules import EditRules
from support.packet_generator.workpath import workdir

class QueryRuleMetric:
    def __init__(self, policy_configuration, verification_result, driver, element_position, traffic_result):
        self.policy_configuration = policy_configuration
        self.verification_result = verification_result
        self.driver = driver
        self.element_position = element_position
        self.traffic_result = traffic_result
        
    def query_rule_metric(self):
        try:
            rule_type = self.policy_configuration["type"]
            rule_action = self.policy_configuration["action"]
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the policy rule metric by ui.", flush=True)
            edit_rule = EditRules(self.driver)
            edit_rule_code, _ = edit_rule.edit(rule_type, rule_action, self.element_position)
            if edit_rule_code != 200:
                return "Fail to edit rule when ui verification."
            if rule_type == "security"  or rule_type == "proxy_intercept" or rule_type == "proxy_manipulation" or rule_type == "monitor" or rule_type == "statistics":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get hit count from ui detail page.", flush=True)
                hit_count = -1
                if rule_type == "statistics":
                    # 如果为Statistics Rule无对应的Log类型，则从Session Records查找
                    hit_count = self.driver.find_element(By.XPATH, statisticsRulePage_rightInfo_72hoursHitCount_posXpath).text
                if rule_action == "shunt":
                    hit_count = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span").text
                else:
                    hit_count = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span[@class='hit-count']").text
                if int(hit_count) == self.verification_result["expected_metric"]["hits"] or int(hit_count) > 0 and self.verification_result["expected_metric"]["hits"] == "many":
                    metric_result = True
                else:
                    metric_result = False
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result at ui page is {}.'.format(metric_result), flush=True)
                elif metric_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result at ui page is {}.'.format(metric_result), flush=True)
                return metric_result
            elif rule_type == "service_chaining":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get value of sent pkts, received pkts, sent bytes, received bytes from UI detail page.", flush=True)
                time.sleep(4)
                sent_pkts_str = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Sent Packets']/parent::tr//td[2]").text
                if sent_pkts_str == "-":
                    sent_pkts = 0
                else:
                    sent_pkts, _ = self.extract_value("packets", sent_pkts_str)
                sent_bytes_str = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Sent Bytes']/parent::tr//td[2]").text
                if sent_bytes_str == "-":
                    sent_bytes = 0
                else:
                    sent_bytes, _ = self.extract_value("bytes", sent_bytes_str)
                received_pkts_str = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Received Packets']/parent::tr//td[2]").text
                if received_pkts_str == "-":
                    received_pkts = 0
                else:
                    received_pkts, _ = self.extract_value("packets", received_pkts_str)
                received_bytes_str = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Received Bytes']/parent::tr//td[2]").text
                if received_bytes_str == "-":
                    received_bytes = 0
                else:
                    received_bytes, _ = self.extract_value("bytes", received_bytes_str)
                parse = configparser.ConfigParser()
                parse_dir = os.path.join(workdir, "configuration_file.ini")
                parse.read(parse_dir, encoding="utf-8")
                ip_str = parse.get("sc_active_dst_ip", "ip_list")
                sc_active_ip_list = ip_str.split(",")
                effective_device_tag = ["group-xxg-tsgx", "center-xxg-tsgx"]
                sff_configuration = self.policy_configuration["action_parameter"]["sff_profiles"]
                sf_configuration = self.policy_configuration["action_parameter"]["sff_profiles"][0]["service_func_profiles"]
                if len(self.traffic_result) > 0:
                    if sent_pkts == 0 and received_pkts == 0:
                        negate_option = self.get_negate_option_from_configration()
                        if sf_configuration[0]["connectivity"]["method"] == "vxlan_g":
                            if sf_configuration[0]["connectivity"]["sf_dest_ip"] not in sc_active_ip_list:
                                metric_result = True
                            elif sf_configuration[0]["connectivity"]["sf_dest_ip"] in sc_active_ip_list and sf_configuration[0]["admin_status"] == 0:
                                metric_result = True
                            elif sf_configuration[0]["device_group"]["tag"] not in effective_device_tag and sff_configuration[0]["load_balance_localization"] == "nearby":
                                metric_result = True
                            elif negate_option == 1:
                                metric_result = True
                            else:
                                metric_result = False
                        elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                            if sf_configuration[0]["admin_status"] == 0:
                                metric_result = True
                            elif sf_configuration[0]["device_group"]["tag"] not in effective_device_tag and sff_configuration[0]["load_balance_localization"] == "nearby":
                                metric_result = True
                            elif negate_option == 1:
                                metric_result = True
                            else:
                                metric_result = False
                    else:
                        if self.policy_configuration["action_parameter"]["targeted_traffic"] == "raw":
                            byte_value = self.traffic_result["total_bytes"]
                            pkt_value = self.traffic_result["total_packets"]
                            if sf_configuration[0]["connectivity"]["method"] == "vxlan_g" and sf_configuration[0]["connectivity"]["sf_dest_ip"] in sc_active_ip_list:
                                if 1000 <= pkt_value < 10000:
                                    pkt_value_temp = round(pkt_value/1000, 2)
                                elif pkt_value < 1000:
                                    pkt_value_temp = pkt_value
                                if 1024 <= byte_value < 1048576:
                                    total_bytes_temp = round(byte_value/1024.0, 2)
                                elif byte_value < 1024:
                                    total_bytes_temp = byte_value
                                elif 1048576 <= byte_value < 1073741824:
                                    total_bytes_temp = round(byte_value/1048576.0, 2)
                                if sff_configuration["type"] == 1:
                                    if sent_bytes == received_bytes == total_bytes_temp and sent_pkts == received_pkts == pkt_value_temp:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                elif sff_configuration["type"] == 2:
                                    if sent_bytes == total_bytes_temp and sent_pkts == pkt_value_temp and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False
                            elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                                if 1000 <= pkt_value < 10000:
                                    pkt_value_temp = round(pkt_value/1000, 2)
                                elif pkt_value < 1000: 
                                    pkt_value_temp = pkt_value
                                if 1024 <= byte_value < 1048576:
                                    total_bytes_temp = round(byte_value/1024.0, 2)
                                elif byte_value < 1024:
                                    total_bytes_temp = byte_value
                                elif 1048576 <= byte_value < 1073741824:
                                    total_bytes_temp = round(byte_value/1048576.0, 2)
                                if sff_configuration["type"] == 2:
                                    if sent_bytes == total_bytes_temp and sent_pkts == pkt_value_temp and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False
                        elif self.policy_configuration["action_parameter"]["targeted_traffic"] == "decrypted":
                            if sf_configuration[0]["connectivity"]["method"] == "vxlan_g" and sf_configuration[0]["connectivity"]["sf_dest_ip"] in sc_active_ip_list:
                                if sff_configuration["type"] == 1:
                                    if sent_bytes == received_bytes and sent_pkts == received_pkts:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                elif sff_configuration["type"] == 2:
                                    if sent_bytes != 0 and sent_pkts != 0 and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False
                            elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                                if sff_configuration["type"] == 2:
                                    if sent_bytes != 0 and sent_pkts != 0 and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False 
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result at ui page is True', flush=True)  
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result at ui page is False', flush=True)      
                return metric_result
            elif rule_type == "dos_protection":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get hit count from ui detail page.", flush=True)
                hit_count = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/following-sibling::td").text
                self.driver.find_element(By.ID, "Log").click()
                self.driver.find_element(By.ID, "Log_DosEventLogs").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "addFilter").click()
                self.driver.find_element(By.XPATH, "//div[@class='el-input el-input--small el-input--suffix is-focus']//input").click()
                self.driver.find_element(By.XPATH, "//div[@class='el-input el-input--small el-input--suffix is-focus']//input").send_keys("destination")
                self.driver.find_element(By.ID, "Destination IP8-_Label_UnrecognizedExp_Expression_groupItem_TagsSearch_FacedtedSearch_Search_VPanel_DosLog_Home_App_anonymousComponent").click()
                self.driver.find_element(By.ID, "operator=").click()
                for t in range(len(self.verification_result)):
                    if self.verification_result[t]["query_field_key"] == "destination_ip":
                        destination_ip = self.verification_result[t]["query_value"]
                self.driver.find_element(By.XPATH, "//div[@class='el-tooltip el-input el-input--mini']//input").send_keys(destination_ip)
                btn = self.driver.find_element(By.ID, "facedQuery")
                self.driver.execute_script("arguments[0].click()", btn)
                log_number_str = self.driver.find_element(By.XPATH, "//div[@class='search-addition-info search-row']//div[1]").text
                log_number = log_number_str.split(": ")[-1]
                if (int(hit_count) == self.verification_result["expected_metric"]["hits"]) or (self.verification_result["expected_metric"]["hits"] == "many" and int(log_number) != 0):
                    metric_result = True
                else:
                    metric_result = False
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result at ui page is {}.'.format(metric_result), flush=True)
                elif metric_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The metric result at ui page is {}.'.format(metric_result), flush=True)
                return metric_result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When querying rule metric, the exception error: ", str(e), flush=True)
            return "When querying rule metric, the exception error: " + str(e)
        
    def extract_value(self, type, value):
        if type == "packets":
            if " " in value:
                value_number = float(value.split(" ")[0])
                value_unit = value.split(" ")[-1]
            else:
                value_number = int(value)
                value_unit = ""
        elif type == "bytes":
            if " " in value:
                value_unit = value.split(" ")[-1]
                if value_unit == "B":
                    value_number = int(value.split(" ")[0])
                else:
                    value_number = float(value.split(" ")[0])
            else:
                value_number = 0
                value_unit = ""
        return value_number, value_unit
    
    def get_negate_option_from_configration(self):
        negate_option_list = []
        action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(action_parameter)):
            negate_option_list.append(action_parameter[i]["negate_option"])
        for value in negate_option_list:
            if value == 1:
                return 1
        return 0