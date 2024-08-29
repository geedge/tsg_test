# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.profile.create_profile import CreateProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.policy.edit_rule import EditRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.packet_generator.verification import Verification
from support.api_utils.create_policy import CreatePolicy
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import DeletePolicy
import support.ui_utils.env
# from support.common.report import *
from datetime import datetime
from support.instance_utils.data_translation import DataTranslation
from support.ui_utils.element_position.map_element_position_library import *

class SecurityGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        result = self._run(self.test_data, self.parameter)
        return result

    def _run(self, test_data, parameter):
        # 参数初始化
        ui_result, api_result= "", ""
        self.api_name_list, self.ui_name_list = [], []
        result = {
            "ui_result": "",
            "api_result": ""
        }
        
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token
        
        need_initialization = False
        if len(parameter["script_type"]) == 0:
            need_initialization = True
        
        if parameter["script_type"] == "ui" or need_initialization == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)
            
            parameter["script_type"] = "ui"
            
            # 环境初始化
            support.ui_utils.env.initiate_selenium_request()
            driver = support.ui_utils.env.my_driver()
            support.ui_utils.env.setup()

            # name_list汇总
            self.ui_name_list = [
                {
                    "type": test_data["policy_type"],
                    "name": test_data["rule_name"]
                },
                {
                    "type": test_data["condition"]["source_ip"][0]['object_type'],
                    "name": test_data["condition"]["source_ip"][0]['name']
                },
                {
                    "type": test_data["condition"]["server_fqdn"][0]['object_type'],
                    "name": test_data["condition"]["server_fqdn"][0]['name']
                }
            ]
            
            # 添加定位库集合
            test_rule_element_position = {}
            if test_data["policy_type"] == "security":
                test_ip_object_element_position = {
                    "page_jump":{
                        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                        "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                        "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_ipAddress_posId
                    },
                    "create": {
                        "objectListPage_createButton_posId": ipObjectListPage_createButton_posId,
                        "objectListPage_dropDown_createButton_posId": ipObjectListPage_dropDown_createButton_posId,
                        "objectPage_inputName_posXpath": ipObjectPage_inputName_posXpath,
                        "objectPage_ipType_posId": ipObjectPage_ipType_posId,
                        "objectPage_addItem_posId": ipObjectPage_addItem_posId,
                        "objectPage_inputItem_posXpath": ipObjectPage_inputItem_posXpath,
                        "objectPage_button_saveItem_posXpath": ipObjectPage_button_saveItem_posXpath,
                        "objectPage_okButton_posId": ipObjectPage_okButton_posId,
                        "objectPage_okButton_warningYes_posXpath": ipObjectPage_okButton_warningYes_posXpath
                    },
                    "search": {
                        "objectListPage_searchLabel_posId": ipObjectListPage_searchLabel_posId,
                        "objectListPage_searchLabel_selectName_posXpath": ipObjectListPage_searchLabel_selectName_posXpath,
                        "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
                    },
                    "delete": {
                        "objectListPage_allSelect_posXpath": ipObjectListPage_allSelect_posXpath,
                        "objectListPage_deleteButton_posId": ipObjectListPage_deleteButton_posId,
                        "objectListPage_deleteButton_warningYes_posXpath": ipObjectListPage_deleteButton_warningYes_posXpath
                    }
                }
                test_fqdn_object_element_position = {
                    "page_jump":{
                        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                        "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                        "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_fqdn_posId
                    },
                    "create": {
                        "objectListPage_createButton_posId": fqdnObjectListPage_createButton_posId,
                        "objectListPage_dropDown_createButton_posId": fqdnObjectListPage_dropDown_createButton_posId,
                        "objectPage_inputName_posXpath": fqdnObjectPage_inputName_posXpath,
                        "objectPage_addItem_posId": fqdnObjectPage_addItem_posId,
                        "objectPage_inputItem_posXpath": fqdnObjectPage_inputItem_posXpath,
                        "objectPage_button_saveItem_posXpath": fqdnObjectPage_button_saveItem_posXpath,
                        "objectPage_okButton_posId": fqdnObjectPage_okButton_posId,
                        "objectPage_okButton_warningYes_posXpath": fqdnObjectPage_okButton_warningYes_posXpath
                    },
                    "search": {
                        "objectListPage_searchLabel_posId": fqdnObjectListPage_searchLabel_posId,
                        "objectListPage_searchLabel_selectName_posXpath": fqdnObjectListPage_searchLabel_selectName_posXpath,
                        "objectListPage_tableTbody_posXpath": fqdnObjectListPage_tableTbody_posXpath
                    },
                    "delete": {
                        "objectListPage_allSelect_posXpath": fqdnObjectListPage_allSelect_posXpath,
                        "objectListPage_deleteButton_posId": fqdnObjectListPage_deleteButton_posId,
                        "objectListPage_deleteButton_warningYes_posXpath": fqdnObjectListPage_deleteButton_warningYes_posXpath
                    }
                }
                test_rule_element_position = {
                    "page_jump":{
                        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                        "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                        "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_security_posId
                    },
                    "create": {
                        "policyRuleListPage_createButton_posId": securityRuleListPage_createButton_posId,
                        "policyRulePage_inputName_posXpath": securityRulePage_inputName_posXpath,
                        "policyRulePage_selectAction_posId": securityRulePage_selectDeny_posId,
                        # srcip
                        "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                        "policyRulePage_searchSrcIP_posXpath": securityRulePage_searchSrcIP_posXpath,
                        "policyRulePage_selectSrcIP_posXpath": securityRulePage_selectSrcIP_posXpath,
                        "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
                        "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                        "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                        "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                        "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                        "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                        "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                        "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                        # fqdn
                        "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                        "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                        "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                        "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                        "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
                        # url
                        "policyRulePage_addConditionUrl_posXpath": securityRulePage_addCondition_url_posXpath,
                        "policyRulePage_addUrl_posXpath": policyRulePage_addUrl_posXpath,
                        "policyRulePage_searchUrl_posXpath": policyRulePage_searchUrl_posXpath,
                        "policyRulePage_selectUrl_posXpath": policyRulePage_selectUrl_posXpath,
                        "policyRulePage_closeUrl_posXpath": policyRulePage_closeUrl_posXpath,
                        # req header
                        "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
                        "policyRulePage_addRequestHeader_posXpath": manipulationRulePage_addRequestHeader_posXpath,
                        "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
                        "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
                        "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
                        "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                        "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                        # block动作
                        "policyRulePage_subAction_block_posXpath": securityRulePage_subAction_block_posXpath,
                        "policyRulePage_subAction_block_responseCode_posXpath": securityRulePage_subAction_block_responseCode_posXpath,
                        "policyRulePage_subAction_block_responseCode_change_posXpath": securityRulePage_subAction_block_responseCode_change_posXpath,
                        "policyRulePage_subAction_block_responseContent_posXpath": securityRulePage_subAction_block_responseContent_posXpath,
                        "policyRulePage_subAction_block_responseContent_change_posXpath": securityRulePage_subAction_block_responseContent_change_posXpath,
                        "policyRulePage_subAction_block_responseContent_clickProfile_posXpath": securityRulePage_subAction_block_responseContent_clickProfile_posXpath,
                        "policyRulePage_subAction_block_responseContent_searchProfile_posXpath": securityRulePage_subAction_block_responseContent_searchProfile_posXpath,
                        "policyRulePage_subAction_block_responseContent_selectProfile_posId": securityRulePage_subAction_block_responseContent_selectProfile_posId,
                        "policyRulePage_subAction_alert_posXpath": securityRulePage_subAction_alert_posXpath,
                        "policyRulePage_subAction_alert_responseCode_posXpath": securityRulePage_subAction_alert_responseCode_posXpath,
                        "policyRulePage_subAction_alert_responseCode_change_posXpath": securityRulePage_subAction_alert_responseCode_change_posXpath,
                        "policyRulePage_subAction_alert_responseContent_posXpath": securityRulePage_subAction_alert_responseContent_posXpath,
                        "policyRulePage_subAction_alert_responseContent_change_posXpath": securityRulePage_subAction_alert_responseContent_change_posXpath,
                        "policyRulePage_subAction_alert_responseContent_clickProfile_posXpath": securityRulePage_subAction_alert_responseContent_clickProfile_posXpath,
                        "policyRulePage_subAction_alert_responseContent_searchProfile_posXpath": securityRulePage_subAction_alert_responseContent_searchProfile_posXpath,
                        "policyRulePage_subAction_alert_responseContent_selectProfile_posId": securityRulePage_subAction_alert_responseContent_selectProfile_posId,
                        "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                        "policyRulePage_okButton_yes_posId": securityRulePage_okButton_yes_posId,
                        "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath
                    },
                    "search": {
                        "policyRuleListPage_searchLable_posId": securityRuleListPage_searchLable_posId,
                        "policyRuleListPage_searchLable_dropDown_item_posXpath": securityRuleListPage_searchLable_dropDown_item_posXpath,
                        "policyRuleListPage_searchLable_input_itemContent_posXpath": securityRuleListPage_searchLable_input_itemContent_posXpath,
                        "policyRuleListPage_searchLable_searchButton_posId": securityRuleListPage_searchLable_searchButton_posId,
                        "policyRuleListPage_tableTbody_posXpath": securityRuleListPage_tableTbody_posXpath
                    },
                    "delete": {
                        "policyRuleListPage_allSelect_posXpath": securityRulelistPage_allSelect_posXpath,
                        "policyRuleListPage_deleteButton_posId": securityRuleListPage_deleteButton_posId,
                        "policyRuleListPage_okButton_warningYes_posXpath": securityRuleListpage_okButton_warningYes_posXpath,
                        "policyRuleListPage_okButton_warningNo_posXpath":securityRuleListpage_okButton_warningNo_posXpath
                    }
                }
            
            
            # 创建object
            if "source_ip" in test_data["condition"] and len(test_data["condition"]["source_ip"]) != 0:
                ip_data = test_data["condition"]["source_ip"]
                create_ip = CreateObject(driver)
                for i in range(len(ip_data)):
                    create_ip_code = create_ip.create(ip_data[i], test_ip_object_element_position)
                    if create_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create ip object successfully.", flush=True)
                    elif create_ip_code != 200:
                        ui_result = "Fail to create ip."
                        break
            if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
                fqdn_data = test_data["condition"]["server_fqdn"]
                create_fqdn = CreateObject(driver)
                for i in range(len(fqdn_data)):
                    create_fqdn_code = create_fqdn.create(fqdn_data[i], test_fqdn_object_element_position)
                    if create_fqdn_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create fqdn object successfully.", flush=True)
                    elif create_fqdn_code != 200:
                        result = "Fail to create fqdn."
                        break
            if "action_parameter" in test_data.keys():
                for prfi_key, prfi_value in(test_data["action_parameter"]).items():
                    prfi_status = 0
                    prfi_key_out = prfi_key.replace("_", " ")
                    if len(prfi_value) != 0:   # 需要创建profile数据
                        prfi_data = prfi_value
                        prfi = CreateProfile(driver)
                        for i in range(len(prfi_data)): # 遍历创建所有 profile
                            element_position_map = get_element_position(prfi_key)
                            prfi_code = prfi.create(prfi_data[i], element_position_map)
                            if prfi_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(prfi_key_out), flush=True)
                            else:
                                result = "Fail to create {} profile.".format(prfi_key_out)
                                prfi_status = 1
                                break
                    if prfi_status == 1:  # 创建失败，退出遍历创建
                        break
            # 创建rule
            if create_ip_code == 200:
                create_rule = CreateRule(driver)
                create_rule_code = create_rule.create(test_data, test_rule_element_position)
                if create_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create security rule successfully.", flush=True)
                elif create_rule_code != 200:
                    ui_result = "Fail to create security rule."

            

            # 触发流量验证
            if create_rule_code == 200:
                search_rule = SearchRule(driver)
                search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
                if search_rule_code == 200:
                    # rule_id = search_rule.get_rule_id()
                    test_data["rule_id"] = rule_id
                    verify = Verification()
                    verification_result = verify.verification(driver, parameter, test_data, [], test_rule_element_position)
                    if len(verification_result) == 4:
                        driver = verification_result[3]
                    elif len(verification_result) == 5:
                        driver = verification_result[4]
            
            # 分析验证结果，并返回给flask
            if len(verification_result) != 0:
                analysis = AnalysisResult()
                ui_result = analysis.analysis_result(test_data, [], verification_result)
            
            # 删除rule
            if create_rule_code == 200:
                search_rule = SearchRule(driver)
                search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
                if search_rule_code == 200:
                    delete_rule = DeleteRule(driver)
                    delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
                    if delete_rule_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete security rule successfully.", flush=True)
                    elif delete_rule_code != 200:
                        ui_result = ui_result + " In addition, fail to delete security rule."
                else:
                    ui_result = ui_result + " In addition, fail to search security rule."
            
            # 删除profile
            if delete_rule_code == 200 and "action_parameter" in test_data.keys():
                # 删除
                for prfi_key, prfi_value in (test_data["action_parameter"].items()):  # 遍历所有cond数据
                    if prfi_key in manipulation_profile_no_create_list:
                        continue  # 直接跳过
                    prfi_status = 0
                    prfi_key_out = prfi_key.replace("_", " ")
                    if len(prfi_value) != 0:  # 不为空
                        for i in range(len(prfi_value)):  # 遍历查询所有profile
                            search_prfi = SearchProfile(driver)
                            element_position_map = get_element_position(prfi_key)
                            prfi_name = prfi_value[i]["profile_file"]["name"].strip()
                            search_prfi_code, first_row_checkbox_element = search_prfi.search(prfi_name, element_position_map)
                            if search_prfi_code == 200:
                                delete_prfi = DeleteProfile(driver)
                                delete_prfi_code = delete_prfi.delete(element_position_map, first_row_checkbox_element, True)
                                if delete_prfi_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} profile successfully.".format(prfi_key_out), flush=True)
                                else:
                                    result = result + " In addition, fail to delete {} profile.".format(prfi_key_out)
                                    break
                            else:
                                result = result + " In addition, fail to search {} profile.".format(prfi_key_out)
                                break
                            # 退出遍历标志
                            if prfi_status == 1:  # 失败，退出遍历创建
                                break
                    # 退出遍历标志
                    if prfi_status == 1:  # 失败，退出遍历创建
                        break
            # 删除object
            if delete_rule_code == 200:
                # 删除ip
                for x in range(len(ip_data)):
                    search_ip = SearchObject(driver)
                    search_ip_code, first_row_checkbox_element = search_ip.search(ip_data[x]["name"], test_ip_object_element_position)
                    if search_ip_code == 200:
                        delete_ip = DeleteObject(driver)
                        delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
                        if delete_ip_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip object successfully.", flush=True)
                        elif delete_ip_code != 200:
                            ui_result = ui_result + " In addition, fail to delete ip object."
                            break
                    else:
                        ui_result = ui_result + " In addition, fail to search ip object."
                        break
                # 删除fqdn
                for x in range(len(fqdn_data)):
                    search_fqdn = SearchObject(driver)
                    search_fqdn_code, first_row_checkbox_element = search_fqdn.search(fqdn_data[x]["name"], test_fqdn_object_element_position)
                    if search_fqdn_code == 200:
                        delete_fqdn = DeleteObject(driver)
                        delete_fqdn_code = delete_fqdn.delete(test_fqdn_object_element_position, first_row_checkbox_element, True)
                        if delete_fqdn_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn object successfully.", flush=True)
                        elif delete_fqdn_code != 200:
                            result = result + " In addition, fail to delete fqdn object."
                            break
                    else:
                        result = result + " In addition, fail to search fqdn object."
                        break
            
            result["ui_result"] = ui_result
        
        if parameter["script_type"] == "api" or need_initialization == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)
            
            parameter["script_type"] = "api"
            
            
            
            # 数据转换，适配API的test_data
            translation = DataTranslation()
            temp_test_data = translation.data_translation(test_data["policy_type"], test_data["condition"])
            test_data["obj_condition"] = temp_test_data["obj_condition"]
            test_data["application"] = temp_test_data["application"]
            
            # 添加测试过程中涉及的template
            template_path = {}
            template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
            template_path["object_template"] = parameter["path"] + "/template/object_template.json"

            # 创建Object、Profile、Rule
            create = CreatePolicy()
            cfg_list = create.create_policy(parameter, test_data, template_path)
            
            # 流量验证
            verify = Verification()
            verification_result = verify.verification("", parameter, test_data, cfg_list, "")
            
            # 分析验证结果，并返回给flask
            analysis = AnalysisResult()
            api_result = analysis.analysis_result(test_data, cfg_list, verification_result)
            
            # 删除配置
            delete = DeletePolicy()
            delete.delele_policy_by_cfg(token, parameter, cfg_list)
            
            result["api_result"] = api_result
    
        return result

    def delete_data(self):
        # 清理环境
        support.ui_utils.env.teardown()
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list):
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        if isinstance(self.api_name_list, list):
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)
            
if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 5,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/api",
        "module_name": "dos_protection",
        "test_case_name": "dos_protect_srcip_http_rate_srcip_d3"
    }