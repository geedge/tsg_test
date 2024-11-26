# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_objects import CreateObjects
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime

class CreateSecurityRulesExample:
    def create_rules(self, policy_configuration, driver):
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)
            
            result = ""

            if "condition" in policy_configuration.keys():
                for cond_key, cond_value in (policy_configuration["condition"].items()):
                    cond_status = 0
                    if cond_key == "application":
                        continue  # 直接跳过
                    cond_key_out = cond_key.replace("_", " ")
                    if len(cond_value) != 0:  # 不为空
                        cond_data = cond_value
                        create_ip = CreateObjects(driver)
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
                                result = "Fail to create {} object.".format(cond_key_out)
                                cond_status = 1
                                break
                    if cond_status == 1:  # 创建失败，退出遍历创建
                        break
            
            # 创建rule
            if cond_code == 200:
                create_rule = CreateRules(driver)
                element_position_map = get_element_position(policy_configuration["policy_type"])
                #动态选择变量
                if policy_configuration["threshold"]["type"] == "rate":
                    element_position_map["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdRateType_posXpath
                    element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = policyRulePage_mitigationTimeouts_select_posXpath
                elif policy_configuration["threshold"]["type"] == "concurrency":
                    element_position_map["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdConcurrencyType_posXpath
                    element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = dosRulePage_mitigationTimeouts_select_bottom_posXpath
                if policy_configuration["mitigation"]["behavior"] == "deny":
                    element_position_map["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_deny_posXpath
                elif policy_configuration["mitigation"]["behavior"] == "none":
                    element_position_map["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_none_posXpath

                create_rule_code = create_rule.create(policy_configuration, element_position_map)
                if create_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(policy_configuration["policy_type"], flush=True))
                elif create_rule_code != 200:
                    result = "Fail to create {} rule.".format(policy_configuration["policy_type"])
                    return "", "", result
                
                search_rule = SearchRules(driver)
                element_position_map = get_element_position(policy_configuration["policy_type"])
                search_rule_code, rule_uuid = search_rule.get_rule_id(policy_configuration["policy_type"], policy_configuration["name"], element_position_map)
                if search_rule_code != 200:
                    result = "Fail to search {} rule uuid.".format(policy_configuration["policy_type"])
                    return "", "", result
                rule_uuids_list = []
                rule_uuids_temp_dict = {}
                rule_uuids_temp_dict["type"] = policy_configuration["type"]
                rule_uuids_temp_dict["uuid"] = rule_uuid
                rule_uuids_temp_dict["name"] = policy_configuration["name"]
                rule_uuids_temp_dict["attribute_name"] = policy_configuration["type"].upper() + "_" + "RULE"
                rule_uuids_list.append(rule_uuids_temp_dict)
                rule_uuids_tuple = tuple(rule_uuids_list)
                
            return rule_uuids_tuple, result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating rule by ui, the exception error: ", str(e), flush=True)
            return "", "When creating rule by ui, the exception error: " + str(e)
