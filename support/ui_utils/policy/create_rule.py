# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
from support.ui_utils.policy.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
import traceback

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
            time.sleep(5)
            self.driver.find_element(By.ID, create_element_position["policyRuleListPage_createButton_posId"]).click()
            
            # 输入name
            rule_name = test_data["rule_name"]
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_inputName_posXpath"]).send_keys(rule_name)
            
            # 选择action
            if test_data["policy_type"] == "security" or test_data["policy_type"] == "intercept":
                self.driver.find_element(By.ID, create_element_position["policyRulePage_selectAction_posId"]).click()
            # 选择target traffic 
            elif test_data["policy_type"] == "service_chaining" and test_data["targeted_traffic"] == "decrypted":
                self.driver.find_element(By.XPATH,create_element_position["policyRulePage_chooseTargetedTraffic_posXpath"]).click()
            elif test_data["policy_type"] == "manipulation":
                if test_data["rule_action"] == "allow":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectAllow_posId"]).click()
                elif test_data["rule_action"] == "deny":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectDeny_posId"]).click()
                elif test_data["rule_action"] == "monitor":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectMonitor_posId"]).click()
                elif test_data["rule_action"] == "redirect":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectRedirect_posId"]).click()
                elif test_data["rule_action"] == "replace":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectReplace_posId"]).click()
                elif test_data["rule_action"] == "hijack":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectHijack_posId"]).click()
                elif test_data["rule_action"] == "insert":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectInsert_posId"]).click()
                elif test_data["rule_action"] == "edit_element":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectEditElement_posId"]).click()
                else:   # run script
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_selectRunScript_posId"]).click()
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

            # 添加application
            if "application" in test_data["condition"] and len(test_data["condition"]["application"]) != 0:
                # 点application的+
                if test_data["policy_type"] == "manipulation":
                    if  test_data["condition"]["application"][0]["name"].lower == "doh":  # doh需要操作application
                        pass
                    else:   # 非doh不需要操作application
                        pass
                else:
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addApplication_posXpath"]).click()
                    application_data = test_data["condition"]["application"]
                    # 通过application name搜索并选中
                    if len(application_data) == 1:
                        override_flag = True
                    for j in range(len(application_data)):
                        if application_data[j]["object_type"] == "application":
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplicationLabel_posXpath"]).click()
                        elif application_data[j]["object_type"] == "application_group":
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplicationGroupLabel_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"]).send_keys(application_data[j]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"]).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplication_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeApplication_posXpath"]).click()
                
            # 添加server fqdn
            if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
                server_fqdn_data = test_data["condition"]["server_fqdn"]
                for t in range(len(server_fqdn_data)):
                    if server_fqdn_data[t]["object_type"] == "fqdn":
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
                        time.sleep(5)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectServerFqdn_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeServerFqdn_posXpath"]).click()
                    elif server_fqdn_data[t]["object_type"] == "category":
                        print("to be added...")
            
            # 添加protocol field
            if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
                protocol_field_data = test_data["condition"]["protocol_filed"]
                for x in range(len(protocol_field_data)):
                    temp = x + 1
                    if protocol_field_data[x]["field_type"] == "url":
                        self.add_protocol_field(protocol_field_data, "Url", create_element_position, temp)
                    elif protocol_field_data[x]["field_type"] == "request_header":
                        self.add_protocol_field(protocol_field_data, "RequestHeader", create_element_position, temp)
                    elif protocol_field_data[x]["field_type"] == "response_header":    
                        print("to be added...")
            
            if "application" in test_data["condition"] and len(test_data["condition"]["application"]) != 0 and "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) == 0:
                override_flag = True
            else:
                override_flag = False
            
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
                    if override_flag == False or sub_action_data[0]["send_tcp_rst"] == False:
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_sendTcpRst_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_sendIcmp_posXpath"]).click()
                elif sub_action_data[0]["type"] == "rate_limit":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_rateLimit_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_rateLimit_rate_posXpath"]).send_keys(sub_action_data[0]["rate_value"])
                elif sub_action_data[0]["type"] == "tamper":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_tamper_posXpath"]).click()
                elif sub_action_data[0]["type"] == "block":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_block_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
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
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_redirect_posXpath"]).clear()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_redirect_posXpath"]).click()
                elif sub_action_data[0]["type"] == "alert":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseCode_posXpath"]).click()
                    dropdown_item_posXpath = create_element_position["policyRulePage_subAction_alert_responseCode_change_posXpath"].format(replaceValue=sub_action_data[0]["code"])
                    self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
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
            
            # 添加packet capture
            if "packet_capture" in test_data["condition"] and len(test_data["condition"]["packet_capture"]) != 0 and test_data["condition"]["packet_capture"][0]["enable"] == True:
                packet_capture_data = test_data["condition"]["packet_capture"]
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_depth_posXpath"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_packetCapture_depth_posXpath"]).send_keys(packet_capture_data[0]["capture_depth"])
           
            # 添加shaping的priority和fair factor
            if test_data["policy_type"] == "shaping":
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_priority_posId"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_priority_posId"]).send_keys(test_data["rulePriority"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_fairFactor_posId"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_fairFactor_posId"]).send_keys(test_data["ruleFairFactor"])
            
            # 添加statistics、shaping、sc的profile
            if "action_parameter" in test_data and len(test_data["action_parameter"]) != 0:
                profile_data = test_data["action_parameter"]
                if test_data["policy_type"] == "shaping":
                    # 点profile的+
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_posXpath"]).click()
                    # 通过profile name搜索并选中
                    profile_data = test_data["action_parameter"]
                    for y in range(len(profile_data)):
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(profile_data[y]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectProfile_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeProfile_posXpath"]).click()
                        if test_data["multiProfile"] == True and y != len(profile_data) - 1:
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_plus_posXpath"]).click()
                elif test_data["policy_type"] == "manipulation":
                    print(212)
                    if test_data["rule_action"] == "deny":
                        # 选择 response code
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
                        #
                    elif test_data["rule_action"] == "redirect":
                        print(343)
                        print(test_data["condition"]["application"][0]["name"].lower().strip())
                        if test_data["condition"]["application"][0]["name"].lower().strip() == "http":
                            response_code = test_data["action_parameter"]["redirect_url"][0]["response_code"]
                            response_code_drop_position = create_element_position["policyRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath"].format(replace_code=response_code)
                            redirect_url = test_data["action_parameter"]["redirect_url"][0]["redirect_url"]
                            # 操作 action parameter
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectHttp_addResponseCodeSelectBox_posXpath"]).click()
                            time.sleep(1)
                            btn = self.driver.find_element(By.XPATH, response_code_drop_position)
                            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
                            time.sleep(1)
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).clear()
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath"]).send_keys(redirect_url)
                        else:
                            print("doh...")
                    else:
                        print("to be added...")
                elif test_data["policy_type"] == "statistics":
                    # 点击Statistics Template添加按钮打开Template侧滑列表
                    self.driver.find_element(By.XPATH, create_element_position["plicyRulePage_addStatisticsTemplate_posXpath"]).click()
                    # 通过Statistics Template name搜索并选中
                    profile_data = test_data["profile"]["statistics_template"]
                    for template in range(len(profile_data)):
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(profile_data[y]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectProfile_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeProfile_posXpath"]).click()
                        if test_data["multiProfile"] == True and y != len(profile_data) - 1:
                            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_plus_posXpath"]).click()
                elif test_data["policy_type"] == "service_chaining":
                    sff_data = test_data["profile"]
                    # 点击SFF Profile添加按钮
                    self.driver.find_element(By.ID,create_element_position["policyRulePage_addSFFProfile_posId"]).click()
                    #在侧滑框中搜索sff并选中
                    for sff in sff_data:
                        self.driver.find_element(By.XPATH,create_element_position["policyRulePage_searchSFFProfile_posXpath"]).send_keys(sff["name"])
                        self.driver.find_element(By.XPATH,create_element_position["policyRulePage_searchSFFProfile_posXpath"]).send_keys(Keys.ENTER)
                        selectSFFXpath = create_element_position["policyRulePage_selectSFFProfile_posXpath"].format(replaceValue=sff["name"])
                        self.driver.find_element(By.XPATH,selectSFFXpath).click()
                        self.driver.find_element(By.XPATH,create_element_position["policyRulePage_closeSFFProfile_posXpath"]).click()
                
            # 点enable
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_enable_posXpath"]).click()
            
            # 确认创建
            self.driver.find_element(By.ID, create_element_position["policyRulePage_okButton_yes_posId"]).click()
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_okButton_warningYes_posXpath"]).click()
            
            return 200
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 400, None
        
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