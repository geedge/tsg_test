# -*- coding: UTF-8 -*-
import time
import os
import sys
import os
import sys

from support.api_utils.delete_config import DeleteConfig
from support.ui_utils.profile.search_profile import SearchProfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.policy.edit_rule import EditRule
from support.traffic_replay.traffic_verification import *
from support.ui_utils.element_position.map_element_position_library import *
from support.api_utils.analysis_result import *
from support.api_utils.log_in import *
from support.ui_utils.profile.create_monitor_profile import CreateProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
import support.ui_utils.env_initialization
import traceback


def run(parameter):
    try:
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
            "policy_type": "monitor",
            "rule_name": "monitor_rule_ssl_sni_true",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [
                    {
                        "name": "monitor_source_ip",
                        "object_type": "ip",
                        "select_type": False,
                        "negate": False,
                        "item": [
                            {
                                "item_operation": "add",
                                "item_type": "ipv4",
                                "item_value": "192.168.64.91",
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
                        "name": "ssl",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed":[
                        {
                            "name": "True",  #
                            "object_type": "boolean",
                            "boolean_type": "NO SNI"
                        }
                ],
                "sub_action_override": True,
                "sub_action": [],
                "packet_capture": []
            },
            "is_mirror":"on",
            "profile": [

                        {
                            "name":"profile1",
                            "vlan_id":"10"
                            #vlan的范围：应该是在3-66
                        }
             ],
            "expected_return": "502",
            "counters_1": {"hits": "many"},
            "log_query_param_1": [{"query_field_key": "client_ip", "query_value": "192.168.64.91"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv https://111.2.182.231"
            },
            "token": ""
        }
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        # name_list汇总
        name_list = [
            {
                "type": "monitor",
                "name": "monitor_rule_ssl_sni_true"
            },
            {
                "type":"ip",
                "name":"monitor_source_ip"
            },
            {
                "type": "traffic_mirror",
                "name": "profile1"
            }

        ]

        # 添加定位库集合
        test_rule_element_position = {}
        if test_data["policy_type"] == "monitor":
            test_ip_object_element_position = {
                "page_jump": {
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


            test_monitor_profile_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
                    "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_trafficMirroringProfiles_posId
                },
                "create": {
                    "profileListPage_createButton_posId": listPage_profile_trafficMirroringProfiles_createButton_posId,
                    "profilePage_inputName_posId": trafficMirroringProfiles_input_Name_posId,
                    "profilePage_addLANID_posCss": trafficMirroringProfiles_button_vlanIdAdd_posCss,
                    "trafficMirroringProfiles_input_vlanIdsInput_posXpath": trafficMirroringProfiles_input_vlanIdsInput_posXpath,
                    "profilePage_button_oK_posCss": trafficMirroringProfiles_button_oK_posCss,
                    "profilePage_button_cancel_posCss": trafficMirroringProfiles_button_cancel_posCss,
                    "profilePage_button_warningSaveYes_posCss": trafficMirroringProfiles_button_warningSaveYes_posCss,
                    # action
                },
                "edit": {
                    "templates_button_chartEdit_posXpath": listPage_profile_statisticsTemplates_editButton_posId
                },
                "search": {
                    "profileListPage_searchLabel_posId": listPage_profileSearch_trafficMirroringProfiles_selectLabel_posId,
                    "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_trafficMirroringProfiles_dropDown_item_posXpath,
                    "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_trafficMirroringProfiles_input_itemContent_posXpath,
                    "profileListPage_tableTbody_posXpath": listPage_profilTable_trafficMirroringProfiles_tableTbody_posXpath
                },
                "delete": {
                    "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
                    "profileListPage_deleteButton_posId": listPage_profile_trafficMirroringProfiles_delButton_posId,
                    "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_trafficMirroringProfiles_button_yes_posCss
                }
            }


            test_rule_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
                    "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_monitor_posId
                },
                "create": {
                    "policyRuleListPage_createButton_posId": monitorRuleListPage_createButton_posId,
                    "policyRulePage_inputName_posXpath": securityRulePage_inputName_posXpath,
                    "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": securityRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": securityRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
                    "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                    "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                    "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                    "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                    "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                    "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                    "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
                    "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                    "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                    "policyRulePage_okButton_yes_posId": monitorRulePage_okButton_posId,
                    "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath,
                    # profile
                    "policyRulePage_mirrorTrafficButton_posXpath": monitorRulePage_mirrorTrafficButton_posXpath,
                    "policyRulePage_addVLANIDButton_posXpath": monitorRulePage_addVLANIDButton_posXpath,
                    "policyRulePage_firstSelectMirrorProfile_posXpath": monitorRulePage_firstSelectMirrorProfile_posXpath,
                    "policyRulePage_searchMirrorProfile_posXpath": monitorRulePage_searchMirrorProfile_posXpath,
                    "policyRulePage_selectMirrorProfile_posXpath": monitorRulePage_selectMirrorProfile_posXpath,
                    "policyRulePage_saveProile_ok_posXpath":monitorRulePage_saveProile_ok_posXpath,
                    "policyRulePage_saveProile_warningYes_posXpath":monitorRulePage_saveProile_warningYes_posXpath,
                    #add ssl sni
                    "policyRulePage_addConditionBoolean_posXpath": policyRulePage_addCondition_Boolean_posXpath,
                    "policyRulePage_addBoolean_posXpath": policyRulePage_addBoolean_posXpath,
                    "policyRulePage_searchBoolean_posXpath": policyRulePage_searchBoolean_posXpath,
                    "policyRulePage_selectBoolean_posXpath": policyRulePage_selectBoolean_posXpath,
                    "policyRulePage_closeBoolean_posXpath": policyRulePage_closeBoolean_posXpath,
                    "policyRulePage_little_button_addBoolean_posXpath":policyRulePage_little_button_addBoolean_posXpath
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
                    "policyRuleListPage_deleteButton_posId": monitorRuleListPage_deleteButton_posId,
                    "policyRuleListPage_okButton_warningYes_posXpath": securityRuleListpage_okButton_warningYes_posXpath,
                    "policyRuleListPage_okButton_warningNo_posXpath": securityRuleListpage_okButton_warningNo_posXpath
                }
            }
        #创建object
        if "source_ip" in test_data["condition"] and len(test_data["condition"]["source_ip"]) != 0:
            ip_data =test_data["condition"]["source_ip"]
            create_ip = CreateObject(driver)
            for i in range(len(ip_data)):
                create_ip_code =create_ip.create(ip_data[i],test_ip_object_element_position)
                if create_ip_code == 200:
                    print("Create ip object successfully.")
                elif create_ip_code != 200:
                    result = "Fail to create ip object."
                    break

        if "profile" in test_data  and len(test_data["profile"]) != 0:
            profile_data = test_data["profile"]
            mirror_traffic_profile = CreateProfile(driver,test_monitor_profile_element_position)
            for i in range(len(profile_data)):
                create_profile_code = mirror_traffic_profile.create_monitor_profile(profile_data[i],test_monitor_profile_element_position,test_data["profile"][i]["name"])
                if create_profile_code == 200:
                    print("Create Traffic Mirroring Profiles successfully.")
                elif create_profile_code != 200:
                    result = "Fail to create Traffic Mirroring Profiles profile."
                    break

        # 创建rule
        if create_ip_code == 200:
            create_rule = CreateRule(driver)
            create_rule_code = create_rule.create(test_data, test_rule_element_position)
            if create_rule_code == 200:
                print("Create security rule successfully.")
            elif create_rule_code != 200:
                result = "Fail to create security rule."
        # 触发流量验证
        if create_rule_code == 200:
            edit_rule = EditRule(driver)
            edit_rule_code, rule_id = edit_rule.edit(test_data["policy_type"], test_data["rule_name"],
                                                     test_rule_element_position)
            if edit_rule_code == 200:
                # rule_id = search_rule.get_rule_id()
                test_data["rule_id"] = rule_id
                verify = TrafficVerification()
                verification_result = verify.traffic_verification(driver, parameter, test_data, [])
                if len(verification_result) == 4:
                    driver = verification_result[3]
                elif len(verification_result) == 5:
                    driver = verification_result[4]

        # 分析验证结果，并返回给flask
        if len(verification_result) != 0:
            analysis = AnalysisResult()
            result = analysis.analysis_result(test_data, [], verification_result)
            if len(result) == 0:
                print("The test case is passed.")
            elif len(result) != 0:
                print("The test case is failed. The failure reason is: ", result)

        # 删除rule
        if create_rule_code == 200:
            search_rule = SearchRule(driver)
            search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"],
                                                                              test_data["rule_name"],
                                                                              test_rule_element_position)
            if search_rule_code == 200:
                delete_rule = DeleteRule(driver)
                delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
                if delete_rule_code == 200:
                    print("Delete security rule successfully.")
                elif delete_rule_code != 200:
                    result = result + " In addition, fail to delete security rule."
            else:
                result = result + " In addition, fail to search security rule."

        # 删除object
        if delete_rule_code == 200:
            # 删除ip
            for x in range(len(ip_data)):
                search_ip = SearchObject(driver)
                search_ip_code, first_row_checkbox_element = search_ip.search(ip_data[x]["name"],
                                                                              test_ip_object_element_position)
                if search_ip_code == 200:
                    delete_ip = DeleteObject(driver)
                    delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
                    if delete_ip_code == 200:
                        print("Delete ip object successfully.")
                    elif delete_ip_code != 200:
                        result = result + " In addition, fail to delete ip object."
                        break
                else:
                    result = result + " In addition, fail to search ip object."
                    break

        #删除profile
        if delete_rule_code == 200:
            for x in range(len(profile_data)):
                search_mirror_profile = SearchProfile(driver)
                profile_return_code,first_row_checkbox_element=search_mirror_profile.search(profile_data[x]['name'],test_monitor_profile_element_position)
                if profile_return_code == 200:
                    delete_mirror_profile = DeleteProfile(driver)
                    delete_profile_code = delete_mirror_profile.delete(test_monitor_profile_element_position,first_row_checkbox_element,True)
                    if delete_profile_code == 200:
                        print("Delete monitor profile successfully.")
                    elif delete_profile_code != 200:
                        result = result + " In addition, fail to delete profile."
                        break
                # else:
                    result = result + " In addition, fail to search profile."
                    break


        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print("Duration of running the test case: ", duration)

        print("Finish test case: " + parameter["test_case_name"])
        return result
    except Exception as e:
        print("Error: ", e)
        return "Error: " + str(e)
    finally:
        # 清理环境
        support.ui_utils.env_initialization.teardown()
        # 删除配置
        erase = DeleteConfig()
        erase.clear_config(token, parameter, name_list)

if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.91",
        "api_server": "http://192.168.44.72",
        "is_log": 1,
        "env": "tsgx",
        "script_type":"ui",
        "vsys_id": 11,
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/testcase/ui",
        "module_name": "monitor",
        "test_case_name": "monitor_rule_ssl_sni_true"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """