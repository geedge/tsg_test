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
from support.ui_utils.policy.edit_rule import EditRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.packet_generator.verification import Verification
from support.api_utils.create_policy import CreatePolicy
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import DeletePolicy
import support.ui_utils.env
# from support.report import *
from datetime import datetime
from support.instance_utils.data_translation import DataTranslation

class DosProtectionInstanceGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        result = self._run(self.test_data, self.parameter)
        return result

    def _run(self, test_data, parameter):
        # 参数初始化
        ui_result, api_result= "", ""
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
                }
            ]
            
            # 添加定位库集合
            test_rule_element_position = {}
            if test_data["policy_type"] == "dos_protection":
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
                test_rule_element_position = {
                    "page_jump":{
                        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                        "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_dos_posId
                    },
                    "create": {
                        "policyRuleListPage_createButton_posId": dosRuleListPage_createButton_posId,
                        "policyRulePage_inputName_posXpath": dosRulePage_inputName_posXpath,
                        "policyRulePage_selectAction_posId": dosRulePage_selectShunt_posId,
                        "policyRulePage_addSrcIP_posXpath": dosRulePage_addSrcIP_posXpath,
                        "policyRulePage_searchSrcIP_posXpath": dosRulePage_searchSrcIP_posXpath,
                        "policyRulePage_selectSrcIP_posXpath": dosRulePage_selectSrcIP_posXpath,
                        "policyRulePage_closeSrcIP_posXpath": dosRulePage_closeSrcIP_posXpath,
                        "policyRulePage_addApplication_posXpath": dosRulePage_addApplication_posXpath,
                        "policyRulePage_selectApplicationLabel_posXpath": dosRulePage_selectApplicationLabel_posXpath,
                        "policyRulePage_searchApplication_posXpath": dosRulePage_searchApplication_posXpath,
                        "policyRulePage_selectApplication_posXpath": dosRulePage_selectApplication_posXpath,
                        "policyRulePage_closeApplication_posXpath": dosRulePage_closeApplication_posXpath,
                        "policyRulePage_thresholdType_posId": dosRulePage_thresholdType_posId,
                        "policyRulePage_groupBy_dropDownBox_posXpath": dosRulePage_groupBy_dropDownBox_posXpath,
                        "policyRulePage_groupBy_select_posXpath": dosRulePage_groupBy_select_posXpath,
                        "policyRulePage_requestPerPeriod_posXpath": dosRulePage_requestPerPeriod_posXpath,
                        "policyRulePage_countingPeriod_dropDownBox_posXpath": dosRulePage_countingPeriod_dropDownBox_posXpath,
                        "policyRulePage_countingPeriod_select_posXpath": dosRulePage_countingPeriod_select_posXpath,
                        "policyRulePage_mitigationBehavior_deny_posId": dosRulePage_mitigationBehavior_deny_posId,
                        "policyRulePage_mitigationTimeouts_dropDownBox_posXpath": dosRulePage_mitigationTimeouts_dropDownBox_posXpath,
                        "policyRulePage_mitigationTimeouts_select_posXpath": dosRulePage_mitigationTimeouts_select_posXpath,
                        "policyRulePage_enable_posXpath": dosRulePage_enable_posXpath,
                        "policyRulePage_okButton_yes_posId": dosRulePage_ok_posId,
                        "policyRulePage_okButton_warningYes_posXpath": dosRulePage_okButton_warningYes_posXpath
                    },
                    "search": {
                        "policyRuleListPage_searchLable_posId": dosRuleListPage_searchLable_posId,
                        "policyRuleListPage_searchLable_dropDown_item_posXpath": dosRuleListPage_searchLable_dropDown_item_posXpath,
                        "policyRuleListPage_searchLable_input_itemContent_posXpath": dosRuleListPage_searchLable_input_itemContent_posXpath,
                        "policyRuleListPage_searchLable_searchButton_posId": dosRuleListPage_searchLable_searchButton_posId,
                        "policyRuleListPage_tableTbody_posXpath": dosRuleListPage_tableTbody_posXpath
                    },
                    "delete": {
                        "policyRuleListPage_allSelect_posXpath": dosRuleListPage_allSelect_posXpath,
                        "policyRuleListPage_deleteButton_posId": dosRuleListPage_deleteButton_posId,
                        "policyRuleListPage_okButton_warningYes_posXpath": dosRuleListpage_okButton_warningYes_posXpath,
                        "policyRuleListPage_okButton_warningNo_posXpath":dosRuleListpage_okButton_warningNo_posXpath
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
            
            result["ui_result"] = ui_result
        
        if parameter["script_type"] == "api" or need_initialization == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)
            
            parameter["script_type"] = "api"
            
            self.api_name_list = []
            
            # 数据转换，适配API的test_data
            translation = DataTranslation()
            test_data = translation.data_translation(parameter, test_data)
            
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