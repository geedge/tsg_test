#!/usr/bin/python3
# coding=utf-8
import copy
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import requests
import support.api_utils.get_application_id as get_application_id
from datetime import datetime


class CreatePolicyRule:
    # 拼接json数据，拼接完成后请求创建策略接口
    def create_rule_from_template(self, token, condition_ids_by_api_dict, condition, create_number, path_dict, api_host, vsys_id, create_profile_ids=[]):
        # condition_ids_by_api_dict 所有api创建的condition id 都通过dict传递
        headers = {"Content-Type": "application/json", "Authorization": token}

        source_list, dst_list, filter_list, flag_list = [], [], [], []
        for k, v in condition_ids_by_api_dict.items():
            if k == "src_list":
                source_list = v
            elif k == "dst_list":
                dst_list = v
            elif k == "int_list":
                int_list = v
            elif k == "ext_list":
                ext_list = v
            elif k == "filter_list":
                filter_list = v
            elif k == "flag_list":
                flag_list = v
        template = path_dict["rule_template"]
        with open(template, 'r', encoding='utf-8') as f:
            rule_template_dict = json.load(f)

        if len(source_list) > 0:
            rule_template_dict['rule']['source'] = source_list
        else:
            rule_template_dict['rule']['source'] = []

        if len(dst_list) > 0:
            rule_template_dict['rule']['destination'] = dst_list
        else:
            rule_template_dict['rule']['destination'] = []

        if len(int_list) > 0:
            rule_template_dict['rule']['internal'] = int_list
        else:
            rule_template_dict['rule']['internal'] = []

        if len(ext_list) > 0:
            rule_template_dict['rule']['external'] = ext_list
        else:
            rule_template_dict['rule']['external'] = []

        if len(filter_list) > 0:
            filter_list = filter_list
            rule_template_dict['rule']['filter'] = filter_list
        else:
            rule_template_dict['rule']['filter'] = []

        if len(flag_list) > 0:
            flag_list = flag_list[0]
            rule_template_dict['rule']['flag'] = flag_list
        else:
            rule_template_dict['rule']['flag'] = None

        temp_rule_action = 'rule_action_' + str(create_number)
        if temp_rule_action in condition.keys():
            action = condition[temp_rule_action]
        else:
            action = condition["rule_action"]
        rule_template_dict['rule']['action'] = action
        rule_template_dict['rule']['vsys_id'] = vsys_id
        policy_type = condition["policy_type"]
        rule_template_dict["rule"]["type"] = policy_type
        rule_template_dict['vsys_id'] = vsys_id

        # 填写security_deny 相关的user_region
        if 'method_' + str(create_number) in condition:
            method = condition['method_' + str(create_number)]
        else:
            method = ''

        if action == 'deny' and policy_type == "security":
            rule_template_dict['rule']['action_parameter']['method'] = method
            if 'packet_capture_' + str(create_number) in condition:
                rule_template_dict["rule"]["action_parameter"]["packet_capture"]["enable"] = condition['packet_capture_' + str(create_number)]["enable"]
                if rule_template_dict['rule']['action_parameter']['packet_capture']["capture_depth"] in condition['packet_capture_' + str(create_number)]:
                    rule_template_dict['rule']['action_parameter']['packet_capture']["capture_depth"] = condition['packet_capture_' + str(create_number)]["capture_depth"]
                else:
                    rule_template_dict['rule']['action_parameter']['packet_capture']["capture_depth"] = 2000
            else:
                rule_template_dict['rule']['action_parameter']['packet_capture'] = {"enable":0}
            if method == 'drop':
                if 'after_n_packets_'+str(create_number) in condition:
                    rule_template_dict['rule']['action_parameter']['after_n_packets'] = condition['after_n_packets_'+str(create_number)]
                else:
                    rule_template_dict['rule']['action_parameter']['after_n_packets'] = 0
                if 'send_icmp_unreachable_'+str(create_number) in condition:
                    rule_template_dict['rule']['action_parameter']['send_icmp_unreachable'] = condition['send_icmp_unreachable_'+str(create_number)]
                else:
                    rule_template_dict['rule']['action_parameter']['send_icmp_unreachable'] = 0
                if 'send_tcp_reset_'+str(create_number) in condition:
                    rule_template_dict['rule']['action_parameter']['send_tcp_reset'] = condition['send_tcp_reset_'+str(create_number)]
                else:
                    rule_template_dict['rule']['action_parameter']['send_tcp_reset'] = 1
            elif method == 'redirect':
                if 'to_'+str(create_number) in condition:
                        rule_template_dict['rule']['action_parameter']['to'] = condition['to_'+str(create_number)]
                if 'code_'+str(create_number) in condition:
                        rule_template_dict['rule']['action_parameter']['code'] = condition['code_'+str(create_number)]
                if 'resolution_'+str(create_number) in condition:
                    rule_template_dict['rule']['action_parameter']['resolution'] = condition['resolution_' + str(create_number)]
                    if "record_id" in condition['resolution_'+str(create_number)][0]["answer"][0].keys():
                        del condition['resolution_'+str(create_number)][0]["answer"][0]["record_id"]
                        rule_template_dict['rule']['action_parameter']['resolution'][0]["answer"][0]["record_uuid"] = create_profile_ids[0]["uuid"]
            elif method == "block" and 'message_'+str(create_number) in condition:
                rule_template_dict['rule']['action_parameter']['code'] = condition['code_'+str(create_number)]
                rule_template_dict['rule']['action_parameter']["message"] = condition['message_'+str(create_number)]
            elif method == "block" and 'message_'+str(create_number) not in condition:
                rule_template_dict['rule']['action_parameter']['code'] = condition['code_'+str(create_number)]
                if str(condition['code_'+str(create_number)])[0] != "5":
                    rule_template_dict['rule']['action_parameter']["profile"] = create_profile_ids[0]["uuid"]
                    rule_template_dict['rule']['action_parameter']["message"] = "html_profile"
            elif method == "alert" and 'message_'+str(create_number) in condition:
                rule_template_dict['rule']['action_parameter']['code'] = condition['code_' + str(create_number)]
                rule_template_dict['rule']['action_parameter']["message"] = condition['message_' + str(create_number)]
            elif method == "alert" and 'message_'+str(create_number) not in condition:
                rule_template_dict['rule']['action_parameter']['code'] = condition['code_' + str(create_number)]
                if condition['code_' + str(create_number)] == 200:
                    rule_template_dict['rule']['action_parameter']["profile"] = create_profile_ids[0]["uuid"]
                    rule_template_dict['rule']['action_parameter']["message"] = "html_profile"
            elif method == "rate_limit":
                rule_template_dict['rule']['action_parameter']['bps'] = condition['bps_' + str(create_number)]
            elif method == "tamper":
                rule_template_dict['rule']['action_parameter']['tamper_mode'] = 'complete'
        elif action == 'monitor' and policy_type == "monitor":
            if 'packet_capture_' + str(create_number) in condition:
                rule_template_dict["rule"]["action_parameter"]["packet_capture"]["enable"] = condition['packet_capture_' + str(create_number)]["enable"]
                if rule_template_dict['rule']['action_parameter']['packet_capture']["capture_depth"] in condition['packet_capture_' + str(create_number)]:
                    rule_template_dict['rule']['action_parameter']['packet_capture']["capture_depth"] = condition['packet_capture_' + str(create_number)]["capture_depth"]
                else:
                    rule_template_dict['rule']['action_parameter']['packet_capture']["capture_depth"] = 2000
            else:
                rule_template_dict['rule']['action_parameter']['packet_capture'] = {"enable": 0}
            if 'traffic_mirror_' + str(create_number) in condition:
                rule_template_dict["rule"]["action_parameter"]["traffic_mirror"]["enable"] = condition['traffic_mirror_' + str(create_number)]["enable"]
            else:
                rule_template_dict["rule"]["action_parameter"]["traffic_mirror"] = {"enable": 0}
        elif policy_type == "dos_protection" and action == "protect":
            if condition["threshold"]["type"] == "rate":
                rule_template_dict['rule']['action_parameter']["threshold"] = {
                    "type": condition["threshold"]["type"],
                    "rate_threshold": {
                        "group_by": condition["threshold"]["rate_threshold"]["group_by"],
                        "request_per_period": condition["threshold"]["rate_threshold"]["request_per_period"],
                        "counting_period": condition["threshold"]["rate_threshold"]["counting_period"]
                    }
                }
            elif condition["threshold"]["type"] == "concurrency":
                rule_template_dict['rule']['action_parameter']["threshold"] = {
                    "type": condition["threshold"]["type"],
                    "concurrency_threshold": {
                        "group_by": condition["threshold"]["concurrency_threshold"]["group_by"],
                        "concurrent_sessions": condition["threshold"]["concurrency_threshold"]["concurrent_sessions"]
                    }
                }
            if condition["mitigation"]["behavior"] == "deny":
                rule_template_dict['rule']['action_parameter']["mitigation"] = {
                    "behavior": condition["mitigation"]["behavior"],
                    "timeout": condition["mitigation"]["timeout"]
                }
            elif condition["mitigation"]["behavior"] == "none":
                rule_template_dict['rule']['action_parameter']["mitigation"] = {
                    "behavior": condition["mitigation"]["behavior"]
                }

        temp_application = 'application_' + str(create_number)
        if temp_application in condition.keys():
            app_name = condition[temp_application]
        else:
            app_name = condition['application']
        if len(app_name) > 0:
            app_group_id_list = get_application_id.get_group_id(str(app_name), api_host)
            objects_list = []
            object_ids = dict(object_uuids=app_group_id_list)
            objects_list.append(object_ids)
            application_dict = dict(objects=objects_list, attribute_name='ATTR_APP_ID', negate_option=False)
            rule_template_dict['rule']['application'] = application_dict
        else:
            rule_template_dict['rule']['application'] = None

        if "ip_protocol" in condition.keys():
            ip_protocol_id_dict = {"ICMP": 5, "TCP": 6, "UDP": 7}
            if len(condition["ip_protocol"]) > 0:
                ip_protocol_id_list = []
                for ip_protocol in condition["ip_protocol"]:
                    ip_protocol_id = int(ip_protocol_id_dict.get(ip_protocol))
                    ip_protocol_id_list.append(ip_protocol_id)
                objects_list = []
                object_ids = dict(object_ids=ip_protocol_id_list)
                objects_list.append(object_ids)
                ip_protocol_dict = dict(objects=objects_list, attribute_name='ATTR_IP_PROTOCOL', is_negate=0)
                rule_template_dict['rule']['ip_protocol'] = ip_protocol_dict
            else:
                rule_template_dict['rule']['ip_protocol'] = None

        temp_do_log = 'do_log_' + str(create_number)
        if temp_do_log in condition.keys():
            if condition[temp_do_log] == 2:
                rule_template_dict['rule']['log_option'] = "all"
            elif condition[temp_do_log] == 0:
                rule_template_dict['rule']['log_option'] = "none"
            # rule_template_dict['rule']['log_option'] = condition[temp_do_log]
        else:
            rule_template_dict['rule']['log_option'] = condition['do_log']

        # 添加sc逻辑
        if condition["policy_type"] == "service_chaining":
            # 如果sc为Decrypted Traffic, 先创建一条intercept策略
            tmp_list = []
            if condition["targeted_traffic"] == "decrypted":
                pre_policy_id_list = self.create_associated_rule(headers, api_host, source_list, tmp_list, path_dict, vsys_id, "service_chaining")
            user_region = {"targeted_traffic": "", "sff_profiles": []}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            temp_rule_action = 'rule_action_' + str(create_number)
            if temp_rule_action in condition.keys():
                rule_template_dict["rule"]["action"] = condition[temp_rule_action]
            else:
                rule_template_dict["rule"]["action"] = condition["rule_action"]
            # temp_application = 'application_' + str(create_number)
            # if temp_application in condition.keys():
            #     if len(condition[temp_application]) == 0:
            #         user_region["protocol"] = ""
            #     else:
            #         user_region["protocol"] = condition[temp_application][0]
            # else:
            #     if len(condition["application"]) == 0:
            #         user_region["protocol"] = ""
            #     else:
            #         user_region["protocol"] = condition["application"][0]
            user_region["targeted_traffic"] = condition["targeted_traffic"]
            user_region["sff_profiles"].append(create_profile_ids[0]["uuid"])
            rule_template_dict["rule"]["action_parameter"] = user_region
        # 添加profile statistics逻辑
        elif condition["policy_type"] == "statistics":
            user_region = {"protocol": "", "template_id": 0}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            temp_rule_action = 'rule_action_' + str(create_number)
            if temp_rule_action in condition.keys():
                rule_template_dict["rule"]["action"] = condition[temp_rule_action]
            else:
                rule_template_dict["rule"]["action"] = condition["rule_action"]
            temp_application = 'application_' + str(create_number)
            if temp_application in condition.keys():
                if len(condition[temp_application]) == 0:
                    user_region["protocol"] = ""
                else:
                    user_region["protocol"] = condition[temp_application][0]
            else:
                if len(condition["application"]) == 0:
                    user_region["protocol"] = ""
                else:
                    user_region["protocol"] = condition["application"][0]
            user_region["template_uuid"] = create_profile_ids[0]["uuid"]
            rule_template_dict["rule"]["action_parameter"] = user_region
        # 添加intercept逻辑, 填写和Intercept相关的user_region
        elif condition["policy_type"] == "pxy_intercept":
            user_region = {"protocol": "", "tcp_option_profile": 1}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            temp_application = 'application_' + str(create_number)
            if temp_application in condition.keys():
                if len(condition[temp_application]) == 0:
                    user_region["protocol"] = ""
                else:
                    user_region["protocol"] = condition[temp_application][0]
                    # 当且仅当application=ssl且action=intercept时, user_region包含解密profiles和解密kering
                    if "ssl" in condition[temp_application][0] and action == "intercept":
                        user_region["keyring_for_untrusted"] = 0
                        user_region["keyring_for_trusted"] = 1
                        user_region["decryption_profile"] = 1
                        user_region["traffic_mirror"] = {"enable": 0}
            else:
                if len(condition["application"]) == 0:
                    user_region["protocol"] = ""
                else:
                    user_region["protocol"] = condition["application"][0]
                    if "ssl" in condition["application"][0] and action == "intercept":
                        user_region["keyring_for_untrusted"] = 0
                        user_region["keyring_for_trusted"] = 1
                        user_region["decryption_profile"] = 1
                        user_region["traffic_mirror"] = {"enable": 0}
            rule_template_dict["rule"]["user_region"] = user_region
        # 创建manipulation策略
        elif condition["policy_type"] == "pxy_manipulation":
            # 创建manipulation策略前先下发一条deny_quic策略和一条intercept策略
            tmp_list = []  # 前置拦截策略，只添加src ip
            pre_policy_id_list = self.create_associated_rule(headers, api_host, source_list, tmp_list, path_dict, vsys_id, "pxy_manipulation")
            user_region = {}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            # 填写不同动作的user_region
            if action == "deny" and 'message_' + str(create_number) in condition:
                user_region["method"] = "block"
                user_region["code"] = condition["code_" + str(create_number)]
                user_region["message"] = condition["message_" + str(create_number)]
            elif action == "deny" and 'message_' + str(create_number) not in condition:
                user_region["method"] = "block"
                user_region["message"] = "html_profile"
                user_region["code"] = condition["code_" + str(create_number)]
                user_region["profile"] = create_profile_ids[0]["uuid"]
            elif action == "hijack":
                user_region["method"] = "hijack"
                user_region["hijack_profile"] = create_profile_ids[0]["uuid"]
            elif action == "insert":
                user_region["method"] = "insert"
                user_region["insert_profile"] = create_profile_ids[0]["uuid"]
            elif action == "run_script":
                user_region["method"] = "run_script"
                user_region["run_script_profile"] = create_profile_ids[0]["uuid"]
            elif action == "redirect":
                user_region["method"] = "redirect"
                user_region["code"] = condition["code_" + str(create_number)]
                user_region["to"] = condition["to_" + str(create_number)]
            elif action == "replace":
                user_region_data = condition["user_region"]
                rules = []
                for i in range(len(user_region_data)):
                    rule_dict = {}
                    rule_dict["regex_enable"] = user_region_data[i]["regex_enable"]
                    rule_dict["search_in"] = user_region_data[i]["search_in"]
                    rule_dict["find"] = user_region_data[i]["find"]
                    rule_dict["replace_with"] = user_region_data[i]["replace_with"]
                    rules.append(copy.deepcopy(rule_dict))
                user_region["rules"] = rules
                user_region["method"] = "replace"
            elif action == "edit_element":
                user_region_data = condition["user_region"]
                rules = []
                for i in range(len(user_region_data)):
                    rule_dict = {"anchor_element": {}, "target_element": {}}
                    search_scope = user_region_data[i]["search_scope"]
                    rule_dict["anchor_element"]["search_scope"] = search_scope
                    if search_scope == "inside_element":
                        rule_dict["anchor_element"]["start_indicator"] = user_region_data[i]["start_indicator"]
                    rule_dict["anchor_element"]["contained_keyword"] = user_region_data[i]["contained_keyword"]
                    rule_dict["target_element"]["target_distance_from_matching"] = int(user_region_data[i]["target_distance_from_matching"])
                    rule_dict["target_element"]["element_treatment"] = user_region_data[i]["element_treatment"]
                    rules.append(copy.deepcopy(rule_dict))
                user_region["rules"] = rules
                user_region["method"] = "edit_element"
            rule_template_dict["rule"]["action_parameter"] = user_region
            # rule_template_dict["rule"].pop("user_region")
        elif condition["policy_type"] == "monitor":
            user_region = {}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            if action == "monitor":
                # 设置 packet_capture 部分
                user_region["packet_capture"] = {
                    "enable": 0  # 根据实际情况调整是否启用
                }
                # 设置 traffic_mirror 部分
                user_region["traffic_mirror"] = {
                    "enable": 1,  # 启用流量镜像
                    "mirror_profile": create_profile_ids[0]["uuid"]  # 使用 create_profile_ids 中的第一个 ID 作为镜像配置
                }
            rule_template_dict["rule"]["action_parameter"] = user_region

        # 添加用例名称
        if "rule_name" in condition:
            rule_template_dict["rule"]["name"] = condition["rule_name"]
        if "effective_range" in condition:
            rule_template_dict["rule"]["effective_range"] = condition["effective_range"]

        # 开始创建rule
        policy_id_list_temp = self.create_rule(rule_template_dict, headers, api_host, vsys_id)
        if condition["policy_type"] == "pxy_manipulation" or (condition["policy_type"] == "service_chaining" and condition["targeted_traffic"] == "decrypted"):
            policy_id_list_temp = [*policy_id_list_temp, *pre_policy_id_list]

        return policy_id_list_temp

    def create_associated_rule(self, headers, api_host, source_list, dst_list, path_dict, vsys_id, associated_policy):
        pre_intercept_path = path_dict["pre_intercept_template_path"]

        # 新建intercept策略，只取source_list和dst_list
        with open(pre_intercept_path, 'r', encoding='utf-8') as f:
            pre_intercept_template_path = json.load(f)
            pre_intercept_template_path["vsys_id"] = vsys_id
            pre_intercept_template_path["rule"]["vsys_id"] = vsys_id

        if len(source_list) > 0:
            pre_intercept_template_path['rule']['source'] = source_list
        else:
            pre_intercept_template_path['rule']['source'] = []

        if len(dst_list) > 0:
            pre_intercept_template_path['rule']['destination'] = dst_list
        else:
            pre_intercept_template_path['rule']['destination'] = []
        if associated_policy == "pxy_manipulation":
            tmp_name = "manipulation_pre_intercept"
        else:
            tmp_name = "service_chaining_pre_intercept"
        pre_intercept_template_path["rule"]["name"] = tmp_name
        pre_intercept_policy_id_dict = self.create_rule(pre_intercept_template_path, headers, api_host, vsys_id)
        pre_policy_id_list = pre_intercept_policy_id_dict
        #pre_policy_id_list = []
        return pre_policy_id_list

    # 请求创建策略接口，下发策略
    def create_rule(self, rule_template_dict, headers, api_host, vsys_id):
        try:
            rule_type = rule_template_dict["rule"]["type"]
            api_path_map = {  
                "security": "security-rules",
                "proxy_intercept": "proxy-intercept-rules",    
                "proxy_manipulation": "proxy-manipulation-rules",  
                "traffic_shaping": "traffic-shaping-rules",  
                "service_chaining": "service-chaining-rules",  
                "statistics": "statistics-rules",  
                "monitor": "monitor-rules",
                "dos_protection": "dos-protection-rules",  
            }  
            api_path_rule_type = api_path_map.get(rule_type)
            url = api_host + "/v1/policies/{}".format(api_path_rule_type)
            #print(json.dumps(rule_template_dict))
            response = requests.post(url, headers=headers, json=rule_template_dict, verify=False)
            return_json_data = json.loads(response.text)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(return_json_data['data']['type']), flush=True)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule failed.".format(return_json_data['data']['type']), flush=True)
            policy_type = return_json_data['data']['type']
            policy_id = return_json_data['data']['uuid']
            policy_id_dict_temp = {}
            policy_id_dict_temp[policy_type] = policy_id
            policy_id_list_temp = []
            policy_id_list_temp.append(policy_id_dict_temp)
            return policy_id_list_temp
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)


if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")