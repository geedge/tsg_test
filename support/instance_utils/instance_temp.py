# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.api_utils.organize_config import OrganizeConfig
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.api_utils.create_policy import CreatePolicy
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime

class InstanceTemp:
    def __init__(self, test_data, parameter, loop_number):
        self.test_data = test_data
        self.parameter = parameter
        self.loop_number = loop_number

    def create(self):
        try:
            api_name_list, ui_name_list = [], []
            ui_result, api_result = "", ""
            creation_result = {
                "ui_result": "", 
                "api_result": ""
            }
            
            log_in = LogIn()
            pwd = log_in.encryptPwd(self.parameter["password"], self.parameter["api_server"])
            token = log_in.login(self.parameter["username"], pwd, self.parameter["api_server"])
            self.test_data["token"] = token

            # 使用trex的随机源ip
            if self.test_data["traffic_generation"]["type"] == "trex":
                organize_config = OrganizeConfig()
                self.test_data = organize_config.generate_random_dos_src_ip(self.test_data, self.parameter)
                self.test_data = organize_config.generate_only_dstip_for_trex_replay(self.test_data)
                
            # name_list汇总
            temp_name_list = []
            policy_name_dict = {}
            policy_name_dict["type"] = self.test_data["policy_configuration"]["type"]
            policy_name_dict["name"] = self.test_data["policy_configuration"]["name"]
            temp_name_list.append(policy_name_dict)
            for con_key, conditions in self.test_data["policy_configuration"].items():
                if conditions:  # 确保conditions不为空
                    for condition in conditions:
                        # 为每个条件项创建一个新的字典
                        obj_name_dict = {
                            "type": condition["type"],
                            "name": condition["name"]
                        }
                        temp_name_list.append(obj_name_dict)
            ui_name_list = temp_name_list
            api_name_list = temp_name_list
            
            if len(self.parameter["script_type"]) == 0:
                if self.loop_number == 0:
                    self.parameter["script_type"] = "ui"
                elif self.loop_number == 1:
                    self.parameter["script_type"] = "api"

            if self.parameter["script_type"] == "ui":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)

                # 环境初始化
                support.ui_utils.env.initiate_selenium_request()
                driver = support.ui_utils.env.my_driver()
                support.ui_utils.env.setup()

                if "condition" in self.test_data.keys():
                    for cond_key, cond_value in (self.test_data["condition"].items()):
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
                    element_position_map = get_element_position(self.test_data["policy_type"])
                    #动态选择变量
                    if self.test_data["threshold"]["type"] == "rate":
                        element_position_map["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdRateType_posId
                        element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = policyRulePage_mitigationTimeouts_select_posXpath
                    elif self.test_data["threshold"]["type"] == "concurrency":
                        element_position_map["create"]["policyRulePage_thresholdType_posId"] = dosRulePage_thresholdConcurrencyType_posId
                        element_position_map["create"]["policyRulePage_mitigationTimeouts_select_posXpath"] = dosRulePage_mitigationTimeouts_select_bottom_posXpath
                    if self.test_data["mitigation"]["behavior"] == "deny":
                        element_position_map["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_deny_posId
                    elif self.test_data["mitigation"]["behavior"] == "none":
                        element_position_map["create"]["policyRulePage_mitigationBehavior_posId"] = dosRulePage_mitigationBehavior_none_posId

                    create_rule_code = create_rule.create(self.test_data, element_position_map)
                    if create_rule_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(self.test_data["policy_type"], flush=True))
                    elif create_rule_code != 200:
                        ui_result = "Fail to create {} rule.".format(self.test_data["policy_type"])

                creation_result["driver"] = driver
                creation_result["element_position_map"] = element_position_map
                
            if self.parameter["script_type"] == "api":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)

                # 添加测试过程中涉及的template
                template_path = {}
                template_path["rule_template"] = self.parameter["root_path"] + "/support/api_utils/template/rule_template.json"
                template_path["object_template"] = self.parameter["root_path"] + "/support/api_utils/template/object_template.json"

                # 创建Object、Profile、Rule
                create = CreatePolicy()
                cfg_list = create.create_policy(self.parameter, self.test_data, template_path)
                
                creation_result["cfg_list"] = cfg_list
            
            creation_result["ui_result"] = ui_result
            creation_result["api_result"] = api_result
            creation_result["ui_name_list"] = ui_name_list
            creation_result["api_name_list"] = api_name_list
            creation_result["token"] = token
            
            return creation_result
        except Exception as e:
            return "Exception Error: " + str(e)
