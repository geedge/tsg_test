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
            # 目前所有object类型都是一个值？？
            
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
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SOURCE_IP")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_ip(object_configuration, "SrcIP", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_ip(object_group_configuration, "SrcIP", creation_element_position, negate_option)
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_DESTINATION_IP")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_ip(object_configuration, "DstIP", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_ip(object_group_configuration, "DstIP", creation_element_position, negate_option)
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_INTERNAL_IP")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_ip(object_configuration, "InternalIP", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_ip(object_group_configuration, "InternalIP", creation_element_position, negate_option)
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_EXTERNAL_IP")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_ip(object_configuration, "ExternalIP", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_ip(object_group_configuration, "ExternalIP", creation_element_position, negate_option)

            # 添加library作为ip
            
            # 添加port
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SOURCE_PORT")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_port(object_configuration, "SrcPort", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_port(object_group_configuration, "SrcPort", creation_element_position, negate_option)
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_DESTINATION_PORT")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_port(object_configuration, "DstPort", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_port(object_group_configuration, "DstPort", creation_element_position, negate_option)
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_INTERNAL_PORT")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_port(object_configuration, "InternalPort", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_port(object_group_configuration, "InternalPort", creation_element_position, negate_option)
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_EXTERNAL_PORT")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_port(object_configuration, "ExternalPort", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_port(object_group_configuration, "ExternalPort", creation_element_position, negate_option)
                
            # 添加subscriber id
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SUBSCRIBER_ID")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_subid(object_configuration, "User", creation_element_position, negate_option)
            if attribute_flag and group_flag:
                self.add_subid(object_group_configuration, "User", creation_element_position, negate_option)

            # 添加device
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_IMSI")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_device(creation_element_position, object_configuration["name"], negate_option)
            if attribute_flag and group_flag:
                print("todo")
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_PHONE_NUMBER")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_device(creation_element_position, object_configuration["name"], negate_option)
            if attribute_flag and group_flag:
                print("todo")
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_IMEI")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_device(creation_element_position, object_configuration["name"], negate_option)
            if attribute_flag and group_flag:
                print("todo")
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_GTP_APN")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                self.add_device(creation_element_position, object_configuration["name"], negate_option)
            if attribute_flag and group_flag:
                print("todo")
            
            # 添加application
            # if "application" in policy_configuration["condition"] and len(policy_configuration["condition"]["application"]) != 0:
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_APP_ID")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
                if policy_configuration["type"] == "proxy_manipulation":
                    if object_configuration["items"][0].lower() == "doh":  # doh需要操作application
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addApplication_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchDoHApplication_posXpath"], find_before_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeApplication_posXpath"]).click()
                    else:   # 非doh不需要操作application
                        pass
                else:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addApplication_posXpath"]).click()
                    application_data = policy_configuration["condition"]["application"]
                    # 通过application name搜索并选中
                    for j in range(len(application_data)):
                        if application_data[j]["object_type"] == "application_group":
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectApplicationGroupLabel_posXpath"]).click()
                        if policy_configuration["type"] == "proxy_intercept":  # intercept 中 application不用搜索，直接选择
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectApplication_posXpath"].format(replaceValue=application_data[j]["name"]), find_after_wait_time=0.5).click()
                        else:
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=1).send_keys(application_data[j]["name"])
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectApplication_posXpath"].format(replaceValue = application_data[j]["name"]), find_after_wait_time=0.5).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeApplication_posXpath"]).click()
            if attribute_flag and group_flag:
                print("todo")
                
            # 添加server fqdn
            attribute_flag, object_configuration, negate_option = self.is_attribute_name_exsit(policy_configuration, "ATTR_SERVER_FQDN")
            group_flag, object_group_configuration, negate_option = self.is_group_exsit(policy_configuration, "member_type")
            if attribute_flag and group_flag == False:
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
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchServerFqdn_posXpath"], find_after_wait_time=1).send_keys(object_configuration["name"])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchServerFqdn_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                btn = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectServerFqdn_posXpath"].format(replaceValue=fqdn_name), find_after_wait_time=1)
                self.driver.execute_script("arguments[0].click()", btn)
                # self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectServerFqdn_posXpath"], find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeServerFqdn_posXpath"]).click()
                if negate_option == True:
                    time.sleep(1)  # 暂停1秒
                    negate_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_negateServerFqdn_posXpath"])
                    # 使用JavaScript确保元素完全进入视图
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", negate_element)
                    # 使用JavaScript执行悬停
                    self.driver.execute_script("var evt = new MouseEvent('mouseover', {'view': window, 'bubbles': true, 'cancelable': true}); arguments[0].dispatchEvent(evt);",negate_element)
                    # 确保元素可点击后进行点击
                    self.driver.execute_script("arguments[0].click();", negate_element)
                    # ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                    # negate_element.click()
            if attribute_flag and group_flag:
                print("todo")
            # 添加library作为fqdn

            #添加ip_protocol
            if "ip_protocol" in policy_configuration["condition"] and len(policy_configuration["condition"]["ip_protocol"]) != 0:
                protocol_field_data = policy_configuration["condition"]["ip_protocol"]
                self.add_ip_protocol(protocol_field_data, "IpProtocol", creation_element_position)

            # 添加protocol field
            if "protocol_filed" in policy_configuration["condition"] and len(policy_configuration["condition"]["protocol_filed"]) != 0:
                protocol_field_datas = policy_configuration["condition"]["protocol_filed"]
                tmp_protocol_field_data_split_by_type = []   # 将 protocol_filed 分类临时存储
                tmp_url, tmp_request_header, tmp_response_header, tmp_request_body, tmp_response_body, tmp_ftp_account, tmp_ftp_content, tmp_cn, tmp_san, tmp_qname = [], [], [], [], [], [], [], [], [], []
                tmp_boolean= []
                tmp_mail_account, tmp_mail_from, tmp_mail_to,tmp_mail_subject,tmp_mail_attachment_name,tmp_mail_content,tmp_mail_attachment_content= [],[],[],[],[],[],[]
                for _ in range(len(protocol_field_datas)):   # 将 rul、request_header等数据分类处理
                    tmp_item = protocol_field_datas[_]
                    if tmp_item["object_type"] == "url":
                        tmp_url.append(tmp_item)
                    elif tmp_item["object_type"] == "fqdn":
                        if tmp_item["items"][0]["item_type"] == "cn":
                            tmp_cn.append(tmp_item)
                        elif tmp_item["items"][0]["item_type"] == "san":
                            tmp_san.append(tmp_item)
                        elif tmp_item["items"][0]["item_type"] == "qname":
                            tmp_qname.append(tmp_item)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "check..")
                    # elif tmp_item["object_type"] == "http_signature":
                    #     if tmp_item["item"][0]["item_type"] == "request_header":
                    #         tmp_request_header.append(tmp_item)
                    #     elif tmp_item["item"][0]["item_type"] == "response_header":
                    #         tmp_response_header.append(tmp_item)
                    #     else:
                    #         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "check..")
                    elif tmp_item["object_type"] == "keywords":
                        if tmp_item["item"][0]["item_type"] == "request_header":
                            tmp_request_header.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "response_header":
                            tmp_response_header.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "request_body":
                            tmp_request_body.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "response_body":
                            tmp_response_body.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "ftp_content":
                            tmp_ftp_content.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "mail_subject":
                            tmp_mail_subject.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "mail_attachment_name":
                            tmp_mail_attachment_name.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "mail_attachment_content":
                            tmp_mail_attachment_content.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "mail_content":
                            tmp_mail_content.append(tmp_item)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "check..")
                    elif tmp_item["object_type"] == "account":
                        if tmp_item["items"][0]["item_type"] == "ftp_account":
                            tmp_ftp_account.append(tmp_item)
                        elif tmp_item["items"][0]["item_type"] == "mail_account":
                            tmp_mail_account.append(tmp_item)
                        elif tmp_item["items"][0]["item_type"] == "mail_from":
                            tmp_mail_from.append(tmp_item)
                        elif tmp_item["items"][0]["item_type"] == "to":
                            tmp_mail_to.append(tmp_item)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "check..")
                    elif tmp_item["object_type"] == "boolean":
                        tmp_boolean.append(tmp_item)
                if len(tmp_url) > 0: tmp_protocol_field_data_split_by_type.append(tmp_url)
                if len(tmp_request_header) > 0: tmp_protocol_field_data_split_by_type.append(tmp_request_header)
                if len(tmp_response_header) > 0: tmp_protocol_field_data_split_by_type.append(tmp_response_header)
                if len(tmp_request_body) > 0: tmp_protocol_field_data_split_by_type.append(tmp_request_body)
                if len(tmp_response_body) > 0: tmp_protocol_field_data_split_by_type.append(tmp_response_body)
                if len(tmp_ftp_account) > 0: tmp_protocol_field_data_split_by_type.append(tmp_ftp_account)
                if len(tmp_ftp_content) > 0: tmp_protocol_field_data_split_by_type.append(tmp_ftp_content)
                if len(tmp_boolean) > 0: tmp_protocol_field_data_split_by_type.append(tmp_boolean)
                if len(tmp_cn) > 0: tmp_protocol_field_data_split_by_type.append(tmp_cn)
                if len(tmp_san) > 0: tmp_protocol_field_data_split_by_type.append(tmp_san)
                if len(tmp_qname) > 0: tmp_protocol_field_data_split_by_type.append(tmp_qname)
                if len(tmp_mail_to) > 0:tmp_protocol_field_data_split_by_type.append(tmp_mail_to)
                if len(tmp_mail_from) > 0:tmp_protocol_field_data_split_by_type.append(tmp_mail_from)
                if len(tmp_mail_account) > 0:tmp_protocol_field_data_split_by_type.append(tmp_mail_account)
                if len(tmp_mail_subject) > 0:tmp_protocol_field_data_split_by_type.append(tmp_mail_subject)
                if len(tmp_mail_attachment_name) > 0: tmp_protocol_field_data_split_by_type.append(tmp_mail_attachment_name)
                if len(tmp_mail_attachment_content) > 0: tmp_protocol_field_data_split_by_type.append(tmp_mail_attachment_content)
                if len(tmp_mail_content) > 0: tmp_protocol_field_data_split_by_type.append(tmp_mail_content)
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], tmp_protocol_field_data_split_by_type)
                for protocol_field_data in tmp_protocol_field_data_split_by_type:
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], protocol_field_data)
                    for x in range(len(protocol_field_data)):
                        temp = x + 1
                        if protocol_field_data[x]["object_type"] == "url":
                            self.add_protocol_field(protocol_field_data, "Url", creation_element_position, temp)
                        elif protocol_field_data[x]["object_type"] == "fqdn":
                            for item_dict in protocol_field_data[x]["items"]:
                                if item_dict["item_type"] == "cn":
                                    self.add_protocol_field(protocol_field_data, "Cn", creation_element_position, temp)
                                elif item_dict["item_type"] == "san":
                                    self.add_protocol_field(protocol_field_data, "San", creation_element_position, temp)
                                elif item_dict["item_type"] == "qname":
                                    self.add_protocol_field(protocol_field_data, "Qname", creation_element_position, temp)
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        # elif protocol_field_data[x]["object_type"] == "http_signature":
                        #     item_dict = protocol_field_data[x]["item"][0]
                        #     if item_dict["item_type"] == "request_header":
                        #         self.add_protocol_field(protocol_field_data, "RequestHeader", creation_element_position, temp)
                        #     elif item_dict["item_type"] == "response_header":
                        #         self.add_protocol_field(protocol_field_data, "ResponseHeader", creation_element_position, temp)
                        #     else:
                        #         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        elif protocol_field_data[x]["object_type"] == "keywords":
                            item_dict = protocol_field_data[x]["item"][0]
                            if item_dict["item_type"] == "request_header":
                                self.add_protocol_field(protocol_field_data, "RequestHeader", creation_element_position, temp)
                            elif item_dict["item_type"] == "response_header":
                                self.add_protocol_field(protocol_field_data, "ResponseHeader", creation_element_position, temp)
                            elif item_dict["item_type"] == "request_body":
                                self.add_protocol_field(protocol_field_data, "RequestBody", creation_element_position, temp)
                            elif item_dict["item_type"] == "response_body":
                                self.add_protocol_field(protocol_field_data, "ResponseBody", creation_element_position, temp)
                            elif item_dict["item_type"] == "ftp_content":
                                self.add_protocol_field(protocol_field_data, "FtpContent", creation_element_position, temp)
                            elif item_dict["item_type"] == "mail_subject":
                                self.add_protocol_field(protocol_field_data, "MailSubject", creation_element_position, temp)
                            elif item_dict["item_type"] == "mail_attachment_name":
                                self.add_protocol_field(protocol_field_data, "MailAttachmentName", creation_element_position, temp)
                            elif item_dict["item_type"] == "mail_attachment_content":
                                self.add_protocol_field(protocol_field_data, "MailAttachmentContent", creation_element_position, temp)
                            elif item_dict["item_type"] == "mail_content":
                                self.add_protocol_field(protocol_field_data, "MailContent", creation_element_position, temp)
                            else:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        elif protocol_field_data[x]["object_type"] == "account":
                            for item_dict in protocol_field_data[x]["items"]:
                                if item_dict["item_type"] == "ftp_account":
                                    self.add_protocol_field(protocol_field_data, "FtpAccount", creation_element_position, temp)
                                elif item_dict["item_type"] == "mail_account":
                                    self.add_protocol_field(protocol_field_data, "MailAccount",creation_element_position, temp)
                                elif item_dict["item_type"] == "mail_from":
                                    self.add_protocol_field(protocol_field_data, "MailFrom", creation_element_position,temp)
                                elif item_dict["item_type"] == "to":
                                    self.add_protocol_field(protocol_field_data, "MailTo", creation_element_position,temp)
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        elif protocol_field_data[x]["object_type"] == 'boolean':
                            self.add_bool_type_protocol_field(protocol_field_data, "Boolean", creation_element_position, temp)
                            break

            if "application" in policy_configuration["condition"] and len(policy_configuration["condition"]["application"]) != 0 and "protocol_filed" in policy_configuration["condition"] and len(policy_configuration["condition"]["protocol_filed"]) == 0:
                override_flag = True
            else:
                override_flag = False
            
            # 选择target traffic 
            if policy_configuration["type"] == "service_chaining":
                if policy_configuration["targeted_traffic"] == "decrypted":
                    self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_decryptedTraffic_posXpath"]).click()
                else:
                    self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_rawTraffic_posXpath"]).click()

            # 添加sub action
            if "sub_action" in policy_configuration["condition"] and len(policy_configuration["condition"]["sub_action"]) != 0 and policy_configuration["condition"]["sub_action_override"] == True:
                sub_action_data = policy_configuration["condition"]["sub_action"]
                if override_flag == True:
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_override_posXpath"]).click()
                if sub_action_data[0]["type"] == "drop":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).clear()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).send_keys(sub_action_data[0]["drop_packet"])
                    # quic不支持tcp rst；默认tcp rst是选中，不需要操作，只有当sendTcpRst为false时
                    if (override_flag == False and len(policy_configuration["condition"]["application"]) == 1 and policy_configuration["condition"]["application"][0]['name'] == "quic")or (sub_action_data[0]["send_tcp_rst"] == False and policy_configuration["condition"]["application"][0]['name'] != "quic" and policy_configuration["condition"]["application"][0]['name'] != "dns"):
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_sendTcpRst_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_drop_sendIcmp_posXpath"]).click()
                elif sub_action_data[0]["type"] == "rate_limit":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_rateLimit_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_rateLimit_rate_posXpath"]).send_keys(sub_action_data[0]["rate_value"])
                elif sub_action_data[0]["type"] == "tamper":
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_tamper_posXpath"]).click()
                elif sub_action_data[0]["type"] == "block":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_block_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    # 如mail协议的block动作，没有content内容，只需要选择code
                    if 'content_type' in sub_action_data[0]:
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_posXpath"]).click()
                        dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_block_responseContent_change_posXpath"].format(replaceValue=sub_action_data[0]["content_type"])
                        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                        if sub_action_data[0]["content_type"].lower() == "text":
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_block_responseContent_text_posId"]).send_keys(sub_action_data[0]["content"])
                        elif sub_action_data[0]["content_type"].lower() == "profile":
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_clickProfile_posXpath"]).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(sub_action_data[0]["content"])
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_block_responseContent_selectProfile_posId"]).click()
                elif sub_action_data[0]["type"] == "redirect":
                    if 'application' in  policy_configuration["condition"] and len(policy_configuration["condition"])>0:
                        application_data = policy_configuration["condition"]["application"]
                        if application_data[0]['name'] == 'http':
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
                            redirect_url = sub_action_data[0]["to_url"]
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_redirect_input_posId"]).clear()
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_redirect_input_posId"]).send_keys(redirect_url)
                        elif application_data[0]['name'] == 'dns':
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
                            resolution_len = len(sub_action_data[0]['resolution'])
                            for detail in sub_action_data[0]['resolution']:
                                answer0_len = len(detail['answer'])
                                qtype = detail['qtype']
                                if len(sub_action_data[0]['resolution']) == 1 and answer0_len == 1:
                                    answer_value_type = detail['answer'][0]['answer_value_type']
                                    atype = detail['answer'][0]['atype']
                                    ttl = detail['answer'][0]['ttl']
                                    # 点击切换qtype,默认即会选中qtype A
                                    if qtype == "AAAA":
                                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_dnsAnswerqTypeAAAA_posXpath"]).click()
                                    # 切换Answer Type
                                    self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerType0Choose_posId"]).click()
                                    answer_type_posXpath = creation_element_position["policyRulePage_dnsAnswerType0ChooseValue_posXpath"].format(replaceValue=atype)
                                    self.driver.find_element(By.XPATH, answer_type_posXpath).click()
                                    # 点击切换answer的返回方式
                                    self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswer0ValueType_posId"]).click()
                                    choose_answer_type_posXpath = creation_element_position["policyRulePage_dnsAnswer0ValueTypeChoose_posXpath"].format(replaceValue=answer_value_type)
                                    self.driver.find_element(By.XPATH, choose_answer_type_posXpath).click()
                                    if answer_value_type == "Profile":
                                        dns_records_profile_name = detail['answer'][0]['profile_name']
                                        self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerValueSelectPlaceholder_posId"]).click()
                                        self.driver.find_element(By.ID, creation_element_position["policyRulePage_dnsAnswerValueNameSearch_posId"]).send_keys(dns_records_profile_name)
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
                elif sub_action_data[0]["type"] == "alert":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_posXpath"]).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_alert_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    if sub_action_data[0]["code"] == 200:
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_posXpath"]).click()
                        dropdown_item_posXpath = creation_element_position["policyRulePage_subAction_alert_responseContent_change_posXpath"].format(replaceValue=sub_action_data[0]["content_type"])
                        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                        if sub_action_data[0]["content_type"].lower() == "text":
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_alert_responseContent_text_posId"]).send_keys(sub_action_data[0]["content"])
                        elif sub_action_data[0]["content_type"].lower() == "profile":
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_clickProfile_posXpath"]).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(sub_action_data[0]["content"])
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                            self.driver.find_element(By.ID, creation_element_position["policyRulePage_subAction_alert_responseContent_selectProfile_posId"]).click()
            
            # 添加flag
            if "flag" in policy_configuration["condition"] and len(policy_configuration["condition"]["flag"]) != 0:
                flag_data = policy_configuration["condition"]["flag"]
                for t in range(len(flag_data)):
                    if flag_data[t]['item'][0]["item_type"] == "flag":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
                        # 调用flag的定位
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addConditionFlag_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点flag的+
                        temp_element_position = creation_element_position["policyRulePage_addFlag_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 通过flag搜索并选中
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchFlag_posXpath"], find_after_wait_time=1).send_keys(flag_data[t]["name"])
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchFlag_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectFlag_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeFlag_posXpath"]).click()

            # 添加packet capture
            if "packet_capture" in policy_configuration["condition"] and len(policy_configuration["condition"]["packet_capture"]) != 0 and policy_configuration["condition"]["packet_capture"][0]["enable"] == True:
                packet_capture_data = policy_configuration["condition"]["packet_capture"]
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_posXpath"]).click()
                # 获取元素
                input_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_depth_posXpath"])
                # 使用JavaScript完全清除并设置新值
                self.driver.execute_script("arguments[0].value = '';", input_element)
                self.driver.execute_script("arguments[0].value = arguments[1];", input_element,packet_capture_data[0]["capture_depth"])
                # self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_depth_posXpath"]).clear()
                # self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_packetCapture_depth_posXpath"]).send_keys(packet_capture_data[0]["capture_depth"])
                #
            
            # 添加shaping的priority和fair factor
            if policy_configuration["type"] == "shaping":
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_priority_posId"]).clear()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_priority_posId"]).send_keys(policy_configuration["rulePriority"])
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_fairFactor_posId"]).clear()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_fairFactor_posId"]).send_keys(policy_configuration["ruleFairFactor"])
            
            # 添加statistics、shaping、sc、manipulation的profile  action parameters
            if ("action_parameter" in policy_configuration and len(policy_configuration["action_parameter"]) != 0) or ("profile" in policy_configuration and len(policy_configuration["profile"]) != 0):
                if policy_configuration["type"] == "shaping":
                    # 点profile的+
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addProfile_posXpath"]).click()
                    # 通过profile name搜索并选中
                    profile_data = policy_configuration["action_parameter"]
                    for y in range(len(profile_data)):
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=1).send_keys(profile_data[y]["name"])
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectProfile_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeProfile_posXpath"]).click()
                        if policy_configuration["multiProfile"] == True and y != len(profile_data) - 1:
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addProfile_plus_posXpath"]).click()
                elif policy_configuration["type"] == "proxy_intercept":
                    profile_data = policy_configuration["action_parameter"]
                    if "ssl_decryption_keyring" in profile_data.keys():
                        ssl_decryption_keyrings = profile_data["ssl_decryption_keyring"]
                        for i in range(len(ssl_decryption_keyrings)):
                            # trusted
                            if ssl_decryption_keyrings[i]["decryption_keying_type"] == "trusted":
                                trusted_profile_name = ssl_decryption_keyrings[i]["profile_file"]["name"]
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addTrustedSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"], find_after_wait_time=0.6).clear()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"]).send_keys(trusted_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrustedDorpItem_posXpath"], find_after_wait_time=0.6).click()
                            # untrusted
                            elif ssl_decryption_keyrings[i]["decryption_keying_type"] == "untrusted":
                                untrusted_profile_name = ssl_decryption_keyrings[i]["profile_file"]["name"]
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addUntrustedSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"], find_after_wait_time=0.6).clear()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"]).send_keys(untrusted_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchUntrustedDorpItem_posXpath"], find_after_wait_time=0.6).click()
                    # mirror decrypted profile
                    if "traffic_mirroring_profile" in profile_data.keys():
                        traffic_mirroring_profiles = profile_data["traffic_mirroring_profile"]
                        for i in range(len(traffic_mirroring_profiles)):
                            value_id = traffic_mirroring_profiles[i]["vlan_id"]
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addTrafficMirrorProfileButton_posXpath"]).click()
                            if value_id == "default":
                                continue
                            else:
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addVlanIDButton_posXpath"]).click()
                                traffic_mirroring_profile_name = traffic_mirroring_profiles[i]["profile_file"]["name"]
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addTrafficMirrorProfileSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"]).send_keys(traffic_mirroring_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTrafficMirrorProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()
                    # decryption profile
                    if "ssl_decryption_profile" in profile_data.keys():
                        ssl_decryption_profiles = profile_data["ssl_decryption_profile"]
                        for i in range(len(ssl_decryption_profiles)):
                            ssl_decryption_profile_name = ssl_decryption_profiles[i]["profile_file"]["name"]
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addDecryptionProfileSelectBox_posXpath"]).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"]).send_keys(ssl_decryption_profile_name)
                            # 点击回车键
                            search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"])
                            search_box.send_keys(Keys.RETURN)
                            # 选择第一个
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchDecryptionProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()
                    # tcp proxy profile
                    if "tcp_proxy_profile" in profile_data.keys():
                        tcp_proxy_profiles = profile_data["tcp_proxy_profile"]
                        for i in range(len(tcp_proxy_profiles)):
                            tcp_proxy_profile_name = tcp_proxy_profiles[i]["profile_file"]["name"]
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_addTcpProfileSelectBox_posXpath"]).click()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"]).send_keys(tcp_proxy_profile_name)
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
                        # 选择 response code
                        if "deny_response_block" in policy_configuration["action_parameter"].keys():    # action为 close connection
                            pass
                        else:
                            if "deny_response_text" in policy_configuration["action_parameter"].keys():
                                response_type = "deny_response_text"   # 这个变量索引key使用
                            else:
                                response_type = "response_page"
                            response_code = policy_configuration["action_parameter"][response_type][0]["response_code"]
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseCodeSelectBox_posXpath"]).click()
                            response_code_drop_position = creation_element_position["policyRulePage_deny_addResponseCodeSelectDropItem_posXpath"].format(replace_code=response_code)
                            self.driver.find_element(By.XPATH, response_code_drop_position).click()
                            # 选择 response content type
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentSelectBox_posXpath"]).click()
                            response_content_type = policy_configuration["action_parameter"][response_type][0]["response_content_type"].strip()
                            response_content_type_position = creation_element_position["policyRulePage_deny_addResponseContentSelectDropItem_posXpath"].format(replace_type=response_content_type)
                            self.driver.find_element(By.XPATH, response_content_type_position).click()
                            if response_content_type == "TEXT":
                                # 输入response content text
                                response_context_text = policy_configuration["action_parameter"][response_type][0]["response_content"].strip()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentTextInput_posXpath"]).clear()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentTextInput_posXpath"]).send_keys(response_context_text)
                            else:   # Profile
                                response_profile_data = policy_configuration["action_parameter"][response_type][0]["profile_file"]
                                response_profile_name = response_profile_data["name"]
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_addResponseContentProfileSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfile_posXpath"]).clear()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfile_posXpath"]).send_keys(response_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfile_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_deny_searchResponseProfileDorpItem_posXpath"]).click()
                    elif policy_configuration["action"] == "redirect":
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], policy_configuration["condition"]["application"][0]["name"].lower().strip())
                        if policy_configuration["condition"]["application"][0]["name"].lower().strip() == "http":
                            response_code = policy_configuration["action_parameter"]["redirect_url"][0]["response_code"]
                            response_code_drop_position = creation_element_position["policyRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath"].format(replace_code=response_code)
                            redirect_url = policy_configuration["action_parameter"]["redirect_url"][0]["redirect_url"]
                            # 操作 action parameter
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectHttp_addResponseCodeSelectBox_posXpath"]).click()
                            time.sleep(0.3)
                            btn = self.driver.find_element(By.XPATH, response_code_drop_position)
                            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
                            time.sleep(0.3)
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).send_keys(redirect_url)
                        else:
                            # 遍历，是否含有多个value
                            doh_parameter_list = policy_configuration["action_parameter"]["doh"]
                            for i in range(len(doh_parameter_list)):
                                q_type = doh_parameter_list[i]["q_type"]
                                a_type = doh_parameter_list[i]["a_type"]
                                doh_value = doh_parameter_list[i]["doh_value"]
                                doh_ttl = doh_parameter_list[i]["doh_ttl"]
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
                    elif policy_configuration["action"] == "replace":
                        # 遍历，是否含有多个search in
                        replace_parameter_list = policy_configuration["action_parameter"]["replace_parameter"]
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subActionButton_replaceText_posXpath"]).click()
                        for i in range(len(replace_parameter_list)):
                            # 从第二次遍历开始点击 + 加号
                            if i != 0:
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_add_posXpath"]).click()
                            regex_status =  replace_parameter_list[i]["regex"].lower()
                            search_in =  replace_parameter_list[i]["search_in"]
                            find_text =  replace_parameter_list[i]["find"]
                            replace_with_text =  replace_parameter_list[i]["replace_with"]
                            # 操作action parameter，  获取regex当前属性   is-checked 表示开
                            regex_class_status = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addRegex_posXpath"].format(replace_sort=i+1)).get_attribute("class")
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], regex_class_status)
                            if regex_status == "on":  # 开
                                if "Mui-checked" in regex_class_status:  # 当前状态开，不用再点击
                                    pass
                                else:   # 当前状态关，需要再点击打开
                                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addRegex_posXpath"].format(replace_sort=i+1)).click()
                            else:   # off  关
                                if "Mui-checked" in regex_class_status:  # 当前状态开，需要点击关闭
                                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addRegex_posXpath"].format(replace_sort=i+1)).click()
                                else:      # # 当前状态关，不用再点击
                                    pass
                            # 操作search in
                            search_in_drop_position = creation_element_position["policyRulePage_replace_addSearchInSelectDropItem_posXpath"].format(replace_sort=i+1, replace_type=search_in)
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addSearchInSelectBox_posXpath"].format(replace_sort=i+1)).click()
                            self.driver.find_element(By.XPATH, search_in_drop_position, find_after_wait_time=0.5).click()
                            # 操作 find   replace with 输入框
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addFindInput_posXpath"].format(replace_sort=i+1)).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addFindInput_posXpath"].format(replace_sort=i+1), find_after_wait_time=0.5).send_keys(find_text)
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addReplaceWithInput_posXpath"].format(replace_sort=i+1)).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_replace_addReplaceWithInput_posXpath"].format(replace_sort=i+1), find_after_wait_time=0.5).send_keys(replace_with_text)
                    elif policy_configuration["action"] == "hijack":
                        hijack_profile_data = policy_configuration["action_parameter"]["hijack_file"][0]["profile_file"]
                        hijack_profile_name = hijack_profile_data["name"]
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_hijack_addHijackProfileSelectBox_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_hijack_searchHijackProfile_posXpath"]).clear()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_hijack_searchHijackProfile_posXpath"]).send_keys(hijack_profile_name)
                        # 点击回车键
                        search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_hijack_searchHijackProfile_posXpath"])
                        search_box.send_keys(Keys.RETURN)
                        # 选择第一个
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_hijack_searchHijackProfileDorpItem_posXpath"]).click()
                    elif policy_configuration["action"] == "insert":
                        hijack_profile_data = policy_configuration["action_parameter"]["insert_script"][0]["profile_file"]
                        hijack_profile_name = hijack_profile_data["name"]
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_insert_addInsertProfileSelectBox_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_insert_searchInsertProfile_posXpath"]).clear()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_insert_searchInsertProfile_posXpath"]).send_keys(hijack_profile_name)
                        # 点击回车键
                        search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_insert_searchInsertProfile_posXpath"])
                        search_box.send_keys(Keys.RETURN)
                        # 选择第一个
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_insert_searchInsertProfileDorpItem_posXpath"]).click()
                    elif policy_configuration["action"] == "edit_element":
                        # 遍历多个编辑内容
                        edit_element_parameter_list = policy_configuration["action_parameter"]["edit_element_parameter"]
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_subActionButton_editElement_posXpath"]).click()
                        for i in range(len(edit_element_parameter_list)):
                            # 从第二次遍历开始点击 + 加号
                            replace_sort = i + 1
                            if i != 0:
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_add_posXpath"]).click()
                            search_scope =  edit_element_parameter_list[i]["search_scope"].lower().strip()
                            start_indicator =  edit_element_parameter_list[i]["start_indicator"].lower()
                            contained_keyword =  edit_element_parameter_list[i]["contained_keyword"].lower()
                            distance_from_anchor =  edit_element_parameter_list[i]["distance_from_anchor"].lower()
                            treatment =  edit_element_parameter_list[i]["treatment"].lower()
                            if search_scope == "whole_file":  # search scope 操作
                                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], creation_element_position["policyRulePage_editElement_addSearchScopeWholeFileRadio_posXpath"])
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addSearchScopeWholeFileRadio_posXpath"].format(replace_sort=replace_sort)).click()
                            else:    # inside_element
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addSearchScopeInsideElementRadio_posXpath"].format(replace_sort=replace_sort)).click()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addStartIndicatorInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).clear()
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addStartIndicatorInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).send_keys(start_indicator)
                            # 输入 contained_keyword
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addContainedKeywordInput_posXpath"].format(replace_sort=replace_sort)).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addContainedKeywordInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).send_keys(contained_keyword)
                            # 输入 distance_from_anchor
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addSDistanceFromAnchorInput_posXpath"].format(replace_sort=replace_sort)).clear()
                            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addSDistanceFromAnchorInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).send_keys(distance_from_anchor)
                            if treatment == "mark":
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addMarkRadio_posXpath"].format(replace_sort=replace_sort)).click()
                            else:    # inside_element
                                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_editElement_addRemoveRadio_posXpath"].format(replace_sort=replace_sort)).click()
                    elif policy_configuration["action"] == "run_script":
                        run_scirpt_profile_data = policy_configuration["action_parameter"]["run_script"][0]["profile_file"]
                        run_scirpt_profile_name = run_scirpt_profile_data["name"]
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_runScript_addrunScriptProfileSelectBox_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_runScript_searchrunScriptProfile_posXpath"]).clear()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_runScript_searchrunScriptProfile_posXpath"]).send_keys(run_scirpt_profile_name)
                        # 点击回车键
                        search_box = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_runScript_searchrunScriptProfile_posXpath"])
                        search_box.send_keys(Keys.RETURN)
                        # 选择第一个
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_runScript_searchrunScriptProfileDorpItem_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_runScript_closerunScriptProfile_posXpath"]).click()
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added manipulation action parameters..")
                elif policy_configuration["type"] == "statistics":
                    # 点击Statistics Template添加按钮打开Template侧滑列表
                    self.driver.find_element(By.XPATH, creation_element_position["plicyRulePage_addStatisticsTemplate_posXpath"]).click()
                    # 通过Statistics Template name搜索并选中
                    profile_data = policy_configuration["action_parameter"]["statistics_template"]
                    for template in range(len(profile_data)):
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=1).send_keys(profile_data[template]["name"])
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_selectProfile_posXpath"].format(replaceValue=profile_data[template]["name"]), find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_closeProfile_posXpath"]).click()
                elif policy_configuration["type"] == "service_chaining":
                    sff_data = policy_configuration["profile"]
                    # 点击SFF Profile添加按钮
                    self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_addSFFProfile_posXpath"]).click()
                    time.sleep(1)
                    #在侧滑框中搜索sff并选中
                    for sff in sff_data:
                        btn = self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_searchSFFProfile_posXpath"], find_after_wait_time=1)
                        self.driver.execute_script("arguments[0].click()", btn)
                        self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_searchSFFProfile_posXpath"]).send_keys(sff["name"])
                        self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_searchSFFProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        selectSFFXpath = creation_element_position["policyRulePage_selectSFFProfile_posXpath"].format(replaceValue=sff["name"])
                        self.driver.find_element(By.XPATH,selectSFFXpath).click()
                        # self.driver.execute_script("arguments[0].click()", btn)
                        self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_closeSFFProfile_posXpath"]).click()
                elif policy_configuration["type"] == "monitor":
                    #步骤：开启vlan_button->选择select->输入name->搜索
                    if policy_configuration["is_mirror"] == "on":
                        self.driver.find_element(By.XPATH, creation_element_position[
                            "policyRulePage_mirrorTrafficButton_posXpath"]).click()
                    else:
                        pass
                    self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_addVLANIDButton_posXpath"]).click()
                    for flag in range(len(policy_configuration["profile"])):
                        self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_firstSelectMirrorProfile_posXpath"]).click()
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchMirrorProfile_posXpath"], find_after_wait_time=1).send_keys(policy_configuration["profile"][flag]["name"])
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_searchMirrorProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH,'//ul[@class="MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd css-1cklc3"]//li[1]//div[@class="MuiListItemButton-root MuiListItemButton-colorNeutral MuiListItemButton-variantPlain css-18mv95p"]').click()
                        self.driver.find_element(By.XPATH,'//div[@class="absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]"]/button').click()

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
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_requestPerPeriod_posXpath"]).send_keys(policy_configuration["threshold"]["rate_threshold"]["request_per_period"])
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_countingPeriod_dropDownBox_posXpath"]).click()
                    temp_counting_period_element_position = creation_element_position["policyRulePage_countingPeriod_select_posXpath"].format(replaceValue=policy_configuration["threshold"]["rate_threshold"]["counting_period"])
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
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_concurrentSsessions_posXpath"]).send_keys(policy_configuration["threshold"]["concurrency_threshold"]["concurrent_sessions"])
                #self.driver.find_element(By.ID, creation_element_position["policyRulePage_mitigationBehavior_posId"]).click()
                if policy_configuration["mitigation"]["behavior"] == "deny":
                    self.driver.find_element(By.XPATH, dosRulePage_mitigationBehavior_deny_posXpath).click()
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_mitigationTimeouts_dropDownBox_posXpath"]).click()
                    temp_mitigation_timeout_element_position = creation_element_position["policyRulePage_mitigationTimeouts_select_posXpath"].format(replaceValue=policy_configuration["mitigation"]["timeout"])
                    self.driver.find_element(By.XPATH, temp_mitigation_timeout_element_position).click()
                elif policy_configuration["mitigation"]["behavior"] == "none":
                    self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_mitigationBehavior_posXpath"]).click()

            # other options 操作
            if policy_configuration["type"] == "proxy_manipulation":
                # log option =》 log all
                if "log_option" in policy_configuration:
                    if policy_configuration["log_option"] == "all":
                        self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_logOptions_all_posXpath"]).click()
                    elif policy_configuration["log_option"] == "off":
                        pass
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: todo...")
                if "effective_devices" in policy_configuration:
                    self.add_effective_devices(policy_configuration["effective_devices"], creation_element_position)

            # 点enable，不加sleep有一定几率点不上
            time.sleep(1)
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_enable_posXpath"]).click()
            # 确认创建
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_okButton_posXpath"]).click()
            #self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_okButton_warningYes_posXpath"]).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            #return 400, None
        
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
            for j in range(len(ip_data)):
                if ip_data[j]["negate"] == True:
                    time.sleep(1)  # 暂停1秒
                    negate_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_negate{}_posXpath".format(ip_condition_type)])
                    # 使用JavaScript确保元素完全进入视图
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",negate_element)
                    # 使用JavaScript执行悬停
                    self.driver.execute_script("var evt = new MouseEvent('mouseover', {'view': window, 'bubbles': true, 'cancelable': true}); arguments[0].dispatchEvent(evt);",negate_element)
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
            for j in range(len(port_data)):
                if port_data[j]["negate"] == True:
                    time.sleep(1)  # 暂停1秒
                    negate_element = self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_negate{}_posXpath".format(port_condition_type)])
                    ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                    negate_element.click()
        except Exception as e:
            raise

    def add_device(self, creation_element_position, name, negate_option):
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
    
    add_subid = add_port

    def add_protocol_field(self, protocol_field_data, filed_type, creation_element_position, num, negate_option):
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

    def add_bool_type_protocol_field(self, protocol_field_data, filed_type, creation_element_position, num, negate_option):
        try:
            for x in range(len(protocol_field_data)):
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
                var1 = protocol_field_data[x]["boolean_type"]
                xpath_temp = creation_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]
                xpath_last = xpath_temp.format(replaceValue=var1)
                self.driver.find_element(By.XPATH, xpath_last).click()
                self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                # 点protocol filed的+
                temp_element_position = creation_element_position["policyRulePage_add{}_posXpath".format(filed_type)].format(replaceValue=num)
                self.driver.find_element(By.XPATH, temp_element_position).click()
                # 通过protocol filed name搜索并选中
                self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_search{}_posXpath".format(filed_type)],find_after_wait_time=1).send_keys(protocol_field_data[x]["name"])
                self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_search{}_posXpath".format(filed_type)],find_after_wait_time=0.5).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_select{}_posXpath".format(filed_type)],find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_close{}_posXpath".format(filed_type)]).click()
                num = num +1
        except Exception as e:
            raise

    def add_ip_protocol(self, ip_protocol_data, filed_type, creation_element_position, negate_option):
        try:
            # 点add condition的+
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition_posXpath"]).click()
            # 选中port
            self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]).click()
            self.driver.find_element(By.XPATH,creation_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点source port的+
            self.driver.find_element(By.XPATH, creation_element_position[ "policyRulePage_add{}_posXpath".format(filed_type)]).click()
            # 通过port name搜索并选中
            is_first_iteration = True
            for z in ip_protocol_data:
                #如果不是第一次循环，需要点加号调侧滑框
                if not is_first_iteration:
                    self.driver.find_element(By.XPATH, policyRulePage_little_button_addIpProtocol_posXpath).click()
                self.driver.find_element(By.XPATH, creation_element_position["policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=1).send_keys(z)
                self.driver.find_element(By.XPATH, creation_element_position[ "policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                temp_element_position = creation_element_position[ "policyRulePage_select{}_posXpath".format(filed_type)].format( replaceValue=z)
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
                        return [True, or_conditions[j], or_conditions["negate_option"]]
        return [False, "", ""]
    
    def is_group_exsit(self, policy_configuration):
        if "and_conditions" in policy_configuration:
            and_conditions = policy_configuration["and_conditions"]
            for i in range(len(and_conditions)):
                or_conditions = and_conditions[i]["or_conditions"]
                for j in range(len(or_conditions)):
                    if "member_type" in or_conditions[j].keys and or_conditions[j]["member_type"] != "":
                        return [True, or_conditions[j], or_conditions["negate_option"]]
        return [False, "", ""]
