# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.profile.create_profile import CreateProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.create_policy import CreatePolicy
from support.packet_generator.verification import Verification
from support.ui_utils.element_position.map_element_position_library import get_element_position, get_name_list, create_pre_policy, delete_pre_policy
from support.ui_utils.element_position.map_element_position_library import manipulation_profile_no_create_list, manipulation_object_no_create_list
from support.api_utils.analysis_result import AnalysisResult
import support.ui_utils.env
from datetime import datetime
import copy


class ManipulationGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        ui_result = self._run(self.test_data, self.parameter)
        return ui_result

    def _run(self, test_data, parameter):
        ui_result, api_result = "", ""
        result = {
            "ui_result": "",
            "api_result": ""
        }

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token
        self.test_data["token"] = token

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
            self.ui_name_list = get_name_list(test_data)

            # 添加测试过程中涉及的template
            template_path = {}
            template_path["trex_workpath"] = "/opt/trex/v3.03"
            template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"

            # 创建object
            if "condition" in test_data.keys():
                for cond_key, cond_value in (test_data["condition"].items()):
                    if cond_key in manipulation_object_no_create_list:
                        continue   # 直接跳过
                    cond_status = 0
                    cond_key_out = cond_key.replace("_", " ")
                    if len(cond_value) != 0:  # 不为空
                        cond_data = cond_value
                        create_ip = CreateObject(driver)
                        for i in range(len(cond_data)):  # 遍历创建所有condition
                            if cond_key == "protocol_filed":
                                tmp_key = cond_data[i]["object_type"]
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
                    if cond_status == 1:   # 创建失败，退出遍历创建
                        break

            # 创建profile
            prfi_code = 200
            if "action_parameter" in test_data.keys():
                for prfi_key, prfi_value in(test_data["action_parameter"]).items():
                    if prfi_key in manipulation_profile_no_create_list:
                        continue  # 直接跳过
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
                                ui_result = "Fail to create {} profile.".format(prfi_key_out)
                                prfi_status = 1
                                break
                    if prfi_status == 1:  # 创建失败，退出遍历创建
                        break

            # 创建rule
            if cond_code == 200 and prfi_code == 200:
                create_rule = CreateRule(driver)
                element_position_map = get_element_position(test_data["policy_type"])
                # 添加deny quic 和 intercept
                tmp_name_list = create_pre_policy(test_data, driver)
                for tmp in tmp_name_list:
                    self.ui_name_list.insert(0, copy.deepcopy(tmp))
                create_rule_code = create_rule.create(test_data, element_position_map)
                if create_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create manipulation rule successfully.", flush=True)
                elif create_rule_code != 200:
                    ui_result = "Fail to create manipulation rule."

            # 触发流量验证
            if create_rule_code == 200:
                search_rule = SearchRule(driver)
                element_position_map = get_element_position(test_data["policy_type"])
                search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], element_position_map)
                if search_rule_code == 200:
                    test_data["rule_id"] = rule_id
                    verify = Verification()
                    verification_result = verify.verification(driver, parameter, test_data, [], element_position_map)
                    if len(verification_result) == 4:
                        driver = verification_result[3]
                    elif len(verification_result) == 5:
                        driver = verification_result[4]
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Traffic verification failed", flush=True)

            # 分析验证结果，并返回给flask
            if len(verification_result) != 0:
                analysis = AnalysisResult()
                ui_result = analysis.analysis_result(test_data, [], verification_result)

            # 删除rule
            if create_rule_code == 200:
                # 删除提前先发的security intercept策略
                delete_pre_policy(tmp_name_list, driver)
                search_rule = SearchRule(driver)
                element_position_map = get_element_position(test_data["policy_type"])
                search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], element_position_map)
                if search_rule_code == 200:
                    delete_rule = DeleteRule(driver)
                    delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                    if delete_rule_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete manipulation rule successfully.", flush=True)
                    elif delete_rule_code != 200:
                        ui_result = ui_result + " In addition, fail to delete {} rule.".format(test_data["policy_type"])
                else:
                    ui_result = ui_result + " In addition, fail to search {} rule.".format(test_data["policy_type"])

            # 删除object
            if delete_rule_code == 200 and "condition" in test_data.keys():
                # 删除
                for cond_key, cond_value in (test_data["condition"].items()):  # 遍历所有cond数据
                    if cond_key in manipulation_object_no_create_list:
                        continue  # 直接跳过
                    cond_status = 0
                    cond_key_out = cond_key.replace("_", " ")
                    if len(cond_value) != 0:  # 不为空
                        cond_data = cond_value
                        for i in range(len(cond_data)):  # 遍历查询所有condition
                            search_cond = SearchObject(driver)
                            if cond_key == "protocol_filed":
                                tmp_key = cond_data[i]["object_type"]
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
                                    ui_result = ui_result + " In addition, fail to delete {} profile.".format(prfi_key_out)
                                    break
                            else:
                                ui_result = ui_result + " In addition, fail to search {} profile.".format(prfi_key_out)
                                break
                            # 退出遍历标志
                            if prfi_status == 1:  # 失败，退出遍历创建
                                break
                    # 退出遍历标志
                    if prfi_status == 1:  # 失败，退出遍历创建
                        break
                    
            result["ui_result"] = ui_result
            
        if parameter["script_type"] == "api" or need_initialization == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)

            parameter["script_type"] = "api"

            self.api_name_list = []

            # 添加测试过程中涉及的template
            template_path = {}
            template_path["rule_template"] = parameter["path"] + "/template/rule_template.json"
            template_path["object_template"] = parameter["path"] + "/template/object_template.json"
            template_path["pre_intercept_template_path"] = parameter["path"] + "/template/pre_intercept_template.json"
            # 添加测试过程中涉及的response pages
            template_path["profiles_hijack_file_path"] = parameter["path"] + "/profile_used_to_create_rule/Create-Hijack-Files-test-3.html"

            # 创建Object、Profile、Rule
            create = CreatePolicy()
            cfg_list = create.create_policy(parameter, test_data, template_path)

            # 流量验证
            verify = Verification()
            verification_result = verify.verification("", parameter, test_data, cfg_list, "")

            # 分析验证结果，并返回给flask
            analysis = AnalysisResult()
            result = analysis.analysis_result(test_data, cfg_list, verification_result)

            # 删除配置
            delete = DeletePolicy()
            delete.delele_policy_by_cfg(token, parameter, cfg_list)

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