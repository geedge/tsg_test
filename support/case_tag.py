# -*- coding: utf-8 -*-
import os
import configparser
from pathlib import Path

class CaseTag:
    def case_statistic_info(self, policy_rule, protocol, action, sub_action, script_type):
        # security_api_number, monitor_api_number, statistics_api_number, intercept_api_number, manipulation_api_number, sc_api_number= 0, 0, 0, 0, 0, 0
        security_number, monitor_number, statistics_number, intercept_number, manipulation_number, sc_number= 0, 0, 0, 0, 0, 0
        
        parse = configparser.ConfigParser()
        parse_dir = os.path.join("configuration_file.ini")
        parse.read(parse_dir, encoding="utf-8")
        
        if policy_rule == "" or "security" in policy_rule or "sec" in policy_rule:
            security_ui_path = parse.get("root_path", "path") + "/tests/security"
            if Path(security_ui_path).exists():
                security_case_name_list = os.listdir(security_ui_path)
                security_number = self.extract_data(security_case_name_list, protocol, action, sub_action)
        
        if policy_rule == "" or "monitor" in policy_rule or "monit" in policy_rule:
            monitor_ui_path = parse.get("root_path", "path") + "/tests/monitor"
            if Path(monitor_ui_path).exists():
                monitor_case_name_list = os.listdir(monitor_ui_path)
                monitor_number = self.extract_data(monitor_case_name_list, protocol, action, sub_action)
        
        if policy_rule == "" or "intercept" in policy_rule or "ic" in policy_rule:
            intercept_ui_path = parse.get("root_path", "path") + "/tests/intercept"
            if Path(intercept_ui_path).exists():
                intercept_case_name_list = os.listdir(intercept_ui_path)
                intercept_number = self.extract_data(intercept_case_name_list, protocol, action, sub_action)
        
        if policy_rule == "" or "manipulation" in policy_rule or "man" in policy_rule:
            manipulation_ui_path = parse.get("root_path", "path") + "/tests/manipulation"
            if Path(manipulation_ui_path).exists():
                manipulation_case_name_list = os.listdir(manipulation_ui_path)
                manipulation_number = self.extract_data(manipulation_case_name_list, protocol, action, sub_action)
        
        if policy_rule == "" or "service_chaining" in policy_rule or "sc" in policy_rule:
            sc_ui_path = parse.get("root_path", "path") + "/tests/service_chaining"
            if Path(sc_ui_path).exists():
                sc_case_name_list = os.listdir(sc_ui_path)
                sc_number = self.extract_data(sc_case_name_list, protocol, action, sub_action)
        
        if policy_rule == "" or "statistics" in policy_rule or "stats" in policy_rule:
            statistics_ui_path = parse.get("root_path", "path") + "/tests/statistics"
            if Path(statistics_ui_path).exists():
                statistics_case_name_list = os.listdir(statistics_ui_path)
                statistics_number = self.extract_data(statistics_case_name_list, protocol, action, sub_action)
        
        total_number = security_number + monitor_number + statistics_number + intercept_number + manipulation_number + sc_number
        result_list = []
        if len(policy_rule) == 0 and len(protocol) == 0:
            result_list.append("The total number in all policy rule is: {}".format(total_number))
            result_list.append("The script number of security case is: {}".format(security_number))
            result_list.append("The script number of monitor case is: {}".format(monitor_number))
            result_list.append("The script number of statistics case is: {}".format(statistics_number))
            result_list.append("The script number of intercept case is: {}".format(intercept_number))
            result_list.append("The script number of manipulation case is: {}".format(manipulation_number))
            result_list.append("The script number of service chaining case is: {}".format(sc_number))
        elif len(policy_rule) != 0 and len(protocol) == 0:
            temp_policy_rule = ""
            temp = policy_rule.split(",")
            if len(temp) > 1:
                temp_policy_rule = ",".join(temp[:-1]) + " and " + temp[-1]
            else:
                temp_policy_rule = policy_rule
            if temp_policy_rule == "sec":
                temp_policy_rule = "security"
            elif temp_policy_rule == "monit":
                temp_policy_rule = "monitor"
            elif temp_policy_rule == "ic":
                temp_policy_rule = "intercept"
            elif temp_policy_rule == "man":
                temp_policy_rule = "manipulation"
            elif temp_policy_rule == "sc":
                temp_policy_rule = "service chaining"
            result_list.append("The total number in {} policy rule is: {}".format(temp_policy_rule, total_number))
            # if "security" in policy_rule:
            #     result_list.append("The script number of security case is: {}".format(security_number))
            # if "monitor" in policy_rule:
            #     result_list.append("The script number of monitor case is: {}".format(monitor_number))
            # if "statistics" in policy_rule:
            #     result_list.append("The script number of statistics case is: {}".format(statistics_number))
            # if "intercept" in policy_rule:
            #     result_list.append("The script number of intercept case is: {}".format(intercept_number))
            # if "manipulation" in policy_rule or "man" in policy_rule:
            #     result_list.append("The script number of manipulation case is: {}".format(manipulation_number))
            # if "service chaining" in policy_rule:
            #     result_list.append("The script number of service chaining case is: {}".format(sc_number))
        elif len(policy_rule) != 0 and len(protocol) != 0:
            temp_policy_rule = ""
            temp = policy_rule.split(",")
            if len(temp) > 1:
                temp_policy_rule = ",".join(temp[:-1]) + " and " + temp[-1]
            else:
                temp_policy_rule = policy_rule
            if temp_policy_rule == "sec":
                temp_policy_rule = "security"
            elif temp_policy_rule == "monit":
                temp_policy_rule = "monitor"
            elif temp_policy_rule == "ic":
                temp_policy_rule = "intercept"
            elif temp_policy_rule == "man":
                temp_policy_rule = "manipulation"
            elif temp_policy_rule == "sc":
                temp_policy_rule = "service chaining"
            result_list.append("The total number of {} protocol in {} policy rule is: {}".format(protocol, temp_policy_rule, total_number))
            # if "security" in policy_rule:
            #     result_list.append("The {} protocol script number of security case is: {}".format(protocol, security_number))
            # if "monitor" in policy_rule:
            #     result_list.append("The {} protocol script number of monitor case is: {}".format(protocol, monitor_number))
            # if "statistics" in policy_rule:
            #     result_list.append("The {} protocol script number of statistics case is: {}".format(protocol, statistics_number))
            # if "intercept" in policy_rule:
            #     result_list.append("The {} protocol script number of intercept case is: {}".format(protocol, intercept_number))
            # if "manipulation" in policy_rule or "man" in policy_rule:
            #     result_list.append("The {} protocol script number of manipulation case is: {}".format(protocol, manipulation_number))
            # if "service chaining" in policy_rule:
            #     result_list.append("The {} protocol script number of service chaining case is: {}".format(protocol, sc_number))
        elif len(policy_rule) == 0 and len(protocol) != 0:
            result_list.append("The total number of {} protocol in all policy rule is: {}".format(protocol, total_number))
            result_list.append("The {} protocol script number of security case is: {}".format(protocol, security_number))
            result_list.append("The {} protocol script number of monitor case is: {}".format(protocol, monitor_number))
            result_list.append("The {} protocol script number of statistics case is: {}".format(protocol, statistics_number))
            result_list.append("The {} protocol script number of intercept case is: {}".format(protocol, intercept_number))
            result_list.append("The {} protocol script number of manipulation case is: {}".format(protocol, manipulation_number))
            result_list.append("The {} protocol script number of service chaining case is: {}".format(protocol, sc_number))
        # print(result_list)
        return result_list
        
    def extract_data(self, case_name_list, protocol, action, sub_action):
        if "__init__.py" in case_name_list:
            case_name_list.remove("__init__.py")
        if "__pycache__" in case_name_list:
            case_name_list.remove("__pycache__")
        # temp = 0
        # if len(protocol) == 0:
        #     temp = len(case_name_list)
        # else:
        #     for i in range(len(case_name_list)):
        #         if protocol in case_name_list[i]:
        #             temp+=1
        str_list = []
        if len(protocol) != 0:
            str_list.append(protocol)
        # 针对no intercept的情况
        if len(action) != 0:
            if "_" in action:
                sub_action_front = action.split("_")[0]
                sub_action_after = action.split("_")[1]
                str_list.append(sub_action_front)
                str_list.append(sub_action_after)
            else:
                str_list.append(action)
        # 针对manipulation action的情况
        if len(sub_action) != 0:
            if "_" in sub_action:
                sub_action_front = sub_action.split("_")[0]
                sub_action_after = sub_action.split("_")[1]
                str_list.append(sub_action_front)
                str_list.append(sub_action_after)
            else:
                str_list.append(sub_action)
        temp = 0
        for i in range(len(case_name_list)):
            case_name = case_name_list[i].split(".")[0]
            case_name_temp_list = case_name.split("_")
            set1 = set(str_list)
            set2 = set(case_name_temp_list)
            bool = not set1.difference(set2)
            if bool == True:
                temp+=1
        return temp
        
if __name__ == '__main__':
    case_tag = CaseTag()
    # policy_rule和script_type中字符串可以有多个，用逗号隔开；protocol中字符串只能有一个协议
    policy_rule = "man"
    protocol = "http"
    action = "allow"
    sub_action = ""
    script_type = "ui"
    case_tag.case_statistic_info(policy_rule, protocol, action, sub_action, script_type)