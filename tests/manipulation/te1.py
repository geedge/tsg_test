a = {
    "return_data": 1,
    "rule": {
        "name": "secy_deny_extip_substr_fqdn_http_block_403responseprofile",
        "type": "security",
        "action": "deny",
        "source": [
            {
                "negate_option": False,
                "attribute_name": "ATTR_SOURCE_IP",
                "objects": [
                    {
                        "type": "ip",
                        "sub_type": "ip",
                        "statistics_option": "elaborate",
                        "name": "secy_srcip",
                        "description": "test",
                        "member_type": "item",
                        "items": [
                            {
                                "op": "add",
                                "ip": "1.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            }
        ],
        "destination": [
            {
                "negate_option": False,
                "attribute_name": "ATTR_SERVER_FQDN",
                "objects": [
                    {
                        "type": "ip",
                        "sub_type": "ip",
                        "statistics_option": "elaborate",
                        "name": "secy_dstip",
                        "description": "test",
                        "member_type": "item",
                        "items": [
                            {
                                "op": "add",
                                "ip": "11.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            }
        ],
        "application": {
            "objects": [
                {
                    "name": "http"
                }
            ],
            "attribute_name": "ATTR_APP_ID",
            "negate_option": False
        },
        "action_parameter": {
            "method": "block",
            "packet_capture": {
                "enable": 0
            },
            "code": 403,
            "profile": {
                "format": "html",
                "name": "secy_respage",
                "content_name": "/testa.html",
            },
            "message": "html_profile"
        },
        "is_enabled": 1,
        "vsys_id": "1",
        "schedule_id": [],
        "user_tags": "",
        "log_option": "metadata",
        "effective_range": {},
    },
    "vsys_id": "1"
}