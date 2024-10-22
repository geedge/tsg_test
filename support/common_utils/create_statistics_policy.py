import os
import sys

from support.api_utils.organize_config import OrganizeConfig
from support.common_utils.data_translation import DataTranslation

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
from support.ui_utils.policy.edit_rule import EditRule
from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.create_policy import CreatePolicy
from support.packet_generator.verify import Verify
from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analyse_result import *
from support.api_utils.log_in import *
import support.ui_utils.env
from datetime import datetime
import time

class CreateStatisticsPolicy:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        ui_result = self._run(self.test_data, self.parameter)
        return ui_result

    def _run(self, test_data, parameter):
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

        # Statistics Rule使用随机IP
        organize_config = OrganizeConfig()
        test_data = organize_config.generate_random_ip(test_data, parameter)
        if "library_condition" not in test_data:
            test_data["library_condition"] = []

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

                # name_list汇总
                self.ui_name_list = get_name_list(test_data)

                # 添加测试过程中涉及的template
                #template_path = {}
                #template_path["trex_workpath"] = "/opt/trex/v3.03"
                #template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"
                """"""
                # 创建object
                if "condition" in test_data.keys():
                    for cond_key, cond_value in (test_data["condition"].items()):
                        if cond_key in manipulation_object_no_create_list:
                            continue   # 直接跳过
                        cond_status = 0
                        #cond_key_out = cond_key.replace("_", " ")
                        if len(cond_value) != 0:  # 不为空
                            cond_data = cond_value
                            create_ip = support.ui_utils.object.create_object.CreateObject(driver)
                            for i in range(len(cond_data)):  # 遍历创建所有condition
                                if "item" in cond_data[i].keys() and cond_data[i]["item"] == []:  # UDP协议为UDP时，Client IP和Server IP不能确定，故会把Client IP和Server IP在系统添加1次，在Rule添加2次添加到Source IP和Destination，
                                    continue  # 遍历创建所有condition
                                tem_key = ""
                                if cond_key == "protocol_filed":
                                    tmp_key = cond_data[i]["object_type"]
                                    #cond_key_out = tmp_key.replace("_", " ")
                                    if tmp_key == "boolean":
                                        continue
                                    else:
                                        element_position_map = get_element_position(tmp_key)
                                else:
                                    element_position_map = get_element_position(cond_key)
                                cond_code = create_ip.create(cond_data[i], element_position_map)
                                if cond_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {}{} object successfully.".format(cond_key, tem_key), flush=True)
                                else:
                                    ui_result = "Fail to create {}{} object.".format(cond_key, tem_key)
                                    cond_status = 1
                                    break
                        if cond_status == 1:   # 创建失败，退出遍历创建
                            break

                # 创建profile
                #cond_code = 200
                # 创建Statistics Template
                create_statistics_template_code = 0
                if cond_code == 200:
                    profile = test_data["action_parameter"]
                    statistics_templates = profile["statistics_template"]
                    for statistics_template in statistics_templates:
                        cond_status = 0
                        create_statistics_template = support.ui_utils.profile.create_profile.CreateStatisticsTemplate(driver)
                        element_position_map = get_profile_element_position("statistics_template")
                        prfi_code = create_statistics_template.create(statistics_template, element_position_map)
                        if prfi_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                                  "Create {} Profile successfully.".format("statistics_template"), flush=True)
                        else:
                            result = "Fail to create {} Profile.".format("statistics_template")
                            cond_status = 1
                            break
                        if cond_status == 1:  # 创建失败，退出遍历创建
                            break
                create_rule_code = 0
                # 创建rule
                if cond_code == 200 and prfi_code == 200:
                    create_rule = support.ui_utils.policy.create_rule.CreateRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    create_rule_code = create_rule.create(test_data, element_position_map)
                    if create_rule_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                              "Create {} rule successfully.".format(test_data["policy_type"], flush=True))
                    elif create_rule_code != 200:
                        result = "Fail to create {} rule.".format(test_data["policy_type"])

                # 触发流量验证
                if create_rule_code == 200:
                    search_rule = support.ui_utils.policy.search_rule.SearchRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], element_position_map)
                    if search_rule_code == 200:
                        test_data["rule_id"] = rule_id
                        verification = Verify()
                        verification_result = verification.verify_result(driver, parameter, test_data, [], element_position_map)
                        if len(verification_result) == 4:
                            driver = verification_result[3]
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Traffic verification failed", flush=True)

                # 分析验证结果，并返回给flask
                if len(verification_result) == 4:
                    analysis = Analyse()
                    ui_result = analysis.analyse_result(test_data["policy_type"], [], verification_result)
                    # if len(ui_result) == 0:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
                    # elif len(ui_result) != 0:
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", ui_result, flush=True)

                # 删除rule
                if create_rule_code == 200:
                    search_rule = support.ui_utils.policy.search_rule.SearchRule(driver)
                    element_position_map = get_element_position(test_data["policy_type"])
                    search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], element_position_map)
                    if search_rule_code == 200:
                        delete_rule = support.ui_utils.policy.delete_rule.DeleteRule(driver)
                        delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                        if delete_rule_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} rule successfully.".format(test_data["policy_type"]), flush=True)
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
                        #cond_key_out = cond_key.replace("_", " ")
                        if len(cond_value) != 0:  # 不为空
                            cond_data = cond_value
                            tmp_key = ""
                            for i in range(len(cond_data)):  # 遍历查询所有condition
                                if "item" in cond_data[i].keys() and cond_data[i]["item"] == []:  # UDP协议为UDP时，Client IP和Server IP不能确定，故会把Client IP和Server IP在系统添加1次，在Rule添加2次添加到Source IP和Destination，
                                    continue  # 遍历创建所有condition
                                search_cond = support.ui_utils.object.search_object.SearchObject(driver)
                                if cond_key == "protocol_filed":
                                    tmp_key = cond_data[i]["object_type"]
                                    if tmp_key == "boolean":
                                        continue
                                    else:
                                        element_position_map = get_element_position(tmp_key)
                                else:
                                    element_position_map = get_element_position(cond_key)
                                search_cond_code, first_row_checkbox_element = search_cond.search(cond_data[i]["name"], element_position_map)
                                if search_cond_code == 200:
                                    delete_cond = support.ui_utils.object.delete_object.DeleteObject(driver)
                                    delete_cond_code = delete_cond.delete(element_position_map, first_row_checkbox_element, True)
                                    if delete_cond_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {}{} object successfully.".format(cond_key, tmp_key), flush=True)
                                    else:
                                        ui_result = ui_result + " In addition, fail to delete {}{} object.".format(cond_key, tmp_key)
                                        break
                                else:
                                    ui_result = ui_result + " In addition, fail to search {}{} object.".format(cond_key, tmp_key)
                                    break
                                # 退出遍历标志
                                if cond_status == 1:  # 失败，退出遍历创建
                                    break
                        # 退出遍历标志
                        if cond_status == 1:  # 失败，退出遍历创建
                            break
                # 删除Statistics Tesmplate
                if delete_rule_code == 200 and "action_parameter" in test_data.keys():
                    for prfi_key, prfi_value in (test_data["action_parameter"].items()):  # 遍历所有cond数据
                        prfi_status = 0
                        prfi_key_out = prfi_key.replace("_", " ")
                        if len(prfi_value) != 0:  # 不为空
                            for i in range(len(prfi_value)):  # 遍历查询所有profile
                                search_prfi = SearchProfile(driver)
                                element_position_map = get_element_position(prfi_key)
                                prfi_name = prfi_value[i]["name"].strip()
                                search_prfi_code, first_row_checkbox_element = search_prfi.search(prfi_name,
                                                                                                  element_position_map)
                                if search_prfi_code == 200:
                                    delete_prfi = DeleteProfile(driver)
                                    delete_prfi_code = delete_prfi.delete(element_position_map,
                                                                          first_row_checkbox_element)
                                    if delete_prfi_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                              str(datetime.now().microsecond)[:3],
                                              "Delete {} profile successfully.".format(prfi_key_out), flush=True)
                                    else:
                                        ui_result = ui_result + " In addition, fail to delete {} profile.".format(
                                            prfi_key_out)
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
            except Exception as e:
                raise
            finally:
                # 清理环境
                result["ui_result"] = ui_result
                support.ui_utils.env.teardown()
        if parameter["script_type"] == "api" or need_initialization == True:
            try:
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "parameter(script_type:{}),test_data(rule_name:{})".format(parameter["script_type"],test_data["rule_name"]), flush=True)
                if need_initialization == True and "sub_id" in test_data["rule_name"]:
                    if "bytes" not in test_data["rule_name"] and "pkts" not in test_data["rule_name"] and "closed_sessions" not in test_data["rule_name"] and "closed_sessions" not in test_data["rule_name"]:
                        # 如果同时跑UI和API，且为SUB ID相关用例时，因SUB ID相关用例在1个Vsys仅注册了一个测试SUBID对象，所以需等待UI用例流量结束：120 seconds
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Subid related use cases need to wait until the UI traffic ends,, wait for 120 seconds", flush=True)
                        time.sleep(120)
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)
                # Statistics Rule使用随机IP
                #organize_config = OrganizeConfig()
                test_data = organize_config.generate_random_ip(test_data, parameter)
                parameter["script_type"] = "api"

                # 数据转换，适配API的test_data
                translation = DataTranslation()
                test_data = translation.data_translation(parameter, test_data)
                # print(test_data)

                self.api_name_list = get_name_list(test_data)

                # 添加测试过程中涉及的template
                template_path = {}
                template_path["rule_template"] = parameter["root_path"] + "/support/api_utils/template/rule_template.json"
                template_path["object_template"] = parameter["root_path"] + "/support/api_utils/template/object_template.json"
                template_path["profile_statistics_template"] = parameter["root_path"] + "/support/api_utils/template/profile_statistics_template.json"

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
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        if isinstance(self.api_name_list, list) and self.api_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)