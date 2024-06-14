from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.element_position.profile_element_position import *



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
test_fqdn_object_element_position = {}
test_http_url_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
        "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_url_posId
    },
    "create": {
        "objectListPage_createButton_posId": urlObjectListPage_createButton_posId,
        "objectListPage_dropDown_createButton_posId": urlObjectListPage_dropDown_createButton_posId,
        "objectPage_inputName_posXpath": urlObjectPage_inputName_posXpath,
        "objectPage_addItem_posId": urlObjectPage_addItem_posId,
        # item简单定位
        "objectPage_inputItem_posXpath": urlObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": urlObjectPage_saveItem_posXpath,
        "objectPage_okButton_posId": urlObjectPage_okButton_posId,
        "objectPage_okButton_warningYes_posXpath": urlObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posId": urlObjectPage_searchLabel_posId,
        "objectListPage_searchLabel_selectName_posXpath": urlObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": urlObjectPage_tableTbody_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": urlObjectPage_allSelect_posXpath,
        "objectListPage_deleteButton_posId": urlObjectListPage_deleteButton_posId,
        "objectListPage_deleteButton_warningYes_posXpath": urlObjectListPage_deleteButton_warningYes_posXpath
    }
}
test_response_page_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_responsePages_posId
    },
    "create": {
        "profileListPage_createButton_posId": listPage_profile_responsePages_createButton_posId,
        "profilePage_inputName_posId": responsePage_input_Name_posId,
        "profilePage_input_file_posXpath": responsePage_input_file_posXpath,
        "profilePage_okButton_posCss": responsePage_button_oK_posCss,
        "profilePage_okButton_warningYes_posCss": responsePage_button_warningSaveYes_posCss,
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_responsePages_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_responsePages_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_responsePages_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_responsePages_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_responsePages_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_responsePages_button_yes_posXpath
    }
}
test_hijack_file_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_hijackFiles_posId
    },
    "create": {
        "profileListPage_createButton_posId": listPage_profile_hijackFiles_createButton_posId,
        "profilePage_inputName_posId": hijackFiles_input_Name_posId,
        "profilePage_okButton_posCss": hijackFiles_button_oK_posCss,
        "profilePage_okButton_warningYes_posCss": hijackFiles_button_warningSaveYes_posCss,
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_hijackFiles_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_hijackFiles_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_hijackFiles_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_hijackFiles_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_hijackFiles_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_hijackFiles_button_yes_posXpath
    }
}
test_manipulation_rule_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
        "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_manipulation_posId
    },
    "create": {
        "policyRuleListPage_createButton_posId": manipulationRuleListPage_createButton_posId,
        # action
        "policyRulePage_inputName_posXpath": manipulationRulePage_inputName_posXpath,
        "policyRulePage_selectAllow_posId": manipulationRulePage_selectAllow_posId,
        "policyRulePage_selectDeny_posId": manipulationRulePage_selectDeny_posId,
        "policyRulePage_selectMonitor_posId": manipulationRulePage_selectMonitor_posId,
        "policyRulePage_selectRedirect_posId": manipulationRulePage_selectRedirect_posId,
        "policyRulePage_selectReplace_posId": manipulationRulePage_selectReplace_posId,
        "policyRulePage_selectHijack_posId": manipulationRulePage_selectHijack_posId,
        "policyRulePage_selectInsert_posId": manipulationRulePage_selectInsert_posId,
        "policyRulePage_selectEditElement_posId": manipulationRulePage_selectEditElement_posId,
        "policyRulePage_selectRunScript_posId": manipulationRulePage_selectRunScript_posId,
        # Add Condition按钮定位
        "policyRulePage_addCondition_posXpath": manipulationRulePage_addCondition_posXpath,
        # add condition侧滑的关闭定位
        "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
        # Source IP
        "policyRulePage_addConditionSrcIP_posXpath": manipulationRulePage_addCondition_srcIP_posXpath,
        "policyRulePage_addSrcIP_posXpath": manipulationRulePage_addSrcIP_posXpath,
        "policyRulePage_searchSrcIP_posXpath": manipulationRulePage_searchSrcIP_posXpath,
        "policyRulePage_selectSrcIP_posXpath": manipulationRulePage_selectSrcIP_posXpath,
        "policyRulePage_closeSrcIP_posXpath": manipulationRulePage_closeSrcIP_posXpath,
        # Internal IP
        "policyRulePage_addConditionInternalIP_posXpath": manipulationRulePage_addCondition_internalIP_posXpath,
        "policyRulePage_addInternalIP_posXpath": manipulationRulePage_addInternalIP_posXpath,
        "policyRulePage_searchInternalIP_posXpath": manipulationRulePage_searchInternalIP_posXpath,
        "policyRulePage_selectInternalIP_posXpath": manipulationRulePage_selectInternalIP_posXpath,
        "policyRulePage_closeInternalIP_posXpath": manipulationRulePage_closeInternalIP_posXpath,
        # Internal Port
        "policyRulePage_addConditionInternalPort_posXpath": manipulationRulePage_addCondition_internalPort_posXpath,
        "policyRulePage_addInternalPort_posXpath": manipulationRulePage_addInternalPort_posXpath,
        "policyRulePage_searchInternalPort_posXpath": manipulationRulePage_searchInternalPort_posXpath,
        "policyRulePage_selectInternalPort_posXpath": manipulationRulePage_selectInternalPort_posXpath,
        "policyRulePage_closeInternalPort_posXpath": manipulationRulePage_closeInternalPort_posXpath,
        # External IP
        "policyRulePage_addConditionExternalIP_posXpath": manipulationRulePage_addCondition_externalIP_posXpath,
        "policyRulePage_addExternalIP_posXpath": manipulationRulePage_addExternalIP_posXpath,
        "policyRulePage_searchExternalIP_posXpath": manipulationRulePage_searchExternalIP_posXpath,
        "policyRulePage_selectExternalIP_posXpath": manipulationRulePage_selectExternalIP_posXpath,
        "policyRulePage_closeExternalIP_posXpath": manipulationRulePage_closeExternalIP_posXpath,
        # Application
        "policyRulePage_addApplication_posXpath": manipulationRulePage_addApplication_posXpath,
        "policyRulePage_searchApplication_posXpath": manipulationRulePage_searchApplication_posXpath,
        "policyRulePage_selectApplication_posXpath": manipulationRulePage_selectApplication_posXpath,
        "policyRulePage_closeApplication_posXpath": manipulationRulePage_closeApplication_posXpath,
        "policyRulePage_selectApplicationLabel_posXpath": manipulationRulePage_selectApplicationLabel_posXpath,
        "policyRulePage_selectApplicationGroupLabel_posXpath": manipulationRulePage_selectApplicationGroupLabel_posXpath,
        # Server FQDN
        "policyRulePage_addConditionServerFqdn_posXpath": manipulationRulePage_addCondition_serverFqdn_posXpath,
        "policyRulePage_addServerFqdn_posXpath": manipulationRulePage_addServerFqdn_posXpath,
        "policyRulePage_searchServerFqdn_posXpath": manipulationRulePage_searchServerFqdn_posXpath,
        "policyRulePage_selectServerFqdn_posXpath": manipulationRulePage_selectServerFqdn_posXpath,
        "policyRulePage_closeServerFqdn_posXpath": manipulationRulePage_closeServerFqdn_posXpath,
        # url
        "policyRulePage_addConditionUrl_posXpath": manipulationRulePage_addCondition_url_posXpath,
        "policyRulePage_addUrl_posXpath": manipulationRulePage_addUrl_posXpath,
        "policyRulePage_searchUrl_posXpath": manipulationRulePage_searchUrl_posXpath,
        "policyRulePage_selectUrl_posXpath": manipulationRulePage_selectUrl_posXpath,
        "policyRulePage_closeUrl_posXpath": manipulationRulePage_closeUrl_posXpath,
        # request header
        "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
        "policyRulePage_addRequestHeader_posXpath": securityRulePage_addRequestHeader_posXpath,
        "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
        # deny action parameter
        "policyRulePage_deny_addResponseCodeSelectBox_posXpath":manipulationRulePage_deny_addResponseCodeSelectBox_posXpath,
        "policyRulePage_deny_addResponseCodeSelectDropItem_posXpath":manipulationRulePage_deny_addResponseCodeSelectDropItem_posXpath,
        "policyRulePage_deny_addResponseContentSelectBox_posXpath": manipulationRulePage_deny_addResponseContentSelectBox_posXpath,
        "policyRulePage_deny_addResponseContentSelectDropItem_posXpath": manipulationRulePage_deny_addResponseContentSelectDropItem_posXpath,
        "policyRulePage_deny_addResponseContentTextInput_posXpath": manipulationRulePage_deny_addResponseContentTextInput_posXpath,
        "policyRulePage_deny_addResponseContentProfileSelectBox_posXpath": manipulationRulePage_deny_addResponseContentProfileSelectBox_posXpath,
        "policyRulePage_deny_searchResponseProfile_posXpath": manipulationRulePage_deny_searchResponseProfile_posXpath,
        "policyRulePage_deny_searchResponseProfileDorpItem_posXpath": manipulationRulePage_deny_searchResponseProfileDorpItem_posXpath,
        # redirect http action parameter
        "policyRulePage_redirectHttp_addResponseCodeSelectBox_posXpath": manipulationRulePage_redirectHttp_addResponseCodeSelectBox_posXpath,
        "policyRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath": manipulationRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath,
        "policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath": manipulationRulePage_redirectHttp_addRedirectUrlInput_posXpath,
        # replace action parameter
        "policyRulePage_replace_addRegex_posXpath": manipulationRulePage_replace_addRegex_posXpath,
        "policyRulePage_replace_addSearchInSelectBox_posXpath": manipulationRulePage_replace_addSearchInSelectBox_posXpath,
        "policyRulePage_replace_addSearchInSelectDropItem_posXpath": manipulationRulePage_replace_addSearchInSelectDropItem_posXpath,
        "policyRulePage_replace_addFindInput_posXpath": manipulationRulePage_replace_addFindInput_posXpath,
        "policyRulePage_replace_addReplaceWithInput_posXpath": manipulationRulePage_replace_addReplaceWithInput_posXpath,
        # hijack profile action parameter
        "policyRulePage_hijack_addHijackProfileSelectBox_posXpath": manipulationRulePage_hijack_addHijackProfileSelectBox_posXpath,
        "policyRulePage_hijack_searchHijackProfile_posXpath": manipulationRulePage_hijack_searchHijackProfile_posXpath,
        "policyRulePage_hijack_searchHijackProfileDorpItem_posXpath": manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath,
        # 保存策略时，ok cancel warnging定位
        "policyRulePage_enable_posXpath": manipulationRulePage_enable_posXpath,
        "policyRulePage_okButton_yes_posId": manipulationRulePage_okButton_yes_posId,
        "policyRulePage_okButton_warningYes_posXpath": manipulationRulePage_okButton_warningYes_posXpath
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
        "policyRuleListPage_deleteButton_posId": manipulationRuleListPage_deleteButton_posId,
        "policyRuleListPage_okButton_warningYes_posXpath": securityRuleListpage_okButton_warningYes_posXpath,
        "policyRuleListPage_okButton_warningNo_posXpath": securityRuleListpage_okButton_warningNo_posXpath
    }
}
test_statistics_template_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_statisticsTemplates_posId
    },
    "create": {
        "templateListPage_createButton_posId": listPage_profile_statisticsTemplates_createButton_posId,
        "templatePage_inputName_posId": statisticsTemplates_input_Name_posId,
        "templates_button_chartAdd_posXpath": statisticsTemplates_button_chartAdd_posXpath,
        "templates_div_paperGrid_posXpath": statisticsTemplates_div_paperGrid_posXpath,
        "templates_radio_visualizationType_posXpath": statisticsTemplates_radio_visualizationType_posXpath,
        "templates_input_other_posXpath": statisticsTemplates_input_other_posXpath,
        "templates_button_ChartOK_posXpath": statisticsTemplates_button_ChartOK_posXpath,
        "templates_button_oK_posCss": statisticsTemplates_button_oK_posCss,
        "templates_button_warningSaveYes_posCss": statisticsTemplates_button_warningSaveYes_posCss,
        # action
    },
    "edit":{
        "templates_button_chartEdit_posXpath":listPage_profile_statisticsTemplates_editButton_posId
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_statisticsTemplates_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_statisticsTemplates_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_statisticsTemplates_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_statisticsTemplates_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_statisticsTemplates_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_statisticsTemplates_button_yes_posXpath
    }
}
#policy
test_statistics_rule_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_policyFirstLevelMenu_posId": mainPage_policyFirstLevelMenu_posId,
        "mainPage_policySecondLevelMenu_posId": mainPage_policySecondLevelMenu_statistics_posId
    },
    "create": {
        "policyRuleListPage_createButton_posId": statisticsRuleListPage_createButton_posId,
        # action
        "policyRulePage_inputName_posXpath": statisticsRulePage_inputName_posXpath,
        # Add Condition按钮定位
        "policyRulePage_addCondition_posXpath": statisticsRulePage_addCondition_posXpath,
        # add condition侧滑的关闭定位
        "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
        # Source IP
        "policyRulePage_addConditionSrcIP_posXpath": statisticsRulePage_addCondition_srcIP_posXpath,
        "policyRulePage_addSrcIP_posXpath": statisticsRulePage_addSrcIP_posXpath,
        "policyRulePage_searchSrcIP_posXpath": statisticsRulePage_searchSrcIP_posXpath,
        "policyRulePage_selectSrcIP_posXpath": statisticsRulePage_selectSrcIP_posXpath,
        "policyRulePage_closeSrcIP_posXpath": statisticsRulePage_closeSrcIP_posXpath,
        # Internal IP
        "policyRulePage_addConditionInternalIP_posXpath": statisticsRulePage_addCondition_internalIP_posXpath,
        "policyRulePage_addInternalIP_posXpath": statisticsRulePage_addInternalIP_posXpath,
        "policyRulePage_searchInternalIP_posXpath": statisticsRulePage_searchInternalIP_posXpath,
        "policyRulePage_selectInternalIP_posXpath": statisticsRulePage_selectInternalIP_posXpath,
        "policyRulePage_closeInternalIP_posXpath": statisticsRulePage_closeInternalIP_posXpath,
        # Internal Port
        "policyRulePage_addConditionInternalPort_posXpath": statisticsRulePage_addCondition_internalPort_posXpath,
        "policyRulePage_addInternalPort_posXpath": statisticsRulePage_addInternalPort_posXpath,
        "policyRulePage_searchInternalPort_posXpath": statisticsRulePage_searchInternalPort_posXpath,
        "policyRulePage_selectInternalPort_posXpath": statisticsRulePage_selectInternalPort_posXpath,
        "policyRulePage_closeInternalPort_posXpath": statisticsRulePage_closeInternalPort_posXpath,
        # External IP
        "policyRulePage_addConditionExternalIP_posXpath": statisticsRulePage_addCondition_externalIP_posXpath,
        "policyRulePage_addExternalIP_posXpath": statisticsRulePage_addExternalIP_posXpath,
        "policyRulePage_searchExternalIP_posXpath": statisticsRulePage_searchExternalIP_posXpath,
        "policyRulePage_selectExternalIP_posXpath": statisticsRulePage_selectExternalIP_posXpath,
        "policyRulePage_closeExternalIP_posXpath": statisticsRulePage_closeExternalIP_posXpath,
        # Application
        "policyRulePage_addApplication_posXpath": statisticsRulePage_addApplication_posXpath,
        "policyRulePage_searchApplication_posXpath": statisticsRulePage_searchApplication_posXpath,
        "policyRulePage_selectApplication_posXpath": statisticsRulePage_selectApplication_posXpath,
        "policyRulePage_closeApplication_posXpath": statisticsRulePage_closeApplication_posXpath,
        "policyRulePage_selectApplicationLabel_posXpath": statisticsRulePage_selectApplicationLabel_posXpath,
        "policyRulePage_selectApplicationGroupLabel_posXpath": statisticsRulePage_selectApplicationGroupLabel_posXpath,
        # Server FQDN
        "policyRulePage_addConditionServerFqdn_posXpath": statisticsRulePage_addCondition_serverFqdn_posXpath,
        "policyRulePage_addServerFqdn_posXpath": statisticsRulePage_addServerFqdn_posXpath,
        "policyRulePage_searchServerFqdn_posXpath": statisticsRulePage_searchServerFqdn_posXpath,
        "policyRulePage_selectServerFqdn_posXpath": statisticsRulePage_selectServerFqdn_posXpath,
        "policyRulePage_closeServerFqdn_posXpath": statisticsRulePage_closeServerFqdn_posXpath,
        # url
        "policyRulePage_addConditionUrl_posXpath": statisticsRulePage_addCondition_url_posXpath,
        "policyRulePage_addUrl_posXpath": statisticsRulePage_addUrl_posXpath,
        "policyRulePage_searchUrl_posXpath": statisticsRulePage_searchUrl_posXpath,
        "policyRulePage_selectUrl_posXpath": statisticsRulePage_selectUrl_posXpath,
        "policyRulePage_closeUrl_posXpath": statisticsRulePage_closeUrl_posXpath,
        # request header
        "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
        "policyRulePage_addRequestHeader_posXpath": securityRulePage_addRequestHeader_posXpath,
        "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
        # 添加Template按钮
        "plicyRulePage_addStatisticsTemplate_posXpath": statisticsRulePage_add_template_posXpath,
        "policyRulePage_searchProfile_posXpath": statisticsRulePage_search_template_posXpath,
        "policyRulePage_selectProfile_posXpath": statisticsRulePage_select_template_posXpath,
        "policyRulePage_closeProfile_posXpath": statisticsRulePage_close_template_posXpath,
        # 保存策略时，ok cancel warnging定位
        "policyRulePage_enable_posXpath": statisticsRulePage_enable_posXpath,
        "policyRulePage_okButton_yes_posId": statisticsRulePage_okButton_yes_posId,
        "policyRulePage_okButton_warningYes_posXpath": statisticsRulePage_okButton_warningYes_posXpath,
        "policyRulePage_okButton_warningNo_posXpath": statisticsRulePage_okButton_warningNo_posXpath
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
        "policyRuleListPage_deleteButton_posId": statisticsRuleListPage_deleteButton_posId,
        "policyRuleListPage_okButton_warningYes_posXpath": statisticsRulePage_delete_tip_button_warningYes_posXpath,
        "policyRuleListPage_okButton_warningNo_posXpath": statisticsRulePage_delete_tip_button_warningNo_posXpath
    }
}

test_ip_object_element_position=test_ip_object_element_position
test_ip_group_object_element_position=test_ip_group_object_element_position
test_port_object_element_position=test_port_object_element_position
test_fqdn_object_element_position=test_fqdn_object_element_position
test_http_signature_object_element_position=test_http_signature_object_element_position
test_http_url_object_element_position = test_http_url_object_element_position
test_response_page_element_position = test_response_page_element_position
test_hijack_file_element_position = test_hijack_file_element_position
test_manipulation_rule_element_position=test_manipulation_rule_element_position

def get_element_position(key_name):
    # object
    if key_name == "source_ip":
        element_position_map = test_ip_object_element_position
    elif key_name == "source_port":
        element_position_map = test_port_object_element_position
    elif key_name == "http_signature":
        element_position_map = test_http_signature_object_element_position
    elif key_name == "server_fqdn":
        element_position_map = test_fqdn_object_element_position
    elif key_name == "url":
        element_position_map = test_http_url_object_element_position
    # profile
    elif key_name == "response_page":
        element_position_map = test_response_page_element_position
    elif key_name == "hijack_file":
        element_position_map = test_hijack_file_element_position
    elif key_name =="statistics_template":
        element_position_map = test_statistics_template_element_position
    # policy
    elif key_name == "manipulation":
        element_position_map = test_manipulation_rule_element_position
    elif key_name == "statistics":
        element_position_map = test_statistics_rule_element_position
    else:
        print("{} no element position map".format(key_name))
        element_position_map = {}
    return element_position_map

def get_profile_element_position(key_name):
    if key_name == "statistics_template":
        element_position_map = test_statistics_template_element_position
    else:
        print("{} no element position map".format(key_name))
        element_position_map = {}
    return element_position_map


# 勿删 zcw make
manipulation_object_no_create_list = ["application", "sub_action_override"]
manipulation_profile_no_create_list = ["deny_response_text", "redirect_url", "replace_parameter"]