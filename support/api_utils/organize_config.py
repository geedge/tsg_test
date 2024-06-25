import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import random
import requests
import json


class OrganizeConfig():
    def organize_cfg(self, parameter, test_data, template_path):
        # 变量初始化
        api_server = parameter["api_server"]
        run_env = parameter["env"]
        vsys_id = parameter["vsys_id"]
        token = test_data["token"]
        create_ip_ids, create_subid_ids, create_fqdn_ids, create_url_ids, create_flag_ids, create_keywords_ids, create_account_ids, create_http_signature_ids, create_http_signature_ids, create_profile_ids, create_policies_ids, create_geo_name_ids = [], [], [], [], [], [], [], [], [], [], [], []
        statistics_sc_info_list, policy_statistics_template_chart_info, policy_sc_sff_sf_info, temp_profile_list = [], [], [], []
        policy_define = self.get_policy_define(token, test_data["rule_id"], test_data["policy_type"], api_server,
                                               vsys_id)
        # statistics和sc需要随机ip
        if test_data["policy_type"] == "statistics":
            # 从Statistics Rule定义信息中获取流量验证所需数据格式
            for policy in policy_define:
                create_policies_ids.append({'statistics': policy["id"]})
                for source in policy["source"]:
                    if source["attribute_name"] == "ATTR_SOURCE_IP":
                        for object in source["objects"]:
                            if object["object_type"] == "ip" and object["object_sub_type"] == "ip":
                                for id in object["object_ids"]:
                                    create_ip_ids.append(id)
                    for source in policy["source"]:
                        if source["attribute_name"] == "ATTR_SOURCE_IP":
                            for object in source["objects"]:
                                if object["object_type"] == "ip" and object["object_sub_type"] == "ip_learning":
                                    for id in object["object_ids"]:
                                        create_ip_ids.append(id)
                for destination in policy["destination"]:
                    if destination["attribute_name"] == "ATTR_DESTINATION_IP":
                        for object in destination["objects"]:
                            if object["object_type"] == "ip" and object["object_sub_type"] == "ip":
                                for id in object["object_ids"]:
                                    create_ip_ids.append(id)
                user_region = policy["user_region"]
                if user_region != {}:
                    template_id = user_region["template_id"]
                    template_define = self.get_template_define(token, template_id, "statistics_template",
                                                               api_server, vsys_id)
                    for template in template_define:
                        template_temp = []
                        for chart in template["dataview"]["charts"]:
                            chart_info = {"template_id": 0, "chart_id": 0, "chart_type": "line", "version": 0,
                                          'sql': ""}
                            chart_info["template_id"] = template_id
                            chart_info["chart_id"] = chart["id"]
                            chart_info["chart_type"] = chart["display"]["type"]
                            chart_info["version"] = chart["version"]
                            chart_info["sql"] = chart["query"]["sql"]
                            template_temp.append(chart_info)
                            statistics_info = {}
                            statistics_info["rule_id"] = test_data["rule_id"]
                            statistics_info["template_id"] = template_id
                            statistics_info["chart_id"] = chart["id"]
                            statistics_info["chart_type"] = chart["display"]["type"]
                            statistics_info["version"] = chart["version"]
                            statistics_info["sql"] = chart["query"]["sql"]
                            statistics_sc_info_list.append(statistics_info)
                        create_profile_ids.append({'profile_type': 'Statistics_Templates', 'id': 50555, 'template_info': template_temp})
                        template_info = {"profile_type": "", "id": 0, "template_info": []}
                        template_info["profile_type"] = ""
                        template_info["id"] = template_id
                        template_info["template_info"] = template_temp

        cfg_list = {}
        cfg_list["create_ip_ids"] = create_ip_ids
        cfg_list["create_subid_ids"] = create_subid_ids
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
        # cfg_list["timeout_result"] = timeout_result
        return cfg_list

    def generate_random_ip(self, config, run_env):
        # statistics中将ip改为随机
        if "condition" in config.keys():
            for obj in config["condition"]:
                if "source_ip" in obj.keys() or "destination_ip" in obj.keys():
                    src_ip = obj["source_ip"][0]["item"][0]["item_value"]
                    if "default" in src_ip:
                        src_ip = "10.64.77.11"
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
                        obj["source_ip"][0]["item"][0]["item_value"] = new_src_ip
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
                        obj["object_list"][0]["add_item_list"][0]["ip_address"] = new_two_ip
        print("Config random ip for statistics and sc rule.")
        return config

    def get_policy_define(self, token, rule_id, rule_type, api_host, vsys_id):
        try:
            # 请求接口查询metric
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = api_host + "/v1/policy/rule"
            # ?page_size=20&page_no=1&ids=849138&type=statistics&is_enabled=&with_sub_vsys=1&page_location=0&location_id=&location_key=&vsys_id=1
            query_condition = {"page_size": 20, "page_no": 1, "ids": rule_id, "type": rule_type,
                            "is_enabled": "True", "with_sub_vsys": 1, "page_location": "oneshot", "location_key": "json",
                            "vsys_id": vsys_id}
            url = (api_host + f"/v1/policy/rule?page_size=20&page_no=1&ids={rule_id}&type={rule_type}&is_enabled=&with_sub_vsys=1&page_location=0&location_id=&location_key=&vsys_id={str(vsys_id)}")
            response = requests.get(url, headers=headers, verify=False)
            assert response.status_code == 200
            response = json.loads(response.text)
            result = response['data']['rules']
            return result
        except AssertionError as e:
                print(f"AssertionError: {e}")

    def get_template_define(self, token, template_id, template_type, api_host, vsys_id):
        try:
            # 请求接口查询metric
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = (api_host + f"/v1/policy/profile/statistics_template?page_size=20&page_no=1&ids={template_id}&vsys_id={str(vsys_id)}")
            response = requests.get(url, headers=headers, verify=False)
            assert response.status_code == 200
            response = json.loads(response.text)
            result = response['data']['statistics_templates']
            return result
        except AssertionError as e:
            print(f"AssertionError: {e}")


if __name__ == "__main__":
    print("test")