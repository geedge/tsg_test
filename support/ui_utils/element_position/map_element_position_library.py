import copy
import time
from datetime import datetime
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.element_position.profile_element_position import *
from support.ui_utils.element_position.log_element_position import *
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.packet_generator.workpath import workdir
import configparser
import os


#policy
policy_security_rule_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_policyFirstLevelMenu_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_policySecondLevelMenu_security_posId
    },
    "create": {
        # "policyRuleListPage_createButton_posXpath": securityRuleListPage_createButton_posId,
        "policyRulePage_inputName_posXpath": securityRulePage_inputName_posXpath,
        "policyRulePage_selectAction_posXpath": securityRulePage_selectDeny_posXpath,
        "policyRulePage_addConditionInternalPort_posXpath": securityRulePage_addCondition_internalPort_posXpath,
        "policyRulePage_addInternalPort_posXpath": securityRulePage_addInternalPort_posXpath,
        "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
        "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
        "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
        "policyRulePage_searchInternalPort_posXpath": securityRulePage_searchInternalPort_posXpath,
        "policyRulePage_selectInternalPort_posXpath": securityRulePage_selectInternalPort_posXpath,
        "policyRulePage_closeInternalPort_posXpath": securityRulePage_closeInternalPort_posXpath,
        "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
        "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
        "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
        "policyRulePage_subAction_drop_posXpath": securityRulePage_subAction_drop_posXpath,
        "policyRulePage_subAction_drop_dropPkt_posXpath": securityRulePage_subAction_drop_dropPkt_posXpath,
        "policyRulePage_subAction_drop_sendTcpRst_posXpath": securityRulePage_subAction_drop_sendTcpRst_posXpath,
        "policyRulePage_subAction_drop_sendIcmp_posXpath": securityRulePage_subAction_drop_sendIcmp_posXpath,
        "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
        "policyRulePage_okButton_yes_posId": securityRulePage_okButton_yes_posId,
        "policyRulePage_okButton_warningYes_posXpath": securityRulePage_okButton_warningYes_posXpath,
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
    },
    "search": {
        "policyRuleListPage_searchLabel_posXpath": securityRuleListPage_searchLable_posId,
        "policyRuleListPage_searchLabel_dropDown_item_posXpath": ruleListPage_searchLabel_dropDown_item_posXpath, #securityRuleListPage_searchLable_dropDown_item_posXpath,
        "policyRuleListPage_searchLabel_input_itemContent_posXpath": securityRuleListPage_searchLable_input_itemContent_posXpath,
        "policyRuleListPage_searchLabel_searchButton_posId": securityRuleListPage_searchLable_searchButton_posId,
        "policyRuleListPage_tableTbody_posXpath": securityRuleListPage_tableTbody_posXpath
    },
    "delete": {
        "policyRuleListPage_allSelect_posXpath": securityRulelistPage_allSelect_posXpath,
        "policyRuleListPage_deleteButton_posXpath": securityRuleListPage_deleteButton_posId,
        "policyRuleListPage_okButton_warningYes_posXpath": securityRuleListpage_okButton_warningYes_posXpath,
        "policyRuleListPage_okButton_warningNo_posXpath": securityRuleListpage_okButton_warningNo_posXpath
    }
}
policy_monitor_rule_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    "mainPage_policyFirstLevelMenu_posXpath": mainPage_policyFirstLevelMenu_posXpath,
                    "mainPage_policySecondLevelMenu_posXpath": mainPage_policySecondLevelMenu_monitor_posXpath
                },
                "create": {
                    "policyRuleListPage_createButton_posXpath": monitorRuleListPage_createButton_posXpath,
                    "policyRulePage_inputName_posXpath": monitorRulePage_inputName_posXpath,
                    #add Condition,close Condition
                    "policyRulePage_addCondition_posXpath": monitorRulePage_addCondition_posXpath,
                    "policyRulePage_addCondition_close_posXpath": monitorRulePage_addCondition_close_posXpath,
                    #end button
                    "policyRulePage_enable_posXpath": monitorRulePage_enable_posXpath,
                    "policyRulePage_okButton_posXpath":serviceChainingRulePage_okButton_posXpach,
                    "policyRulePage_okButton_yes_posId": monitorRulePage_okButton_posId,
                    "policyRulePage_okButton_warningYes_posXpath": monitorRulePage_okButton_warningYes_posXpath,
                    # add negate
                    "policyRulePage_negateSrcIP_posXpath":monitorRulePage_negateSrcIP_posXpath,
                    "policyRulePage_negateServerFqdn_posXpath":monitorRulePage_negateServerFqdn_posXpath,
                    #add profile/mirror
                    "policyRulePage_mirrorTrafficButton_posXpath": monitorRulePage_mirrorTrafficButton_posXpath,
                    "policyRulePage_addVLANIDButton_posXpath": monitorRulePage_addVLANIDButton_posXpath,
                    "policyRulePage_firstSelectMirrorProfile_posXpath": monitorRulePage_firstSelectMirrorProfile_posXpath,
                    "policyRulePage_searchMirrorProfile_posXpath": monitorRulePage_searchMirrorProfile_posXpath,
                    "policyRulePage_selectMirrorProfile_posXpath": monitorRulePage_selectMirrorProfile_posXpath,
                    #add DstPort
                    "policyRulePage_addConditionDstPort_posXpath": monitorRulePage_addCondition_dstPort_posXpath,
                    "policyRulePage_addDstPort_posXpath": monitorRulePage_addDstPort_posXpath,
                    "policyRulePage_searchDstPort_posXpath": monitorRulePage_searchDstPort_posXpath,
                    "policyRulePage_selectDstPort_posXpath": monitorRulePage_selectDstPort_posXpath,
                    "policyRulePage_closeDstPort_posXpath": monitorRulePage_closeDstPort_posXpath,
                    #添加external port
                    "policyRulePage_addConditionExternalPort_posXpath": monitorRulePage_addCondition_externalPort_posXpath,
                    "policyRulePage_addExternalPort_posXpath": monitorRulePage_addExternalPort_posXpath,
                    "policyRulePage_searchExternalPort_posXpath": monitorRulePage_searchExternalPort_posXpath,
                    "policyRulePage_selectExternalPort_posXpath": monitorRulePage_selectExternalPort_posXpath,
                    "policyRulePage_closeExternalPort_posXpath": monitorRulePage_closeExternalPort_posXpath,
                    #添加internal port
                    "policyRulePage_addConditionInternalPort_posXpath": monitorRulePage_addCondition_internalPort_posXpath,
                    "policyRulePage_addInternalPort_posXpath": monitorRulePage_addInternalPort_posXpath,
                    "policyRulePage_searchInternalPort_posXpath": monitorRulePage_searchInternalPort_posXpath,
                    "policyRulePage_selectInternalPort_posXpath": monitorRulePage_selectInternalPort_posXpath,
                    "policyRulePage_closeInternalPort_posXpath": monitorRulePage_closeInternalPort_posXpath,
                    #add Application
                    "policyRulePage_searchApplication_posXpath": monitorRulePage_searchApplication_posXpath,
                    "policyRulePage_selectApplication_posXpath": monitorRulePage_selectApplication_posXpath,
                    "policyRulePage_closeApplication_posXpath": monitorRulePage_closeApplication_posXpath,
                    "policyRulePage_selectApplicationLabel_posXpath": monitorRulePage_selectApplicationLabel_posXpath,
                    "policyRulePage_addApplication_posXpath": monitorRulePage_addApplication_posXpath,
                    #add app_group
                    "policyRulePage_selectApplicationGroupLabel_posXpath": monitorRulePage_selectApplicationGroupLabel_posXpath,
                    # add flag
                    "policyRulePage_addConditionFlag_posXpath":policyRulePage_addCondition_flag_posXpath,
                    "policyRulePage_addFlag_posXpath": monitorRulePage_addFlag_posXpath,
                    "policyRulePage_searchFlag_posXpath": monitorRulePage_searchFlag_posXpath,
                    "policyRulePage_selectFlag_posXpath": monitorRulePage_selectFlag_posXpath,
                    "policyRulePage_closeFlag_posXpath": monitorRulePage_closeFlag_posXpath,
                    #add Src ip
                    "policyRulePage_addSrcIP_posXpath": monitorRulePage_addSrcIP_posXpath,
                    "policyRulePage_searchSrcIP_posXpath": monitorRulePage_searchSrcIP_posXpath,
                    "policyRulePage_selectSrcIP_posXpath": monitorRulePage_selectSrcIP_posXpath,
                    "policyRulePage_closeSrcIP_posXpath": monitorRulePage_closeSrcIP_posXpath,

                    #add  dst ip
                    "policyRulePage_addDstIP_posXpath": policyRulePage_addDstIP_posXpath,
                    "policyRulePage_searchDstIP_posXpath": policyRulePage_searchDstIP_posXpath,
                    "policyRulePage_selectDstIP_posXpath": policyRulePage_selectDstIP_posXpath,
                    "policyRulePage_closeDstIP_posXpath": policyRulePage_closeDstIP_posXpath,
                    # add internal ip
                    "policyRulePage_addConditionInternalIP_posXpath": policyRulePage_addCondition_internalIP_posXpath,
                    "policyRulePage_addInternalIP_posXpath": monitorRulePage_addInternalIP_posXpath,
                    "policyRulePage_searchInternalIP_posXpath": monitorRulePage_searchInternalIP_posXpath,
                    "policyRulePage_selectInternalIP_posXpath": monitorRulePage_selectInternalIP_posXpath,
                    "policyRulePage_closeInternalIP_posXpath": monitorRulePage_closeInternalIP_posXpath,
                    # add external ip
                    "policyRulePage_addConditionExternalIP_posXpath": policyRulePage_addCondition_externalIP_posXpath,
                    "policyRulePage_addExternalIP_posXpath": monitorRulePage_addExternalIP_posXpath,
                    "policyRulePage_searchExternalIP_posXpath": monitorRulePage_searchExternalIP_posXpath,
                    "policyRulePage_selectExternalIP_posXpath": monitorRulePage_selectExternalIP_posXpath,
                    "policyRulePage_closeExternalIP_posXpath": monitorRulePage_closeExternalIP_posXpath,
                    # add ip Protocol
                    "policyRulePage_addConditionIpProtocol_posXpath": policyRulePage_addCondition_IpProtocol_posXpath,
                    "policyRulePage_addIpProtocol_posXpath": policyRulePage_addIpProtocol_posXpath,
                    "policyRulePage_searchIpProtocol_posXpath": policyRulePage_searchIpProtocol_posXpath,
                    "policyRulePage_selectIpProtocol_posXpath": policyRulePage_selectIpProtocol_posXpath,
                    "policyRulePage_closeIpProtocol_posXpath": policyRulePage_closeIpProtocol_posXpath,
                    # add subid
                    "policyRulePage_addConditionUser_posXpath": monitorRulePage_addCondition_user_posXpath,
                    "policyRulePage_addUser_posXpath": monitorRulePage_addUser_posXpath,
                    "policyRulePage_searchUser_posXpath": monitorRulePage_searchUser_posXpath,
                    "policyRulePage_selectUser_posXpath": monitorRulePage_selectUser_posXpath,
                    "policyRulePage_closeUser_posXpath": monitorRulePage_closeUser_posXpath,
                    # add imsi
                    "policyRulePage_addConditionImsi_posXpath": monitorRulePage_addCondition_imsi_posXpath,
                    "policyRulePage_addImsi_posXpath": monitorRulePage_addImsi_posXpath,
                    "policyRulePage_searchImsi_posXpath": policyRulePage_searchImsi_posXpath,
                    "policyRulePage_selectImsi_posXpath": policyRulePage_selectImsi_posXpath,
                    "policyRulePage_closeImsi_posXpath": policyRulePage_closeImsi_posXpath,
                    # phone number Apn Imei
                    "policyRulePage_choosePhoneNumber_posXpath": monitorRulePage_choosePhoneNumber_posXpath,
                    "policyRulePage_chooseApn_posXpath": policyRulePage_chooseApn_posXpath,
                    "policyRulePage_chooseImei_posXpath":policyRulePage_chooseImei_posXpath,

                    #add Server FQDN
                    "policyRulePage_addConditionServerFqdn_posXpath": policyRulePage_addCondition_serverFqdn_posXpath,
                    "policyRulePage_addServerFqdn_posXpath": policyRulePage_addServerFqdn_posXpath,
                    "policyRulePage_searchServerFqdn_posXpath": policyRulePage_searchServerFqdn_posXpath,
                    "policyRulePage_selectServerFqdn_posXpath": policyRulePage_selectServerFqdn_posXpath,
                    "policyRulePage_closeServerFqdn_posXpath": policyRulePage_closeServerFqdn_posXpath,
                    #add url
                    "policyRulePage_addConditionUrl_posXpath": monitorRulePage_addCondition_url_posXpath,
                    "policyRulePage_addUrl_posXpath": policyRulePage_addUrl_posXpath,
                    "policyRulePage_searchUrl_posXpath": policyRulePage_searchUrl_posXpath,
                    "policyRulePage_selectUrl_posXpath": policyRulePage_selectUrl_posXpath,
                    "policyRulePage_closeUrl_posXpath": policyRulePage_closeUrl_posXpath,
                    #add request header
                    "policyRulePage_addConditionRequestHeader_posXpath": monitorRulePage_addCondition_requestHeader_posXpath,
                    "policyRulePage_addRequestHeader_posXpath": monitorRulePage_addRequestHeader_posXpath,
                    "policyRulePage_searchRequestHeader_posXpath": monitorRulePage_searchRequestHeader_posXpath,
                    "policyRulePage_selectRequestHeader_posXpath": monitorRulePage_selectRequestHeader_posXpath,
                    "policyRulePage_closeRequestHeader_posXpath": monitorRulePage_closeRequestHeader_posXpath,
                    #add response header
                    "policyRulePage_addConditionResponseHeader_posXpath": policyRulePage_addCondition_responseHeader_posXpath,
                    "policyRulePage_addResponseHeader_posXpath": monitorRulePage_addResponseHeader_posXpath,
                    "policyRulePage_searchResponseHeader_posXpath": monitorRulePage_searchResponseHeader_posXpath,
                    "policyRulePage_selectResponseHeader_posXpath": monitorRulePage_selectResponseHeader_posXpath,
                    "policyRulePage_closeResponseHeader_posXpath": monitorRulePage_closeResponseHeader_posXpath,
                    #add request body
                    "policyRulePage_addConditionRequestBody_posXpath": monitorRulePage_addCondition_requestBody_posXpath,
                    "policyRulePage_addRequestBody_posXpath": manipulationRulePage_addRequestBody_posXpath,
                    "policyRulePage_searchRequestBody_posXpath": monitorRulePage_searchRequestHeader_posXpath,
                    "policyRulePage_selectRequestBody_posXpath": monitorRulePage_selectRequestHeader_posXpath,
                    "policyRulePage_closeRequestBody_posXpath": monitorRulePage_closeRequestHeader_posXpath,
                    #add response body
                    "policyRulePage_addConditionResponseBody_posXpath": monitorRulePage_addCondition_responseBody_posXpath,
                    "policyRulePage_addResponseBody_posXpath": manipulationRulePage_addResponseBody_posXpath,
                    "policyRulePage_searchResponseBody_posXpath": monitorRulePage_searchRequestHeader_posXpath,
                    "policyRulePage_selectResponseBody_posXpath": monitorRulePage_selectRequestHeader_posXpath,
                    "policyRulePage_closeResponseBody_posXpath": monitorRulePage_closeRequestHeader_posXpath,
                    #add ssl boolean type
                    "policyRulePage_addConditionBoolean_posXpath": policyRulePage_addCondition_Boolean_posXpath,
                    "policyRulePage_addBoolean_posXpath": policyRulePage_addBoolean_posXpath,
                    "policyRulePage_searchBoolean_posXpath": policyRulePage_searchBoolean_posXpath,
                    "policyRulePage_selectBoolean_posXpath": policyRulePage_selectBoolean_posXpath,
                    "policyRulePage_closeBoolean_posXpath": policyRulePage_closeBoolean_posXpath,
                    "policyRulePage_little_button_addBoolean_posXpath":policyRulePage_little_button_addBoolean_posXpath,
                    # san
                    "policyRulePage_addConditionSan_posXpath": monitorRulePage_addCondition_san_posXpath,
                    "policyRulePage_addSan_posXpath": monitorRulePage_addSan_posXpath,
                    "policyRulePage_searchSan_posXpath": monitorRulePage_searchSan_posXpath,
                    "policyRulePage_selectSan_posXpath": monitorRulePage_selectSan_posXpath,
                    "policyRulePage_closeSan_posXpath": monitorRulePage_closeSan_posXpath,
                    # cn
                    "policyRulePage_addConditionCn_posXpath": monitorRulePage_addCondition_cn_posXpath,
                    "policyRulePage_addCn_posXpath": monitorRulePage_addCn_posXpath,
                    "policyRulePage_searchCn_posXpath": monitorRulePage_searchCn_posXpath,
                    "policyRulePage_selectCn_posXpath": monitorRulePage_selectCn_posXpath,
                    "policyRulePage_closeCn_posXpath": monitorRulePage_closeCn_posXpath,
                    # 添加mail account
                    "policyRulePage_addConditionMailAccount_posXpath": policyRulePage_addCondition_mailAccount_posXpath,
                    "policyRulePage_addMailAccount_posXpath": monitorRulePage_addmailAccount_posXpath,
                    "policyRulePage_searchMailAccount_posXpath": monitorRulePage_searchmailAccount_posXpath,
                    "policyRulePage_selectMailAccount_posXpath": monitorRulePage_selectmailAccount_posXpath,
                    "policyRulePage_closeMailAccount_posXpath": monitorRulePage_closemailAccount_posXpath,
                    #添加mail from
                    "policyRulePage_addConditionMailFrom_posXpath": policyRulePage_addCondition_mailFrom_posXpath,
                    "policyRulePage_addMailFrom_posXpath": monitorRulePage_addmailFrom_posXpath,
                    "policyRulePage_searchMailFrom_posXpath": monitorRulePage_searchmailFrom_posXpath,
                    "policyRulePage_selectMailFrom_posXpath": monitorRulePage_selectmailFrom_posXpath,
                    "policyRulePage_closeMailFrom_posXpath": monitorRulePage_closemailFrom_posXpath,
                    #添加mail to
                    "policyRulePage_addConditionMailTo_posXpath": policyRulePage_addCondition_mailTo_posXpath,
                    "policyRulePage_addMailTo_posXpath": monitorRulePage_addmailTo_posXpath,
                    "policyRulePage_searchMailTo_posXpath": monitorRulePage_searchmailTo_posXpath,
                    "policyRulePage_selectMailTo_posXpath": monitorRulePage_selectmailTo_posXpath,
                    "policyRulePage_closeMailTo_posXpath": monitorRulePage_closemailTo_posXpath,
                    #添加mail subject
                    "policyRulePage_addConditionMailSubject_posXpath": policyRulePage_addCondition_mailSubject_posXpath,
                    "policyRulePage_addMailSubject_posXpath": monitorRulePage_addmailSubject_posXpath,
                    "policyRulePage_searchMailSubject_posXpath": monitorRulePage_searchmailSubject_posXpath,
                    "policyRulePage_selectMailSubject_posXpath": monitorRulePage_selectmailSubject_posXpath,
                    "policyRulePage_closeMailSubject_posXpath": monitorRulePage_closemailSubject_posXpath,
                    #添加mail attachment name
                    "policyRulePage_addConditionMailAttachmentName_posXpath": policyRulePage_addCondition_mailAttachmentName_posXpath,
                    "policyRulePage_addMailAttachmentName_posXpath": policyRulePage_addMailAttachmentName_posXpath,
                    "policyRulePage_searchMailAttachmentName_posXpath": policyRulePage_searchMailAttachmentName_posXpath,
                    "policyRulePage_selectMailAttachmentName_posXpath": policyRulePage_selectMailAttachmentName_posXpath,
                    "policyRulePage_closeMailAttachmentName_posXpath": policyRulePage_closeMailAttachmentName_posXpath,
                    #添加mail attachment content
                    "policyRulePage_addConditionMailAttachmentContent_posXpath": policyRulePage_addCondition_mailAttachmentContent_posXpath,
                    "policyRulePage_addMailAttachmentContent_posXpath": policyRulePage_addMailAttachmentContent_posXpath,
                    "policyRulePage_searchMailAttachmentContent_posXpath": policyRulePage_searchMailAttachmentContent_posXpath,
                    "policyRulePage_selectMailAttachmentContent_posXpath": policyRulePage_selectMailAttachmentContent_posXpath,
                    "policyRulePage_closeMailAttachmentContent_posXpath": policyRulePage_closeMailAttachmentContent_posXpath,
                    #添加mail content
                    "policyRulePage_addConditionMailContent_posXpath": policyRulePage_addCondition_mailContent_posXpath,
                    "policyRulePage_addMailContent_posXpath": policyRulePage_addMailContent_posXpath,
                    "policyRulePage_searchMailContent_posXpath": policyRulePage_searchMailContent_posXpath,
                    "policyRulePage_selectMailContent_posXpath": policyRulePage_selectMailContent_posXpath,
                    "policyRulePage_closeMailContent_posXpath": policyRulePage_closeMailContent_posXpath,
                    # qname
                    "policyRulePage_addConditionQname_posXpath": monitorRulePage_addCondition_qname_posXpath,
                    "policyRulePage_addQname_posXpath": monitorRulePage_addQname_posXpath,
                    "policyRulePage_searchQname_posXpath": monitorRulePage_searchQname_posXpath,
                    "policyRulePage_selectQname_posXpath": monitorRulePage_selectQname_posXpath,
                    "policyRulePage_closeQname_posXpath": monitorRulePage_closeQname_posXpath,
                    # keywords:content
                    "policyRulePage_addConditionFtpContent_posXpath": monitorRulePage_addCondition_ftpContent_posXpath,
                    "policyRulePage_addFtpContent_posXpath": monitorRulePage_addftpContent_posXpath,
                    "policyRulePage_searchFtpContent_posXpath": monitorRulePage_searchftpContent_posXpath,
                    "policyRulePage_selectFtpContent_posXpath": monitorRulePage_selectftpContent_posXpath,
                    "policyRulePage_closeFtpContent_posXpath": monitorRulePage_closeftpContent_posXpath,
                    # 添加account
                    "policyRulePage_addConditionFtpAccount_posXpath": monitorRulePage_addCondition_ftpAccount_posXpath,
                    "policyRulePage_addFtpAccount_posXpath": monitorRulePage_addftpAccount_posXpath,
                    "policyRulePage_searchFtpAccount_posXpath": monitorRulePage_searchftpAccount_posXpath,
                    "policyRulePage_selectFtpAccount_posXpath": monitorRulePage_selectftpAccount_posXpath,
                    "policyRulePage_closeFtpAccount_posXpath": monitorRulePage_closeftpAccount_posXpath,
                    # packet capture depth
                    "policyRulePage_packetCapture_posXpath": monitorRulePage_packetCapture_posXpath,
                    "policyRulePage_packetCapture_depth_posXpath": monitorRulePage_packetCapture_depth_posXpath,
                },
                "search": {
                    "policyRuleListPage_searchLabel_posXpath": monitorRuleListPage_searchLabel_posXpath,
                    "policyRuleListPage_searchLabel_dropDown_item_posXpath": ruleListPage_searchLabel_dropDown_item_posXpath, #monitorRuleListPage_searchLabel_dropDown_item_posXpath,
                    "policyRuleListPage_searchLabel_input_itemContent_posXpath": monitorRuleListPage_searchLabel_input_itemContent_posXpath,
                    "policyRuleListPage_searchLabel_searchButton_posId": monitorRuleListPage_searchLabel_searchButton_posXpath,
                    "policyRuleListPage_tableTbody_posXpath": monitorRuleListPage_tableTbody_posXpath
                },
                "delete": {
                    "policyRuleListPage_allSelect_posXpath": monitorRulelistPage_allSelect_posXpath,
                    "policyRuleListPage_deleteButton_posXpath": monitorRuleListPage_deleteButton_posXpath,
                    "policyRuleListPage_okButton_warningYes_posXpath": monitorRuleListpage_okButton_warningYes_posXpath,
                    "policyRuleListPage_okButton_warningNo_posXpath": monitorRuleListpage_okButton_warningNo_posXpath
                }
            }
policy_dos_protection_rule_element_position = {
                    "page_jump":{
                        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
                        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                        "mainPage_policyFirstLevelMenu_posXpath": mainPage_policyFirstLevelMenu_posXpath,
                        "mainPage_policySecondLevelMenu_posXpath": mainPage_policySecondLevelMenu_dos_posXpath
                    },
                    "create": {
                        "policyRuleListPage_createButton_posXpath": dosRuleListPage_createButton_posXpath,
                        "policyRulePage_inputName_posXpath": dosRulePage_inputName_posXpath,
                        "policyRulePage_selectAction_posXpath": "",
                        "policyRulePage_addSrcIP_posXpath": dosRulePage_addSrcIP_posXpath,
                        "policyRulePage_searchSrcIP_posXpath": dosRulePage_searchSrcIP_posXpath,
                        "policyRulePage_selectSrcIP_posXpath": dosRulePage_selectSrcIP_posXpath,
                        "policyRulePage_closeSrcIP_posXpath": dosRulePage_closeSrcIP_posXpath,
                        "policyRulePage_addApplication_posXpath": dosRulePage_addApplication_posXpath,
                        "policyRulePage_selectApplicationLabel_posXpath": dosRulePage_selectApplicationLabel_posXpath,
                        "policyRulePage_searchApplication_posXpath": dosRulePage_searchApplication_posXpath,
                        "policyRulePage_selectApplication_posXpath": dosRulePage_selectApplication_posXpath,
                        "policyRulePage_closeApplication_posXpath": dosRulePage_closeApplication_posXpath,
                        "policyRulePage_thresholdType_posXpath": "",
                        "policyRulePage_groupBy_dropDownBox_posXpath": dosRulePage_groupBy_dropDownBox_posXpath,
                        "policyRulePage_groupBy_select_posXpath": dosRulePage_groupBy_select_posXpath,
                        "policyRulePage_requestPerPeriod_posXpath": dosRulePage_requestPerPeriod_posXpath,
                        "policyRulePage_countingPeriod_dropDownBox_posXpath": dosRulePage_countingPeriod_dropDownBox_posXpath,
                        "policyRulePage_countingPeriod_select_posXpath": dosRulePage_countingPeriod_select_posXpath,
                        "policyRulePage_concurrentSsessions_posXpath" : dosRulePage_concurrentSsessions_posXpath,
                        "policyRulePage_mitigationBehavior_posXpath": "",
                        "policyRulePage_mitigationTimeouts_dropDownBox_posXpath": dosRulePage_mitigationTimeouts_dropDownBox_posXpath,
                        "policyRulePage_mitigationTimeouts_select_posXpath": "",
                        "policyRulePage_enable_posXpath": dosRulePage_enable_posXpath,
                        "policyRulePage_okButton_posXpath": dosRulePage_ok_posXpath,
                        "policyRulePage_okButton_warningYes_posXpath": dosRulePage_okButton_warningYes_posXpath
                    },
                    "search": {
                        "policyRuleListPage_searchLabel_posXpath": dosRuleListPage_searchLable_posXpath,
                        "policyRuleListPage_searchLabel_dropDown_item_posXpath": ruleListPage_searchLabel_dropDown_item_posXpath, #dosRuleListPage_searchLable_dropDown_item_posXpath,
                        "policyRuleListPage_searchLabel_input_itemContent_posXpath": dosRuleListPage_searchLable_input_itemContent_posXpath,
                        "policyRuleListPage_searchLabel_searchButton_posId": dosRuleListPage_searchLable_searchButton_posXpath,
                        "policyRuleListPage_tableTbody_posXpath": dosRuleListPage_tableTbody_posXpath
                    },
                    "delete": {
                        "policyRuleListPage_allSelect_posXpath": dosRuleListPage_allSelect_posXpath,
                        "policyRuleListPage_deleteButton_posXpath": dosRuleListPage_deleteButton_posXpath,
                        "policyRuleListPage_okButton_warningYes_posXpath": dosRuleListpage_okButton_warningYes_posXpath,
                        "policyRuleListPage_okButton_warningNo_posXpath":dosRuleListpage_okButton_warningNo_posXpath
                    }
                }
policy_statistics_rule_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_policyFirstLevelMenu_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_policySecondLevelMenu_statistics_posXpath
    },
    "create": {
        "policyRuleListPage_createButton_posXpath": statisticsRuleListPage_createButton_posXpath,
        # action
        "policyRulePage_inputName_posXpath": statisticsRulePage_inputName_posXpath,
        # Add Condition按钮定位
        "policyRulePage_addCondition_posXpath": statisticsRulePage_addCondition_posXpath,
        # add condition侧滑的关闭定位
        "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
        # Source IP
        "policyRulePage_addConditionSrcIP_posXpath": policyRulePage_addSrcIP_posXpath,#statisticsRulePage_addCondition_srcIP_posXpath,
        "policyRulePage_addSrcIP_posXpath": statisticsRulePage_addSrcIP_posXpath,
        "policyRulePage_searchSrcIP_posXpath": statisticsRulePage_searchSrcIP_posXpath,
        "policyRulePage_selectSrcIP_posXpath": statisticsRulePage_selectSrcIP_posXpath,
        "policyRulePage_closeSrcIP_posXpath": statisticsRulePage_closeSrcIP_posXpath,
        # source Port
        "policyRulePage_addConditionSrcPort_posXpath": policyRulePage_addCondition_srcPort_posXpath,
        "policyRulePage_addSrcPort_posXpath": statisticsRulePage_addSourcePort_posXpath,
        "policyRulePage_searchSrcPort_posXpath": statisticsRulePage_searchSourcePort_posXpath,
        "policyRulePage_selectSrcPort_posXpath": statisticsRulePage_selectSourcePort_posXpath,
        "policyRulePage_closeSrcPort_posXpath": statisticsRulePage_closeSourcePort_posXpath,
        # Destination IP
        "policyRulePage_addConditionDstIP_posXpath": policyRulePage_addDstIP_posXpath,#statisticsRulePage_addCondition_dstcIP_posXpath,
        "policyRulePage_addDstIP_posXpath": statisticsRulePage_addDstIP_posXpath,
        "policyRulePage_searchDstIP_posXpath": statisticsRulePage_searchDstIP_posXpath,
        "policyRulePage_selectDstIP_posXpath": statisticsRulePage_selectDstIP_posXpath,
        "policyRulePage_closeDstIP_posXpath": statisticsRulePage_closeDstIP_posXpath,
        # Destination Port
        "policyRulePage_addConditionDstPort_posXpath": policyRulePage_addCondition_dstPort_posXpath,
        "policyRulePage_addDstPort_posXpath": manipulationRulePage_addDstPort_posXpath,
        "policyRulePage_searchDstPort_posXpath": manipulationRulePage_searchDstPort_posXpath,
        "policyRulePage_selectDstPort_posXpath": manipulationRulePage_selectDstPort_posXpath,
        "policyRulePage_closeDstPort_posXpath": manipulationRulePage_closeDstPort_posXpath,
        # Internal IP
        "policyRulePage_addConditionInternalIP_posXpath": policyRulePage_addCondition_internalIP_posXpath,
        "policyRulePage_addInternalIP_posXpath": statisticsRulePage_addInternalIP_posXpath,
        "policyRulePage_searchInternalIP_posXpath": statisticsRulePage_searchInternalIP_posXpath,
        "policyRulePage_selectInternalIP_posXpath": statisticsRulePage_selectInternalIP_posXpath,
        "policyRulePage_closeInternalIP_posXpath": statisticsRulePage_closeInternalIP_posXpath,
        # Internal Port
        "policyRulePage_addConditionInternalPort_posXpath": policyRulePage_addCondition_internalPort_posXpath,
        "policyRulePage_addInternalPort_posXpath": statisticsRulePage_addInternalPort_posXpath,
        "policyRulePage_searchInternalPort_posXpath": statisticsRulePage_searchInternalPort_posXpath,
        "policyRulePage_selectInternalPort_posXpath": statisticsRulePage_selectInternalPort_posXpath,
        "policyRulePage_closeInternalPort_posXpath": statisticsRulePage_closeInternalPort_posXpath,
        # External IP
        "policyRulePage_addConditionExternalIP_posXpath": policyRulePage_addCondition_externalIP_posXpath,
        "policyRulePage_addExternalIP_posXpath": statisticsRulePage_addExternalIP_posXpath,
        "policyRulePage_searchExternalIP_posXpath": statisticsRulePage_searchExternalIP_posXpath,
        "policyRulePage_selectExternalIP_posXpath": statisticsRulePage_selectExternalIP_posXpath,
        "policyRulePage_closeExternalIP_posXpath": statisticsRulePage_closeExternalIP_posXpath,
        # external Port
        "policyRulePage_addConditionExternalPort_posXpath": policyRulePage_addCondition_externalPort_posXpath,
        "policyRulePage_addExternalPort_posXpath": manipulationRulePage_addExternalPort_posXpath,
        "policyRulePage_searchExternalPort_posXpath": manipulationRulePage_searchExternalPort_posXpath,
        "policyRulePage_selectExternalPort_posXpath": manipulationRulePage_selectExternalPort_posXpath,
        "policyRulePage_closeExternalPort_posXpath": manipulationRulePage_closeExternalPort_posXpath,
        # subid
        "policyRulePage_addConditionUser_posXpath": policyRulePage_addCondition_User_posXpath,
        "policyRulePage_addUser_posXpath": manipulationRulePage_addUser_posXpath,
        "policyRulePage_searchUser_posXpath": manipulationRulePage_searchUser_posXpath,
        "policyRulePage_selectUser_posXpath": manipulationRulePage_selectUser_posXpath,
        "policyRulePage_closeUser_posXpath": manipulationRulePage_closeUser_posXpath,
        # Device imsi imei phone number
        "policyRulePage_addConditionImsi_posXpath": policyRulePage_addConditionImsi_posXpath,
        "policyRulePage_addImsi_posXpath": manipulationRulePage_addImsi_posXpath,
        "policyRulePage_searchImsi_posXpath": manipulationRulePage_searchImsi_posXpath,
        "policyRulePage_selectImsi_posXpath": manipulationRulePage_selectImsi_posXpath,
        "policyRulePage_closeImsi_posXpath": manipulationRulePage_closeImsi_posXpath,
        "policyRulePage_chooseImei_posXpath": policyRulePage_chooseImei_posXpath,
        "policyRulePage_choosePhoneNumber_posXpath": policyRulePage_choosePhoneNumber_posXpath,
        "policyRulePage_chooseApn_posXpath": policyRulePage_chooseApn_posXpath,
        # Application
        "policyRulePage_addApplication_posXpath": statisticsRulePage_addApplication_posXpath,
        "policyRulePage_searchApplication_posXpath": statisticsRulePage_searchApplication_posXpath,
        "policyRulePage_selectApplication_posXpath": statisticsRulePage_selectApplication_posXpath,
        "policyRulePage_closeApplication_posXpath": statisticsRulePage_closeApplication_posXpath,
        "policyRulePage_selectApplicationLabel_posXpath": statisticsRulePage_selectApplicationLabel_posXpath,
        "policyRulePage_selectApplicationGroupLabel_posXpath": statisticsRulePage_selectApplicationGroupLabel_posXpath,
        # Server FQDN
        "policyRulePage_addConditionServerFqdn_posXpath": policyRulePage_addCondition_serverFqdn_posXpath,
        "policyRulePage_addServerFqdn_posXpath": statisticsRulePage_addServerFqdn_posXpath,
        "policyRulePage_searchServerFqdn_posXpath": statisticsRulePage_searchServerFqdn_posXpath,
        "policyRulePage_selectServerFqdn_posXpath": statisticsRulePage_selectServerFqdn_posXpath,
        "policyRulePage_closeServerFqdn_posXpath": statisticsRulePage_closeServerFqdn_posXpath,
        # Qname
        "policyRulePage_addConditionQname_posXpath": policyRulePage_addCondition_qname_posXpath,
        "policyRulePage_addQname_posXpath": manipulationRulePage_addServerQname_posXpath,
        "policyRulePage_searchQname_posXpath": manipulationRulePage_searchQname_posXpath,
        "policyRulePage_selectQname_posXpath": manipulationRulePage_selectQname_posXpath,
        "policyRulePage_closeQname_posXpath": manipulationRulePage_closeServerQname_posXpath,
        # url
        "policyRulePage_addConditionUrl_posXpath": policyRulePage_addCondition_url_posXpath,
        "policyRulePage_addUrl_posXpath": statisticsRulePage_addUrl_posXpath,
        "policyRulePage_searchUrl_posXpath": statisticsRulePage_searchUrl_posXpath,
        "policyRulePage_selectUrl_posXpath": statisticsRulePage_selectUrl_posXpath,
        "policyRulePage_closeUrl_posXpath": statisticsRulePage_closeUrl_posXpath,
        # request headerpolicyRulePage_addCondition_responseHeader_posXpath
        "policyRulePage_addConditionRequestHeader_posXpath": policyRulePage_addCondition_requestHeader_posXpath,
        "policyRulePage_addRequestHeader_posXpath": statisticsRulePage_addRequestHeader_posXpath,
        "policyRulePage_searchRequestHeader_posXpath": statisticsRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectRequestHeader_posXpath": statisticsRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeRequestHeader_posXpath": statisticsRulePage_closeRequestHeader_posXpath,
        # response header
        "policyRulePage_addConditionResponseHeader_posXpath": policyRulePage_addCondition_responseHeader_posXpath,
        "policyRulePage_addResponseHeader_posXpath": statisticsRulePage_addResponseHeader_posXpath,
        "policyRulePage_searchResponseHeader_posXpath": statisticsRulePage_searchResponseHeader_posXpath,
        "policyRulePage_selectResponseHeader_posXpath": statisticsRulePage_selectResponseHeader_posXpath,
        "policyRulePage_closeResponseHeader_posXpath": statisticsRulePage_closeResponseHeader_posXpath,
        # request body
        "policyRulePage_addConditionRequestBody_posXpath": policyRulePage_addCondition_requestBody_posXpath,
        "policyRulePage_addRequestBody_posXpath": statisticsRulePage_addRequestBody_posXpath,
        "policyRulePage_searchRequestBody_posXpath": statisticsRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectRequestBody_posXpath": statisticsRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeRequestBody_posXpath": statisticsRulePage_closeRequestHeader_posXpath,
        # response body
        "policyRulePage_addConditionResponseBody_posXpath": policyRulePage_addCondition_responseBody_posXpath,
        "policyRulePage_addResponseBody_posXpath": statisticsRulePage_addResponseBody_posXpath,
        "policyRulePage_searchResponseBody_posXpath": statisticsRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectResponseBody_posXpath": statisticsRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeResponseBody_posXpath": statisticsRulePage_closeRequestHeader_posXpath,
        #add boolean
        "policyRulePage_addConditionBoolean_posXpath": policyRulePage_addCondition_Boolean_posXpath,
        "policyRulePage_addBoolean_posXpath": policyRulePage_addBoolean_posXpath,
        "policyRulePage_searchBoolean_posXpath": policyRulePage_searchBoolean_posXpath,
        "policyRulePage_selectBoolean_posXpath": policyRulePage_selectBoolean_posXpath,
        "policyRulePage_closeBoolean_posXpath": policyRulePage_closeBoolean_posXpath,
        "policyRulePage_little_button_addBoolean_posXpath": policyRulePage_little_button_addBoolean_posXpath,
        # san
        "policyRulePage_addConditionSan_posXpath": policyRulePage_addCondition_san_posXpath,
        "policyRulePage_addSan_posXpath": policyRulePage_addSan_posXpath,
        "policyRulePage_searchSan_posXpath": policyRulePage_searchSan_posXpath,
        "policyRulePage_selectSan_posXpath": policyRulePage_selectSan_posXpath,
        "policyRulePage_closeSan_posXpath": policyRulePage_closeSan_posXpath,
        # cn
        "policyRulePage_addConditionCn_posXpath": policyRulePage_addCondition_cn_posXpath,
        "policyRulePage_addCn_posXpath": policyRulePage_addCn_posXpath,
        "policyRulePage_searchCn_posXpath": policyRulePage_searchCn_posXpath,
        "policyRulePage_selectCn_posXpath": policyRulePage_selectCn_posXpath,
        "policyRulePage_closeCn_posXpath": policyRulePage_closeCn_posXpath,
        # 添加Template按钮
        "plicyRulePage_addStatisticsTemplate_posXpath": statisticsRulePage_add_template_posXpath,
        "policyRulePage_searchProfile_posXpath": statisticsRulePage_search_template_posXpath,
        "policyRulePage_selectProfile_posXpath": statisticsRulePage_select_template_posXpath,
        "policyRulePage_closeProfile_posXpath": statisticsRulePage_close_template_posXpath,
        # 保存策略时，ok cancel warnging定位
        "policyRulePage_enable_posXpath": statisticsRulePage_enable_posXpath,
        "policyRulePage_okButton_posXpath": rulePage_okButton_posXpath,
        "policyRulePage_okButton_warningYes_posXpath": statisticsRulePage_okButton_warningYes_posXpath,
        "policyRulePage_okButton_warningNo_posXpath": statisticsRulePage_okButton_warningNo_posXpath
    },
    "search": {
        "policyRuleListPage_searchLabel_posXpath": statisticsRuleListPage_searchLabel_posXpath,
        "policyRuleListPage_searchLabel_dropDown_item_posXpath": ruleListPage_searchLabel_dropDown_item_posXpath, #statisticsRuleListPage_searchLabel_dropDown_item_posXpath,
        "policyRuleListPage_searchLabel_input_itemContent_posXpath": statisticsRuleListPage_searchLabel_input_itemContent_posXpath,
        "policyRuleListPage_searchLabel_searchButton_posId": statisticsRuleListPage_searchLabel_searchButton_posXpath,
        "policyRuleListPage_tableTbody_posXpath": statisticsRruleListPage_tableTbody_posXpath
    },
    "delete": {
        "policyRuleListPage_allSelect_posXpath": statisticsRruleListPage_allSelect_posXpath,
        "policyRuleListPage_deleteButton_posXpath": statisticsRuleListPage_deleteButton_posXpath,
        "policyRuleListPage_okButton_warningYes_posXpath": statisticsRuleListPage_delete_tip_button_warningYes_posXpath,
        "policyRuleListPage_okButton_warningNo_posXpath": statisticsRuleListPage_delete_tip_button_warningNo_posXpath
    }
}
policy_intercept_rule_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_policyFirstLevelMenu_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_policySecondLevelMenu_intercept_posXpath
    },
    "create": {
        "policyRuleListPage_createButton_posXpath": interceptRuleListPage_createButton_posXpath,
        "policyRulePage_inputName_posXpath": interceptRulePage_inputName_posXpath,
        "policyRulePage_selectAction_posXpath": interceptRulePage_selectAction_posXpath,
        "policyRulePage_addConditionInternalPort_posXpath": securityRulePage_addCondition_internalPort_posXpath,
        "policyRulePage_addInternalPort_posXpath": securityRulePage_addInternalPort_posXpath,

        "policyRulePage_searchInternalPort_posXpath": securityRulePage_searchInternalPort_posXpath,
        "policyRulePage_selectInternalPort_posXpath": securityRulePage_selectInternalPort_posXpath,
        "policyRulePage_closeInternalPort_posXpath": securityRulePage_closeInternalPort_posXpath,
        "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
        "policyRulePage_subAction_drop_posXpath": securityRulePage_subAction_drop_posXpath,
        "policyRulePage_subAction_drop_dropPkt_posXpath": securityRulePage_subAction_drop_dropPkt_posXpath,
        "policyRulePage_subAction_drop_sendTcpRst_posXpath": securityRulePage_subAction_drop_sendTcpRst_posXpath,
        "policyRulePage_subAction_drop_sendIcmp_posXpath": securityRulePage_subAction_drop_sendIcmp_posXpath,
        # ok
        "policyRulePage_enable_posXpath": interceptRulePage_enable_posXpath,
        "policyRulePage_okButton_posXpath": interceptRulePage_okButton_posXpath,
        "policyRulePage_okButton_warningYes_posXpath": interceptRulePage_okButton_warningYes_posXpath,
        # Add Condition按钮定位
        "policyRulePage_addCondition_posXpath": interceptRulePage_addCondition_posXpath,
        # add condition侧滑的关闭定位
        "policyRulePage_addCondition_close_posXpath": interceptRulePage_addCondition_close_posXpath,
        # Source IP
        "policyRulePage_addConditionSrcIP_posXpath": manipulationRulePage_addCondition_srcIP_posXpath,
        "policyRulePage_addSrcIP_posXpath": manipulationRulePage_addSrcIP_posXpath,
        "policyRulePage_searchSrcIP_posXpath": manipulationRulePage_searchSrcIP_posXpath,
        "policyRulePage_selectSrcIP_posXpath": manipulationRulePage_selectSrcIP_posXpath,
        "policyRulePage_closeSrcIP_posXpath": manipulationRulePage_closeSrcIP_posXpath,
        "policyRulePage_negateSrcIP_posXpath":interceptRulePage_negateSrcIP_posXpath,
        # Application
        "policyRulePage_addApplication_posXpath": interceptRulePage_addApplication_posXpath,
        "policyRulePage_searchApplication_posXpath": interceptRulePage_searchApplication_posXpath,
        "policyRulePage_selectApplication_posXpath": interceptRulePage_selectApplication_posXpath,
        "policyRulePage_closeApplication_posXpath": interceptRulePage_closeApplication_posXpath,
        "policyRulePage_selectApplicationLabel_posXpath": interceptRulePage_selectApplicationLabel_posXpath,
        "policyRulePage_selectApplicationGroupLabel_posXpath": interceptRulePage_selectApplicationGroupLabel_posXpath,
        # Server FQDN
        "policyRulePage_addConditionServerFqdn_posXpath": interceptRulePage_addCondition_serverFqdn_posXpath,
        "policyRulePage_addServerFqdn_posXpath": interceptRulePage_addServerFqdn_posXpath,
        "policyRulePage_searchServerFqdn_posXpath": interceptRulePage_searchServerFqdn_posXpath,
        "policyRulePage_selectServerFqdn_posXpath": interceptRulePage_selectServerFqdn_posXpath,
        "policyRulePage_closeServerFqdn_posXpath": interceptRulePage_closeServerFqdn_posXpath,
        # action parameter trusted servers
        "policyRulePage_intercept_addTrustedSelectBox_posXpath": interceptRulePage_intercept_addTrustedSelectBox_posXpath,
        "policyRulePage_intercept_searchTrustedInput_posXpath": interceptRulePage_intercept_searchTrustedInput_posXpath,
        "policyRulePage_intercept_searchTrustedDorpItem_posXpath": interceptRulePage_intercept_searchTrustedDorpItem_posXpath,
        # action parameter untrusted servers
        "policyRulePage_intercept_addUntrustedSelectBox_posXpath": interceptRulePage_intercept_addUntrustedSelectBox_posXpath,
        "policyRulePage_intercept_searchUntrustedInput_posXpath": interceptRulePage_intercept_searchUntrustedInput_posXpath,
        "policyRulePage_intercept_searchUntrustedDorpItem_posXpath": interceptRulePage_intercept_searchUntrustedDorpItem_posXpath,
        # action parameter mirror decrypted traffic
        "policyRulePage_intercept_addTrafficMirrorProfileButton_posXpath": interceptRulePage_intercept_addTrafficMirrorProfileButton_posXpath,
        "policyRulePage_intercept_addVlanIDButton_posXpath": interceptRulePage_intercept_addVlanIDButton_posXpath,
        "policyRulePage_intercept_addTrafficMirrorProfileSelectBox_posXpath": interceptRulePage_intercept_addTrafficMirrorProfileSelectBox_posXpath,
        "policyRulePage_intercept_searcTrafficMirrorProfileInput_posXpath": interceptRulePage_intercept_searcTrafficMirrorProfileInput_posXpath,
        "policyRulePage_intercept_searchTrafficMirrorProfileDorpItem_posXpath": interceptRulePage_intercept_searchTrafficMirrorProfileDorpItem_posXpath,
        # action parameter decryption profile
        "policyRulePage_intercept_addDecryptionProfileSelectBox_posXpath": interceptRulePage_intercept_addDecryptionProfileSelectBox_posXpath,
        "policyRulePage_intercept_searchDecryptionProfileInput_posXpath": interceptRulePage_intercept_searchDecryptionProfileInput_posXpath,
        "policyRulePage_intercept_searchDecryptionProfileDorpItem_posXpath": interceptRulePage_intercept_searchDecryptionProfileDorpItem_posXpath,
        # action parameter tcp proxy profile
        "policyRulePage_intercept_addTcpProfileSelectBox_posXpath": interceptRulePage_intercept_addTcpProfileSelectBox_posXpath,
        "policyRulePage_intercept_searchTcpProfileInput_posXpath": interceptRulePage_intercept_searchTcpProfileInput_posXpath,
        "policyRulePage_intercept_searchTcpProfileDorpItem_posXpath": interceptRulePage_intercept_searchTcpProfileDorpItem_posXpath,
    },
    "search": {
        "policyRuleListPage_searchLabel_posXpath": interceptRuleListPage_searchLabel_posXpath,
        "policyRuleListPage_searchLabel_dropDown_item_posXpath": ruleListPage_searchLabel_dropDown_item_posXpath, #interceptRuleListPage_searchLabel_dropDown_item_posXpath,
        "policyRuleListPage_searchLabel_input_itemContent_posXpath": interceptRuleListPage_searchLabel_input_itemContent_posXpath,
        "policyRuleListPage_searchLabel_searchButton_posId": interceptRuleListPage_searchLabel_searchButton_posXpath,
        "policyRuleListPage_tableTbody_posXpath": interceptRuleListPage_tableTbody_posXpath
    },
    "delete": {
        "policyRuleListPage_allSelect_posXpath": interceptRuleListPage_allSelect_posXpath,
        "policyRuleListPage_deleteButton_posXpath": interceptRuleListPage_deleteButton_posXpath,
        "policyRuleListPage_okButton_warningYes_posXpath": interceptRuleListPage_deleteTipButton_warningYes_posXpath,
        "policyRuleListPage_okButton_warningNo_posXpath": interceptRuleListPage_deleteTipButton_warningNo_posXpath
    }
}
policy_manipulation_rule_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_policyFirstLevelMenu_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_policySecondLevelMenu_manipulation_posXpath
    },
    "create": {
        "policyRuleListPage_createButton_posXpath": manipulationRuleListPage_createButton_posXpath,
        # action
        "policyRulePage_inputName_posXpath": manipulationRulePage_inputName_posXpath,
        "policyRulePage_selectAllow_posXpath": manipulationRulePage_selectAllow_posXpath,
        "policyRulePage_selectDeny_posXpath": manipulationRulePage_selectDeny_posXpath,
        "policyRulePage_selectMonitor_posXpath": manipulationRulePage_selectMonitor_posXpath,
        "policyRulePage_selectRedirect_posXpath": manipulationRulePage_selectRedirect_posXpath,
        "policyRulePage_selectModify_posXpath": manipulationRulePage_selectModify_posXpath,
        "policyRulePage_selectHijack_posXpath": manipulationRulePage_selectHijack_posXpath,
        "policyRulePage_selectInsert_posXpath": manipulationRulePage_selectInsert_posXpath,
        "policyRulePage_selectEditElement_posXpath": manipulationRulePage_selectEditElement_posXpath,
        "policyRulePage_selectRunScript_posXpath": manipulationRulePage_selectRunScript_posXpath,
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
        # Destination IP
        "policyRulePage_addConditionDstIP_posXpath": policyRulePage_addDstIP_posXpath,#statisticsRulePage_addCondition_dstcIP_posXpath,
        "policyRulePage_addDstIP_posXpath": statisticsRulePage_addDstIP_posXpath,
        "policyRulePage_searchDstIP_posXpath": statisticsRulePage_searchDstIP_posXpath,
        "policyRulePage_selectDstIP_posXpath": statisticsRulePage_selectDstIP_posXpath,
        "policyRulePage_closeDstIP_posXpath": statisticsRulePage_closeDstIP_posXpath,
        # Internal IP
        "policyRulePage_addConditionInternalIP_posXpath": manipulationRulePage_addCondition_internalIP_posXpath,
        "policyRulePage_addInternalIP_posXpath": manipulationRulePage_addInternalIP_posXpath,
        "policyRulePage_searchInternalIP_posXpath": manipulationRulePage_searchInternalIP_posXpath,
        "policyRulePage_selectInternalIP_posXpath": manipulationRulePage_selectInternalIP_posXpath,
        "policyRulePage_closeInternalIP_posXpath": manipulationRulePage_closeInternalIP_posXpath,
        # source Port
        "policyRulePage_addConditionSrcPort_posXpath": manipulationRulePage_addCondition_srcPort_posXpath,
        "policyRulePage_addSrcPort_posXpath": manipulationPage_addSrcPort_posXpath,
        "policyRulePage_searchSrcPort_posXpath": manipulationRulePage_searchSrcPort_posXpath,
        "policyRulePage_selectSrcPort_posXpath": manipulationRulePage_selectSrcPort_posXpath,
        "policyRulePage_closeSrcPort_posXpath": manipulationRulePage_closeSrcPort_posXpath,
        # Internal Port
        "policyRulePage_addConditionInternalPort_posXpath": manipulationRulePage_addCondition_internalPort_posXpath,
        "policyRulePage_addInternalPort_posXpath": manipulationRulePage_addInternalPort_posXpath,
        "policyRulePage_searchInternalPort_posXpath": manipulationRulePage_searchInternalPort_posXpath,
        "policyRulePage_selectInternalPort_posXpath": manipulationRulePage_selectInternalPort_posXpath,
        "policyRulePage_closeInternalPort_posXpath": manipulationRulePage_closeInternalPort_posXpath,
        # Destination Port
        "policyRulePage_addConditionDstPort_posXpath": manipulationRulePage_addCondition_destinationPort_posXpath,
        "policyRulePage_addDstPort_posXpath": manipulationRulePage_addDstPort_posXpath,
        "policyRulePage_searchDstPort_posXpath": manipulationRulePage_searchDstPort_posXpath,
        "policyRulePage_selectDstPort_posXpath": manipulationRulePage_selectDstPort_posXpath,
        "policyRulePage_closeDstPort_posXpath": manipulationRulePage_closeDstPort_posXpath,
        # external Port
        "policyRulePage_addConditionExternalPort_posXpath": manipulationRulePage_addCondition_externalPort_posXpath,
        "policyRulePage_addExternalPort_posXpath": manipulationRulePage_addExternalPort_posXpath,
        "policyRulePage_searchExternalPort_posXpath": manipulationRulePage_searchExternalPort_posXpath,
        "policyRulePage_selectExternalPort_posXpath": manipulationRulePage_selectExternalPort_posXpath,
        "policyRulePage_closeExternalPort_posXpath": manipulationRulePage_closeExternalPort_posXpath,
        # External IP
        "policyRulePage_addConditionExternalIP_posXpath": manipulationRulePage_addCondition_externalIP_posXpath,
        "policyRulePage_addExternalIP_posXpath": manipulationRulePage_addExternalIP_posXpath,
        "policyRulePage_searchExternalIP_posXpath": manipulationRulePage_searchExternalIP_posXpath,
        "policyRulePage_selectExternalIP_posXpath": manipulationRulePage_selectExternalIP_posXpath,
        "policyRulePage_closeExternalIP_posXpath": manipulationRulePage_closeExternalIP_posXpath,
        # subid
        "policyRulePage_addConditionUser_posXpath": manipulationRulePage_addCondition_user_posXpath,
        "policyRulePage_addUser_posXpath": manipulationRulePage_addUser_posXpath,
        "policyRulePage_searchUser_posXpath": manipulationRulePage_searchUser_posXpath,
        "policyRulePage_selectUser_posXpath": manipulationRulePage_selectUser_posXpath,
        "policyRulePage_closeUser_posXpath": manipulationRulePage_closeUser_posXpath,
        # Device imsi imei phone number
        "policyRulePage_addConditionImsi_posXpath": manipulationRulePage_addCondition_imsi_posXpath,
        "policyRulePage_addImsi_posXpath": manipulationRulePage_addImsi_posXpath,
        "policyRulePage_searchImsi_posXpath": manipulationRulePage_searchImsi_posXpath,
        "policyRulePage_selectImsi_posXpath": manipulationRulePage_selectImsi_posXpath,
        "policyRulePage_closeImsi_posXpath": manipulationRulePage_closeImsi_posXpath,
        "policyRulePage_chooseImei_posXpath": policyRulePage_chooseImei_posXpath,
        "policyRulePage_choosePhoneNumber_posXpath": policyRulePage_choosePhoneNumber_posXpath,
        "policyRulePage_chooseApn_posXpath": policyRulePage_chooseApn_posXpath,
        # Application
        "policyRulePage_addApplication_posXpath": manipulationRulePage_addApplication_posXpath,
        "policyRulePage_searchDoHApplication_posXpath": manipulationRulePage_searchDoHApplication_posXpath,
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
        # Qname
        "policyRulePage_addConditionQname_posXpath": manipulationRulePage_addCondition_qname_posXpath,
        "policyRulePage_addQname_posXpath": manipulationRulePage_addServerQname_posXpath,
        "policyRulePage_searchQname_posXpath": manipulationRulePage_searchQname_posXpath,
        "policyRulePage_selectQname_posXpath": manipulationRulePage_selectQname_posXpath,
        "policyRulePage_closeQname_posXpath": manipulationRulePage_closeServerQname_posXpath,
        # url
        "policyRulePage_addConditionUrl_posXpath": manipulationRulePage_addCondition_url_posXpath,
        "policyRulePage_addUrl_posXpath": manipulationRulePage_addUrl_posXpath,
        "policyRulePage_searchUrl_posXpath": manipulationRulePage_searchUrl_posXpath,
        "policyRulePage_selectUrl_posXpath": manipulationRulePage_selectUrl_posXpath,
        "policyRulePage_closeUrl_posXpath": manipulationRulePage_closeUrl_posXpath,
        # request header
        "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
        "policyRulePage_addRequestHeader_posXpath": manipulationRulePage_addRequestHeader_posXpath,
        "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
        # response header
        "policyRulePage_addConditionResponseHeader_posXpath": securityRulePage_addCondition_responseHeader_posXpath,
        "policyRulePage_addResponseHeader_posXpath": manipulationRulePage_addResponseHeader_posXpath,
        "policyRulePage_searchResponseHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectResponseHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeResponseHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
        # request body
        "policyRulePage_addConditionRequestBody_posXpath": securityRulePage_addCondition_requestBody_posXpath,
        "policyRulePage_addRequestBody_posXpath": manipulationRulePage_addRequestBody_posXpath,
        "policyRulePage_searchRequestBody_posXpath": securityRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectRequestBody_posXpath": securityRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeRequestBody_posXpath": securityRulePage_closeRequestHeader_posXpath,
        # response body
        "policyRulePage_addConditionResponseBody_posXpath": securityRulePage_addCondition_responseBody_posXpath,
        "policyRulePage_addResponseBody_posXpath": manipulationRulePage_addResponseBody_posXpath,
        "policyRulePage_searchResponseBody_posXpath": securityRulePage_searchRequestHeader_posXpath,
        "policyRulePage_selectResponseBody_posXpath": securityRulePage_selectRequestHeader_posXpath,
        "policyRulePage_closeResponseBody_posXpath": securityRulePage_closeRequestHeader_posXpath,
        # deny action parameter
        "policyRulePage_deny_addResponseCodeSelectBox_posXpath":manipulationRulePage_deny_addResponseCodeSelectBox_posXpath,
        "policyRulePage_deny_addResponseCodeSelectDropItem_posXpath":manipulationRulePage_deny_addResponseCodeSelectDropItem_posXpath,
        "policyRulePage_deny_addResponseContentSelectBox_posXpath": manipulationRulePage_deny_addResponseContentSelectBox_posXpath,
        "policyRulePage_deny_addResponseContentSelectDropItem_posXpath": manipulationRulePage_deny_addResponseContentSelectDropItem_posXpath,
        "policyRulePage_deny_addResponseContentTextInput_posXpath": manipulationRulePage_deny_addResponseContentTextInput_posXpath,
        "policyRulePage_deny_addResponseContentProfileSelectBox_posXpath": manipulationRulePage_deny_addResponseContentProfileSelectBox_posXpath,
        "policyRulePage_deny_searchResponseProfile_posXpath": manipulationRulePage_deny_searchResponseProfile_posXpath,
        "policyRulePage_deny_searchResponseProfileDorpItem_posXpath": manipulationRulePage_deny_searchResponseProfileDorpItem_posXpath,
        # redirect http doh action parameter
        "policyRulePage_redirectHttp_addResponseCodeSelectBox_posXpath": manipulationRulePage_redirectHttp_addResponseCodeSelectBox_posXpath,
        "policyRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath": manipulationRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath,
        "policyRulePage_redirectHttp_redirectHttp_addRedirectUrlInput_posXpath": manipulationRulePage_redirectHttp_addRedirectUrlInput_posXpath,
        "policyRulePage_redirectDoH_qtypeRadio_posXpath": manipulationRulePage_redirectDoH_qtypeRadio_posXpath,
        "policyRulePage_redirectDoH_atypeSelectBox_posXpath": manipulationRulePage_redirectDoH_atypeSelectBox_posXpath,
        "policyRulePage_redirectDoH_atypeSelectDropItem_posXpath": manipulationRulePage_redirectDoH_atypeSelectDropItem_posXpath,
        "policyRulePage_redirectDoH_valueInput_posXpath": manipulationRulePage_redirectDoH_valueInput_posXpath,
        "policyRulePage_redirectDoH_ttlInput_posXpath": manipulationRulePage_redirectDoH_ttlInput_posXpath,
        "policyRulePage_redirectDoH_add_posXpath": manipulationRulePage_redirectDoH_add_posXpath,
        # replace action parameter
        "policyRulePage_subActionButton_replaceText_posXpath": manipulationRulePage_subActionButton_replaceText_posXpath,
        "policyRulePage_replace_addRegex_posXpath": manipulationRulePage_replace_addRegex_posXpath,
        "policyRulePage_replace_addSearchInSelectBox_posXpath": manipulationRulePage_replace_addSearchInSelectBox_posXpath,
        "policyRulePage_replace_addSearchInSelectDropItem_posXpath": manipulationRulePage_replace_addSearchInSelectDropItem_posXpath,
        "policyRulePage_replace_addFindInput_posXpath": manipulationRulePage_replace_addFindInput_posXpath,
        "policyRulePage_replace_addReplaceWithInput_posXpath": manipulationRulePage_replace_addReplaceWithInput_posXpath,
        "policyRulePage_replace_add_posXpath": manipulationRulePage_replace_add_posXpath,
        # hijack profile action parameter
        "policyRulePage_hijack_addHijackProfileSelectBox_posXpath": manipulationRulePage_hijack_addHijackProfileSelectBox_posXpath,
        "policyRulePage_hijack_searchHijackProfile_posXpath": manipulationRulePage_hijack_searchHijackProfile_posXpath,
        "policyRulePage_hijack_searchHijackProfileDorpItem_posXpath": manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath,
        # insert script action parameter
        "policyRulePage_insert_addInsertProfileSelectBox_posXpath": manipulationRulePage_insert_addInsertProfileSelectBox_posXpath,
        "policyRulePage_insert_searchInsertProfile_posXpath": manipulationRulePage_insert_searchInsertProfile_posXpath,
        "policyRulePage_insert_searchInsertProfileDorpItem_posXpath": manipulationRulePage_insert_searchInsertProfileDorpItem_posXpath,
        # edit element action parameter
        "policyRulePage_subActionButton_editElement_posXpath": manipulationRulePage_subActionButton_editElement_posXpath,
        "policyRulePage_editElement_addSearchScopeWholeFileRadio_posXpath": manipulationRulePage_editElement_addSearchScopeWholeFileRadio_posXpath,
        "policyRulePage_editElement_addSearchScopeInsideElementRadio_posXpath": manipulationRulePage_editElement_addSearchScopeInsideElementRadio_posXpath,
        "policyRulePage_editElement_addContainedKeywordInput_posXpath": manipulationRulePage_editElement_addContainedKeywordInput_posXpath,
        "policyRulePage_editElement_addStartIndicatorInput_posXpath": manipulationRulePage_editElement_addStartIndicatorInput_posXpath,
        "policyRulePage_editElement_addSDistanceFromAnchorInput_posXpath": manipulationRulePage_editElement_addSDistanceFromAnchorInput_posXpath,
        "policyRulePage_editElement_addMarkRadio_posXpath": manipulationRulePage_editElement_addMarkRadio_posXpath,
        "policyRulePage_editElement_addRemoveRadio_posXpath": manipulationRulePage_editElement_addRemoveRadio_posXpath,
        "policyRulePage_editElement_add_posXpath": manipulationRulePage_editElement_add_posXpath,
        # insert script action parameter
        "policyRulePage_runScript_addrunScriptProfileSelectBox_posXpath": manipulationRulePage_insert_addrunScriptProfileSelectBox_posXpath,
        "policyRulePage_runScript_searchrunScriptProfile_posXpath": manipulationRulePage_insert_searchrunScriptProfile_posXpath,
        "policyRulePage_runScript_searchrunScriptProfileDorpItem_posXpath": manipulationRulePage_insert_searchrunScriptProfileDorpItem_posXpath,
        # other options
        "policyRulePage_logOptions_all_posXpath": manipulationRulePage_logOptions_all_posXpath,
        # effective devices
        "policyRulePage_addEffectiveDevices_posXpath": manipulationRulePage_addEffectiveDevices_posXpath,
        "policyRulePage_selectEffectiveDevices_posXpath": manipulationRulePage_selectEffectiveDevices_posXpath,
        "policyRulePage_closeEffectiveDevices_posXpath": manipulationRulePage_closeEffectiveDevices_posXpath,
        # 保存策略时，ok cancel warnging定位
        "policyRulePage_enable_posXpath": manipulationRulePage_enable_posXpath,
        "policyRulePage_okButton_posXpath": manipulationRulePage_okButton_posXpath,
        "policyRulePage_okButton_warningYes_posXpath": manipulationRulePage_okButton_warningYes_posXpath,
    },
    "search": {
        "policyRuleListPage_searchLabel_posXpath": manipulationRuleListpage_searchLabel_posXpath,
        "policyRuleListPage_searchLabel_dropDown_item_posXpath": ruleListPage_searchLabel_dropDown_item_posXpath, #manipulationRuleListpage_searchLabel_dropDown_item_posXpath,
        "policyRuleListPage_searchLabel_input_itemContent_posXpath": manipulationRuleListpage_searchLabel_input_itemContent_posXpath,
        "policyRuleListPage_searchLabel_searchButton_posId": manipulationRuleListpage_searchLabel_searchButton_posXpath,
        "policyRuleListPage_tableTbody_posXpath": manipulationRuleListpage_tableTbody_posXpath
    },
    "delete": {
        "policyRuleListPage_allSelect_posXpath": manipulationRuleListpage_allSelect_posXpath,
        "policyRuleListPage_deleteButton_posXpath": manipulationRuleListpage_deleteButton_posXpath,
        "policyRuleListPage_okButton_warningYes_posXpath": manipulationRuleListpage_deleteTipButton_warningYes_posXpath,
        "policyRuleListPage_okButton_warningNo_posXpath": manipulationRuleListpage_deleteTipButton_warningNo_posXpath
    }
}
policy_service_chaining_rule_element_position = {
    "page_jump":{
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_policyFirstLevelMenu_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_policySecondLevelMenu_servicechaining_posXpath
    },
    "create": {
        "policyRuleListPage_createButton_posXpath":serviceChainingRuleListPage_createButton_posXpath,
        "policyRulePage_inputName_posXpath": serviceChainingRulePage_inputName_posXpath,
        # Target Traffic
        "policyRulePage_rawTraffic_posXpath": serviceChainingRulePage_rawTrafficButton_posXpath,
        "policyRulePage_decryptedTraffic_posXpath": serviceChainingRulePage_decryptedTrafficButton_posXpath,
        "policyRulePage_addCondition_posXpath": policyRulePage_addCondition_posXpath,
        "policyRulePage_addCondition_close_posXpath": policyRulePage_addCondition_close_posXpath,
        "policyRulePage_negateSrcIP_posXpath":serviceChainingRulePage_negateSrcIP_posXpath,
        "policyRulePage_negateDstIP_posXpath":serviceChainingRulePage_negateDstIP_posXpath,
        "policyRulePage_negateUser_posXpath":serviceChainingRulePage_negateUser_posXpath,
        "policyRulePage_negateImsi_posXpath":serviceChainingRulePage_negateImsi_posXpath,
        "policyRulePage_negateSrcPort_posXpath":serviceChainingRulePage_negateSrcPort_posXpath,
        "policyRulePage_negateDstPort_posXpath":serviceChainingRulePage_negateDstPort_posXpath,
        "policyRulePage_negateServerFqdn_posXpath":serviceChainingRulePage_negateServerFqdn_posXpath,
        "policyRulePage_negateInternalPort_posXpath":serviceChainingRulePage_negateInternalPort_posXpath,
        "policyRulePage_negateExternalPort_posXpath":serviceChainingRulePage_negateExternalPort_posXpath,
        # Source IP
        "policyRulePage_addSrcIP_posXpath": serviceChainingRulePage_addSrcIP_posXpath,
        "policyRulePage_searchSrcIP_posXpath": serviceChainingRulePage_searchSrcIP_posXpath,
        "policyRulePage_selectSrcIP_posXpath": serviceChainingRulePage_selectSrcIP_posXpath,
        "policyRulePage_closeSrcIP_posXpath": serviceChainingRulePage_closeSrcIP_posXpath,
        # User
        "policyRulePage_addConditionUser_posXpath": serviceChainingRulePage_addCondition_user_posXpath,
        "policyRulePage_addUser_posXpath": serviceChainingRulePage_addUser_posXpath,
        "policyRulePage_searchUser_posXpath": serviceChainingRulePage_searchUser_posXpath,
        "policyRulePage_selectUser_posXpath": serviceChainingRulePage_selectUser_posXpath,
        "policyRulePage_closeUser_posXpath": serviceChainingRulePage_closeUser_posXpath,
        # Device imsi imei phone number
        "policyRulePage_addConditionImsi_posXpath": serviceChainingRulePage_addCondition_imsi_posXpath,
        "policyRulePage_addImsi_posXpath": manipulationRulePage_addImsi_posXpath,
        "policyRulePage_searchImsi_posXpath": manipulationRulePage_searchImsi_posXpath,
        "policyRulePage_selectImsi_posXpath": manipulationRulePage_selectImsi_posXpath,
        "policyRulePage_closeImsi_posXpath": manipulationRulePage_closeImsi_posXpath,
        "policyRulePage_chooseImei_posXpath": policyRulePage_chooseImei_posXpath,
        "policyRulePage_choosePhoneNumber_posXpath": policyRulePage_choosePhoneNumber_posXpath,
        "policyRulePage_chooseApn_posXpath": policyRulePage_chooseApn_posXpath,
        # Dest IP
        "policyRulePage_addDstIP_posXpath": serviceChainingRulePage_addDstIP_posXpath,
        "policyRulePage_searchDstIP_posXpath": serviceChainingRulePage_searchDstIP_posXpath,
        "policyRulePage_selectDstIP_posXpath": serviceChainingRulePage_selectDstIP_posXpath,
        "policyRulePage_closeDstIP_posXpath": serviceChainingRulePage_closeDstIP_posXpath,
        # Server FQDN
        "policyRulePage_addConditionServerFqdn_posXpath": serviceChainingRulePage_addCondition_serverFqdn_posXpath,
        "policyRulePage_addServerFqdn_posXpath": serviceChainingRulePage_addServerFqdn_posXpath,
        "policyRulePage_searchServerFqdn_posXpath": serviceChainingRulePage_searchServerFqdn_posXpath,
        "policyRulePage_selectServerFqdn_posXpath": serviceChainingRulePage_selectServerFqdn_posXpath,
        "policyRulePage_closeServerFqdn_posXpath": serviceChainingRulePage_closeServerFqdn_posXpath,
        # Source Port
        "policyRulePage_addConditionSrcPort_posXpath": policyRulePage_addCondition_srcPort_posXpath,
        "policyRulePage_addSrcPort_posXpath": policyRulePage_addSrcPort_posXpath,
        "policyRulePage_searchSrcPort_posXpath": policyRulePage_searchSrcPort_posXpath,
        "policyRulePage_selectSrcPort_posXpath": policyRulePage_selectSrcPort_posXpath,
        "policyRulePage_closeSrcPort_posXpath": policyRulePage_closeSrcPort_posXpath,
        # Internal Port
        "policyRulePage_addConditionInternalPort_posXpath": policyRulePage_addCondition_internalPort_posXpath,
        "policyRulePage_addInternalPort_posXpath": policyRulePage_addInternalPort_posXpath,
        "policyRulePage_searchInternalPort_posXpath": policyRulePage_searchInternalPort_posXpath,
        "policyRulePage_selectInternalPort_posXpath": policyRulePage_selectInternalPort_posXpath,
        "policyRulePage_closeInternalPort_posXpath": policyRulePage_closeInternalPort_posXpath,
        # Destination Port
        "policyRulePage_addConditionDstPort_posXpath": policyRulePage_addCondition_dstPort_posXpath,
        "policyRulePage_addDstPort_posXpath": policyRulePage_addDstPort_posXpath,
        "policyRulePage_searchDstPort_posXpath": policyRulePage_searchDstPort_posXpath,
        "policyRulePage_selectDstPort_posXpath": policyRulePage_selectDstPort_posXpath,
        "policyRulePage_closeDstPort_posXpath": policyRulePage_closeDstPort_posXpath,
        # External Port
        "policyRulePage_addConditionExternalPort_posXpath": policyRulePage_addCondition_externalPort_posXpath,
        "policyRulePage_addExternalPort_posXpath": policyRulePage_addExternalPort_posXpath,
        "policyRulePage_searchExternalPort_posXpath": policyRulePage_searchExternalPort_posXpath,
        "policyRulePage_selectExternalPort_posXpath": policyRulePage_selectExternalPort_posXpath,
        "policyRulePage_closeExternalPort_posXpath": policyRulePage_closeExternalPort_posXpath,
        # Application
        "policyRulePage_addApplication_posXpath": serviceChainingRulePage_addApplication_posXpath,
        "policyRulePage_selectApplicationLabel_posXpath":serviceChainingRulePage_selectApplicationLabel_posXpath,
        "policyRulePage_searchApplication_posXpath": serviceChainingRulePage_searchApplication_posXpath,
        "policyRulePage_selectApplication_posXpath": serviceChainingRulePage_selectApplication_posXpath,
        "policyRulePage_closeApplication_posXpath": serviceChainingRulePage_closeApplication_posXpath,
        #Qname
        "policyRulePage_addConditionQname_posXpath": serviceChainingRulePage_addConditionQname_posXpath,
        "policyRulePage_addQname_posXpath": policyRulePage_addQname_posXpath,
        "policyRulePage_searchQname_posXpath": policyRulePage_searchQname_posXpath,
        "policyRulePage_selectQname_posXpath": policyRulePage_selectQname_posXpath,
        "policyRulePage_closeQname_posXpath": policyRulePage_closeQname_posXpath,
        # IP Protocol
        "policyRulePage_addConditionIpProtocol_posXpath": policyRulePage_addCondition_IpProtocol_posXpath,
        "policyRulePage_addIpProtocol_posXpath": policyRulePage_addIpProtocol_posXpath,
        "policyRulePage_searchIpProtocol_posXpath": policyRulePage_searchIpProtocol_posXpath,
        "policyRulePage_selectIpProtocol_posXpath": policyRulePage_selectIpProtocol_posXpath,
        "policyRulePage_closeIpProtocol_posXpath": policyRulePage_closeIpProtocol_posXpath,
        # add ssl boolean type
        "policyRulePage_addConditionBoolean_posXpath": policyRulePage_addCondition_Boolean_posXpath,
        "policyRulePage_addBoolean_posXpath": policyRulePage_addBoolean_posXpath,
        "policyRulePage_searchBoolean_posXpath": policyRulePage_searchBoolean_posXpath,
        "policyRulePage_selectBoolean_posXpath": policyRulePage_selectBoolean_posXpath,
        "policyRulePage_closeBoolean_posXpath": policyRulePage_closeBoolean_posXpath,
        "policyRulePage_little_button_addBoolean_posXpath":policyRulePage_little_button_addBoolean_posXpath,
        # URL
        "policyRulePage_addConditionUrl_posXpath": serviceChainingRulePage_addCondition_url_posXpath,
        "policyRulePage_addUrl_posXpath": policyRulePage_addUrl_posXpath,
        "policyRulePage_searchUrl_posXpath": policyRulePage_searchUrl_posXpath,
        "policyRulePage_selectUrl_posXpath": policyRulePage_selectUrl_posXpath,
        "policyRulePage_closeUrl_posXpath": policyRulePage_closeUrl_posXpath,
        # 添加account
        "policyRulePage_addConditionFtpAccount_posXpath": policyRulePage_addCondition_ftpAccount_posXpath,
        "policyRulePage_addFtpAccount_posXpath": policyRulePage_addFtpAccount_posXpath,
        "policyRulePage_searchFtpAccount_posXpath": policyRulePage_searchFtpAccount_posXpath,
        "policyRulePage_selectFtpAccount_posXpath": policyRulePage_selectFtpAccount_posXpath,
        "policyRulePage_closeFtpAccount_posXpath": policyRulePage_closeFtpAccount_posXpath,
         # 添加mail account
        "policyRulePage_addConditionMailAccount_posXpath": policyRulePage_addCondition_mailAccount_posXpath,
        "policyRulePage_addMailAccount_posXpath": policyRulePage_addMailAccount_posXpath,
        "policyRulePage_searchMailAccount_posXpath": policyRulePage_searchMailAccount_posXpath,
        "policyRulePage_selectMailAccount_posXpath": policyRulePage_selectMailAccount_posXpath,
        "policyRulePage_closeMailAccount_posXpath": policyRulePage_closeMailAccount_posXpath,
        #添加mail from
        "policyRulePage_addConditionMailFrom_posXpath": policyRulePage_addCondition_mailFrom_posXpath,
        "policyRulePage_addMailFrom_posXpath": policyRulePage_addMailFrom_posXpath,
        "policyRulePage_searchMailFrom_posXpath": policyRulePage_searchMailFrom_posXpath,
        "policyRulePage_selectMailFrom_posXpath": policyRulePage_selectMailFrom_posXpath,
        "policyRulePage_closeMailFrom_posXpath": policyRulePage_closeMailFrom_posXpath,
        #添加mail to
        "policyRulePage_addConditionMailTo_posXpath": policyRulePage_addCondition_mailTo_posXpath,
        "policyRulePage_addMailTo_posXpath":policyRulePage_addMailTo_posXpath,
        "policyRulePage_searchMailTo_posXpath": policyRulePage_searchMailTo_posXpath,
        "policyRulePage_selectMailTo_posXpath": policyRulePage_selectMailTo_posXpath,
        "policyRulePage_closeMailTo_posXpath": policyRulePage_closeMailTo_posXpath,
        # SFF Profile
        "policyRulePage_addSFFProfile_posXpath": serviceChainingRulePage_addSFFProfile_posXpath,
        "policyRulePage_searchSFFProfile_posXpath":serviceChainingRulePage_searchSFFProfile_posXpath,
        "policyRulePage_selectSFFProfile_posXpath":serviceChainingRulePage_selectSFFProfile_posXpath,
        "policyRulePage_closeSFFProfile_posXpath":serviceChainingRulePage_closeSFFProfile_posXpath,
        "policyRulePage_enable_posXpath": serviceChainingRulePage_enable_posXpath,
        "policyRulePage_okButton_posXpath": serviceChainingRulePage_okButton_posXpach,
        "policyRulePage_okButton_warningYes_posXpath": serviceChainingRulePage_warningYes_posXpath
    },
    "search": {
        "policyRuleListPage_searchLabel_posXpath": serviceChainingRuleListPage_searchLable_posXpath,
        "policyRuleListPage_searchLabel_dropDown_item_posXpath": ruleListPage_searchLabel_dropDown_item_posXpath, #serviceChainingRuleListPage_searchLable_dropDown_item_posXpath,
        "policyRuleListPage_searchLabel_input_itemContent_posXpath": serviceChainingRuleListPage_searchLable_input_itemContent_posXpath,
        "policyRuleListPage_searchLabel_searchButton_posId": serviceChainingRuleListPage_searchLable_searchButton_posXpath,
        "policyRuleListPage_tableTbody_posXpath": serviceChainingRuleListPage_tableTbody_posXpath
    },
    "delete": {
        "policyRuleListPage_allSelect_posXpath": securityRulelistPage_allSelect_posXpath,
        "policyRuleListPage_deleteButton_posXpath": serviceChainingRuleListPage_deleteButton_posXpath,
        "policyRuleListPage_okButton_warningYes_posXpath": serviceChainingRuleListPage_warningYes_posXpath
    }
}

# object
object_ip_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_ipAddress_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": ipObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": ipObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": ipObjectPage_inputName_posXpath,
        "objectPage_ipType_posXpath": ipObjectPage_ipType_posXpath,
        "objectPage_addItem_posXpath": ipObjectPage_addItem_posXpath,
        "objectPage_inputItem_posXpath": ipObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": ipObjectPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": ipObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": ipObjectPage_okButton_warningYes_posXpath,
        "objectPage_statistics_select_posXpath": ObjectPage_statistics_select_posXpath,
        "objectPage_statistics_select_option_posXpath": ObjectPage_statistics_select_option_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posXpath": ipObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": ipObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": ipObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": ipObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": ipObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": ipObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posXpath": ipObjectListPage_deleteButton_posXpath,
        "objectListPage_deleteButton_warningYes_posXpath": ipObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_ip_group_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_ipAddress_posXpath
    },
    "create": {
        "objectListPage_createButton_posId": ipObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createGroupButton_posId": ipObjectListPage_dropDown_createGroupButton_posId,
        "objectPage_inputName_posXpath": ipObjectPage_inputName_posXpath,
        "objectPage_ipType_posXpath": ipObjectPage_ipType_posXpath,
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
        "objectPage_okButton_posId": ipObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": ipObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posId": ipObjectListPage_searchLabel_posId,
        "objectListPage_searchLabel_selectName_posXpath": ipObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": ipObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": ipObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": ipObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": ipObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posXpath": ipObjectListPage_deleteButton_posXpath,
        "objectListPage_deleteButton_warningYes_posXpath": ipObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_port_object_element_position = {
    "page_jump":{
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_port_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": portObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": portObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": portObjectPage_inputName_posXpath,
        "objectPage_addItem_posXpath": portObjectPage_addItem_posXpath,
        "objectPage_inputItem_posXpath": portObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": portObjectPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": portObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": portObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posXpath": portObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": portObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": portObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": portObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": portObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": portObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": portObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posXpath": portObjectListPage_deleteButton_posXpath,
        "objectListPage_deleteButton_warningYes_posXpath": portObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_fqdn_object_element_position = {
    "page_jump":{
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_fqdn_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": fqdnObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": fqdnObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": fqdnObjectPage_inputName_posXpath,
        "objectPage_addItem_posXpath": fqdnobjectPage_addItem_posXpath,
        "objectPage_inputItem_posXpath": fqdnObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": fqdnObjectPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": fqdnObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": fqdnObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posXpath": fqdnObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": fqdnObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": fqdnObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": fqdnObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": fqdnObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": fqdnObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": fqdnObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posXpath": fqdnObjectListPage_deleteButton_posXpath,
        "objectListPage_deleteButton_warningYes_posXpath": fqdnObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_subscriberid_object_element_position = {
    "page_jump":{
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_subid_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": subscriberidObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": subscriberidObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": subscriberidObjectPage_inputName_posXpath,
        "objectPage_addItem_posXpath": subscriberidobjectPage_addItem_posXpath,
        "objectPage_inputItem_posXpath": subscriberidObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": subscriberidPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": subscriberidObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": subscriberidObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posXpath": subscriberidObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": subscriberidObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": subscriberidObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": subscriberidObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": subscriberidObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": subscriberidObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": subscriberidObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posXpath": subscriberidObjectListPage_deleteButton_posXpath,
        "objectListPage_deleteButton_warningYes_posXpath": subscriberiObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_keywords_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_keywords_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": keywordsObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": keywordsObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": keywordsObjectPage_inputName_posXpath,
        "objectPage_addItem_posXpath": keywordsobjectPage_addItem_posXpath,
        "objectPage_item_value_select_posXpath": keywordsObjectPage_item_value_select_posXpath,
        "objectPage_inputItem_posXpath": keywordsObjectPage_inputItem_posXpath,
        "objectPage_item_value_plus_posXpath": keywordsObjectPage_item_value_plus_posXpath,
        "objectPage_button_saveItem_posXpath": keywordsObjectPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": keywordsObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": keywordsObjectPage_okButton_warningYes_posXpath,
        "ObjectPage_sameItem_addItem_posXpath": urlObjectPage_sameItem_addItem_posXpath,
    },
    "search": {
        "objectListPage_searchLabel_posXpath": keywordsObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": keywordsObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": keywordsObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": keywordsObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": keywordsObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": keywordsObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": keywordsObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posId": keywordsObjectListPage_deleteButton_posId,
        "objectListPage_deleteButton_warningYes_posXpath": keywordsObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_http_url_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_url_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": urlObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": urlObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": urlObjectPage_inputName_posXpath,
        "objectPage_addItem_posXpath": urlObjectPage_addItem_posXpath,
        # item简单定位objectPage_okButton_posXpath
        "objectPage_inputItem_posXpath": urlObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": urlObjectPage_saveItem_posXpath,
        "objectPage_okButton_posXpath": urlObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": urlObjectPage_okButton_warningYes_posXpath,
        "ObjectPage_sameItem_addItem_posXpath":urlObjectPage_sameItem_addItem_posXpath,
        "ObjectPage_sameItem_inputItem_posXpath": urlObjectPage_sameItem_inputItem_posXpath,
    },
    "search": {
        "objectListPage_searchLabel_posXpath": urlObjectPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": urlObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": urlObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": urlObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": urlObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": urlObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": urlObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posXpath": urlObjectListPage_deleteButton_posXpath,
        "objectListPage_deleteButton_warningYes_posXpath": urlObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_account_object_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
                    "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_account_posXpath
                },
                "create": {
                    "objectListPage_createButton_posXpath": accountObjectListPage_createButton_posXpath,
                    "objectListPage_dropDown_createButton_posXpath": accountObjectListPage_dropDown_createButton_posXpath,
                    "objectPage_inputName_posXpath": accountObjectPage_inputName_posXpath,
                    "objectPage_addItem_posXpath": accountobjectPage_addItem_posXpath,
                    # item简单定位
                    "objectPage_inputItem_posXpath": accountObjectPage_inputItem_posXpath,
                    "objectPage_button_saveItem_posXpath": accountObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posXpath": accountObjectPage_okButton_posXpath,
                    "objectPage_okButton_warningYes_posXpath": accountObjectPage_okButton_warningYes_posXpath,
                    "ObjectPage_sameItem_addItem_posXpath": urlObjectPage_sameItem_addItem_posXpath,
                    "ObjectPage_sameItem_inputItem_posXpath": urlObjectPage_sameItem_inputItem_posXpath,
                },
                "search": {
                    "objectListPage_searchLabel_posXpath": accountObjectPage_searchLabel_posXpath,
                    "objectListPage_searchLabel_selectName_posXpath": accountObjectListPage_searchLabel_selectName_posXpath,
                    "objectListPage_tableTbody_posXpath": accountObjectListPage_tableTbody_posXpath,
                    "objectListPage_search_input_posXpath": accountObjectListPage_search_input_posXpath,
                    "objectListPage_search_dropDown_item_posXpath": accountObjectListPage_search_dropDown_item_posXpath,
                    "objectListPage_search_button_posXpath": accountObjectListPage_search_button_posXpath
                },
                "delete": {
                    "objectListPage_allSelect_posXpath": accountObjectListPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posXpath": accountObjectListPage_deleteButton_posXpath,
                    "objectListPage_deleteButton_warningYes_posXpath": accountObjectListPage_deleteButton_warningYes_posXpath
                }
            }
object_imsi_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_mobileIdentify_posXpath
    },
    "create": {
        "objectListPage_createButton_posId": mobile_identitiesObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": mobile_identitiesObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": mobile_identitiesObjectPage_inputName_posXpath,
        "objectPage_imsiType_posXpath": imsiObjectPage_imsiType_posXpath,
        "objectPage_addItem_posXpath": imsiobjectPage_addItem_posXpath,
        "objectPage_inputItem_posXpath": imsiObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": imsiObjectPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": imsiObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": imsiObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posXpath": imsiObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": imsiObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": imsiObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posId": imsiObjectListPage_deleteButton_posId,
        "objectListPage_deleteButton_warningYes_posXpath": imsiObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_phone_number_object_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
                    "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_mobileIdentify_posXpath
                },
                "create": {
                    "objectListPage_createButton_posId": mobile_identitiesObjectListPage_createButton_posXpath,
                    "objectListPage_dropDown_createButton_posXpath": mobile_identitiesObjectListPage_dropDown_createButton_posXpath,
                    "objectPage_inputName_posXpath": mobile_identitiesObjectPage_inputName_posXpath,
                    "objectPage_phnoeNumberType_posXpath": phoneNumberObjectPage_phoneNumberType_posXpath,
                    "objectPage_addItem_posXpath": phoneNumberobjectPage_addItem_posXpath,
                    "objectPage_inputItem_posXpath": phoneNumberObjectPage_inputItem_posXpath,
                    "objectPage_button_saveItem_posXpath": phoneNumberObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posId": phoneNumberObjectPage_okButton_posId,
                    "objectPage_okButton_warningYes_posXpath": phoneNumberObjectPage_okButton_warningYes_posXpath
                },
                "search": {
                    "objectListPage_searchLabel_posXpath": imsiObjectListPage_searchLabel_posXpath,
                    "objectListPage_searchLabel_selectName_posXpath": imsiObjectListPage_searchLabel_selectName_posXpath,
                    "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
                },
                "delete": {
                    "objectListPage_allSelect_posXpath": imsiObjectListPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posId": imsiObjectListPage_deleteButton_posId,
                    "objectListPage_deleteButton_warningYes_posXpath": imsiObjectListPage_deleteButton_warningYes_posXpath
                }
            }
object_mobile_identity_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_mobileIdentify_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": mobile_identitiesObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": mobile_identitiesObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": mobile_identitiesObjectPage_inputName_posXpath,
        "objectPage_imsiType_posXpath": imsiObjectPage_imsiType_posXpath,
        "objectPage_imeiType_posXpath": imeiObjectPage_imsiType_posXpath,
        "objectPage_phnoeNumberType_posXpath": phoneNumberObjectPage_phoneNumberType_posXpath,
        "objectPage_addItem_posXpath": imsiobjectPage_addItem_posXpath,
        "objectPage_inputItem_posXpath": imsiObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": imsiObjectPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": imsiObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": imsiObjectPage_okButton_warningYes_posXpath

    },
    "search": {
        "objectListPage_searchLabel_posXpath": imsiObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": imsiObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": imsiObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": imsiObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": imsiObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": imsiObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": imsiObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posId": imsiObjectListPage_deleteButton_posId,
        "objectListPage_deleteButton_warningYes_posXpath": imsiObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_apn_object_element_position = {
    "page_jump":{
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_apn_posXpath
    },
    "create": {
        "objectListPage_createButton_posXpath": apnObjectListPage_createButton_posXpath,
        "objectListPage_dropDown_createButton_posXpath": apnObjectListPage_dropDown_createButton_posXpath,
        "objectPage_inputName_posXpath": apnObjectPage_inputName_posXpath,
        "objectPage_addItem_posXpath": apnobjectPage_addItem_posXpath,
        "objectPage_inputItem_posXpath": apnObjectPage_inputItem_posXpath,
        "objectPage_button_saveItem_posXpath": apnPage_button_saveItem_posXpath,
        "objectPage_okButton_posXpath": apnObjectPage_okButton_posXpath,
        "objectPage_okButton_warningYes_posXpath": apnObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posXpath": apnObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": apnObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": apnObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": apnObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": apnObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": apnObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": apnObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posXpath": apnObjectListPage_deleteButton_posXpath,
        "objectListPage_deleteButton_warningYes_posXpath": apnObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_application_group_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_appliactionGroup_posId
    },
    "create": {
        "objectListPage_createButton_posId": applicationGroupobjectListPage_createButton_posId,
        "objectPage_inputName_posXpath": groupObjectPage_inputName_posXpath,
        "groupObjectPage_addSubordinate_posXpath": groupObjectPage_addSubordinate_posXpath,
        "groupObjectPage_searchSubordinateApplicationGroup_posXpath": groupObjectPage_searchSubordinate_posXpath,
        "groupObjectPage_selectSubordinateApplicationGroup_posXpath": groupObjectPage_selectSubordinate_posXpath,
        "groupObjectPage_closeSubordinateApplicationGroup_posXpath": groupObjectPage_closeSubordinate_posXpath,
        "groupObjectPage_addSubordinateObject_posId": groupObjectPage_addSubordinateObject_posId,
        "groupObjectPage_enableExclude_posXpath": groupObjectPage_enableExclude_posXpath,
        "groupObjectPage_addExclude_posXpath": groupObjectPage_addExclude_posXpath,
        "groupObjectPage_searchExcludeApplicationGroup_posXpath": groupObjectPage_searchExclude_posXpath,
        "groupObjectPage_selectExcludeApplicationGroup_posXpath": groupObjectPage_selectExclude_posXpath,
        "groupObjectPage_closeExcludeApplicationGroup_posXpath": groupObjectPage_closeSubordinate_posXpath,
        "groupObjectPage_addExcludeObject_posId": groupObjectPage_addExcludeObject_posId,
        "objectPage_okButton_posId": applicationGroupObjectPage_okButton_posId,
        "objectPage_okButton_warningYes_posXpath": appllicationGroupObjectPage_okButton_warningYes_posXpath
    },
    "search": {
        "objectListPage_searchLabel_posId": ObjectListPage_searchLabel_posId,
        "objectListPage_tableTbody_posXpath": ObjectListPage_tableTbody_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": ObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posId": applicationGroupObjectListPage_deleteButton_posId,
        "objectListPage_deleteButton_warningYes_posXpath": ObjectListPage_deleteButton_warningYes_posXpath
    }
}
object_flag_object_element_position = {
                "page_jump": {
                    "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
                    "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                    "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                    # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                    "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
                    "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_flag_posXpath
                },
                "create": {
                    "objectListPage_createButton_posXpath": flagObjectListPage_createButton_posXpath,
                    "objectListPage_dropDown_createButton_posXpath": flagObjectListPage_dropDown_createButton_posXpath,
                    "objectPage_inputName_posXpath": flagObjectPage_inputName_posXpath,
                    "objectPage_addItem_posXpath": flagObjectPage_addItem_posXpath,
                    # item简单定位
                    "objectPage_inputItem_posXpath": accountObjectPage_inputItem_posXpath,
                    "objectPage_button_saveItem_posXpath": accountObjectPage_button_saveItem_posXpath,
                    "objectPage_okButton_posXpath": accountObjectPage_okButton_posXpath,
                    "objectPage_okButton_warningYes_posXpath": accountObjectPage_okButton_warningYes_posXpath,
                    "ObjectPage_sameItem_addItem_posXpath": urlObjectPage_sameItem_addItem_posXpath,
                    "ObjectPage_sameItem_inputItem_posXpath": urlObjectPage_sameItem_inputItem_posXpath,
                },
                "search": {
                    "objectListPage_searchLabel_posXpath": accountObjectPage_searchLabel_posXpath,
                    "objectListPage_searchLabel_selectName_posXpath": '//*[@class="base-Popper-root MuiAutocomplete-listbox css-18r31z0"]//li[1]',
                    "objectListPage_tableTbody_posXpath": accountObjectListPage_tableTbody_posXpath,

                },
                "delete": {
                    "objectListPage_allSelect_posXpath": accountObjectListPage_allSelect_posXpath,
                    "objectListPage_deleteButton_posXpath": accountObjectListPage_deleteButton_posXpath,
                    "objectListPage_deleteButton_warningYes_posXpath": accountObjectListPage_deleteButton_warningYes_posXpath
                }
            }
object_http_signature_object_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_policyFirstLevelMenu_posXpath": mainPage_firstLevelMenu_Objects_posXpath,
        "mainPage_policySecondLevelMenu_posXpath": mainPage_secondLevelMenu_httpSignature_posId
    },
    "create": {
        "objectListPage_createButton_posId": httpSignatureObjectListPage_createButton_posId,
        "objectListPage_dropDown_createButton_posId": httpSignatureObjectListPage_dropDown_createButton_posId,
        "objectPage_inputName_posXpath": httpSignatureObjectPage_inputName_posXpath,
        "objectPage_addItem_posXpath": httpSignatureobjectPage_addItem_posXpath,
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
        "objectListPage_searchLabel_posId": httpSignatureObjectListPage_searchLabel_posXpath,
        "objectListPage_searchLabel_selectName_posXpath": httpSignatureObjectListPage_searchLabel_selectName_posXpath,
        "objectListPage_tableTbody_posXpath": httpSignatureObjectListPage_tableTbody_posXpath,
        "objectListPage_search_input_posXpath": httpSignatureObjectListPage_search_input_posXpath,
        "objectListPage_search_dropDown_item_posXpath": httpSignatureObjectListPage_search_dropDown_item_posXpath,
        "objectListPage_search_button_posXpath": httpSignatureObjectListPage_search_button_posXpath
    },
    "delete": {
        "objectListPage_allSelect_posXpath": httpSignatureObjectListPage_allSelect_posXpath,
        "objectListPage_deleteButton_posId": httpSignatureObjectListPage_deleteButton_posId,
        "objectListPage_deleteButton_warningYes_posXpath": httpSignatureObjectListPage_deleteButton_warningYes_posXpath
    }
}

# profile
profile_response_page_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_leftMenu_posXpath": mainPage_leftMenu_posXpath,
        "mainPage_profileFirstLevelMenu_Name": mainPage_firstLevelMenu_profiles_posName,
        "mainPage_profileSecondLevelMenu_Name": mainPage_secondLevelMenu_responsePages_Name,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posXpath": mainPage_secondLevelMenu_responsePages_posXpath
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_responsePages_createButton_posXpath,
        "profilePage_inputName_posXpath": responsePage_input_Name_posXpath,
        "profilePage_input_file_posXpath": responsePage_input_file_posXpath,
        "profilePage_okButton_posCss": responsePage_button_oK_posXpath,
        "profilePage_okButton_warningYes_posCss": responsePage_button_warningSaveYes_posXpath,
    },
    "search": {
        "profileListPage_searchLabel_posXpath": listPage_profileSearch_responsePages_selectLabel_posXpath,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_responsePages_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_responsePages_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_responsePages_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posXpath": listPage_profile_responsePages_delButton_posXpath,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_responsePages_button_yes_posXpath
    }
}
profile_traffic_mirroring_profile_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_trafficMirroringProfiles_posId
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_trafficMirroringProfiles_createButton_posXpath,
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
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_trafficMirroringProfiles_button_yes_posXpath
    }
}
profile_monitor_profile_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_trafficMirroringProfiles_posId,
        "mainPage_leftMenu_posXpath": mainPage_leftMenu_posXpath,
        "mainPage_profileFirstLevelMenu_Name": mainPage_firstLevelMenu_profiles_posName,
        "mainPage_profileSecondLevelMenu_Name": mainPage_secondLevelMenu_trafficTemplates_Name
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_trafficMirroringProfiles_createButton_posXpath,
        "profilePage_inputName_posXpath": trafficMirroringProfiles_input_Name_posXpath,
        "profilePage_addLANID_posXpath": trafficMirroringProfiles_button_vlanIdAdd_posXpath,
        "trafficMirroringProfiles_input_vlanIdsInput_posXpath": trafficMirroringProfiles_input_vlanIdsInput_posXpath,
        "profilePage_button_oK_posXpath": trafficMirroringProfiles_button_oK_posXpath,
        "profilePage_button_cancel_posCss": trafficMirroringProfiles_button_cancel_posCss,
        "profilePage_button_warningSaveYes_posCss": trafficMirroringProfiles_button_warningSaveYes_posCss,
        # action
    },
    "edit": {
        "templates_button_chartEdit_posXpath": listPage_profileHandleButton_posXpath.format(replaceName=listPage_profile_statisticsTemplates_editButton_name)
    },
    "search": {
        "profileListPage_searchLabel_posXpath": listPage_profileSearch_trafficMirroringProfiles_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_trafficMirroringProfiles_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_trafficMirroringProfiles_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_trafficMirroringProfiles_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posXpath": listPage_profileHandleButton_posXpath.format(replaceName=listPage_profile_statisticsTemplates_delButton_name),
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_trafficMirroringProfiles_button_yes_posXpath
    }
}
profile_ssl_decryption_keyring_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_sslDecryptionKeyrings_posId
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_sslDecryptionKeyrings_createButton_posId,
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_sslDecryptionKeyrings_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_sslDecryptionKeyrings_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_sslDecryptionKeyrings_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_sslDecryptionKeyrings_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_sslDecryptionKeyrings_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_sslDecryptionKeyrings_button_yes_posXpath
    }
}
profile_ssl_decryption_profile_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_sslDecryptionProfiles_posId
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_sslDecryptionProfiles_createButton_posId,
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_sslDecryptionProfiles_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_sslDecryptionProfiles_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_sslDecryptionProfiles_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_sslDecryptionProfiles_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_sslDecryptionProfiles_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_sslDecryptionProfiles_button_yes_posXpath
    }
}
profile_tcp_proxy_profile_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_tcpProxyProfiles_posId
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_tcpProxyProfiles_createButton_posId,
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_tcpProxyProfiles_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_tcpProxyProfiles_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_tcpProxyProfiles_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_tcpProxyProfiles_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_tcpProxyProfiles_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_tcpProxyProfiles_button_yes_posXpath
    }
}
profile_hijack_file_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_leftMenu_posXpath": mainPage_leftMenu_posXpath,
        "mainPage_profileFirstLevelMenu_Name": mainPage_firstLevelMenu_profiles_posName,
        "mainPage_profileSecondLevelMenu_Name": mainPage_secondLevelMenu_hijackFiles_posName,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_hijackFiles_posId
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_hijackFiles_createButton_posXpath,
        "profilePage_inputName_posXpath": hijackFiles_input_Name_posXpath,
        "profilePage_okButton_posXpath": hijackFiles_button_oK_posXpath,
        "profilePage_okButton_warningYes_posCss": hijackFiles_button_warningSaveYes_posXpath,
    },
    "search": {
        "profileListPage_searchLabel_posXpath": listPage_profileSearch_hijackFiles_selectLabel_posXpath,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_hijackFiles_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_hijackFiles_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_hijackFiles_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posXpath": listPage_profile_hijackFiles_delButton_posXpath,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_hijackFiles_button_yes_posXpath
    }
}
profile_insert_script_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_insertScripts_posId
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_insertScripts_createButton_posId,
        "profilePage_inputName_posId": insertScripts_input_Name_posId,
        "profilePage_okButton_posCss": insertScripts_button_oK_posCss,
        "profilePage_okButton_warningYes_posCss": insertScripts_button_warningSaveYes_posCss,
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_insertScripts_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_insertScripts_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_insertScripts_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_insertScripts_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_insertScripts_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_insertScripts_button_yes_posXpath
    }
}
profile_run_script_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_tsgProxyScripts_posId
    },
    "create": {
        "profileListPage_createButton_posXpath": listPage_profile_tsgProxyScripts_createButton_posId,
        "profilePage_inputName_posXpath": tsgProxyScripts_input_Name_posXpath,
        "profilePage_okButton_posCss": tsgProxyScripts_button_oK_posCss,
        "profilePage_okButton_warningYes_posCss": tsgProxyScripts_button_warningSaveYes_posCss,
    },
    "search": {
        "profileListPage_searchLabel_posId": listPage_profileSearch_insertScripts_selectLabel_posId,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_insertScripts_dropDown_item_posXpath,
        "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_insertScripts_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_insertScripts_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posId": listPage_profile_tsgProxyScripts_delButton_posId,
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_tsgProxyScripts_button_yes_posXpath
    }
}
profile_statistics_template_element_position = {
    "page_jump": {
        "mainPage_menu_bar_posXpath": mainPage_menu_bar_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
        "mainPage_profileFirstLevelMenu_posXpath": mainPage_firstLevelMenu_profiles_posXpath,
        "mainPage_profileSecondLevelMenu_posXpath": mainPage_secondLevelMenu_statisticsTemplates_posXpath,
        "mainPage_leftMenu_posXpath": mainPage_leftMenu_posXpath,
        "mainPage_profileFirstLevelMenu_Name": mainPage_firstLevelMenu_profiles_posName,
        "mainPage_profileSecondLevelMenu_Name": mainPage_secondLevelMenu_statisticsTemplates_Name
    },
    "create": {
        "templateListPage_createButton_posXpath": listPage_profileHandleButton_posXpath.format(replaceName=listPage_profile_statisticsTemplates_createButton_name),
        "templatePage_inputName_posId": statisticsTemplates_input_Name_posId,
        "statisticsTemplates_input_Name_posXpath": statisticsTemplates_input_Name_posXpath,
        "templates_button_chartAdd_posXpath": statisticsTemplates_button_chartAdd_posXpath,
        "templates_div_paperGrid_posXpath": statisticsTemplates_div_paperGrid_posXpath,
        "templates_radio_visualizationType_posXpath": statisticsTemplates_radio_visualizationType_posXpath,
        "templates_input_other_posXpath": statisticsTemplates_input_other_posXpath,
        "templates_input_thresholds_posXpath": statisticsTemplates_input_thresholds_posXpath,
        "templates_button_other_posXpath": statisticsTemplates_button_other_posXpath,
        "templates_button_chartOK_posXpath": statisticsTemplates_button_chartSubmit_posXpath,
        "templates_button_chartCancel_posXpath": statisticsTemplates_button_chartCancel_posXpath,
        "templates_button_oK_posCss": statisticsTemplates_button_oK_posXpath,
        "templates_button_cacel_posCss": statisticsTemplates_button_cancel_posXpath,
        "templates_button_warningSaveYes_posCss": statisticsTemplates_button_warningSaveYes_posCss,
        #"listPage_profileHandleButton_posXpath": listPage_profileHandleButton_posXpath
        # action
    },
    "edit":{
        "templates_button_chartEdit_posXpath": listPage_profileHandleButton_posXpath.format(replaceName=listPage_profile_statisticsTemplates_editButton_name)
    },
    "search": {
        "profileListPage_searchLabel_posXpath": listPage_profileSearch_statisticsTemplates_selectLabel_posXpath,
        "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_statisticsTemplates_dropDown_item_posXpath,
        #"profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_statisticsTemplates_input_itemContent_posXpath,
        "profileListPage_tableTbody_posXpath": listPage_profilTable_statisticsTemplates_tableTbody_posXpath
    },
    "delete": {
        "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
        "profileListPage_deleteButton_posXpath": listPage_profileHandleButton_posXpath.format(replaceName=listPage_profile_statisticsTemplates_delButton_name),
        "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_statisticsTemplates_button_yes_posXpath
    }
}

# log
log_session_log_element_position = {
    "page_jump": {
        "mainPage_navigationBar_logo_posXpath": mainPage_navigationBar_logo_posXpath,
        "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
        "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
        "mainPage_logFirstLevelMenu_posId": mainPage_firstLevelMenu_logs_posId,
        "mainPage_logSecondLevelMenu_posId": mainPage_secondLevelMenu_sessionRecords_posId
    },
    "search": {
        "logListPage_addFilterButton_posId": logListPage_addFilterButton_posId,
        "logListPage_enterModelButton_posId": logListPage_enterModelButton_posId,
        "logListPage_clearButton_posId": logListPage_clearButton_posId,
        "logListPage_queryButton_posId": logListPage_queryButton_posId,
        "logListPage_enterModel_posXpath": logListPage_enterModel_posXpath,
        "logListPage_totalText_posXpath": logListPage_totalText_posXpath,
        "logListPage_searchField_input_posXpath": logListPage_searchField_input_posXpath,
        "logListPage_searchRuleList_operation_posXpath": logListPage_searchRuleList_operation_posXpath,
        "logListPage_search_text_area_posXpath": logListPage_search_text_area_posXpath
    }
}


def get_profile_element_position(key_name):
    if key_name == "statistics_template":
        element_position_map = profile_statistics_template_element_position
    elif key_name == "monitor_profile":
        element_position_map = profile_monitor_profile_element_position
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{} no element position map".format(key_name))
        element_position_map = {}
    return element_position_map


def get_name_list(test_data):
    # 提取test_data数据中name列表，用于删除数据
    # [
    #             {
    #                 "type": "security",
    #                 "name": "security_rule_deny_ip",
    #             }
    #         ]
    name_list = []
    tmp_name_dict = {}
    # 添加策略的
    tmp_name_dict["type"] = test_data["policy_type"]
    if "rule_name" in test_data:
        tmp_name_dict["name"] = test_data["rule_name"]
        name_list.append(copy.deepcopy(tmp_name_dict))
    #"""
    if "condition" in test_data.keys() and len(test_data["condition"]) != 0:
        for key, value in test_data["condition"].items():
            if key in manipulation_object_no_create_list:
                continue  # 直接跳过
            if len(value) != 0:
                for i in range(len(value)):
                    tmp_name_dict = {}
                    tmp_name_dict["type"] = value[i]["object_type"]
                    if value[i]["object_type"] == "http_signature":
                        tmp_name_dict["type"] = "keywords"
                    tmp_name_dict["name"] = value[i]["name"]
                    name_list.append(copy.deepcopy(tmp_name_dict))
    if "action_parameter" in test_data.keys() and len(test_data["action_parameter"]) != 0:
        for key, value in test_data["action_parameter"].items():
            if key in manipulation_profile_no_create_list:
                continue  # 直接跳过
            if len(value) != 0:
                for i in range(len(value)):
                    tmp_name_dict = {}
                    tmp_name_dict["type"] = value[i]["profile_type"]
                    if value[i]["profile_type"] == "statistics_template":
                        tmp_name_dict["name"] = value[i]["name"]
                    elif value[i]["profile_type"] == "insert_script":
                        tmp_name_dict["script_type"] = value[i]["profile_file"]["script_type"]
                        tmp_name_dict["name"] = value[i]["profile_file"]["name"]
                    else:
                        tmp_name_dict["name"] = value[i]["profile_file"]["name"]
                     
                    name_list.append(copy.deepcopy(tmp_name_dict))
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], name_list)
    #"""
    return name_list

def create_pre_policy(data, driver):
    "manipulition创建前添加前置策略，security deny quic 和 intercept"
    create_rule = CreateRule(driver)
    test_data = data
    security_temp_deny_quic = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "security",
            "rule_name": "manipulation_pre_deny_quic",
            "rule_action": "deny",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
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
                        "name": "quic",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "新闻",
            "counters_1": {"hits": "many"},
            "log_query_param_1": [{"query_field_key":"client_ip", "query_value": "192.168.64.91"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv --connect-timeout 5 -m 10 http://www.news.cn/"
            },
            "token": ""
        }
    intercept_temp = {
            "is_multi_priority": False,
            "rule_num": 1,
            "policy_type": "proxy_intercept",
            "rule_name": "manipulation_pre_intercept",
            "rule_action": "intercept",
            "rule_type": "create",
            "condition": {
                "source_ip": [],
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
                    },
                    {
                        "name": "ssl",  #
                        "object_type": "application",
                        "negate": False
                    }
                ],
                "server_fqdn": [],
                "protocol_filed": [],
                "sub_action_override": True,
                "sub_action": [],
                "packet_capture": []
            },
            "profile": [],
            "expected_return": "新闻",
            "counters_1": {"hits": "many"},
            "log_query_param_1": [{"query_field_key":"client_ip", "query_value": "192.168.64.91"}],
            "traffic": {
                "type": "curl",
                "command": "curl -kv --connect-timeout 5 -m 10 http://www.news.cn/"
            },
            "token": ""
        }
    security_temp_deny_quic["condition"]["source_ip"] = data["condition"]["source_ip"]
    if test_data["policy_type"] == "service_chaining":
        intercept_temp["rule_name"] = "service_chaining_pre_intercept"
    intercept_temp["condition"]["source_ip"] = data["condition"]["source_ip"]
    security_rule_element_position = get_element_position("security")
    intercept_rule_element_position = get_element_position("proxy_intercept")
    #create_rule.create(security_temp_deny_quic, security_rule_element_position)
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create security rule successfully.", flush=True)
    result_info = create_rule.create(intercept_temp, intercept_rule_element_position)
    if result_info == 200:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create intercept rule successfully.", flush=True)
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create intercept rule failed.", flush=True)
    tmp_list = [
        # {
        #     "type": "security",
        #     "name": security_temp_deny_quic["rule_name"],
        # },
        {
            "type": "proxy_intercept",
            "name": intercept_temp["rule_name"],
        }
    ]
    return tmp_list

def delete_pre_policy(name_list, driver):
    for i in range(len(name_list)):
        policy_type = name_list[i]["type"]
        policy_name = name_list[i]["name"]
        element_position = get_element_position(policy_type)
        search_rule = SearchRule(driver)
        search_rule_code, first_row_checkbox_element = search_rule.search(policy_type, policy_name, element_position)
        delete_rule = DeleteRule(driver)
        delete_rule_code = delete_rule.delete(element_position, first_row_checkbox_element, True)
        if policy_type == "proxy_intercept":
            policy_type = "intercept"
        if delete_rule_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} rule successfully.".format(policy_type))
        elif delete_rule_code != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} rule failed.".format(policy_type))
        time.sleep(2)

def get_element_position(key_name):
    # object
    if key_name == "source_ip" or key_name == "internal_ip" or  key_name == "destination_ip" or key_name == "external_ip":
        element_position_map = object_ip_object_element_position
    elif key_name == "source_port" or key_name == "destination_port" or key_name == "external_port" or key_name == "internal_port":
        element_position_map = object_port_object_element_position
    elif key_name == "sub_id":
        element_position_map = object_subscriberid_object_element_position
    elif key_name == "apn":
        element_position_map = object_apn_object_element_position
    elif key_name == "device":
        element_position_map = object_mobile_identity_object_element_position
    # elif key_name == "mobile_identity":
    #     element_position_map = test_mobile_identity_object_element_position
    elif key_name == "http_signature":
        element_position_map = object_http_signature_object_element_position
    elif key_name == "keywords":
        element_position_map = object_keywords_object_element_position
    elif key_name == "server_fqdn" or key_name == "fqdn":
        element_position_map = object_fqdn_object_element_position
    elif key_name == "url":
        element_position_map = object_http_url_object_element_position
    elif key_name == "account":
        element_position_map =object_account_object_element_position
    elif key_name == "flag":
        element_position_map =object_flag_object_element_position
    # profile
    elif key_name == "response_page":
        element_position_map = profile_response_page_element_position
    elif key_name == "ssl_decryption_keyring":
        element_position_map = profile_ssl_decryption_keyring_element_position
    elif key_name == "ssl_decryption_profile":
        element_position_map = profile_ssl_decryption_profile_element_position
    elif key_name == "tcp_proxy_profile":
        element_position_map = profile_tcp_proxy_profile_element_position
    elif key_name == "traffic_mirroring_profile":
        element_position_map = profile_traffic_mirroring_profile_element_position
    elif key_name == "hijack_file":
        element_position_map = profile_hijack_file_element_position
    elif key_name == "insert_script":
        element_position_map = profile_insert_script_element_position
    elif key_name =="statistics_template":
        element_position_map = profile_statistics_template_element_position
    elif key_name == "run_script":
        element_position_map = profile_run_script_element_position
    # policy
    elif key_name == "proxy_manipulation":
        element_position_map = policy_manipulation_rule_element_position
    elif key_name == "security":
        element_position_map = policy_security_rule_element_position
    elif key_name == "monitor":
        element_position_map = policy_monitor_rule_element_position
    elif key_name == "dos_protection":
        element_position_map = policy_dos_protection_rule_element_position
    elif key_name == "proxy_intercept":
        element_position_map = policy_intercept_rule_element_position
    elif key_name == "statistics":
        element_position_map = policy_statistics_rule_element_position
    elif key_name == "service_chaining":
        element_position_map = policy_service_chaining_rule_element_position
    elif key_name == "session_log":
        element_position_map = log_session_log_element_position
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{} no element position map".format(key_name))
        element_position_map = {}
    return element_position_map


def replace_paras(parameter):
    #print(workdir)
    conf_path = os.path.join(workdir, "configuration_file.ini")
    parse = configparser.ConfigParser()
    parse.read(conf_path, encoding="utf-8")

    parameter["username"] = parse.get("account", "username")
    parameter["password"] = parse.get("account", "password")
    parameter["api_server"] = parse.get("tsg_url", "login_url")
    parameter["test_pc_ip"] = parse.get("network_address", "ip")
    parameter['test_subcriber_id'] = parse.get("network_address", "subcriber_id")
    parameter['test_imsi'] = parse.get("network_address", "imsi")
    parameter['test_phone_number'] = parse.get("network_address", "phone_number")
    parameter['test_imei'] = parse.get("network_address", "imei")
    parameter['test_apn'] = parse.get("network_address", "apn")
    parameter["vsys_id"] = parse.get("vsys", "for_traffic_verification")
    parameter["is_log"] = parse.get("is_log", "value")
    parameter["script_type"] = parse.get("debug_script_type", "script_type")

    #project_path = parse.get("root_path", "path")
    #parameter["root_path"] = project_path
    #print(parameter)
    return parameter

# 勿删 zcw make
manipulation_object_no_create_list = ["application", "sub_action_override", "sub_action", "ip_protocol"]
manipulation_profile_no_create_list = ["deny_response_text", "deny_response_block", "redirect_url", "replace_parameter", "edit_element_parameter", "doh"]