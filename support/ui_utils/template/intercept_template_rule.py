# 测试数据
test_data = \
            {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "proxy_intercept",
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
                "ssl_decryption_keyring": [
                    {
                        "profile_type": "ssl_keyring",
                        "decryption_keying_type": "trusted",
                        "profile_file": {
                            "name": "manipulation_trusted_page",
                            "model": "create",
                            "file_certificate": "test_root_cert_catest.cer",
                            "file_private_key": "test_root_key_catest.key",
                            "certificate_type": "Root-Certificate",
                            "private_key_format": "true",
                            "is_match": "match",
                            "reissue_expiry_hours": "C-120",
                            "type": "Root-Certificate",
                            "public_key_algorithm": "RSA-2048",
                            "certificate_revocation_list": "",
                            "include_root": "on"
                        }
                    },
                    {
                        "profile_type": "ssl_keyring",
                        "decryption_keying_type": "untrusted",
                        "profile_file": {
                            "name": "manipulation_untrusted_page",
                            "model": "create",
                            "file_certificate": "test_root_cert_catest.cer",
                            "file_private_key": "test_root_key_catest.key",
                            "certificate_type": "Root-Certificate",
                            "private_key_format": "true",
                            "is_match": "match",
                            "reissue_expiry_hours": "C-120",
                            "type": "Root-Certificate",
                            "public_key_algorithm": "RSA-2048",
                            "certificate_revocation_list": "",
                            "include_root": "on"
                        }
                    }
                ],
                "ssl_decryption_profile": [
                    {
                        "profile_type": "ssl_decryption",
                        "profile_file": {
                            "name": "manipulation_ssl_decryption_profile",
                            "model": "create",
                            "common_name": "on",
                            "issuer": "on",
                            "self_signed": "on",
                            "expiry_date": "on",
                            "fail_action": "Pass-through",
                            "ev_certificate": "off",
                            "certificate_transparency": "off",
                            "mutual_authentication": "on",
                            "protocol_errors": "on",
                            "certificate_pinning": "on",
                            "certificate_not_installed": "off",
                            "mirror_client_versions": "on",
                            "min_client_version": "TLSv1.0",
                            "max_client_version": "TLSv1.2",
                            "allow_HTTP2": "on"
                        }
                    }
                ],
                "tcp_proxy_profile": [
                    {
                        "profile_type": "tcp_option",
                        "profile_file": {
                            "name": "manipulation_tcp_proxy_profile",
                            "model": "create",
                            "enable_TCP_passthrough": "off",
                            "c_override_MSS": "off",
                            "c_overrideMSS": "536",
                            "c_no_delay": "on",
                            "c_ttl": "70",
                            "c_keepalive": "on",
                            "c_probe_number": "8",
                            "c_idle_time": "30",
                            "c_interval": "15",
                            "c_UserTimeout_switch": "on",
                            "c_userTimeout": "600",
                            "s_override_MSS": "off",
                            "s_overrideMSS": "1460",
                            "s_no_delay": "on",
                            "s_ttl": "75",
                            "s_keepalive": "on",
                            "s_probe_number": "8",
                            "s_idle_time": "30",
                            "s_interval": "15",
                            "s_UserTimeout_switch": "on",
                            "s_userTimeout": "600"
                        }
                    }
                ],
                "traffic_mirroring_profile": [
                    {
                        "profile_type": "traffic_mirror",
                        "vlan_id": "no_default",
                        "profile_file": {
                            "name": "manipulation_traffic_mirroring_profile",
                            "model": "create",
                            "vlan_id":
                                [
                                    "16"
                                ]
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