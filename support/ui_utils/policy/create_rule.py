# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
from telnetlib import EC

from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from trio import sleep

from support.ui_utils.policy.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
import traceback
from datetime import datetime 

class CreateRule:
    def __init__(self, driver):
        self.driver = driver
        
    def create(self, test_data, rule_element_position):
        page_jump_element_position = rule_element_position["page_jump"]
        create_element_position = rule_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_policy_page(page_jump_element_position)

            # 点击create
            time.sleep(0.3)
            self.driver.find_element(By.XPATH, create_element_position["policyRuleListPage_createButton_posXpath"]).click()
            
            # 输入name
            rule_name = test_data["rule_name"]
            time.sleep(0.5)
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_inputName_posXpath"]).send_keys(rule_name)
            
            # 选择action
            if test_data["policy_type"] == "security" or test_data["policy_type"] == "pxy_intercept" or test_data["policy_type"] == "dos_protection":
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectAction_posXpath"]).click()
            elif test_data["policy_type"] == "pxy_manipulation":
                if test_data["rule_action"] == "allow":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectAllow_posXpath"]).click()
                elif test_data["rule_action"] == "deny":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectDeny_posXpath"]).click()
                elif test_data["rule_action"] == "monitor":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectMonitor_posXpath"]).click()
                elif test_data["rule_action"] == "redirect":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectRedirect_posXpath"]).click()
                elif test_data["rule_action"] == "replace":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectReplace_posXpath"]).click()
                elif test_data["rule_action"] == "hijack":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectHijack_posXpath"]).click()
                elif test_data["rule_action"] == "insert":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectInsert_posXpath"]).click()
                elif test_data["rule_action"] == "edit_element":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectEditElement_posXpath"]).click()
                else:   # run script
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectRunScript_posXpath"]).click()
            elif test_data["policy_type"]== "monitor" and  "is_mirror" in test_data :
                if test_data["is_mirror"] == "on":
                    self.driver.find_element(By.XPATH,create_element_position["policyRulePage_mirrorTrafficButton_posXpath"]).click()
                else:
                    pass
                if "log_options" in test_data  and test_data["log_options"] == "all":
                    self.driver.find_element(By.XPATH,monitorRulePage_logOptions_all_posXpath).click()

            # 添加ip
            if "source_ip" in test_data["condition"] and len(test_data["condition"]["source_ip"]) != 0:
                src_ip_data = test_data["condition"]["source_ip"]
                self.add_ip(src_ip_data, "SrcIP", create_element_position)
            if "source_ip_group" in test_data["condition"] and len(test_data["condition"]["source_ip_group"]) != 0:
                src_ip_group_data = test_data["condition"]["source_ip_group"]
                self.add_ip(src_ip_group_data, "SrcIP", create_element_position)
            if "destination_ip" in test_data["condition"] and len(test_data["condition"]["destination_ip"]) != 0:
                dst_ip_data = test_data["condition"]["destination_ip"]
                self.add_ip(dst_ip_data, "DstIP", create_element_position)
            if "destination_ip_group" in test_data["condition"] and len(test_data["condition"]["destination_ip_group"]) != 0:
                dst_ip_group_data = test_data["condition"]["destination_ip_group"]
                self.add_ip(dst_ip_group_data, "DstIP", create_element_position)
            if "internal_ip" in test_data["condition"] and len(test_data["condition"]["internal_ip"]) != 0:
                internal_ip_data = test_data["condition"]["internal_ip"]
                self.add_ip(internal_ip_data, "InternalIP", create_element_position)
            if "internal_ip_group" in test_data["condition"] and len(test_data["condition"]["internal_ip_group"]) != 0:
                internal_ip_group_data = test_data["condition"]["internal_ip_group"]
                self.add_ip(internal_ip_group_data, "InternalIP", create_element_position)
            if "external_ip" in test_data["condition"] and len(test_data["condition"]["external_ip"]) != 0:
                external_ip_data = test_data["condition"]["external_ip"]
                self.add_ip(external_ip_data, "ExternalIP", create_element_position)
            if "external_ip_group" in test_data["condition"] and len(test_data["condition"]["external_ip_group"]) != 0:
                external_ip_group_data = test_data["condition"]["external_ip_group"]
                self.add_ip(external_ip_group_data, "ExternalIP", create_element_position)
                
            # 添加port
            if "source_port" in test_data["condition"] and len(test_data["condition"]["source_port"]) != 0:
                src_port_data = test_data["condition"]["source_port"]
                self.add_port(src_port_data, "SrcPort", create_element_position)
            if "source_port_group" in test_data["condition"] and len(test_data["condition"]["source_port_group"]) != 0:
                src_port_group_data = test_data["condition"]["source_port_group"]
                self.add_port(src_port_group_data, "SrcPort", create_element_position)
            if "destination_port" in test_data["condition"] and len(test_data["condition"]["destination_port"]) != 0:
                dst_port_data = test_data["condition"]["destination_port"]    
                self.add_port(dst_port_data, "DstPort", create_element_position)
            if "destination_port_group" in test_data["condition"] and len(test_data["condition"]["destination_port_group"]) != 0:
                dst_port_group_data = test_data["condition"]["destination_port_group"]
                self.add_port(dst_port_group_data, "DstPort", create_element_position)
            if "internal_port" in test_data["condition"] and len(test_data["condition"]["internal_port"]) != 0:
                internal_port_data = test_data["condition"]["internal_port"]
                self.add_port(internal_port_data, "InternalPort", create_element_position)
            if "internal_port_group" in test_data["condition"] and len(test_data["condition"]["internal_port_group"]) != 0:
                internal_port_group_data = test_data["condition"]["internal_port_group"]
                self.add_port(internal_port_group_data, "InternalPort", create_element_position)
            if "external_port" in test_data["condition"] and len(test_data["condition"]["external_port"]) != 0:
                external_port_data = test_data["condition"]["external_port"]
                self.add_port(external_port_data, "ExternalPort", create_element_position)
            if "external_port_group" in test_data["condition"] and len(test_data["condition"]["external_port_group"]) != 0:
                external_port_group_data = test_data["condition"]["external_port_group"]
                self.add_port(external_port_group_data, "ExternalPort", create_element_position)

            if "sub_id" in test_data["condition"] and len(test_data["condition"]["sub_id"]) != 0:
                subid_data = test_data["condition"]["sub_id"]
                self.add_subid(subid_data, "User", create_element_position)

            # 添加device
            if "device" in test_data["condition"] and len(test_data["condition"]["device"]) != 0:
                device_data = test_data["condition"]["device"]
                for t in range(len(device_data)):
                    if device_data[t]['item'][0]["item_type"] == "imsi":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                        # 选中imsi
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addConditionImsi_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点imsi的+，因为dst ip已经是第一层且t初始值是0，所以要+2
                        temp_element_position = create_element_position["policyRulePage_addImsi_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 通过imsi搜索并选中
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=1).send_keys(device_data[t]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectImsi_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeImsi_posXpath"]).click()
                    elif device_data[t]['item'][0]["item_type"] == "phone_number":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                        # 都属于device，所以调用imsi的定位即可
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addConditionImsi_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点device的+
                        temp_element_position = create_element_position["policyRulePage_addImsi_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 选中phone number
                        temp_element_position = create_element_position["policyRulePage_choosePhoneNumber_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 通过phone number搜索并选中(与imsi共用)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=1).send_keys(device_data[t]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectImsi_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeImsi_posXpath"]).click()
                    elif device_data[t]['item'][0]["item_type"] ==  "imei":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                        # 都属于device，所以调用imsi的定位即可
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addConditionImsi_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点device的+
                        temp_element_position = create_element_position["policyRulePage_addImsi_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 选中phone number
                        temp_element_position = create_element_position["policyRulePage_chooseImei_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 通过phone number搜索并选中(与imsi共用)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=1).send_keys(device_data[t]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectImsi_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeImsi_posXpath"]).click()
                    for j in range(len(device_data)):
                            if device_data[j]["negate"] == True:
                                time.sleep(1)  # 暂停1秒
                                negate_element = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_negateImsi_posXpath"])
                                ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                                negate_element.click()
            # 添加apn
            if "apn" in test_data["condition"] and len(test_data["condition"]["apn"]) != 0:
                device_data = test_data["condition"]["apn"]
                for t in range(len(device_data)):
                    if device_data[t]['items'][0]["item_type"] == "apn":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                        # 都属于device，所以调用apn的定位即可
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addConditionImsi_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点device的+
                        temp_element_position = create_element_position["policyRulePage_addImsi_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 选中apn
                        temp_element_position = create_element_position["policyRulePage_chooseApn_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 通过apn搜索并选中(与imsi共用)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=1).send_keys(device_data[t]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchImsi_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectImsi_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeImsi_posXpath"]).click()

            # 添加application
            if "application" in test_data["condition"] and len(test_data["condition"]["application"]) != 0:
                if test_data["policy_type"] == "pxy_manipulation":
                    if  test_data["condition"]["application"][0]["name"].lower() == "doh":  # doh需要操作application
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addApplication_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchDoHApplication_posXpath"], find_before_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeApplication_posXpath"]).click()
                    else:   # 非doh不需要操作application
                        pass
                else:
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addApplication_posXpath"]).click()
                    application_data = test_data["condition"]["application"]
                    # 通过application name搜索并选中
                    for j in range(len(application_data)):
                        if application_data[j]["object_type"] == "application_group":
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplicationGroupLabel_posXpath"]).click()
                        if test_data["policy_type"] == "pxy_intercept":  # intercept 中 application不用搜索，直接选择
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplication_posXpath"].format(replaceValue=application_data[j]["name"]), find_after_wait_time=0.5).click()
                        else:
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=1).send_keys(application_data[j]["name"])
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplication_posXpath"].format(replaceValue = application_data[j]["name"]), find_after_wait_time=0.5).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeApplication_posXpath"]).click()

            # 添加server fqdn
            if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
                server_fqdn_data = test_data["condition"]["server_fqdn"]
                for t in range(len(server_fqdn_data)):
                    if server_fqdn_data[t]["object_type"] == "fqdn":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                        time.sleep(1)
                        # 选中server fqdn
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addConditionServerFqdn_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点server fqdn的+，因为dst ip已经是第一层且t初始值是0，所以要+2
                        # temp = t + 2
                        # temp_element_position = create_element_position["policyRulePage_addServerFqdn_posXpath"].format(replaceValue=temp)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addServerFqdn_posXpath"]).click()
                        time.sleep(1)
                        # 通过server fqdn name搜索并选中
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchServerFqdn_posXpath"], find_after_wait_time=1).send_keys(server_fqdn_data[t]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchServerFqdn_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        btn = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectServerFqdn_posXpath"], find_after_wait_time= 1)
                        self.driver.execute_script("arguments[0].click()", btn)
                        # self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectServerFqdn_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeServerFqdn_posXpath"]).click()
                        if server_fqdn_data[t]["negate"] == True:
                            time.sleep(1)
                            negate_element = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_negateServerFqdn_posXpath"].format(replaceValue=temp))
                            ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                            negate_element.click()
                    elif server_fqdn_data[t]["object_type"] == "category":
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added...")

            #添加ip_protocol
            if "ip_protocol" in test_data["condition"] and len(test_data["condition"]["ip_protocol"]) != 0:
                protocol_field_data = test_data["condition"]["ip_protocol"]
                self.add_ip_protocol(protocol_field_data, "IpProtocol", create_element_position)

            # 添加protocol field
            if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
                protocol_field_datas = test_data["condition"]["protocol_filed"]
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
                    elif tmp_item["object_type"] == "http_signature":
                        if tmp_item["item"][0]["item_type"] == "request_header":
                            tmp_request_header.append(tmp_item)
                        elif tmp_item["item"][0]["item_type"] == "response_header":
                            tmp_response_header.append(tmp_item)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "check..")
                    elif tmp_item["object_type"] == "keywords":
                        if tmp_item["item"][0]["item_type"] == "request_body":
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
                        elif tmp_item["items"][0]["item_type"] == "mail_to":
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
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], tmp_protocol_field_data_split_by_type)
                for protocol_field_data in tmp_protocol_field_data_split_by_type:
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], protocol_field_data)
                    for x in range(len(protocol_field_data)):
                        temp = x + 1
                        if protocol_field_data[x]["object_type"] == "url":
                            self.add_protocol_field(protocol_field_data, "Url", create_element_position, temp)
                        elif protocol_field_data[x]["object_type"] == "fqdn":
                            for item_dict in protocol_field_data[x]["items"]:
                                if item_dict["item_type"] == "cn":
                                    self.add_protocol_field(protocol_field_data, "Cn", create_element_position, temp)
                                elif item_dict["item_type"] == "san":
                                    self.add_protocol_field(protocol_field_data, "San", create_element_position, temp)
                                elif item_dict["item_type"] == "qname":
                                    self.add_protocol_field(protocol_field_data, "Qname", create_element_position, temp)
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        elif protocol_field_data[x]["object_type"] == "http_signature":
                            item_dict = protocol_field_data[x]["item"][0]
                            if item_dict["item_type"] == "request_header":
                                self.add_protocol_field(protocol_field_data, "RequestHeader", create_element_position, temp)
                            elif item_dict["item_type"] == "response_header":
                                self.add_protocol_field(protocol_field_data, "ResponseHeader", create_element_position, temp)
                            else:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        elif protocol_field_data[x]["object_type"] == "keywords":
                            item_dict = protocol_field_data[x]["item"][0]
                            if item_dict["item_type"] == "request_body":
                                self.add_protocol_field(protocol_field_data, "RequestBody", create_element_position, temp)
                            elif item_dict["item_type"] == "response_body":
                                self.add_protocol_field(protocol_field_data, "ResponseBody", create_element_position, temp)
                            elif item_dict["item_type"] == "ftp_content":
                                self.add_protocol_field(protocol_field_data, "FtpContent", create_element_position, temp)
                            elif item_dict["item_type"] == "mail_subject":
                                self.add_protocol_field(protocol_field_data, "MailSubject", create_element_position, temp)
                            elif item_dict["item_type"] == "mail_attachment_name":
                                self.add_protocol_field(protocol_field_data, "MailAttachmentName", create_element_position, temp)
                            elif item_dict["item_type"] == "mail_attachment_content":
                                self.add_protocol_field(protocol_field_data, "MailAttachmentContent", create_element_position, temp)
                            elif item_dict["item_type"] == "mail_content":
                                self.add_protocol_field(protocol_field_data, "MailContent", create_element_position, temp)
                            else:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        elif protocol_field_data[x]["object_type"] == "account":
                            for item_dict in protocol_field_data[x]["items"]:
                                if item_dict["item_type"] == "ftp_account":
                                    self.add_protocol_field(protocol_field_data, "FtpAccount", create_element_position, temp)
                                elif item_dict["item_type"] == "mail_account":
                                    self.add_protocol_field(protocol_field_data, "MailAccount",create_element_position, temp)
                                elif item_dict["item_type"] == "mail_from":
                                    self.add_protocol_field(protocol_field_data, "MailFrom", create_element_position,temp)
                                elif item_dict["item_type"] == "mail_to":
                                    self.add_protocol_field(protocol_field_data, "MailTo", create_element_position,temp)
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"todo {item_dict['item_type']}")
                        elif protocol_field_data[x]["object_type"] == 'boolean':
                            self.add_bool_type_protocol_field(protocol_field_data, "Boolean", create_element_position, temp)
                            break

            if "application" in test_data["condition"] and len(test_data["condition"]["application"]) != 0 and "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) == 0:
                override_flag = True
            else:
                override_flag = False
            
            # 选择target traffic 
            if test_data["policy_type"] == "service_chaining":
                if test_data["targeted_traffic"] == "decrypted":
                    self.driver.find_element(By.XPATH,create_element_position["policyRulePage_decryptedTraffic_posXpath"]).click()
                else:
                    self.driver.find_element(By.XPATH,create_element_position["policyRulePage_rawTraffic_posXpath"]).click()

            # 添加sub action
            if "sub_action" in test_data["condition"] and len(test_data["condition"]["sub_action"]) != 0 and test_data["condition"]["sub_action_override"] == True:
                sub_action_data = test_data["condition"]["sub_action"]
                if override_flag == True:
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_override_posXpath"]).click()
                if sub_action_data[0]["type"] == "drop":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).clear()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).send_keys(sub_action_data[0]["drop_packet"])
                    # quic不支持tcp rst；默认tcp rst是选中，不需要操作，只有当sendTcpRst为false时
                    if (override_flag == False and len(test_data["condition"]["application"]) == 1 and test_data["condition"]["application"][0]['name'] == "quic")or (sub_action_data[0]["send_tcp_rst"] == False and test_data["condition"]["application"][0]['name'] != "quic" and test_data["condition"]["application"][0]['name'] != "dns"):
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_sendTcpRst_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_sendIcmp_posXpath"]).click()
                elif sub_action_data[0]["type"] == "rate_limit":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_rateLimit_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_rateLimit_rate_posXpath"]).send_keys(sub_action_data[0]["rate_value"])
                elif sub_action_data[0]["type"] == "tamper":
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_tamper_posXpath"]).click()
                elif sub_action_data[0]["type"] == "block":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_block_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    # 如mail协议的block动作，没有content内容，只需要选择code
                    if 'content_type' in sub_action_data[0]:
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_posXpath"]).click()
                        dropdown_item_posXpath = create_element_position["policyRulePage_subAction_block_responseContent_change_posXpath"].format(replaceValue=sub_action_data[0]["content_type"])
                        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                        if sub_action_data[0]["content_type"].lower() == "text":
                            self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_block_responseContent_text_posId"]).send_keys(sub_action_data[0]["content"])
                        elif sub_action_data[0]["content_type"].lower() == "profile":
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_clickProfile_posXpath"]).click()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(sub_action_data[0]["content"])
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                            self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_block_responseContent_selectProfile_posId"]).click()
                elif sub_action_data[0]["type"] == "redirect":
                    if 'application' in  test_data["condition"] and len(test_data["condition"])>0:
                        application_data = test_data["condition"]["application"]
                        if application_data[0]['name'] == 'http':
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
                            redirect_url = sub_action_data[0]["to_url"]
                            self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_redirect_input_posId"]).clear()
                            self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_redirect_input_posId"]).send_keys(redirect_url)
                        elif application_data[0]['name'] == 'dns':
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
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
                                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_dnsAnswerqTypeAAAA_posXpath"]).click()
                                    # 切换Answer Type
                                    self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswerType0Choose_posId"]).click()
                                    answer_type_posXpath = create_element_position["policyRulePage_dnsAnswerType0ChooseValue_posXpath"].format(replaceValue=atype)
                                    self.driver.find_element(By.XPATH, answer_type_posXpath).click()
                                    # 点击切换answer的返回方式
                                    self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswer0ValueType_posId"]).click()
                                    choose_answer_type_posXpath = create_element_position["policyRulePage_dnsAnswer0ValueTypeChoose_posXpath"].format(replaceValue=answer_value_type)
                                    self.driver.find_element(By.XPATH, choose_answer_type_posXpath).click()
                                    if answer_value_type == "Profile":
                                        dns_records_profile_name = detail['answer'][0]['profile_name']
                                        self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswerValueSelectPlaceholder_posId"]).click()
                                        self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswerValueNameSearch_posId"]).send_keys(dns_records_profile_name)
                                        self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswerValueNameSearch_posId"]).send_keys(Keys.ENTER)
                                        self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswerValueNameSelect_posId"]).click()
                                    else:
                                        dns_text_value = detail['answer'][0]['answer_value']
                                        if atype == "A":
                                            self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswer0ATextPlaceholder_posId"]).send_keys(dns_text_value)
                                        elif atype == "AAAA":
                                            self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswer0AAAATextPlaceholder_posId"]).send_keys(dns_text_value)
                                        elif atype == "CNAME":
                                            self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswer0CnameTextPlaceholder_posId"]).send_keys(dns_text_value)   
                                    self.driver.find_element(By.ID, create_element_position["policyRulePage_dnsAnswerValueTTL0_posId"]).send_keys(ttl)
                elif sub_action_data[0]["type"] == "alert":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_alert_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    if sub_action_data[0]["code"] == 200:
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_posXpath"]).click()
                        dropdown_item_posXpath = create_element_position["policyRulePage_subAction_alert_responseContent_change_posXpath"].format(replaceValue=sub_action_data[0]["content_type"])
                        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                        if sub_action_data[0]["content_type"].lower() == "text":
                            self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_alert_responseContent_text_posId"]).send_keys(sub_action_data[0]["content"])
                        elif sub_action_data[0]["content_type"].lower() == "profile":
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_clickProfile_posXpath"]).click()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(sub_action_data[0]["content"])
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                            self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_alert_responseContent_selectProfile_posId"]).click()
            # 添加flag
            if "flag" in test_data["condition"] and len(test_data["condition"]["flag"]) != 0:
                flag_data = test_data["condition"]["flag"]
                for t in range(len(flag_data)):
                    if flag_data[t]['item'][0]["item_type"] == "flag":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                        # 调用flag的定位
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addConditionFlag_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点flag的+
                        temp_element_position = create_element_position["policyRulePage_addFlag_posXpath"]
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 通过flag搜索并选中(与imsi共用)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchFlag_posXpath"], find_after_wait_time=1).send_keys(flag_data[t]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchFlag_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectFlag_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeFlag_posXpath"]).click()

            # 添加packet capture
            if "packet_capture" in test_data["condition"] and len(test_data["condition"]["packet_capture"]) != 0 and test_data["condition"]["packet_capture"][0]["enable"] == True:
                packet_capture_data = test_data["condition"]["packet_capture"]
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_posXpath"]).click()
                # 获取元素
                input_element = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_depth_posXpath"])
                # 使用JavaScript完全清除并设置新值
                self.driver.execute_script("arguments[0].value = '';", input_element)
                self.driver.execute_script("arguments[0].value = arguments[1];", input_element,packet_capture_data[0]["capture_depth"])
                # self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_depth_posXpath"]).clear()
                # self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_depth_posXpath"]).send_keys(packet_capture_data[0]["capture_depth"])
                #
            # 添加shaping的priority和fair factor
            if test_data["policy_type"] == "shaping":
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_priority_posId"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_priority_posId"]).send_keys(test_data["rulePriority"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_fairFactor_posId"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_fairFactor_posId"]).send_keys(test_data["ruleFairFactor"])
            
            # 添加statistics、shaping、sc、manipulation的profile  action parameters
            if ("action_parameter" in test_data and len(test_data["action_parameter"]) != 0) or ("profile" in test_data and len(test_data["profile"]) != 0):
                if test_data["policy_type"] == "shaping":
                    # 点profile的+
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_posXpath"]).click()
                    # 通过profile name搜索并选中
                    profile_data = test_data["action_parameter"]
                    for y in range(len(profile_data)):
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=1).send_keys(profile_data[y]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectProfile_posXpath"], find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeProfile_posXpath"]).click()
                        if test_data["multiProfile"] == True and y != len(profile_data) - 1:
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_plus_posXpath"]).click()
                elif test_data["policy_type"] == "pxy_intercept":
                    profile_data = test_data["action_parameter"]
                    if "ssl_decryption_keyring" in profile_data.keys():
                        ssl_decryption_keyrings = profile_data["ssl_decryption_keyring"]
                        for i in range(len(ssl_decryption_keyrings)):
                            # trusted
                            if ssl_decryption_keyrings[i]["decryption_keying_type"] == "trusted":
                                trusted_profile_name = ssl_decryption_keyrings[i]["profile_file"]["name"]
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_addTrustedSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"], find_after_wait_time=0.6).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"]).send_keys(trusted_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTrustedInput_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTrustedDorpItem_posXpath"], find_after_wait_time=0.6).click()
                            # untrusted
                            elif ssl_decryption_keyrings[i]["decryption_keying_type"] == "untrusted":
                                untrusted_profile_name = ssl_decryption_keyrings[i]["profile_file"]["name"]
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_addUntrustedSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"], find_after_wait_time=0.6).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"]).send_keys(untrusted_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchUntrustedInput_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchUntrustedDorpItem_posXpath"], find_after_wait_time=0.6).click()
                    # mirror decrypted profile
                    if "traffic_mirroring_profile" in profile_data.keys():
                        traffic_mirroring_profiles = profile_data["traffic_mirroring_profile"]
                        for i in range(len(traffic_mirroring_profiles)):
                            value_id = traffic_mirroring_profiles[i]["vlan_id"]
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_addTrafficMirrorProfileButton_posXpath"]).click()
                            if value_id == "default":
                                continue
                            else:
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_addVlanIDButton_posXpath"]).click()
                                traffic_mirroring_profile_name = traffic_mirroring_profiles[i]["profile_file"]["name"]
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_addTrafficMirrorProfileSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"]).send_keys(traffic_mirroring_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTrafficMirrorProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()
                    # decryption profile
                    if "ssl_decryption_profile" in profile_data.keys():
                        ssl_decryption_profiles = profile_data["ssl_decryption_profile"]
                        for i in range(len(ssl_decryption_profiles)):
                            ssl_decryption_profile_name = ssl_decryption_profiles[i]["profile_file"]["name"]
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_addDecryptionProfileSelectBox_posXpath"]).click()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"]).send_keys(ssl_decryption_profile_name)
                            # 点击回车键
                            search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchDecryptionProfileInput_posXpath"])
                            search_box.send_keys(Keys.RETURN)
                            # 选择第一个
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchDecryptionProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()
                    # tcp proxy profile
                    if "tcp_proxy_profile" in profile_data.keys():
                        tcp_proxy_profiles = profile_data["tcp_proxy_profile"]
                        for i in range(len(tcp_proxy_profiles)):
                            tcp_proxy_profile_name = tcp_proxy_profiles[i]["profile_file"]["name"]
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_addTcpProfileSelectBox_posXpath"]).click()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"], find_after_wait_time=0.6).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"]).send_keys(tcp_proxy_profile_name)
                            # 点击回车键
                            search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTcpProfileInput_posXpath"])
                            search_box.send_keys(Keys.RETURN)
                            # 选择第一个
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_intercept_searchTcpProfileDorpItem_posXpath"], find_after_wait_time=0.6).click()

                elif test_data["policy_type"] == "pxy_manipulation":
                    profile_data = test_data["action_parameter"]
                    # 页面滚动到最底部
                    div_container = self.driver.find_element(By.XPATH, "//div[@class='VEditPanel']/div[@class='panel-container']")
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", div_container)  # 移动到页面最底部
                    if test_data["rule_action"] == "deny":
                        # 选择 response code
                        if "deny_response_block" in test_data["action_parameter"].keys():    # action为 close connection
                            pass
                        else:
                            if "deny_response_text" in test_data["action_parameter"].keys():
                                response_type = "deny_response_text"   # 这个变量索引key使用
                            else:
                                response_type = "response_page"
                            response_code = test_data["action_parameter"][response_type][0]["response_code"]
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_addResponseCodeSelectBox_posXpath"]).click()
                            response_code_drop_position = create_element_position["policyRulePage_deny_addResponseCodeSelectDropItem_posXpath"].format(replace_code=response_code)
                            self.driver.find_element(By.XPATH, response_code_drop_position).click()
                            # 选择 response content type
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_addResponseContentSelectBox_posXpath"]).click()
                            response_content_type = test_data["action_parameter"][response_type][0]["response_content_type"].strip()
                            response_content_type_position = create_element_position["policyRulePage_deny_addResponseContentSelectDropItem_posXpath"].format(replace_type=response_content_type)
                            self.driver.find_element(By.XPATH, response_content_type_position).click()
                            if response_content_type == "TEXT":
                                # 输入response content text
                                response_context_text = test_data["action_parameter"][response_type][0]["response_content"].strip()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_addResponseContentTextInput_posXpath"]).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_addResponseContentTextInput_posXpath"]).send_keys(response_context_text)
                            else:   # Profile
                                response_profile_data = test_data["action_parameter"][response_type][0]["profile_file"]
                                response_profile_name = response_profile_data["name"]
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_addResponseContentProfileSelectBox_posXpath"]).click()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_searchResponseProfile_posXpath"]).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_searchResponseProfile_posXpath"]).send_keys(response_profile_name)
                                # 点击回车键
                                search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_searchResponseProfile_posXpath"])
                                search_box.send_keys(Keys.RETURN)
                                # 选择第一个
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_deny_searchResponseProfileDorpItem_posXpath"]).click()
                    elif test_data["rule_action"] == "redirect":
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], test_data["condition"]["application"][0]["name"].lower().strip())
                        if test_data["condition"]["application"][0]["name"].lower().strip() == "http":
                            response_code = test_data["action_parameter"]["redirect_url"][0]["response_code"]
                            response_code_drop_position = create_element_position["policyRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath"].format(replace_code=response_code)
                            redirect_url = test_data["action_parameter"]["redirect_url"][0]["redirect_url"]
                            # 操作 action parameter
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectHttp_addResponseCodeSelectBox_posXpath"]).click()
                            time.sleep(0.3)
                            btn = self.driver.find_element(By.XPATH, response_code_drop_position)
                            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
                            time.sleep(0.3)
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).send_keys(redirect_url)
                        else:
                            # 遍历，是否含有多个value
                            doh_parameter_list = test_data["action_parameter"]["doh"]
                            for i in range(len(doh_parameter_list)):
                                q_type = doh_parameter_list[i]["q_type"]
                                a_type = doh_parameter_list[i]["a_type"]
                                doh_value = doh_parameter_list[i]["doh_value"]
                                doh_ttl = doh_parameter_list[i]["doh_ttl"]
                                replace_index = i + 2
                                if i != 0:    # 非第一次遍历点击
                                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_add_posXpath"]).click()
                                if i == 0:   # 只有第一次遍历点击
                                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_qtypeRadio_posXpath"].format(replace_qtype=q_type)).click()
                                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_atypeSelectBox_posXpath"].format(replace_index=replace_index)).click()
                                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_atypeSelectDropItem_posXpath"].format(replace_atype=a_type)).click()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_valueInput_posXpath"].format(replace_index=replace_index)).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_valueInput_posXpath"].format(replace_index=replace_index), find_after_wait_time=0.5).send_keys(doh_value)
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_ttlInput_posXpath"].format(replace_index=replace_index)).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectDoH_ttlInput_posXpath"].format(replace_index=replace_index), find_after_wait_time=0.5).send_keys(doh_ttl)
                    elif test_data["rule_action"] == "replace":
                        # 遍历，是否含有多个search in
                        replace_parameter_list = test_data["action_parameter"]["replace_parameter"]
                        for i in range(len(replace_parameter_list)):
                            # 从第二次遍历开始点击 + 加号
                            if i != 0:
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_add_posXpath"]).click()
                            regex_status =  replace_parameter_list[i]["regex"].lower()
                            search_in =  replace_parameter_list[i]["search_in"]
                            find_text =  replace_parameter_list[i]["find"]
                            replace_with_text =  replace_parameter_list[i]["replace_with"]
                            # 操作action parameter，  获取regex当前属性   is-checked 表示开
                            regex_class_status = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addRegex_posXpath"].format(replace_sort=i+1)).get_attribute("class")
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], regex_class_status)
                            if regex_status == "on":  # 开
                                if "is-checked" in regex_class_status:  # 当前状态开，不用再点击
                                    pass
                                else:   # 当前状态关，需要再点击打开
                                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addRegex_posXpath"].format(replace_sort=i+1)).click()
                            else:   # off  关
                                if "is-checked" in regex_class_status:  # 当前状态开，需要点击关闭
                                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addRegex_posXpath"].format(replace_sort=i+1)).click()
                                else:      # # 当前状态关，不用再点击
                                    pass
                            # 操作search in
                            search_in_drop_position = create_element_position["policyRulePage_replace_addSearchInSelectDropItem_posXpath"].format(replace_type=search_in)
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addSearchInSelectBox_posXpath"].format(replace_sort=i+1)).click()
                            self.driver.find_element(By.XPATH, search_in_drop_position, find_after_wait_time=0.5).click()
                            # 操作 find   replace with 输入框
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addFindInput_posXpath"].format(replace_sort=i+1)).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addFindInput_posXpath"].format(replace_sort=i+1), find_after_wait_time=0.5).send_keys(find_text)
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addReplaceWithInput_posXpath"].format(replace_sort=i+1)).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_replace_addReplaceWithInput_posXpath"].format(replace_sort=i+1), find_after_wait_time=0.5).send_keys(replace_with_text)
                    elif test_data["rule_action"] == "hijack":
                        hijack_profile_data = test_data["action_parameter"]["hijack_file"][0]["profile_file"]
                        hijack_profile_name = hijack_profile_data["name"]
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_hijack_addHijackProfileSelectBox_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_hijack_searchHijackProfile_posXpath"]).clear()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_hijack_searchHijackProfile_posXpath"]).send_keys(hijack_profile_name)
                        # 点击回车键
                        search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_hijack_searchHijackProfile_posXpath"])
                        search_box.send_keys(Keys.RETURN)
                        # 选择第一个
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_hijack_searchHijackProfileDorpItem_posXpath"]).click()
                    elif test_data["rule_action"] == "insert":
                        hijack_profile_data = test_data["action_parameter"]["insert_script"][0]["profile_file"]
                        hijack_profile_name = hijack_profile_data["name"]
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_insert_addInsertProfileSelectBox_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_insert_searchInsertProfile_posXpath"]).clear()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_insert_searchInsertProfile_posXpath"]).send_keys(hijack_profile_name)
                        # 点击回车键
                        search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_insert_searchInsertProfile_posXpath"])
                        search_box.send_keys(Keys.RETURN)
                        # 选择第一个
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_insert_searchInsertProfileDorpItem_posXpath"]).click()
                    elif test_data["rule_action"] == "edit_element":
                        # 遍历多个编辑内容
                        edit_element_parameter_list = test_data["action_parameter"]["edit_element_parameter"]
                        for i in range(len(edit_element_parameter_list)):
                            # 从第二次遍历开始点击 + 加号
                            replace_sort = i + 1
                            if i != 0:
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_add_posXpath"]).click()
                            search_scope =  edit_element_parameter_list[i]["search_scope"].lower().strip()
                            start_indicator =  edit_element_parameter_list[i]["start_indicator"].lower()
                            contained_keyword =  edit_element_parameter_list[i]["contained_keyword"].lower()
                            distance_from_anchor =  edit_element_parameter_list[i]["distance_from_anchor"].lower()
                            treatment =  edit_element_parameter_list[i]["treatment"].lower()
                            if search_scope == "whole_file":  # search scope 操作
                                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], create_element_position["policyRulePage_editElement_addSearchScopeWholeFileRadio_posXpath"])
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addSearchScopeWholeFileRadio_posXpath"].format(replace_sort=replace_sort)).click()
                            else:    # inside_element
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addSearchScopeInsideElementRadio_posXpath"].format(replace_sort=replace_sort)).click()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addStartIndicatorInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).clear()
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addStartIndicatorInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).send_keys(start_indicator)
                            # 输入 contained_keyword
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addContainedKeywordInput_posXpath"].format(replace_sort=replace_sort)).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addContainedKeywordInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).send_keys(contained_keyword)
                            # 输入 distance_from_anchor
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addSDistanceFromAnchorInput_posXpath"].format(replace_sort=replace_sort)).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addSDistanceFromAnchorInput_posXpath"].format(replace_sort=replace_sort), find_after_wait_time=0.5).send_keys(distance_from_anchor)
                            if treatment == "mark":
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addMarkRadio_posXpath"].format(replace_sort=replace_sort)).click()
                            else:    # inside_element
                                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_editElement_addRemoveRadio_posXpath"].format(replace_sort=replace_sort)).click()
                    elif test_data["rule_action"] == "run_script":
                        run_scirpt_profile_data = test_data["action_parameter"]["run_script"][0]["profile_file"]
                        run_scirpt_profile_name = run_scirpt_profile_data["name"]
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_runScript_addrunScriptProfileSelectBox_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_runScript_searchrunScriptProfile_posXpath"]).clear()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_runScript_searchrunScriptProfile_posXpath"]).send_keys(run_scirpt_profile_name)
                        # 点击回车键
                        search_box = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_runScript_searchrunScriptProfile_posXpath"])
                        search_box.send_keys(Keys.RETURN)
                        # 选择第一个
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_runScript_searchrunScriptProfileDorpItem_posXpath"]).click()
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added manipulation action parameters..")
                elif test_data["policy_type"] == "statistics":
                    # 点击Statistics Template添加按钮打开Template侧滑列表
                    self.driver.find_element(By.XPATH, create_element_position["plicyRulePage_addStatisticsTemplate_posXpath"]).click()
                    # 通过Statistics Template name搜索并选中
                    profile_data = test_data["action_parameter"]["statistics_template"]
                    for template in range(len(profile_data)):
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=1).send_keys(profile_data[template]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectProfile_posXpath"].format(replaceValue=profile_data[template]["name"]), find_after_wait_time=0.5).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeProfile_posXpath"]).click()
                elif test_data["policy_type"] == "service_chaining":
                    sff_data = test_data["profile"]
                    # 点击SFF Profile添加按钮
                    self.driver.find_element(By.XPATH,create_element_position["policyRulePage_addSFFProfile_posXpath"]).click()
                    time.sleep(1)
                    #在侧滑框中搜索sff并选中
                    for sff in sff_data:
                        btn = self.driver.find_element(By.XPATH,create_element_position["policyRulePage_searchSFFProfile_posXpath"], find_after_wait_time=1)
                        self.driver.execute_script("arguments[0].click()", btn)
                        self.driver.find_element(By.XPATH,create_element_position["policyRulePage_searchSFFProfile_posXpath"]).send_keys(sff["name"])
                        self.driver.find_element(By.XPATH,create_element_position["policyRulePage_searchSFFProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        selectSFFXpath = create_element_position["policyRulePage_selectSFFProfile_posXpath"].format(replaceValue=sff["name"])
                        self.driver.find_element(By.XPATH,selectSFFXpath).click()
                        # self.driver.execute_script("arguments[0].click()", btn)
                        self.driver.find_element(By.XPATH,create_element_position["policyRulePage_closeSFFProfile_posXpath"]).click()
                elif test_data["policy_type"] == "monitor":
                    #步骤：开启vlan_button->选择select->输入name->搜索
                    if test_data["is_mirror"] == "on":
                        self.driver.find_element(By.XPATH, create_element_position[
                            "policyRulePage_mirrorTrafficButton_posXpath"]).click()
                    else:
                        pass
                    self.driver.find_element(By.XPATH,create_element_position["policyRulePage_addVLANIDButton_posXpath"]).click()
                    for flag in range(len(test_data["profile"])):
                        self.driver.find_element(By.XPATH,create_element_position["policyRulePage_firstSelectMirrorProfile_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchMirrorProfile_posXpath"], find_after_wait_time=1).send_keys(test_data["profile"][flag]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchMirrorProfile_posXpath"], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH,'//ul[@class="MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd css-1cklc3"]//li[1]//div[@class="MuiListItemButton-root MuiListItemButton-colorNeutral MuiListItemButton-variantPlain css-18mv95p"]').click()
                        self.driver.find_element(By.XPATH,'//div[@class="absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]"]/button').click()

                        # selectProfileXpath = create_element_position["policyRulePage_selectMirrorProfile_posXpath"].format(replaceValue=test_data["profile"][flag]["name"])
                        # self.driver.find_element(By.XPATH,selectProfileXpath, find_after_wait_time=0.5).click()

            # 配置DoS的Threshold和Mitigation
            if test_data["policy_type"] == "dos_protection" and test_data["rule_action"] == "protect":
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_thresholdType_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_groupBy_dropDownBox_posXpath"]).click()
                if test_data["threshold"]["type"] == "rate":
                    if test_data["threshold"]["rate_threshold"]["group_by"] == "source_ip":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP")
                    elif test_data["threshold"]["rate_threshold"]["group_by"] == "source_asn":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source ASN")
                    elif test_data["threshold"]["rate_threshold"]["group_by"] == "source_country":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source Country")
                    elif test_data["threshold"]["rate_threshold"]["group_by"] == "server_fqdn":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Server FQDN")
                    elif test_data["threshold"]["rate_threshold"]["group_by"] == "source_ip_and_destination_ip":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP and Destination IP")
                    self.driver.find_element(By.XPATH, temp_group_by_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_requestPerPeriod_posXpath"]).send_keys(test_data["threshold"]["rate_threshold"]["request_per_period"])
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_countingPeriod_dropDownBox_posXpath"]).click()
                    temp_counting_period_element_position = create_element_position["policyRulePage_countingPeriod_select_posXpath"].format(replaceValue=test_data["threshold"]["rate_threshold"]["counting_period"])
                    self.driver.find_element(By.XPATH, temp_counting_period_element_position).click()
                elif test_data["threshold"]["type"] == "concurrency":
                    if test_data["threshold"]["concurrency_threshold"]["group_by"] == "source_ip":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP")
                    elif test_data["threshold"]["concurrency_threshold"]["group_by"] == "source_asn":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source ASN")
                    elif test_data["threshold"]["rate_threshold"]["group_by"] == "source_country":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source Country")
                    elif test_data["threshold"]["rate_threshold"]["group_by"] == "server_fqdn":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Server FQDN")
                    elif test_data["threshold"]["rate_threshold"]["group_by"] == "source_ip_and_destination_ip":
                        temp_group_by_element_position = create_element_position["policyRulePage_groupBy_select_posXpath"].format(replaceValue="Source IP and Destination IP")
                    self.driver.find_element(By.XPATH, temp_group_by_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_concurrentSsessions_posXpath"]).send_keys(test_data["threshold"]["concurrency_threshold"]["concurrent_sessions"])
                #self.driver.find_element(By.ID, create_element_position["policyRulePage_mitigationBehavior_posId"]).click()
                if test_data["mitigation"]["behavior"] == "deny":
                    self.driver.find_element(By.XPATH, dosRulePage_mitigationBehavior_deny_posXpath).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_mitigationTimeouts_dropDownBox_posXpath"]).click()
                    temp_mitigation_timeout_element_position = create_element_position["policyRulePage_mitigationTimeouts_select_posXpath"].format(replaceValue=test_data["mitigation"]["timeout"])
                    self.driver.find_element(By.XPATH, temp_mitigation_timeout_element_position).click()
                elif test_data["mitigation"]["behavior"] == "none":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_mitigationBehavior_posXpath"]).click()

            # other options 操作
            if test_data["policy_type"] == "pxy_manipulation":
                # log option =》 log all
                if "log_options" in test_data:
                    if test_data["log_options"] == "all":
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_logOptions_all_posXpath"]).click()
                    elif test_data["log_options"] == "off":
                        pass
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: todo...")
                if "effective_devices" in test_data:
                    self.add_effective_devices(test_data["effective_devices"], create_element_position)

            # 点enable，不加sleep有一定几率点不上
            time.sleep(1)
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_enable_posXpath"]).click()
            # 确认创建
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_okButton_posXpath"]).click()
            #self.driver.find_element(By.XPATH, create_element_position["policyRulePage_okButton_warningYes_posXpath"]).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            #return 400, None
        
    def add_ip(self, ip_data, ip_condition_type, create_element_position):
        try:
            if ip_condition_type != "SrcIP" and ip_condition_type != "DstIP":
                # 点add condition的+
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                # 选中port
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition{}_posXpath".format(ip_condition_type)]).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点ip address的+
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_add{}_posXpath".format(ip_condition_type)]).click()
            # 通过ip name搜索并选中
            for i in range(len(ip_data)):
                #self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)]).send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)], find_after_wait_time=1).send_keys(ip_data[i]["name"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                temp_element_position = create_element_position["policyRulePage_select{}_posXpath".format(ip_condition_type)].format(replaceValue=ip_data[i]["name"])
                self.driver.find_element(By.XPATH, temp_element_position, find_after_wait_time=0.5).click()
                # self.driver.find_element(By.XPATH, create_element_position["policyRulePage_select{}_posXpath".format(ip_condition_type)]).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(ip_condition_type)]).click()
            for j in range(len(ip_data)):
                if ip_data[j]["negate"] == True:
                    time.sleep(1)  # 暂停1秒
                    negate_element = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_negate{}_posXpath".format(ip_condition_type)])
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
    
    def add_port(self, port_data, port_condition_type, create_element_position):
        try:
            # 点add condition的+
            btn = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"])
            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
            # 选中port
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition{}_posXpath".format(port_condition_type)]).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点source port的+
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_add{}_posXpath".format(port_condition_type)]).click()
            # 通过port name搜索并选中
            for z in range(len(port_data)):
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(port_condition_type)], find_after_wait_time=1).send_keys(port_data[z]["name"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(port_condition_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                temp_element_position = create_element_position["policyRulePage_select{}_posXpath".format(port_condition_type)].format(replaceValue=port_data[z]["name"])
                self.driver.find_element(By.XPATH, temp_element_position, find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(port_condition_type)]).click()
            for j in range(len(port_data)):
                if port_data[j]["negate"] == True:
                    time.sleep(1)  # 暂停1秒
                    negate_element = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_negate{}_posXpath".format(port_condition_type)])
                    ActionChains(self.driver).move_to_element(negate_element).perform()  # 悬停以使元素可见
                    negate_element.click()
        except Exception as e:
            raise

    add_subid = add_port

    def add_protocol_field(self, protocol_field_data, filed_type, create_element_position, num):
        try:
            # 强制点击add condition的+
            btn = self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"])
            self.driver.execute_script("arguments[0].click()", btn)
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点protocol filed的+
            temp_element_position = create_element_position["policyRulePage_add{}_posXpath".format(filed_type)].format(replaceValue=num)
            self.driver.find_element(By.XPATH, temp_element_position).click()
            # 通过protocol filed name搜索并选中
            for x in range(len(protocol_field_data)):
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=1).send_keys(protocol_field_data[x]["name"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_select{}_posXpath".format(filed_type)].format(replaceValue=protocol_field_data[x]["name"]), find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(filed_type)]).click()
        except Exception as e:
            raise

    def add_bool_type_protocol_field(self, protocol_field_data, filed_type, create_element_position, num):
        try:
            for x in range(len(protocol_field_data)):
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                var1 = protocol_field_data[x]["boolean_type"]
                xpath_temp = create_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]
                xpath_last = xpath_temp.format(replaceValue=var1)
                self.driver.find_element(By.XPATH, xpath_last).click()
                self.driver.find_element(By.XPATH,create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                # 点protocol filed的+
                temp_element_position = create_element_position["policyRulePage_add{}_posXpath".format(filed_type)].format(replaceValue=num)
                self.driver.find_element(By.XPATH, temp_element_position).click()
                # 通过protocol filed name搜索并选中
                self.driver.find_element(By.XPATH,create_element_position["policyRulePage_search{}_posXpath".format(filed_type)],find_after_wait_time=1).send_keys(protocol_field_data[x]["name"])
                self.driver.find_element(By.XPATH,create_element_position["policyRulePage_search{}_posXpath".format(filed_type)],find_after_wait_time=0.5).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH,create_element_position["policyRulePage_select{}_posXpath".format(filed_type)],find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(filed_type)]).click()
                num = num +1
        except Exception as e:
            raise

    def add_ip_protocol(self, ip_protocol_data, filed_type, create_element_position):
        try:
            # 点add condition的+
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
            # 选中port
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]).click()
            self.driver.find_element(By.XPATH,create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
            # 点source port的+
            self.driver.find_element(By.XPATH, create_element_position[ "policyRulePage_add{}_posXpath".format(filed_type)]).click()
            # 通过port name搜索并选中
            is_first_iteration = True
            for z in ip_protocol_data:
                #如果不是第一次循环，需要点加号调侧滑框
                if not is_first_iteration:
                    self.driver.find_element(By.XPATH, policyRulePage_little_button_addIpProtocol_posXpath).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=1).send_keys(z)
                self.driver.find_element(By.XPATH, create_element_position[ "policyRulePage_search{}_posXpath".format(filed_type)], find_after_wait_time=0.5).send_keys(Keys.ENTER)
                temp_element_position = create_element_position[ "policyRulePage_select{}_posXpath".format(filed_type)].format( replaceValue=z)
                self.driver.find_element(By.XPATH, temp_element_position, find_after_wait_time=0.5).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(filed_type)]).click()
                is_first_iteration = False
        except Exception as e:
            raise

    def add_effective_devices(self, effective_device_data, create_element_position):
        try:
            # 点击 add effective devices按钮
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addEffectiveDevices_posXpath"]).click()
            # 从侧滑中选择数据
            for i in range(len(effective_device_data)):
                replace_device = effective_device_data[i].strip()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectEffectiveDevices_posXpath"].format(replace_device=replace_device), find_after_wait_time=1).click()
            # 关闭侧滑
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeEffectiveDevices_posXpath"]).click()
        except Exception as e:
            raise




