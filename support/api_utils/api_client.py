# -*- coding: UTF-8 -*-
import copy
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import random
from support.api_utils.log_in import LogIn
from support.api_utils.create_object import CreateObject
from support.api_utils.create_rule import CreatePolicyRule
from support.api_utils.create_profile import CreateProfile
from support.api_utils.create_library import CreateLibrary
from datetime import datetime
from support.packet_generator.workpath import workdir
import configparser
import os

class APIClient:
    def __init__(self, parameter):
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        self.token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        
    def create_object(self, parameter, policy_configuration):
        headers = {"Content-Type": "application/json", "Authorization": self.token}
        api_server = parameter["api_server"]
        vsys_id = parameter["vsys_id"]
        
        object_uuid = {
            "ip": ["111"]
        }
        return object_uuid
        
    def create_rule(self, token, condition_ids_by_api_dict, test_data, create_number, template_path, api_server, vsys_id, create_profile_ids):
        print(1111111)
    
    def create_policy(self, parameter, test_data, template_path):
        # 变量初始化
        api_server = parameter["api_server"]
        run_env = parameter["env"]
        vsys_id = parameter["vsys_id"]
        token = test_data["token"]
        create_ip_ids, create_subid_ids, create_port_ids, create_imsi_ids, create_phone_number_ids, create_imei_ids, create_apn_ids, create_fqdn_ids, create_url_ids, create_flag_ids, create_keywords_ids, create_account_ids, create_http_signature_ids, create_http_signature_ids, create_profile_ids, create_policies_ids, create_geo_name_ids, library_tag_ids, library_catalog_ids = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        statistics_sc_info_list, policy_statistics_template_chart_info, policy_sc_sff_sf_info, temp_profile_list = [], [], [], []

        # sc需要随机ip
        if  (test_data["policy_type"] == "service_chaining" and test_data["targeted_traffic"] == "raw"):
            test_data = self.generate_random_ip(test_data, run_env, vsys_id)
        
        # 指定循环次数
        is_multi_priority = test_data["is_multi_priority"]
        if is_multi_priority:
            rule_num = test_data["rule_num"]
        else:
            rule_num = 1
            
        for i in range(rule_num):
            # 第i次循环，创建第i组object、profile和rule
            create_number = i + 1
            
            temp_obj_condition = "obj_condition_{}".format(create_number)
            if temp_obj_condition in test_data.keys():
                object_condition_value = test_data[temp_obj_condition]
            else:
                object_condition_value = test_data["obj_condition"]
            
            # 创建object
            create_object = CreateObject()
            object_template = template_path["object_template"]
            #print("object_condition_value: {}".format(object_condition_value))
            timeout_result, condition_ids_by_api_dict = create_object.create_object_from_template(token, parameter, object_condition_value, object_template, api_server, vsys_id)

            if "library_condition" in test_data.keys():# 创建library
                library_condition = test_data["library_condition"]
                create_library = CreateLibrary()
                library_condition_ids_dict, library_tag_ids, library_catalog_ids = create_library.create_library(token, library_condition, api_server, vsys_id)
                condition_ids_by_api_dict = create_library.tags_ids_to_policy_condition_list(library_condition_ids_dict,condition_ids_by_api_dict)
            for k, v_0 in condition_ids_by_api_dict.items():
                v = copy.deepcopy(v_0)
                if k == "ip_ids" and len(v) > 0:
                    create_ip_ids.extend(v)
                if k == "subid_ids" and len(v) > 0:
                    create_subid_ids.extend(v)
                if k == "port_ids" and len(v) > 0:
                    create_port_ids.extend(v)
                if k == "imsi_ids" and len(v) > 0:
                    create_imsi_ids.extend(v)
                if k == "phone_number_ids" and len(v) > 0:
                    create_phone_number_ids.extend(v)
                if k == "imei_ids" and len(v) > 0:
                    create_imei_ids.extend(v)
                if k == "apn_ids" and len(v) > 0:
                    create_apn_ids.extend(v)
                if k == "fqdn_ids" and len(v) > 0:
                    create_fqdn_ids.extend(v)
                if k == "url_ids" and len(v) > 0:
                    create_url_ids.extend(v)
                if k == "flag_ids" and len(v) > 0:
                    create_flag_ids.extend(v)
                if k == "keywords_ids" and len(v) > 0:
                    create_keywords_ids.extend(v)
                if k == "account_ids" and len(v) > 0:
                    create_account_ids.extend(v)
                if k == "http_signature_ids" and len(v) > 0:
                    create_http_signature_ids.extend(v)
                if k == "geo_name_ids" and len(v) > 0:
                    create_geo_name_ids.extend(v)

            # 创建profile
            temp_profile_condition = "profile_condition_{}".format(create_number)
            if temp_profile_condition in test_data.keys():
                profile_condition_value = test_data[temp_profile_condition]
            elif "profile_condition" not in test_data:
                profile_condition_value = ""
            else:
                profile_condition_value = test_data["profile_condition"]
            if len(profile_condition_value) > 0:
                create_profile = CreateProfile()
                for profile_data in profile_condition_value:
                    create_profile_ids_dict = create_profile.create_profile_from_template(template_path, profile_data, token, api_server, vsys_id)
                    #print("create_profile_ids_dict: {}".format(create_profile_ids_dict))
                    create_profile_ids.append(create_profile_ids_dict)
                    #print("create_profile_ids: {}".format(create_profile_ids))

                    if test_data["policy_type"] == "statistics" or test_data["policy_type"] == "service_chaining":
                        temp_profile_list.append(create_profile_ids_dict)
            
            # 创建rule
            create_rule = CreatePolicyRule()
            policy_id_list = create_rule.create_rule_from_template(token, condition_ids_by_api_dict, test_data, create_number, template_path, api_server, vsys_id, create_profile_ids=create_profile_ids)
            # policy_id = list(policy_id_list[0].values())[0]
            if len(create_profile_ids) > i:
                if test_data["policy_type"] == "statistics":
                    temp_info = {}
                    temp_info["policy_id"] = list(policy_id_list[i].values())[i]
                    test_data["rule_id"] = temp_info["policy_id"]
                    temp_info["profile_info"] = temp_profile_list
                    policy_statistics_template_chart_info.append(temp_info)
                    if len(policy_statistics_template_chart_info) > 0:
                        for chart in policy_statistics_template_chart_info[0]["profile_info"][0]["template_info"]:
                            statistics_info = {}
                            statistics_info["rule_id"] = policy_statistics_template_chart_info[0]["policy_id"]
                            for k, v in chart.items():    # 将chart字典中的数据，copy到statistics_info
                                statistics_info[k] = v
                            statistics_sc_info_list.append(statistics_info)
                elif test_data["policy_type"] == "service_chaining":
                    sc_sff_sf_info = {}
                    sc_sff_sf_info["policy_id"] = list(policy_id_list[i].values())[i]
                    sc_sff_sf_info["sff_info"] = temp_profile_list
                    policy_sc_sff_sf_info.append(sc_sff_sf_info)
                    if len(policy_sc_sff_sf_info) > 0:
                        for sff in policy_sc_sff_sf_info[0]["sff_info"]:
                            sc_info = {}
                            sc_info["rule_id"] = policy_sc_sff_sf_info[0]["policy_id"]
                            sc_info["targeted_traffic"] = test_data["targeted_traffic"]
                            temp_application = 'application_'+str(create_number)
                            if temp_application in test_data.keys():
                                sc_info["application"] = test_data[temp_application]
                            else:
                                sc_info["application"] = test_data['application']
                            sc_info["sff_id"] = sff["id"]
                            sc_info["type"] = sff["sff_info"]["type"]
                            sc_info["sf_id"] = sff["sff_info"]["sf_info"][0]["id"]
                            sc_info["device_tag"] = sff["sff_info"]["sf_info"][0]["device_tag"]
                            sc_info["admin_status"] = sff["sff_info"]["sf_info"][0]["admin_status"]
                            sc_info["load_balance_localization"] = sff["sff_info"]["load_balance_localization"]
                            if sff["sff_info"]["sf_info"][0]["connectivity"]["method"] == "vxlan_g":
                                sc_info["sf_method"] = sff["sff_info"]["sf_info"][0]["connectivity"]["method"]
                                sc_info["sf_dest_ip"] = sff["sff_info"]["sf_info"][0]["connectivity"]["dest_ip"]
                                sc_info["health_check_method"] = sff["sff_info"]["sf_info"][0]["health_check"]["method"]
                            else:
                                sc_info["sf_method"] = sff["sff_info"]["sf_info"][0]["connectivity"]["method"]
                                sc_info["health_check_method"] = "none"
                            negate_list = []
                        if "condition" in test_data.keys():
                            for con_key , con_value in test_data["condition"].items():
                                if con_key == "ip_protocol" or con_key == "sub_action_override":
                                    continue
                                else:
                                    if len(con_value) > 0:
                                        for i in range(len(con_value)):
                                            if "negate" in con_value[i].keys() and con_value[i]["negate"] == True:
                                                negate_list.append(1)
                                            else:
                                                negate_list.append(0)
                            if 1 in negate_list:
                                sc_info["is_negate"] = 1
                            else:
                                sc_info["is_negate"] = 0
                        statistics_sc_info_list.append(sc_info)
            if len(policy_id_list) > 0:
                create_policies_ids.extend(policy_id_list)
        
        cfg_list = {}
        cfg_list["create_ip_ids"] = create_ip_ids
        cfg_list["create_subid_ids"] = create_subid_ids
        cfg_list["create_port_ids"] = create_port_ids
        cfg_list["create_imsi_ids"] = create_imsi_ids
        cfg_list["create_phone_number_ids"] = create_phone_number_ids
        cfg_list["create_imei_ids"] = create_imei_ids
        cfg_list["create_apn_ids"] = create_apn_ids
        cfg_list["create_fqdn_ids"] = create_fqdn_ids
        cfg_list["create_url_ids"] = create_url_ids
        cfg_list["create_flag_ids"] = create_flag_ids
        cfg_list["create_keywords_ids"] = create_keywords_ids
        cfg_list["create_account_ids"] = create_account_ids
        cfg_list["create_http_signature_ids"] = create_http_signature_ids
        cfg_list["create_geo_name_ids"] = create_geo_name_ids
        cfg_list["create_profile_ids"] = create_profile_ids
        cfg_list["create_policies_ids"] = create_policies_ids
        cfg_list["statistics_sc_info_list"] = statistics_sc_info_list
        cfg_list["create_library_tag_ids"] = library_tag_ids
        cfg_list["create_library_catalog_ids"] = library_catalog_ids
        cfg_list["timeout_result"] = timeout_result
        
        return cfg_list
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")