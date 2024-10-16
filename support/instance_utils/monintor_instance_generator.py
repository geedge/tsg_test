# -*- coding: UTF-8 -*-
import os
import sys

from support.api_utils.organize_config import OrganizeConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.profile.create_monitor_profile import CreateMonitorProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.create_policy import CreatePolicy
from support.packet_generator.verify import Verify
from support.ui_utils.element_position.map_element_position_library import get_element_position, get_name_list
from support.ui_utils.element_position.map_element_position_library import test_monitor_profile_element_position,get_profile_element_position
from support.api_utils.analyse_result import Analyse
from support.instance_utils.data_translation import DataTranslation
import support.ui_utils.env
from datetime import datetime

import copy


class MonitorInstanceGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        ui_result = self._run(self.test_data, self.parameter)
        return ui_result

    def _run(self, test_data, parameter):
        # 声明定义数据
        ui_result, api_result = "", ""
        self.api_name_list, self.ui_name_list = [], []
        result = {
            "ui_result": "",
            "api_result": ""
        }

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token
        self.test_data["token"] = token

        #使用随机ip
        if test_data["traffic"]["type"] == "trex":
            organize_config = OrganizeConfig()
            test_data = organize_config.generate_random_ip(test_data, parameter)

        need_initialization = False
        if len(parameter["script_type"]) == 0:
            need_initialization = True

        if parameter["script_type"] == "ui" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Begin to run ui test case", flush=True)
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
                # # 构建source ip 的name list
                # if "source_ip" in test_data["condition"] and len(test_data["condition"]["source_ip"]) != 0:
                #     object_data = test_data["condition"]["source_ip"]
                #     for i in range(len(object_data)):
                #         tmp_name_dict = {}
                #         tmp_name_dict["type"] = object_data[i]['object_type']
                #         tmp_name_dict["name"] = object_data[i]['name']
                #         self.ui_name_list.append(tmp_name_dict)
                # # 构建server fqdn 的name list
                # if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
                #     object_data = test_data["condition"]["server_fqdn"]
                #     for i in range(len(object_data)):
                #         tmp_name_dict = {}
                #         tmp_name_dict["type"] = test_data["condition"]["server_fqdn"][i]['object_type']
                #         tmp_name_dict["name"] = test_data["condition"]["server_fqdn"][i]['name']
                #         self.ui_name_list.append(tmp_name_dict)
                # # 构建protocol field 的name list
                # if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
                #     object_data = test_data["condition"]["protocol_filed"]
                #     for i in range(len(object_data)):
                #         # 排除 boolean 类型的 protocol_filed
                #         if object_data[i]['object_type'] == 'boolean':
                #             continue
                #         tmp_name_dict = {}
                #         tmp_name_dict["type"] = test_data["condition"]["protocol_filed"][i]['object_type']
                #         tmp_name_dict["name"] = test_data["condition"]["protocol_filed"][i]['name']
                #         self.ui_name_list.append(tmp_name_dict)

                if "condition" in test_data.keys():
                    for cond_key, cond_value in (test_data["condition"].items()):
                        cond_status = 0
                        if cond_key == "application" or cond_key == "ip_protocol" or cond_key =="packet_capture":
                            continue  # 直接跳过
                        cond_key_out = cond_key.replace("_", " ")
                        if len(cond_value) != 0:
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
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                          "Create {} object successfully.".format(cond_key_out), flush=True)
                                else:
                                    ui_result = "Fail to create {} object.".format(cond_key_out)
                                    cond_status = 1
                                    break
                        if cond_status == 1:  # 创建失败，退出遍历创建
                            break

                # 创建profile
                prfi_code = 200
                if "profile" in test_data.keys()  and test_data["profile"] != "":
                    profile_data = test_data["profile"]
                    element_position_map = get_profile_element_position("monitor_profile")
                    create_monitor_profile = CreateMonitorProfile(driver, element_position_map)
                    for i in range(len(profile_data)):
                        create_monitor_profile_code = create_monitor_profile.create_monitor_profile(profile_data[i],
                                                                                                    test_monitor_profile_element_position,
                                                                                                    test_data[
                                                                                                        "profile"][i][
                                                                                                        "name"])
                        if create_monitor_profile_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                  "Create traffic mirroring profile successfully.", flush=True)
                        elif create_monitor_profile_code != 200:
                            ui_result = "Fail to create Traffic Mirroring Profiles profile."
                            break

                # 创建rule
                if cond_code == 200:
                    create_rule = CreateRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
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
                    search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"],
                                                                        element_position_map)
                    if search_rule_code == 200:
                        test_data["rule_id"] = rule_id
                        verification = Verify()
                        verification_result = verification.verify_result(driver, parameter, test_data, [], element_position_map)
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
                        delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                        if delete_rule_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                  "Delete monitor rule successfully.", flush=True)
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
                                search_cond_code, first_row_checkbox_element = search_cond.search(cond_data[i]["name"],
                                                                                                  element_position_map)
                                if search_cond_code == 200:
                                    delete_cond = DeleteObject(driver)
                                    delete_cond_code = delete_cond.delete(element_position_map, first_row_checkbox_element,
                                                                          True)
                                    if delete_cond_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                              str(datetime.now().microsecond)[:3],
                                              "Delete {} object successfully.".format(cond_key_out), flush=True)
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
                if delete_rule_code == 200 and "profile" in test_data.keys() and test_data["profile"] != "":
                    # 删除
                    if delete_rule_code == 200:
                        for x in range(len(profile_data)):
                            search_mirror_profile = SearchProfile(driver)
                            profile_return_code, first_row_checkbox_element = search_mirror_profile.search(
                                profile_data[x]['name'], test_monitor_profile_element_position)
                            if profile_return_code == 200:
                                delete_mirror_profile = DeleteProfile(driver)
                                delete_profile_code = delete_mirror_profile.delete(
                                    test_monitor_profile_element_position,
                                    first_row_checkbox_element, True)
                                if delete_profile_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          str(datetime.now().microsecond)[:3],
                                          "Delete monitor profile successfully.", flush=True)
                                elif delete_profile_code != 200:
                                    ui_result = ui_result + " In addition, fail to delete profile."
                                    break
                            else:
                                ui_result = ui_result + " In addition, fail to search profile."
                                break
            except Exception as e:
                raise
            finally:
                # 清理环境
                result["ui_result"] = ui_result
                support.ui_utils.env.teardown()

        if parameter["script_type"] == "api" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Begin to run api test case", flush=True)

                parameter["script_type"] = "api"

                self.api_name_list = []

                # 数据转换，适配API的test_data
                translation = DataTranslation()
                test_data = translation.data_translation(parameter, test_data)
                # temp_test_data = translation.data_translation(test_data["policy_type"], test_data)
                # test_data["obj_condition"] = temp_test_data["obj_condition"]
                # test_data["application"] = temp_test_data["application"]
                # test_data["profile_condition"] = temp_test_data["profile_condition"]

                # 添加测试过程中涉及的template
                template_path = {}
                template_path["rule_template"] = parameter["root_path"] + "/support/api_utils/template/rule_template.json"
                template_path["object_template"] = parameter["root_path"] + "/support/api_utils/template/object_template.json"
                template_path["pre_intercept_template_path"] = parameter["root_path"] + "/support/api_utils/template/pre_intercept_template.json"
                # 添加测试过程中涉及的response pages
                template_path["profiles_hijack_file_path"] = parameter[
                                                                 "root_path"] + "/support/api_utils/preset_profile/Create-Hijack-Files-test-3.html"

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
                delete.delele_policy_by_cfg(token, parameter, cfg_list)

        return result

    def clean_up(self):
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.ui_name_list != []:
            # 清理环境
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        if isinstance(self.api_name_list, list) and self.api_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)