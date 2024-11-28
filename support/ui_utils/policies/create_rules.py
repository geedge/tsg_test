# -*- coding: UTF-8 -*-
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
import traceback
from datetime import datetime
from telnetlib import EC
from trio import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.map_element_position_library import *
from support.ui_utils.policies.page_jump import PageJump

class CreateRules:
    def __init__(self, driver):
        self.driver = driver
        
    def create_rules(self, policy_configuration):
        try:
            # 目前所有object类型在json data中都只有一个？？
            # 根据rule type获取增删改查全部元素定位库，若有需要补充的，在下面或在map_element_position_library中追加
            element_position_library = get_element_position(policy_configuration["type"])
            page_jump_element_position = element_position_library["page_jump"]
            creation_element_position = element_position_library["create"]
            
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_policy_page(page_jump_element_position)

            # 点击create
            time.sleep(0.3)
            self.driver.find_element(By.XPATH, creation_element_position["policyRuleListPage_createButton_posXpath"]).click()
            
            # 输入name
            rule_name = policy_configuration["name"]
            time.sleep(0.5)
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_inputName_posXpath"]).send_keys(rule_name)
            
            # 选择action
            if policy_configuration["type"] == "security" or policy_configuration["type"] == "proxy_intercept" or policy_configuration["type"] == "dos_protection":
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectAction_posXpath"]).click()
            elif policy_configuration["type"] == "proxy_manipulation":
                if policy_configuration["action"] == "allow":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectAllow_posXpath"]).click()
                elif policy_configuration["action"] == "deny":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectDeny_posXpath"]).click()
                elif policy_configuration["action"] == "monitor":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectMonitor_posXpath"]).click()
                elif policy_configuration["action"] == "redirect":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectRedirect_posXpath"]).click()
                elif policy_configuration["action"] in ["replace", "hijack", "insert", "edit_element"]:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectModify_posXpath"]).click()
                # elif policy_configuration["action"] == "hijack":
                #     self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectHijack_posXpath"]).click()
                # elif policy_configuration["action"] == "insert":
                #     self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectInsert_posXpath"]).click()
                # elif policy_configuration["action"] == "edit_element":
                #     self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectEditElement_posXpath"]).click()
                else:
                    # run script
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectRunScript_posXpath"]).click()
            elif policy_configuration["type"]== "monitor":
                if policy_configuration["action_parameter"]["traffic_mirroring"]["enable"] == 1:
                    self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_mirrorTrafficButton_posXpath"]).click()
                if "log_option" in policy_configuration and policy_configuration["log_option"] == "all":
                    self.driver.find_element(By.XPATH,monitorRulePage_logOptions_all_posXpath).click()

            # 添加ip
            # 如果出现多个相同类型的attribute name，需要增加一个函数来判断该attribute name出现的次数
            src_ip_object_flag, src_ip_object_configuration, src_ip_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SOURCE_IP")
            src_ip_group_flag, src_ip_object_group_configuration, src_ip_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if src_ip_object_flag and src_ip_group_flag == False:
                self.add_ip(src_ip_object_configuration, "SrcIP", creation_element_position, src_ip_object_negate_option)
            if src_ip_object_flag and src_ip_group_flag:
                self.add_ip(src_ip_object_group_configuration, "SrcIP", creation_element_position, src_ip_object_group_negate_option)
            dst_ip_object_flag, dst_ip_object_configuration, dst_ip_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_DESTINATION_IP")
            dst_ip_object_group_flag, dst_ip_object_group_configuration, dst_ip_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if dst_ip_object_flag and dst_ip_object_group_flag == False:
                self.add_ip(dst_ip_object_configuration, "DstIP", creation_element_position, dst_ip_object_negate_option)
            if dst_ip_object_flag and dst_ip_object_group_flag:
                self.add_ip(dst_ip_object_group_configuration, "DstIP", creation_element_position, dst_ip_object_group_negate_option)
            internal_ip_object_flag, internal_ip_object_configuration, internal_ip_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_INTERNAL_IP")
            internal_ip_object_group_flag, internal_ip_object_group_configuration, internal_ip_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if internal_ip_object_flag and internal_ip_object_group_flag == False:
                self.add_ip(internal_ip_object_configuration, "InternalIP", creation_element_position, internal_ip_object_negate_option)
            if internal_ip_object_flag and internal_ip_object_group_flag:
                self.add_ip(internal_ip_object_group_configuration, "InternalIP", creation_element_position, internal_ip_object_group_negate_option)
            external_ip_object_flag, external_ip_object_configuration, external_ip_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_EXTERNAL_IP")
            external_ip_object_group_flag, external_ip_object_group_configuration, external_ip_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if external_ip_object_flag and external_ip_object_group_flag == False:
                self.add_ip(external_ip_object_configuration, "ExternalIP", creation_element_position, external_ip_object_negate_option)
            if external_ip_object_flag and external_ip_object_group_flag:
                self.add_ip(external_ip_object_group_configuration, "ExternalIP", creation_element_position, external_ip_object_group_negate_option)

            # 添加library作为ip
            
            # 添加port
            src_port_object_flag, src_port_object_configuration, src_port_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SOURCE_PORT")
            src_port_object_group_flag, src_port_object_group_configuration, src_port_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if src_port_object_flag and src_port_object_group_flag == False:
                self.add_port(src_port_object_configuration, "SrcPort", creation_element_position, src_port_object_negate_option)
            if src_port_object_flag and src_port_object_group_flag:
                self.add_port(src_port_object_group_configuration, "SrcPort", creation_element_position, src_port_object_group_negate_option)
            dst_port_object_flag, dst_port_object_configuration, dst_port_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_DESTINATION_PORT")
            dst_port_object_group_flag, dst_port_object_group_configuration, dst_port_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if dst_port_object_flag and dst_port_object_group_flag == False:
                self.add_port(dst_port_object_configuration, "DstPort", creation_element_position, dst_port_object_negate_option)
            if dst_port_object_flag and dst_port_object_group_flag:
                self.add_port(dst_port_object_group_configuration, "DstPort", creation_element_position, dst_port_object_group_negate_option)
            internal_port_object_flag, internal_port_object_configuration, internal_port_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_INTERNAL_PORT")
            internal_port_object_group_flag, internal_port_object_group_configuration, internal_port_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if internal_port_object_flag and internal_port_object_group_flag == False:
                self.add_port(internal_port_object_configuration, "InternalPort", creation_element_position, internal_port_object_negate_option)
            if internal_port_object_flag and internal_port_object_group_flag:
                self.add_port(internal_port_object_group_configuration, "InternalPort", creation_element_position, internal_port_object_group_negate_option)
            external_port_object_flag, external_port_object_configuration, external_port_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_EXTERNAL_PORT")
            external_port_object_group_flag, external_port_object_group_configuration, external_port_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if external_port_object_flag and external_port_object_group_flag == False:
                self.add_port(external_port_object_configuration, "ExternalPort", creation_element_position, external_port_object_negate_option)
            if external_port_object_flag and external_port_object_group_flag:
                self.add_port(external_port_object_group_configuration, "ExternalPort", creation_element_position, external_port_object_group_negate_option)
                
            # 添加subscriber id
            sub_id_object_flag, sub_id_object_configuration,sub_id_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SUBSCRIBER_ID")
            sub_id_objectgroup_flag, sub_id_object_group_configuration, sub_id_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if sub_id_object_flag and sub_id_objectgroup_flag == False:
                self.add_subid(sub_id_object_configuration, "User", creation_element_position, sub_id_object_negate_option)
            if sub_id_object_flag and sub_id_objectgroup_flag:
                self.add_subid(sub_id_object_group_configuration, "User", creation_element_position, sub_id_object_group_negate_option)

            # 添加device
            imsi_object_flag, imsi_object_configuration, imsi_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_IMSI")
            imsi_object_group_flag, imsi_object_group_configuration, imsi_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if imsi_object_flag and imsi_object_group_flag == False:
                self.add_device(creation_element_position, imsi_object_configuration["name"], imsi_object_negate_option)
            if imsi_object_flag and imsi_object_group_flag:
                print("todo")
            pn_object_flag, pn_object_configuration, pn_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_PHONE_NUMBER")
            pn_object_object_flag, pn_object_group_configuration, pn_object_gorup_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if pn_object_flag and pn_object_object_flag == False:
                self.add_device(creation_element_position, pn_object_configuration["name"], pn_object_negate_option)
            if pn_object_flag and pn_object_object_flag:
                print("todo")
            imei_object_attribute_flag, imei_object_configuration, imei_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_IMEI")
            imei_object_group_flag, imei_object_group_configuration, imei_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if imei_object_attribute_flag and imei_object_group_flag == False:
                self.add_device(creation_element_position, imei_object_configuration["name"], imei_object_negate_option)
            if imei_object_attribute_flag and imei_object_group_flag:
                print("todo")
            apn_object_flag, apn_object_configuration, apn_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_APN")
            apn_object_group_flag, apn_object_group_configuration, apn_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if apn_object_flag and apn_object_group_flag == False:
                self.add_device(creation_element_position, apn_object_configuration["name"], apn_object_negate_option)
            if apn_object_flag and apn_object_group_flag:
                print("todo")
            
            # 添加application
            application_object_flag, application_object_configuration, application_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_APP_ID")
            application_object_group_flag, application_object_group_configuration, application_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if application_object_flag and application_object_group_flag == False:
                if policy_configuration["type"] == "proxy_manipulation":
                    if application_object_configuration["items"][0].lower() == "doh":  # doh需要操作application
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addApplication_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchDoHApplication_posXpath"], find_before_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeApplication_posXpath"]).click()
                    else:   # 非doh不需要操作application
                        pass
                else:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addApplication_posXpath"]).click()
                    # 通过application name搜索并选中
                    for j in range(len(application_object_configuration["items"])):
                        if policy_configuration["type"] == "proxy_intercept":  # intercept 中 application不用搜索，直接选择
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectApplication_posXpath"].format(replaceValue=application_object_configuration["items"][j]), find_after_wait_time=0.5).click()
                        else:
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=1).send_keys(application_object_configuration["items"][j])
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectApplication_posXpath"].format(replaceValue=application_object_configuration["items"][j]), find_after_wait_time=0.5).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeApplication_posXpath"]).click()
            if application_object_flag and application_object_group_flag:
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addApplication_posXpath"]).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectApplicationGroupLabel_posXpath"]).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).clear()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=1).send_keys(application_object_group_configuration["items"][j])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectApplication_posXpath"].format(replaceValue=application_object_group_configuration["items"][j]), find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeApplication_posXpath"]).click()
                
            # 添加server fqdn
            fqdn_object_flag, fqdn_object_configuration, fqdn_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SERVER_FQDN")
            fqdn_object_group_flag, fqdn_object_group_configuration, fqdn_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if fqdn_object_flag and fqdn_object_group_flag == False:
                # 点add condition的+
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
                time.sleep(1)
                # 选中server fqdn
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addConditionServerFqdn_posXpath"]).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                # 点server fqdn的+，因为dst ip已经是第一层且t初始值是0，所以要+2
                # temp = t + 2
                # temp_element_position = creation_element_position["policyRulePage_addServerFqdn_posXpath"].format(replaceValue=temp)
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addServerFqdn_posXpath"]).click()
                time.sleep(1)
                # 通过server fqdn name搜索并选中
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchServerFqdn_posXpath"], find_after_wait_time=1).send_keys(fqdn_object_configuration["name"])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchServerFqdn_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                btn = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectServerFqdn_posXpath"].format(replaceValue=fqdn_object_configuration["name"]), find_after_wait_time=1)
                self.driver.execute_script("arguments[0].click()", btn)
                # self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectServerFqdn_posXpath"], find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeServerFqdn_posXpath"]).click()
                if fqdn_object_negate_option == True:
                    time.sleep(1)  # 暂停1秒
                    negate_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_negateServerFqdn_posXpath"])
                    # 使用JavaScript确保元素完全进入视图
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", negate_element)
                    # 使用JavaScript执行悬停
                    self.driver.execute_script("var evt = new MouseEvent('mouseover', {'view': window, 'bubbles': true, 'cancelable': true}); arguments[0].dispatchEvent(evt);", negate_element)
                    # 确保元素可点击后进行点击
                    self.driver.execute_script("arguments[0].click();", negate_element)
                    # ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                    # negate_element.click()
            if fqdn_object_flag and fqdn_object_group_flag:
                print("todo")
            # 添加library作为fqdn

            # 添加ip protocol
            ip_protocol_object_flag, ip_protocol_object_configuration, ip_protocol_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_IP_PROTOCOL")
            if ip_protocol_object_flag:
                self.add_ip_protocol(ip_protocol_object_configuration["items"][0], "IpProtocol", creation_element_position, ip_protocol_object_negate_option)

            # 添加protocol field
            protocol_filed_attribute_flag = False
            tmp_protocol_field_data_split_by_type = []   # 将 protocol_filed 分类临时存储
            tmp_url, tmp_request_header, tmp_response_header, tmp_request_body, tmp_response_body, tmp_ftp_account, tmp_ftp_content, tmp_cn, tmp_san, tmp_qname = [], [], [], [], [], [], [], [], [], []
            tmp_mail_account, tmp_mail_from, tmp_mail_to, tmp_mail_subject, tmp_mail_attachment_name, tmp_mail_content, tmp_mail_attachment_content, tmp_boolean= [], [], [], [], [], [], [], []
            tmp_cn_cat, tmp_san_cat, tmp_ech, tmp_esni, tmp_no_sni, tmp_ftp_uri, tmp_sip_ori_description, tmp_sip_res_description = [], [], [], [], [], [], [], []
            count = 1
            http_url_flag, http_url_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_HTTP_URL")
            if http_url_flag:
                protocol_filed_attribute_flag = True
                tmp_url.append(http_url_configuration)
                count += 1
                self.add_protocol_field(tmp_url, "Url", creation_element_position, count)
            http_req_header_flag, http_req_header_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_HTTP_REQ_HDR")
            if http_req_header_flag:
                protocol_filed_attribute_flag = True
                tmp_request_header.append(http_req_header_configuration)
                count += 1
                self.add_protocol_field(tmp_request_header, "RequestHeader", creation_element_position, count)
            http_res_header_flag, http_res_header_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_HTTP_RES_HDR")
            if http_res_header_flag:
                protocol_filed_attribute_flag = True
                tmp_response_header.append(http_res_header_configuration)
                count += 1
                self.add_protocol_field(tmp_response_header, "ResponseHeader", creation_element_position, count)
            http_req_body_flag, http_req_body_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_HTTP_REQ_BODY")
            if http_req_body_flag:
                protocol_filed_attribute_flag = True
                tmp_request_body.append(http_req_body_configuration)
                count += 1
                self.add_protocol_field(tmp_request_body, "RequestBody", creation_element_position, count)
            http_res_body_flag, http_res_body_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_HTTP_RES_BODY")
            if http_req_header_flag:
                protocol_filed_attribute_flag = True
                tmp_response_body.append(http_res_body_configuration)
                count += 1
                self.add_protocol_field(tmp_response_body, "ResponseBody", creation_element_position, count)
            ssl_cn_flag, ssl_cn_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SSL_CN")
            if ssl_cn_flag:
                protocol_filed_attribute_flag = True
                tmp_cn.append(ssl_cn_configuration)
                count += 1
                self.add_protocol_field(tmp_cn, "Cn", creation_element_position, count)
            ssl_cn_cat_flag, ssl_cn_cat_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SSL_CN_CAT")
            if ssl_cn_cat_flag:
                protocol_filed_attribute_flag = True
                tmp_cn_cat.append(ssl_cn_cat_configuration)
                count += 1
                self.add_protocol_field(tmp_cn_cat, "CnCat", creation_element_position, count)
            ssl_san_flag, ssl_san_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SSL_SAN")
            if ssl_san_flag:
                protocol_filed_attribute_flag = True
                tmp_san.append(ssl_san_configuration)
                count += 1
                self.add_protocol_field(tmp_san, "San", creation_element_position, count)
            ssl_san_cat_flag, ssl_san_cat_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SSL_SAN_CAT")
            if ssl_san_cat_flag:
                protocol_filed_attribute_flag = True
                tmp_san_cat.append(ssl_san_cat_configuration)
                count += 1
                self.add_protocol_field(tmp_san_cat, "SanCat", creation_element_position, count)
            ssl_ech_flag, ssl_ech_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SSL_ECH")
            if ssl_ech_flag:
                protocol_filed_attribute_flag = True
                tmp_ech.append(ssl_ech_configuration)
                count += 1
                self.add_bool_type_protocol_field(tmp_ech, "Ech", creation_element_position, count)
            ssl_esni_flag, ssl_esni_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SSL_ESNI")
            if ssl_esni_flag:
                protocol_filed_attribute_flag = True
                tmp_esni.append(ssl_esni_configuration)
                count += 1
                self.add_bool_type_protocol_field(tmp_esni, "Esni", creation_element_position, count)
            ssl_no_sni_flag, ssl_no_sni_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SSL_NO_SNI")
            if ssl_no_sni_flag:
                protocol_filed_attribute_flag = True
                tmp_no_sni.append(ssl_no_sni_configuration)
                count += 1
                self.add_bool_type_protocol_field(tmp_no_sni, "NoSni", creation_element_position, count)
            dns_qname_flag, dns_qname_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_DNS_QNAME")
            if dns_qname_flag:
                protocol_filed_attribute_flag = True
                tmp_qname.append(dns_qname_configuration)
                count += 1
                self.add_protocol_field(tmp_qname, "Qname", creation_element_position, count)
            mail_subject_flag, mail_subject_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_MAIL_SUBJECT")
            if mail_subject_flag:
                protocol_filed_attribute_flag = True
                tmp_mail_subject.append(mail_subject_configuration)
                count += 1
                self.add_protocol_field(tmp_mail_subject, "MailSubject", creation_element_position, count)
            mail_content_flag, mail_content_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_MAIL_CONTENT")
            if mail_content_flag:
                protocol_filed_attribute_flag = True
                tmp_mail_content.append(mail_content_configuration)
                count += 1
                self.add_protocol_field(tmp_mail_content, "MailContent", creation_element_position, count)
            mail_att_name_flag, mail_att_name_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_MAIL_ATT_NAME")
            if mail_att_name_flag:
                protocol_filed_attribute_flag = True
                tmp_mail_attachment_name.append(mail_att_name_configuration)
                count += 1
                self.add_protocol_field(tmp_mail_attachment_name, "MailAttachmentName", creation_element_position, count)
            mail_att_content_flag, mail_att_content_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_MAIL_ATT_CONTENT")
            if mail_att_content_flag:
                protocol_filed_attribute_flag = True
                tmp_mail_attachment_content.append(mail_att_content_configuration)
                count += 1
                self.add_protocol_field(tmp_mail_attachment_content, "MailAttachmentContent", creation_element_position, count)
            mail_from_flag, mail_from_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_MAIL_FROM")
            if mail_from_flag:
                protocol_filed_attribute_flag = True
                tmp_mail_from.append(mail_from_configuration)
                count += 1
                self.add_protocol_field(tmp_mail_from, "MailFrom", creation_element_position, count)
            mail_to_flag, mail_to_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_MAIL_TO")
            if mail_to_flag:
                protocol_filed_attribute_flag = True
                tmp_mail_to.append(mail_to_configuration)
                count += 1
                self.add_protocol_field(tmp_mail_to, "MailTo", creation_element_position, count)
            mail_account_flag, mail_account_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_MAIL_ACCOUNT")
            if mail_account_flag:
                protocol_filed_attribute_flag = True
                tmp_mail_account.append(mail_account_configuration)
                count += 1
                self.add_protocol_field(tmp_mail_account, "MailAccount", creation_element_position, count)
            ftp_uri_flag, ftp_uri_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_FTP_URI")
            if ftp_uri_flag:
                protocol_filed_attribute_flag = True
                tmp_ftp_uri.append(ftp_uri_configuration)
                count += 1
                self.add_protocol_field(tmp_ftp_uri, "FtpUri", creation_element_position, count)
            ftp_content_flag, ftp_content_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_FTP_CONTENT")
            if ftp_content_flag:
                protocol_filed_attribute_flag = True
                tmp_ftp_content.append(ftp_content_configuration)
                count += 1
                self.add_protocol_field(tmp_ftp_content, "FtpContent", creation_element_position, count)
            ftp_account_flag, ftp_account_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_FTP_ACCOUNT")
            if ftp_account_flag:
                protocol_filed_attribute_flag = True
                tmp_ftp_account.append(ftp_account_configuration)
                count += 1
                self.add_protocol_field(tmp_ftp_account, "FtpAccount", creation_element_position, count)
            sip_ori_description_flag, sip_ori_description_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SIP_ORIGINATOR_DESCRIPTION")
            if sip_ori_description_flag:
                protocol_filed_attribute_flag = True
                tmp_sip_ori_description.append(sip_ori_description_configuration)
                count += 1
                self.add_protocol_field(tmp_sip_ori_description, "SipOriDescription", creation_element_position, count)
            sip_res_description_flag, sip_res_description_configuration = self.is_protocol_filed_exsit(policy_configuration, "ATTR_SIP_RESPONDER_DESCRIPTION")
            if sip_res_description_flag:
                protocol_filed_attribute_flag = True
                tmp_sip_res_description.append(sip_res_description_configuration)
                count += 1
                self.add_protocol_field(tmp_sip_res_description, "SipResDescription", creation_element_position, count)
            
            # override_flag赋值
            if application_object_flag and protocol_filed_attribute_flag == False:
                override_flag = True
            else:
                override_flag = False
            
            # 选择target traffic 
            if policy_configuration["type"] == "service_chaining":
                if policy_configuration["action_parameter"]["targeted_traffic"] == "decrypted":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_decryptedTraffic_posXpath"]).click()
                else:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_rawTraffic_posXpath"]).click()

            # 添加sub action
            if "sub_action" in policy_configuration["action_parameter"]:
                if override_flag == True:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_override_posXpath"]).click()
                if policy_configuration["action_parameter"]["sub_action"] == "drop":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).clear()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).send_keys(policy_configuration["action_parameter"]["after_n_packets"])
                    # quic不支持tcp rst；默认tcp rst是选中，不需要操作，只有当send_tcp_reset为false时
                    if (override_flag == False and len(application_object_configuration["items"]) == 1 and application_object_configuration["items"][0] == "quic") or (policy_configuration["action_parameter"]["send_tcp_reset"] == False and application_object_configuration["items"][0] != "quic" and application_object_configuration["items"][0] != "dns"):
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_sendTcpRst_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_sendIcmp_posXpath"]).click()
                elif policy_configuration["action_parameter"]["sub_action"] == "rate_limit":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_rateLimit_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_rateLimit_rate_posXpath"]).send_keys(policy_configuration["action_parameter"]["bps"])
                elif policy_configuration["action_parameter"]["sub_action"] == "tamper":
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_tamper_posXpath"]).click()
                elif policy_configuration["action_parameter"]["sub_action"] == "block":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_posXpath"]).click()
                    if "mail" not in application_object_configuration["items"]:
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseCode_posXpath"]).click()
                        dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_block_responseCode_change_posXpath"].format(replaceValue=policy_configuration["action_parameter"]["code"])
                        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                        if "message" in policy_configuration["action_parameter"].keys():
                            type = "TEXT"
                        else:
                            type = "Profile"
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_posXpath"]).click()
                        dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_block_responseContent_change_posXpath"].format(replaceValue=type)
                        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                        if type.lower() == "text":
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_block_responseContent_text_posId"]).send_keys(policy_configuration["action_parameter"]["message"])
                        elif type.lower() == "profile":
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_clickProfile_posXpath"]).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(policy_configuration["action_parameter"]["html_profile"]["name"])
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_block_responseContent_selectProfile_posId"]).click()
                elif policy_configuration["action_parameter"]["sub_action"] == "redirect":
                    if application_object_configuration["items"][0] == 'http':
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
                        redirect_url = policy_configuration["action_parameter"]["to"]
                        self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_redirect_input_posId"]).clear()
                        self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_redirect_input_posId"]).send_keys(redirect_url)
                    elif application_object_configuration["items"][0] == 'dns':
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
                        if len(policy_configuration["action_parameter"]["resolution"]) == 1:
                            detail = policy_configuration["action_parameter"]["resolution"][0]
                            qtype = detail['qtype']
                            if len(detail['answer']) == 1:
                                if "value" in detail['answer'][0].keys():
                                    answer_type = "TEXT"
                                else:
                                    answer_type = "Profile"
                                atype = detail['answer'][0]['atype']
                                min_ttl = detail['answer'][0]['ttl']["min"]
                                max_ttl = detail['answer'][0]['ttl']["max"]
                                if min_ttl == max_ttl:
                                    ttl = min_ttl
                                else:
                                    ttl = min_ttl + "-" + max_ttl
                                # 点击切换qtype,默认即会选中qtype A
                                if qtype == "AAAA":
                                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_dnsAnswerqTypeAAAA_posXpath"]).click()
                                # 切换Answer Type
                                self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerType0Choose_posId"]).click()
                                answer_type_posXpath = creation_element_position["policyRulePage_dnsAnswerType0ChooseValue_posXpath"].format(replaceValue=atype)
                                self.driver.find_element(By.XPATH, answer_type_posXpath).click()
                                # 点击切换answer的返回方式
                                self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswer0ValueType_posId"]).click()
                                choose_answer_type_posXpath = creation_element_position["policyRulePage_dnsAnswer0ValueTypeChoose_posXpath"].format(replaceValue=answer_type)
                                self.driver.find_element(By.XPATH, choose_answer_type_posXpath).click()
                                if answer_type == "Profile":
                                    dns_record_profile_name = detail['answer'][0]['record_profile']
                                    self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerValueSelectPlaceholder_posId"]).click()
                                    self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerValueNameSearch_posId"]).send_keys(dns_record_profile_name)
                                    self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerValueNameSearch_posId"]).send_keys(Keys.ENTER)
                                    self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerValueNameSelect_posId"]).click()
                                else:
                                    dns_text_value = detail['answer'][0]['answer_value']
                                    if atype == "A":
                                        self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswer0ATextPlaceholder_posId"]).send_keys(dns_text_value)
                                    elif atype == "AAAA":
                                        self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswer0AAAATextPlaceholder_posId"]).send_keys(dns_text_value)
                                    elif atype == "CNAME":
                                        self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswer0CnameTextPlaceholder_posId"]).send_keys(dns_text_value)   
                                self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerValueTTL0_posId"]).send_keys(ttl)
                elif policy_configuration["action_parameter"]["sub_action"] == "alert":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_alert_responseCode_change_posXpath"].format(replaceValue=policy_configuration["action_parameter"]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    if policy_configuration["action_parameter"]["code"] == 200:
                        if "message" in policy_configuration["action_parameter"].keys():
                            type = "TEXT"
                        else:
                            type = "Profile"
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_posXpath"]).click()
                        dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_alert_responseContent_change_posXpath"].format(replaceValue=type)
                        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                        if type.lower() == "text":
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_alert_responseContent_text_posId"]).send_keys(policy_configuration["action_parameter"]["message"])
                        elif type.lower() == "profile":
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_clickProfile_posXpath"]).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(policy_configuration["action_parameter"]["html_profile"]["name"])
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_alert_responseContent_selectProfile_posId"]).click()
            
            # 添加flag
            flag_object, flag_object_configuration, flag_object_negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_FLAG")
            flag_group_object, flag_object_group_configuration, flag_object_group_negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if flag_object and flag_group_object == False:
                for t in range(len(flag_object_configuration)):
                    # 点add condition的+
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
                    # 调用flag的定位
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addConditionFlag_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                    # 点flag的+
                    temp_element_position = creation_element_position["policyRulePage_addFlag_posXpath"]
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    # 通过flag搜索并选中
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchFlag_posXpath"], find_after_wait_time=1).send_keys(flag_object_configuration[t]["name"])
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchFlag_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectFlag_posXpath"], find_after_wait_time=0.5).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeFlag_posXpath"]).click()
            if flag_object and flag_group_object:
                print("todo")
            
            # 添加packet capture
            if "packet_capture" in policy_configuration["action_parameter"] and policy_configuration["action_parameter"]["packet_capture"]["enable"] == 1:
                capture_depth = policy_configuration["action_parameter"]["packet_capture"]["capture_depth"]
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_posXpath"]).click()
                # 获取元素
                input_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_depth_posXpath"])
                # 使用JavaScript完全清除并设置新值
                self.driver.execute_script("arguments[0].value = '';", input_element)
                self.driver.execute_script("arguments[0].value = arguments[1];", input_element, capture_depth)
                # self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_depth_posXpath"]).clear()
                # self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_depth_posXpath"]).send_keys(packet_capture_data[0]["capture_depth"])
            
            # 添加shaping的priority和fair factor
            if policy_configuration["type"] == "traffic_shaping":
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_priority_posId"]).clear()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_priority_posId"]).send_keys(policy_configuration["action_parameter"]["priority"])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_fairFactor_posId"]).clear()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_fairFactor_posId"]).send_keys(policy_configuration["action_parameter"]["fair_factor"])
            
            # 添加statistics、shaping、sc、manipulation的profile
            if policy_configuration["type"] == "traffic_shaping":
                # 点profile的+
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addProfile_posXpath"]).click()
                # 通过profile name搜索并选中
                profile_chain = policy_configuration["action_parameter"]["profile_chain"]
                for y in range(len(profile_chain)):
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=1).send_keys(profile_chain[y]["name"])
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectProfile_posXpath"], find_after_wait_time=0.5).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeProfile_posXpath"]).click()
                    # if policy_configuration["multiProfile"] == True and y != len(profile_chain) - 1:
                    #     self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addProfile_plus_posXpath"]).click()
            elif policy_configuration["type"] == "proxy_intercept":
                profile_data = policy_configuration["action_parameter"]
                if "keyring_for_trusted" in profile_data.keys():
                    keyring_for_trusted_name = profile_data["keyring_for_trusted"]["name"]
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addTrustedSelectBox_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"], find_after_wait_time=0.6).clear()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"]).send_keys(keyring_for_trusted_name)
                    # 点击回车键
                    search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"])
                    search_box.send_keys(Keys.RETURN)
                    # 选择第一个
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedDorpItem_posXpath"], find_after_wait_time=0.6).click()
                if "keyring_for_untrusted" in profile_data.keys():
                    keyring_for_untrusted_name = profile_data["keyring_for_untrusted"]["name"]
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addUntrustedSelectBox_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"], find_after_wait_time=0.6).clear()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"]).send_keys(keyring_for_untrusted_name)
                    # 点击回车键
                    search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"])
                    search_box.send_keys(Keys.RETURN)
                    # 选择第一个
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedDorpItem_posXpath"], find_after_wait_time=0.6).click()
                # mirror decrypted profile
                if "traffic_mirroring" in profile_data.keys():
                    traffic_mirroring_name = profile_data["traffic_mirroring"]["name"]
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addVlanIDButton_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addTrafficMirrorProfileSelectBox_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"]).send_keys(traffic_mirroring_name)
                    # 点击回车键
                    search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"])
                    search_box.send_keys(Keys.RETURN)
                    # 选择第一个
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrafficMirrorProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()
                # decryption profile
                if "decryption_profile" in profile_data.keys():
                    decryption_profile_name = profile_data["decryption_profile"]["name"]
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addDecryptionProfileSelectBox_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"]).send_keys(decryption_profile_name)
                    # 点击回车键
                    search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"])
                    search_box.send_keys(Keys.RETURN)
                    # 选择第一个
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()
                # tcp proxy profile
                if "tcp_option_profile" in profile_data.keys():
                    tcp_option_profile_name = profile_data["tcp_option_profile"]["name"]
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addTcpProfileSelectBox_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"]).send_keys(tcp_option_profile_name)
                    # 点击回车键
                    search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"])
                    search_box.send_keys(Keys.RETURN)
                    # 选择第一个
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTcpProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()
            elif policy_configuration["type"] == "proxy_manipulation":
                profile_data = policy_configuration["action_parameter"]
                # 页面滚动到最底部
                div_container = self.driver.find_element(By.XPATH, "//div[@id='root']//div[contains(@class, 'manipulation-policy-page')]")
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", div_container)  # 移动到页面最底部
                if policy_configuration["action"] == "deny":
                    if "manipulation_block" in policy_configuration["action_parameter"].keys():  
                        response_code = policy_configuration["action_parameter"]["code"]
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseCodeSelectBox_posXpath"]).click()
                        response_code_dropdown_position = creation_element_position["policyRulePage_deny_addResponseCodeSelectDropItem_posXpath"].format(replace_code=response_code)
                        self.driver.find_element(By.XPATH, response_code_dropdown_position).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentSelectBox_posXpath"]).click()
                        if "message" in policy_configuration["action_parameter"].keys():
                            type = "TEXT"
                        else:
                            type = "Profile"
                        response_content_type_position = creation_element_position["policyRulePage_deny_addResponseContentSelectDropItem_posXpath"].format(replace_type=type)
                        self.driver.find_element(By.XPATH, response_content_type_position).click()
                        if type == "TEXT":
                            response_context_text = policy_configuration["action_parameter"]["message"]
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentTextInput_posXpath"]).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentTextInput_posXpath"]).send_keys(response_context_text)
                        else:
                            response_profile_name = policy_configuration["action_parameter"]["html_profile"]
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentProfileSelectBox_posXpath"]).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfile_posXpath"]).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfile_posXpath"]).send_keys(response_profile_name)
                            # 点击回车键
                            search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfile_posXpath"])
                            search_box.send_keys(Keys.RETURN)
                            # 选择第一个
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfileDorpItem_posXpath"]).click()
                elif policy_configuration["action"] == "redirect":
                    if application_object_configuration["items"][0] == "http":
                        response_code = policy_configuration["action_parameter"]["code"]
                        response_code_dropdown_position = creation_element_position["policyRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath"].format(replace_code=response_code)
                        redirect_url = policy_configuration["action_parameter"]["to"]
                        # 操作 action parameter
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectHttp_addResponseCodeSelectBox_posXpath"]).click()
                        time.sleep(0.3)
                        btn = self.driver.find_element(By.XPATH, response_code_dropdown_position)
                        self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
                        time.sleep(0.3)
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).clear()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).send_keys(redirect_url)
                    else:
                        # 遍历，是否含有多个value
                        doh_action_parameter_list = policy_configuration["action_parameter"]
                        for i in range(len(doh_action_parameter_list)):
                            q_type = doh_action_parameter_list[i]["q_type"]
                            a_type = doh_action_parameter_list[i]["a_type"]
                            doh_value = doh_action_parameter_list[i]["doh_value"]
                            doh_ttl = doh_action_parameter_list[i]["doh_ttl"]
                            replace_index = i + 2
                            if i != 0:    # 非第一次遍历点击
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_add_posXpath"]).click()
                            if i == 0:   # 只有第一次遍历点击
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_qtypeRadio_posXpath"].format(replace_qtype=q_type)).click()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_atypeSelectBox_posXpath"].format(replace_index=replace_index)).click()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_atypeSelectDropItem_posXpath"].format(replace_atype=a_type)).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_valueInput_posXpath"].format(replace_index=replace_index)).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_valueInput_posXpath"].format(replace_index=replace_index), find_after_wait_time=0.5).send_keys(doh_value)
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_ttlInput_posXpath"].format(replace_index=replace_index)).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectDoH_ttlInput_posXpath"].format(replace_index=replace_index), find_after_wait_time=0.5).send_keys(doh_ttl)
                elif policy_configuration["action"] == "modify":
                    # ？？
                    if policy_configuration["action_parameter"]["sub_action"] == "replace_file":
                        print("todo")
                    elif policy_configuration["action_parameter"]["sub_action"] == "inject_javascript":
                        print("todo")
            elif policy_configuration["type"] == "statistics":
                # 点击Statistics Template添加按钮打开Template侧滑列表
                self.driver.find_element(By.XPATH, creation_element_position["plicyRulePage_addStatisticsTemplate_posXpath"]).click()
                # 通过Statistics Template name搜索并选中
                template_profile = policy_configuration["action_parameter"]["template_profile"]
                if len(template_profile) > 0:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=1).send_keys(template_profile["name"])
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectProfile_posXpath"].format(replaceValue=template_profile["name"]), find_after_wait_time=0.5).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeProfile_posXpath"]).click()
            elif policy_configuration["type"] == "service_chaining":
                sff_profiles = policy_configuration["action_parameter"]["sff_profiles"]
                # 点击SFF Profile添加按钮
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addSFFProfile_posXpath"]).click()
                time.sleep(1)
                #在侧滑框中搜索sff并选中
                for sff in sff_profiles:
                    btn = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchSFFProfile_posXpath"], find_after_wait_time=1)
                    self.driver.execute_script("arguments[0].click()", btn)
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchSFFProfile_posXpath"]).send_keys(sff["name"])
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchSFFProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                    select_sff_xpath = creation_element_position["policyRulePage_selectSFFProfile_posXpath"].format(replaceValue=sff["name"])
                    self.driver.find_element(By.XPATH, select_sff_xpath).click()
                    # self.driver.execute_script("arguments[0].click()", btn)
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeSFFProfile_posXpath"]).click()
            elif policy_configuration["type"] == "monitor":
                # 步骤：开启vlan_button->选择select->输入name->搜索
                if policy_configuration["action_parameter"]["traffic_mirroring"]["enable"] == 1:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_mirrorTrafficButton_posXpath"]).click()
                else:
                    pass
                self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_addVLANIDButton_posXpath"]).click()
                if len(policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]) > 0:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_firstSelectMirrorProfile_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchMirrorProfile_posXpath"], find_after_wait_time=1).send_keys(policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]["name"])
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchMirrorProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                    self.driver.find_element(By.XPATH, '//ul[@class="MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd css-1cklc3"]//li[1]//div[@class="MuiListItemButton-root MuiListItemButton-colorNeutral MuiListItemButton-variantPlain css-18mv95p"]').click()
                    self.driver.find_element(By.XPATH, '//div[@class="absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]"]/button').click()
                    # selectProfileXpath = creation_element_position["policyRulePage_selectMirrorProfile_posXpath"].format(replaceValue=policy_configuration["profile"][flag]["name"])
                    # self.driver.find_element(By.XPATH,selectProfileXpath, find_after_wait_time=0.5).click()

            # 配置DoS的Threshold和Mitigation
            if policy_configuration["type"] == "dos_protection" and policy_configuration["action"] == "protect":
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_thresholdType_posXpath"]).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_groupBy_dropDownBox_posXpath"]).click()
                if policy_configuration["threshold"]["type"] == "rate":
                    if policy_configuration["threshold"]["rate_threshold"]["group_by"] == "source_ip":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP")
                    elif policy_configuration["threshold"]["rate_threshold"]["group_by"] == "source_asn":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source ASN")
                    elif policy_configuration["threshold"]["rate_threshold"]["group_by"] == "source_country":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source Country")
                    elif policy_configuration["threshold"]["rate_threshold"]["group_by"] == "server_fqdn":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Server FQDN")
                    elif policy_configuration["threshold"]["rate_threshold"]["group_by"] == "source_ip_and_destination_ip":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP and Destination IP")
                    self.driver.find_element(By.XPATH, temp_group_by_element_position).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_requestPerPeriod_posXpath"]).send_keys(policy_configuration["action_parameter"]["threshold"]["rate_threshold"]["request_per_period"])
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_countingPeriod_dropDownBox_posXpath"]).click()
                    temp_counting_period_element_position = creation_element_position["policyRulePage_countingPeriod_select_posXpath"].format(replaceValue=policy_configuration["action_parameter"]["threshold"]["rate_threshold"]["counting_period"])
                    self.driver.find_element(By.XPATH, temp_counting_period_element_position).click()
                elif policy_configuration["threshold"]["type"] == "concurrency":
                    if policy_configuration["threshold"]["concurrency_threshold"]["group_by"] == "source_ip":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP")
                    elif policy_configuration["threshold"]["concurrency_threshold"]["group_by"] == "source_asn":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source ASN")
                    elif policy_configuration["threshold"]["rate_threshold"]["group_by"] == "source_country":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source Country")
                    elif policy_configuration["threshold"]["rate_threshold"]["group_by"] == "server_fqdn":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Server FQDN")
                    elif policy_configuration["threshold"]["rate_threshold"]["group_by"] == "source_ip_and_destination_ip":
                        temp_group_by_element_position = creation_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP and Destination IP")
                    self.driver.find_element(By.XPATH, temp_group_by_element_position).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_concurrentSsessions_posXpath"]).send_keys(policy_configuration["action_parameter"]["threshold"]["concurrency_threshold"]["concurrent_sessions"])
                #self.driver.find_element(By.ID, creation_element_position["policyRulePage_mitigationBehavior_posId"]).click()
                if policy_configuration["mitigation"]["behavior"] == "deny":
                    self.driver.find_element(By.XPATH, dosRulePage_mitigationBehavior_deny_posXpath).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_mitigationTimeouts_dropDownBox_posXpath"]).click()
                    temp_mitigation_timeout_element_position = creation_element_position["policyRulePage_mitigationTimeouts_select_posXpath"].format(replaceValue=policy_configuration["mitigation"]["timeout"])
                    self.driver.find_element(By.XPATH, temp_mitigation_timeout_element_position).click()
                elif policy_configuration["mitigation"]["behavior"] == "none":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_mitigationBehavior_posXpath"]).click()

            # other options 操作
            if policy_configuration["type"] == "monitor":
                if policy_configuration["log_option"] == "all":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_logOptions_all_posXpath"]).click()
                elif policy_configuration["log_option"] == "off":
                    pass
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: todo...")
            if "effective_range" in policy_configuration:
                # ？？
                self.add_effective_devices(policy_configuration["effective_range"], creation_element_position)

            # 点enable，不加sleep有一定几率点不上
            time.sleep(1)
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_enable_posXpath"]).click()
            # 确认创建
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_okButton_posXpath"]).click()
            #self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_okButton_warningYes_posXpath"]).click()
            return ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating rule, the exception error: ", str(e), flush=True)
            return "When creating rule, the exception error: " + str(e)
        
    def add_ip(self, ip_data, ip_condition_type, creation_element_position, negate_option):
        try:
            if ip_condition_type != "SrcIP" and ip_condition_type != "DstIP":
                # 点add condition的+
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
                # 选中port
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition{}_posXpath".format(ip_condition_type)]).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点ip address的+
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_add{}_posXpath".format(ip_condition_type)]).click()
            # 通过ip name搜索并选中
            for i in range(len(ip_data)):
                #self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)]).clear()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)]).send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)], find_after_wait_time=1).send_keys(ip_data[i]["name"])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                temp_element_position = creation_element_position["policyRulePage_select{}_posXpath".format(ip_condition_type)].format(replaceValue=ip_data[i]["name"])
                self.driver.find_element(By.XPATH, temp_element_position, find_after_wait_time=0.5).click()
                # self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_select{}_posXpath".format(ip_condition_type)]).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_close{}_posXpath".format(ip_condition_type)]).click()
            # for j in range(len(ip_data)):
            if negate_option == True:
                time.sleep(1)  # 暂停1秒
                negate_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_negate{}_posXpath".format(ip_condition_type)])
                # 使用JavaScript确保元素完全进入视图
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", negate_element)
                # 使用JavaScript执行悬停
                self.driver.execute_script("var evt = new MouseEvent('mouseover', {'view': window, 'bubbles': true, 'cancelable': true}); arguments[0].dispatchEvent(evt);", negate_element)
                # 确保元素可点击后进行点击
                self.driver.execute_script("arguments[0].click();", negate_element)
                # ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                # negate_element.click()
        except Exception as e:
            raise
    
    def add_port(self, port_data, port_condition_type, creation_element_position, negate_option):
        try:
            # 点add condition的+
            btn = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"])
            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
            # 选中port
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition{}_posXpath".format(port_condition_type)]).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点source port的+
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_add{}_posXpath".format(port_condition_type)]).click()
            # 通过port name搜索并选中
            for z in range(len(port_data)):
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(port_condition_type)], find_after_wait_time=1).send_keys(port_data[z]["name"])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(port_condition_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                temp_element_position = creation_element_position["policyRulePage_select{}_posXpath".format(port_condition_type)].format(replaceValue=port_data[z]["name"])
                self.driver.find_element(By.XPATH, temp_element_position, find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_close{}_posXpath".format(port_condition_type)]).click()
            # for j in range(len(port_data)):
            if negate_option == True:
                time.sleep(1)  # 暂停1秒
                negate_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_negate{}_posXpath".format(port_condition_type)])
                ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                negate_element.click()
        except Exception as e:
            raise

    def add_device(self, creation_element_position, name, negate_option):
        try:
            # 点add condition的+
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
            # 选中imsi
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addConditionImsi_posXpath"]).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点imsi的+，因为dst ip已经是第一层且t初始值是0，所以要+2
            temp_element_position = creation_element_position["policyRulePage_addImsi_posXpath"]
            self.driver.find_element(By.XPATH, temp_element_position).click()
            # 通过imsi搜索并选中
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=1).send_keys(name)
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectImsi_posXpath"], find_after_wait_time=0.5).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeImsi_posXpath"]).click()
            if negate_option == True:
                time.sleep(1)  # 暂停1秒
                negate_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_negateImsi_posXpath"])
                ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                negate_element.click()
        except Exception as e:
            raise
    
    add_subid = add_port

    def add_protocol_field(self, protocol_field_data, filed_type, creation_element_position, num):
        try:
            # 强制点击add condition的+
            btn = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"])
            self.driver.execute_script("arguments[0].click()", btn)
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点protocol filed的+
            temp_element_position = creation_element_position["policyRulePage_add{}_posXpath".format(filed_type)].format(replaceValue=num)
            self.driver.find_element(By.XPATH, temp_element_position).click()
            # 通过protocol filed name搜索并选中
            for x in range(len(protocol_field_data)):
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=1).send_keys(protocol_field_data[x]["name"])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_select{}_posXpath".format(filed_type)].format(replaceValue=protocol_field_data[x]["name"]), find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_close{}_posXpath".format(filed_type)]).click()
        except Exception as e:
            raise

    def add_bool_type_protocol_field(self, protocol_field_data, filed_type, creation_element_position, num):
        try:
            # for x in range(len(protocol_field_data)):
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
            value = filed_type.lower()
            xpath_temp = creation_element_position["policyRulePage_addCondition{}_posXpath".format("Boolean")]
            xpath_last = xpath_temp.format(replaceValue=value)
            self.driver.find_element(By.XPATH, xpath_last).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点protocol filed的+
            temp_element_position = creation_element_position["policyRulePage_add{}_posXpath".format("Boolean")].format(replaceValue=num)
            self.driver.find_element(By.XPATH, temp_element_position).click()
            # 通过protocol filed name搜索并选中
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format("Boolean")], find_after_wait_time=1).send_keys(protocol_field_data["name"])
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format("Boolean")], find_after_wait_time=0.5).send_keys(Keys.ENTER)
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_select{}_posXpath".format("Boolean")], find_after_wait_time=0.5).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_close{}_posXpath".format("Boolean")]).click()
            num = num +1
        except Exception as e:
            raise

    def add_ip_protocol(self, ip_protocol_data, filed_type, creation_element_position, negate_option):
        try:
            # 点add condition的+
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
            # 选中port
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]).click()
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点source port的+
            self.driver.find_element(By.XPATH, creation_element_position[ "policyRulePage_add{}_posXpath".format(filed_type)]).click()
            # 通过port name搜索并选中
            is_first_iteration = True
            for z in ip_protocol_data["items"]:
                # 如果不是第一次循环，需要点加号调侧滑框
                if not is_first_iteration:
                    self.driver.find_element(By.XPATH, policyRulePage_little_button_addIpProtocol_posXpath).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=1).send_keys(z)
                self.driver.find_element(By.XPATH, creation_element_position[ "policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                temp_element_position = creation_element_position[ "policyRulePage_select{}_posXpath".format(filed_type)].format(replaceValue=z)
                self.driver.find_element(By.XPATH, temp_element_position, find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_close{}_posXpath".format(filed_type)]).click()
                is_first_iteration = False
        except Exception as e:
            raise

    def add_effective_devices(self, effective_device_data, creation_element_position):
        try:
            # 点击 add effective devices按钮
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addEffectiveDevices_posXpath"]).click()
            # 从侧滑中选择数据
            for i in range(len(effective_device_data)):
                replace_device = effective_device_data[i].strip()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectEffectiveDevices_posXpath"].format(replace_device=replace_device), find_after_wait_time=1).click()
            # 关闭侧滑
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeEffectiveDevices_posXpath"]).click()
        except Exception as e:
            raise

    def is_attribute_name_exsit(self, policy_configuration, attribute_name):
        if "and_conditions" in policy_configuration:
            and_conditions = policy_configuration["and_conditions"]
            for i in range(len(and_conditions)):
                or_conditions = and_conditions[i]["or_conditions"]
                for j in range(len(or_conditions)):
                    if or_conditions[j]["attribute_name"] == attribute_name:
                        return True, or_conditions, and_conditions[i]["negate_option"]
        return False, "", ""
    
    def is_group_exsit(self, policy_configuration):
        if "and_conditions" in policy_configuration:
            and_conditions = policy_configuration["and_conditions"]
            for i in range(len(and_conditions)):
                or_conditions = and_conditions[i]["or_conditions"]
                for j in range(len(or_conditions)):
                    if "member_type" in or_conditions[j].keys and or_conditions[j]["member_type"] != "":
                        return True, or_conditions, and_conditions[i]["negate_option"]
        return False, "", ""

    def is_protocol_filed_exsit(self, policy_configuration, attribute_value):
        """
        # protocol_filed_list = [
        #     "ATTR_HTTP_URL",
        #     "ATTR_HTTP_REQ_HDR",
        #     "ATTR_HTTP_RES_HDR",
        #     "ATTR_HTTP_REQ_BODY",
        #     "ATTR_HTTP_RES_BODY",
        #     "ATTR_SSL_CN",
        #     "ATTR_SSL_CN_CAT",
        #     "ATTR_SSL_SAN",
        #     "ATTR_SSL_SAN_CAT",
        #     "ATTR_SSL_ECH",
        #     "ATTR_SSL_ESNI",
        #     "ATTR_SSL_NO_SNI",
        #     "ATTR_DNS_QNAME",
        #     "ATTR_MAIL_SUBJECT",
        #     "ATTR_MAIL_CONTENT",
        #     "ATTR_MAIL_ATT_NAME",
        #     "ATTR_MAIL_ATT_CONTENT",
        #     "ATTR_MAIL_FROM",
        #     "ATTR_MAIL_TO",
        #     "ATTR_MAIL_ACCOUNT",
        #     "ATTR_FTP_URI",
        #     "ATTR_FTP_CONTENT",
        #     "ATTR_FTP_ACCOUNT",
        #     "ATTR_SIP_ORIGINATOR_DESCRIPTION",
        #     "ATTR_SIP_RESPONDER_DESCRIPTION"
        # ]
        """
        if "and_conditions" in policy_configuration:
            and_conditions = policy_configuration["and_conditions"]
            for i in range(len(and_conditions)):
                or_conditions = and_conditions[i]["or_conditions"]
                for j in range(len(or_conditions)):
                    if or_conditions[j]["attribute_name"] == attribute_value:
                        return True, or_conditions
        return False, ""