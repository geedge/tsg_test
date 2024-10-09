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
                    delete_rule_template['uuids'] = list(create_policies_ids[i].values())[0]
                    delete_rule_template['vsys_id'] = vsys_id
                    url = api_server + "/v1/vsys{}/policy/rule/{}".format(vsys_id, delete_rule_template['type'])
                    response = requests.delete(url, headers=headers, params=delete_rule_template, verify=False)
                    assert response.status_code == 200
                    if response.status_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete rule successfully.", flush=True)
                    else:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete rule failed.", flush=True)
            if len(create_ip_ids) > 0:
                delete_object_template['uuids'] = create_ip_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "ip")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip failed.", flush=True)
            if len(create_port_ids) > 0:
                delete_object_template['uuids'] = create_port_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "port")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete port successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete port failed.", flush=True)
            if len(create_imsi_ids) > 0:
                delete_object_template['uuids'] = create_imsi_ids
                delete_object_template["vsys_id"] = vsys_id
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "mobile_identity")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imsi successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imsi failed.", flush=True)
            if len(create_phone_number_ids) > 0:
                delete_object_template['uuids'] = create_phone_number_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "mobile_identity")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete phone number successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete phone number failed.", flush=True)
            if len(create_imei_ids) > 0:
                delete_object_template['uuids'] = create_imei_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "mobile_identity")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imei successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete imei failed.", flush=True)
            if len(create_apn_ids) > 0:
                delete_object_template['uuids'] = create_apn_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "apn")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete apn successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete apn failed.", flush=True)
            if len(create_subid_ids) > 0:
                delete_object_template['uuids'] = create_subid_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "subscriberid")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete sub id successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete sub id failed.", flush=True)
            if len(create_fqdn_ids) > 0:
                delete_object_template['uuids'] = create_fqdn_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "fqdn")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn failed.", flush=True)
            if len(create_url_ids) > 0:
                delete_object_template['uuids'] = create_url_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "url")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete url successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete url failed.", flush=True)
            if len(create_flag_ids) > 0:
                delete_object_template['uuids'] = create_flag_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "flag")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete flag successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete flag failed.", flush=True)
            if len(create_keywords_ids) > 0:
                delete_object_template['uuids'] = create_keywords_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "keyword")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete keyword successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete keyword failed.", flush=True)
            if len(create_account_ids) > 0:
                delete_object_template['uuids'] = create_account_ids
                delete_object_template["vsys_id"] = vsys_id
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "account")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete account successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete account failed.", flush=True)
            if len(create_http_signature_ids) > 0:
                delete_object_template['uuids'] = create_http_signature_ids
                url = api_server + "/v1/vsys{}/policy/object/{}".format(vsys_id, "http_signature")
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
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
                response = requests.delete(url, headers=headers, params=delete_object_template, verify=False)
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
                        url = "{}/v1/policy/profile/statistics_template".format(api_server)
                        response = requests.delete(url, headers=headers, params=del_profile_template, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete statistics template successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete statistics template failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "service_function_forwarder":  # 删除SFF和SF
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        del_profile_sff = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        url = "{}/v1/policy/profile/service_function_forwarder".format(api_server)
                        response = requests.delete(url, headers=headers, params=del_profile_sff, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function forwarder successfully.", flush=True)
                            profile_id = create_profile_ids[del_porfile_index]["sff_info"]["sf_info"][0]["id"]
                            del_profile_sf = {"ids": str(profile_id), "vsys_id": vsys_id}
                            url = "{}/v1/policy/profile/service_function".format(api_server)
                            response = requests.delete(url, headers=headers, params=del_profile_sf, verify=False)
                            assert response.status_code == 200
                            if response.status_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function successfully.", flush=True)
                            else:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function failed.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete service function forwarder failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "response_page":  # 删除response_page
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/vsys{}/policy/profile/response_page".format(api_server, vsys_id)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, params=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete response page successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete response page failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "hijack_files":  # 删除hijack_files
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/vsys{}/policy/profile/hijack_file".format(api_server, vsys_id)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, params=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete hijack files successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete hijack files failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "insert_profile":  # 删除insert
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/vsys{}/policy/profile/insert_script".format(api_server, vsys_id)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, params=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete insert profile successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete insert profile failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "run_script":  # 删除run_script
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/vsys{}/policy/profile/run_script".format(api_server, vsys_id)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, params=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete run script successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete run script failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "dns_record":  # 删除dns_record
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/vsys{}/policy/profile/dns_record".format(api_server, vsys_id)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, params=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns record successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns record failed.", flush=True)
                    elif create_profile_ids[del_porfile_index]["profile_type"] == "traffic_mirror":  # 删除traffic mirror
                        profile_id = create_profile_ids[del_porfile_index]["uuid"]
                        url = "{}/v1/vsys{}/policy/profile/traffic_mirror".format(api_server, vsys_id)
                        del_profile_sf = {"uuids": str(profile_id), "vsys_id": vsys_id}
                        response = requests.delete(url, headers=headers, params=del_profile_sf, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns record successfully.", flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns record failed.", flush=True)
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
        rule_url = api_server + "/v1/vsys{}/policy/rule".format(vsys_id)
        obj_url = api_server + "/v1/vsys{}/policy/object".format(vsys_id)
        profile_url = api_server + "/v1/vsys{}/policy/profile".format(vsys_id)
        dashboard_url = api_server + "/v1/dashboard"
        template = {'type': 'security', 'name': '', 'with_sub_vsys': 0, 'vsys_id': vsys_id}
        # script_type = parameter["script_type"]

        if len(name_list) == 0:
            # # 删除security rule
            # template['name'] = 'automation_test_policy'
            # template['type'] = 'security'
            # security_url = rule_url + "security"
            # self.query_and_delete_by_name(security_url, template, headers)
            # # 删除monitor rule
            # template['type'] = 'monitor'
            # monitor_url = rule_url + "monitor"
            # self.query_and_delete_by_name(monitor_url, template, headers)
            # # 删除statistics rule
            # template['type'] = 'statistics'
            # statistics_url = rule_url + "statistics"
            # self.query_and_delete_by_name(statistics_url, template, headers)
            # # 删除intercept rule
            # template['type'] = 'pxy_intercept'
            # self.query_and_delete_by_name(rule_url, template, headers)
            # # 删除manipulation rule
            # template['type'] = 'pxy_manipulation'
            # self.query_and_delete_by_name(rule_url, template, headers)
            # # 删除Service Chaining rule
            # template['type'] = 'service_chaining'
            # self.query_and_delete_by_name(rule_url, template, headers)
            # # 删除Service Chaining rule
            # template['type'] = 'dos_protection'
            # self.query_and_delete_by_name(rule_url, template, headers)

            # 定义要删除的规则类型
            rule_types = ['security', 'monitor', 'statistics', 'pxy_intercept', 'pxy_manipulation',
                          'service_chaining', 'dos_protection']

            for rule_type in rule_types:
                template['name'] = 'automation_test_policy'
                template['type'] = rule_type
                rule_url_full = rule_url + '/' + rule_type
                self.query_and_delete_by_name(rule_url_full, template, headers)

                # # 删除IP Addresses
            # template['name'] = 'automation_test_object'
            # template['type'] = 'ip'
            # if template['type'] == 'ip_learning': template['type'] = 'ip'
            # self.query_and_delete_by_name(obj_url, template, headers)
            # # 删除FQDNs
            # template['type'] = 'fqdn'
            # self.query_and_delete_by_name(obj_url, template, headers)
            # # 删除Subscriber IDs
            # template['type'] = 'subscriberid'
            # self.query_and_delete_by_name(obj_url, template, headers)
            # # 删除HTTP Signatures
            # template['type'] = 'http_signature'
            # self.query_and_delete_by_name(obj_url, template, headers)
            # # 删除Keywords
            # template['type'] = 'keywords'
            # self.query_and_delete_by_name(obj_url, template, headers)
            # # 删除URLs
            # template['type'] = 'url'
            # self.query_and_delete_by_name(obj_url, template, headers)
            # # 删除Accounts
            # template['type'] = 'account'
            # self.query_and_delete_by_name(obj_url, template, headers)
            # # 删除Flags
            # template['type'] = 'flag'
            # self.query_and_delete_by_name(obj_url, template, headers)

            # 删除object
            object_types = [
                'ip', 'fqdn', 'subscriberid', 'http_signature',
                'keywords', 'url', 'account', 'flag'
            ]

            for obj_type in object_types:
                template['name'] = 'automation_test_object'
                template['type'] = obj_type
                rule_url_full = obj_url + '/' + obj_type
                self.query_and_delete_by_name(rule_url_full, template, headers)

                # 删除profile
            # 删除Response Pages
            # template['name'] = 'automation_test_profile'
            # profile_url = api_server + "/v1/vsys{}/policy/profile/response_page".format(vsys_id)
            # if 'type' in template:
            #     del template["type"]
            # self.query_and_delete_by_name(profile_url, template, headers)
            # # 删除DNS Records
            # profile_url = api_server + "/v1/vsys{}/policy/profile/dns_record".format(vsys_id)
            # self.query_and_delete_by_name(profile_url, template, headers)
            # # 删除Hijack Files
            # profile_url = api_server + "/v1/vsys{}/policy/profile/hijack_file".format(vsys_id)
            # self.query_and_delete_by_name(profile_url, template, headers)
            # # 删除Insert Scripts
            # profile_url = api_server + "/v1/vsys{}/policy/profile/insert_script".format(vsys_id)
            # self.query_and_delete_by_name(profile_url, template, headers)
            # # 删除TSG Proxy Scripts
            # profile_url = api_server + "/v1/vsys{}/policy/profile/run_script".format(vsys_id)
            # self.query_and_delete_by_name(profile_url, template, headers)
            # # 删除Service Function Forwarders
            # template['name'] = 'test_sc_api'
            # profile_url = api_server + "/v1/policy/profile/service_function_forwarder"
            # self.query_and_delete_by_name(profile_url, template, headers)
            # # 删除Service Functions
            # template['name'] = 'test_sc_api'
            # profile_url = api_server + "/v1/policy/profile/service_function"
            # self.query_and_delete_by_name(profile_url, template, headers)
            # # 删除Statistics Templates
            # template['name'] = 'test_statistics_api'
            # profile_url = api_server + "/v1/policy/profile/statistics_template"
            # self.query_and_delete_by_name(profile_url, template, headers)
            # 删除Response Pages及其他配置
            template['name'] = 'automation_test_profile'
            profile_types = [
                "response_page", "dns_record", "hijack_file",
                "insert_script", "run_script"
            ]

            for profile_type in profile_types:
                profile_url = f"{api_server}/v1/vsys{vsys_id}/policy/profile/{profile_type}"
                if 'type' in template:
                    del template["type"]
                self.query_and_delete_by_name(profile_url, template, headers)

                # 删除Service Function Forwarders和Service Functions
            template['name'] = 'test_sc_api'
            service_function_endpoints = [
                "service_function_forwarder", "service_function"
            ]

            for endpoint in service_function_endpoints:
                profile_url = f"{api_server}/v1/vsys{vsys_id}/policy/profile/{endpoint}"
                self.query_and_delete_by_name(profile_url, template, headers)

                # 删除Statistics Templates
            template['name'] = 'test_statistics_api'
            profile_url = f"{api_server}/v1/vsys{vsys_id}/policy/profile/statistics_template"
            self.query_and_delete_by_name(profile_url, template, headers)

            # 删除geolocation  24.08 版本临时注释掉
            # geolocation_template = {'location_type': 'geoname_id', 'country': 'auto_geo_obj', 'vsys_id': vsys_id}
            # geolocation_url = api_server + "/v1/policy/library/geolocation"
            # self.delete_geolocation(geolocation_url, geolocation_template, headers, vsys_id)
        elif len(name_list) > 0:
            for name_item in name_list:
                if name_item["type"] in ["security", "service_chaining", "pxy_manipulation", "pxy_intercept", "monitor", "statistics", "dos_protection"]:
                    temp_url = "{}/{}".format(rule_url, name_item["type"])
                    template['name'] = name_item["name"]
                    template['type'] = name_item["type"]
                    self.query_and_delete_by_name(temp_url, template, headers)
                elif name_item["type"] in ["ip", "port", "url", "fqdn", "http_signature", "mobile_identity", "keywords", "account", "subscriberid"]:
                    temp_url = "{}/{}".format(obj_url, name_item["type"])
                    template['name'] = name_item["name"]
                    template['type'] = name_item["type"]
                    self.query_and_delete_by_name(temp_url, template, headers)

                elif name_item["type"] in ["service_function_forwarder", "service_function", "statistics_template", "response_page", "hijack_file",
                                         "insert_script", "traffic_mirror", "run_script", "dns_record"]:
                    if 'type' in template:
                        del template["type"]
                    template['name'] = name_item["name"]
                    temp_url = "{}/{}".format(profile_url, name_item["type"])
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
            if '/policy/rule' in url or '/policy/object' in url or 'dashboard' in url:
                tmp_type = template['type']
            if '/policy/rule' in url:
                data_list = return_json_data['data']['list']
                delete_info = tmp_type.title() + ' ' + 'rule'
            elif '/policy/object' in url:
                data_list = return_json_data['data']['list']
                delete_info = tmp_type
            elif '/dashboard' in url:
                data_list = return_json_data['data']['list']
                delete_info = tmp_type
            elif 'response_page' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'response_page'.replace("_", " ")
            elif 'dns_record' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'dns_records'.replace("_", " ")
            elif 'hijack_file' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'hijack_files'.replace("_", " ")
            elif 'insert_script' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'insert_scripts'.replace("_", " ")
            elif 'run_script' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'run_scripts'.replace("_", " ")
            elif 'service_function_forwarder' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'service_function_forwarder'.replace("_", " ")
            elif 'service_function' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'service_function'.replace("_", " ")
            elif 'statistics_template' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'statistics_template'.replace("_", " ")
            elif 'traffic_mirror' in url:
                data_list = return_json_data['data']['list']
                delete_info = 'traffic_mirror'.replace("_", " ")
            if len(data_list) > 0:
                delete_data = self.combine_delete_ids(template, data_list)
                for i in range(len(delete_data)):
                    tmp_delete = {"uuids":""}
                    tmp_delete["uuids"] = delete_data[i]
                    response = requests.delete(url, headers=headers, params=tmp_delete, verify=False)
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
                response = requests.delete(geolocation_url, headers=headers, params=delete_data, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete geolocation object successfully.", flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete geolocation object failed.", flush=True)
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)


if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")