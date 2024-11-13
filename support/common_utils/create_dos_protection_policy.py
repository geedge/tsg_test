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
from support.packet_generator.verify import Verify
from support.api_utils.analyse_result import Analyse
from support.common_utils.data_translation import DataTranslation
import support.ui_utils.env
from datetime import datetime
from support.ui_utils.element_position.map_element_position_library import *



class CreateDosProtectionPolicy:
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

        # 使用trex的随机源ip
        if test_data["traffic"]["type"] == "trex":
            organize_config = OrganizeConfig()
            test_data = organize_config.generate_random_dos_src_ip(test_data,parameter)
            test_data = organize_config.generate_only_dstip_for_trex_replay(test_data)

        # 无需创建的condition
        dos_protection_no_create_list = ["application", "ip_protocol", "sub_action_override"]
        # name_list汇总
        temp_name_list = []
        policy_name_dict = {}
        policy_name_dict["type"] = test_data["policy_type"]
        policy_name_dict["name"] = test_data["rule_name"]
        temp_name_list.append(policy_name_dict)
        for con_key, conditions in test_data["condition"].items():
            if conditions:  # 确保conditions不为空
                if con_key in dos_protection_no_create_list:
                    continue
                for condition in conditions:
                    # 为每个条件项创建一个新的字典
                    obj_name_dict = {
                        "type": condition["object_type"],
                        "name": condition["name"]
                    }
                    temp_name_list.append(obj_name_dict)

        self.ui_name_list = temp_name_list
        self.api_name_list = temp_name_list

        need_initialization = False
        if len(parameter["script_type"]) == 0:
            need_initialization = True

        if parameter["script_type"] == "ui" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)

                parameter["script_type"] = "ui"

                # 环境初始化
                support.ui_utils.env.initiate_selenium_request()
                driver = support.ui_utils.env.my_driver()
                support.ui_utils.env.setup()

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
                cond_code = 200
                if cond_code == 200:
                    create_rule = CreateRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    #动态选择变量
                    if test_data["rule_action"] == "protect":
                        element_position_map["create"]["policyRulePage_selectAction_posXpath"] = dosRulePage_selectProtect_posXpath
                        if test_data["threshold"]["type"] == "rate":
                            element_position_map["create"]["policyRulePage_thresholdType_posXpath"] = dosRulePage_thresholdRateType_posXpath
                            element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = policyRulePage_mitigationTimeouts_select_posXpath
                        elif test_data["threshold"]["type"] == "concurrency":
                            element_position_map["create"]["policyRulePage_thresholdType_posXpath"] = dosRulePage_thresholdConcurrencyType_posXpath
                            element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = dosRulePage_mitigationTimeouts_select_bottom_posXpath
                        if test_data["mitigation"]["behavior"] == "deny":
                            element_position_map["create"]["policyRulePage_mitigationBehavior_posXpath"] = dosRulePage_mitigationBehavior_deny_posXpath
                        elif test_data["mitigation"]["behavior"] == "none":
                            element_position_map["create"]["policyRulePage_mitigationBehavior_posXpath"] = dosRulePage_mitigationBehavior_none_posXpath
                    elif test_data["rule_action"] == "allow":
                        element_position_map["create"]["policyRulePage_selectAction_posXpath"] = dosRulePage_selectAllow_posXpath
                    elif test_data["rule_action"] == "deny":
                        element_position_map["create"]["policyRulePage_selectAction_posXpath"] = dosRulePage_selectDeny_posXpath
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
                    # search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"],
                    #                                                     test_data["rule_name"],
                    #                                                     element_position_map)
                    search_rule_code = 200
                    if search_rule_code == 200:
                        #test_data["rule_id"] = rule_id
                        verification = Verify()
                        verification_result = verification.verify_result(driver, parameter, test_data, [],
                                                                  element_position_map)
                        if len(verification_result) == 4:
                            driver = verification_result[3]
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                              "Traffic verification failed", flush=True)

                # 分析验证结果，并返回给flask
                if len(verification_result) == 4:
                    analysis = Analyse()
                    ui_result = analysis.analyse_result(test_data["policy_type"], [], verification_result)

                # 删除rule
                if create_rule_code == 200:
                    search_rule = SearchRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"],
                                                                                      test_data["rule_name"],
                                                                                      element_position_map)
                    if search_rule_code == 200:
                        delete_rule = DeleteRule(driver)
                        delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element,
                                                              True)
                        if delete_rule_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                  "Delete monitor rule successfully.", flush=True)
                        elif delete_rule_code != 200:
                            ui_result = ui_result + " In addition, fail to delete {} rule.".format(
                                test_data["policy_type"])
                    else:
                        ui_result = ui_result + " In addition, fail to search {} rule.".format(
                            test_data["policy_type"])

                # 删除object
                if delete_rule_code == 200 and "condition" in test_data.keys():
                    # 删除
                    for cond_key, cond_value in (test_data["condition"].items()):  # 遍历所有cond数据
                        if cond_key == "application":
                            continue  # 直接跳过
                        cond_status = 0
                        cond_key_out = cond_key.replace("_", " ")
                        if len(cond_value) != 0:  # 不为空
                            cond_data = cond_value
                            for i in range(len(cond_data)):  # 遍历查询所有condition
                                search_cond = SearchObject(driver)
                                if cond_key == "protocol_filed":
                                    tmp_key = cond_data[i]["object_type"]
                                    if tmp_key == "boolean":  # "object_type": "boolean"时无需删除
                                        continue
                                    cond_key_out = tmp_key.replace("_", " ")
                                    element_position_map = get_element_position(tmp_key)
                                else:
                                    element_position_map = get_element_position(cond_key)
                                search_cond_code, first_row_checkbox_element = search_cond.search(
                                    cond_data[i]["name"],
                                    element_position_map)
                                if search_cond_code == 200:
                                    delete_cond = DeleteObject(driver)
                                    delete_cond_code = delete_cond.delete(element_position_map,
                                                                          first_row_checkbox_element,
                                                                          True)
                                    if delete_cond_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                              str(datetime.now().microsecond)[:3],
                                              "Delete {} object successfully.".format(cond_key_out), flush=True)
                                    else:
                                        ui_result = ui_result + " In addition, fail to delete {} object.".format(
                                            cond_key_out)
                                        break
                                else:
                                    ui_result = ui_result + " In addition, fail to search {} object.".format(
                                        cond_key_out)
                                    break
                                # 退出遍历标志
                                if cond_status == 1:  # 失败，退出遍历创建
                                    break
                        # 退出遍历标志
                        # if cond_status == 1:  # 失败，退出遍历创建
                        #     break
            except Exception as e:
                raise
            finally:
                result["ui_result"] = ui_result
                # 删除配置
                # delete = DeletePolicy()
                # delete.delele_policy_by_uuid(token, parameter, temp_name_list)

        if parameter["script_type"] == "api" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Begin to run api test case", flush=True)

                parameter["script_type"] = "api"

                # 数据转换，适配API的test_data
                translation = DataTranslation()
                test_data = translation.data_translation(parameter, test_data)

                # 添加测试过程中涉及的template
                template_path = {}
                template_path["rule_template"] = parameter["root_path"] + "/support/api_utils/template/rule_template.json"
                template_path["object_template"] = parameter["root_path"] + "/support/api_utils/template/object_template.json"

                # 创建Object、Profile、Rule
                create = CreatePolicy()
                cfg_list = create.create_policy(parameter, test_data, template_path)

                # 流量验证
                verification = Verify()
                verification_result = verification.verify_result("", parameter, test_data, cfg_list, "")

                # 分析验证结果，并返回给flask
                analysis = Analyse()
                api_result = analysis.analyse_result(test_data["policy_type"], cfg_list, verification_result)

            except Exception as e:
                raise
            finally:
                result["api_result"] = api_result
                # 删除配置
                delete = DeletePolicy()
                delete.delele_policy_by_uuid(token, parameter, cfg_list)

        return result

    def clean_up(self):
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.ui_name_list != []:
            # 清理环境
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