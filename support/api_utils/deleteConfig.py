#!/usr/bin/python3
# coding=utf-8
import time
import requests

class DeleteConfig():    
    def delele_cfg(self, token, parameter, cfg_list):
        headers = {"Authorization": token}
        api_server = parameter["api_server"]
        vsys_id = parameter["vsys_id"]
        create_ip_ids = cfg_list["create_ip_ids"]
        create_subid_ids = cfg_list["create_subid_ids"]
        create_fqdn_ids = cfg_list["create_fqdn_ids"]
        create_url_ids = cfg_list["create_url_ids"]
        create_flag_ids = cfg_list["create_flag_ids"]
        create_keywords_ids = cfg_list["create_keywords_ids"]
        create_account_ids = cfg_list["create_account_ids"]
        create_http_signature_ids = cfg_list["create_http_signature_ids"]
        create_profile_ids = cfg_list["create_profile_ids"]
        create_policies_ids = cfg_list["create_policies_ids"]
        delete_object_template = {"type":"ip", "ids":[], "vsys_id":1}
        delete_rule_template = {"ids":[], "type":"tsg_security", "vsys_id":1}
        # 多条id删除的时候需要区分policy_type
        if len(create_policies_ids) > 0:
            for i in range(len(create_policies_ids)):
                delete_rule_template['type'] = list(create_policies_ids[i].keys())[0]
                delete_rule_template['ids'] = list(create_policies_ids[i].values())[0]
                delete_rule_template['vsys_id'] = vsys_id
                url = api_server + "/v1/policy/rule"
                response = requests.delete(url, headers=headers, params=delete_rule_template)
                assert response.status_code == 200
        if len(create_ip_ids) > 0:
            delete_object_template['type'] = "ip"
            delete_object_template['ids'] = create_ip_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_subid_ids) > 0:
            delete_object_template['type'] = "subscriberid"
            delete_object_template['ids'] = create_subid_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_fqdn_ids) > 0:
            delete_object_template['type'] = "fqdn"
            delete_object_template['ids'] = create_fqdn_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_url_ids) > 0:
            delete_object_template['type'] = "url"
            delete_object_template['ids'] = create_url_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_flag_ids) > 0:
            delete_object_template['type'] = "flag"
            delete_object_template['ids'] = create_flag_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_keywords_ids) > 0:
            delete_object_template['type'] = "keywords"
            delete_object_template['ids'] = create_keywords_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_account_ids) > 0:
            delete_object_template['type'] = "account"
            delete_object_template['ids'] = create_account_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_http_signature_ids) > 0:
            delete_object_template['type'] = "http_signature"
            delete_object_template['ids'] = create_http_signature_ids
            delete_object_template["vsys_id"] = vsys_id
            url = api_server + "/v1/policy/object"
            response = requests.delete(url, headers=headers, params=delete_object_template)
            assert response.status_code == 200
        if len(create_profile_ids) > 0:
            for del_porfile_index in range(len(create_profile_ids)):
                if create_profile_ids[del_porfile_index]["profile_type"] == "Statistics_Templates":    # 删除逻辑
                    profile_id = create_profile_ids[del_porfile_index]["id"]
                    del_profile_template = {"ids":str(profile_id),"vsys_id":vsys_id}
                    url = "{}/v1/policy/profile/statistics_template".format(api_server)
                    response = requests.delete(url, headers=headers, params=del_profile_template)
                    assert response.status_code == 200
                elif create_profile_ids[del_porfile_index]["profile_type"] == "service_function_forwarder":    # 删除SFF和SF
                    profile_id = create_profile_ids[del_porfile_index]["id"]
                    del_profile_sff = {"ids": str(profile_id),"vsys_id":vsys_id}
                    url = "{}/v1/policy/profile/service_function_forwarder".format(api_server)
                    response = requests.delete(url, headers=headers, params=del_profile_sff)
                    if response.status_code == 200:
                        profile_id = create_profile_ids[del_porfile_index]["sff_info"]["sf_info"][0]["id"]
                        del_profile_sf = {"ids": str(profile_id),"vsys_id":vsys_id}
                        url = "{}/v1/policy/profile/service_function".format(api_server)
                        response = requests.delete(url, headers=headers, params=del_profile_sf)
                    assert response.status_code == 200
                elif create_profile_ids[del_porfile_index]["profile_type"] == "response_page": # 删除response_page
                    profile_id = create_profile_ids[del_porfile_index]["id"]
                    url = "{}/v1/policy/profile/response_page".format(api_server)
                    del_profile_sf = {"ids": str(profile_id), "vsys_id": vsys_id}
                    response = requests.delete(url, headers=headers, params=del_profile_sf)
                    assert response.status_code == 200
                elif create_profile_ids[del_porfile_index]["profile_type"] == "hijack_files": # 删除hijack_files
                    profile_id = create_profile_ids[del_porfile_index]["id"]
                    url = "{}/v1/policy/profile/hijack_file".format(api_server)
                    del_profile_sf = {"ids": str(profile_id), "vsys_id": vsys_id}
                    response = requests.delete(url, headers=headers, params=del_profile_sf)
                    assert response.status_code == 200
                elif create_profile_ids[del_porfile_index]["profile_type"] == "insert_profile": # 删除insert
                    profile_id = create_profile_ids[del_porfile_index]["id"]
                    url = "{}/v1/policy/profile/insert_script".format(api_server)
                    del_profile_sf = {"ids": str(profile_id), "vsys_id": vsys_id}
                    response = requests.delete(url, headers=headers, params=del_profile_sf)
                    assert response.status_code == 200
                elif create_profile_ids[del_porfile_index]["profile_type"] == "run_script": # 删除run_script
                    profile_id = create_profile_ids[del_porfile_index]["id"]
                    url = "{}/v1/policy/profile/run_script".format(api_server)
                    del_profile_sf = {"ids": str(profile_id), "vsys_id": vsys_id}
                    response = requests.delete(url, headers=headers, params=del_profile_sf)
                    assert response.status_code == 200
                elif create_profile_ids[del_porfile_index]["profile_type"] == "dns_record": # 删除dns_record
                    profile_id = create_profile_ids[del_porfile_index]["id"]
                    url = "{}/v1/policy/profile/run_script".format(api_server)
                    del_profile_sf = {"ids": str(profile_id), "vsys_id": vsys_id}
                    response = requests.delete(url, headers=headers, params=del_profile_sf)
                    assert response.status_code == 200

if __name__ == '__main__':
    print("test")