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
                if "ip_protocol" in data["condition"].keys() :
                    temp_test_data["ip_protocol"] = data["condition"]["ip_protocol"]
            if key in {"action_parameter", "profile"}:
                temp_test_data["profile_condition"] = self.push_profile_data(parameter, data)
        if len(temp_test_data["obj_condition"]) > 0:
            data["obj_condition"] = temp_test_data["obj_condition"]
        if len(temp_test_data["application"]) >= 0:
            data["application"] = temp_test_data["application"]
        if "ip_protocol" in data["condition"].keys() and len(temp_test_data["ip_protocol"]) >= 0:
            data["ip_protocol"] = temp_test_data["ip_protocol"]
        if len(temp_test_data["profile_condition"]) > 0:
            data["profile_condition"] = temp_test_data["profile_condition"]
        data["do_log_1"] = temp_test_data["do_log_1"]
        data["obj_condition_1"] = copy.deepcopy(temp_test_data["obj_condition"])
        if "effective_devices" in data.keys() and len(data["effective_devices"]) > 0:
            effective_range = {"tag_sets": [
                                      # [
                                      #     {
                                      #         "value": [
                                      #             # "center-xxg-tsgx"
                                      #         ],
                                      #         "tag": "data_center"
                                      #     }
                                      # ]
                                  ]
                              }
            for i in range(len(data["effective_devices"])):
                temp = {
                    "value": [
                        # "center-xxg-tsgx"
                    ],
                    "tag": "data_center"
                }
                effective_devices = data["effective_devices"][i].split(",")
                for j in range(len(effective_devices)):
                    temp["value"].append(effective_devices[j])
                if "center" in data["effective_devices"][i]:
                    temp["tag"] = "data_center"
                else:
                    temp["tag"] = "device_group"
                effective_range["tag_sets"].append(copy.deepcopy([temp]))
            data["effective_range"] = effective_range
        if "log_options" in data.keys():
            if data["log_options"] == "all":    # 1
                data["do_log_1"] = 1
        # manipulation api test_data 数据补齐
        if policy_type == "pxy_manipulation":
            if data["rule_action"] == "deny":
                if "response_page" in data["action_parameter"]:
                    data["code_1"] = data["action_parameter"]["response_page"][0]["response_code"]
                elif "deny_response_text" in data["action_parameter"]:
                    data["code_1"] = data["action_parameter"]["deny_response_text"][0]["response_code"]
                    data["message_1"] = data["action_parameter"]["deny_response_text"][0]["response_content"]   # 匹配原有api test_data数据
                else:
                    data["code_1"] = 404
                    data["message_1"] = "text"  # 匹配原有api test_data数据
            elif data["rule_action"] == "redirect":
                data["code_1"] = data["action_parameter"]["redirect_url"][0]["response_code"]
                data["to_1"] = data["action_parameter"]["redirect_url"][0]["redirect_url"]
            elif data["rule_action"] == "replace":
                replace_parameter_list = data["action_parameter"]["replace_parameter"]
                user_region = []
                map_search_in = {
                    "HTTP Request-URI": "http_req_uri",
                    "HTTP Request Body": "http_req_body",
                    "HTTP Response Body": "http_resp_body",
                    "HTTP Request Header": "http_req_header",
                    "HTTP Response Header": "http_resp_header"
                }
                for i in range(len(replace_parameter_list)):
                    rule_dict = {}
                    regex_name = replace_parameter_list[i]["regex"]
                    if regex_name == "on":
                        rule_dict["regex_enable"] = 1
                    else:
                        rule_dict["regex_enable"] = 0
                    search_in = replace_parameter_list[i]["search_in"]
                    rule_dict["search_in"] = map_search_in[search_in]
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
        elif policy_type == "security":
            if data["rule_action"] == "deny":
                if len(data["condition"]["sub_action"])>0:
                    if data["condition"]["sub_action"][0]["type"] == "drop":
                        data["method_1"] = "drop"
                        if data["condition"]["sub_action"][0]["send_tcp_rst"] == False:
                            data["send_tcp_reset_1"] = 0
                        if data["condition"]["sub_action"][0]["send_icmp_unreachable"] == True:
                            data["send_icmp_unreachable_1"] = 1
                    elif data["condition"]["sub_action"][0]["type"] == "rate_limit":
                        data["method_1"] = "rate_limit"
                        bps = int(float(data["condition"]["sub_action"][0]["rate_value"])*1000)
                        data["bps_1"] = bps
                    elif data["condition"]["sub_action"][0]["type"] == "tamper":
                        data["method_1"] = "tamper"

                    elif data["condition"]["sub_action"][0]["type"] == "block":
                        if data["condition"]["application"][0]["name"] == "mail":
                            data["method_1"] = "block"
                            data["code_1"] = data["condition"]["sub_action"][0]["code"]
                        elif data["condition"]["application"][0]["name"] == "http":
                            data["method_1"] = "block"
                            data["code_1"] = data["condition"]["sub_action"][0]["code"]
                            if "action_parameter" not in data:
                                data["message_1"] = data["condition"]["sub_action"][0]["content"]
                    elif data["condition"]["sub_action"][0]["type"] == "alert":
                        data["method_1"] = "alert"
                        data["code_1"] = data["condition"]["sub_action"][0]["code"]
                        if "action_parameter" not in data and data["code_1"] == 200:
                                data["message_1"] = data["condition"]["sub_action"][0]["content"]
                    elif data["condition"]["sub_action"][0]["type"] == "redirect":
                        data["method_1"] = "redirect"
                        if data["condition"]["application"][0]["name"] == "http":
                            data["code_1"] = 303
                            data["to_1"] = data["condition"]["sub_action"][0]["to_url"]
                        elif data["condition"]["application"][0]["name"] == "dns":
                            if len(data["profile"]) == 0:
                                resolution = []
                                resolution_dict = {}
                                for resolution_item in data["condition"]["sub_action"][0]["resolution"]:
                                    answer_dict = {}
                                    answer = []
                                    resolution_dict["qtype"] = resolution_item["qtype"]
                                    for answer_item in resolution_item["answer"]:
                                        answer_dict["atype"] = answer_item["atype"]
                                        answer_dict["value"] = answer_item["answer_value"]
                                        ttl_range = answer_item["ttl"]
                                        ttl_split = ttl_range.split('-')
                                        answer_dict["ttl"] = {}
                                        answer_dict["ttl"]["min"] = int(ttl_split[0])
                                        answer_dict["ttl"]["max"] = int(ttl_split[1])
                                        answer.append(copy.deepcopy(answer_dict))
                                    resolution_dict["answer"] = answer
                                    resolution.append(copy.deepcopy(resolution_dict))
                            else:
                                resolution = []
                                resolution_dict = {}
                                answer = []
                                answer_dict = {}
                                # resolution 部分
                                for resolution_item in data["condition"]["sub_action"][0]["resolution"]:
                                    resolution_dict["qtype"] = resolution_item["qtype"]
                                    for answer_item in resolution_item["answer"]:
                                        answer_dict["atype"] = answer_item["atype"]
                                        answer_dict["record_id"] = ""
                                        answer_dict["selected_num"] = 1
                                        ttl_range = answer_item["ttl"]
                                        ttl_split = ttl_range.split('-')
                                        answer_dict["ttl"] = {}
                                        answer_dict["ttl"]["min"] = int(ttl_split[0])
                                        answer_dict["ttl"]["max"] = int(ttl_split[1])
                                        answer.append(copy.deepcopy(answer_dict))
                                    resolution_dict["answer"] = answer
                                # profile 部分
                                data["profile_condition_1"] = []
                                data["profile_condition_1"].append({})
                                data["profile_condition_1"][0]["profile_type"] = "dns_record"
                                data["profile_condition_1"][0]["type"] = data["profile"][0]["type"]
                                data["profile_condition_1"][0]["value"] = data["profile"][0]["items"][0]
                            data["resolution_1"] = resolution
                else:
                    if data["condition"]["sub_action_override"] == False:
                        data["method_1"] = "default"
            if data["rule_action"] == "shunt":
                data["do_log_1"] = 0
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
                                    #     "op": "add",
                                    #     "ip": v[0]["item"][0]["item_value"],
                                    #     "interval": "0-65535"
                                    # }
                                ]
                            }
                        ]
                    }
                    if "negate" in v[i]:
                        temp["is_negate"] = v[i]["negate"]
                    for u in range(len(v[i]["item"])):
                        # 添加多个item
                        add_item_dict = {}
                        add_item_dict["ip"] = v[i]["item"][u]["item_value"]
                        add_item_dict["interval"] = "0-65535"
                        add_item_dict["op"] =  v[i]["item"][u]["item_operation"]
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    temp["is_negate"] = v[i]["negate"]
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
            elif k == "device":
                for i in range(len(v)):
                    if v[i]["item"][0]["item_type"] == "imsi":
                        temp = {
                            "name": v[i]["name"],
                            "attribute_name": "ATTR_GTP_IMSI",
                            "object_type": "mobile_identity",
                            "object_sub_type": "imsi",
                            "is_negate": 0,
                            "object_list": [
                                {
                                    "add_item_list": [
                                    ]
                                }
                            ]
                        }
                        for u in range(len(v[i]["item"])):
                            # 添加多个item
                            add_item_dict = {
                                "keyword_array": []
                            }
                            add_item_dict["keyword_array"].append(v[i]["item"][u]["item_value"])
                            temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                        object.append(copy.deepcopy(temp))
                    elif v[i]["item"][0]["item_type"] == "phone_number":
                        temp = {
                            "name": v[i]["name"],
                            "attribute_name": "ATTR_GTP_PHONE_NUMBER",
                            "object_type": "mobile_identity",
                            "object_sub_type": "phone_number",
                            "is_negate": 0,
                            "object_list": [
                                {
                                    "add_item_list": [
                                    ]
                                }
                            ]
                        }
                        for u in range(len(v[i]["item"])):
                            # 添加多个item
                            add_item_dict = {
                                "keyword_array": []
                            }
                            add_item_dict["keyword_array"].append(v[i]["item"][u]["item_value"])
                            temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                        object.append(copy.deepcopy(temp))
                    elif v[i]["item"][0]["item_type"] == "imei":
                        temp = {
                            "name": v[i]["name"],
                            "attribute_name": "ATTR_GTP_IMEI",
                            "object_type": "mobile_identity",
                            "object_sub_type": "imei",
                            "is_negate": 0,
                            "object_list": [
                                {
                                    "add_item_list": [
                                    ]
                                }
                            ]
                        }
                        for u in range(len(v[i]["item"])):
                            # 添加多个item
                            add_item_dict = {
                                "keyword_array": []
                            }
                            add_item_dict["keyword_array"].append(v[i]["item"][u]["item_value"])
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
                    if "negate" in v[i]:
                        temp["is_negate"] = v[i]["negate"]
                    for u in range(len(v[i]["items"])):
                        # 添加多个item
                        add_item_dict = {
                            "keyword_array": []
                        }
                        add_item_dict["keyword_array"].append(v[i]["items"][u]["item_value"])
                        temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                    temp["is_negate"] = v[i]["negate"]
                    object.append(copy.deepcopy(temp))
            elif k == "apn":
                for i in range(len(v)):
                    temp = {
                        "name": v[i]["name"],
                        "attribute_name": "ATTR_GTP_APN",
                        "object_type": "apn",
                        "object_sub_type": "apn",
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
                    temp["is_negate"] = v[i]["negate"]
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
                                        v[0]["items"][0]["item_value"]
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
                                    "keyword_array": [],
                                    "is_hexbin": 0,
                                    "expr_type": 0
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                if v[i]["item"][u]["item_value"] == "HEX":
                                    add_item_dict["is_hexbin"] = 1
                                    add_item_dict["expr_type"] = 0
                                elif v[i]["item"][u]["item_value"] == "REGEX":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 2
                                elif "range" in v[i]["item"][u].keys() and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 3
                                    add_item_dict["range"] = v[i]["item"][u]["range"]
                                elif "&" in v[i]["item"][u]["value"][0] and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 1
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
                                    "keyword_array": [],
                                    "is_hexbin": 0,
                                    "expr_type": 0
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                if v[i]["item"][u]["item_value"] == "HEX":
                                    add_item_dict["is_hexbin"] = 1
                                    add_item_dict["expr_type"] = 0
                                elif v[i]["item"][u]["item_value"] == "REGEX":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 2
                                elif "range" in v[i]["item"][u].keys() and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 3
                                    add_item_dict["range"] = v[i]["item"][u]["range"]
                                elif "&" in v[i]["item"][u]["value"][0] and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 1
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
                                    "keyword_array": [],
                                    "is_hexbin": 0,
                                    "expr_type": 0
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                if v[i]["item"][u]["item_value"] == "HEX":
                                    add_item_dict["is_hexbin"] = 1
                                    add_item_dict["expr_type"] = 0
                                elif v[i]["item"][u]["item_value"] == "REGEX":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 2
                                elif "range" in v[i]["item"][u].keys() and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 3
                                    add_item_dict["range"] = v[i]["item"][u]["range"]
                                elif "&" in v[i]["item"][u]["value"][0] and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 1
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
                                    "keyword_array": [],
                                    "is_hexbin": 0,
                                    "expr_type": 0
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                if v[i]["item"][u]["item_value"] == "HEX":
                                    add_item_dict["is_hexbin"] = 1
                                    add_item_dict["expr_type"] = 0
                                elif v[i]["item"][u]["item_value"] == "REGEX":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 2
                                elif "range" in v[i]["item"][u].keys() and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 3
                                    add_item_dict["range"] = v[i]["item"][u]["range"]
                                elif "&" in v[i]["item"][u]["value"][0] and v[i]["item"][u]["item_value"] == "TEXT":
                                    add_item_dict["is_hexbin"] = 0
                                    add_item_dict["expr_type"] = 1
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
                        elif v[i]["item"][0]["item_type"] == "mail_subject":
                            temp = {
                                "name": v[i]["name"],
                                "attribute_name": "ATTR_MAIL_SUBJECT",
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
                                    "keyword_array": [],
                                    "is_hexbin": 0,
                                    "expr_type": 0
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
                        elif v[i]["item"][0]["item_type"] == "ftp_content":
                            temp = {
                                "name": v[i]["name"],
                                "attribute_name": "ATTR_FTP_CONTENT",
                                "object_type": "keywords",
                                "object_sub_type": "keywords",
                                "object_list": [
                                    {
                                        "add_item_list": [],
                                    }
                                ]
                            }
                            for u in range(len(v[i]["item"])):
                                # 添加多个item
                                add_item_dict = {
                                    "keyword_array": [],
                                    "is_hexbin": 0,
                                    "expr_type": 0
                                }
                                add_item_dict["keyword_array"].append(v[i]["item"][u]["value"][0])
                                temp["object_list"][0]["add_item_list"].append(copy.deepcopy(add_item_dict))
                            object.append(copy.deepcopy(temp))
                    elif v[i]["object_type"] == "account":
                        temp = {
                            "name": v[i]["name"],
                            "attribute_name": "ATTR_MAIL_ACCOUNT",
                            "object_type": "account",
                            "object_sub_type": "account",
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
                        if v[i]["items"][0]["item_type"] == "ftp_account":
                            temp["attribute_name"] = "ATTR_FTP_ACCOUNT"
                        if v[i]["items"][0]["item_type"] == "mail_from":
                            temp["attribute_name"] = "ATTR_MAIL_FROM"
                        if v[i]["items"][0]["item_type"] == "mail_to":
                            temp["attribute_name"] = "ATTR_MAIL_TO"
                        for u in range(len(v[i]["items"])):
                            # 添加多个item
                            add_item_dict = {
                                "keyword_array": []
                            }
                            add_item_dict["keyword_array"].append(v[i]["items"][u]["item_value"])
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
                        if filter_temp["attribute_name"] == "ATTR_SSL_NO SNI":
                            filter_temp["attribute_name"] = "ATTR_SSL_NO_SNI"
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
            load_balance_dict = {"hash_int-ip": "hash-int-ip", "hash_ext-ip" : "hash-ext-ip",
                "hash_innermost_int-ip" : "hash-innermost-int-ip", "hash_int-ip_and_ext-ip": "hash-int-ip-and-ext-ip"}
            temp_profile = data["profile"]
            for i in range(len(temp_profile)):
                temp = {
                    "profile_type": "service_function_forwarder",
                    "name": temp_profile[i]["name"],
                    "type": "2",
                    "load_balance_method": "",
                    "load_balance_localization": temp_profile[i]["load_balance_localization"],
                    "failure_action": "",
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
                            },
                            "is_valid": 1,
                            "vsys_id": 1
                        }
                    ]
                }
                load_balance_method = temp_profile[i]["load_balance_method"]
                temp["load_balance_method"] = load_balance_dict[load_balance_method]
                temp["failure_action"] = temp_profile[i]["failure_action"].split(":")[0].lower()
                if temp["failure_action"] == "re-dispatch":
                    temp["unavailability_action"] = {}
                    temp["unavailability_action"]["action"] = temp_profile[i]["failure_action"].split(":")[1].lower()
                    if temp["unavailability_action"]["action"] == "bypass":
                        temp["unavailability_action"]["health_service_func_lt"] = int(temp_profile[i]["failure_action"].split(":")[2])
                    else:
                        temp["unavailability_action"]["health_service_func_lt"] = 0
                if temp_profile[i]["type"] == "steering":
                    temp["type"] = "1"
                elif temp_profile[i]["type"] == "mirroring":
                    temp["type"] = "2"
                if temp_profile[i]["profile_type"] == "create":
                    temp["op_action"] = "add"
                    for x in range(len(temp_profile[i]["service_functions"])):
                        temp["sf_condition"][x]["name"] = temp_profile[i]["service_functions"][x]["name"]
                        temp["sf_condition"][x]["device_group"]["tag"] = temp_profile[i]["service_functions"][x]["device_group"].split(":")[0].lower()
                        temp["sf_condition"][x]["device_group"]["value"] = temp_profile[i]["service_functions"][x]["device_group"].split(":")[1].lower()
                        if temp_profile[i]["service_functions"][x]["connectivity"].split(":")[0] == "VXLAN-G":
                            temp["sf_condition"][x]["connectivity"]["method"] = "vxlan_g"
                            temp["sf_condition"][x]["connectivity"]["dest_ip"] = temp_profile[i]["service_functions"][x]["connectivity"].split(":")[1]
                        if temp_profile[i]["service_functions"][x]["connectivity"].split(":")[0] == "Layer_2_Switch":
                            temp["sf_condition"][x]["connectivity"]["method"] = "layer2_switch"
                        if temp_profile[i]["service_functions"][x]["health_check"].split(":")[0] == "BFD":
                            temp["sf_condition"][x]["health_check"]["method"] = "bfd"
                            temp["sf_condition"][x]["health_check"]["interval_ms"] = temp_profile[i]["service_functions"][x]["health_check"].split(":")[1]
                            temp["sf_condition"][x]["health_check"]["retires"] = temp_profile[i]["service_functions"][x]["health_check"].split(":")[2]
                        else:
                            temp["sf_condition"][x]["health_check"]["method"] = temp_profile[i]["service_functions"][x]["health_check"]

                        if temp_profile[i]["service_functions"][x]["enable"] == "on":
                            temp["sf_condition"][x]["admin_status"] = 1
                        else:
                            temp["sf_condition"][x]["admin_status"] = 0
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
                    chart_tmp = {}
                    series_limit_flag = False
                    if "dimensions" in temp_profile[j]["charts"][m].keys():
                        for y in temp_profile[j]["charts"][m]["dimensions"]:
                            series_limit_flag = True
                            dimension_array_tmp = []
                            dimension_array_tmp.append(all_dimensions[y])
                            dimension_tmp = {
                                "source_columns": copy.deepcopy(dimension_array_tmp),
                                "is_drilldown": 0
                            }
                            dimensions_tmp.append(copy.deepcopy(dimension_tmp))
                        if temp_profile[j]["charts"][m]["visualization_type"].lower() == "line":
                            dimension_array_tmp = []
                            dimension_array_tmp.append("__time")
                            dimension_tmp = {
                                "source_columns": copy.deepcopy(dimension_array_tmp),
                                "is_drilldown": 0
                            }
                            dimensions_tmp.append(copy.deepcopy(dimension_tmp))
                            #dimension_temp_json = {
                            #            "dimensions": [
                            #                all_dimensions[temp_profile[j]["charts"][m]["dimensions"][0]]
                            #            ],
                            #            "metric": all_dimensions[temp_profile[j]["charts"][m]["dimensions"][0]],
                            #            "limit": temp_profile[j]["charts"][m]["row_limit"],
                            #        }
                    if temp_profile[j]["charts"][m]["visualization_type"].lower() == "line" and series_limit_flag == True:
                        chart_tmp = {
                            "type": temp_profile[j]["charts"][m]["visualization_type"].lower(),
                            "metrics": metrics_tmp,
                            "dimensions": dimensions_tmp,
                            "order_by": "",
                            #"order_by": temp_profile[j]["charts"][m]["order_by"],
                            #"custom.statistics.subquery.topk": dimension_temp_json,
                            "series_limit": temp_profile[j]["charts"][m]["row_limit"],
                            "drilldown_limit": None,
                            "threshold": {
                                "in_bytes": temp_profile[j]["charts"][m]["min_in_size"],
                                "out_bytes": temp_profile[j]["charts"][m]["min_out_size"]
                            }
                        }
                    else:
                        order_by_tmp = temp_profile[j]["charts"][m]["order_by"]
                        if temp_profile[j]["charts"][m]["visualization_type"].lower() == "line":
                            order_by_tmp = ""
                        chart_tmp = {
                                    "type": temp_profile[j]["charts"][m]["visualization_type"].lower(),
                                    "metrics": metrics_tmp,
                                    "dimensions": dimensions_tmp,
                                    "order_by": order_by_tmp,
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
        elif policy_type == "security" and "action_parameter" in data:
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
                            "health_check": "BFD:10:2",
                            "enable": "off"
                        }
                    ]
                }
            ]
        }
    }
    translation = DataTranslation()
    temp_test_data = translation.data_translation(policy_type, test_data)