# -*- coding: utf-8 -*-
import copy

from support.api_utils.util_statistics_template import UtilStatisticsTemplate


class DataTranslation:
    def data_translation(self, parameter, data):
        policy_type = data["policy_type"]
        temp_test_data = {
            "obj_condition": [],
            "profile_condition": [],
            "application": [],
            "do_log_1": 2
        }
        for key in data.keys():
            if key in {"condition"}:
                temp_test_data["obj_condition"] = self.push_object_data(data)
                if "application" in data["condition"].keys() and len(data["condition"]["application"]) > 0:
                    for app_index in range(len(data["condition"]["application"])):
                        temp_test_data["application"].append(data["condition"]["application"][app_index]["name"])
            if key in {"action_parameter", "profile"}:
                temp_test_data["profile_condition"] = self.push_profile_data(parameter, data)

        if len(temp_test_data["obj_condition"]) > 0:
            data["obj_condition"] = temp_test_data["obj_condition"]
        if len(temp_test_data["application"]) > 0:
            data["application"] = temp_test_data["application"]
        if len(temp_test_data["profile_condition"]) > 0:
            data["profile_condition"] = temp_test_data["profile_condition"]
        data["do_log_1"] = temp_test_data["do_log_1"]
        data["obj_condition_1"] = copy.deepcopy(temp_test_data["obj_condition"])
        #data["profile_condition_1"] = copy.deepcopy(temp_test_data["profile_condition"])

        # manipulation api test_data 数据补齐
        if policy_type == "pxy_manipulation":
            if data["rule_action"] == "deny":
                if "response_page" in data["action_parameter"]:
                    data["code_1"] = data["action_parameter"]["response_page"][0]["response_code"]
                elif "deny_response_text" in data["action_parameter"]:
                    data["code_1"] = data["action_parameter"]["deny_response_text"][0]["response_code"]
                    data["message_1"] = "text"    # 匹配原有api test_data数据
                else:
                    data["code_1"] = 404
                    data["message_1"] = "text"  # 匹配原有api test_data数据
            elif data["rule_action"] == "redirect":
                data["code_1"] = data["action_parameter"]["redirect_url"][0]["response_code"]
                data["to_1"] = data["action_parameter"]["redirect_url"][0]["redirect_url"]
            elif data["rule_action"] == "replace":
                replace_parameter_list = data["action_parameter"]["replace_parameter"]
                user_region = []
                for i in range(len(replace_parameter_list)):
                    rule_dict = {}
                    regex_name = replace_parameter_list[i]["regex"]
                    if regex_name == "on":
                        rule_dict["regex_enable"] = 1
                    else:
                        rule_dict["regex_enable"] = 0
                    rule_dict["search_in"] = replace_parameter_list[i]["search_in"]
                    rule_dict["find"] = replace_parameter_list[i]["find"]
                    rule_dict["replace_with"] = replace_parameter_list[i]["replace_with"]
                    user_region.append(copy.deepcopy(rule_dict))
                data["user_region"] = user_region
            elif data["rule_action"] == "edit_element":
                edit_element_parameter_list = data["action_parameter"]["edit_element_parameter"]
                user_region = []
                for i in range(len(edit_element_parameter_list)):
                    rule_dict = {}
                    search_scope = edit_element_parameter_list[i]["search_scope"]
                    rule_dict["search_scope"] = search_scope
                    if search_scope == "inside_element":
                        rule_dict["start_indicator"] = edit_element_parameter_list[i]["start_indicator"]
                    rule_dict["contained_keyword"] = edit_element_parameter_list[i]["contained_keyword"]
                    rule_dict["target_distance_from_matching"] = edit_element_parameter_list[i]["distance_from_anchor"]
                    rule_dict["element_treatment"] = edit_element_parameter_list[i]["treatment"]
                    user_region.append(copy.deepcopy(rule_dict))
                data["user_region"] = user_region
        return data
    
    def push_object_data(self, data):
        object = []
        for k, v in data["condition"].items():
            if type(v) == bool:
                continue
            if len(v) == 0:   # 空跳过
                continue
            if k == "source_ip":
                for i in range(len(v)):
                    temp = {
                        "name": v[i]["name"],
                        "attribute_name": "ATTR_SOURCE_IP",
                        "object_type": "ip",
                        "object_sub_type": "ip",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "ip_address": v[0]["item"][0]["item_value"],
                                    #     "port_range": "0-65535"
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["ip_address"] = v[i]["item"][u]["item_value"]
                        add_item_dict["port_range"] = "0-65535"
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "destination_ip":
                for i in range(len(v)):
                    temp = {
                        "name": v[i]["name"],
                        "attribute_name": "ATTR_DESTINATION_IP",
                        "object_type": "ip",
                        "object_sub_type": "ip",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "ip_address": v[0]["item"][0]["item_value"],
                                    #     "port_range": "0-65535"
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["ip_address"] = v[i]["item"][u]["item_value"]
                        add_item_dict["port_range"] = "0-65535"
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "internal_ip":
                for i in range(len(v)):
                    temp = {
                        "name": v[i]["name"],
                        "attribute_name": "ATTR_INTERNAL_IP",
                        "object_type": "ip",
                        "object_sub_type": "ip",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "ip_address": v[0]["item"][0]["item_value"],
                                    #     "port_range": "0-65535"
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["ip_address"] = v[i]["item"][u]["item_value"]
                        add_item_dict["port_range"] = "0-65535"
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "external_ip":
                for i in range(len(v)):
                    temp = {
                        "name": v[i]["name"],
                        "attribute_name": "ATTR_EXTERNAL_IP",
                        "object_type": "ip",
                        "object_sub_type": "ip",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "ip_address": v[0]["item"][0]["item_value"],
                                    #     "port_range": "0-65535"
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["ip_address"] = v[i]["item"][u]["item_value"]
                        add_item_dict["port_range"] = "0-65535"
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "source_port":
                for i in range(len(v)):
                    temp = {
                        "name": v[0]["name"],
                        "attribute_name": "ATTR_SOURCE_PORT",
                        "object_type": "port",
                        "object_sub_type": "port",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "port": v[0]["item"][0]["item_value"]
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["port"] = v[i]["item"][u]["item_value"]
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "destination_port":
                for i in range(len(v)):
                    temp = {
                        "name": v[0]["name"],
                        "attribute_name": "ATTR_DESTINATION_PORT",
                        "object_type": "port",
                        "object_sub_type": "port",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "port": v[0]["item"][0]["item_value"]
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["port"] = v[i]["item"][u]["item_value"]
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "internal_port":
                for i in range(len(v)):
                    temp = {
                        "name": v[0]["name"],
                        "attribute_name": "ATTR_INTERNAL_PORT",
                        "object_type": "port",
                        "object_sub_type": "port",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "port": v[0]["item"][0]["item_value"]
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["port"] = v[i]["item"][u]["item_value"]
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "external_port":
                for i in range(len(v)):
                    temp = {
                        "name": v[i]["name"],
                        "attribute_name": "ATTR_EXTERNAL_PORT",
                        "object_type": "port",
                        "object_sub_type": "port",
                        "is_negate": 0,
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "port": v[0]["item"][0]["item_value"]
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["port"] = v[i]["item"][u]["item_value"]
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "server_fqdn":
                for i in range(len(v)):
                    temp = {
                        "name": v[i]["name"],
                        "attribute_name": "ATTR_SERVER_FQDN",
                        "object_type": "fqdn",
                        "object_sub_type": "fqdn",
                        "object_list": [
                            {
                                "add_item_list": [
                                    # {
                                    #     "keyword_array": [
                                    #         v[0]["items"][0]["item_value"]
                                    #     ]
                                    # }
                                ]
                            }
                        ]
                    }
                    for u in range(len(v[i]["items"])):
                        # 添加多个item
                        add_item_dict = {
                            "keyword_array": []
                        }
                        add_item_dict["keyword_array"].append(v[i]["items"][u]["item_value"])
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    object.append(copy.deepcopy(temp))
            elif k == "sub_id":
                temp = {
                    "name": v[0]["name"],
                    "attribute_name": "ATTR_SUBSCRIBER_ID",
                    "object_type": "subscriberid",
                    "object_sub_type": "subscriberid",
                    "object_list": [
                        {
                            "add_item_list": [
                                {
                                    "keyword_array": [
                                        v[0]["item"][0]["item_value"]
                                    ]
                                }
                            ]
                        }
                    ]
                }
                object.append(copy.deepcopy(temp))
            elif k == "protocol_filed":
                for i in range(len(v)):
                    if v[i]["object_type"] == "url":
                        temp = {
                            "name": v[i]["name"],
                            "attribute_name": "ATTR_HTTP_URL",
                            "object_type": "url",
                            "object_sub_type": "url",
                            "object_list": [
                                {
                                    "add_item_list": [
                                        # {
                                        #     "keyword_array": [
                                        #         v[i]["items"][0]["item_value"]
                                        #     ]
                                        # }
                                    ]
                                }
                            ]
                        }
                        if v[i]["items"][0]["item_type"] == "ftp_url":
                            temp["attribute_name"] = "ATTR_FTP_URI"
                        for u in range(len(v[i]["items"])):
                            # 添加多个item
                            add_item_dict = {
                                "keyword_array": []
                            }
                            add_item_dict["keyword_array"].append(v[i]["items"][u]["item_value"])
                            temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                        object.append(copy.deepcopy(temp))
                    elif v[i]["object_type"] == "http_signature":
                        if v[i]["item"][0]["item_type"] == "request_header":
                            temp = {
                                "name": v[i]["name"],
                                "attribute_name": "ATTR_HTTP_REQ_HDR",
                                "object_type": "http_signature",
                                "object_sub_type": "http_signature",
                                "object_list": [
                                    {
                                        "context_name": v[i]["item"][0]["item_key"],
                                        "add_item_list": [
                                            # {
                                            #     "keyword_array": [
                                            #         v[i]["item"][0]["value"][0]
                                            #     ]
                                            # }
                                        ]
                                    }
                                ]
                            }
                            for u in range(len(v[i]["item"])):
                                # 添加多个item
                                add_item_dict = {
                                    "keyword_array": []
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
                        elif v[i]["item"][0]["item_type"] == "response_header":
                            temp = {
                                "name": v[i]["name"],
                                "attribute_name": "ATTR_HTTP_RES_HDR",
                                "object_type": "http_signature",
                                "object_sub_type": "http_signature",
                                "object_list": [
                                    {
                                        "context_name": v[i]["item"][0]["item_key"],
                                        "add_item_list": [
                                            # {
                                            #     "keyword_array": [
                                            #         v[i]["item"][0]["value"][0]
                                            #     ]
                                            # }
                                        ]
                                    }
                                ]
                            }
                            for u in range(len(v[i]["item"])):
                                # 添加多个item
                                add_item_dict = {
                                    "keyword_array": []
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
                    elif v[i]["object_type"] == "keywords":
                        if v[i]["item"][0]["item_type"] == "request_body":
                            temp = {
                                "name": v[i]["name"],
                                "attribute_name": "ATTR_HTTP_REQ_BODY",
                                "object_type": "keywords",
                                "object_sub_type": "keywords",
                                "object_list": [
                                    {
                                        "add_item_list": [
                                            # {
                                            #     "keyword_array": [
                                            #         v[i]["item"][0]["value"][0]
                                            #     ]
                                            # }
                                        ]
                                    }
                                ]
                            }
                            for u in range(len(v[i]["item"])):
                                # 添加多个item
                                add_item_dict = {
                                    "keyword_array": []
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
                        elif v[i]["item"][0]["item_type"] == "response_body":
                            temp = {
                                "name": v[i]["name"],
                                "attribute_name": "ATTR_HTTP_RES_BODY",
                                "object_type": "keywords",
                                "object_sub_type": "keywords",
                                "object_list": [
                                    {
                                        "add_item_list": [
                                            # {
                                            #     "keyword_array": [
                                            #         v[i]["item"][0]["value"][0]
                                            #     ]
                                            # }
                                        ]
                                    }
                                ]
                            }
                            for u in range(len(v[i]["item"])):
                                # 添加多个item
                                add_item_dict = {
                                    "keyword_array": []
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
                    elif v[i]["object_type"] == "boolean":
                        boolean_id_tmps = 3
                        if v[i]["name"] == 'True':
                            boolean_id_tmps = 2
                        filter_temp = {
                                "is_negate": 0,
                                "attribute_name": "ATTR_SSL_{}".format(v[i]["boolean_type"]),
                                "objects": [
                                    {
                                        "object_type": "boolean",
                                        "object_ids": [boolean_id_tmps]
                                    }
                                ],
                                "library_tags": [

                                ]
                            }
                        object.append(copy.deepcopy(filter_temp))

                    elif v[i]["object_type"] == "fqdn":
                        if v[i]["items"][0]["item_type"] == "cn" or v[i]["items"][0]["item_type"] == "san" or v[i]["items"][0]["item_type"] == "qname":
                            temp = {
                                "name": v[i]["name"],
                                "attribute_name": "ATTR_SSL_CN",
                                "object_type": "fqdn",
                                "object_sub_type": "fqdn",
                                "object_list": [
                                    {
                                        "add_item_list": []
                                    }
                                ]
                            }
                            if v[i]["items"][0]["item_type"] == "san":
                                temp["attribute_name"] = "ATTR_SSL_SAN"
                            if v[i]["items"][0]["item_type"] == "qname":
                                temp["attribute_name"] = "ATTR_DNS_QNAME"
                            for u in range(len(v[i]["items"])):
                                # 添加多个item
                                add_item_dict = {
                                    "keyword_array": []
                                }
                                add_item_dict["keyword_array"].append(v[i]["items"][u]["item_value"])
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
        return object
    
    def push_profile_data(self, parameter, data):
        policy_type = data["policy_type"]
        vsys_id = parameter["vsys_id"]
        profile = []
        if policy_type == "service_chaining":
            temp_profile = data["profile"]
            for i in range(len(temp_profile)):
                temp = {
                    "profile_type": "service_function_forwarder",
                    "name": temp_profile[i]["name"],
                    "type": "2",
                    "load_balance_method": temp_profile[i]["load_balance_method"],
                    "load_balance_localization": temp_profile[i]["load_balance_localization"],
                    "failure_action": temp_profile[i]["failure_action"],
                    "return_data": 1,
                    "op_action": "add",
                    "sf_condition": [
                        {
                            "profile_type": "service_function",
                            "name": "test_sc_api_vlan_none",
                            "profile_id": None,
                            "device_group": {
                                "tag": "device_group",
                                "value":"group-xxg-tsgx"
                            },
                            "admin_status": 1,
                            "connectivity": {
                                "method": "vxlan_g",
                                "dest_ip": "2.2.2.53"
                            },
                            "health_check": {
                                "method": "bfd",
                                "interval_ms": 200,
                                "retires": 5
                            },
                            "is_valid": 1,
                            "vsys_id": 1
                        }
                    ]
                }
                if temp_profile[i]["type"] == "steering":
                    temp["type"] = "1"
                elif temp_profile[i]["type"] == "mirroring":
                    temp["type"] = "2"
                if temp_profile[i]["profile_type"] == "create":
                    temp["op_action"] = "add"
                    for x in range(len(temp_profile[i]["service_functions"])):
                        temp["sf_condition"][x]["name"] = temp_profile[i]["service_functions"][x]["name"]
                        temp["sf_condition"][x]["device_group"]["tag"] = temp_profile[i]["service_functions"][x]["device_group"].split(":")[0]
                        temp["sf_condition"][x]["device_group"]["value"] = temp_profile[i]["service_functions"][x]["device_group"].split(":")[1]
                        if temp_profile[i]["service_functions"][x]["connectivity"].split(":")[0] == "VXLAN-G":
                            temp["sf_condition"][x]["connectivity"]["method"] = "vlan_g"
                            temp["sf_condition"][x]["connectivity"]["dest_ip"] = temp_profile[i]["service_functions"][x]["connectivity"].split(":")[1]
                        if temp_profile[i]["service_functions"][x]["health_check"].split(":")[0] == "Bfd":
                            temp["sf_condition"][x]["health_check"]["method"] = "bfd"
                            temp["sf_condition"][x]["health_check"]["interval_ms"] = temp_profile[i]["service_functions"][x]["health_check"].split(":")[1]
                            temp["sf_condition"][x]["health_check"]["retires"] = temp_profile[i]["service_functions"][x]["health_check"].split(":")[2]
                profile.append(temp)
        elif policy_type == "statistics":
            temp_profile = data["action_parameter"]["statistics_template"]
            util = UtilStatisticsTemplate()
            code, all_metrics = util.get_all_metrics_or_dimensions("metrics")
            if code != 200:
                return False, "Failed to obtain all Metric Field!"
            code, all_dimensions = util.get_all_metrics_or_dimensions("dimensions")
            if code != 200:
                return False, "Failed to obtain all Dimensions Field!"

            for j in range(len(temp_profile)):
                charts_tmp = []
                for m in range(len(temp_profile[j]["charts"])):
                    metrics_tmp = []
                    for n in temp_profile[j]["charts"][m]["metrics"]:
                        metric_tmp_array = n.split(":")
                        metric_tmp_source_columns_array = metric_tmp_array[0].split("+")
                        metric_tmp_source_columns_str = ""
                        for x in metric_tmp_source_columns_array:
                            if metric_tmp_source_columns_str == "":
                                metric_tmp_source_columns_str = all_metrics[x]
                            else:
                                metric_tmp_source_columns_str = "{}+{}".format(metric_tmp_source_columns_str, all_metrics[x])
                        metric_tmp = {"source_columns": metric_tmp_source_columns_str, "function": metric_tmp_array[1], "label": metric_tmp_array[2]}
                        metrics_tmp.append(metric_tmp)

                    dimensions_tmp = []
                    if "dimensions" in temp_profile[j]["charts"][m].keys():
                        dimension_array_tmp = []
                        for y in temp_profile[j]["charts"][m]["dimensions"]:
                            dimension_array_tmp.append(all_dimensions[y])
                        dimension_tmp = {
                            "source_columns": dimension_array_tmp,
                            "is_drilldown": 0
                        }
                        dimensions_tmp.append(dimension_tmp)
                    chart_tmp = {
                                "type": temp_profile[j]["charts"][m]["visualization_type"].lower(),
                                "metrics": metrics_tmp,
                                "dimensions": dimensions_tmp,
                                "order_by": temp_profile[j]["charts"][m]["order_by"],
                                #"order_by": None,#为适配后面API Metrics的Label随机生成,此处order_by设置为None
                                "limit": temp_profile[j]["charts"][m]["row_limit"],
                                "drilldown_limit": None,
                                "threshold": {
                                    "in_bytes": temp_profile[j]["charts"][m]["min_in_size"],
                                    "out_bytes": temp_profile[j]["charts"][m]["min_out_size"]
                                }
                            }
                    charts_tmp.append(chart_tmp)

                temp = {
                    "profile_type": "Statistics_Templates",
                    "name": temp_profile[j]["name"],
                    "chart_list": charts_tmp
                }
                """
                for t in range(temp_profile["charts"]):
                    for k in range(len(temp_profile["charts"][t]["metrics"])): 
                        temp["chart_list"][t]["metrics"][k]["source_columns"] = temp_profile["charts"][t]["metrics"][k].split(":")[0]
                        temp["chart_list"][t]["metrics"][k]["function"] = temp_profile["charts"][t]["metrics"][k].split(":")[1]
                """
                profile.append(temp)
        elif policy_type == "pxy_manipulation":
            temp_profile = data["action_parameter"]
            for k, v in temp_profile.items():
                if len(v) == 0:
                    continue
                if k == "response_page":
                    for t in range(len(v)):
                        temp = {
                            "profile_type": "response_page",
                            "format": "html",
                            "name": "auto_test_obj",
                            "content_name": "testa.html",
                            "return_data": 1
                        }
                        temp["name"] = v[t]["profile_file"]["name"]
                        temp["content_name"] = v[t]["profile_file"]["file"]
                        file_name = v[t]["profile_file"]["file"]
                        if file_name.endswith(".html"):
                            temp["format"] = "html"
                        elif file_name.endswith(".htm"):
                            temp["format"] = "htm"
                        else:
                            print("check file type: {}".format(file_name))
                        profile.append(copy.deepcopy(temp))
                elif k == "hijack_file":
                    element_type_replace_name = {
                        'gif': 'image/gif', 'jpeg': 'image/jpeg', 'png': 'image/png', 'svg+xml': 'image/svg+xml', 'svg': 'image/svg+xml',
                        'exe': 'application/x-msdos-program', 'apk': 'application/vnd.android.package-archive', 'html': 'text/html'
                    }
                    for t in range(len(v)):
                        temp = {
                            "profile_type": "hijack_files",
                            "content_type": "text/html",
                            "name": "auto_test_obj",
                            "content_name": "Files-test-5.png",
                            "vsys_id": 6,
                            "return_data": 1
                        }
                        temp["content_type"] = element_type_replace_name[v[t]["profile_file"]["file_type"]]
                        temp["name"] = v[t]["profile_file"]["name"]
                        temp["content_name"] = v[t]["profile_file"]["download_name"]
                        temp["vsys_id"] = vsys_id
                        profile.append(copy.deepcopy(temp))
                elif k == "insert_script":
                    insert_map = {
                        "Before Page Load": "before_page_load", "After Page Load": "after_page_load"
                    }
                    for t in range(len(v)):
                        temp = {
                            "profile_type": "insert_profile",
                            "is_enabled": 1,
                            "format": "js",
                            "name": "auto_test_obj",
                            "opAction": "add",
                            "insert_on": "before_page_load",
                            "content_name": "Create-Insert-Script-test1.js",
                            "isShared": 0,
                            "return_data": 1
                        }
                        temp["format"] = v[t]["profile_file"]["script_type"]
                        temp["name"] = v[t]["profile_file"]["name"]
                        if temp["format"] == "js":
                            temp["insert_on"] = insert_map[v[t]["profile_file"]["insert_position"]]
                        else:
                            temp["insert_on"] = None
                        temp["content_name"] = v[t]["profile_file"]["script"]
                        profile.append(copy.deepcopy(temp))
                elif k == "run_script":
                    for t in range(len(v)):
                        temp = {
                        "profile_type": "run_script",
                        "max_exec_time": 1000,
                        "name": "auto_test_obj",
                        "content_name": "run_script_insert.lua",
                        "return_data": 1
                       }
                        temp["max_exec_time"] = int(v[t]["profile_file"]["max_exec_time"])
                        temp["name"] = v[t]["profile_file"]["name"]
                        temp["content_name"] = v[t]["profile_file"]["script"]
                        profile.append(copy.deepcopy(temp))
                else:
                    print("no match {}".format(k))
        return profile
    
if __name__ == '__main__':
    policy_type = "dos_protection"
    test_data =  {
        "condition": {
            "source_ip": [
                {
                    "name": "dos_srcip",
                    "object_type": "ip",
                    "select_type": False,
                    "negate": False,
                    "item": [
                        {
                            "item_operation": "add",
                            "item_type": "ipv4",
                            "item_value": "1.1.1.1",
                        }
                    ]
                }
            ],
            "application": [
                {
                    "name": "http",
                    "object_type": "application",
                    "negate": False
                }
            ],
            "protocol_filed": [
                {
                    "name": "secy_ftp_url",
                    "object_type": "url",
                    "item_operation": "add",
                    "select_type": False,
                    "negate": False,
                    "items": [
                        {
                            "item_operation": "add",
                            "item_type": "url",
                            "item_value": "english"
                        }
                    ],
                },
                {
                    "name": "secy_http_sig",
                    "object_type": "http_signature",
                    "item_operation": "add",
                    "select_type": False,
                    "negate": False,
                    "statistics": "None",
                    "item": [
                        {
                            "item_operation": "add",
                            "item_type": "request_header",
                            "item_key": "User-Agent",
                            "item_value": "TEXT",
                            "value": [
                                "curl"
                            ]
                        }
                    ],
                }
            ],
        "action_parameter": {
            "statistics_template": [
                {
                    "name": "stats_table_all_bytes_dim_c_ip_s_ip",
                    "profile_type": "statistics_template",
                    "charts": [
                        {
                            "chart_name": "table_all_bytes_dim_c_ip_s_ip",
                            "visualization_type": "Table",
                            "metrics": [
                                "in_bytes:SUM:incoming bytes",
                                "out_bytes:SUM:outgoing bytes",
                                "in_bytes+out_bytes:SUM:all bytes"
                            ],
                            "dimensions": [
                                "client_ip",
                                "server_ip"
                            ],
                            "order_by": "all bytes",
                            "row_limit": "100",
                            "min_in_size": "0",
                            "min_out_size": "0"
                        }
                    ]
                }
            ]
        },
        "profile": [
                {
                    "name": "mirror_block_disabled_vxlan_activeip_bfd",
                    "profile_type": "create",
                    "type": "mirroring",
                    "load_balance_method": "hash_int-ip_and_ext-ip",
                    "load_balance_localization": "nearby",
                    "failure_action": "Block",
                    "service_functions": [
                        {
                            "name": "vxlan_activeip_bfd",
                            "profile_type": "create",
                            "device_group": "Device_Group:group-xxg-tsgx",
                            "connectivity": "VXLAN-G:2.2.2.53",
                            "health_check": "Bfd:10:2",
                            "enable": "off"
                        }
                    ]
                }
            ]
        }
    }
    translation = DataTranslation()
    temp_test_data = translation.data_translation(policy_type, test_data)