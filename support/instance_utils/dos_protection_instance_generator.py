# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import os
import sys

from support.api_utils.organize_config import OrganizeConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.create_policy import CreatePolicy
from support.packet_generator.verification import Verification
from support.api_utils.analysis_result import AnalysisResult
from support.instance_utils.data_translation import DataTranslation
import support.ui_utils.env
from datetime import datetime
from support.ui_utils.element_position.map_element_position_library import *



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
        self.api_name_list, self.ui_name_list = [], []
        result = {
            "ui_result": "",
            "api_result": ""
        }
        
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        # 使用随机ip
        if test_data["traffic"]["type"] == "trex":
            organize_config = OrganizeConfig()
            test_data = organize_config.generate_random_ip(test_data, parameter)
        
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
            tmp_name_dict = {}
            tmp_name_dict["type"] = test_data["policy_type"]
            tmp_name_dict["name"] = test_data["rule_name"]
            self.ui_name_list.append(tmp_name_dict)
            # 构建source ip 的name list
            if "source_ip" in test_data["condition"] and len(test_data["condition"]["source_ip"]) != 0:
                object_data = test_data["condition"]["source_ip"]
                for i in range(len(object_data)):
                    tmp_name_dict = {}
                    tmp_name_dict["type"] = object_data[i]['object_type']
                    tmp_name_dict["name"] = object_data[i]['name']
                    self.ui_name_list.append(tmp_name_dict)
            # 构建server fqdn 的name list
            if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
                object_data = test_data["condition"]["server_fqdn"]
                for i in range(len(object_data)):
                    tmp_name_dict = {}
                    tmp_name_dict["type"] = test_data["condition"]["server_fqdn"][i]['object_type']
                    tmp_name_dict["name"] = test_data["condition"]["server_fqdn"][i]['name']
                    self.ui_name_list.append(tmp_name_dict)
            # 构建protocol field 的name list
            if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
                object_data = test_data["condition"]["protocol_filed"]
                for i in range(len(object_data)):
                    # 排除 boolean 类型的 protocol_filed
                    if object_data[i]['object_type'] == 'boolean':
                        continue
                    tmp_name_dict = {}
                    tmp_name_dict["type"] = test_data["condition"]["protocol_filed"][i]['object_type']
                    tmp_name_dict["name"] = test_data["condition"]["protocol_filed"][i]['name']
                    self.ui_name_list.append(tmp_name_dict)
            
            # 添加dos_protection_rule定位库集合
            test_rule_element_position = {}
            if test_data["policy_type"] == "dos_protection":
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
                        "policyRulePage_thresholdType_posId": "",
                        "policyRulePage_groupBy_dropDownBox_posXpath": dosRulePage_groupBy_dropDownBox_posXpath,
                        "policyRulePage_groupBy_select_posXpath": dosRulePage_groupBy_select_posXpath,
                        "policyRulePage_requestPerPeriod_posXpath": dosRulePage_requestPerPeriod_posXpath,
                        "policyRulePage_countingPeriod_dropDownBox_posXpath": dosRulePage_countingPeriod_dropDownBox_posXpath,
                        "policyRulePage_countingPeriod_select_posXpath": dosRulePage_countingPeriod_select_posXpath,
                        "policyRulePage_concurrentSsessions_posXpath" : dosRulePage_concurrentSsessions_posXpath,
                        "policyRulePage_mitigationBehavior_posId": "",
                        "policyRulePage_mitigationTimeouts_dropDownBox_posXpath": dosRulePage_mitigationTimeouts_dropDownBox_posXpath,
                        "policyRulePage_mitigationTimeouts_select_posXpath": "",
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

            # if test_data["threshold"]["type"] == "rate":
            #     get_element_position(test_data["policy_type"])["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdRateType_posId
            #     get_element_position(test_data["policy_type"])["policyRulePage_mitigationTimeouts_select_posXpath"] = policyRulePage_mitigationTimeouts_select_posXpath
            # elif test_data["threshold"]["type"] == "concurrency":
            #     get_element_position(test_data["policy_type"])["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdConcurrencyType_posId
            #     get_element_position(test_data["policy_type"])["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = dosRulePage_mitigationTimeouts_select_bottom_posXpath
            # if test_data["mitigation"]["behavior"] == "deny":
            #     get_element_position(test_data["policy_type"])["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_deny_posId
            # elif test_data["mitigation"]["behavior"] == "none":
            #     get_element_position(test_data["policy_type"])["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_none_posId


            if "condition" in test_data.keys():
                for cond_key, cond_value in (test_data["condition"].items()):
                    cond_status = 0
                    if cond_key == "application":
                        continue  # 直接跳过
                    cond_key_out = cond_key.replace("_", " ")
                    if len(cond_value) != 0:  # 不为空
                        cond_data = cond_value
                        create_ip = CreateObject(driver)
                        for i in range(len(cond_data)):  # 遍历创建所有condition
                            if cond_key == "protocol_filed":
                                tmp_key = cond_data[i]["object_type"]
                                if tmp_key == "boolean":  # "object_type": "boolean"时无需创建
                                    continue
                                cond_key_out = tmp_key.replace("_", " ")
                                element_position_map = get_element_position(tmp_key)
                            else:
                                element_position_map = get_element_position(cond_key)
                            cond_code = create_ip.create(cond_data[i], element_position_map)
                            if cond_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      str(datetime.now().microsecond)[:3],
                                      "Create {} object successfully.".format(cond_key_out), flush=True)
                            else:
                                ui_result = "Fail to create {} object.".format(cond_key_out)
                                cond_status = 1
                                break
                    if cond_status == 1:  # 创建失败，退出遍历创建
                        break


            # 创建rule
            if cond_code == 200:
                create_rule = CreateRule(driver)
                element_position_map = get_element_position(test_data["policy_type"])
                #动态选择变量
                if test_data["threshold"]["type"] == "rate":
                    element_position_map["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdRateType_posId
                    element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = policyRulePage_mitigationTimeouts_select_posXpath
                elif test_data["threshold"]["type"] == "concurrency":
                    element_position_map["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdConcurrencyType_posId
                    element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = dosRulePage_mitigationTimeouts_select_bottom_posXpath
                if test_data["mitigation"]["behavior"] == "deny":
                    element_position_map["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_deny_posId
                elif test_data["mitigation"]["behavior"] == "none":
                    element_position_map["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_none_posId

                create_rule_code = create_rule.create(test_data, element_position_map)
                if create_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Create {} rule successfully.".format(test_data["policy_type"], flush=True))
                elif create_rule_code != 200:
                    ui_result = "Fail to create {} rule.".format(test_data["policy_type"])

            # 触发流量验证
            if create_rule_code == 200:
                search_rule = SearchRule(driver)
                element_position_map = get_element_position(test_data["policy_type"])
                search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"],
                                                                    test_data["rule_name"],
                                                                    element_position_map)
                if search_rule_code == 200:
                    test_data["rule_id"] = rule_id
                    verify = Verification()
                    verification_result = verify.verification(driver, parameter, test_data, [],
                                                              element_position_map)
                    if len(verification_result) == 4:
                        driver = verification_result[3]
                    elif len(verification_result) == 5:
                        driver = verification_result[4]
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Traffic verification failed", flush=True)

            # 分析验证结果，并返回给flask
            if len(verification_result) != 0:
                analysis = AnalysisResult()
                ui_result = analysis.analysis_result(test_data, [], verification_result)

            # # 删除rule
            # if create_rule_code == 200:
            #     search_rule = SearchRule(driver)
            #     element_position_map = get_element_position(test_data["policy_type"])
            #     search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"],
            #                                                                       test_data["rule_name"],
            #                                                                       element_position_map)
            #     if search_rule_code == 200:
            #         delete_rule = DeleteRule(driver)
            #         delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element,
            #                                               True)
            #         if delete_rule_code == 200:
            #             print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
            #                   "Delete monitor rule successfully.", flush=True)
            #         elif delete_rule_code != 200:
            #             ui_result = ui_result + " In addition, fail to delete {} rule.".format(
            #                 test_data["policy_type"])
            #     else:
            #         ui_result = ui_result + " In addition, fail to search {} rule.".format(
            #             test_data["policy_type"])
            #
            # # 删除object
            # if delete_rule_code == 200 and "condition" in test_data.keys():
            #     # 删除
            #     for cond_key, cond_value in (test_data["condition"].items()):  # 遍历所有cond数据
            #         if cond_key == "application":
            #             continue  # 直接跳过
            #         cond_status = 0
            #         cond_key_out = cond_key.replace("_", " ")
            #         if len(cond_value) != 0:  # 不为空
            #             cond_data = cond_value
            #             for i in range(len(cond_data)):  # 遍历查询所有condition
            #                 search_cond = SearchObject(driver)
            #                 if cond_key == "protocol_filed":
            #                     tmp_key = cond_data[i]["object_type"]
            #                     if tmp_key == "boolean":  # "object_type": "boolean"时无需删除
            #                         continue
            #                     cond_key_out = tmp_key.replace("_", " ")
            #                     element_position_map = get_element_position(tmp_key)
            #                 else:
            #                     element_position_map = get_element_position(cond_key)
            #                 search_cond_code, first_row_checkbox_element = search_cond.search(
            #                     cond_data[i]["name"],
            #                     element_position_map)
            #                 if search_cond_code == 200:
            #                     delete_cond = DeleteObject(driver)
            #                     delete_cond_code = delete_cond.delete(element_position_map,
            #                                                           first_row_checkbox_element,
            #                                                           True)
            #                     if delete_cond_code == 200:
            #                         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #                               str(datetime.now().microsecond)[:3],
            #                               "Delete {} object successfully.".format(cond_key_out), flush=True)
            #                     else:
            #                         ui_result = ui_result + " In addition, fail to delete {} object.".format(
            #                             cond_key_out)
            #                         break
            #                 else:
            #                     ui_result = ui_result + " In addition, fail to search {} object.".format(
            #                         cond_key_out)
            #                     break
            #                 # 退出遍历标志
            #                 if cond_status == 1:  # 失败，退出遍历创建
            #                     break
            #         # 退出遍历标志
            #         if cond_status == 1:  # 失败，退出遍历创建
            #             break


                result["ui_result"] = ui_result

        if parameter["script_type"] == "api" or need_initialization == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                  "Begin to run api test case", flush=True)

            parameter["script_type"] = "api"

            self.api_name_list = []

            # 数据转换，适配API的test_data
            translation = DataTranslation()
            temp_test_data = translation.data_translation(test_data["policy_type"], test_data)
            test_data["obj_condition"] = temp_test_data["obj_condition"]
            test_data["application"] = temp_test_data["application"]
            test_data["profile_condition"] = temp_test_data["profile_condition"]
            print(test_data)

            # 添加测试过程中涉及的template
            template_path = {}
            template_path["rule_template"] = parameter["root_path"] + "/support/api_utils/template/rule_template.json"
            template_path["object_template"] = parameter["root_path"] + "/support/api_utils/template/object_template.json"
            template_path["pre_intercept_template_path"] = parameter[
                                                               "root_path"] + "/support/api_utils/template/pre_intercept_template.json"
            # 添加测试过程中涉及的response pages
            template_path["profiles_hijack_file_path"] = parameter[
                                                             "root_path"] + "/support/api_utils/preset_profile/Create-Hijack-Files-test-3.html"

            # 创建Object、Profile、Rule
            create = CreatePolicy()
            cfg_list = create.create_policy(parameter, test_data, template_path)

            # 流量验证
            verify = Verification()
            verification_result = verify.verification("", parameter, test_data, cfg_list, "")

            # 分析验证结果，并返回给flask
            analysis = AnalysisResult()
            api_result = analysis.analysis_result(test_data, cfg_list, verification_result)

            result["api_result"] = api_result
            # 删除配置
            delete = DeletePolicy()
            delete.delele_policy_by_cfg(token, parameter, cfg_list)

            return result

    def delete_data(self):
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.ui_name_list != []:
            # 清理环境
            support.ui_utils.env.teardown()
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        if isinstance(self.api_name_list, list) and self.api_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)
            
if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 5,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/ui",
        "module_name": "dos_protection",
        "test_case_name": "dos_protect_srcip_http_rate_srcip_d3"
    }