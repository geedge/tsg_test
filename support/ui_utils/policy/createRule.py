# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.policy.pageJump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from element_position.policyElementPosition import *

class CreateRule():
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
            self.driver.find_element(By.ID, create_element_position["policyRuleListPage_createButton_posId"]).click()
            
            # 输入name
            rule_name = test_data["ruleName"]
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_inputName_posXpath"]).send_keys(rule_name)
            
            # 选择action
            if test_data["policyType"] == "security" or test_data["policyType"] == "intercept" or test_data["policyType"] == "manipulation":
                self.driver.find_element(By.ID, create_element_position["policyRulePage_selectAction_posId"]).click()
            
            # 添加ip
            if "sourceIP" in test_data["condition"] and len(test_data["condition"]["sourceIP"]) != 0:
                src_ip_data = test_data["condition"]["sourceIP"]
                self.add_ip(src_ip_data, "SrcIP", create_element_position)
            if "sourceIPGroup" in test_data["condition"] and len(test_data["condition"]["sourceIPGroup"]) != 0:
                src_ip_group_data = test_data["condition"]["sourceIPGroup"]
                self.add_ip(src_ip_group_data, "SrcIP", create_element_position)
            if "destinationIP" in test_data["condition"] and len(test_data["condition"]["destinationIP"]) != 0:
                dst_ip_data = test_data["condition"]["destinationIP"]
                self.add_ip(dst_ip_data, "DstIP", create_element_position)
            if "destinationIPGroup" in test_data["condition"] and len(test_data["condition"]["destinationIPGroup"]) != 0:
                dst_ip_group_data = test_data["condition"]["destinationIPGroup"]
                self.add_ip(dst_ip_group_data, "DstIP", create_element_position)
            if "internalIP" in test_data["condition"] and len(test_data["condition"]["internalIP"]) != 0:
                internal_ip_data = test_data["condition"]["internalIP"]
                self.add_ip(internal_ip_data, "InternalIP", create_element_position)
            if "internalIPGroup" in test_data["condition"] and len(test_data["condition"]["internalIPGroup"]) != 0:
                internal_ip_group_data = test_data["condition"]["internalIPGroup"]
                self.add_ip(internal_ip_group_data, "InternalIP", create_element_position)
            if "externalIP" in test_data["condition"] and len(test_data["condition"]["externalIP"]) != 0:
                external_ip_data = test_data["condition"]["externalIP"]
                self.add_ip(external_ip_data, "ExternalIP", create_element_position)
            if "externalIPGroup" in test_data["condition"] and len(test_data["condition"]["externalIPGroup"]) != 0:
                external_ip_group_data = test_data["condition"]["externalIPGroup"]
                self.add_ip(external_ip_group_data, "ExternalIP", create_element_position)
                
            # 添加port
            if "sourcePort" in test_data["condition"] and len(test_data["condition"]["sourcePort"]) != 0:
                src_port_data = test_data["condition"]["sourcePort"]
                self.add_port(src_port_data, "SrcPort", create_element_position)
            if "sourcePortGroup" in test_data["condition"] and len(test_data["condition"]["sourcePortGroup"]) != 0:
                src_port_group_data = test_data["condition"]["sourcePortGroup"]
                self.add_port(src_port_group_data, "SrcPort", create_element_position)
            if "destinationPort" in test_data["condition"] and len(test_data["condition"]["destinationPort"]) != 0:
                dst_port_data = test_data["condition"]["destinationPort"]    
                self.add_port(dst_port_data, "DstPort", create_element_position)
            if "destinationPortGroup" in test_data["condition"] and len(test_data["condition"]["destinationPortGroup"]) != 0:
                dst_port_group_data = test_data["condition"]["destinationPortGroup"]
                self.add_port(dst_port_group_data, "DstPort", create_element_position)
            if "internalPort" in test_data["condition"] and len(test_data["condition"]["internalPort"]) != 0:
                internal_port_data = test_data["condition"]["internalPort"]
                self.add_port(internal_port_data, "InternalPort", create_element_position)
            if "internalPortGroup" in test_data["condition"] and len(test_data["condition"]["internalPortGroup"]) != 0:
                internal_port_group_data = test_data["condition"]["internalPortGroup"]
                self.add_port(internal_port_group_data, "InternalPort", create_element_position)
            if "externalPort" in test_data["condition"] and len(test_data["condition"]["externalPort"]) != 0:
                external_port_data = test_data["condition"]["externalPort"]
                self.add_port(external_port_data, "ExternalPort", create_element_position)
            if "externalPortGroup" in test_data["condition"] and len(test_data["condition"]["externalPortGroup"]) != 0:
                external_port_group_data = test_data["condition"]["externalPortGroup"]
                self.add_port(external_port_group_data, "ExternalPort", create_element_position)
            
            # 增加quic标记位，用于判断是否存在send tcp reset勾选框
            quic_protocol_flag = False
            # 添加application
            if "application" in test_data["condition"] and len(test_data["condition"]["application"]) != 0:
                # 点application的+
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addApplication_posXpath"]).click()
                application_data = test_data["condition"]["application"]
                # 通过application name搜索并选中
                for j in range(len(application_data)):
                    if application_data[j]["name"] == "quic" and len(application_data) == 1:
                        quic_protocol_flag = True
                    if application_data[j]["objectType"] == "application":
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplicationLabel_posXpath"]).click()
                    elif application_data[j]["objectType"] == "application_group":
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplicationGroupLabel_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"]).send_keys(application_data[j]["name"])
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"]).send_keys(Keys.ENTER)
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplication_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeApplication_posXpath"]).click()
                
            # 添加server fqdn
            if "serverFqdn" in test_data["condition"] and len(test_data["condition"]["serverFqdn"]) != 0:
                server_fqdn_data = test_data["condition"]["serverFqdn"]
                for t in range(len(server_fqdn_data)):
                    if server_fqdn_data[t]["objectType"] == "fqdn":
                        # 点add condition的+
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                        # 选中server fqdn
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addConditionServerFqdn_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                        # 点server fqdn的+，因为dst ip已经是第一层且t初始值是0，所以要+2
                        temp = t + 2
                        temp_element_position = create_element_position["policyRulePage_addServerFqdn_posXpath"].format(replaceValue=temp)
                        self.driver.find_element(By.XPATH, temp_element_position).click()
                        # 通过server fqdn name搜索并选中
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchServerFqdn_posXpath"]).send_keys(server_fqdn_data[t]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchServerFqdn_posXpath"]).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectServerFqdn_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeServerFqdn_posXpath"]).click()
                    elif server_fqdn_data[x]["objectType"] == "category":
                        print("to be added...")
            
            # 添加protocol field
            protocol_field_flag = False
            if "protocolFiled" in test_data["condition"] and len(test_data["condition"]["protocolFiled"]) != 0:
                protocol_field_data = test_data["condition"]["protocolFiled"]
                # protocol_field_flag为true，表示sub action被激活，不需要点Override Application Deny Action
                protocol_field_flag = True
                for x in range(len(protocol_field_data)):
                    temp = x + 1
                    if protocol_field_data[x]["fieldType"] == "url":
                        self.add_protocol_field(protocol_field_data, "Url", create_element_position, temp)
                    elif protocol_field_data[x]["fieldType"] == "request_header":
                        self.add_protocol_field(protocol_field_data, "RequestHeader", create_element_position, temp)
                    elif protocol_field_data[x]["fieldType"] == "response_header":    
                        print("to be added...")
            
            # 添加sub action
            if "subAction" in test_data["condition"] and len(test_data["condition"]["subAction"]) != 0 and test_data["condition"]["subActionOverride"] == True:
                sub_action_data = test_data["condition"]["subAction"]
                if protocol_field_flag == False:
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_override_posXpath"]).click()
                if sub_action_data[0]["type"] == "drop":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).clear()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).send_keys(sub_action_data[0]["dropPacket"])
                    # quic不支持tcp rst；默认tcp rst是选中，不需要操作，只有当sendTcpRst为false时
                    if quic_protocol_flag == False or sub_action_data["sendTcpRst"] == False:
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_sendTcpRst_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_sendIcmp_posXpath"]).click()
                elif sub_action_data[0]["type"] == "rate_limit":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_rateLimit_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_rateLimit_rate_posXpath"]).send_keys(sub_action_data[0]["rateValue"])
                elif sub_action_data[0]["type"] == "tamper":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_tamper_posXpath"]).click()
                elif sub_action_data[0]["type"] == "block":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_block_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_block_responseContent_change_posXpath"].format(replaceValue=sub_action_data[0]["contentType"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    if sub_action_data[0]["contentType"].lower() == "text":
                        self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_block_responseContent_text_posId"]).send_keys(sub_action_data[0]["content"])
                    elif sub_action_data[0]["contentType"].lower() == "profile":
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_clickProfile_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(sub_action_data[0]["content"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                        self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_block_responseContent_selectProfile_posId"]).click()
                elif sub_action_data[0]["type"] == "redirect":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_redirect_posXpath"]).clear()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
                elif sub_action_data[0]["type"] == "alert":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_alert_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_alert_responseContent_change_posXpath"].format(replaceValue=sub_action_data[0]["contentType"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                    if sub_action_data[0]["contentType"].lower() == "text":
                        self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_alert_responseContent_text_posId"]).send_keys(sub_action_data[0]["content"])
                    elif sub_action_data[0]["contentType"].lower() == "profile":
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_clickProfile_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(sub_action_data[0]["content"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                        self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_alert_responseContent_selectProfile_posId"]).click()
            
            # 添加packet capture
            if "packetCapture" in test_data["condition"] and len(test_data["condition"]["packetCapture"]) != 0 and test_data["condition"]["packetCapture"][0]["enable"] == True:
                packet_capture_data = test_data["condition"]["packetCapture"]
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_depth_posXpath"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_depth_posXpath"]).send_keys(packet_capture_data[0]["captureDepth"])
           
            # 添加shaping的priority和fair factor
            if test_data["policyType"] == "shaping":
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_priority_posId"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_priority_posId"]).send_keys(test_data["rulePriority"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_fairFactor_posId"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_fairFactor_posId"]).send_keys(test_data["ruleFairFactor"])
            
            # 添加statistics、shaping、sc的profile
            if "profile" in test_data and len(test_data["profile"]) != 0:
                profile_data = test_data["profile"]
                if test_data["policyType"] == "shaping":
                    # 点profile的+
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_posXpath"]).click()
                    # 通过profile name搜索并选中
                    profile_data = test_data["profile"]
                    for y in range(len(profile_data)):
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(profile_data[y]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectProfile_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeProfile_posXpath"]).click()
                        if test_data["multiProfile"] == True and y != len(profile_data) - 1:
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_plus_posXpath"]).click()
                elif test_data["policyType"] == "statistics":
                    print("to be added...")
                elif test_data["policyType"] == "service_Chaining":
                    print("to be added...")
                
            # 点enable
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_enable_posXpath"]).click()
            
            # 确认创建
            self.driver.find_element(By.ID, create_element_position["policyRulePage_okButton_yes_posId"]).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_okButton_warningYes_posXpath"]).click()
            
            return 200
        except:
            return 400  
        
    def add_ip(self, ip_data, ip_condition_type, create_element_position):
        if ip_condition_type != "SrcIP":
            # 点add condition的+
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
            # 选中port
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition{}_posXpath".format(ip_condition_type)]).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
        # 点ip address的+
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_add{}_posXpath".format(ip_condition_type)]).click()
        # 通过ip name搜索并选中
        for i in range(len(ip_data)):
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)]).send_keys(ip_data[i]["name"])
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(ip_condition_type)]).send_keys(Keys.ENTER)
            temp_element_position = create_element_position["policyRulePage_select{}_posXpath".format(ip_condition_type)].format(replaceValue=ip_data[i]["name"])
            self.driver.find_element(By.XPATH, temp_element_position).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(ip_condition_type)]).click()
    
    def add_port(self, port_data, port_condition_type, create_element_position):
        # 点add condition的+
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
        # 选中port
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition{}_posXpath".format(port_condition_type)]).click()
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
        # 点source port的+
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_add{}_posXpath".format(port_condition_type)]).click()
        # 通过port name搜索并选中
        for z in range(len(port_data)):
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(port_condition_type)]).send_keys(port_data[z]["name"])
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(port_condition_type)]).send_keys(Keys.ENTER)
            temp_element_position = create_element_position["policyRulePage_select{}_posXpath".format(port_condition_type)].format(replaceValue=port_data[z]["name"])
            self.driver.find_element(By.XPATH, temp_element_position).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(port_condition_type)]).click()
            
    def add_protocol_field(self, protocol_field_data, filed_type, create_element_position, num):
        # 点add condition的+
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
        # 选中protocol filed
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition{}_posXpath".format(filed_type)]).click()
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
        # 点protocol filed的+
        temp_element_position = create_element_position["policyRulePage_add{}_posXpath".format(filed_type)].format(replaceValue=num)
        self.driver.find_element(By.XPATH, temp_element_position).click()
        # 通过protocol filed name搜索并选中
        for x in range(len(protocol_field_data)):
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(filed_type)]).send_keys(protocol_field_data[x]["name"])
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_search{}_posXpath".format(filed_type)]).send_keys(Keys.ENTER)
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_select{}_posXpath".format(filed_type)]).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_close{}_posXpath".format(filed_type)]).click()