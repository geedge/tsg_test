# -*- coding: UTF-8 -*-
import configparser
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from support.packet_generator.workpath import workdir
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.map_element_position_library import *
from support.ui_utils.log.search_log import SearchLog
from support.ui_utils.policy.edit_rules import EditRules

class QueryRuleLog:
    def __init__(self, policy_configuration, verification_result, rule_uuids_tuple, driver, element_position, traffic_result):
        self.policy_configuration = policy_configuration
        self.verification_result = verification_result
        rule_uuids_list = list(rule_uuids_tuple)
        self.rule_uuid = rule_uuids_list["uuid"]
        self.driver = driver
        self.element_position = element_position
        self.traffic_result = traffic_result
    
    def query_rule_log(self):
        try:
            rule_type = self.policy_configuration["type"]
            rule_action = self.policy_configuration["action"]
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the policy rule log by ui.", flush=True)
            # 进入edit页面目的是为了找到hit count
            edit_rule = EditRules(self.driver)
            edit_rule_code, _ = edit_rule.edit(rule_type, rule_action, self.element_position)
            if edit_rule_code != 200:
                return "Fail to edit rule when ui verification."
            if rule_type == "security"  or rule_type == "proxy_intercept" or rule_type == "proxy_manipulation" or rule_type == "monitor" or rule_type == "statistics":
                if rule_type != "statistics" and rule_action != "shunt":
                    hit_count = -1
                    if rule_type == "statistics":
                        # 如果为Statistics Rule无对应的Log类型，则从Session Records查找
                        hit_count = self.driver.find_element(By.XPATH, statisticsRulePage_rightInfo_72hoursHitCount_posXpath).text
                    if rule_action == "shunt":
                        hit_count = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span").text
                    else:
                        hit_count = self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span[@class='hit-count']").text
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log value from log page.", flush=True)
                    self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span[@class='hit-count']").click()
                    is_save_element_exist = "//button[contains(@class, 'el-button el-button--default el-button--small el-button--primary operation-confirm-Leave')]"
                    element_exist_flag = self.driver.is_element_exist(is_save_element_exist)
                    if element_exist_flag == True:
                        self.driver.find_element(By.XPATH, is_save_element_exist).click()
                    time.sleep(3)
                    # 需要等待日志。为了Selenium Server保活，对页面进行如下操作：回退到策略页面再点击hit count跳转到log
                    for _ in range(90):
                        log_number_str = self.driver.find_element(By.XPATH, "//div[@class='search-addition-info search-row']//div[1]").text
                        log_number = log_number_str.split(": ")[-1]
                        if int(log_number) == 0 or int(hit_count) > int(log_number):
                            time.sleep(7)
                            self.driver.back()
                            self.driver.find_element(By.XPATH, "//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr//span[@class='hit-count']", find_before_wait_time=0.5).click()
                        else:
                            break
                    # 需要注意的是：negate要带着src ip，目的是减少更繁琐的判断，可复用下面的流程，如果是negate src ip，建议app选择除http和ssl外的协议
                    if self.verification_result["expected_metric"]["hits"] != "many":
                        # 等于0，则是bug，不需要进一步判断，直接返回false
                        if int(hit_count) == 0 or int(log_number) == 0:
                            if len(self.verification_result["expected_log"]) == 0:
                                log_result = "no_set"
                            else:
                                log_result = False
                                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The hit count or log number is 0. Maybe it's a bug, need to check.", flush=True)
                        elif int(hit_count) == int(log_number) and 0 < int(hit_count) <= 2:
                            parse = configparser.ConfigParser()
                            parse_dir = os.path.join(workdir, "support", "packet_generator", "log_query_list.ini")
                            parse.read(parse_dir, encoding="utf-8")
                            temp_log_result_list = []
                            # 点击展开
                            time.sleep(2)
                            self.driver.find_element(By.XPATH, "//i[@class='vxe-table--expand-btn vxe-icon-arrow-right']").click()
                            for t in range(len(self.verification_result["expected_log"])):
                                log_query_key = self.verification_result["expected_log"][t]["query_field_key"]
                                log_str = parse.get("log", log_query_key)
                                if log_query_key == "server_ip" or log_query_key == "decoded_as" or log_query_key == "client_ip":
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                    temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                                    if temp_value == self.verification_result["expected_log"][t]["query_value"]:
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                elif log_query_key in ["ssl_cn", "ssl_san", "ssl_sni", "ftp_account", "security_action", "ftp_url", "ftp_link_type", "mail_account", "mail_from","mail_attachment_name","imsi", "phone_number", "server_fqdn", "ip_protocol", "mail_to", "mail_to_cmd", "mail_from_cmd", "mail_subject", "dns_qname"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                    # 当不存在此定位时,value为空,日志查询与预期不符,置为false
                                    log_item_pos_exist = self.driver.is_element_exist(log_item_pos_xpath)
                                    if log_item_pos_exist == True:
                                        temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                                        if temp_value == self.verification_result["expected_log"][t]["query_value"]:
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                elif log_query_key  in {"packet_capture_file","http_response_body,http_request_body"}:   #日志中非结构文件断言
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                    element_exist_flag = self.driver.is_element_exist(log_item_pos_xpath)
                                    # 验证开关开启
                                    if self.verification_result["expected_log"][t]["query_value"] == True:
                                        # 有下载按钮，点击下载按钮，验证是否报错
                                        if element_exist_flag == True:
                                            # 连续点击下载按钮5次（防止下载异常的时候异常信息消失的太快）
                                            for _ in range(5):
                                                log_item_element = self.driver.find_element(By.XPATH,log_item_pos_xpath)
                                                self.driver.execute_script("arguments[0].scrollIntoView();", log_item_element)
                                                self.driver.find_element(By.XPATH, log_item_pos_xpath).click()
                                                time.sleep(1)
                                            log_item_element = self.driver.find_element(By.XPATH, log_item_pos_xpath)
                                            self.driver.execute_script("arguments[0].scrollIntoView();", log_item_element)
                                            self.driver.find_element(By.XPATH, log_item_pos_xpath).click()
                                            time.sleep(1)
                                            # 只有下载失败的时候界面才有此定位
                                            error_text_posXpath = "//div[contains(@class, 'el-message el-message--error')]"
                                            is_error_text_exist = self.driver.is_element_exist(error_text_posXpath)
                                            # 有错误提示，下载失败
                                            if is_error_text_exist == True:
                                                temp_log_result = False
                                            # 下载成功时无错误提示.
                                            else:
                                                temp_log_result = True
                                        else:
                                            # 没有下载按钮，false
                                            temp_log_result = False
                                    # 验证开关不开启
                                    elif self.verification_result["expected_log"][t]["query_value"] == False:
                                        if element_exist_flag == False:
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False
                                elif log_query_key in ["http_host", "http_url", "http_response_content_type", "http_user_agent", "http_version", "http_request_line", "http_response_line", "http_cookie", "http_set_cookie"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]".format(replaceValue=log_str)
                                    temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text.strip()
                                    #print("实际值:{}".format(temp_value))
                                    #print("预期值:{}".format(self.verification_result["expected_log"][t]["query_value"]))
                                    if temp_value == self.verification_result["expected_log"][t]["query_value"]:
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                elif log_query_key in ["proxy_pinning_status", "proxy_intercept_status", "proxy_passthrough_reason"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]".format(replaceValue=log_str)
                                    temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text.strip()
                                    #print("实际值:{}".format(temp_value))
                                    #print("预期值:{}".format(self.verification_result["expected_log"][t]["query_value"]))
                                    if temp_value == self.verification_result["expected_log"][t]["query_value"]:
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                elif log_query_key in ["server_port"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(
                                        replaceValue=log_str)
                                    temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text.strip()
                                    if int(temp_value.replace(',', '')) == int(self.verification_result["expected_log"][t]["query_value"]) :
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                                elif log_query_key == "monitor_mirrored_pkts":
                                        log_pkt_value = self.verification_result["expected_log"][t]["query_value"]
                                        log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                                        log_pkt_temp = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                                        temp_value = int(log_pkt_temp.replace(",", ""))
                                        if temp_value == log_pkt_value:
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False
                                        temp_log_result_list.append(temp_log_result)
                                elif log_query_key == "monitor_mirrored_bytes":
                                        log_byte_value = self.verification_result["expected_log"][t]["query_value"]
                                        log_bytes_temp = "" #对于bytes，之后还要进行处理
                                        if 1024 <= log_byte_value < 1048576:
                                            log_bytes_temp = str(round(log_byte_value / 1024.0, 2)) + " KB"
                                        elif log_byte_value < 1024:
                                            log_bytes_temp = str(log_byte_value) + " B"
                                        elif 1048576 <= log_byte_value < 1073741824:
                                            log_bytes_temp = str(round(log_byte_value / 1048576.0, 2)) + " MB"
                                        log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(
                                            replaceValue=log_str)
                                        temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                                        if temp_value == log_bytes_temp:
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False
                                        temp_log_result_list.append(temp_log_result)
                                elif log_query_key in ["client_port"]:
                                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(
                                        replaceValue=log_str)
                                    temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text.strip()
                                    temp_value = int(temp_value.replace(',', ''))
                                    # test_data中的client_port为string类型时,进行port的范围验证
                                    if type(self.verification_result["expected_log"][t]["query_value"]) == str:
                                        start, end = map(int, self.verification_result["expected_log"][t]["query_value"].split('-'))
                                        if start <= temp_value <= end:
                                            temp_log_result = True
                                        else:
                                            temp_log_result = False
                                    temp_log_result_list.append(temp_log_result)
                            if False not in temp_log_result_list:
                                log_result = True
                            else:
                                log_result = False
                        elif int(hit_count) > int(log_number):
                            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The hit count is greater than the log number, need to check.")
                            log_result = False
                    else:
                        log_result = True
                elif rule_type == "statistics":
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log value from session records page.", flush=True)
                    element_position_map = get_element_position("session_log")
                    search_log = SearchLog(self.driver)
                    sql = "has(statistics_rule_list,{})".format(self.rule_uuid)
                    search_rule_code, _ = search_log.search(sql, element_position_map)
                    if search_rule_code == 200:
                        log_result = True
                elif rule_action == "shunt":
                    log_result = "no_set"
                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result at ui page is {}.'.format(log_result), flush=True)
                elif log_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result at ui page is {}.'.format(log_result), flush=True)
                return log_result
            elif rule_type == "service_chaining":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log value from ui log page.", flush=True)
                sc_rule_uuid = self.rule_uuid
                parse = configparser.ConfigParser()
                parse_dir = os.path.join(workdir, "configuration_file.ini")
                parse.read(parse_dir, encoding="utf-8")
                ip_str = parse.get("sc_active_dst_ip", "ip_list")
                sc_active_ip_list = ip_str.split(",")
                effective_device_tag = ["group-xxg-tsgx", "center-xxg-tsgx"]
                self.driver.find_element(By.ID, "Log").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "Log_SesssionRecords").click()
                time.sleep(1.5)
                # 以policy id作为filter查找命中策略的session
                self.driver.find_element(By.ID, "addFilter").click()
                time.sleep(1)
                self.driver.find_element(By.XPATH, "//div[@class='el-input el-input--small el-input--suffix is-focus']//input").click()
                self.driver.find_element(By.XPATH, "//div[@class='el-input el-input--small el-input--suffix is-focus']//input").send_keys("service")
                time.sleep(1.5)
                self.driver.find_element(By.ID, "Service Chaining Rule List26-_Label_UnrecognizedExp_Expression_groupItem_TagsSearch_FacedtedSearch_Search_VPanel_SessionLog_Home_App_anonymousComponent").click()
                self.driver.find_element(By.ID, "operatorhas").click()
                time.sleep(1)
                self.driver.find_element(By.XPATH, "//div[@class='el-tooltip el-input el-input--mini']//input").send_keys(sc_rule_uuid)
                btn = self.driver.find_element(By.ID, "facedQuery")
                self.driver.execute_script("arguments[0].click()", btn)
                time.sleep(1.5)
                # 等待日志
                for _ in range(50) :
                    log_number_str = self.driver.find_element(By.XPATH, "//div[@class='search-addition-info search-row']//div[1]").text
                    log_number = log_number_str.split(": ")[-1]
                    if int(log_number) == 0:
                        self.driver.execute_script("arguments[0].click()", btn)
                        time.sleep(7)
                    elif int(log_number) > 0:
                        break
                negate_option = self.get_negate_option_from_configration()
                if int(log_number) == 0:
                    if negate_option == 1:
                        log_result = True
                    else:
                        log_result = False
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to get log value from log page.", flush=True)
                else:
                    time.sleep(0.5)
                    # 点击展开
                    btn = self.driver.find_element(By.XPATH, "//i[@class='vxe-table--expand-btn vxe-icon-arrow-right']")
                    self.driver.execute_script("arguments[0].click()", btn)
                    # self.driver.find_element(By.XPATH, "//i[@class='vxe-table--expand-btn vxe-icon-arrow-right']").click()
                    time.sleep(2)
                    parse = configparser.ConfigParser()
                    parse_dir = os.path.join(workdir, "support", "packet_generator", "log_query_list.ini")
                    parse.read(parse_dir, encoding="utf-8")
                    temp_log_result_list = []
                    sff_configuration = self.policy_configuration["action_parameter"]["sff_profiles"]
                    sf_configuration = self.policy_configuration["action_parameter"]["sff_profiles"][0]["service_func_profiles"]
                    for t in range(len(self.verification_result["expected_log"])):
                        log_query_key = self.verification_result["expected_log"][t]["query_field_key"]
                        if log_query_key == "sc_rsp_raw" or log_query_key == "sc_rsp_decrypted":
                            # self.verification_result["expected_log"][t]["query_value"] = sc_info["sf_id_list"]
                            print("手工获取下sf uuid？？")
                        elif log_query_key == "sent_pkts":
                            self.verification_result["expected_log"][t]["query_value"] = self.traffic_result["total_packets_sent"]
                        elif log_query_key == "received_pkts":
                            self.verification_result["expected_log"][t]["query_value"] = self.traffic_result["total_packets_received"]
                        elif log_query_key == "sent_bytes":
                            self.verification_result["expected_log"][t]["query_value"] = self.traffic_result["total_bytes_sent"]
                        elif log_query_key == "received_bytes":
                            self.verification_result["expected_log"][t]["query_value"] = self.traffic_result["total_bytes_received"] 
                        log_str = parse.get("log", log_query_key)
                        if log_query_key == "sc_rsp_raw" or log_query_key == "sc_rsp_decrypted":
                            log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue1}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span \
                                | //div[normalize-space(text())='{replaceValue2}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//div[@style='white-space: nowrap;']".format(replaceValue1=log_str, replaceValue2=log_str)
                            temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                            if temp_value == "[]":
                                if sf_configuration[0]["connectivity"]["method"] == "vxlan_g":
                                    if sf_configuration[0]["connectivity"]["sf_dest_ip"] not in sc_active_ip_list:
                                        temp_log_result = True
                                    elif sf_configuration[0]["connectivity"]["sf_dest_ip"] in sc_active_ip_list and sf_configuration[0]["admin_status"] == 0:
                                        temp_log_result = True
                                    elif sf_configuration[0]["device_group"]["tag"] not in effective_device_tag and sff_configuration[0]["load_balance_localization"] == "nearby":
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False
                                elif sf_configuration[0]["connectivity"]["method"] == "layer2_switch":
                                    if sf_configuration[0]["admin_status"] == 0:
                                        temp_log_result = True
                                    elif sf_configuration[0]["device_group"]["tag"] not in effective_device_tag and sff_configuration[0]["load_balance_localization"] == "nearby":
                                        temp_log_result = True
                                    else:
                                        temp_log_result = False 
                            else:
                                temp_value = temp_value.strip('[] ')   
                                temp_value_list = temp_value.split(',')
                                log_value_list = []
                                for item in temp_value_list:
                                    log_value_list.append(int(item))
                                if log_value_list == self.verification_result["expected_log"][t]["query_value"]:
                                    temp_log_result = True
                                else:
                                    temp_log_result = False
                        elif log_query_key == "sent_pkts" or log_query_key == "received_pkts":
                            log_pkt_value = self.verification_result["expected_log"][t]["query_value"]
                            log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                            log_pkt_temp = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                            temp_value = int(log_pkt_temp.replace(",",""))
                            if temp_value == log_pkt_value:
                                temp_log_result = True
                            else:
                                temp_log_result = False
                        elif log_query_key == "sent_bytes" or log_query_key == "received_bytes":
                            log_byte_value = self.verification_result["expected_log"][t]["query_value"]
                            if 1024 <= log_byte_value < 1048576:
                                log_bytes_temp = str(round(log_byte_value/1024.0, 2)) + " KB"
                            elif log_byte_value < 1024:
                                log_bytes_temp = str(log_byte_value) + " B"
                            elif 1048576 <= log_byte_value < 1073741824:
                                log_bytes_temp = str(round(log_byte_value/1048576.0, 2)) + " MB"
                            log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                            temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                            if temp_value == log_bytes_temp:
                                temp_log_result = True
                            else:
                                temp_log_result = False
                        elif log_query_key in ["ssl_esni_flag", "ssl_ech_flag", "ssl_sni", "ip_protocol", "imei", "imsi", "apn", "phone_number", "subscriber_id"]:
                            log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                            temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                            if temp_value == self.verification_result["expected_log"][t]["query_value"]:
                                temp_log_result = True
                            else:
                                temp_log_result = False
                        temp_log_result_list.append(temp_log_result)
                    if False not in temp_log_result_list:
                        log_result = True
                    else:
                        log_result = False
                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result at ui page is True', flush=True)    
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result at ui page is False', flush=True)
                return log_result
            elif rule_type == "dos_protection":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Get log value from log page.", flush=True)
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
                time.sleep(1.5)
                # 等待日志
                for _ in range(50) :
                    log_number_str = self.driver.find_element(By.XPATH, "//div[@class='search-addition-info search-row']//div[1]").text
                    log_number = log_number_str.split(": ")[-1]
                    if int(log_number) == 0:
                        self.driver.execute_script("arguments[0].click()", btn)
                        time.sleep(20)
                    elif int(log_number) > 0:
                        # 24.10版本后是否只有一条日志？？
                        break
                parse = configparser.ConfigParser()
                parse_dir = os.path.join(workdir, "support", "packet_generator", "log_query_list.ini")
                parse.read(parse_dir, encoding="utf-8")
                if int(log_number) == 2: #暂未添加tcp_syn_flood的校验
                    expand_element_postion = "//i[@class='vxe-table--expand-btn vxe-icon-arrow-right']"
                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue="Attack Type")
                    temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                    if temp_value == "Custom Network Attack":
                        query_key_list = ["attack_type", "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate"]
                    elif temp_value == "TCP SYN Flood" or temp_value == "UDP Flood" or temp_value == "DNS Flood" or temp_value == "NTP Flood":
                        query_key_list = ["basic_attack_type", "basic_sessions", "basic_session_rate", "basic_packets", "basic_packet_rate", "basic_bytes", "basic_bit_rate"]
                    temp_log_result_list = self.verify_dos_events(expand_element_postion, parse, query_key_list)
                elif int(log_number) == 1:
                    query_key_list_1 = ["attack_type", "sessions", "session_rate", "packets", "packet_rate", "bytes", "bit_rate","rule_uuid","conditions","destination_ip"]
                    expand_element_postion_1 = "//tr[1]//i[@class='vxe-table--expand-btn vxe-icon-arrow-right']"
                    temp_log_result_list = self.verify_dos_events(expand_element_postion_1, parse, query_key_list_1)
                if False not in temp_log_result_list:
                    log_result = True
                else:
                    log_result = False
                if log_result == True:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result at ui page is {}.'.format(log_result), flush=True)
                elif log_result == False:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The log result at ui page is {}.'.format(log_result), flush=True)
                return log_result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When querying rule log, the exception error: ", str(e), flush=True)
            return "When querying rule log, the exception error: " + str(e)
    
    def get_negate_option_from_configration(self):
        negate_option_list = []
        action_parameter = self.policy_configuration["action_parameter"]
        for i in range(len(action_parameter)):
            negate_option_list.append(action_parameter[i]["negate_option"])
        for value in negate_option_list:
            if value == 1:
                return 1
        return 0
    
    def verify_dos_events(self, expand_element_postion, parse, query_key_list):
        log_result_list = []
        self.driver.find_element(By.XPATH, expand_element_postion).click()
        for i in range(len(self.verification_result["expected_log"])):
            log_query_key = self.verification_result["expected_log"][i]["query_field_key"]
            if log_query_key in query_key_list:
                log_str = parse.get("log", log_query_key)
                log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                temp_value = self.driver.find_element(By.XPATH, log_item_pos_xpath).text
                log_query_value = self.verification_result["expected_log"][i]["query_value"]
                if log_query_key == "attack_type" or log_query_key == "basic_attack_type":
                    if log_query_value.replace("_", " ") == temp_value.lower():
                        log_result_list.append(True)
                    else:
                        log_result_list.append(False)
                elif log_query_key == "bit_rate" or log_query_key == "basic_bit_rate":
                    log_str = parse.get("log", log_query_key)
                    api_bit_rate_value = self.verification_result["expected_log"][i]["query_value"]

                    if api_bit_rate_value < 1024:
                        api_bit_rate_value = f"{round(api_bit_rate_value, 0)} b"
                    elif 1024 <= api_bit_rate_value < 1048576:
                        api_bit_rate_value = f"{round(api_bit_rate_value / 1000, 2)} K"
                    elif 1048576 <= api_bit_rate_value < 1073741824:
                        api_bit_rate_value = f"{round(api_bit_rate_value / 1048576, 2)} M"
                    else:
                        api_bit_rate_value = f"{round(api_bit_rate_value / 1073741824, 2)} G"
                    if api_bit_rate_value == temp_value: #String类型的比较
                        log_result_list.append(True)
                    else:
                        log_result_list.append(False)
                elif log_query_key in {"source_ip_list"}:  # 日志中非结构文件断言
                    log_item_pos_xpath = "//div[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class, 'FieldItem')]//div[contains(@class, 'field-value')]//span".format(replaceValue=log_str)
                    element_exist_flag = self.driver.is_element_exist(log_item_pos_xpath)
                    # 验证开关开启
                    if len(self.verification_result["expected_log"][i]["query_value"]) != 0 :
                        # 有下载按钮，点击下载按钮，验证是否报错
                        if element_exist_flag == True:
                            # 连续点击下载按钮5次（防止下载异常的时候异常信息消失的太快）
                            for _ in range(5):
                                log_item_element = self.driver.find_element(By.XPATH, log_item_pos_xpath)
                                self.driver.execute_script("arguments[0].scrollIntoView();", log_item_element)
                                self.driver.find_element(By.XPATH, log_item_pos_xpath).click()
                                time.sleep(1)
                            log_item_element = self.driver.find_element(By.XPATH, log_item_pos_xpath)
                            self.driver.execute_script("arguments[0].scrollIntoView();", log_item_element)
                            self.driver.find_element(By.XPATH, log_item_pos_xpath).click()
                            time.sleep(1)
                            # 只有下载失败的时候界面才有此定位
                            error_text_posXpath = "//div[contains(@class, 'el-message el-message--error')]"
                            is_error_text_exist = self.driver.is_element_exist(error_text_posXpath)
                            # 有错误提示，下载失败
                            if is_error_text_exist == True:
                                temp_log_result = False
                            # 下载成功时无错误提示.
                            else:
                                temp_log_result = True
                        else:
                            # 没有下载按钮，false
                            temp_log_result = False
                    # 验证开关不开启
                    elif self.verification_result["expected_log"][i]["query_value"]:
                        if element_exist_flag == False:
                            temp_log_result = True
                        else:
                            temp_log_result = False
                    log_result_list.append(temp_log_result)
                else:
                    if temp_value == str(log_query_value):
                        log_result_list.append(True)
                    else:
                        log_result_list.append(False)
        return log_result_list