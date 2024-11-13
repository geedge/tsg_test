# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime

class CreateSecurityRuleExample:
    def create_rules(self, parameter, policy_configuration):
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)
            
            result = ""
            configured_policy = {}
            
            log_in = LogIn()
            pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
            token = log_in.login(parameter["username"], pwd, parameter["api_server"])
            configured_policy["token"] = token
            
            support.ui_utils.env.initiate_selenium_request()
            driver = support.ui_utils.env.my_driver()
            support.ui_utils.env.setup()

            if "condition" in policy_configuration.keys():
                for cond_key, cond_value in (policy_configuration["condition"].items()):
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
                                result = "Fail to create {} object.".format(cond_key_out)
                                cond_status = 1
                                break
                    if cond_status == 1:  # 创建失败，退出遍历创建
                        break
            
            # 创建rule
            if cond_code == 200:
                create_rule = CreateRule(driver)
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
            
            configured_policy["driver"] = driver
            return token, driver, result
        except Exception as e:
            return "Exception Error: " + str(e)
