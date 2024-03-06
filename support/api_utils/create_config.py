import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import random
from support.api_utils.create_object import CreateObject
from support.api_utils.create_rule import CreatePolicyRule
from support.api_utils.create_profile import CreateProfile

class CreateConfig():
    def create_cfg(self, parameter, condition, template_path):
        # 变量初始化
        test_pc_ip = parameter["test_pc_ip"]
        api_server = parameter["api_server"]
        run_env = parameter["env"]
        vsys_id = parameter["vsys_id"]
        token = parameter["token"]
        create_ip_ids, create_subid_ids, create_fqdn_ids, create_url_ids, create_flag_ids, create_keywords_ids, create_account_ids, create_http_signature_ids, create_http_signature_ids, create_profile_ids, create_policies_ids = [], [], [], [], [], [], [], [], [], [], []
        statistics_sc_info_list, policy_statistics_template_chart_info, policy_sc_sff_sf_info, temp_profile_list = [], [], [], []
        # statistics和sc需要随机ip
        if condition["policyType"] == "statistics" or (condition["policyType"] == "service_chaining" and condition["targeted_traffic"] == "raw"):
            condition = self.generate_random_ip(condition, run_env)
        # 指定循环次数
        isMultiPriority = condition['isMultiPriority']
        if isMultiPriority:
            rule_num = condition['ruleNum']
        else:
            rule_num = 1
        for i in range(rule_num):
            # 第i次循环，创建第i组object、profile和rule
            create_number = i + 1
            object_condition_key = "obj_condition_{}".format(create_number)
            object_condition_value = condition[object_condition_key]
            # 创建object
            create_object = CreateObject()
            object_template = template_path["object_template"]
            timeout_result, src_list, dst_list, filter_list, flag_list, ip_ids, subid_ids, fqdn_ids, url_ids, flag_ids, keywords_ids, account_ids, http_signature_ids = create_object.create_object_from_template(token, object_condition_value, object_template, api_server, test_pc_ip, vsys_id)
            if len(ip_ids) > 0:
                create_ip_ids.extend(ip_ids)
            if len(subid_ids) > 0:
                create_subid_ids.extend(subid_ids)
            if len(fqdn_ids) > 0:
                create_fqdn_ids.extend(fqdn_ids)
            if len(url_ids) > 0:
                create_url_ids.extend(url_ids)
            if len(flag_ids) > 0:
                create_flag_ids.extend(flag_ids)
            if len(keywords_ids) > 0:
                create_keywords_ids.extend(keywords_ids)
            if len(account_ids) > 0:
                create_account_ids.extend(account_ids)
            if len(http_signature_ids) > 0:
                create_http_signature_ids.extend(http_signature_ids)
            # 创建profile
            profile_condition_key = "profile_condition_{}".format(create_number)
            if (profile_condition_key in condition.keys()) and len(condition[profile_condition_key]) > 0:    # 含有profile_condition_ key 并且非空
                create_profile = CreateProfile()
                profile_condition_value = condition[profile_condition_key]
                for profile_data in profile_condition_value:
                    create_profile_ids_dict = create_profile.create_profile_from_template(template_path, profile_data, token, api_server, vsys_id)
                    create_profile_ids.append(create_profile_ids_dict)
                    if condition["policyType"] == "statistics" or condition["policyType"] == "service_chaining":
                        temp_profile_list.append(create_profile_ids_dict)
            # 创建rule
            create_rule = CreatePolicyRule()
            policy_id_list = create_rule.create_rule_from_template(token, src_list, dst_list, filter_list, flag_list, condition, create_number, template_path, api_server, vsys_id, create_profile_ids=create_profile_ids)
            policy_id = list(policy_id_list[0].values())[0]
            if len(create_profile_ids) > i:
                if condition["policyType"] == "statistics":
                    temp_info = {}
                    temp_info["policy_id"] = list(policy_id_list[i].values())[i]
                    temp_info["profile_info"] = temp_profile_list
                    policy_statistics_template_chart_info.append(temp_info)
                    if len(policy_statistics_template_chart_info) > 0:
                        for chart in policy_statistics_template_chart_info[0]["profile_info"][0]["template_info"]:
                            statistics_info = {}
                            statistics_info["rule_id"] = policy_statistics_template_chart_info[0]["policy_id"]
                            statistics_info["template_id"] = chart["template_id"]
                            statistics_info["chart_id"] = chart["chart_id"]
                            statistics_info["chart_type"] = chart["chart_type"]
                            statistics_info["version"] = chart["version"]
                            statistics_info["sql"] = chart["sql"]
                            statistics_sc_info_list.append(statistics_info)
                elif condition["policyType"] == "service_chaining":
                    sc_sff_sf_info = {}
                    sc_sff_sf_info["policy_id"] = list(policy_id_list[i].values())[i]
                    sc_sff_sf_info["sff_info"] = temp_profile_list
                    policy_sc_sff_sf_info.append(sc_sff_sf_info)
                    if len(policy_sc_sff_sf_info) > 0:
                        for sff in policy_sc_sff_sf_info[0]["sff_info"]:
                            sc_info = {}
                            sc_info["rule_id"] = policy_sc_sff_sf_info[0]["policy_id"]
                            sc_info["targeted_traffic"] = condition["targeted_traffic"]
                            sc_info["app_name_1"] = condition["app_name_1"]
                            sc_info["sff_id"] = sff["id"]
                            sc_info["type"] = sff["sff_info"]["type"]
                            sc_info["sf_id"] = sff["sff_info"]["sf_info"][0]["id"]
                            if sff["sff_info"]["sf_info"][0]["connectivity"]["method"] == "vxlan_g":
                                sc_info["sf_method"] = sff["sff_info"]["sf_info"][0]["connectivity"]["method"]
                                sc_info["sf_dest_ip"] = sff["sff_info"]["sf_info"][0]["connectivity"]["dest_ip"]
                                sc_info["health_check_method"] = sff["sff_info"]["sf_info"][0]["health_check"]["method"]
                            else:
                                sc_info["sf_method"] = sff["sff_info"]["sf_info"][0]["connectivity"]["method"]
                                sc_info["health_check_method"] = "none"
                            statistics_sc_info_list.append(sc_info)
            if len(policy_id_list) > 0:
                create_policies_ids.extend(policy_id_list)
        cfg_list = {}
        cfg_list["create_ip_ids"] = create_ip_ids
        cfg_list["create_subid_ids"] = create_subid_ids
        cfg_list["create_fqdn_ids"] = create_fqdn_ids
        cfg_list["create_url_ids"] = create_url_ids
        cfg_list["create_flag_ids"] = create_flag_ids
        cfg_list["create_keywords_ids"] = create_keywords_ids
        cfg_list["create_account_ids"] = create_account_ids
        cfg_list["create_http_signature_ids"] = create_http_signature_ids
        cfg_list["create_profile_ids"] = create_profile_ids
        cfg_list["create_policies_ids"] = create_policies_ids
        cfg_list["statistics_sc_info_list"] = statistics_sc_info_list
        cfg_list["timeout_result"] = timeout_result
        return cfg_list
    
    def generate_random_ip(self, config, run_env):
        # statistics中将ip改为随机
        if "obj_condition_1" in config.keys():
            for obj in config["obj_condition_1"]:
                if obj["protocolField"] == "ATTR_SOURCE_IP" or obj["protocolField"] == "ATTR_DESTINATION_ADDR":
                    src_ip = obj["objectList"][0]["addItemList"][0]["ip_address"]
                    if "-" not in src_ip and "/" not in src_ip:
                        src_ip_list = src_ip.split(".")
                        src_ip_list[2] = str(random.randint(200, 250))
                        src_ip_list[3] = str(random.randint(100, 250))
                        if run_env == "9140":
                            src_ip_list[0] = "172"
                            src_ip_list[1] = "56"
                        elif run_env == "tsgx":
                            src_ip_list[0] = "10"
                            src_ip_list[1] = "64"
                        new_src_ip = ".".join(src_ip_list)
                        obj["objectList"][0]["addItemList"][0]["ip_address"] = new_src_ip
                    elif "-" in src_ip and "/" not in src_ip:
                        two_ip_list = src_ip.split("-")
                        ip_list_1 = two_ip_list[0].split(".")
                        ip_list_2 = two_ip_list[1].split(".")
                        ip_list_1[2] = str(random.randint(200, 250))
                        ip_list_1[3] = str(random.randint(1, 50))
                        ip_list_2[2] = ip_list_1[2]
                        ip_list_2[3] = str(int(ip_list_1[3]) + 200)
                        new_ip_1 = ".".join(ip_list_1)
                        new_ip_2 = ".".join(ip_list_2)
                        if run_env == "9140":
                            ip_list_1[0] = "172"
                            ip_list_1[1] = "56"
                            ip_list_2[0] = "172"
                            ip_list_2[1] = "56"
                        elif run_env == "tsgx":
                            ip_list_1[0] = "10"
                            ip_list_1[1] = "64"
                            ip_list_2[0] = "10"
                            ip_list_2[1] = "64"
                        new_two_ip_list = []
                        new_two_ip_list.append(new_ip_1)
                        new_two_ip_list.append(new_ip_2)
                        new_two_ip = "-".join(new_two_ip_list)
                        obj["objectList"][0]["addItemList"][0]["ip_address"] = new_two_ip
        return config

if __name__ == "__main__":
    print("test")