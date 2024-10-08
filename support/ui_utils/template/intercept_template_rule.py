# 测试数据
test_data = \
            {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "pxy_intercept",
            "rule_name": "intercept_rule_with_src_ip",
            "rule_action": "allow",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "intercept_source_ip",
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
                        "name": "mintercept_destination_ip",
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
                        "name": "intercept_internal_ip",
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
                        "name": "intercept_external_ip",
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
                        "name": "intercept_src_port",
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
                        "name": "intercept_internal_port",
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
                        "name": "intercept_destination_port",
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
                        "name": "intercept_external_port",
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
                        "name": "intercept_imsi",
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
                        "name": "intercept_pn",
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
                        "name": "intercept_imei",
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
                        "name": "intercept_apn",
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
                        "name": "intercept_subid",
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
                        "name": "intercept_fqdn",
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
                        "name": "intercept_apn",
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
                    }
                ],
                "sub_action_override": True,
                "sub_action": [
                ],
                "packet_capture": []
            },
            "action_parameter": {
                "decryption_keyring_trusted": [
                    {
                        "profile_type": "redirect_response",
                        "response_code": 301,
                        "redirect_url": "https://www.jd.com"
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