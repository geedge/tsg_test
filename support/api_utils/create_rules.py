# -*- coding: UTF-8 -*-
import json
import requests
from datetime import datetime
from support.api_utils.get_application_id import get_group_id

class CreateRules:
    def __init__(self, parameter, headers, object_uuids_tuple, library_uuids_tuple, profile_uuids_tuple):
        self.parameter = parameter
        self.headers = headers
        self.object_uuids_tuple = object_uuids_tuple
        if len(library_uuids_tuple) > 0:
            self.library_uuids_tuple = library_uuids_tuple
        if len(profile_uuids_tuple) > 0:
            self.profile_uuids_tuple = profile_uuids_tuple
    
    def create_rules(self, policy_configuration):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        root_path = self.parameter["root_path"]
        try:
            self.policy_configuration = policy_configuration
            object_uuids_list = list(self.object_uuids_tuple)
            rule_template = root_path + "/support/api_utils/template/rule_template.json"
            with open(rule_template, 'r', encoding='utf-8') as f:
                rule_template_json = json.load(f)
            rule_uuids_list = []
            rule_template_json["vsys"] = vsys
            rule_template_json["return_data"] = 1
            rule_template_json["rule"]["name"] = policy_configuration["name"]
            rule_template_json["rule"]["type"] = policy_configuration["type"]
            rule_template_json["rule"]["action"] = policy_configuration["action"]
            rule_template_json["rule"]["log_event"] = policy_configuration["log_event"]
            rule_template_json["rule"]["log_option"] = policy_configuration["log_option"]
            # rule_template_json["rule"]["do_log"] = 2
            rule_template_json["rule"]["is_enabled"] = policy_configuration["is_enabled"]
            source_condition_temp_list, destination_condition_temp_list, application_condition_temp_list = [], [], []
            for i in range(len(policy_configuration["and_conditions"])):
                if "attr_source" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    source_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_destination" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    destination_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_app" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    application_condition_temp_list.append(policy_configuration["and_conditions"][i])
            rule_template_json["rule"]["and_conditions"] = []
            if len(source_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(api_server, source_condition_temp_list, object_uuids_list, "attr_source"))
            if len(destination_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(api_server, destination_condition_temp_list, object_uuids_list, "attr_destination"))
            if len(application_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(api_server, application_condition_temp_list, object_uuids_list, "attr_app"))
            if len(policy_configuration["action_parameter"]) > 0:
                if policy_configuration["type"] == "security" and policy_configuration["action"] == "deny":
                    rule_template_json["rule"]["action_parameter"]["sub_action"] = policy_configuration["action_parameter"]["sub_action"]
                    rule_template_json["rule"]["action_parameter"]["packet_capture"] = {}
                    rule_template_json["rule"]["action_parameter"]["packet_capture"]["enable"] = policy_configuration["action_parameter"]["packet_capture"]["enable"]
                    rule_template_json["rule"]["action_parameter"]["after_n_packets"] = policy_configuration["action_parameter"]["after_n_packets"]
                    rule_template_json["rule"]["action_parameter"]["send_icmp_unreachable"] = policy_configuration["action_parameter"]["send_icmp_unreachable"]
                    rule_template_json["rule"]["action_parameter"]["send_tcp_reset"] = policy_configuration["action_parameter"]["send_tcp_reset"]
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
            url = api_server + "/v1/policies/{}".format(rule_type_dict[policy_configuration["type"]])
            response = requests.post(url, headers=self.headers, json=rule_template_json, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(policy_configuration["type"].replace("_", " ")), flush=True)
                response_dict = json.loads(response.text)
                uuid = self.get_uuids(response_dict, policy_configuration["type"])
                rule_uuids_temp_dict = {}
                rule_uuids_temp_dict["type"] = policy_configuration["type"]
                rule_uuids_temp_dict["uuid"] = uuid
                rule_uuids_temp_dict["name"] = policy_configuration["name"]
                rule_uuids_temp_dict["attribute_name"] = policy_configuration["type"].upper() + "_" + "RULE"
                rule_uuids_list.append(rule_uuids_temp_dict)
                rule_uuids_tuple = tuple(rule_uuids_list)
                return rule_uuids_tuple, ""
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule failed.".format(policy_configuration["type"].replace("_", " ")), flush=True)
                return "", "Create {} rule failed.".format(policy_configuration["type"].replace("_", " "))
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating rule, the exception error: ", str(e), flush=True)
            return "", "When creating rule, the exception error: " + str(e)
        
    def generate_rule_condition_list(self, api_server, and_condition, object_uuids_list, condition_type):
        if condition_type in ["attr_source", "attr_destination"]:
            condition_list = []
            for i in range(len(and_condition)):
                negate_option = and_condition[i]["negate_option"]
                objects_configuration = and_condition[i]["or_conditions"]
                object_list = []
                object_uuids_temp_list = []
                for j in range(len(objects_configuration)):
                    for t in range(len(object_uuids_list)):
                        if objects_configuration[j]["name"] == object_uuids_list[t]["name"]:
                            object_uuids_temp_list.append(object_uuids_list[t]["uuid"])
                attribute_name = objects_configuration[0]["attribute_name"]
                object_temp_dict = dict(attribute_name=attribute_name, object_uuids=object_uuids_temp_list)
                object_list.append(object_temp_dict)
                temp_dict = dict(negate_option=negate_option, or_conditions=object_list)
                condition_list.append(temp_dict)
            return condition_list
        if condition_type == "attr_app":
            application_list = []
            negate_option = and_condition[0]["negate_option"]
            application_name_list = []
            application_uuid_list = []
            application_configuration = and_condition[0]["or_conditions"]
            for i in range(len(application_configuration)):
                application_name = application_configuration[i]["items"]
                application_uuid_temp_list = []
                for j in range(len(application_name)):
                    application_name_list.append(application_name[j])
                    application_uuid = get_group_id(str(application_name_list), api_server)
                    application_uuid_temp_list.append(application_uuid)
                attribute_name = application_configuration[i]["attribute_name"]
                application_uuid_dict = dict(attribute_name=attribute_name, object_uuids=application_uuid_temp_list[len(application_uuid_temp_list)-1])
                application_uuid_list.append(application_uuid_dict)
            application_dict = dict(negate_option=negate_option, or_conditions=application_uuid_list)
            application_list.append(application_dict)
            return application_list
        
    def get_uuids(self, response_dict, type):
        if type == "security":
            uuid = response_dict["data"]["rule"]["uuid"]
            return uuid