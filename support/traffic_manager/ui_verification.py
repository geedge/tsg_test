# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import configparser
from support.ui_utils.policy.edit_rule import EditRule
from support.traffic_manager.workpath import workdir
from support.ui_utils.element_position.log_element_position import *
from support.ui_utils.element_position.map_element_position_library import *
from support.ui_utils.log.search_log import SearchLog
from selenium.webdriver.common.by import By
from datetime import datetime

class UiVerification:
    def ui_verification(self, driver, parameter, test_data, api_verification_result, test_rule_element_position, traffic_result, cfg_list):
        my_driver = driver
        policy_type = test_data["policy_type"]
        rule_action = test_data["rule_action"]
        is_log = parameter["is_log"]
        metric_result = False
        log_result = False
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule by ui.", flush=True)
        
        edit_rule = EditRule(my_driver)
        edit_rule_code, _ = edit_rule.edit(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
        if edit_rule_code == 200:
            if policy_type == "security" and rule_action != "shunt" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor" or policy_type == "statistics":
                # 判断api的metric_result为true，只是为了作为命中和生成log的基本判断，无其他特殊意义
                if api_verification_result[2] == True:
                    # 从ui上判断metric_result
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get hit count from UI detail page.", flush=True)
                    hit_count = -1
                    if policy_type == "statistics":  # 如果为Statistics Rule无对应的Log类型，则从Session Records查找
                        hit_count = my_driver.find_element(By.XPATH, statisticsRulePage_rightInfo_72hoursHitCount_posXpath).text
                    else:
                        hit_count = my_driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span[@class='hit-count']").text
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "hit_count:", hit_count, flush=True)
                    if int(hit_count) == test_data["counters"]["hits"] or int(hit_count) > 2 and test_data["counters"]["hits"] == "many":
                        metric_result = True
                    
                    # 从ui上判断log_result
                    if int(is_log) == 1 and policy_type != "statistics":
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log value from log page.", flush=True)
                        my_driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span[@class='hit-count']").click()
                        is_save_element = "//button[contains(@class, 'el-button el-button--default el-button--small el-button--primary operation-confirm-Leave')]"
                        element_exist_flag = my_driver.is_exist_element(is_save_element)
                        if element_exist_flag == True:
                            my_driver.find_element(By.XPATH, is_save_element).click()
                        time.sleep(1)
                        log_number_str = my_driver.find_element(By.XPATH, "//div[@class='search-addition-info search-row']//div").text
                        log_number = log_number_str.split(": ")[-1]
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "log_number:", log_number, flush=True)
                        # 等于0，则是bug，不需要进一步判断，直接返回false
                        if int(hit_count) == 0 or int(log_number) == 0:
                            if len(test_data['log_query_param']) == 0:
                                log_result = "no_set"
                            else:
                                log_result = False
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The value of hit_count or log_number is 0. The mean is: maybe it's a bug.", flush=True)
                        elif int(hit_count) == int(log_number) and 0 < int(hit_count) <= 2 :
                            # ui日志校验，以server ip为例，在log_query_list.ini中通过log api查找log ui的值
                            parse = configparser.ConfigParser()
                            parse_dir = os.path.join(workdir, "support", "traffic_manager", "log_query_list.ini")
                            parse.read(parse_dir, encoding="utf-8")
                            temp_log_result_list = []
                            # 点击展开
                            time.sleep(2)
                            my_driver.find_element(By.XPATH, "//i[@class='vxe-table--expand-btn vxe-icon-arrow-right']").click()
                            for t in range(len(test_data["log_query_param"])):
                                log_query_key = test_data["log_query_param"][t]["query_field_key"]
                                log_str = parse.get("log", log_query_key)
                                if log_query_key == "server_ip" or log_query_key == "decoded_as" or log_query_key == "client_ip":
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/parent::div//span[@class='el-dropdown-link popover-click color262626 el-dropdown-selfdefine']".format(replaceValue=log_str)
                                    temp_value = my_driver.find_element(By.XPATH, log_item_pos_xpath).text
                                    if temp_value == test_data["log_query_param"][t]["query_value"]:
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                # elif log_query_key == "ssl_cn" or log_query_key == "ssl_san" or log_query_key == "ssl_sni" or log_query_key == "ftp_account" or log_query_key == "security_action" or log_query_key == "ftp_url" or log_query_key == "ftp_link_type":
                                elif log_query_key in ["ssl_cn", "ssl_san", "ssl_sni", "ftp_account", "security_action", "ftp_url", "ftp_link_type", "mail_account", "mail_from","imsi", "phone_number", "server_fqdn", "ip_protocol", "mail_to", "mail_to_cmd", "mail_from_cmd", "mail_subject", "server_port"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                    temp_value = my_driver.find_element(By.XPATH, log_item_pos_xpath).text
                                    if temp_value == test_data["log_query_param"][t]["query_value"]:
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                elif log_query_key == "packet_capture_file":
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                    element_exist_flag = my_driver.is_exist_element(log_item_pos_xpath)
                                    # 验证开关开启
                                    if test_data["log_query_param"][t]["query_value"] == True:
                                        # 有下载按钮，点击下载按钮，验证是否报错
                                        if element_exist_flag == True:
                                            # 连续点击下载按钮5次（防止下载异常的时候异常信息消失的太快）
                                            for _ in range(5):
                                                log_item_element = my_driver.find_element_by_xpath(log_item_pos_xpath)
                                                my_driver.execute_script("arguments[0].scrollIntoView();", log_item_element)
                                                my_driver.find_element(By.XPATH, log_item_pos_xpath).click()
                                                time.sleep(1)
                                            log_item_element = my_driver.find_element_by_xpath(log_item_pos_xpath)
                                            my_driver.execute_script("arguments[0].scrollIntoView();", log_item_element)
                                            print("had scroll")
                                            my_driver.find_element(By.XPATH, log_item_pos_xpath).click()
                                            time.sleep(1)
                                            # 只有下载失败的时候界面才有此定位
                                            error_text_posXpath = "//div[contains(@class, 'el-message el-message--error')]"
                                            error_text_is_exist = my_driver.is_exist_element(error_text_posXpath)
                                            # 有错误提示，下载失败
                                            if error_text_is_exist == True:
                                                temp_log_result = False
                                            # 下载成功时无错误提示.

                                            else:
                                                temp_log_result = True
                                        else:
                                            # 没有下载按钮，false
                                            temp_log_result = False
                                    # 验证开关不开启
                                    elif test_data["log_query_param"][t]["query_value"] == False:
                                        if element_exist_flag == False:
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False
                                elif log_query_key in ["http_host", "http_url", "http_response_content_type", "http_user_agent", "http_version", "http_request_line", "http_response_line"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]".format(replaceValue=log_str)
                                    temp_value = my_driver.find_element(By.XPATH, log_item_pos_xpath).text.strip()
                                    #print(temp_value)
                                    #print(test_data["log_query_param"][t]["query_value"])
                                    if temp_value == test_data["log_query_param"][t]["query_value"]:
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                elif log_query_key in ["monitor_mirrored_bytes", "monitor_mirrored_pkts"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(
                                        replaceValue=log_str)
                                    temp_value = my_driver.find_element(By.XPATH, log_item_pos_xpath).text.strip()
                                    print(temp_value)
                                    print(test_data["log_query_param"][t]["query_value"])
                                    if int(temp_value.replace(',', '')) == int(test_data["log_query_param"][t]["query_value"]) :
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                            if False not in temp_log_result_list:
                                log_result = True
                            else:
                                log_result = False
                        elif int(hit_count) > 2 and test_data["counters"]["hits"] == "many":
                            log_result = True
                    elif int(is_log) == 1 and policy_type == "statistics":
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log value from session records page.", flush=True)
                        element_position_map = get_element_position("session_log")
                        search_log = SearchLog(driver)
                        sql = "has(statistics_rule_list,{})".format(test_data["rule_id"])
                        search_rule_code, total = search_log.search(sql, element_position_map)
                        if search_rule_code == 200:
                            log_number = total
                            log_result = True
                
                if metric_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], '"metric_result" of ui is {}. The mean is: the metrics match the expected value from test data.'.format(metric_result), flush=True)
                elif metric_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], '"metric_result" of ui is {}. The mean is: the metrics do not match the expected value from test data.'.format(metric_result), flush=True)

                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], '"log_result" of ui is {}. The mean is: the logs result match the expected value from test data.'.format(log_result), flush=True)
                elif log_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], '"log_result" of ui is {}. The mean is: the logs result do not match the expected value from test data.'.format(log_result), flush=True)
            
                return api_verification_result[0], log_result, metric_result, my_driver
            elif policy_type == "service_chaining":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get value of sent pkts, received pkts, sent bytes, received bytes from UI detail page.", flush=True)
                sent_pkts_str = my_driver.find_element(By.XPATH, "//td[normalize-space(text())='Sent Packets']/parent::tr//td[2]").text
                if sent_pkts_str == "-":
                    sent_pkts = 0
                else:
                    sent_pkts, sent_pkts_unit = self.extract_value("packets", sent_pkts_str)
                
                sent_bytes_str = my_driver.find_element(By.XPATH, "//td[normalize-space(text())='Sent Bytes']/parent::tr//td[2]").text
                if sent_bytes_str == "-":
                    sent_bytes = 0
                else:
                    sent_bytes, sent_bytes_unit = self.extract_value("bytes", sent_bytes_str)

                received_pkts_str = my_driver.find_element(By.XPATH, "//td[normalize-space(text())='Received Packets']/parent::tr//td[2]").text
                if received_pkts_str == "-":
                    received_pkts = 0
                else:
                    received_pkts, received_pkts_unit = self.extract_value("packets", received_pkts_str)

                received_bytes_str = my_driver.find_element(By.XPATH, "//td[normalize-space(text())='Received Bytes']/parent::tr//td[2]").text
                if received_bytes_str == "-":
                    received_bytes = 0
                else:
                    received_bytes, received_bytes_unit = self.extract_value("bytes", received_bytes_str)

                parse = configparser.ConfigParser()
                parse_dir = os.path.join(workdir, "configuration_file.ini")
                parse.read(parse_dir, encoding="utf-8")
                ip_str = parse.get("sc_active_dst_ip", "ip_list")
                sc_active_ip_list = ip_str.split(",")
                effective_device_tag = ["group-xxg-tsgx","center-xxg-tsgx"]
                # traffic_result = {'total_packets': 175, 'total_packets_sent': 45, 'total_packets_received': 130, 'total_bytes': 180025, 'total_bytes_sent': 5799, 'total_bytes_received': 174226, 'total_syn_pkt': 1}
                if len(traffic_result) > 0:
                    if sent_pkts == 0 and received_pkts == 0:
                        if cfg_list["sf_method"] == "vxlan_g":
                            if cfg_list["sf_dest_ip"] not in sc_active_ip_list:
                                metric_result = True
                            elif cfg_list["sf_dest_ip"] in sc_active_ip_list and cfg_list["admin_status"] == 0:
                                metric_result = True
                            elif cfg_list["device_tag"] not in effective_device_tag and cfg_list["load_balance_localization"] == "nearby":
                                metric_result = True
                            else:
                                metric_result = False
                        elif cfg_list["sf_method"] == "layer2_switch":
                            if cfg_list["admin_status"] == 0:
                                metric_result = True
                            elif cfg_list["device_tag"] not in effective_device_tag and cfg_list["load_balance_localization"] == "nearby":
                                metric_result = True
                            else:
                                metric_result = False
                    else:
                        if cfg_list["targeted_traffic"] == "raw":
                            byte_value = traffic_result["total_bytes"]
                            pkt_value = traffic_result["total_packets"]
                            if cfg_list["sf_method"] == "vxlan_g" and cfg_list["sf_dest_ip"] in sc_active_ip_list:
                                if 1000 <= pkt_value < 10000:
                                    pkt_value_temp = int(round(pkt_value/1000, 0))
                                elif pkt_value < 1000:
                                    pkt_value_temp = pkt_value
                                if 1024 <= byte_value < 1048576:
                                    total_bytes_temp = round(byte_value/1024.0, 2)
                                elif byte_value < 1024:
                                    total_bytes_temp = byte_value
                                elif 1048576 <= byte_value < 1073741824:
                                    total_bytes_temp = round(byte_value/1048576.0, 2)
                                if cfg_list["type"] == 1:
                                    if sent_bytes == received_bytes == total_bytes_temp and sent_pkts == received_pkts == pkt_value_temp:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                elif cfg_list["type"] == 2:
                                    if sent_bytes == total_bytes_temp and sent_pkts == pkt_value_temp and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False
                            elif cfg_list["sf_method"] == "layer2_switch":
                                if 1000 <= pkt_value < 10000:
                                    pkt_value_temp = int(round(pkt_value/1000, 0))
                                elif pkt_value < 1000: 
                                    pkt_value_temp = pkt_value
                                if 1024 <= byte_value < 1048576:
                                    total_bytes_temp = round(byte_value/1024.0, 2)
                                elif byte_value < 1024:
                                    total_bytes_temp = byte_value
                                elif 1048576 <= byte_value < 1073741824:
                                    total_bytes_temp = round(byte_value/1048576.0, 2)
                                if cfg_list["type"] == 2:
                                    if sent_bytes == total_bytes_temp and sent_pkts == pkt_value_temp and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False
                        elif cfg_list["targeted_traffic"] == "decrypted":
                            if cfg_list["sf_method"] == "vxlan_g" and cfg_list["sf_dest_ip"] in sc_active_ip_list:
                                if cfg_list["type"] == 1:
                                    if sent_bytes == received_bytes and sent_pkts == received_pkts:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                elif cfg_list["type"] == 2:
                                    if sent_bytes != 0 and sent_pkts != 0 and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False
                            elif cfg_list["sf_method"] == "layer2_switch":
                                if cfg_list["type"] == 2:
                                    if sent_bytes != 0 and sent_pkts != 0 and received_bytes == received_pkts == 0:
                                        metric_result = True
                                    else:
                                        metric_result = False
                                else:
                                    metric_result = False
                if int(is_log) == 1:
                    # 跳转至session record路径
                    sc_rule_id = test_data["rule_id"]
                    my_driver.find_element(By.ID,"Log").click()
                    my_driver.find_element(By.ID,"Log_SesssionRecords").click()
                    time.sleep(3)
                    # 以policy id作为filter查找命中策略的session
                    my_driver.find_element(By.ID,"addFilter").click()
                    time.sleep(1)
                    my_driver.find_element(By.XPATH,"//div[@class='el-input el-input--small el-input--suffix is-focus']//input").click()
                    my_driver.find_element(By.XPATH,"//div[@class='el-input el-input--small el-input--suffix is-focus']//input").send_keys("service")
                    time.sleep(1)
                    my_driver.find_element(By.ID,"Service Chaining Rule List26-_Label_UnrecognizedExp_Expression_groupItem_TagsSearch_FacedtedSearch_Search_VPanel_SessionLog_Home_App_anonymousComponent").click()
                    my_driver.find_element(By.ID,"operatorhas").click()
                    time.sleep(1)
                    my_driver.find_element(By.XPATH,"//div[@class='el-tooltip el-input el-input--mini']//input").send_keys(sc_rule_id)
                    my_driver.find_element(By.ID,"facedQuery").click()
                    time.sleep(1)
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log value from log page.", flush=True)
                    for i in range(50) :
                        log_number_str = my_driver.find_element(By.XPATH, "//div[@class='search-addition-info search-row']//div").text
                        log_number = log_number_str.split(": ")[-1]
                        if int(log_number) == 0:
                            i += 1
                            my_driver.find_element(By.ID,"facedQuery").click()
                            time.sleep(7)
                        elif int(log_number) > 0:
                            break
                    if int(log_number) == 0:
                        log_result = False
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Failed to get log value from log page.", flush=True)
                    else:
                        # 点击展开
                        time.sleep(3)
                        my_driver.find_element(By.XPATH, "//i[@class='vxe-table--expand-btn vxe-icon-arrow-right']").click()
                        parse = configparser.ConfigParser()
                        parse_dir = os.path.join(workdir, "support", "traffic_manager", "log_query_list.ini")
                        parse.read(parse_dir, encoding="utf-8")
                        temp_log_result_list = []
                        for t in range(len(test_data["log_query_param"])):
                            log_query_key = test_data["log_query_param"][t]["query_field_key"]
                            if log_query_key == "sc_rsp_raw" or log_query_key == "sc_rsp_raw":
                                test_data["log_query_param"][t]["query_value"] = cfg_list["sf_id_list"]
                            elif log_query_key == "sent_pkts":
                                test_data["log_query_param"][t]["query_value"] = traffic_result["total_packets_sent"]
                            elif log_query_key == "received_pkts":
                                test_data["log_query_param"][t]["query_value"] = traffic_result["total_packets_received"]
                            elif log_query_key == "sent_bytes":
                                test_data["log_query_param"][t]["query_value"] = traffic_result["total_bytes_sent"]
                            elif log_query_key == "received_bytes":
                                test_data["log_query_param"][t]["query_value"] = traffic_result["total_bytes_received"] 
                            log_str = parse.get("log", log_query_key)
                            if log_query_key == "sc_rsp_raw" or log_query_key == "sc_rsp_decrypted":
                                log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue1}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span \
                                    | //div[normalize-space(text())='{replaceValue2}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//div[@style='white-space: nowrap;']".format(replaceValue1=log_str,replaceValue2=log_str)
                                temp_value = my_driver.find_element(By.XPATH, log_item_pos_xpath).text
                                if temp_value == "[]":
                                    if cfg_list["sf_method"] == "vxlan_g":
                                        if cfg_list["sf_dest_ip"] not in sc_active_ip_list:
                                            temp_log_result = True
                                        elif cfg_list["sf_dest_ip"] in sc_active_ip_list and cfg_list["admin_status"] == 0:
                                            temp_log_result = True
                                        elif cfg_list["device_tag"] not in effective_device_tag and cfg_list["load_balance_localization"] == "nearby":
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False
                                    elif cfg_list["sf_method"] == "layer2_switch":
                                        if cfg_list["admin_status"] == 0:
                                            temp_log_result = True
                                        elif cfg_list["device_tag"] not in effective_device_tag and cfg_list["load_balance_localization"] == "nearby":
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False 
                                else:
                                    temp_value = temp_value.strip('[] ')   
                                    temp_value_list = temp_value.split(',')
                                    log_value_list = []
                                    for item in temp_value_list:
                                        log_value_list.append(int(item))
                                    if log_value_list == test_data["log_query_param"][t]["query_value"]:
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                            elif log_query_key == "sent_pkts" or log_query_key == "received_pkts":
                                log_pkt_value = test_data["log_query_param"][t]["query_value"]
                                log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                temp_value = int(my_driver.find_element(By.XPATH, log_item_pos_xpath).text)
                                if temp_value == log_pkt_value:
                                    temp_log_result = True
                                else:
                                    temp_log_result = False
                            elif log_query_key == "sent_bytes" or log_query_key == "received_bytes":
                                log_byte_value = test_data["log_query_param"][t]["query_value"]
                                if 1024 <= log_byte_value < 1048576:
                                    log_bytes_temp = str(round(log_byte_value/1024.0, 2)) + " KB"
                                elif log_byte_value < 1024:
                                    log_bytes_temp = str(log_byte_value) + " B"
                                elif 1048576 <= log_byte_value < 1073741824:
                                    log_bytes_temp = str(round(log_byte_value/1048576.0, 2)) + " MB"
                                log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                temp_value = my_driver.find_element(By.XPATH, log_item_pos_xpath).text
                                if temp_value == log_bytes_temp:
                                    temp_log_result = True
                                else:
                                    temp_log_result = False
                            temp_log_result_list.append(temp_log_result)
                        if False not in temp_log_result_list:
                                log_result = True
                        else:
                                log_result = False
                return api_verification_result[0], log_result, metric_result, my_driver
    
    def extract_value(self, type, value):
        if type == "packets":
            if " " in value:
                value_number = int(value.split(" ")[0])
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
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")