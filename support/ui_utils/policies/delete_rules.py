# -*- coding: UTF-8 -*-
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
import json
import time
import requests
from datetime import datetime 
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.map_element_position_library import *
from support.ui_utils.policies.page_jump import PageJump

class DeleteRules:
    def __init__(self, driver):
        self.driver = driver
        
    def delete_rules(self, rule_uuids_tuple):
        try:
            time.sleep(0.3)
            rule_uuids_linst = list(rule_uuids_tuple)
            for i in range(len(rule_uuids_linst)):
                element_position_library = get_element_position(rule_uuids_linst[i]["type"])
                search_element_position = element_position_library["search"]
                deletion_element_position = element_position_library["delete"]
                page_jump_element_position = element_position_library["page_jump"]
                page_jump = PageJump(self.driver)
                page_jump.jump_sub_policy_page(page_jump_element_position)
                btn = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_posXpath"])
                self.driver.execute_script("arguments[0].click()", btn)
                self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_input_itemContent_posXpath"]).send_keys(rule_uuids_linst[i]["uuid"])
                dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLabel_dropDown_item_posXpath"].format(replaceValue="UUID")
                btn = self.driver.find_element(By.XPATH, dropdown_item_posXpath)
                self.driver.execute_script("arguments[0].click()", btn)
                self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_searchButton_posId"]).click()
                time.sleep(0.3)
                element_tr = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_tableTbody_posXpath"])
                row = element_tr.find_elements(By.XPATH, "div")
                if len(row) != 0:
                    first_row = row[0]
                    first_row_checkbox_element = first_row.find_element(By.XPATH, '//*[@inputprops="[object Object]"]')
                    first_row_checkbox_element.click()
                    time.sleep(0.3)
                    self.driver.find_element(By.XPATH, deletion_element_position["policyRuleListPage_deleteButton_posXpath"]).click()
                    self.driver.find_element(By.XPATH, deletion_element_position["policyRuleListPage_okButton_warningYes_posXpath"]).click()
                    time.sleep(2)
                    return ""
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting rule, the exception error: ", str(e), flush=True)
                    return "When deleting rule, the exception error: " + str(e)
        except Exception as e:
            raise
        
    def delete_rules_by_name(self, parameter, policy_configuration, headers):
        try:
            api_server = parameter["api_server"]
            rule_type_dict = {
                "security": "security-rules",
                "proxy_intercept": "proxy-intercept-rules",
                "proxy_manipulation": "proxy-manipulation-rules",
                "traffic_shaping": "traffic-shaping-rules",
                "service_chaining": "service-chaining-rules",
                "statistics": "statistics-rules",
                "monitor": "monitor-rules",
                "dos_protection": "dos-protection-rules",
            }
            type = policy_configuration["type"]
            url = api_server + "/v1/policies/{}".format(rule_type_dict[type])
            template = {"type": "", "name": "", "with_sub_vsys": 0, "vsys": parameter["vsys"]}
            template["name"] = policy_configuration["name"]
            template["type"] = policy_configuration["type"]
            # 如果有预置的policy rule，需要根据rule type进行判断，再删除。如执行manipulation脚本后，判断rule type决定需要删除预置intercept
            # 预置的policy rule使用固定的name和type，不需要额外判断或传参
            # 有上述需求的要额外补充逻辑？？
            response = requests.get(url, headers=headers, params=template, verify=False)
            if response.status_code != 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Search {} rule failed.".format(policy_configuration["type"]))
                return "Search {} rule failed.".format(policy_configuration["type"])
            return_json_data = json.loads(response.text)
            if "/policies" in url:
                data_list = return_json_data["data"]["list"]
                deletion_rule_type = template["type"].title() + " " + "rule"
            if len(data_list) > 0:
                deletion_uuids_list = self.combine_rules_uuid(template, data_list)
                for i in range(len(deletion_uuids_list)):
                    deletion_template = {"uuids": "", "vsys": parameter["vsys"]}
                    deletion_template["uuids"] = deletion_uuids_list[i]
                    response = requests.delete(url, headers=headers, json=deletion_template, verify=False)
                if len(deletion_uuids_list) > 0:
                    if response.status_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully by name.".format(deletion_rule_type), flush=True)
                        return ""
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed by name.".format(deletion_rule_type))
                        return "Delete {} failed by name.".format(deletion_rule_type)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting rule by name, the exception error: ", str(e), flush=True)
            return "When deleting rule by name, the exception error: " + str(e)
        
    def combine_rules_uuid(self, template, data_list):
        uuid_list = []
        for _, json_obj in enumerate(data_list):
            if template["name"] == json_obj["name"]:
                uuid = json_obj["uuid"]
                uuid_list.append(uuid)
        return uuid_list