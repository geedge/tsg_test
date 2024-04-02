from support.ui_utils import env_initialization
from support.traffic_replay.traffic_verification import TrafficVerification
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.api_utils.analysis_result import *
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
import traceback


class ManipulationPub():
    """
    Manipulation策略创建时调用公共方法
    """
    def __init__(self, test_data):
        self.test_data = test_data
        self.generate_location_library()

    def initiate_selenium_setup(self):
        # 环境初始化
        env_initialization.initiate_selenium_request()
        self.driver = env_initialization.my_driver()
        env_initialization.setup()
        return self.driver

    def selenium_teardown(self):
        env_initialization.teardown()

    def generate_location_library(self):
        # 添加定位库集合
        self.element_map = {}
        if self.test_data["policy_type"] == "manipulation":
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
            test_ip_group_object_element_position = {
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
                "page_jump": {
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
                "page_jump": {
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
                "page_jump": {
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
                    "policyRuleListPage_okButton_warningNo_posXpath": securityRuleListpage_okButton_warningNo_posXpath
                }
            }
            self.element_map["ip"] = test_ip_object_element_position
            self.element_map["ip_group"] = test_ip_group_object_element_position
            self.element_map["port"] = test_port_object_element_position
            self.element_map["http_signature"] = test_http_signature_object_element_position

    def create_condition(self):
        #创建condition
        group_object_type = {}
        group_object_type["ip_group"] = "IP"
        for condi in self.test_data["condition"]:   # 遍历condition
            if len(condi) != 0:    #不为空则执行创建
                condi_data = self.test_data["condition"][condi]
                if not isinstance(condi_data, list):   # 不是list列表，跳过执行
                    continue
                create_obj = CreateObject(self.driver)
                for i in range(len(condi_data)):    # 遍历内部创建obj
                    print(condi_data[i])
                    create_obj_code = 200
                    object_type = condi_data[i]["object_type"]
                    if object_type == "application":
                        continue     # application暂时使用默认
                    try:
                        condi_element_map = self.element_map[object_type]
                    except Exception as e:
                        print("Exception type:{}".format(type(e).__name__))
                        traceback.print_exc()  # 打印异常的完整堆栈跟踪
                    if "group" in object_type:   # 包含子对象、排除对象的创建方式
                        if "group_subordinate" in condi_data[i].keys() and len(condi_data[i]) != 0:   # group_subordinate存在且有值
                            for x in range(len(condi_data[i]["group_subordinate"])):
                                condi_element_map = self.element_map[condi_data[i]["group_subordinate"][x]["object_type"]]  # 最里层object_type
                                create_obj_code = create_obj.create(condi_data[i]["group_subordinate"][x], condi_element_map)  # 创建object
                                if create_obj_code != 200:  # obj操作失败，直接返回了。
                                    result = "Fail to create {} object.".format(condi_data[i]["group_subordinate"][x]["object_type"].replace("_", " "))
                                    print(result)
                                    return 400
                        if "group_exclude"  in condi_data[i].keys() and len(condi_data[i]) != 0:   # group_exclude存在且有值
                            for y in range(len(condi_data[i]["group_exclude"])):
                                condi_element_map = self.element_map[condi_data[i]["group_exclude"][y]["object_type"]]  # 最里层object_type
                                create_obj_code = create_obj.create(condi_data[i]["group_exclude"][y], condi_element_map)  # 创建object
                                if create_obj_code != 200:  # obj操作失败，直接返回了。
                                    result = "Fail to create {} object.".format(condi_data[i]["group_exclude"][y]["object_type"].replace("_", " "))
                                    print(result)
                                    return 400
                        condi_element_map = self.element_map[object_type]   # group_type的
                        create_obj_code = create_obj.create_group(condi_data[i], group_object_type[object_type], condi_element_map)  # 创建object group
                    else:
                        create_obj_code = create_obj.create(condi_data[i], condi_element_map)   #创建object
                    if create_obj_code != 200:   # obj操作失败，直接返回了。
                        result = "Fail to create {} object.".format(object_type.replace("_", " "))
                        print(result)
                        return 400
        # obj执行全部成功，返回200。
        return 200

    def create_action_parameters(self):
        pass

    def create_rule(self):
        create_rule = CreateRule(self.driver)
        create_rule_code = create_rule.create(self.test_data, self.test_rule_element_position)
        if create_rule_code != 200:
            result = "Fail to create security rule."

    def verification_and_analysis(self, parameter):
        # 添加测试过程中涉及的template
        template_path = {}
        template_path["trex_workpath"] = "/opt/trex/v3.03"
        template_path["traffic_playback_workpath"] = parameter["root_path"] + "/src/traffic_replay"
        verify = TrafficVerification()
        verification_result = verify.traffic_verification(parameter, self.test_data, template_path, [])
        print("verification result: ", verification_result)

        # 分析验证结果，并返回给flask
        if len(verification_result) != 0:
            analysis = AnalysisResult()
            result = analysis.analysis_result(self.test_data, [], verification_result)
            print("analysis result: ", result)

    def delete_rule(self):
        search_rule = SearchRule(self.driver)
        search_rule_code, first_row_checkbox_element = search_rule.search(self.test_data["policy_type"],
                                                                          self.test_data["rule_name"],
                                                                          self.test_rule_element_position)
        if search_rule_code == 200:
            delete_rule = DeleteRule(self.driver)
            delete_rule_code = delete_rule.delete(self.test_rule_element_position, first_row_checkbox_element, True)
            if delete_rule_code != 200:
                result =  " In addition, fail to delete security rule."
        else:
            result = " In addition, fail to search security rule."

    def delete_condition(self):
        delete_rule_code = 200
        if delete_rule_code == 200:
            for t in range(len(internal_ip_group_data)):
                search_ip_group = SearchObject(self.driver)
                search_ip_group_code, first_row_checkbox_element = search_ip_group.search(internal_ip_group_data[t]["name"],
                                                                                          self.test_ip_group_object_element_position)
                if search_ip_group_code == 200:
                    delete_ip_group = DeleteObject(self.driver)
                    delete_ip_group_code = delete_ip_group.delete(self.test_ip_group_object_element_position,
                                                                  first_row_checkbox_element, True)
