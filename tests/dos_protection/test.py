import os
import sys
import time
from datetime import datetime, timedelta
import pytz
from support.api_utils.log_in import LogIn
from support.packet_generator.ui_verification import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from support.instance_utils.data_translation import DataTranslation

import support.api_utils.get_log
import support.api_utils.policy_verify
import support.ui_utils.env
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.api_utils.log_in import LogIn
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.create_policy import CreatePolicy
from support.packet_generator.verify import Verify
from support.api_utils.analysis_result import AnalysisResult
from support.instance_utils.data_translation import DataTranslation
import support.ui_utils.env
from datetime import datetime
from support.ui_utils.element_position.map_element_position_library import *
def main():
    # 已知参数
    test_rule_element_position = {
        "page_jump": {
            "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
            "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
            "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
            "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
            "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_dos_posId
        },
        "create": {
            "policyRuleListPage_createButton_posId": dosRuleListPage_createButton_posId,
            "policyRulePage_inputName_posXpath": dosRulePage_inputName_posXpath,
            "policyRulePage_selectAction_posId": dosRulePage_selectShunt_posId,
            "policyRulePage_addSrcIP_posXpath": dosRulePage_addSrcIP_posXpath,
            "policyRulePage_searchSrcIP_posXpath": dosRulePage_searchSrcIP_posXpath,
            "policyRulePage_selectSrcIP_posXpath": dosRulePage_selectSrcIP_posXpath,
            "policyRulePage_closeSrcIP_posXpath": dosRulePage_closeSrcIP_posXpath,
            "policyRulePage_addApplication_posXpath": dosRulePage_addApplication_posXpath,
            "policyRulePage_selectApplicationLabel_posXpath": dosRulePage_selectApplicationLabel_posXpath,
            "policyRulePage_searchApplication_posXpath": dosRulePage_searchApplication_posXpath,
            "policyRulePage_selectApplication_posXpath": dosRulePage_selectApplication_posXpath,
            "policyRulePage_closeApplication_posXpath": dosRulePage_closeApplication_posXpath,
            "policyRulePage_thresholdType_posId": "",
            "policyRulePage_groupBy_dropDownBox_posXpath": dosRulePage_groupBy_dropDownBox_posXpath,
            "policyRulePage_groupBy_select_posXpath": dosRulePage_groupBy_select_posXpath,
            "policyRulePage_requestPerPeriod_posXpath": dosRulePage_requestPerPeriod_posXpath,
            "policyRulePage_countingPeriod_dropDownBox_posXpath": dosRulePage_countingPeriod_dropDownBox_posXpath,
            "policyRulePage_countingPeriod_select_posXpath": dosRulePage_countingPeriod_select_posXpath,
            "policyRulePage_concurrentSsessions_posXpath": dosRulePage_concurrentSsessions_posXpath,
            "policyRulePage_mitigationBehavior_posId": "",
            "policyRulePage_mitigationTimeouts_dropDownBox_posXpath": dosRulePage_mitigationTimeouts_dropDownBox_posXpath,
            "policyRulePage_mitigationTimeouts_select_posXpath": "",
            "policyRulePage_enable_posXpath": dosRulePage_enable_posXpath,
            "policyRulePage_okButton_yes_posId": dosRulePage_ok_posId,
            "policyRulePage_okButton_warningYes_posXpath": dosRulePage_okButton_warningYes_posXpath
        },
        "search": {
            "policyRuleListPage_searchLable_posId": dosRuleListPage_searchLable_posId,
            "policyRuleListPage_searchLable_dropDown_item_posXpath": dosRuleListPage_searchLable_dropDown_item_posXpath,
            "policyRuleListPage_searchLable_input_itemContent_posXpath": dosRuleListPage_searchLable_input_itemContent_posXpath,
            "policyRuleListPage_searchLable_searchButton_posId": dosRuleListPage_searchLable_searchButton_posId,
            "policyRuleListPage_tableTbody_posXpath": dosRuleListPage_tableTbody_posXpath
        },
        "delete": {
            "policyRuleListPage_allSelect_posXpath": dosRuleListPage_allSelect_posXpath,
            "policyRuleListPage_deleteButton_posId": dosRuleListPage_deleteButton_posId,
            "policyRuleListPage_okButton_warningYes_posXpath": dosRuleListpage_okButton_warningYes_posXpath,
            "policyRuleListPage_okButton_warningNo_posXpath": dosRuleListpage_okButton_warningNo_posXpath
        }
    }

    parameter = {
        "username": "lina2024",
        "password": "lina2024",
        "test_pc_ip": "192.168.64.96",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 1,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "E:/tsg_test",
        "path": "E:/tsg_test/tests/ui",
        "module_name": "dos_protection",
        "test_case_name": "dos_protect_srcip_http_rate_srcip_d3"
    }

    # 其他参数
    rule_num = 1
    # 获取开始时间
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.now(utc_tz) - timedelta(seconds=8000)
    start_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    #获取结束时间
    utc_tz = pytz.timezone('UTC')
    current_utc_time = datetime.now(utc_tz)
    end_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    test_data = {
        "is_multi_priority": False,
        "rule_num": 1,
        "policy_type": "dos_protection",
        "rule_name": "dos_protect_srcip_http_rate_srcip_d3",
        "rule_action": "protect",
        "rule_type": "create",
        "do_log": 2,
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
                            "item_value": '10.64.20.223',
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
            ]
        },
        "threshold": {
            "type": "rate",
            "rate_threshold": {
                "group_by": "source_ip",
                "request_per_period": 2,
                "counting_period": "1min"
            }
        },
        "mitigation": {
            "behavior": "none",
        },
        "expected_return": "",
        "counters": {"hits": "many"},
        "log_query_param": [
            {"query_field_key": "attack_type", "query_value": "custom_network_attack"},
            {"query_field_key": "sessions", "query_value": ""},
            {"query_field_key": "packets", "query_value": ""},
            {"query_field_key": "bytes", "query_value": ""},
            {"query_field_key": "bit_rate", "query_value": ""},
            {"query_field_key": "packet_rate", "query_value": ""},
            {"query_field_key": "session_rate", "query_value": ""},
        ],
        "traffic": {
            "protocol": "",
            "type": "trex",
            "clients_start_ip": "10.64.12.191",
            "clients_end_ip": "10.64.12.191",
            "servers_start_ip": "2.1.1.21",
            "servers_end_ip": "2.1.1.21",
            "m": 2,
            "d": 5,
            "yaml_name": "test",
            "pcap_name": "http"
        },
        "token": "",
        'rule_id': '158489'
    }
    output = {'total_bytes': 978822, 'total_bytes_received': 901953, 'total_bytes_sent': 76869, 'total_packets': 873, 'total_packets_received': 675, 'total_packets_sent': 198, 'total_syn_pkt': 9}
    log_in = LogIn()
    pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
    token = log_in.login(parameter["username"], pwd, parameter["api_server"])
    test_data["token"] = token

    # support.ui_utils.env.initiate_selenium_request()
    # driver = support.ui_utils.env.my_driver()
    # support.ui_utils.env.setup()

    # 数据转换，适配API的test_data
    translation = DataTranslation()
    temp_test_data = translation.data_translation(test_data["policy_type"], test_data)
    test_data["obj_condition"] = temp_test_data["obj_condition"]
    test_data["application"] = temp_test_data["application"]
    print(test_data)

    # 添加测试过程中涉及的template
    template_path = {}
    template_path["rule_template"] = parameter["root_path"] + "/support/api_utils/template/rule_template.json"
    template_path["object_template"] = parameter["root_path"] + "/support/api_utils/template/object_template.json"

    # 创建Object、Profile、Rule
    create = CreatePolicy()
    cfg_list = create.create_policy(parameter, test_data, template_path)

    #1.api校验
    api_server = parameter["api_server"]
    vsys_id = parameter["vsys_id"]
    script_type = parameter["script_type"]
    create_policies_ids = [{'dos_protection': test_data['rule_id']}]

    # 调用 GetLog 的 get_log_by_condition 函数
    log = support.api_utils.get_log.GetLog()

    log_result = log.get_log_by_condition(
        token,
        rule_num,
        start_time,
        end_time,
        parameter["test_pc_ip"],
        parameter["test_subcriber_id"],
        create_policies_ids,
        test_data,
        api_server,
        vsys_id,
        script_type,
        output
    )
    #打印 log_result 结果
    print("log_result:", log_result)
    print(test_data)

    # 删除配置
    delete = DeletePolicy()
    delete.delele_policy_by_cfg(token, parameter, cfg_list)
    # #2.ui校验
    # api_verification_result = [True,True,True]
    #
    # ui_verification = UiVerification()
    #
    # ui_verification_result = ui_verification.ui_verification(driver,parameter, test_data, api_verification_result,test_rule_element_position, output,111111)
    # print("ui_verification_result:", ui_verification_result)


if __name__ == "__main__":
    main()


# # 打印所有参数
#         print(f"token: {token}")
#         print(f"rule_num: {rule_num}")
#         print(f"start_time: {start_time}")
#         print(f"end_time: {end_time}")
#         print(f"test_pc_ip: {test_pc_ip}")
#         print(f"test_sub_id: {test_sub_id}")
#         print(f"create_policies_ids: {create_policies_ids}")
#         print(f"test_data: {test_data}")
#         print(f"api_server: {api_host}")
#         print(f"vsys_id: {vsys_id}")
#         print(f"script_type: {script_type}")
#         print(f"output: {output}")

#concurrency_test_data
# test_data = {
#         'is_multi_priority': False,
#         'rule_num': 1,
#         'policy_type': 'dos_protection',
#         'rule_name': 'dos_protect_srcip_http_concurrency_srcip_d3',
#         'rule_action': 'protect',
#         'rule_type': 'create',
#         'do_log': 2,
#         'condition': {
#             'source_ip': [{'name': 'dos_srcip', 'object_type': 'ip', 'select_type': False, 'negate': False,
#                            'item': [{'item_operation': 'add', 'item_type': 'ipv4', 'item_value': '10.64.20.210'}]}],
#             'application': [{'name': 'ssl', 'object_type': 'application', 'negate': False}]
#         },
#         'threshold': {
#             'type': 'concurrency',
#             'concurrency_threshold': {'group_by': 'source_ip', 'concurrent_sessions': 2}
#         },
#         'mitigation': {'behavior': 'deny', 'timeout': '5min'},
#         'expected_return': '',
#         'counters': {'hits': 'many'},
#         'log_query_param': [
#             {'query_field_key': 'attack_type', 'query_value': 'custom_network_attack'},
#             {'query_field_key': 'sessions', 'query_value': ''},
#             {'query_field_key': 'packets', 'query_value': ''},
#             {'query_field_key': 'bytes', 'query_value': ''},
#             {'query_field_key': 'bit_rate', 'query_value': ''},
#             {'query_field_key': 'packet_rate', 'query_value': ''},
#             {'query_field_key': 'session_rate', 'query_value': ''}
#         ],
#         'traffic': {
#             'protocol': '',
#             'type': 'trex',
#             'clients_start_ip': '10.64.20.210',
#             'clients_end_ip': '10.64.20.210',
#             'servers_start_ip': '2.1.1.18',
#             'servers_end_ip': '2.1.1.18',
#             'active_flows': 3,
#             'd': 5,
#             'm': 1,
#             'yaml_name': 'test',
#             'pcap_name': 'tls_long'
#         },
#         'token': 'd21627b9-cb69-4c83-b111-8c8a2149cf26&27&',
#         'rule_id': '157553'
#     }
#     output = {'total_bytes': 19027648, 'total_bytes_received': 18671260, 'total_bytes_sent': 356388, 'total_packets': 18056, 'total_packets_received': 12368, 'total_packets_sent': 5688, 'total_syn_pkt': 4}  # 示例的输出

