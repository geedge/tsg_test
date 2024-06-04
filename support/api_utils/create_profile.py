#!/usr/bin/python3
# coding=utf-8
import time
import requests
import json
import random
import string
import datetime
import copy

class CreateProfile():
    """
    创建profile接口api
    """
    def process_statistics_post_data(self, profile_statistics_template, post_statistics_data, vsys_id):
        """
        根据测试用例数据，构建post数据请求数据
        :param profile_statistics_template:    模板路径
        :param post_statistics_data:   测试用例数据
        :return:
        """
        # 读取profile_statistics_template模板文件
        with open(profile_statistics_template, "r", encoding="utf-8") as f_template:
            f_template_dict = json.load(f_template)
        # 处理请求数据，并合并到模板数据中
        chart_template_dict = copy.deepcopy(f_template_dict["statistics_template"]["dataview"]["charts"][0])     # 单个chart模板
        f_template_dict["statistics_template"]["dataview"]["charts"].clear()
        for _ in range(len(post_statistics_data["chart_list"])):
            f_template_dict["statistics_template"]["dataview"]["charts"].append(copy.deepcopy(chart_template_dict))
        for chart_idex in range(len(post_statistics_data["chart_list"])):     # 将数据值复制到post模板中
            chart_type = post_statistics_data["chart_list"][chart_idex]["type"]
            # 重组 type
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["display"]["type"] = chart_type
            # 判断是否需要 table_type的数值
            if chart_type == "table":    # 需要判断drill down = drill_down  regular
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["display"]["table_type"] = "regular"
            else:
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["display"]["table_type"] = ""
            # 重组metric
            metrics_dict = copy.deepcopy(f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"][0])
            # 清空原有的list内容，在重组
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"].clear()
            chart_pre_name = ""
            chart_after_name = ""
            for metric_index in range(len(post_statistics_data["chart_list"][chart_idex]["metrics"])):
                metrics_dict["source_columns"][0] = post_statistics_data["chart_list"][chart_idex]["metrics"][metric_index]["source_columns"]
                metrics_dict["function"]["name"] = post_statistics_data["chart_list"][chart_idex]["metrics"][metric_index]["function"]
                metrics_dict["alias"] = post_statistics_data["chart_list"][chart_idex]["metrics"][metric_index]["source_columns"].title()
                metrics_dict["alias"] = " ".join(metrics_dict["alias"].split("_"))    # 将_连接改为空格连接
                # 根据metric和function判断unit是什么
                metrics = metrics_dict["source_columns"][0]
                fun_name = metrics_dict["function"]["name"]
                if "bytes" in metrics:   # 和byte有关的meitric
                    if fun_name == "SUM":
                        unit = "bytes"
                    elif fun_name == "RATE":
                        unit = "Bps"
                    else:
                        unit = "bps"
                elif "flows" in metrics:
                    if fun_name == "SUM":
                        unit = "flows"
                    else:
                        unit = "fps"
                elif "sessions" in metrics:
                    if fun_name == "SUM":
                        unit = "sessions"
                    elif fun_name == "APPROX_COUNT_DISTINCT_HLLD":
                        unit = "sessions"
                    else:
                        unit = "sps"
                elif "syn_pkts" in metrics:
                    if fun_name == "SUM":
                        unit = "packets"
                    else:
                        unit = "pps"
                elif "ip_sketch" in metrics:
                    if fun_name == "APPROX_COUNT_DISTINCT_HLLD":
                        unit = "short"
                elif "ms_sketch" in metrics:
                    if fun_name == "PERCENTILES_HDR":
                        unit = "ms"
                else:
                    unit = "default"
                metrics_dict["unit"] = unit
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"].append(copy.deepcopy(metrics_dict))
                chart_pre_name = metrics_dict["source_columns"][0] + " "
            # 重组dimensions
            dimensions_dict = copy.deepcopy(f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["dimensions"][0])
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["dimensions"].clear()
            for dimension_index in range(len(post_statistics_data["chart_list"][chart_idex]["dimensions"])):
                dimensions_dict["source_columns"][0] = post_statistics_data["chart_list"][chart_idex]["dimensions"][dimension_index]["source_columns"][0]
                dimensions_dict["is_drilldown"] = post_statistics_data["chart_list"][chart_idex]["dimensions"][dimension_index]["is_drilldown"]
                if "__time" in dimensions_dict["source_columns"][0]:
                    dimensions_dict["alias"] = "Time"
                else:
                    dimensions_dict["alias"] = dimensions_dict["source_columns"][0].lower()
                    dimensions_dict["alias"] = " ".join(dimensions_dict["alias"].split("_"))  # 将_连接改为空格连接
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["dimensions"].append(copy.deepcopy(dimensions_dict))
                chart_after_name = dimensions_dict["source_columns"][0] + " "
            # 重组order by
            post_order_by = post_statistics_data["chart_list"][chart_idex]["order_by"]
            function_name = ""
            if post_order_by == None:
                if chart_type == "table" or chart_type == "bar":
                    f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] = f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"][0]["alias"]
                else:
                    f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] = ""
            else:
                for _ in range(len(post_statistics_data["chart_list"][chart_idex]["metrics"])):
                    if post_statistics_data["chart_list"][chart_idex]["metrics"][_]["source_columns"].lower().strip() == post_order_by.lower().strip():
                        function_name = post_statistics_data["chart_list"][chart_idex]["metrics"][_]["function"]
                        break
                    print("order_by参数错误：{}".format(post_order_by))
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] =  "{}_{}_autoapi".format(function_name.lower(), post_order_by.lower())
            # 重组 limit、 drilldown_limit
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["limit"] = str(post_statistics_data["chart_list"][chart_idex]["limit"])
            # 重组threshold
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["threshold"]["in_bytes"] =  int(post_statistics_data["chart_list"][chart_idex]["threshold"]["in_bytes"])
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["threshold"]["out_bytes"] =  int(post_statistics_data["chart_list"][chart_idex]["threshold"]["out_bytes"])
            # 重组 chart name
            if chart_after_name == "":
                chart_name = "{}".format(chart_pre_name)
            else:
                chart_name = "{}Distributed by{}".format(chart_pre_name, chart_after_name)
            chart_name = chart_name.strip()
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["name"] = chart_name
        # 重组statistics template name
        if post_statistics_data["name"] == "random_name":
            temp_list = []
            for _ in range(16):
                temp_list.append(random.choice(string.ascii_letters))
            r_letter = "".join(temp_list)
            formatted_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
            f_template_dict["statistics_template"]["name"] = "test_statistics_api_no{}_{}".format(r_letter, formatted_time)
        else:
            f_template_dict["statistics_template"]["name"] = post_statistics_data["name"]
        # 重组vsys id
        f_template_dict["vsys_id"] = vsys_id
        f_template_dict["statistics_template"]["vsys_id"] = vsys_id
        #f_template_dict["statistics_template"]["id"] = vsys_id
        return f_template_dict

    # 生成随机的vlan_id
    def random_vlan_id(self):
        random_num = random.randint(1, 4094)
        return random_num
    
    # 用传入的sf数据替换模板中的数据
    def process_sf_post_data(self, sf_template_path, sf_post_data,vsys_id):
        with open(sf_template_path, "r") as f:
            sf_template_dict = json.load(f)
        sf_template_dict["vsys_id"] = vsys_id
        sf_template_dict["service_function"]["vsys_id"] = vsys_id
        sf_template_dict["service_function"]["name"] = sf_post_data["name"]
        sf_template_dict["service_function"]["connectivity"]["method"] = sf_post_data["connectivity"]["method"]
        if sf_post_data["connectivity"]["method"] == "vxlan_g":
            sf_template_dict["service_function"]["connectivity"]["dest_ip"] = sf_post_data["connectivity"]["dest_ip"]
            sf_template_dict["service_function"]["health_check"]["method"] = sf_post_data["health_check"]["method"]
            if sf_post_data["health_check"]["method"] == "bfd":
                sf_template_dict["service_function"]["health_check"]["interval_ms"] = sf_post_data["health_check"]["interval_ms"]
                sf_template_dict["service_function"]["health_check"]["retires"] = sf_post_data["health_check"]["retires"]
        else:
            sf_template_dict["service_function"]["connectivity"]["int_vlan_tag"] = self.random_vlan_id()
            sf_template_dict["service_function"]["connectivity"]["ext_vlan_tag"] = self.random_vlan_id()
            sf_template_dict["service_function"]["health_check"]["method"] = "none"
        return sf_template_dict
    
    # 获取sf profile id
    def get_sf_id(self, headers, sf_tempalte_path, sf_post_data, api_host,vsys_id):
        # create_profile_id_dict = {"profile_type": "", "id": ""}
        profile_type = sf_post_data['profile_type']
        if profile_type == "service_function":
            process_post_data = self.process_sf_post_data(sf_tempalte_path, sf_post_data,vsys_id)
            url = "{}/v1/policy/profile/service_function".format(api_host)
            response = requests.post(url, headers=headers, json=process_post_data, verify=False)
            response_dict = response.json()
            sf_profile_id = response_dict["data"]["service_function"]["id"]
        return sf_profile_id

    # 用传入的sff数据替换模板中的数据
    def process_sff_post_data(self, sf_profile_id, sff_template_path, sff_post_data,vsys_id):
        with open(sff_template_path,"r") as f:
            sff_template_dict = json.load(f)
        sff_template_dict["vsys_id"] = vsys_id
        sff_template_dict["service_function_forwarder"]["name"] = sff_post_data["name"]
        sff_template_dict["service_function_forwarder"]["type"] = sff_post_data["type"]
        sff_template_dict["service_function_forwarder"]["load_balance_method"] = sff_post_data["load_balance_method"]
        sff_template_dict["service_function_forwarder"]["load_balance_localization"] = sff_post_data["load_balance_localization"]
        sff_template_dict["service_function_forwarder"]["failure_action"] = sff_post_data["failure_action"]
        if sff_post_data["failure_action"] == "re-dispatch":
            sff_template_dict["service_function_forwarder"]["unavailability_action"] = {}
            sff_template_dict["service_function_forwarder"]["unavailability_action"]["action"] = sff_post_data["unavailability_action"]["action"]
            if sff_post_data["unavailability_action"]["action"] == "bypass":
                sff_template_dict["service_function_forwarder"]["unavailability_action"]["health_service_func_lt"] = sff_post_data["unavailability_action"]["health_service_func_lt"]
        sff_template_dict["service_function_forwarder"]["service_func_profiles"] = sf_profile_id
        return sff_template_dict

    #用传入的dns_record数据代替模板数据
    def process_dns_record_post_data(self, dns_record_template_path, dns_record_post_data, vsys_id):
        with open(dns_record_template_path, "r") as f:
            dns_record_template_dict = json.load(f)
        dns_record_template_dict["vsys_id"] = vsys_id
        dns_record_template_dict["dns_record"]["type"] = dns_record_post_data["type"]
        dns_record_template_dict["dns_record"]["values"][0]["value"] = dns_record_post_data["value"]
        return dns_record_template_dict
    
    # 调用创建profile的接口
    def create_profile_from_template(self, path_dict, profile_data, token, api_host, vsys_id):
        """
        创建prfile接口
        :param path_dict:  模板路径 {}
        :param post_data:     请求数据
        :param token:
        :return:   例如：{'profile_type': 'Statistics_Templates', 'id': 1223, 'template_info': [{'template_id': 1223, 'chart_id': 2881, 'chart_type': 'table'}, {'template_id': 1223, 'chart_id': 2883, 'chart_type': 'table'}]}
        """
        # 处理请求体数据
        headers = {"Authorization": token}
        create_profile_id_dict = {"profile_type":"", "id":""}
        profile_type = profile_data["profile_type"]
        if profile_type == "Statistics_Templates":
            profile_statistics_template = path_dict["profile_statistics_template"]
            process_post_data = self.process_statistics_post_data(profile_statistics_template, profile_data, vsys_id)
            url = "{}/v1/policy/profile/statistics_template".format(api_host)
            headers["Content-Type"] = "application/json"
            #print(process_post_data)
            response = requests.post(url, headers=headers, json=process_post_data, verify=False)
            response_dict = response.json()
            # 处理返回数据，提取id
            #print(response_dict)
            profile_id = response_dict["data"]["statistics_template"]["id"]
            create_profile_id_dict["profile_type"] = profile_type
            create_profile_id_dict["id"] = profile_id
            path_profile_type = "statistics_template"
            template_info = self.search_statistics_templates(profile_id, path_profile_type, headers, api_host, vsys_id)
            create_profile_id_dict["template_info"] = template_info
            return create_profile_id_dict
        elif profile_type == "service_function_forwarder":
            profile_sff_template = path_dict["profile_sff_template"]
            profile_sf_template = path_dict["profile_sf_template"]
            sf_profile_id_list = []
            sf_condition_values = profile_data["sf_condition"]
            for sf_profile_data in sf_condition_values:
                sf_profile_id = self.get_sf_id(headers, profile_sf_template, sf_profile_data, api_host,vsys_id)
                sf_profile_id_list.append(sf_profile_id)
            process_post_data = self.process_sff_post_data(sf_profile_id_list, profile_sff_template, profile_data,vsys_id)
            url = "{}/v1/policy/profile/service_function_forwarder".format(api_host)
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json= process_post_data, verify=False)
            response_dict = response.json()
            sff_id = response_dict["data"]["service_function_forwarder"]["id"]
            create_profile_id_dict["profile_type"] = profile_type
            create_profile_id_dict["id"] = sff_id
            sff_info = self.search_sc_sff(sff_id, headers, api_host, profile_type, vsys_id)
            create_profile_id_dict["sff_info"] = sff_info
            return create_profile_id_dict
        elif profile_type == "response_page":
            files = {"file":("Response-Pages_1.html", open(path_dict["profiles_deny_path"], 'rb'), "text/plain")}
            del profile_data["profile_type"]
            # 添加vsys id
            profile_data["vsys_id"] = vsys_id
            url = "{}/v1/policy/profile/response_page".format(api_host)
            response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
            response_dict = response.json()
            profile_id = response_dict["data"]["response_page"]["id"]
            create_profile_id_dict["profile_type"] = profile_type
            create_profile_id_dict["id"] = profile_id
            return create_profile_id_dict
        elif profile_type == "hijack_files":
            files = {"file":("Create-hijack-Files-test-5.png", open(path_dict["profiles_hijack_file_path"], 'rb'), "text/plain")}
            del profile_data["profile_type"]
            # 添加vsys id
            profile_data["vsys_id"] = vsys_id
            url = "{}/v1/policy/profile/hijack_file".format(api_host)
            response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
            response_dict = response.json()
            profile_id = response_dict["data"]["hijack_file"]["id"]
            create_profile_id_dict["profile_type"] = profile_type
            create_profile_id_dict["id"] = profile_id
            return create_profile_id_dict
        elif profile_type == "insert_profile":
            files = {"file": ("Create-Insert-Script-test1.js", open(path_dict["profiles_insert_profile_path"], 'rb'), "text/plain")}
            del profile_data["profile_type"]
            # 添加vsys id
            profile_data["vsys_id"] = vsys_id
            url = "{}/v1/policy/profile/insert_script".format(api_host)
            response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
            response_dict = response.json()
            profile_id = response_dict["data"]["insert_script"]["id"]
            create_profile_id_dict["profile_type"] = profile_type
            create_profile_id_dict["id"] = profile_id
            return create_profile_id_dict
        elif profile_type == "run_script":
            files = {"file": ("run_script_hijack.lua", open(path_dict["profiles_run_script_path"], 'rb'), "text/plain")}
            del profile_data["profile_type"]
            # 添加vsys id
            profile_data["vsys_id"] = vsys_id
            url = "{}/v1/policy/profile/run_script".format(api_host)
            response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
            response_dict = response.json()
            profile_id = response_dict["data"]["run_script"]["id"]
            create_profile_id_dict["profile_type"] = profile_type
            create_profile_id_dict["id"] = profile_id
            return create_profile_id_dict
        elif profile_type == "dns_record":
            profile_dns_record_template = path_dict["profile_dns_record_template"]
            process_post_data = self.process_dns_record_post_data(profile_dns_record_template, profile_data, vsys_id)
            url = "{}/v1/policy/profile/dns_record".format(api_host)
            response = requests.post(url, headers=headers, json=process_post_data)
            response_dict = response.json()
            profile_id = response_dict["data"]["dns_record"]["id"]
            create_profile_id_dict["profile_type"] = profile_type
            create_profile_id_dict["id"] = profile_id
            return create_profile_id_dict
        else:
            print("需要补充其它profile对象请求体数据处理函数")
    
    def search_statistics_templates(self, template_id, profile_type, headers, api_host, vsys_id):
        url = "{}/v1/policy/profile/{type}/{id}".format(api_host, type=profile_type, id=template_id)
        params_dict = {
            "vsys_id": vsys_id
        }
        response = requests.get(url, params=params_dict, headers=headers)
        # 打桩数据
        r_dict = response.json()
        template_info = []
        chart_info = {"template_id":template_id, "chart_id":0, "chart_type":""}
        for chart in r_dict["data"]["statistics_template"]["dataview"]["charts"]:
            chart_info["chart_type"] = chart["display"]["type"]
            chart_info["chart_id"] = chart["id"]
            chart_info["version"] = chart["version"]
            chart_info["sql"] = chart["query"]["sql"]
            template_info.append(copy.deepcopy(chart_info))
        return template_info

    #搜索sf并获取返回结果中的sf相关信息
    def search_sc_sff(self, sff_id, headers, api_host, profile_type, vsys_id):
        url = "{}/v1/policy/profile/{type}/{ids}".format(api_host, type=profile_type, ids=sff_id)
        params_dict = {
            "vsys_id": vsys_id
        }
        response = requests.get(url=url, params=params_dict, headers=headers)
        r_dict = response.json()
        sff_info = {"id": sff_id, "type":"","sf_info":[]}
        if(len(r_dict["data"]["service_function_forwarder"]["service_func_profiles"])>0):
            sf_profile_id_list = r_dict["data"]["service_function_forwarder"]["service_func_profiles"]
            for i in sf_profile_id_list:
                sf_profile_id = i
                sff_info["sf_info"].append(self.search_sc_sf(sf_profile_id, headers, api_host,vsys_id))
            sff_info["type"] = r_dict["data"]["service_function_forwarder"]["type"]
            sff_info["failure_action"] = r_dict["data"]["service_function_forwarder"]["failure_action"]
        return sff_info

    #搜索sff并获取返回结果中的相关信息
    def search_sc_sf(self, sf_id, headers, api_host,vsys_id):
        url = "{}/v1/policy/profile/{type}/{id}".format(api_host, type="service_function", id=sf_id)
        params_dict = {
            "vsys_id": vsys_id
        }
        response = requests.get(url, params=params_dict, headers=headers)
        r_dict = response.json()
        sf_info = {"id": sf_id, "connectivity": {"method": ""}, "health_check":{"method": ""}}
        if r_dict["data"]["service_function"]["connectivity"]["method"] == "vxlan_g":
            sf_info["connectivity"]["method"] = r_dict["data"]["service_function"]["connectivity"]["method"]
            sf_info["connectivity"]["dest_ip"] = r_dict["data"]["service_function"]["connectivity"]["dest_ip"]
            sf_info["health_check"]["method"] = r_dict["data"]["service_function"]["health_check"]["method"]
        else:
            sf_info["connectivity"]["method"] = r_dict["data"]["service_function"]["connectivity"]["method"]
            sf_info["health_check"]["method"] = "none"
        return sf_info

if __name__ == '__main__':
    print("test")