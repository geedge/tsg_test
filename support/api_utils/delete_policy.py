#!/usr/bin/python3
# coding=utf-8
import copy
import requests
import json
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.api_utils.log_in import LogIn


class DeletePolicy:
    def delele_policy_by_cfg(self, token, parameter, cfg_list):
        try:
            headers = {"Authorization": token}
            api_server = parameter["api_server"]
            vsys_id = parameter["vsys_id"]
            create_ip_ids = cfg_list["create_ip_ids"]
            create_port_ids = cfg_list["create_port_ids"]
            create_imsi_ids = cfg_list["create_imsi_ids"]
            create_phone_number_ids = cfg_list["create_phone_number_ids"]
            create_imei_ids = cfg_list["create_imei_ids"]
            create_apn_ids = cfg_list["create_apn_ids"]
            create_subid_ids = cfg_list["create_subid_ids"]
            create_fqdn_ids = cfg_list["create_fqdn_ids"]
            create_url_ids = cfg_list["create_url_ids"]
            create_flag_ids = cfg_list["create_flag_ids"]
            create_keywords_ids = cfg_list["create_keywords_ids"]
            create_account_ids = cfg_list["create_account_ids"]
            create_http_signature_ids = cfg_list["create_http_signature_ids"]
            create_profile_ids = cfg_list["create_profile_ids"]
            create_policies_ids = cfg_list["create_policies_ids"]
            create_geo_name_ids = cfg_list["create_geo_name_ids"]

            delete_object_template = {}
            delete_rule_template = {"uuids": [], "type": "tsg_security", "vsys_id": 1}
            # 多条id删除的时候需要区分policy_type
            if len(create_policies_ids) > 0:
                for i in range(len(create_policies_ids)):
                    delete_rule_template['type'] = list(create_policies_ids[i].keys())[0]
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
                    api_path_rule_type = api_path_map.get(delete_rule_template['type'])
                    delete_rule_template['uuids'] = list(create_policies_ids[i].values())[0]
                    delete_rule_template['vsys_id'] = vsys_id
                    url = api_server + "/v1/policies/{}".format(api_path_rule_type)
                    response = requests.delete(url, headers=headers, json=delete_rule_template, verify=False)
                    assert response.status_code == 200
                    if response.status_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete rule successfully.", flush=True)
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete rule failed.", flush=True)
            if len(create_ip_ids) > 0:
                delete_object_template['uuids'] = create_ip_ids
                url = api_server + "/v1/objects/{}".format("ip-addresses")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip failed.", flush=True)
            if len(create_port_ids) > 0:
                delete_object_template['uuids'] = create_port_ids
                url = api_server + "/v1/objects/{}".format("ports")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete port successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete port failed.", flush=True)
            if len(create_imsi_ids) > 0:
                delete_object_template['uuids'] = create_imsi_ids
                delete_object_template["vsys_id"] = vsys_id
                url = api_server + "/v1/objects/{}".format("mobile-identities")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imsi successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imsi failed.", flush=True)
            if len(create_phone_number_ids) > 0:
                delete_object_template['uuids'] = create_phone_number_ids
                url = api_server + "/v1/objects/{}".format("mobile-identities")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete phone number successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete phone number failed.", flush=True)
            if len(create_imei_ids) > 0:
                delete_object_template['uuids'] = create_imei_ids
                url = api_server + "/v1/objects/{}".format("mobile-identities")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imei successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imei failed.", flush=True)
            if len(create_apn_ids) > 0:
                delete_object_template['uuids'] = create_apn_ids
                url = api_server + "/v1/objects/{}".format("apns")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete apn successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete apn failed.", flush=True)
            if len(create_subid_ids) > 0:
                delete_object_template['uuids'] = create_subid_ids
                url = api_server + "/v1/objects/{}".format("subscriber-ids")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete sub id successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete sub id failed.", flush=True)
            if len(create_fqdn_ids) > 0:
                delete_object_template['uuids'] = create_fqdn_ids
                url = api_server + "/v1/objects/{}".format("fqdns")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn failed.", flush=True)
            if len(create_url_ids) > 0:
                delete_object_template['uuids'] = create_url_ids
                url = api_server + "/v1/objects/{}".format("urls")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete url successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete url failed.", flush=True)
            if len(create_flag_ids) > 0:
                delete_object_template['uuids'] = create_flag_ids
                url = api_server + "/v1/objects/{}".format("flags")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete flag successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete flag failed.", flush=True)
            if len(create_keywords_ids) > 0:
                delete_object_template['uuids'] = create_keywords_ids
                url = api_server + "/v1/objects/{}".format("keywords")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete keyword successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete keyword failed.", flush=True)
            if len(create_account_ids) > 0:
                delete_object_template['uuids'] = create_account_ids
                delete_object_template["vsys_id"] = vsys_id
                url = api_server + "/v1/objects/{}".format("accounts")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete account successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete account failed.", flush=True)
            if len(create_http_signature_ids) > 0:
                delete_object_template['uuids'] = create_http_signature_ids
                url = api_server + "/v1/objects/{}".format("http_signature")
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete http signature successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete http signature failed.", flush=True)
            if len(create_geo_name_ids) > 0:
                del delete_object_template["type"]
                del delete_object_template["ids"]
                create_geo_name_id = create_geo_name_ids[0]
                delete_object_template["geoname_ids"] = create_geo_name_id
                delete_object_template["vsys_id"] = vsys_id
                url = api_server + "/v1/policy/library/geolocation"
                response = requests.delete(url, headers=headers, json=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete geolocation successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete geolocation failed.", flush=True)
            if len(create_profile_ids) > 0:
                for del_porfile_index in range(len(create_profile_ids)):
                    if create_profile_ids[del_porfile_index]["profile_type"] == "statistics_templates":  # 删除逻辑
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        del_profile_template = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        url = "{}/v1/profiles/statistics-templates".format(api_server)
                        response = requests.delete(url, headers=headers, json=del_profile_template, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete statistics template successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete statistics template failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "service_function_forwarder":  # 删除SFF和SF
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        del_profile_sff = {"uuids": str(profile_id), "vsys": vsys_id}
                        url = "{}/v1/profiles/service-function-forwarders".format(api_server)
                        response = requests.delete(url, headers=headers, json=del_profile_sff, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function forwarder successfully.", flush=True)
                            profile_id = create_profile_ids[del_porfile_index]["sff_info"]["sf_info"][0]["uuid"]
                            del_profile_sf = {"uuids": str(profile_id), "vsys": vsys_id}
                            url = "{}/v1/profiles/service-functions".format(api_server)
                            response = requests.delete(url, headers=headers, json=del_profile_sf, verify=False)
                            assert response.status_code == 200
                            if response.status_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function successfully.", flush=True)
                            else:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function failed.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function forwarder failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "response_page":  # 删除response_page
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/profiles/response-pages".format(api_server)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, json=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete response page successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete response page failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "hijack_files":  # 删除hijack_files
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/profiles/proxy-hijack-files".format(api_server)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, json=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete hijack files successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete hijack files failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "insert_profile":  # 删除insert
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/profiles/proxy-inject-scripts".format(api_server)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, json=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete insert profile successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete insert profile failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "run_script":  # 删除run_script
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/profiles/http-manipulation-scripts".format(api_server)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, json=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete run script successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete run script failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "dns_record":  # 删除dns_record
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/profiles/dns-records".format(api_server)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, json=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns record successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns record failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "traffic_mirror":  # 删除traffic mirror
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/profiles/traffic-mirror-profiles".format(api_server, vsys_id)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, json=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete traffic mirror profile successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete traffic mirror profile failed.", flush=True)
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def delete_policy_by_name(self, token, parameter, name_list):
        if len(token) == 0:
            log_in = LogIn()
            pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
            token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        headers = {"Authorization": token}
        api_server = parameter["api_server"]
        vsys_id = parameter["vsys_id"]
        rule_url = api_server + "/v1/policies"
        obj_url = api_server + "/v1/objects"
        profile_url = api_server + "/v1/profiles"
        dashboard_url = api_server + "/v1/dashboard"
        template = {'type': 'security', 'name': '', 'with_sub_vsys': 0, 'vsys': int(vsys_id)}
        # script_type = parameter["script_type"]

        if len(name_list) == 0:

            # 定义要删除的规则类型
            rule_types = ['security-rules', 'monitor-rules', 'statistics-rules', 'proxy-intercept-rules', 'proxy-manipulation-rules',
                          'service-chaining-rules', 'dos-protection-rules']

            for rule_type in rule_types:
                template['name'] = 'automation_test_policy'
                template['type'] = rule_type
                rule_url_full = rule_url + '/' + rule_type
                self.query_and_delete_by_name(rule_url_full, template, headers)


            # 删除object
            object_types = [
                'ip-addresses', 'fqdns', 'subscriber-ids',
                'keywords', 'urls', 'accounts', 'flags'
            ]

            for obj_type in object_types:
                template['name'] = 'automation_test_object'
                template['type'] = obj_type
                rule_url_full = obj_url + '/' + obj_type
                self.query_and_delete_by_name(rule_url_full, template, headers)

            # 删除profiles   
            # 删除Response Pages及其他配置
            template['name'] = 'automation_test_profile'
            profile_types = [
                "response-pages", "dns-records", "proxy-hijack-files",
                "proxy-inject-scripts", "http-manipulation-scripts"
            ]

            for profile_type in profile_types:
                profile_url = f"{api_server}/v1/vsys{vsys_id}/profiles/{profile_type}"
                if 'type' in template:
                    del template["type"]
                self.query_and_delete_by_name(profile_url, template, headers)

                # 删除Service Function Forwarders和Service Functions
            template['name'] = 'test_sc_api'
            service_function_endpoints = [
                "service-function-forwarders", "service-functions"
            ]

            for endpoint in service_function_endpoints:
                profile_url = f"{api_server}/v1/vsys{vsys_id}/profiles/{endpoint}"
                self.query_and_delete_by_name(profile_url, template, headers)

                # 删除Statistics Templates
            template['name'] = 'test_statistics_api'
            profile_url = f"{api_server}/v1/vsys{vsys_id}/profiles/statistics-templates"
            self.query_and_delete_by_name(profile_url, template, headers)

            # 删除geolocation  24.08 版本临时注释掉
            # geolocation_template = {'location_type': 'geoname_id', 'country': 'auto_geo_obj', 'vsys_id': vsys_id}
            # geolocation_url = api_server + "/v1/policy/library/geolocation"
            # self.delete_geolocation(geolocation_url, geolocation_template, headers, vsys_id)
        elif len(name_list) > 0:
            for name_item in name_list:
                if name_item["type"] in ["security", "service_chaining", "pxy_manipulation", "pxy_intercept", "monitor", "statistics", "dos_protection"]:
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
                    api_path_rule_type = api_path_map.get(name_item["type"])
                    temp_url = "{}/{}".format(rule_url, api_path_rule_type)
                    template['name'] = name_item["name"]
                    template['type'] = name_item["type"]
                    self.query_and_delete_by_name(temp_url, template, headers)
                elif name_item["type"] in ["ip", "port", "url", "fqdn", "http_signature", "mobile_identity", "keywords", "account", "subscriberid"]:
                    api_path_map = {  
                        "ip": "ip-addresses",  
                        "url": "urls",  
                        "fqdn": "fqdns",
                        "keywords": "keywords",
                        "subscriberid": "subscriber-ids",
                        "account": "accounts",
                        "mobile_identity": "mobile-identities",
                        "apn": "apns",
                        "application": "applications",
                        "tunnel": "tunnels",
                        "flag": "flags",
                        "interval": "intervals",
                        "port": "ports",
                        "boolean": "boolean",
                        "ip_protocol": "ip-protocols",
                        "tunnel_level": "tunnel-levels"
                    }  
                    api_path_obj_type = api_path_map.get(name_item["type"])                    
                    temp_url = "{}/{}".format(obj_url, api_path_obj_type)
                    template['name'] = name_item["name"]
                    template['type'] = name_item["type"]
                    if template['type'] == "keywords":
                        template['type'] = "keyword"
                    self.query_and_delete_by_name(temp_url, template, headers)

                elif name_item["type"] in ["service_function_forwarder", "service_function", "statistics_template", "response_page", "hijack_file",
                                         "insert_script", "traffic_mirror", "run_script", "dns_record"]:
                    if 'type' in template:
                        del template["type"]
                    api_path_map = {  
                        "service_function_forwarder": "service-function-forwarders",  
                        "service_function": "service-functions",  
                        "statistics_template": "statistics-templates",
                        "response_page": "response-pages",
                        "hijack_file": "proxy-hijack-files",
                        "insert_script": "proxy-inject-scripts",
                        "traffic_mirror": "traffic-mirror-profiles",
                        "run_script": "http-manipulation-scripts",
                        "dns_record": "dns-records"
                    }  
                    api_path_profile_type = api_path_map.get(name_item["type"])                     
                    template['name'] = name_item["name"]
                    temp_url = "{}/{}".format(profile_url, api_path_profile_type)
                    self.query_and_delete_by_name(temp_url, template, headers)
                elif name_item["type"] in ["dashboard"]:
                    template['name'] = name_item["name"]
                    template['type'] = name_item["type"]
                    self.query_and_delete_by_name(dashboard_url, template, headers)

    def query_and_delete_by_name(self, url, template, headers):
        try:
            response = requests.get(url, headers=headers, params=template, verify=False)
            if response.status_code != 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "search {} failed, please check".format(template['type']))
                return 0
            return_json_data = json.loads(response.text)
            if return_json_data["data"] == None:
                return 0
            if "list" not in return_json_data["data"]:
                return 0
            if '/policies' in url or '/objects' in url or 'dashboard' in url:
                tmp_type = template['type']
            if '/policies' in url:
                data_list = return_json_data['data']['list']
                delete_info = tmp_type.title() + ' ' + 'rule'
            elif '/objects' in url:
                data_list = return_json_data['data']['list']
                delete_info = tmp_type
            elif '/dashboard' in url:
                data_list = return_json_data['data']['list']
                delete_info = tmp_type
            elif 'response-pages' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'response_page'.replace("_", " ")
            elif 'dns-records' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'dns_records'.replace("_", " ")
            elif 'proxy-hijack-files' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'hijack_files'.replace("_", " ")
            elif 'proxy-inject-scripts' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'insert_scripts'.replace("_", " ")
            elif 'http-manipulation-scripts' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'run_scripts'.replace("_", " ")
            elif 'service-function-forwarders' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'service_function_forwarder'.replace("_", " ")
            elif 'service-functions' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'service_function'.replace("_", " ")
            elif 'statistics-templates' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'statistics_template'.replace("_", " ")
            elif 'traffic-mirror-profiles' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'traffic_mirror'.replace("_", " ")
            if len(data_list) > 0:
                delete_data = self.combine_delete_ids(template, data_list)
                for i in range(len(delete_data)):
                    tmp_delete = {"uuids":""}
                    tmp_delete["uuids"] = delete_data[i]
                    response = requests.delete(url, headers=headers, json=tmp_delete, verify=False)
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully.".format(delete_info), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed, please check {}".format(delete_info, delete_data))
            # else:
            #     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "No configuration needs to be deleted.", flush=True)
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def combine_delete_ids(self, template, list_data):
        temp_template = []
        # 遍历列表中的每个 JSON 对象
        for i, json_obj in enumerate(list_data):
            # 提取 uuid 键的值
            uuid = json_obj.get("uuid")
            temp_template.append(uuid)
        return temp_template

    def delete_geolocation(self, geolocation_url, geolocation_template, headers, vsys_id):
        try:
            response = requests.get(geolocation_url, headers=headers, params=geolocation_template, verify=False)
            return_json_data = json.loads(response.text)
            data_list = return_json_data['data']['geolocation_list']
            if len(data_list) > 0:
                ids = [item["geoname_id"] for item in data_list]
                ids_str = ",".join(map(str, ids))
                delete_data = {'geoname_ids': ids_str, 'vsys_id': vsys_id}
                response = requests.delete(geolocation_url, headers=headers, json=delete_data, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete geolocation object successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete geolocation object failed.", flush=True)
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)


if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")