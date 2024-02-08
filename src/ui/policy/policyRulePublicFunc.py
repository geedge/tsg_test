import os
import sys
import time
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from element_position.policyElementPosition import *
from workpath import workdir

class PolicyRulePublicFunc():
    def __init__(self, driver):
        self.workdir = workdir
        self.driver = driver
        
    def _create(self, test_data, rule_element_position):
        page_jump_element_position = rule_element_position["page_jump"]
        create_element_position = rule_element_position["create"]
        # 页面跳转
        self._goto_subPolicyPage(page_jump_element_position)
        # 点击create
        self.driver.find_element(By.ID, create_element_position["policyRuleListPage_createButton_posId"]).click()
        # 输入name
        rule_name = test_data["ruleName"]
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_inputName_posXpath"]).send_keys(rule_name)
        # 选择action
        if test_data["policyType"] == "security" or test_data["policyType"] == "intercept" or test_data["policyType"] == "manipulation":
            self.driver.find_element(By.ID, create_element_position["policyRulePage_selectAction_posId"]).click()
        # 添加ip
        ip_data = test_data["condition"]["ip"]
        if len(ip_data) != 0:
            # 点source ip address的+
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addSrcIP_posXpath"]).click()
            # 通过ip name搜索并选中
            for i in range(len(ip_data)):
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchSrcIP_posXpath"]).send_keys(ip_data[i]["name"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchSrcIP_posXpath"]).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectSrcIP_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeSrcIP_posXpath"]).click()
        # 添加application
        application_data = test_data["condition"]["application"]
        # 增加quic标记位，用于判断是否存在send tcp reset框
        quic_protoco_flag = False
        if len(application_data) != 0:
            # 点application的+
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addApplication_posXpath"]).click()
            # 通过application name搜索并选中
            for j in range(len(application_data)):
                if application_data[j]["name"] == "quic" and len(application_data) == 1:
                    quic_protoco_flag = True
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"]).send_keys(application_data[j]["name"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchApplication_posXpath"]).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectApplication_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeApplication_posXpath"]).click()
        # 添加server fqdn
        server_fqdn_data = test_data["condition"]["serverFqdn"]
        if len(server_fqdn_data) != 0:
            for t in range(len(server_fqdn_data)):
                if server_fqdn_data[t]["type"] == "fqdn":
                    # 点add condition的+
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                    # 选中server fqdn
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_serverFqdn_posXpath"]).click()
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
                elif server_fqdn_data[x]["type"] == "category":   
                    print("to be added...")       
        # 添加protocol filed
        protocol_filed_data = test_data["condition"]["protocolFiled"]
        protocol_filed_flag = False
        if len(protocol_filed_data) != 0:
            # protocol_filed_flag为true，表示sub action被激活，不需要点Override Application Deny Action
            protocol_filed_flag = True
            for x in range(len(protocol_filed_data)):
                temp = x + 1
                if protocol_filed_data[x]["type"] == "url":
                    # 点add condition的+
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_posXpath"]).click()
                    # 选中url
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_url_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addCondition_close_posXpath"]).click()
                    # 点url的+，
                    temp_element_position = create_element_position["policyRulePage_addUrl_posXpath"].format(replaceValue=temp)
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    # 通过url name搜索并选中
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchUrl_posXpath"]).send_keys(protocol_filed_data[t]["name"])
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchUrl_posXpath"]).send_keys(Keys.ENTER)
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectUrl_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_closeUrl_posXpath"]).click()
                elif protocol_filed_data[x]["type"] == "request_header":
                    print("to be added...")
        # 添加sub action
        sub_action_data = test_data["condition"]["subAction"]
        if len(sub_action_data) != 0 and test_data["condition"]["subActionOverride"] == True:
            if protocol_filed_flag == False:
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_override_posXpath"]).click()
            if sub_action_data[0]["type"] == "drop":
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).clear()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_drop_dropPkt_posXpath"]).send_keys(sub_action_data[0]["dropPacket"])
                # quic不支持tcp rst；默认tcp rst是选中，不需要操作，只有当sendTcpRst为false时
                if quic_protoco_flag == False or sub_action_data["sendTcpRst"] == False:
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
                dropdown_item_posXpath = create_element_position["policyRulePage_subAction_block_responseCode_change_posXpath"].format(replaceName=sub_action_data[0]["code"])
                self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_block_responseContent_posXpath"]).click()
                dropdown_item_posXpath = create_element_position["policyRulePage_subAction_block_responseContent_change_posXpath"].format(replaceName=sub_action_data[0]["contentType"])
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
                dropdown_item_posXpath = create_element_position["policyRulePage_subAction_alert_responseCode_change_posXpath"].format(replaceName=sub_action_data[0]["code"])
                self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_posXpath"]).click()
                dropdown_item_posXpath = create_element_position["policyRulePage_subAction_alert_responseContent_change_posXpath"].format(replaceName=sub_action_data[0]["contentType"])
                self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()
                if sub_action_data[0]["contentType"].lower() == "text":
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_alert_responseContent_text_posId"]).send_keys(sub_action_data[0]["content"])
                elif sub_action_data[0]["contentType"].lower() == "profile":
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_clickProfile_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(sub_action_data[0]["content"])
                    self.driver.find_element(By.XPATH, create_element_position["policyRulePage_subAction_alert_responseContent_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                    self.driver.find_element(By.ID, create_element_position["policyRulePage_subAction_alert_responseContent_selectProfile_posId"]).click()
        # 添加packet capture
        packet_capture_data = test_data["condition"]["packetCapture"]
        if len(packet_capture_data) != 0 and packet_capture_data[0]["enable"] == True:
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
        profile_data = test_data["profile"]
        if len(profile_data) != 0:
            # 点profile的+
            self.driver.find_element(By.XPATH, create_element_position["policyRulePage_addProfile_posXpath"]).click()
            # 通过profile name搜索并选中
            profile_data = test_data["profile"]
            for y in range(len(profile_data)):
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(profile_data[y]["name"])
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_searchProfile_posXpath"]).send_keys(Keys.ENTER)
                self.driver.find_element(By.XPATH, create_element_position["policyRulePage_selectProfile_posXpath"]).click()
        # 点enable
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_enable_posXpath"]).click()
        # 确认创建
        self.driver.find_element(By.ID, create_element_position["policyRulePage_okButton_yes_posId"]).click()
        self.driver.find_element(By.XPATH, create_element_position["policyRulePage_okButton_warningYes_posXpath"]).click()
        return 200
    
    def _search(self, type, name, rule_element_position, vsys_name=""):
        search_element_position = rule_element_position["search"]
        page_jump_element_position = rule_element_position["page_jump"]
        # 打开该列表
        self._goto_subPolicyPage(page_jump_element_position)
        # 点击search查询框
        self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_posId"]).click()
        dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLable_dropDown_item_posXpath"].format(replaceName="Name")
        self.driver.find_element(By.XPATH, dropdown_item_posXpath).click()    # 点击下拉item
        input_item_posXpath = search_element_position["policyRuleListPage_searchLable_input_itemContent_posXpath"].format(replaceName="Name")
        self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)       # 输入查询值
        self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLable_searchButton_posId"]).click()
        element_tr = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "tr")
        if len(row) != 0 and type != "security":
            first_row = row[0]
            self.first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='el-checkbox__input']")
    
    def _delete(self, rule_element_position, is_del_all):
        delete_element_position = rule_element_position["delete"]
        if is_del_all == True:
            self.driver.find_element(By.XPATH, delete_element_position["policyRuleListPage_allSelect_posXpath"]).click()    # 点击all按钮
        else:
            # 点击勾选第一行选择框
            self.first_row_checkBox_element.click()     # 变量来自查询函数
        self.delete(delete_element_position["policyRuleListPage_deleteButton_posId"], delete_element_position["policyRuleListPage_okButton_warningYes_posXpath"], delete_element_position["policyRuleListPage_okButton_warningNo_posXpath"])
    
    def _goto_subPolicyPage(self, page_jump_element_position, vsys_name=""):
        # 菜单操作
        self.driver.find_element(By.CSS_SELECTOR, page_jump_element_position["mainPage_navigationBar_logo_posCss"]).click()
        self.change_vsys(vsys_name=vsys_name)
        self.driver.find_element(By.ID, page_jump_element_position["mainPage_policyFirstLevelMenu_posId"]).click()
        self.driver.find_element(By.ID, page_jump_element_position["mainPage_policySecondLevelMenu_posId"]).click()
        
    def change_vsys(self, vsys_name=""):
        current_vsys_name = self.driver.find_element(By.XPATH, mainPage_currentPage_vsysName_posXpath).text.strip().lower()
        if vsys_name.lower() == current_vsys_name:
            print(f"the current vsys: {current_vsys_name}")
            return 0
        else:    # 空为切换默认   剩下为指定切换
            if vsys_name == "":     # 空，切换到默认vsys
                change_vsys_name = "UIAutoTestVsys"
                if change_vsys_name.lower() == current_vsys_name:    # 如果默认系统和当前一直，也不用点击
                    print(f"the current vsys: {current_vsys_name}")
                    return 0
            else:     # 切换到指定vsys
                change_vsys_name = vsys_name
            print(f"the current vsys: {current_vsys_name}, switch to vsys: {change_vsys_name}")
            self.driver.find_element(By.CSS_SELECTOR, mainPage_button_menu_posXCss).click()     # 点击vsys menu
            vsys_tree_name_list = self.driver.find_elements(By.XPATH, mainPage_vsysTree_vsysName_posXpath)
            flag_num = 0
            for el_vsys_item in vsys_tree_name_list:
                vsys_item_name = el_vsys_item.text.strip().lower()
                if vsys_item_name == change_vsys_name.lower():
                    flag_num = 1
                    el_vsys_item.click()
                    break
            if flag_num == 0:
                print(f"no vsys: {change_vsys_name}")
                raise ValueError(f"no vsys: {change_vsys_name}")
    
    def delete(self, policyRuleListPage_deleteButton_posId, policyRuleListPage_okButton_warningYes_posXpath, policyRuleListPage_okButton_warningNo_posXpath):
        self.driver.find_element(By.ID, policyRuleListPage_deleteButton_posId).click()  # 点击删除按钮
        random_yes_or_no = random.randint(0, 1)
        if random_yes_or_no == 0:  # 点击yes，删除
            self.driver.find_element(By.XPATH, policyRuleListPage_okButton_warningYes_posXpath).click()  # 直接删除
        else:
            # self.driver.find_element(By.CSS_SELECTOR, policyRuleListPage_okButton_warningNo_posXpath).click()  # 先取消，再删除
            # self.driver.find_element(By.ID, policyRuleListPage_deleteButton_posId).click()  # 点击删除按钮
            self.driver.find_element(By.XPATH, policyRuleListPage_okButton_warningYes_posXpath).click()  # 点击yes，删除
        time.sleep(0.5)