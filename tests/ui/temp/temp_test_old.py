# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.traffic_replay.traffic_verification import *
from support.api_utils.analysis_result import *
import support.ui_utils.env_initialization

def run(parameter):
    print("Begin to run test case: " + parameter["test_case_name"])
        # 参数初始化
        result = ""
        
    # 脚本启动时间
    start_time = time.time()
    
    # 环境初始化
    support.ui_utils.env_initialization.initiate_selenium_request()
    driver = support.ui_utils.env_initialization.my_driver()
    support.ui_utils.env_initialization.setup()
    
    # 测试数据
    test_data = {
        "is_multi_priority": False,
        "rule_num": 1,
        "policy_type": "security",
        "rule_name": "security_rule_with_deny_ip_quic",
        "rule_action": "deny",
        "rule_type": "create",
        "condition": {
            "source_port": [],
            "destination_ip": [],
            "destination_port": [],
            # "internal_ip": [
            #     {
            #         "name": "security_internal_ip",
            #         "object_type": "ip",
            #         "select_type": False,
            #         "negate": False,
            #         "item": [
            #             "1.1.1.1",
            #             "1.1.1.1-1.1.1.2"
            #         ]
            #     }
            # ],
            "internal_ip_group": [
                {
                    "name": "security_src_ip_group",
                    "object_type": "ip_group",
                    "select_type": True,
                    "negate": False,
                    "group_subordinate": [
                        {
                            "name": "security_include_1_src_ip",
                            "object_type": "ip",
                            "negate": False,
                            "item": [
                                "1.1.1.1",
                                "1.1.1.1-1.1.1.2"
                            ]
                        },
                        {
                            "name": "security_include_2_src_ip",
                            "object_type": "ip",
                            "negate": False,
                            "item": [
                                "2.1.1.1",
                                "2.1.1.1-2.1.1.2"
                            ]
                        }
                    ],
                    "group_exclude": [
                        {
                            "name": "security_exclude_src_ip",
                            "object_type": "ip",
                            "negate": False,
                            "item": [
                                "3.1.1.1",
                                "3.1.1.1-3.1.1.2"
                            ]
                        }
                    ]
                }
            ],
            "internal_port": [
                {
                    "name": "security_internal_port",
                    "object_type": "port",
                    "select_type": False,
                    "negate": False,
                    "item": [
                        "1000-1110",
                        "2222"
                    ]
                }
            ],
            "external_ip": [
                {
                    "name": "security_external_ip",
                    "object_type": "ip",
                    "select_type": False,
                    "negate": False,
                    "item": [
                        "11.1.1.1",
                        "11.1.1.1-11.1.1.2"
                    ]
                }
            ],
            "external_port": [],
            "source_geography": [],
            "destination_geography": [],
            "sub_id": [],
            "device": [
                # {
                #     "name": "security_mobile_phone_number",
                #     "object_type": "phone_number",
                #     "select_type": False,
                #     "negate": False,
                #     "plus": True,
                #     "item": [
                #         "test",
                #         "test11"
                #     ]
                # }
            ],
            "tunnel": [],
            "tunnel_level": [],
            "flag": [
                # {
                #     "name": "security_flag",    
                #     "object_type": "flag",
                #     "select_type": False,
                #     "negate": False,
                #     "item": [
                #         {
                #             "flag_type": "asymmetric",
                #             "flag_num": 1,
                #             "flag_status": "True"
                #         },
                #         {
                #             "flag_type": "Bidirectional",
                #             "flag_num": 16,
                #             "flag_status": "True"
                #         },
                #     ]
                # }
            ],
            "application": [
                {
                    "name": "http",
                    "object_type": "application",
                    "negate": False
                }
                # {
                #     "name": "http_group",
                #     "object_type": "application_group",
                #     "negate": False
                # }
            ],
            "server_fqdn": [
                {
                    "name": "www.baidu.com", # 需要新建，不能使用已存在的object，保证自动化的统一性，这里只是示例
                    "object_type": "fqdn",
                    "select_type": False,
                    "negate": False,
                    "plus": False,
                    "item": [
                        "*google.com"
                    ]
                }
            ],
            "protocol_field": [
                # {
                #     "name": "security_url", # 需要新建，不能使用已存在的object，保证自动化的统一性，这里只是示例
                #     "field_type": "url", # Protocol Field独有字段
                #     "object_type": "url",
                #     "select_type": False,
                #     "negate": False,
                #     "plus": False,
                #     "item": [
                #         "youtube.com", 
                #         "google.com"
                #     ]
                # },
                {
                    "name": "security_request_header",
                    "field_type": "request_header",
                    "object_type": "http_signature",
                    "select_type": False,
                    "negate": False,
                    "plus": True,
                    "item": [
                        {
                            "item_key": "Set-Cookie",
                            "item_value": "TEXT",
                            "value": ["test", "test11"]
                        },
                        {
                            "item_key": "Content-Type",
                            "item_value": "HEX",
                            "value": ["123"]
                        }
                    ]
                },
                # {
                #     "name": "security_keyword",
                #     "field_type": "keyword",
                #     "object_type": "keyword",
                #     "select_type": False,
                #     "negate": False,
                #     "plus": True,
                #     "item": [
                #         {
                #             "item_value": "TEXT",
                #             "value": ["test", "test11"]
                #         },
                #         {
                #             "item_value": "HEX",
                #             "value": ["123"]
                #         }
                #     ]
                # }
            ],
            "sub_action_override": True,
            "sub_action": [
                {
                    "type": "drop",
                    "drop_packet": 1,
                    "send_tcp_rst": False,
                    "send_icmp_unreachable": True
                }
                # {
                #     "type": "rate_limit",
                #     "rate_unit": "kbps",
                #     "rate_value": 200
                # }
                # {
                #     "type": "block",
                #     "code": 404,
                #     "content_type": "TEXT",
                #     "content": "block_change_response_profile"
                # }
                # {
                #     "type": "redirect",
                #     "redirect_url": "www.google.com"
                # }
            ],
            "packet_capture": [
                {
                    "enable": True,
                    "capture_depth": 3000
                }
            ]
        },
        "profile": [
        ],
        "expected_return": "POST",
        "counters_1": {"hits": 0},
        "log_query_param_1": [],
        "command": "curl -kv https://www.google.com"
    }
    
    # 添加定位库集合
    if test_data["policy_type"] == "security":
        test_ip_object_element_position = {
            "page_jump":{
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_ipAddress_posId
            },
            "create": {
                "objectListPage_createButton_posId": ipObjectListPage_createButton_posId,
                "objectListPage_dropDown_createButton_posId": ipObjectListPage_dropDown_createButton_posId,
                "objectPage_inputName_posXpath": ipObjectPage_inputName_posXpath,
                "objectPage_ipType_posId": ipObjectPage_ipType_posId,
                "objectPage_addItem_posId": ipObjectPage_addItem_posId,
                "objectPage_inputItem_posXpath": ipObjectPage_inputItem_posXpath,
                "objectPage_button_saveItem_posXpath": ipObjectPage_button_saveItem_posXpath,
                "objectPage_okButton_posId": ipObjectPage_okButton_posId,
                "objectPage_okButton_warningYes_posXpath": ipObjectPage_okButton_warningYes_posXpath
            },
            "search": {
                "objectListPage_searchLabel_posId": ipObjectListPage_searchLabel_posId,
                "objectListPage_searchLabel_selectName_posXpath": ipObjectListPage_searchLabel_selectName_posXpath,
                "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
            },
            "delete": {
                "objectListPage_allSelect_posXpath": ipObjectListPage_allSelect_posXpath,
                "objectListPage_deleteButton_posId": ipObjectListPage_deleteButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": ipObjectListPage_deleteButton_warningYes_posXpath
            }
        }
        test_ip_group_object_element_position = {
            "page_jump":{
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_ipAddress_posId
            },
            "create": {
                "objectListPage_createButton_posId": ipObjectListPage_createButton_posId,
                "objectListPage_dropDown_createGroupButton_posId": ipObjectListPage_dropDown_createGroupButton_posId,
                "objectPage_inputName_posXpath": ipObjectPage_inputName_posXpath,
                "objectPage_ipType_posId": ipObjectPage_ipType_posId,
                "groupObjectPage_selectTypeIP_posId": ipGroupObjectPage_selectTypeIP_posId,
                "groupObjectPage_addSubordinate_posXpath": ipGroupObjectPage_addSubordinate_posXpath,
                "groupObjectPage_searchSubordinateIP_posXpath": ipGroupObjectPage_searchSubordinateIP_posXpath,
                "groupObjectPage_selectSubordinateIP_posXpath": ipGroupObjectPage_selectSubordinateIP_posXpath,
                "groupObjectPage_closeSubordinateIP_posXpath": ipGroupObjectPage_closeSubordinateIP_posXpath,
                "groupObjectPage_addSubordinateObject_posId": ipGroupObjectPage_addSubordinateObject_posId,
                "groupObjectPage_enableExclude_posXpath": ipGroupObjectPage_enableExclude_posXpath,
                "groupObjectPage_addExclude_posXpath": ipGroupObjectPage_addExclude_posXpath,
                "groupObjectPage_searchExcludeIP_posXpath": ipGroupObjectPage_searchExcludeIP_posXpath,
                "groupObjectPage_selectExcludeIP_posXpath": ipGroupObjectPage_selectExcludeIP_posXpath,
                "groupObjectPage_closeExcludeIP_posXpath": ipGroupObjectPage_closeExcludeIP_posXpath,
                "groupObjectPage_addExcludeObject_posId": ipGroupObjectPage_addExcludeObject_posId,
                "objectPage_okButton_posId": ipObjectPage_okButton_posId,
                "objectPage_okButton_warningYes_posXpath": ipObjectPage_okButton_warningYes_posXpath
            },
            "search": {
                "objectListPage_searchLabel_posId": ipObjectListPage_searchLabel_posId,
                "objectListPage_searchLabel_selectName_posXpath": ipObjectListPage_searchLabel_selectName_posXpath,
                "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
            },
            "delete": {
                "objectListPage_allSelect_posXpath": ipObjectListPage_allSelect_posXpath,
                "objectListPage_deleteButton_posId": ipObjectListPage_deleteButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": ipObjectListPage_deleteButton_warningYes_posXpath
            }
        }
        test_port_object_element_position = {
            "page_jump":{
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_port_posId
            },
            "create": {
                "objectListPage_createButton_posId": portObjectListPage_createButton_posId,
                "objectListPage_dropDown_createButton_posId": portObjectListPage_dropDown_createButton_posId,
                "objectPage_inputName_posXpath": portObjectPage_inputName_posXpath,
                "objectPage_addItem_posId": portObjectPage_addItem_posId,
                "objectPage_inputItem_posXpath": portObjectPage_inputItem_posXpath,
                "objectPage_button_saveItem_posXpath": portObjectPage_button_saveItem_posXpath,
                "objectPage_okButton_posId": portObjectPage_okButton_posId,
                "objectPage_okButton_warningYes_posXpath": portObjectPage_okButton_warningYes_posXpath
            },
            "search": {
                "objectListPage_searchLabel_posId": portObjectListPage_searchLabel_posId,
                "objectListPage_searchLabel_selectName_posXpath": portObjectListPage_searchLabel_selectName_posXpath,
                "objectListPage_tableTbody_posXpath": portObjectListPage_tableTbody_posXpath
            },
            "delete": {
                "objectListPage_allSelect_posXpath": portObjectListPage_allSelect_posXpath,
                "objectListPage_deleteButton_posId": portObjectListPage_deleteButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": portObjectListPage_deleteButton_warningYes_posXpath
            }
        }
        test_http_signature_object_element_position = {
            "page_jump":{
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_httpSignature_posId
            },
            "create": {
                "objectListPage_createButton_posId": httpSignatureObjectListPage_createButton_posId,
                "objectListPage_dropDown_createButton_posId": httpSignatureObjectListPage_dropDown_createButton_posId,
                "objectPage_inputName_posXpath": httpSignatureObjectPage_inputName_posXpath,
                "objectPage_addItem_posId": httpSignatureObjectPage_addItem_posId,
                "objectPage_item_key_dropDown_posXpath": httpSignatureObjectPage_item_key_dropDown_posXpath,
                "objectPage_item_key_dropDown_select_posXpath": httpSignatureObjectPage_item_key_dropDown_select_posXpath,
                "objectPage_item_value_select_posXpath": httpSignatureObjectPage_item_value_select_posXpath,
                "objectPage_inputItem_posXpath": httpSignatureObjectPage_inputItem_posXpath,
                "objectPage_item_value_plus_posXpath": httpSignatureObjectPage_item_value_plus_posXpath,
                "objectPage_button_saveItem_posXpath": httpSignatureObjectPage_button_saveItem_posXpath,
                "objectPage_okButton_posId": httpSignatureObjectPage_okButton_posId,
                "objectPage_okButton_warningYes_posXpath": httpSignatureObjectPage_okButton_warningYes_posXpath
            },
            "search": {
                "objectListPage_searchLabel_posId": httpSignatureObjectListPage_searchLabel_posId,
                "objectListPage_searchLabel_selectName_posXpath": httpSignatureObjectListPage_searchLabel_selectName_posXpath,
                "objectListPage_tableTbody_posXpath": httpSignatureObjectListPage_tableTbody_posXpath
            },
            "delete": {
                "objectListPage_allSelect_posXpath": httpSignatureObjectListPage_allSelect_posXpath,
                "objectListPage_deleteButton_posId": httpSignatureObjectListPage_deleteButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": httpSignatureObjectListPage_deleteButton_warningYes_posXpath
            }
        }
        test_rule_element_position = {
            "page_jump":{
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_security_posId
            },
            "create": {
                "policyRuleListPage_createButton_posId": securityRuleListPage_createButton_posId,
                "policyRulePage_inputName_posXpath": securityRulePage_inputName_posXpath,
                "policyRulePage_selectAction_posId": securityRulePage_selectDeny_posId,
                "policyRulePage_addConditionInternalIP_posXpath": securityRulePage_addCondition_internalIP_posXpath,
                "policyRulePage_addInternalIP_posXpath": securityRulePage_addInternalIP_posXpath,
                "policyRulePage_searchInternalIP_posXpath": securityRulePage_searchInternalIP_posXpath,
                "policyRulePage_selectInternalIP_posXpath": securityRulePage_selectInternalIP_posXpath,
                "policyRulePage_closeInternalIP_posXpath": securityRulePage_closeInternalIP_posXpath,
                "policyRulePage_addConditionInternalPort_posXpath": securityRulePage_addCondition_internalPort_posXpath,
                "policyRulePage_addInternalPort_posXpath": securityRulePage_addInternalPort_posXpath,
                "policyRulePage_searchInternalPort_posXpath": securityRulePage_searchInternalPort_posXpath,
                "policyRulePage_selectInternalPort_posXpath": securityRulePage_selectInternalPort_posXpath,
                "policyRulePage_closeInternalPort_posXpath": securityRulePage_closeInternalPort_posXpath,
                "policyRulePage_addConditionExternalIP_posXpath": securityRulePage_addCondition_externalIP_posXpath,
                "policyRulePage_addExternalIP_posXpath": securityRulePage_addExternalIP_posXpath,
                "policyRulePage_searchExternalIP_posXpath": securityRulePage_searchExternalIP_posXpath,
                "policyRulePage_selectExternalIP_posXpath": securityRulePage_selectExternalIP_posXpath,
                "policyRulePage_closeExternalIP_posXpath": securityRulePage_closeExternalIP_posXpath,
                "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                "policyRulePage_selectApplicationGroupLabel_posXpath": securityRulePage_selectApplicationGroupLabel_posXpath,
                "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                "policyRulePage_addConditionUrl_posXpath": securityRulePage_addCondition_url_posXpath,
                "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
                "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
                "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                "policyRulePage_addUrl_posXpath": securityRulePage_addUrl_posXpath,
                "policyRulePage_searchUrl_posXpath": securityRulePage_searchUrl_posXpath,
                "policyRulePage_selectUrl_posXpath": securityRulePage_selectUrl_posXpath,
                "policyRulePage_closeUrl_posXpath": securityRulePage_closeUrl_posXpath,
                "policyRulePage_addRequestHeader_posXpath": securityRulePage_addRequestHeader_posXpath,
                "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
                "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
                "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
                "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                "policyRulePage_subAction_drop_posXpath": securityRulePage_subAction_drop_posXpath,
                "policyRulePage_subAction_drop_dropPkt_posXpath": securityRulePage_subAction_drop_dropPkt_posXpath,
                "policyRulePage_subAction_drop_sendTcpRst_posXpath": securityRulePage_subAction_drop_sendTcpRst_posXpath,
                "policyRulePage_subAction_drop_sendIcmp_posXpath": securityRulePage_subAction_drop_sendIcmp_posXpath,
                "policyRulePage_subAction_block_posXpath": securityRulePage_subAction_block_posXpath,
                "policyRulePage_subAction_block_responseCode_posXpath": securityRulePage_subAction_block_responseCode_posXpath,
                "policyRulePage_subAction_block_responseCode_change_posXpath": securityRulePage_subAction_block_responseCode_change_posXpath,
                "policyRulePage_subAction_block_responseContent_posXpath": securityRulePage_subAction_block_responseContent_posXpath,
                "policyRulePage_subAction_block_responseContent_change_posXpath": securityRulePage_subAction_block_responseContent_change_posXpath,
                "policyRulePage_subAction_block_responseContent_text_posId": securityRulePage_subAction_block_responseContent_text_posId,
                "policyRulePage_subAction_block_responseContent_clickProfile_posXpath": securityRulePage_subAction_block_responseContent_clickProfile_posXpath,
                "policyRulePage_subAction_block_responseContent_searchProfile_posXpath": securityRulePage_subAction_block_responseContent_searchProfile_posXpath,
                "policyRulePage_subAction_block_responseContent_selectProfile_posId": securityRulePage_subAction_block_responseContent_selectProfile_posId,
                "policyRulePage_packetCapture_posXpath": securityRulePage_packetCapture_posXpath,
                "policyRulePage_packetCapture_depth_posXpath": securityRulePage_packetCapture_depth_posXpath,
                "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                "policyRulePage_okButton_yes_posId": securityRulePage_okButton_yes_posId,
                "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath
            },
            "search": {
                "policyRuleListPage_searchLable_posId": securityRuleListPage_searchLable_posId,
                "policyRuleListPage_searchLable_dropDown_item_posXpath": securityRuleListPage_searchLable_dropDown_item_posXpath,
                "policyRuleListPage_searchLable_input_itemContent_posXpath": securityRuleListPage_searchLable_input_itemContent_posXpath,
                "policyRuleListPage_searchLable_searchButton_posId": securityRuleListPage_searchLable_searchButton_posId,
                "policyRuleListPage_tableTbody_posXpath": securityRuleListPage_tableTbody_posXpath
            },
            "delete": {
                "policyRuleListPage_allSelect_posXpath": securityRulelistPage_allSelect_posXpath,
                "policyRuleListPage_deleteButton_posId": securityRuleListPage_deleteButton_posId,
                "policyRuleListPage_okButton_warningYes_posXpath": securityRuleListpage_okButton_warningYes_posXpath,
                "policyRuleListPage_okButton_warningNo_posXpath":securityRuleListpage_okButton_warningNo_posXpath
            }
        }
    
    # 添加测试过程中涉及的template
    template_path = {}
    template_path["trex_workpath"] = "/opt/trex/v3.03"
    template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"
    
    # 创建object
    if "internal_ip" in test_data["condition"] and len(test_data["condition"]["internal_ip"]) != 0:
        internal_ip_data = test_data["condition"]["internal_ip"]
        create_ip = CreateObject(driver)
        for i in range(len(internal_ip_data)):
            create_internal_ip_code = create_ip.create(internal_ip_data[i], test_ip_object_element_position)
            if create_internal_ip_code != 200:
                result = "Fail to create internal ip object."
                break
    if "internal_ip_group" in test_data["condition"] and len(test_data["condition"]["internal_ip_group"]) != 0:
        internal_ip_group_data = test_data["condition"]["internal_ip_group"]
        for x in range(len(internal_ip_group_data)):
            include_ip_data = internal_ip_group_data[x]["group_subordinate"]
            for y in range(len(include_ip_data)):
                create_ip = CreateObject(driver)
                create_include_internal_ip_code = create_ip.create(include_ip_data[y], test_ip_object_element_position)
                if create_include_internal_ip_code != 200:
                    result = "Fail to create include internal ip object."
                    break  
            exclude_ip_data = internal_ip_group_data[x]["group_exclude"]
            for z in range(len(exclude_ip_data)):
                create_ip = CreateObject(driver)
                create_exclude_internal_ip_code = create_ip.create(exclude_ip_data[z], test_ip_object_element_position)
                if create_exclude_internal_ip_code != 200:
                    result = "Fail to create exclude internal ip object."
                    break
            if create_include_internal_ip_code == 200 and create_exclude_internal_ip_code == 200:
                create_ip_group = CreateObject(driver)
                create_internal_ip_group_code = create_ip_group.create_group(internal_ip_group_data[x], "IP", test_ip_group_object_element_position)
                if create_internal_ip_group_code != 200:
                    result = "Fail to create internal ip group object."
                    break 
    if "external_ip" in test_data["condition"] and len(test_data["condition"]["external_ip"]) != 0:
        external_ip_data = test_data["condition"]["external_ip"]
        create_ip = CreateObject(driver)
        for t in range(len(external_ip_data)):
            create_external_ip_code = create_ip.create(external_ip_data[t], test_ip_object_element_position)
            if create_external_ip_code != 200:
                result = "Fail to create external ip object."
                break
    if "internal_port" in test_data["condition"] and len(test_data["condition"]["internal_port"]) != 0:
        internal_port_data = test_data["condition"]["internal_port"]
        create_port = CreateObject(driver)
        for j in range(len(internal_port_data)):
            create_internal_port_code = create_port.create(internal_port_data[j], test_port_object_element_position)
            if create_internal_port_code != 200:
                result = "Fail to create internal port object."
                break
    if "protocol_field" in test_data["condition"] and len(test_data["condition"]["protocol_field"]) != 0:
        protocol_filed_data = test_data["condition"]["protocol_field"]
        for n in range(len(protocol_filed_data)):
            create_protocol_filed = CreateObject(driver)
            if protocol_filed_data[n]["object_type"] == "http_signature":
                create_protocol_filed_code = create_protocol_filed.create(protocol_filed_data[n], test_http_signature_object_element_position)
                if create_protocol_filed_code != 200:
                    result = "Fail to create http signature object."
                    break
            elif protocol_filed_data[n]["object_type"] == "url":
                print("to be added...")
    
    # 创建rule
    if create_internal_ip_group_code == 200 and create_internal_port_code == 200 and create_external_ip_code == 200 and create_protocol_filed_code == 200:
        create_rule = CreateRule(driver)
        create_rule_code = create_rule.create(test_data, test_rule_element_position)
        if create_rule_code != 200:
            result = "Fail to create security rule."
        
    # 触发流量验证
    if create_rule_code == 200:
        verify = TrafficVerification()
        verification_result = verify.traffic_verification(parameter, test_data, template_path, [])
        print("verification result: ", verification_result)
    
    # 分析验证结果，并返回给flask
    if len(verification_result) != 0:
        analysis = AnalysisResult()
        result = analysis.analysis_result(test_data, [], verification_result)
        print("analysis result: ", result)
    
    # 删除rule
    if create_rule_code == 200:
        search_rule = SearchRule(driver)
        search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
        if search_rule_code == 200:
            delete_rule = DeleteRule(driver)
            delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
            if delete_rule_code != 200:
                result = result + " In addition, fail to delete security rule."
        else:
            result = result + " In addition, fail to search security rule."
    
    # 删除object
    delete_rule_code = 200
    if delete_rule_code == 200:
        for t in range(len(internal_ip_group_data)):
            search_ip_group = SearchObject(driver)
            search_ip_group_code, first_row_checkbox_element = search_ip_group.search(internal_ip_group_data[t]["name"], test_ip_group_object_element_position)
            if search_ip_group_code == 200:
                delete_ip_group = DeleteObject(driver)
                delete_ip_group_code = delete_ip_group.delete(test_ip_group_object_element_position, first_row_checkbox_element, True)
                if delete_ip_group_code == 200:
                    include_ip_data = internal_ip_group_data[t]["group_subordinate"]
                    for t1 in range(len(include_ip_data)):
                        search_ip = SearchObject(driver)
                        search_ip_code, first_row_checkbox_element = search_ip.search(include_ip_data[t1]["name"], test_ip_object_element_position)
                        if search_ip_code == 200:
                            delete_ip = DeleteObject(driver)
                            delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
                            if delete_ip_code != 200:
                                result = result + " In addition, fail to delete include internal ip object."
                                break
                        else:
                            result = result + " In addition, fail to search include internal ip object."
                            break
                    exclude_ip_data = internal_ip_group_data[t]["group_exclude"]
                    for t2 in range(len(exclude_ip_data)):
                        search_ip = SearchObject(driver)
                        search_ip_code, first_row_checkbox_element = search_ip.search(exclude_ip_data[t2]["name"], test_ip_object_element_position)
                        if search_ip_code == 200:
                            delete_ip = DeleteObject(driver)
                            delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
                            if delete_ip_code != 200:
                                result = result + " In addition, fail to delete exclude internal ip object."
                                break
                        else:
                            result = result + " In addition, fail to search exclude internal ip object."
                            break
                elif delete_ip_group_code != 200:
                    result = result + " In addition, fail to delete internal ip group object."
                    break
            else:
               result = result + " In addition, fail to search internal ip group object."
               break
        # for x in range(len(internal_ip_data)):
        #     search_ip = SearchObject(driver)
        #     search_ip_code, first_row_checkbox_element = search_ip.search(internal_ip_data[x]["name"], test_ip_object_element_position)
        #     if search_ip_code == 200:
        #         delete_ip = DeleteObject(driver)
        #         delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
        #         if delete_ip_code != 200:
        #             result = result + " In addition, fail to delete internal ip object."
        #             break
        #     else:
        #        result = result + " In addition, fail to search internal ip object."
        #        break
        for z in range(len(external_ip_data)):
            search_ip = SearchObject(driver)
            search_ip_code, first_row_checkbox_element = search_ip.search(external_ip_data[z]["name"], test_ip_object_element_position)
            if search_ip_code == 200:
                delete_ip = DeleteObject(driver)
                delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
                if delete_ip_code != 200:
                    result = result + " In addition, fail to delete external ip object."
                    break
            else:
               result = result + " In addition, fail to search external ip object."
               break
        for y in range(len(internal_port_data)):
            search_port = SearchObject(driver)
            search_port_code, first_row_checkbox_element = search_port.search(internal_port_data[y]["name"], test_port_object_element_position)
            if search_port_code == 200:
                delete_port = DeleteObject(driver)
                delete_port_code = delete_port.delete(test_port_object_element_position, first_row_checkbox_element, True)
                if delete_port_code != 200:
                    result = result + " In addition, fail to delete internal port object."
                    break
            else:
               result = result + " In addition, fail to search internal port object."
               break
        for n in range(len(protocol_filed_data)):
            if protocol_filed_data[n]["object_type"] == "http_signature":
                search_protocol_filed = SearchObject(driver)
                search_protocol_filed_code, first_row_checkbox_element = search_protocol_filed.search(protocol_filed_data[n]["name"], test_http_signature_object_element_position)
                if search_protocol_filed_code == 200:
                    delete_protocol_filed = DeleteObject(driver)
                    delete_protocol_filed_code = delete_protocol_filed.delete(test_http_signature_object_element_position, first_row_checkbox_element, True)
                    if delete_protocol_filed_code != 200:
                        result = result + " In addition, fail to delete http signature object."
                        break
                else:
                    result = result + " In addition, fail to search http signature object."
                    break
            elif protocol_filed_data[n]["object_type"] == "url":
                print("to be added...")
    
    # 清理环境
    support.ui_utils.env_initialization.teardown()
    # support.ui_utils.env_initialization.kill_selenium()
    
    # 脚本结束时间和耗时
    end_time = time.time()
    duration = end_time - start_time
    print("duration: ", duration)
    
    print("Finish test case: " + parameter["test_case_name"])
    return result

if __name__ == '__main__':
    parameter = {
      "username": "zhaokun",
      "password": "zhaokun1",
      "test_pc_ip": "192.168.64.73",
      "api_server": "http://192.168.44.72",
      "is_log": 0,
      "env": "tsgx",
      "vsys_id": 6,
      "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
      "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
      "module_name": "security",
      "test_case_name": "security_rule_test"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """