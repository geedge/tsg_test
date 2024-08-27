# -*- coding: utf-8 -*-

class DataTranslation:
    def data_translation(self, policy_type, data):
        temp_test_data = {
            "obj_condition": [],
            "profile_condition": [],
            "application": [],
        }
        for key in data:
            if key in {"source_ip", "source_port", "destination_ip", "destination_port", "internal_ip", "internal_port", "external_ip", "external_port", "sub_id", "device""tunnel", "tunnel_level", "flag", "server_fqdn", "protocol_filed"}:
                object = self.push_object_data(key, data)
            if key in {"action_parameter", "profile"}:
                profile = self.push_profile_data(policy_type, key, data)
        if "application" in data.keys():
            temp_test_data["application"] = data["application"]
        temp_test_data = {
            "obj_condition": object,
            "profile_condition": profile,
        }
        return temp_test_data
    
    def push_object_data(self, key, data):
        object = []
        if key == "source_ip":
            temp = {
                "attribute_name": "ATTR_SOURCE_IP",
                "object_type": "ip",
                "object_sub_type": "ip",
                "is_negate": 0,
                "object_list": [
                    {
                        "add_item_list": [
                            {
                                "ip_address": data["source_ip"][0]["item"][0]["item_value"],
                                "port_range": "0-65535"
                            }
                        ]
                    }
                ]
            }
            object.append(temp)
        elif key == "destination_ip":
            temp = {
                "attribute_name": "ATTR_DESTINATION_IP",
                "object_type": "ip",
                "object_sub_type": "ip",
                "is_negate": 0,
                "object_list": [
                    {
                        "add_item_list": [
                            {
                                "ip_address": data["source_ip"][0]["item"][0]["item_value"],
                                "port_range": "0-65535"
                            }
                        ]
                    }
                ]
            }
            object.append(temp)
        elif key == "server_fqdn":
            temp = {
                "attribute_name": "ATTR_SERVER_FQDN",
                "object_type": "fqdn",
                "object_sub_type": "fqdn",
                "object_list": [
                    {
                        "add_item_list": [
                            {
                                "keyword_array": [
                                    data["server_fqdn"][0]["item"][0]["item_value"]
                                ]
                            }
                        ]
                    }
                ]
            }
            object.append(temp)
        elif key == "sub_id":
            temp = {
                "attribute_name": "ATTR_SUBSCRIBER_ID",
                "object_type": "subscriberid",
                "object_sub_type": "subscriberid",
                "object_list": [
                    {
                        "add_item_list": [
                            {
                                "keyword_array": [
                                    data["sub_id"][0]["item"][0]["item_value"]
                                ]
                            }
                        ]
                    }
                ]
            }
            object.append(temp)
        elif key == "protocol_filed":
            for i in range(len(data["protocol_filed"])):
                if data["protocol_filed"][i]["object_type"] == "url":
                    temp = {
                        "attribute_name": "ATTR_HTTP_URL",
                        "object_type": "url",
                        "object_sub_type": "url",
                        "object_list": [
                            {
                                "add_item_list": [
                                    {
                                        "keyword_array": [
                                            data["protocol_filed"][i]["items"][0]["item_value"]
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                    object.append(temp)
                elif data["protocol_filed"][i]["object_type"] == "http_signature":
                    if data["protocol_filed"][i]["item"][0]["item_type"] == "request_header":
                        temp = {
                            "attribute_name": "ATTR_HTTP_REQ_HDR",
                            "object_type": "http_signature",
                            "object_sub_type": "http_signature",
                            "object_list": [
                                {
                                    "context_name": data["protocol_filed"][i]["item"][0]["item_key"],
                                    "add_item_list": [
                                        {
                                            "keyword_array": [
                                                data["protocol_filed"][i]["item"][0]["value"][0]
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                        object.append(temp)
                    elif data["protocol_filed"][i]["item"][0]["item_type"] == "response_header":
                        temp = {
                            "attribute_name": "ATTR_HTTP_RES_HDR",
                            "object_type": "http_signature",
                            "object_sub_type": "http_signature",
                            "object_list": [
                                {
                                    "context_name": data["protocol_filed"][i]["item"][0]["item_key"],
                                    "add_item_list": [
                                        {
                                            "keyword_array": [
                                                data["protocol_filed"][i]["item"][0]["value"][0]
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                        object.append(temp)
        return object
    
    def push_profile_data(self, policy_type, key, data):
        profile = []
        if policy_type == "service_chaining":
            temp_profile = data[key]
            for i in range(len(temp_profile)):
                temp = {
                    "profile_type": "service_function_forwarder",
                    "name": "test_sc_api_mirror_block_vlan_none",
                    "type": "2",
                    "load_balance_method": "hash-int-ip",
                    "load_balance_localization": "nearby",
                    "failure_action": "block",
                    "return_data": 1,
                    "op_action": "add",
                    "sf_condition":[
                        {
                            "profile_type": "service_function",
                            "name": "test_sc_api_vlan_none",
                            "profile_id":None,
                            "device_group":{
                                "tag":"device_group",
                                "value":"group-xxg-tsgx"
                            },
                            "admin_status":1,
                            "connectivity":{
                                "method":"layer2_switch"
                            },
                            "health_check":{
                                "method":"none"
                            },
                            "is_valid":1,
                            "vsys_id":1
                        }
                    ]
                }
                profile.append(temp)
        elif policy_type == "statistics":
            temp_profile = data[key]["statistics_template"]
            for j in range(len(temp_profile)):
                temp = {
                    "profile_type": "Statistics_Templates",
                    "name": temp_profile[j]["name"],
                    "chart_list": [
                        {
                            "type": temp_profile[j]["charts"][0]["visualization_type"].lower(),
                            "metrics": [
                                {
                                    "source_columns": "",
                                    "function": ""
                                }
                            ],
                            "dimensions": [
                                {
                                    "source_columns": temp_profile[j]["charts"][0]["dimensions"][0],
                                    "is_drilldown": 0
                                }
                            ],
                            "order_by": temp_profile[j]["charts"][0]["order_by"],
                            "limit": temp_profile[j]["charts"][0]["row_limit"],
                            "drilldown_limit": None,
                            "threshold": {
                                "in_bytes": temp_profile[j]["charts"][0]["min_in_size"],
                                "out_bytes": temp_profile[j]["charts"][0]["min_out_size"]
                            }
                        }
                    ]
                }
                profile.append(temp)
        return profile
    
if __name__ == '__main__':
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
    temp_test_data = translation.data_translation(test_data["condition"])