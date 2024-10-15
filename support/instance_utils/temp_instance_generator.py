# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.api_utils.organize_config import OrganizeConfig
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.create_policy import CreatePolicy
from support.instance_utils.data_translation import DataTranslation
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime

class DosProtectionInstanceGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        result = self.create(self.test_data, self.parameter)
        return result

    def create(self, test_data, parameter, number):
        self.api_name_list, self.ui_name_list = [], []
        ui_result, api_result = "", ""
        creation_result = {
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

        if len(parameter["script_type"]) == 0:
            if number == 0:
                parameter["script_type"] = "ui"
            elif number == 1:
                parameter["script_type"] = "api"

        if parameter["script_type"] == "ui":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)

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
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(cond_key_out), flush=True)
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
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(test_data["policy_type"], flush=True))
                elif create_rule_code != 200:
                    ui_result = "Fail to create {} rule.".format(test_data["policy_type"])

            creation_result["driver"] = driver
            creation_result["element_position_map"] = element_position_map
            
        if parameter["script_type"] == "api":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)

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
            creation_result["cfg_list"] = cfg_list
        
        creation_result["ui_result"] = ui_result
        creation_result["api_result"] = api_result
        return creation_result

    def delete_data(self, test_data, creation_result):
        ui_result, api_result = "", ""
        deletion_result = {
            "ui_result": "",
            "api_result": ""
        }
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.ui_name_list != [] and "driver" in creation_result and len(creation_result["driver"]) > 0:
            driver = creation_result["driver"]
            # 删除rule
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(test_data["policy_type"])
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], element_position_map)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete monitor rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    ui_result = ui_result + " In addition, fail to delete {} rule.".format(test_data["policy_type"])
            else:
                ui_result = ui_result + " In addition, fail to search {} rule.".format(test_data["policy_type"])
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
                            search_cond_code, first_row_checkbox_element = search_cond.search(cond_data[i]["name"], element_position_map)
                            if search_cond_code == 200:
                                delete_cond = DeleteObject(driver)
                                delete_cond_code = delete_cond.delete(element_position_map, first_row_checkbox_element, True)
                                if delete_cond_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(cond_key_out), flush=True)
                                else:
                                    ui_result = ui_result + " In addition, fail to delete {} object.".format(cond_key_out)
                                    break
                            else:
                                ui_result = ui_result + " In addition, fail to search {} object.".format(cond_key_out)
                                break
                            # 退出遍历标志
                            if cond_status == 1:  # 失败，退出遍历创建
                                break
                    # 退出遍历标志
                    if cond_status == 1:  # 失败，退出遍历创建
                        break
            # 环境清理
            support.ui_utils.env.teardown()
            # 强行删除，防止有配置残留影响其他用例测试
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        if isinstance(self.api_name_list, list) and self.api_name_list != [] and "cfg_list" in creation_result and len(creation_result["cfg_list"]) > 0:
            cfg_list = creation_result["cfg_list"]
            # 按配置进行删除
            delete.delele_policy_by_cfg(test_data["token"], parameter, cfg_list)
            # 强行删除，防止有配置残留影响其他用例测试
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)
        deletion_result["ui_result"] = ui_result
        deletion_result["api_result"] = api_result
        return deletion_result
        
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