# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.api_utils.log_in import LogIn
# from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.delete_rules import DeleteRules
from support.ui_utils.object.search_objects import SearchObject
from support.ui_utils.object.delete_objects import DeleteObject
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime

class DeleteSecurityRulesExample:
    def delete_rules(self, parameter, policy_configuration, driver, rule_uuids_tuple):
        try:
            result = ""
            
            # 删除rule
            search_rule = SearchRule(driver)
            element_position_map = get_element_position(policy_configuration["type"])
            search_rule_code, first_row_checkbox_element = search_rule.search(policy_configuration["type"], policy_configuration["type"], element_position_map)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(element_position_map, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete monitor rule successfully.", flush=True)
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete {} rule.".format(policy_configuration["type"])
            else:
                result = result + " In addition, fail to search {} rule.".format(policy_configuration["type"])
            
            # 删除object
            if delete_rule_code == 200 and "condition" in policy_configuration["type"].keys():
                # 删除
                for cond_key, cond_value in (policy_configuration["policy_configuration"]["condition"].items()):  # 遍历所有cond数据
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
                                    result = result + " In addition, fail to delete {} object.".format(cond_key_out)
                                    break
                            else:
                                result = result + " In addition, fail to search {} object.".format(cond_key_out)
                                break
                            # 退出遍历标志
                            if cond_status == 1:  # 失败，退出遍历创建
                                break
                    # 退出遍历标志
                    if cond_status == 1:  # 失败，退出遍历创建
                        break
            
            # 环境清理
            support.ui_utils.env.teardown()
            
            # 强制删除
            log_in = LogIn()
            pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
            token = log_in.login(parameter["username"], pwd, parameter["api_server"])
            headers = {"Content-Type": "application/json", "Authorization": token}
            rules = DeleteRules(parameter, headers)
            rules.delete_rules(rule_uuids_tuple)
            
            return result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting rule by ui, the exception error: ", str(e), flush=True)
            return "", "When deleting rule by ui, the exception error: " + str(e)