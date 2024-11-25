# -*- coding: UTF-8 -*-
import json
import requests
from datetime import datetime

class CreateRules:
    def __init__(self, parameter, headers, object_uuids_tuple, library_uuids_tuple, profile_uuids_tuple):
        self.parameter = parameter
        self.headers = headers
        self.object_uuids_tuple = object_uuids_tuple
        self.library_uuids_tuple = library_uuids_tuple
        self.profile_uuids_tuple = profile_uuids_tuple
    
    def create_rules(self, policy_configuration):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        root_path = self.parameter["root_path"]
        try:
            self.policy_configuration = policy_configuration
            object_uuids_list = list(self.object_uuids_tuple)
            if len(self.library_uuids_tuple) > 0:
                library_uuids_list = list(self.library_uuids_tuple)
                for i in range(len(library_uuids_list)):
                    library_list = list(library_uuids_list[i])
                    for j in range(len(library_list)):
                        if library_list[j]["type"] == "tag":
                            object_uuids_list.append(library_list[j])
            rule_template = root_path + "/support/api_utils/template/rule_template.json"
            with open(rule_template, 'r', encoding='utf-8') as f:
                rule_template_json = json.load(f)
            rule_uuids_list = []
            rule_template_json["vsys"] = vsys
            rule_template_json["return_data"] = 1
            rule_template_json["rule"]["name"] = policy_configuration["name"]
            rule_template_json["rule"]["type"] = policy_configuration["type"]
            rule_template_json["rule"]["action"] = policy_configuration["action"]
            rule_template_json["rule"]["log_option"] = policy_configuration["log_option"]
            # rule_template_json["rule"]["do_log"] = 2
            rule_template_json["rule"]["is_enabled"] = policy_configuration["is_enabled"]
            source_condition_temp_list, destination_condition_temp_list, application_condition_temp_list, protocol_field_condition_temp_list = [], [], [], []
            tunnel_condition_temp_list, flag_condition_temp_list, ip_protocol_condition_list, internal_condition_temp_list, external_condition_temp_list = [], [], [], [], []
            for i in range(len(policy_configuration["and_conditions"])):
                if "attr_tunnel" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    tunnel_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_source" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                    "attr_gtp" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                    "attr_subscriber" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower()  :
                    source_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_destination" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                   "attr_server" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() :
                    destination_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_inter" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() :
                    internal_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_ext" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() :
                    external_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_flag" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    flag_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_ip" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    ip_protocol_condition_list.append(policy_configuration["and_conditions"][i])
                if "attr_app" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    application_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_http" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                    "attr_ssl" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                    "attr_mail" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                    "attr_dns" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                    "attr_ftp" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower() or \
                    "attr_sip" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    protocol_field_condition_temp_list.append(policy_configuration["and_conditions"][i])
            rule_template_json["rule"]["and_conditions"] = []
            pre_intercept_rule_template_source_condition = []
            if len(tunnel_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(tunnel_condition_temp_list, object_uuids_list))
            if len(source_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(source_condition_temp_list, object_uuids_list))
                pre_intercept_rule_template_source_condition.extend(rule_template_json["rule"]["and_conditions"])
            if len(destination_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(destination_condition_temp_list, object_uuids_list))
            if len(internal_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(internal_condition_temp_list, object_uuids_list))
            if len(external_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(external_condition_temp_list, object_uuids_list))
            if len(flag_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(flag_condition_temp_list, object_uuids_list))
            if len(ip_protocol_condition_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(ip_protocol_condition_list, object_uuids_list))
            if len(application_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(application_condition_temp_list, object_uuids_list))
            if len(protocol_field_condition_temp_list) > 0:
                rule_template_json["rule"]["and_conditions"].extend(self.generate_rule_condition_list(protocol_field_condition_temp_list, object_uuids_list))
            if "action_parameter" in policy_configuration.keys() and len(policy_configuration["action_parameter"]) > 0:
                rule_template_json["rule"]["action_parameter"] = self.generate_rule_action_parameter(policy_configuration)
            if "effective_range" in policy_configuration.keys() and len(policy_configuration["effective_range"]) > 0:
                rule_template_json["rule"]["effective_range"] = policy_configuration["effective_range"]
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
            if policy_configuration["type"] == "proxy_manipulation" or (policy_configuration["type"] == "service_chaining" and policy_configuration["action_parameter"]["targeted_traffic"] == "decrypted"):
                pre_intercept_rule_uuid_dict, api_error = self.create_preset_intercept_rules(policy_configuration["type"], pre_intercept_rule_template_source_condition, policy_configuration["is_enabled"])
                if len(api_error) > 0:
                    return "", api_error
                rule_uuids_list.append(pre_intercept_rule_uuid_dict)
            url = api_server + "/v1/policies/{}".format(rule_type_dict[policy_configuration["type"]])
            #print(json.dumps(rule_template_json))
            response = requests.post(url, headers=self.headers, json=rule_template_json, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(policy_configuration["type"].replace("_", " ")), flush=True)
                response_dict = json.loads(response.text)
                uuid = self.get_uuids(response_dict)
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
        
    def generate_rule_condition_list(self, and_condition, object_uuids_list):
        if len(object_uuids_list) > 0:
            condition_list = []
            for i in range(len(and_condition)):
                negate_option = and_condition[i]["negate_option"]
                objects_configuration = and_condition[i]["or_conditions"]
                object_list = []
                object_uuids_temp_list = []
                for j in range(len(objects_configuration)):
                    for t in range(len(object_uuids_list)):
                        if "attribute_name" in object_uuids_list[t].keys() and (object_uuids_list[t]["attribute_name"] == objects_configuration[j]["attribute_name"]):
                            if objects_configuration[j]["type"] in ["boolean", "ip_protocol"]:
                                object_uuids_temp_list = object_uuids_list[t]["uuid"]
                            elif objects_configuration[j]["type"] == "application" and "application" not in objects_configuration[j].keys():
                                object_uuids_temp_list = object_uuids_list[t]["uuid"]
                            else:
                                object_uuids_temp_list.append(object_uuids_list[t]["uuid"])
                attribute_name = objects_configuration[0]["attribute_name"]
                object_temp_dict = dict(attribute_name=attribute_name, object_uuids=object_uuids_temp_list)
                object_list.append(object_temp_dict)
                temp_dict = dict(negate_option=negate_option, or_conditions=object_list)
                condition_list.append(temp_dict)
            return condition_list

    def generate_rule_action_parameter(self, policy_configuration):
        action_parameter_dict = {}
        if policy_configuration["type"] == "security" and policy_configuration["action"] == "deny":
            action_parameter_dict["sub_action"] = policy_configuration["action_parameter"]["sub_action"]
            action_parameter_dict["packet_capture"] = {}
            action_parameter_dict["packet_capture"]["enable"] = policy_configuration["action_parameter"]["packet_capture"]["enable"]
            action_parameter_dict["send_icmp_unreachable"] = policy_configuration["action_parameter"]["send_icmp_unreachable"]
            if policy_configuration["action_parameter"]["sub_action"] == "default":
                action_parameter_dict["send_tcp_reset"] = policy_configuration["action_parameter"]["send_tcp_reset"]
            elif policy_configuration["action_parameter"]["sub_action"] == "drop":
                action_parameter_dict["send_tcp_reset"] = policy_configuration["action_parameter"]["send_tcp_reset"]
                action_parameter_dict["after_n_packets"] = policy_configuration["action_parameter"]["after_n_packets"]
            elif policy_configuration["action_parameter"]["sub_action"] == "block":
                action_parameter_dict["code"] = policy_configuration["action_parameter"]["code"]
                if "html_profile" in policy_configuration["action_parameter"].keys():
                    action_parameter_dict["html_profile"] = policy_configuration["action_parameter"]["html_profile"]
                elif "message" in policy_configuration["action_parameter"].keys():
                    action_parameter_dict["message"] = policy_configuration["action_parameter"]["message"]
            elif policy_configuration["action_parameter"]["sub_action"] == "redirect":
                # dns redirect
                if "resolution" in policy_configuration["action_parameter"].keys() and len(policy_configuration["action_parameter"]["resolution"]) > 0:
                    action_parameter_dict["resolution"] = [
                        {
                            "qtype":policy_configuration["action_parameter"]["resolution"][0]["qtype"],
                            "answer":[]
                        }
                    ]
                    for i in range(len(policy_configuration["action_parameter"]["resolution"][0]["answer"])):
                        answer_dict = {}
                        answer_dict["atype"] = policy_configuration["action_parameter"]["resolution"][0]["answer"][i]["atype"]
                        answer_dict["value"] = policy_configuration["action_parameter"]["resolution"][0]["answer"][i]["value"]
                        answer_dict["ttl"] = {
                            "min": policy_configuration["action_parameter"]["resolution"][0]["answer"][i]["ttl"]["min"],
                            "max": policy_configuration["action_parameter"]["resolution"][0]["answer"][i]["ttl"]["max"]
                        }
                        action_parameter_dict["resolution"]["answer"].append(answer_dict) 
                # http redirect
                else:
                    action_parameter_dict["code"] = policy_configuration["action_parameter"]["code"]
                    action_parameter_dict["to"] = policy_configuration["action_parameter"]["to"]
            elif policy_configuration["action_parameter"]["sub_action"] == "alert":
                action_parameter_dict["code"] = policy_configuration["action_parameter"]["code"]
                if policy_configuration["action_parameter"]["code"] == 200 and "message" in policy_configuration["action_parameter"].keys():
                    action_parameter_dict["message"] = policy_configuration["action_parameter"]["message"]
                elif policy_configuration["action_parameter"]["code"] == 200 and "html_profile" in policy_configuration["action_parameter"].keys():
                    action_parameter_dict["html_profile"] = policy_configuration["action_parameter"]["html_profile"]
            elif policy_configuration["action_parameter"]["sub_action"] == "rate_limit":
                action_parameter_dict["bps"] = policy_configuration["action_parameter"]["bps"]
                action_parameter_dict["limitUnit"] = policy_configuration["action_parameter"]["limitUnit"]
            elif policy_configuration["action_parameter"]["sub_action"] == "tamper":
                action_parameter_dict["tamper_mode"] = policy_configuration["action_parameter"]["tamper_mode"]
                if policy_configuration["action_parameter"]["tamper_mode"] == "sample":
                    action_parameter_dict["sampling_method"] = policy_configuration["action_parameter"]["sampling_method"]
                    action_parameter_dict["samples"] = policy_configuration["action_parameter"]["samples"]
                    action_parameter_dict["batch_size"] = policy_configuration["action_parameter"]["batch_size"]      
        elif policy_configuration["type"] == "monitor":
            action_parameter_dict["packet_capture"] = {}
            action_parameter_dict["packet_capture"]["enable"] = policy_configuration["action_parameter"]["packet_capture"]["enable"]
            if policy_configuration["action_parameter"]["packet_capture"]["enable"] == 1:
                action_parameter_dict["packet_capture"]["capture_depth"] = policy_configuration["action_parameter"]["packet_capture"]["capture_depth"]
            action_parameter_dict["traffic_mirroring"] = {}
            action_parameter_dict["traffic_mirroring"]["enable"] = policy_configuration["action_parameter"]["traffic_mirroring"]["enable"]
            if policy_configuration["action_parameter"]["traffic_mirroring"]["enable"] == 1:
                action_parameter_dict["traffic_mirroring"]["vlanID"] = policy_configuration["action_parameter"]["traffic_mirroring"]["vlanID"]
                action_parameter_dict["traffic_mirroring"]["mirroring_profile"] = policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"]
        elif policy_configuration["type"] == "statistics":   
            action_parameter_dict = {
                "template_profile" : policy_configuration["action_parameter"]["template_profile"]
            } 
        elif policy_configuration["type"] == "dos_protection" and policy_configuration["action"] == "protect":
            if policy_configuration["action_parameter"]["mitigation"]["behavior"] == "deny":
                action_parameter_dict["mitigation"] = {
                    "behavior" : policy_configuration["action_parameter"]["mitigation"]["behavior"],
                    "timeout" : policy_configuration["action_parameter"]["mitigation"]["timeout"]
                }
            elif policy_configuration["action_parameter"]["mitigation"]["behavior"] == "none":
                action_parameter_dict["mitigation"] = {
                    "behavior" : policy_configuration["action_parameter"]["mitigation"]["behavior"]
                }
            if policy_configuration["action_parameter"]["threshold"]["type"] == "concurrency":
                action_parameter_dict["threshold"] = {
                    "type" : policy_configuration["action_parameter"]["threshold"]["type"],
                    "concurrency_threshold" :{
                        "group_by" : policy_configuration["action_parameter"]["threshold"]["concurrency_threshold"]["group_by"],
                        "concurrent_sessions" : policy_configuration["action_parameter"]["threshold"]["concurrency_threshold"]["concurrent_sessions"],
                    }
                }
            elif policy_configuration["action_parameter"]["threshold"]["type"] == "rate":
                action_parameter_dict["threshold"] = {
                    "type" : policy_configuration["action_parameter"]["threshold"]["type"],
                    "rate_threshold" :{
                        "group_by" : policy_configuration["action_parameter"]["threshold"]["rate_threshold"]["group_by"],
                        "request_per_period" : policy_configuration["action_parameter"]["threshold"]["rate_threshold"]["request_per_period"],
                        "counting_period" : policy_configuration["action_parameter"]["threshold"]["rate_threshold"]["counting_period"],
                    }
                }
        elif policy_configuration["type"] == "proxy_intercept":
            proxy_intercept_template_path = self.parameter["root_path"] + "/support/api_utils/template/pre_intercept_template.json"
            with open(proxy_intercept_template_path, 'r', encoding='utf-8') as f:
                proxy_intercept_template_json = json.load(f)
                default_keyring_for_untrusted_uuid = proxy_intercept_template_json["rule"]["action_parameter"]["keyring_for_untrusted"]
                default_keyring_for_trusted_uuid = proxy_intercept_template_json["rule"]["action_parameter"]["keyring_for_trusted"]
                default_decryption_profile_uuid = proxy_intercept_template_json["rule"]["action_parameter"]["decryption_profile"]
                default_tcp_option_profile_uuid = proxy_intercept_template_json["rule"]["action_parameter"]["tcp_option_profile"]
                traffic_mirror_enable = proxy_intercept_template_json["rule"]["action_parameter"]["traffic_mirroring"]["enable"]
            action_parameter_dict = {
                "keyring_for_trusted" : default_keyring_for_trusted_uuid,
                "keyring_for_untrusted" : default_keyring_for_untrusted_uuid,
                "tcp_option_profile" : default_tcp_option_profile_uuid,
                "decryption_profile" : default_decryption_profile_uuid,
                "traffic_mirroring" : {
                    "enable" : traffic_mirror_enable
                }
            } 
            for key in policy_configuration["action_parameter"].keys():
                if key in {"keyring_for_trusted","keyring_for_untrusted","tcp_option_profile","decryption_profile"}:
                    action_parameter_dict[key] = policy_configuration["action_parameter"][key]
                elif key == "traffic_mirroring" and policy_configuration["action_parameter"][key]["enable"] == 1:
                    action_parameter_dict[key]["enable"] = policy_configuration["action_parameter"][key]["enable"]
                    action_parameter_dict[key]["vlanID"] = policy_configuration["action_parameter"][key]["vlanID"]
                    action_parameter_dict[key]["mirroring_profile"] = policy_configuration["action_parameter"][key]["mirroring_profile"]
                else:
                    continue
        elif policy_configuration["type"] == "proxy_manipulation":
            if policy_configuration["action"] == "deny":
                action_parameter_dict = {
                    "sub_action" : policy_configuration["action_parameter"]["sub_action"]   
                }
                if "manipulation_block" in policy_configuration["action_parameter"].keys():
                    action_parameter_dict["manipulation_block"] = policy_configuration["action_parameter"]["manipulation_block"]
                    action_parameter_dict["code"] = policy_configuration["action_parameter"]["code"]
                    if "message" in policy_configuration["action_parameter"].keys():
                        action_parameter_dict["message"] = policy_configuration["action_parameter"]["message"]
                    elif "html_profile" in policy_configuration["action_parameter"].keys():
                        action_parameter_dict["html_profile"] = policy_configuration["action_parameter"]["html_profile"]
            elif policy_configuration["action"] == "redirect":
                action_parameter_dict["code"] = policy_configuration["action_parameter"]["code"]
                action_parameter_dict["to"] = policy_configuration["action_parameter"]["to"]
            elif policy_configuration["action"] == "modify":
                if policy_configuration["action_parameter"]["sub_action"] == "replace_text":
                    action_parameter_dict = {
                        "sub_action" : policy_configuration["action_parameter"]["sub_action"],  
                        "rules" : [] 
                    }
                    for i in range(len(policy_configuration["action_parameter"]["rules"])):
                        rules_dict = {
                            "regex_enable" : policy_configuration["action_parameter"]["rules"][i]["regex_enable"],
                            "_id" : policy_configuration["action_parameter"]["rules"][i]["_id"],
                            "search_in" : policy_configuration["action_parameter"]["rules"][i]["search_in"],
                            "find" : policy_configuration["action_parameter"]["rules"][i]["find"],
                            "replace_with" : policy_configuration["action_parameter"]["rules"][i]["replace_with"]
                        }
                        action_parameter_dict["rules"].append(rules_dict)
                elif policy_configuration["action_parameter"]["sub_action"] == "replace_file":
                    action_parameter_dict = {
                        "sub_action" : policy_configuration["action_parameter"]["sub_action"],  
                        "replacement_file" : policy_configuration["action_parameter"]["replacement_file"]
                    }
                elif policy_configuration["action_parameter"]["sub_action"] == "inject_javascript":
                    action_parameter_dict = {
                        "sub_action" : policy_configuration["action_parameter"]["sub_action"],  
                        "js_file" : policy_configuration["action_parameter"]["js_file"],
                        "injection_section" : policy_configuration["action_parameter"]["injection_section"]
                    } 
                elif policy_configuration["action_parameter"]["sub_action"] == "inject_css":
                    action_parameter_dict = {
                        "sub_action" : policy_configuration["action_parameter"]["sub_action"],  
                        "css_file" : policy_configuration["action_parameter"]["css_file"]
                    }
                elif policy_configuration["action_parameter"]["sub_action"] == "edit_element":
                    action_parameter_dict = {
                        "sub_action" : policy_configuration["action_parameter"]["sub_action"],  
                        "rules" : [] 
                    }
                    for i in range(len(policy_configuration["action_parameter"]["rules"])):
                        rules_dict = {
                            "anchor_element": {
                                "contained_keyword" : policy_configuration["action_parameter"]["rules"][i]["anchor_element"]["contained_keyword"],
                                "search_scope" : policy_configuration["action_parameter"]["rules"][i]["anchor_element"]["search_scope"]
                            },
                            "target_element": {
                                "element_treatment" : policy_configuration["action_parameter"]["rules"][i]["target_element"]["element_treatment"],
                                "target_distance_from_matching" : policy_configuration["action_parameter"]["rules"][i]["target_element"]["target_distance_from_matching"]
                            }
                        }
                        if policy_configuration["action_parameter"]["rules"][i]["anchor_element"]["search_scope"] == "inside_element":
                            rules_dict["anchor_element"]["start_indicator"] = policy_configuration["action_parameter"]["rules"][i]["anchor_element"]["start_indicator"]
                        action_parameter_dict["rules"].append(rules_dict)
            elif policy_configuration["action"] == "execute":  
                action_parameter_dict = {
                    "lua_script" : policy_configuration["action_parameter"]["lua_script"]
                }
        elif policy_configuration["type"] == "service_chaining":
            action_parameter_dict = {
                "targeted_traffic" : policy_configuration["action_parameter"]["targeted_traffic"],
                "sff_profiles" : policy_configuration["action_parameter"]["sff_profiles"]
            }

        return action_parameter_dict

    def create_preset_intercept_rules(self, policy_type, source_condition, enabled):
        vsys = self.parameter["vsys"]
        api_server = self.parameter["api_server"]
        root_path = self.parameter["root_path"]
        proxy_intercept_template_path = root_path + "/support/api_utils/template/pre_intercept_template.json"
        try:
            with open(proxy_intercept_template_path, 'r', encoding='utf-8') as f:
                proxy_intercept_template_json = json.load(f)
            and_condition = source_condition[0]
            proxy_intercept_template_json["vsys"] = vsys
            if policy_type == "service_chaining":
                proxy_intercept_template_json["rule"]["name"] = "service_chaining_pre_intercept"
            elif policy_type == "proxy_manipulation":
                proxy_intercept_template_json["rule"]["name"] = "manipulation_pre_intercept"
            proxy_intercept_template_json["return_data"] = 1
            proxy_intercept_template_json["is_enabled"] = enabled
            proxy_intercept_template_json["rule"]["and_conditions"].append(and_condition)
            url = api_server + "/v1/policies/{}".format("proxy-intercept-rules")
            response = requests.post(url, headers=self.headers, json=proxy_intercept_template_json, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create preset intercept rule successfully.", flush=True)
                response_dict = json.loads(response.text)
                uuid = self.get_uuids(response_dict)
                rule_uuids_temp_dict = {
                    "type" : "proxy_intercept",
                    "uuid" : uuid,
                    "name" : proxy_intercept_template_json["rule"]["name"],
                    "attribute_name" : "PROXY_INTERCEPT_RULE"
                }
                return rule_uuids_temp_dict, ""
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create preset intercept rule failed.", flush=True)
                return "", "Create preset intercept rule failed."
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating preset intercept rule, the exception error: ", str(e), flush=True)
            return "", "When creating preset intercept rule, the exception error: " + str(e)
        
    def get_uuids(self, response_dict):
        uuid = response_dict["data"]["uuid"]
        return uuid