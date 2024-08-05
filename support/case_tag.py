# -*- coding: utf-8 -*-
import os
import configparser
from pathlib import Path 

class CaseTag:
    def case_tag(self, policy_rule, protocol, action, sub_action, script_type):
        print("=====================Start statistic=====================")
        security_api_number, monitor_api_number, statistics_api_number, intercept_api_number, manipulation_api_number, sc_api_number= 0, 0, 0, 0, 0, 0
        security_ui_number, monitor_ui_number, statistics_ui_number, intercept_ui_number, manipulation_ui_number, sc_ui_number= 0, 0, 0, 0, 0, 0
        
        parse = configparser.ConfigParser()
        parse_dir = os.path.join("configuration_file.ini")
        parse.read(parse_dir, encoding="utf-8")
        
        if script_type == "" or "api" in script_type:
            if policy_rule == "" or "security" in policy_rule:
                security_api_path = parse.get("root_path", "path") + "/tests/api/security"
                if Path(security_api_path).exists():
                    security_api_case_name_list = os.listdir(security_api_path)
                    security_api_number = self.extract_data(security_api_case_name_list, protocol)
            
            if policy_rule == "" or "monitor" in policy_rule:
                monitor_api_path = parse.get("root_path", "path") + "/tests/api/monitor"
                if Path(monitor_api_path).exists():
                    monitor_api_case_name_list = os.listdir(monitor_api_path)
                    monitor_api_number = self.extract_data(monitor_api_case_name_list, protocol)
            
            if policy_rule == "" or "intercept" in policy_rule:
                intercept_api_path = parse.get("root_path", "path") + "/tests/api/intercept"
                if Path(intercept_api_path).exists():
                    intercept_api_case_name_list = os.listdir(intercept_api_path)
                    intercept_api_number = self.extract_data(intercept_api_case_name_list, protocol)
            
            if policy_rule == "" or "manipulation" in policy_rule:
                manipulation_api_path = parse.get("root_path", "path") + "/tests/api/manipulation"
                if Path(manipulation_api_path).exists():
                    manipulation_api_case_name_list = os.listdir(manipulation_api_path)
                    manipulation_api_number = self.extract_data(manipulation_api_case_name_list, protocol)
            
            if policy_rule == "" or "service_chaining" in policy_rule:
                sc_api_path = parse.get("root_path", "path") + "/tests/api/service_chaining"
                if Path(sc_api_path).exists():
                    sc_api_case_name_list = os.listdir(sc_api_path)
                    sc_api_number = self.extract_data(sc_api_case_name_list, protocol)
            
            if policy_rule == "" or "statistics" in policy_rule:
                statistics_api_path = parse.get("root_path", "path") + "/tests/api/statistics"
                if Path(statistics_api_path).exists():
                    statistics_api_case_name_list = os.listdir(statistics_api_path)
                    statistics_api_number = self.extract_data(statistics_api_case_name_list, protocol)
        
        if script_type == "" or "ui" in script_type:
            if policy_rule == "" or "security" in policy_rule:
                security_ui_path = parse.get("root_path", "path") + "/tests/ui/security"
                if Path(security_ui_path).exists():
                    security_ui_case_name_list = os.listdir(security_ui_path)
                    security_ui_number = self.extract_data(security_ui_case_name_list, protocol)
            
            if policy_rule == "" or "monitor" in policy_rule:
                monitor_ui_path = parse.get("root_path", "path") + "/tests/ui/monitor"
                if Path(monitor_ui_path).exists():
                    monitor_ui_case_name_list = os.listdir(monitor_ui_path)
                    monitor_ui_number = self.extract_data(monitor_ui_case_name_list, protocol)
            
            if policy_rule == "" or "intercept" in policy_rule:
                intercept_ui_path = parse.get("root_path", "path") + "/tests/ui/intercept"
                if Path(intercept_ui_path).exists():
                    intercept_ui_case_name_list = os.listdir(intercept_ui_path)
                    intercept_ui_number = self.extract_data(intercept_ui_case_name_list, protocol)
            
            if policy_rule == "" or "manipulation" in policy_rule:
                manipulation_ui_path = parse.get("root_path", "path") + "/tests/ui/manipulation"
                if Path(manipulation_ui_path).exists():
                    manipulation_ui_case_name_list = os.listdir(manipulation_ui_path)
                    manipulation_ui_number = self.extract_data(manipulation_ui_case_name_list, protocol)
            
            if policy_rule == "" or "service_chaining" in policy_rule:
                sc_ui_path = parse.get("root_path", "path") + "/tests/ui/service_chaining"
                if Path(sc_ui_path).exists():
                    sc_ui_case_name_list = os.listdir(sc_ui_path)
                    sc_ui_number = self.extract_data(sc_ui_case_name_list, protocol)
            
            if policy_rule == "" or "statistics" in policy_rule:
                statistics_ui_path = parse.get("root_path", "path") + "/tests/ui/statistics"
                if Path(statistics_ui_path).exists():
                    statistics_ui_case_name_list = os.listdir(statistics_ui_path)
                    statistics_ui_number = self.extract_data(statistics_ui_case_name_list, protocol)
        
        api_number = security_api_number + monitor_api_number + statistics_api_number + intercept_api_number + manipulation_api_number + sc_api_number
        ui_number = security_ui_number + monitor_ui_number + statistics_ui_number + intercept_ui_number + manipulation_ui_number + sc_ui_number
        total_number = api_number + ui_number
        if len(policy_rule) == 0 and len(protocol) == 0:
            print("The total number in all policy rule is {}".format(total_number))
            print("The api total number in all policy rule is {}".format(api_number))
            print("The ui total number in all policy rule is {}".format(ui_number))
            print("The script number of security api case is {}".format(security_api_number))
            print("The script number of monitor api case is {}".format(monitor_api_number))
            print("The script number of statistics api case is {}".format(statistics_api_number))
            print("The script number of intercept api case is {}".format(intercept_api_number))
            print("The script number of manipulation api case is {}".format(manipulation_api_number))
            print("The script number of service chaining api case is {}".format(sc_api_number))
            print("The script number of security ui case is {}".format(security_ui_number))
            print("The script number of monitor ui case is {}".format(monitor_ui_number))
            print("The script number of statistics ui case is {}".format(statistics_ui_number))
            print("The script number of intercept ui case is {}".format(intercept_ui_number))
            print("The script number of manipulation ui case is {}".format(manipulation_ui_number))
            print("The script number of service chaining ui case is {}".format(sc_ui_number))
        elif len(policy_rule) != 0 and len(protocol) == 0:
            temp_policy_rule = ""
            temp = policy_rule.split(",")
            if len(temp) > 1:
                temp_policy_rule = ",".join(temp[:-1]) + " and " + temp[-1]
            else:
                temp_policy_rule = policy_rule
            print("The total number in {} policy rule is {}".format(temp_policy_rule, total_number))
            print("The api total number in {} policy rule is {}".format(temp_policy_rule, api_number))
            print("The ui total number in {} policy rule is {}".format(temp_policy_rule, ui_number))
            if "security" in policy_rule:
                print("The script number of security api case is {}".format(security_api_number))
            if "monitor" in policy_rule:
                print("The script number of monitor api case is {}".format(monitor_api_number))
            if "statistics" in policy_rule:
                print("The script number of statistics api case is {}".format(statistics_api_number))
            if "intercept" in policy_rule:
                print("The script number of intercept api case is {}".format(intercept_api_number))
            if "manipulation" in policy_rule:
                print("The script number of manipulation api case is {}".format(manipulation_api_number))
            if "service chaining" in policy_rule:
                print("The script number of service chaining api case is {}".format(sc_api_number))
            if "security" in policy_rule:
                print("The script number of security ui case is {}".format(security_ui_number))
            if "monitor" in policy_rule:
                print("The script number of monitor ui case is {}".format(monitor_ui_number))
            if "statistics" in policy_rule:
                print("The script number of statistics ui case is {}".format(statistics_ui_number))
            if "intercept" in policy_rule:
                print("The script number of intercept ui case is {}".format(intercept_ui_number))
            if "manipulation" in policy_rule:
                print("The script number of manipulation ui case is {}".format(manipulation_ui_number))
            if "service chaining" in policy_rule:
                print("The script number of service chaining ui case is {}".format(sc_ui_number))
        elif len(policy_rule) != 0 and len(protocol) != 0:
            temp_policy_rule = ""
            temp = policy_rule.split(",")
            if len(temp) > 1:
                temp_policy_rule = ",".join(temp[:-1]) + " and " + temp[-1]
            else:
                temp_policy_rule = policy_rule
            print("The total number of {} protocol in {} policy rule is {}".format(protocol, temp_policy_rule, total_number))
            print("The api total number of {} protocol in {} policy rule is {}".format(protocol, temp_policy_rule, api_number))
            print("The ui total number of {} protocol in {} policy rule is {}".format(protocol, temp_policy_rule, ui_number))
            if "security" in policy_rule:
                print("The {} protocol script number of security api case is {}".format(protocol, security_api_number))
            if "monitor" in policy_rule:
                print("The {} protocol script number of monitor api case is {}".format(protocol, monitor_api_number))
            if "statistics" in policy_rule:
                print("The {} protocol script number of statistics api case is {}".format(protocol, statistics_api_number))
            if "intercept" in policy_rule:
                print("The {} protocol script number of intercept api case is {}".format(protocol, intercept_api_number))
            if "manipulation" in policy_rule:
                print("The {} protocol script number of manipulation api case is {}".format(protocol, manipulation_api_number))
            if "service chaining" in policy_rule:
                print("The {} protocol script number of service chaining api case is {}".format(protocol, sc_api_number))
            if "security" in policy_rule:
                print("The {} protocol script number of security ui case is {}".format(protocol, security_ui_number))
            if "monitor" in policy_rule:
                print("The {} protocol script number of monitor ui case is {}".format(protocol, monitor_ui_number))
            if "statistics" in policy_rule:
                print("The {} protocol script number of statistics ui case is {}".format(protocol, statistics_ui_number))
            if "intercept" in policy_rule:
                print("The {} protocol script number of intercept ui case is {}".format(protocol, intercept_ui_number))
            if "manipulation" in policy_rule:
                print("The {} protocol script number of manipulation ui case is {}".format(protocol, manipulation_ui_number))
            if "service chaining" in policy_rule:
                print("The {} protocol script number of service chaining ui case is {}".format(protocol, sc_ui_number))
        elif len(policy_rule) == 0 and len(protocol) != 0:
            print("The total number of {} protocol in all policy rule is {}".format(protocol, total_number))
            print("The api total number of {} protocol in all policy rule is {}".format(protocol, api_number))
            print("The ui total number of {} protocol in all policy rule is {}".format(protocol, ui_number))
            print("The {} protocol script number of security api case is {}".format(protocol, security_api_number))
            print("The {} protocol script number of monitor api case is {}".format(protocol, monitor_api_number))
            print("The {} protocol script number of statistics api case is {}".format(protocol, statistics_api_number))
            print("The {} protocol script number of intercept api case is {}".format(protocol, intercept_api_number))
            print("The {} protocol script number of manipulation api case is {}".format(protocol, manipulation_api_number))
            print("The {} protocol script number of service chaining api case is {}".format(protocol, sc_api_number))
            print("The {} protocol script number of security ui case is {}".format(protocol, security_ui_number))
            print("The {} protocol script number of monitor ui case is {}".format(protocol, monitor_ui_number))
            print("The {} protocol script number of statistics ui case is {}".format(protocol, statistics_ui_number))
            print("The {} protocol script number of intercept ui case is {}".format(protocol, intercept_ui_number))
            print("The {} protocol script number of manipulation ui case is {}".format(protocol, manipulation_ui_number))
            print("The {} protocol script number of service chaining ui case is {}".format(protocol, sc_ui_number))
        print("=====================End statistic=======================")
        
    def extract_data(self, case_name_list, protocol):
        if "__init__.py" in case_name_list:
            case_name_list.remove("__init__.py")
        if "__pycache__" in case_name_list:
            case_name_list.remove("__pycache__")
        temp = 0
        if len(protocol) == 0:
            temp = len(case_name_list)
        else:
            for i in range(len(case_name_list)):
                if protocol in case_name_list[i]:
                    temp+=1
        return temp
        
if __name__ == '__main__':
    print("Start test")
    statistics = CaseTag()
    # policy_rule和script_type中字符串可以有多个，用逗号隔开；protocol中字符串只能有一个协议
    # policy_rule = ""
    # protocol = ""
    # script_type = ""
    # statistics.case_tag(policy_rule, protocol, script_type)
    
    # policy_rule = "security,monitor"
    # protocol = ""
    # script_type = ""
    # statistics.case_tag(policy_rule, protocol, script_type)
    
    # policy_rule = "security,monitor"
    # protocol = "http"
    # script_type = ""
    # statistics.case_tag(policy_rule, protocol, script_type)
    
    # policy_rule = "security"
    # protocol = "http"
    # script_type = ""
    # statistics.case_tag(policy_rule, protocol, script_type)
    
    # policy_rule = "security,monitor"
    # protocol = "http"
    # script_type = "ui,api"
    # statistics.case_tag(policy_rule, protocol, script_type)
    
    # policy_rule = "security,monitor"
    # protocol = "http"
    # script_type = "ui"
    # statistics.case_tag(policy_rule, protocol, script_type)
    
    # policy_rule = "security,monitor"
    # protocol = ""
    # script_type = "api"
    # statistics.case_tag(policy_rule, protocol, script_type)
    
    policy_rule = ""
    protocol = "http"
    action = ""
    sub_action = ""
    script_type = ""
    statistics.case_tag(policy_rule, protocol, action, sub_action, script_type)
    print("End test")