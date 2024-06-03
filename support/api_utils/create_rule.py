#!/usr/bin/python3
# coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import requests
import support.api_utils.get_application_id as get_application_id

class CreatePolicyRule():       
    # 拼接json数据，拼接完成后请求创建策略接口
    def create_rule_from_template(self, token, source_list, dst_list, filter_list, flag_list, condition, create_number, path_dict, api_host, vsys_id, create_profile_ids=[]):
        headers = {"Content-Type": "application/json", "Authorization": token}
        
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
        
        action = condition['rule_action_'+str(create_number)]
        policy_type = condition["policy_type"]
        rule_template_dict['rule']['action'] = action
        rule_template_dict['rule']['vsys_id'] = vsys_id
        rule_template_dict["rule"]["type"] = policy_type
        rule_template_dict['vsys_id'] = vsys_id
        
        # 填写security_deny 相关的user_region
        if 'method_'+str(create_number) in condition:
             method = condition['method_'+str(create_number)]
        else:
             method = ''
             
        if action == 'deny' and policy_type == "security":
            rule_template_dict['rule']['user_region']['method'] = method
            if 'packet_capture_'+str(create_number) in condition:
                rule_template_dict["rule"]["user_region"]["packet_capture"]["enable"] = condition['packet_capture_'+str(create_number)]["enable"]
                if rule_template_dict['rule']['user_region']['packet_capture']["capture_depth"] in condition['packet_capture_'+str(create_number)]:
                    rule_template_dict['rule']['user_region']['packet_capture']["capture_depth"] = condition['packet_capture_' + str(create_number)]["capture_depth"]
                else:
                    rule_template_dict['rule']['user_region']['packet_capture']["capture_depth"] = 2000
            else:
                rule_template_dict['rule']['user_region']['packet_capture'] = {"enable":0}
            if method == 'drop':
                if 'after_n_packets_'+str(create_number) in condition:
                    rule_template_dict['rule']['user_region']['after_n_packets'] = condition['after_n_packets_'+str(create_number)]
                else:
                    rule_template_dict['rule']['user_region']['after_n_packets'] = 0
                if 'send_icmp_unreachable_'+str(create_number) in condition:
                    rule_template_dict['rule']['user_region']['send_icmp_unreachable'] = condition['send_icmp_unreachable_'+str(create_number)]
                else:
                    rule_template_dict['rule']['user_region']['send_icmp_unreachable'] = 0
                if 'send_tcp_reset_'+str(create_number) in condition:
                    rule_template_dict['rule']['user_region']['send_tcp_reset'] = condition['send_tcp_reset_'+str(create_number)]
                else:
                    rule_template_dict['rule']['user_region']['send_tcp_reset'] = 1
            elif method == 'redirect':
                if 'to_'+str(create_number) in condition:
                        rule_template_dict['rule']['user_region']['to'] = condition['to_'+str(create_number)]
                if 'code_'+str(create_number) in condition:
                        rule_template_dict['rule']['user_region']['code'] = condition['code_'+str(create_number)]
                if 'resolution_'+str(create_number) in condition:
                    rule_template_dict['rule']['user_region']['resolution'] = condition['resolution_' + str(create_number)]
                    if "record_id" in condition['resolution_'+str(create_number)][0]["answer"][0].keys():
                        rule_template_dict['rule']['user_region']['resolution'][0]["answer"][0]["record_id"] = create_profile_ids[0]["id"]
            elif method == "block" and 'message_'+str(create_number) in condition:
                rule_template_dict['rule']['user_region']['code'] = condition['code_'+str(create_number)]
                rule_template_dict['rule']['user_region']["message"] = condition['message_'+str(create_number)]
            elif method == "block" and 'message_'+str(create_number) not in condition:
                rule_template_dict['rule']['user_region']['code'] = condition['code_'+str(create_number)]
                if str(condition['code_'+str(create_number)])[0] != "5":
                    rule_template_dict['rule']['user_region']["html_profile"] = create_profile_ids[0]["id"]
            elif method == "alert" and 'message_'+str(create_number) in condition:
                rule_template_dict['rule']['user_region']['code'] = condition['code_' + str(create_number)]
                rule_template_dict['rule']['user_region']["message"] = condition['message_' + str(create_number)]
            elif method == "alert" and 'message_'+str(create_number) not in condition:
                rule_template_dict['rule']['user_region']['code'] = condition['code_' + str(create_number)]
                if condition['code_' + str(create_number)] == 200:
                    rule_template_dict['rule']['user_region']["html_profile"] = create_profile_ids[0]["id"]
            elif method == "rate_limit":
                rule_template_dict['rule']['user_region']['bps'] = condition['bps_' + str(create_number)]
        elif action == 'monitor' and policy_type == "monitor":
            if 'packet_capture_'+str(create_number) in condition:
                rule_template_dict["rule"]["user_region"]["packet_capture"]["enable"] = condition['packet_capture_'+str(create_number)]["enable"]
                if rule_template_dict['rule']['user_region']['packet_capture']["capture_depth"] in condition['packet_capture_'+str(create_number)]:
                    rule_template_dict['rule']['user_region']['packet_capture']["capture_depth"] = condition['packet_capture_' + str(create_number)]["capture_depth"]
                else:
                    rule_template_dict['rule']['user_region']['packet_capture']["capture_depth"] = 2000
            else:
                rule_template_dict['rule']['user_region']['packet_capture'] = {"enable":0}
            if 'traffic_mirror_' +str(create_number) in condition:
                rule_template_dict["rule"]["user_region"]["traffic_mirror"]["enable"] = condition['traffic_mirror_'+str(create_number)]["enable"]
            else:
                rule_template_dict["rule"]["user_region"]["traffic_mirror"] = {"enable":0}
        
        app_name = condition['app_name_'+str(create_number)]
        if len(app_name) > 0:
            app_group_id_list = get_application_id.get_group_id(str(app_name), api_host)
            objects_list = []
            object_ids = dict(object_ids=app_group_id_list)
            objects_list.append(object_ids)
            application_dict = dict(objects=objects_list, attribute_name='ATTR_APP_ID', is_negate=0)
            rule_template_dict['rule']['application'] = application_dict
        else:
            rule_template_dict['rule']['application'] = None
            
        rule_template_dict['rule']['do_log'] = condition['do_log_' + str(create_number)]
        
        #添加sc逻辑
        if condition["policy_type"] == "service_chaining":
            #如果sc为Decrypted Traffic,先创建一条intercept策略
            if condition["targeted_traffic"] == "decrypted":
                pre_policy_id_list = self.create_associated_rule(condition, headers, api_host, source_list, dst_list, path_dict,vsys_id)
            user_region = {"targeted_traffic": "", "sff_profiles": []}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            rule_template_dict["rule"]["action"] = condition["rule_action_1"]
            if len(condition["app_name_1"]) == 0:
                user_region["protocol"] = ""
            else:
                user_region["protocol"] = condition["app_name_1"][0]
            user_region["targeted_traffic"] = condition["targeted_traffic"]
            user_region["sff_profiles"].append(create_profile_ids[0]["id"])
            rule_template_dict["rule"]["user_region"] = user_region
        # 添加profile statistics逻辑
        elif condition["policy_type"] == "statistics":
            user_region = {"protocol":"", "template_id":0}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            rule_template_dict["rule"]["action"] = condition["rule_action_1"]
            if len(condition["app_name_1"]) == 0:
                user_region["protocol"] = ""
            else:
                user_region["protocol"] = condition["app_name_1"][0]
            user_region["template_id"] = create_profile_ids[0]["id"]
            rule_template_dict["rule"]["user_region"] = user_region
        # 添加intercept逻辑,填写和Intercept相关的user_region
        elif condition["policy_type"] == "pxy_intercept":
            user_region = {"protocol": "", "tcp_option_profile": 1}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            if len(condition["app_name_1"]) == 0:
                user_region["protocol"] = ""
            else:
                user_region["protocol"] = condition["app_name_1"][0]
            # 当且仅当application=ssl且action=intercept时,user_region包含解密profiles和解密kering
            if "ssl" in condition["app_name_1"][0] and action == "intercept":
                user_region["keyring_for_untrusted"] = 0
                user_region["keyring_for_trusted"] = 1
                user_region["decryption"] = 1
                user_region["traffic_mirror"] = {"enable": 0}
            rule_template_dict["rule"]["user_region"] = user_region
        # 创建manipulation策略
        elif condition["policy_type"] == "pxy_manipulation":
            # 创建manipulation策略前先下发一条deny_quic策略和一条intercept策略
            pre_policy_id_list = self.create_associated_rule(condition, headers, api_host, source_list, dst_list, path_dict)
            user_region = {}
            rule_template_dict["rule"]["type"] = condition["policy_type"]
            # 填写不同动作的user_region
            if action == "deny" and 'message_'+str(create_number) in condition:
                user_region["method"] = "block"
                user_region["code"] = condition["code_"+str(create_number)]
                user_region["message"] = condition["message_"+str(create_number)]
            elif action == "deny" and 'message_'+str(create_number) not in condition:
                user_region["method"] = "block"
                user_region["code"] = condition["code_"+str(create_number)]
                user_region["html_profile"] = create_profile_ids[0]["id"]
            elif action == "hijack":
                user_region["method"] = "hijack"
                user_region["hijack_profile"] = create_profile_ids[0]["id"]
            elif action == "insert":
                user_region["method"] = "insert"
                user_region["insert_profile"] = create_profile_ids[0]["id"]
            elif action == "run_script":
                user_region["method"] = "run_script"
                user_region["run_script_profile"] = create_profile_ids[0]["id"]
            elif action == "redirect":
                user_region["method"] = "redirect"
                user_region["code"] = condition["code_"+str(create_number)]
                user_region["to"] = condition["to_"+str(create_number)]
            elif action == "replace":
                user_region["method"] = "replace"
                rules = []
                rule_dict = {}
                rule_dict["regex_enable"] = condition["regex_enable"]
                rule_dict["regexEnable"] = condition["regexEnable"]
                rule_dict["search_in"] = condition["search_in"]
                rule_dict["find"] = condition["find"]
                rule_dict["replace_with"] = condition["replace_with"]
                rules.append(rule_dict)
                user_region["rules"] = rules
            elif action == "edit_element" and condition["search_scope"] == "whole_file":
                user_region["method"] = "edit_element"
                rules = []
                rule_dict = {"anchor_element": {}, "target_element": {}}
                rule_dict["anchor_element"]["search_scope"] = condition["search_scope"]
                rule_dict["anchor_element"]["contained_keyword"] = condition["contained_keyword"]
                rule_dict["target_element"]["target_distance_from_matching"] = condition["target_distance_from_matching"]
                rule_dict["target_element"]["element_treatment"] = condition["element_treatment"]
                rules.append(rule_dict)
                user_region["rules"] = rules
            elif action == "edit_element" and condition["search_scope"] == "inside_element":
                user_region["method"] = "edit_element"
                rules = []
                rule_dict = {"anchor_element": {}, "target_element": {}}
                rule_dict["anchor_element"]["search_scope"] = condition["search_scope"]
                rule_dict["anchor_element"]["contained_keyword"] = condition["contained_keyword"]
                rule_dict["anchor_element"]["start_indicator"] = condition["start_indicator"]
                rule_dict["target_element"]["target_distance_from_matching"] = condition["target_distance_from_matching"]
                rule_dict["target_element"]["element_treatment"] = condition["element_treatment"]
                rules.append(rule_dict)
                user_region["rules"] = rules
            rule_template_dict["rule"]["user_region"] = user_region
        
        # 开始创建rule
        policy_id_list_temp = self.create_rule(rule_template_dict, headers, api_host)
        if condition["policy_type"] == "pxy_manipulation" or (condition["policy_type"] == "service_chaining" and condition["targeted_traffic"] == "decrypted"):
            policy_id_list_temp = [*policy_id_list_temp, *pre_policy_id_list]
        
        return policy_id_list_temp

    def create_associated_rule(self, condition, headers, api_host, source_list, dst_list, path_dict,vsys_id):
        pre_deny_quic_path = path_dict["pre_deny_quic_template_path"]
        pre_intercept_path = path_dict["pre_intercept_template_path"]
        
        # 新建security_deny_quic策略,只取source_list和dst_list
        if condition["policy_type"] == "pxy_manipulation":
            with open(pre_deny_quic_path, 'r', encoding='utf-8') as f:
                pre_deny_quic_template_dict = json.load(f)
            if len(source_list) > 0:
                pre_deny_quic_template_dict['rule']['source'] = source_list
            else:
                pre_deny_quic_template_dict['rule']['source'] = []
            if len(dst_list) > 0:
                dst_list = dst_list[0]
                pre_deny_quic_template_dict['rule']['destination'] = dst_list
            else:
                pre_deny_quic_template_dict['rule']['destination'] = []
            pre_deny_quic_policy_id_dict = self.create_rule(pre_deny_quic_template_dict, headers, api_host)
        
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
        
        pre_intercept_policy_id_dict = self.create_rule(pre_intercept_template_path, headers, api_host)
        if condition["policy_type"] == "pxy_manipulation":
            pre_policy_id_list = [*pre_deny_quic_policy_id_dict, *pre_intercept_policy_id_dict]
        else:
            pre_policy_id_list = pre_intercept_policy_id_dict
        
        return pre_policy_id_list

    #请求创建策略接口，下发策略    
    def create_rule(self, rule_template_dict, headers, api_host):
        url = api_host + "/v1/policy/rule"
        response = requests.post(url, headers=headers, json=rule_template_dict, verify=False)
        assert response.status_code == 200
        return_json_data = json.loads(response.text)
        if response.status_code == 200:
            print("Create {} rule successfully.".format(return_json_data['data']['rule']['type']))
        else:
            print("Create {} rule failed.".format(return_json_data['data']['rule']['type']))
        policy_type = return_json_data['data']['rule']['type']
        policy_id = return_json_data['data']['rule']['id']
        policy_id_dict_temp = {}
        policy_id_dict_temp[policy_type] = policy_id
        policy_id_list_temp = []
        policy_id_list_temp.append(policy_id_dict_temp)
        return policy_id_list_temp

if __name__ == '__main__':
    print("test")