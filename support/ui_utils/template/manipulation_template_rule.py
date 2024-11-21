# 测试数据
parameter={}  #临时使用
policy_configuration = {
    "name": parameter["test_case_name"],
    "type": "proxy_manipulation",
    "action": "allow",
    "and_conditions": [
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_SOURCE_IP",
                    "name": "manipulation_source_ip",
                    "type": "ip",
                    "sub_type": "ip",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "ip": parameter["test_pc_ip"],
                            "interval": "0-65535"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_DESTINATION_IP",
                    "name": "manipulation_destination_ip",
                    "type": "ip",
                    "sub_type": "ip",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "ip": "192.168.40.206",
                            "interval": "0-65535"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_EXTERNAL_IP",
                    "name": "manipulation_external_ip",
                    "type": "ip",
                    "sub_type": "ip",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "ip": "192.168.40.206",
                            "interval": "0-65535"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_INTERNAL_IP",
                    "name": "manipulation_internal_ip",
                    "type": "ip",
                    "sub_type": "ip",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "ip": "192.168.40.206",
                            "interval": "0-65535"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_GTP_APN",
                    "name": "manipulation_apn",
                    "type": "apn",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "eas.com$"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_GTP_PHONE_NUMBER",
                    "name": "manipulation_phone_number",
                    "type": "mobile_identity",
                    "sub_type": "phone_number",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "^12312312321"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_GTP_IMSI",
                    "name": "manipulation_imsi",
                    "type": "mobile_identity",
                    "sub_type": "imsi",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "^12312312321$"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_GTP_IMEI",
                    "name": "manipulation_imei",
                    "type": "mobile_identity",
                    "sub_type": "imei",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "^12312312321"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_INTERNAL_PORT",
                    "name": "manipulation_internal_port",
                    "type": "port",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "interval": "443"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_DESTINATION_PORT",
                    "name": "manipulation_destination_port",
                    "type": "port",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "interval": "443"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_EXTERNAL_PORT",
                    "name": "manipulation_external_port",
                    "type": "port",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "interval": "443"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_SUBSCRIBER_ID",
                    "name": "manipulation_subid",
                    "type": "subscriberid",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "baidu.com"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_SERVER_FQDN",
                    "name": "manipulation_fqdn",
                    "type": "fqdn",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "baidu.com"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_HTTP_URL",
                    "name": "manipulation_url",
                    "type": "url",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "www.baidu.com"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_HTTP_REQ_HDR",
                    "name": "manipulation_http_reqheader",
                    "type": "keyword",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "Wget&Windows&Chrome&Safari&Win64&AppleWebKit&KHTML&Wget"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_HTTP_RES_HDR",
                    "name": "manipulation_http_resheader",
                    "type": "keyword",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "text&/html&char&set&UTF-8&charset&UTF-8&text"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_HTTP_REQ_BODY",
                    "name": "manipulation_keywords_request_body",
                    "type": "keyword",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "text"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_HTTP_RES_BODY",
                    "name": "manipulation_keywords_response_body",
                    "type": "keyword",
                    "statistics_option": "none",
                    "member_type": "item",
                    "items": [
                        {
                            "op": "add",
                            "expr_type": "and",
                            "expression": "text"
                        }
                    ]
                }
            ]
        },
        {
            "negate_option": False,
            "or_conditions": [
                {
                    "attribute_name": "ATTR_APP_ID",
                    "type": "application",
                    "items": ["http"]
                }
            ]
        }
    ],
    "action_parameter": {
        {
            "manipulation_block": "warning_page",
            "sub_action": "block",
            "code": 403,
            "message": "testsaaa"
        },
        {
            "manipulation_block": "warning_page",
            "sub_action": "block",
            "code": 403,
            "html_profile": {
                "name": "test",
                "format": "html",
                "file_path": "Response-Pages_1.html"
            }
        },
        {
            "sub_action": "block"
        },
        {
            "sub_action": "edit_element",
            "rules": [
                {
                    "anchor_element": {
                        "contained_keyword": "tessa1",
                        "search_scope": "whole_file"
                    },
                    "target_element": {
                        "element_treatment": "mark",
                        "target_distance_from_matching": 2
                    }
                },
                {
                    "anchor_element": {
                        "contained_keyword": "testsa2",
                        "search_scope": "inside_element",
                        "start_indicator": "testsss"
                    },
                    "target_element": {
                        "element_treatment": "remove",
                        "target_distance_from_matching": 3
                    }
                }
            ]
        },
        {
            "sub_action": "replace_file",
            "replacement_file": {
                "name": "test",
                "file_path": "hijack_png_1.png",
                "content_name": "hijack_png_1.png",
                "content_type": "application / vnd.android.package - archive"
            }
        },
        {
            "sub_action": "inject_css",
            "css_file": {
                "name": "automanipulation_insert_profile",
                "file_path": "insert_css_1.css"
            }
        },
        {
            "sub_action": "inject_javascript",
            "injection_section": "html_body",   #html_head
            "js_file": {
                "name": "manipulation_insert_profile",
                "file_path": "insert_js_1.js"
            }
        },
        {
            "sub_action": "replace_text",
            "rules": [
                {
                    "regex_enable": 0,
                    "search_in": "http_req_uri",
                    "find": "sdsd",
                    "replace_with": "ggss"
                },
                {
                    "regex_enable": 1,
                    "search_in": "http_resp_body",
                    "find": "dfsdfg",
                    "replace_with": "dsdfsds"
                }
            ]
        },
        {
            "lua_script": {
                "name": "test",
                "file_path": "run_script_replace_reqbody.lua",
                "max_exec_time": 100
            }
        }
    },
    "effective_range": {
        "tag_sets": [
            [
                {
                    "tag": "data_center",
                    "value": [
                        "center-xxg-tsgx"
                    ]
                }
            ]
        ]
    },
    "effective_range2": {
        "tag_sets": [
            [
                {
                    "tag": "device_group",
                    "value": [
                        "group-xxg-tsgx"
                    ]
                }
            ]
        ]
    },
    "effective_range3": {
        "tag_sets": [
            [
                {
                    "tag": "data_center",
                    "value": [
                        "center-xxg-tsgx"
                    ]
                }
            ],
            [
                {
                    "tag": "device_group",
                    "value": [
                        "group-xxg-tsgx"
                    ]
                }
            ]
        ]
    },
    "is_enabled": 1,
    "log_option": "metadata",
}

traffic_generation = {
    "tool": "ssl",  # or trex/http
    "command": "curl --connect-timeout 30 -m 60 -H \"Content-Type:application/json;charset=UTF-8\" -X POST -d \"{\\\"requestbody\\\":\\\"test_request_body\\\",\\\"setcook\\\":\\\"test_setcook\\\",\\\"contenttype\\\": \\\"test_cont\\\",\\\"responsebody\\\": \\\"test_resbody\\\"}\" -kv --user-agent \"Wget (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36\" https://open.node.com:1443/go"
}

verification_result = {
    "excepted_traffic_result": "test_resbody",
    "expected_metric": {"hits": 1},
    "expected_log": [
        {"query_field_key": "http_host", "query_value": "open.node.com"},
        {"query_field_key": "decoded_as", "query_value": "HTTP"}
    ]
}



test_data = \
            {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "proxy_manipulation",
            "rule_name": "manipulation_rule_with_allow_src_ip",
            "rule_action": "allow",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "manipulation_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "192.168.64.99",
                            },
                        ]
                    }
                ],
                "destination_ip": [
                    {
                        "name": "manipulation_destination_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "192.168.40.206",
                            },
                        ]
                    }
                ],
                "internal_ip": [
                    {
                        "name": "manipulation_internal_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "192.168.64.99",
                            }
                        ]
                    }
                ],
                "external_ip": [
                    {
                        "name": "manipulation_external_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "192.168.40.206",
                            }
                        ]
                    }
                ],
                "source_port": [
                    {
                        "name": "manipulation_src_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "port",
                                "item_value": "1000-65530",
                            },
                        ]
                    }
                ],
                "internal_port": [
                    {
                        "name": "manipulation_internal_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "port",
                                "item_value": "1000-65530",
                            },
                        ]
                    }
                ],
                "destination_port": [
                    {
                        "name": "manipulation_destination_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "port",
                                "item_value": "443",
                            },
                        ]
                    }
                ],
                "external_port": [
                    {
                        "name": "manipulation_external_port",
                        "object_type": "port",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "port",
                                "item_value": "443",
                            },
                        ]
                    }
                ],
                "device": [
                    {
                        "name": "manipulation_imsi",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "imsi",
                                "item_value": '$' + 'test_imsi',
                            }
                        ]
                    },
                    {
                        "name": "manipulation_pn",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "phone_number",
                                "item_value": '$' + 'test_phone_number',
                            }
                        ]
                    },
                    {
                        "name": "manipulation_imei",
                        "object_type": "mobile_identity",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "imei",
                                "item_value": '$' + 'imei',
                            }
                        ]
                    },
                    {
                        "name": "manipulation_apn",
                        "object_type": "apn",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "apn",
                                "item_value": '$' + 'apn',
                            }
                        ]
                    }
                ],
                "source_geography": [],
                "destination_geography": [],
                "sub_id": [
                    {
                        "name": "manipulation_subid",
                        "object_type": "subscriberid",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "subscriberid",
                                "item_value": "$test6493",
                            }
                        ]
                    }
                ],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [
                    {
                        "name": "secy_flag",
                        "object_type": "flag",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "flag",
                                "flag": "64",
                                "mask": "64",
                            }
                        ]
                    }
                ],
                "application": [
                    {
                        "name": "http",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                    {
                        "name": "manipulation_fqdn",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "fqdn",
                                "item_value": "baidu.com",
                            }
                        ]
                    }
                ],
                "apn": [
                    {
                        "name": "manipulation_apn",
                        "object_type": "apn",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "apn",
                                "item_value": "*.baidu.com",
                            }
                        ]
                    }
                ],
                "protocol_filed": [
                    {
                        "name": "manipulation_url",
                        "object_type": "url",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "items": [
                            {
                                "item_operation": "add",
                                "item_type": "url",
                                "item_value": "baidu->"
                            }
                        ],
                    },
                    {
                        "name": "manipulation_http_signature",
                        "object_type": "http_signature",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus" : False,
                        "Statistics": "None",
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
                    },
                    {
                        "name": "manipulation_res_header_http_signature",
                        "object_type": "http_signature",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "response_header",
                                "item_key": "Content-Type",
                                "item_value": "TEXT",
                                "value": [
                                    "text/html"
                                ]
                            }
                        ],
                    },
                    {
                        "name": "manipulation_keywords_request_body",
                        "object_type": "keywords",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "request_body",
                                "item_value": "TEXT",
                                "value": [
                                    "test_request_body"
                                ]
                            }
                        ],
                    },
                    {
                        "name": "manipulation_keywords_response_body",
                        "object_type": "keywords",
                        "item_operation": "add",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "Statistics": "None",
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "response_body",
                                "item_value": "TEXT",
                                "value": [
                                    "test_resbody"
                                ]
                            }
                        ],
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                ],
                "packet_capture": []
            },
            "action_parameter": {
                "deny_response_text": [
                    {
                        "response_code": 403,
                        "response_content_type": "TEXT",
                        "response_content": "test_response_code",
                    }
                ],
                "response_page": [
                    {
                        "response_code": 404,
                        "response_content_type": "Profile",
                        "profile_file": {
                            "name": "test_tsg_ui_profile_page",
                            "model": "create",
                            "file": "response_testa.html->"
                        },
                    },
                ],
                "deny_response_block": [
                    {
                        "Manipulation_block": "close_connection"
                    }
                ],
                "redirect_url": [
                    {
                        "profile_type": "redirect_response",
                        "response_code": 301,
                        "redirect_url": "https://www.jd.com"
                    }
                ],
                "replace_parameter": [
                    {
                        "profile_type": "replace",
                        "regex": "off",
                        "search_in": "HTTP Request-URI",
                        "find": "forecast",
                        "replace_with": "team"
                    }
                ],
                "hijack_file": [
                    {
                        "profile_type": "hijack",
                        "profile_file": {
                            "name": "test_tsg_ui_profile_page",
                            "model": "create",
                            "file": "hijack_png_1.png->",
                            "download_name": "Mirror Server Response->",
                            "file_type": "png->"
                        }
                    }
                ],
                "insert_script": [
                    {
                        "profile_type": "insert",
                        "profile_file": {
                            "name": "test_tsg_ui_profile_page",
                            "model": "create",
                            "script": "insert_js_1.js->",
                            "script_type": "js->",
                            "insert_position": "Before Page Load->"
                        }
                    }
                ],
                "run_script": [
                    {
                        "profile_type": "run_script",
                        "profile_file": {
                            "name": "test_tsg_ui_profile_page",
                            "model": "create",
                            "script": "run_script_insert.lua->",
                            "max_exec_time": "1000->"
                        }
                    }
                ]
            },
            "expected_return": "reset",
            "counters_1": {"hits": 1},
            "log_query_param_1": [{"query_field_key": "ssl_sni", "query_value": "www.baidu.com"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv https://www.baidu.com"
            },
            # "traffic": {
            #     "type": "trex",
            #     "clients_start_ip": "192.168.64.86",
            #     "clients_end_ip": "192.168.64.86",
            #     "servers_start_ip": "2.1.1.1",
            #     "servers_end_ip": "2.1.1.2",
            #     "m": 1,
            #     "d": 1,
            #     "yaml_name": "test",
            #     "pcap_name": "test_https"
            # },
            # "traffic": {
            #     "type": "nslookup",
            #     "command": "nslookup www.facebook.com"
            # },
            # "traffic": {
            #     "type": "wget",
            #     "command": "wget -q -O- http://open.node.com:180"
            # },
            "token": ""
        }