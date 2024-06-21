# 测试数据
test_data = \
            {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "pxy_manipulation",
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
                                "item_value": "192.168.64.88",
                            },
                        ]
                    }
                ],
                "source_port": [],
                "destination_ip": [],
                "destination_port": [],
                "internal_ip": [],
                "internal_port": [],
                "external_ip": [],
                "external_port": [],
                "source_geography": [],
                "destination_geography": [],
                "sub_id": [],
                "device": [],
                "tunnel": [],
                "tunnel_level": [],
                "flag": [],
                "application": [
                    {
                        "name": "http",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [
                    {
                        "name": "manipulation_fqdn_node",
                        "object_type": "fqdn",
                        "select_type": False,
                        "negate": False,
                        "plus": False,
                        "items": [
                            {
                                "item_value": "baidu.com",
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
                            "file": "testa.html->"
                        },
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
                            "file": "test_png_1.png->",
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
                            "script": "test_js_1.js->",
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
            #     "yaml_name": "test_https",
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