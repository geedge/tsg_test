# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from support.ui_utils.object.create_object import CreateObject
from support.ui_utils.object.search_object import SearchObject
from support.ui_utils.object.delete_object import DeleteObject
from support.ui_utils.policy.create_rule import CreateRule
from support.ui_utils.policy.search_rule import SearchRule
from support.ui_utils.policy.delete_rule import DeleteRule
from support.ui_utils.profile.create_profile import CreateProfile
from support.ui_utils.profile.search_profile import SearchProfile
from support.ui_utils.profile.delete_profile import DeleteProfile
from support.ui_utils.profile.create_dns_records_profile import CreateDnsProfile
from support.ui_utils.policy.edit_rule import EditRule
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.element_position.object_element_position import *
from support.packet_generator.verify import Verify
from support.api_utils.create_policy import CreatePolicy
from support.api_utils.analyse_result import *
from support.api_utils.log_in import *
from support.api_utils.delete_policy import DeletePolicy
import support.ui_utils.env
# from support.common.report import *
from datetime import datetime
from support.instance_utils.data_translation import DataTranslation
from support.ui_utils.element_position.map_element_position_library import *

class SecurityGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        result = self._run(self.test_data, self.parameter)
        return result

    def _run(self, test_data, parameter):
        # 参数初始化
        ui_result, api_result= "", ""
        self.api_name_list, self.ui_name_list = [], []
        result = {
            "ui_result": "",
            "api_result": ""
        }
        
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        need_initialization = False
        if len(parameter["script_type"]) == 0:
            need_initialization = True

        if parameter["script_type"] == "ui" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run ui test case", flush=True)

                parameter["script_type"] = "ui"

                # 环境初始化
                support.ui_utils.env.initiate_selenium_request()
                driver = support.ui_utils.env.my_driver()
                support.ui_utils.env.setup()
                # 组织security 的name list
                tmp_name_dict = {}
                tmp_name_dict["type"] = test_data["policy_type"]
                tmp_name_dict["name"] = test_data["rule_name"]
                self.ui_name_list.append(tmp_name_dict)
                # 组织object类的name list
                for key in ["source_ip", "external_ip", "internal_ip", "device", "server_fqdn", "protocol_filed", "internal_port"]:
                    if key in test_data["condition"] and len(test_data["condition"][key]) != 0:
                        object_data = test_data["condition"][key]
                        for i in range(len(object_data)):
                            # 针对 protocol_filed 进行特殊处理，排除 boolean 类型
                            if key == "protocol_filed" and object_data[i]['object_type'] == 'boolean':
                                continue

                            tmp_name_dict = {
                                "type": object_data[i]['object_type'],
                                "name": object_data[i]['name']
                            }
                            self.ui_name_list.append(tmp_name_dict)
                # 添加定位库集合
                test_rule_element_position = {}
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
                    test_fqdn_object_element_position = {
                        "page_jump":{
                            "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                            "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                            "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                            # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                            "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                            "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_fqdn_posId
                        },
                        "create": {
                            "objectListPage_createButton_posId": fqdnObjectListPage_createButton_posId,
                            "objectListPage_dropDown_createButton_posId": fqdnObjectListPage_dropDown_createButton_posId,
                            "objectPage_inputName_posXpath": fqdnObjectPage_inputName_posXpath,
                            "objectPage_addItem_posId": fqdnObjectPage_addItem_posId,
                            "objectPage_inputItem_posXpath": fqdnObjectPage_inputItem_posXpath,
                            "objectPage_button_saveItem_posXpath": fqdnObjectPage_button_saveItem_posXpath,
                            "objectPage_okButton_posId": fqdnObjectPage_okButton_posId,
                            "objectPage_okButton_warningYes_posXpath": fqdnObjectPage_okButton_warningYes_posXpath
                        },
                        "search": {
                            "objectListPage_searchLabel_posId": fqdnObjectListPage_searchLabel_posId,
                            "objectListPage_searchLabel_selectName_posXpath": fqdnObjectListPage_searchLabel_selectName_posXpath,
                            "objectListPage_tableTbody_posXpath": fqdnObjectListPage_tableTbody_posXpath
                        },
                        "delete": {
                            "objectListPage_allSelect_posXpath": fqdnObjectListPage_allSelect_posXpath,
                            "objectListPage_deleteButton_posId": fqdnObjectListPage_deleteButton_posId,
                            "objectListPage_deleteButton_warningYes_posXpath": fqdnObjectListPage_deleteButton_warningYes_posXpath
                        }
                    }
                    test_url_object_element_position = {
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
                    test_imsi_object_element_position = {
                        "page_jump":{
                            "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                            "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                            "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                            # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                            "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                            "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_mobileIdentify_posId
                        },
                        "create": {
                            "objectListPage_createButton_posId": mobile_identitiesObjectListPage_createButton_posId,
                            "objectListPage_dropDown_createButton_posId": mobile_identitiesObjectListPage_dropDown_createButton_posId,
                            "objectPage_inputName_posXpath": mobile_identitiesObjectPage_inputName_posXpath,
                            "objectPage_imsiType_posId": imsiObjectPage_imsiType_posId,
                            "objectPage_addItem_posId": imsiObjectPage_addItem_posId,
                            "objectPage_inputItem_posXpath": imsiObjectPage_inputItem_posXpath,
                            "objectPage_button_saveItem_posXpath": imsiObjectPage_button_saveItem_posXpath,
                            "objectPage_okButton_posId": imsiObjectPage_okButton_posId,
                            "objectPage_okButton_warningYes_posXpath": imsiObjectPage_okButton_warningYes_posXpath
                        },
                        "search": {
                            "objectListPage_searchLabel_posId": imsiObjectListPage_searchLabel_posId,
                            "objectListPage_searchLabel_selectName_posXpath": imsiObjectListPage_searchLabel_selectName_posXpath,
                            "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
                        },
                        "delete": {
                            "objectListPage_allSelect_posXpath": imsiObjectListPage_allSelect_posXpath,
                            "objectListPage_deleteButton_posId": imsiObjectListPage_deleteButton_posId,
                            "objectListPage_deleteButton_warningYes_posXpath": imsiObjectListPage_deleteButton_warningYes_posXpath
                        }
                    }
                    test_phone_number_object_element_position = {
                        "page_jump":{
                            "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                            "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                            "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                            # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                            "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                            "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_mobileIdentify_posId
                        },
                        "create": {
                            "objectListPage_createButton_posId": mobile_identitiesObjectListPage_createButton_posId,
                            "objectListPage_dropDown_createButton_posId": mobile_identitiesObjectListPage_dropDown_createButton_posId,
                            "objectPage_inputName_posXpath": mobile_identitiesObjectPage_inputName_posXpath,
                            "objectPage_phnoeNumberType_posId": phoneNumberObjectPage_phoneNumberType_posId,
                            "objectPage_addItem_posId": phoneNumberObjectPage_addItem_posId,
                            "objectPage_inputItem_posXpath": phoneNumberObjectPage_inputItem_posXpath,
                            "objectPage_button_saveItem_posXpath": phoneNumberObjectPage_button_saveItem_posXpath,
                            "objectPage_okButton_posId": phoneNumberObjectPage_okButton_posId,
                            "objectPage_okButton_warningYes_posXpath": phoneNumberObjectPage_okButton_warningYes_posXpath
                        },
                        "search": {
                            "objectListPage_searchLabel_posId": imsiObjectListPage_searchLabel_posId,
                            "objectListPage_searchLabel_selectName_posXpath": imsiObjectListPage_searchLabel_selectName_posXpath,
                            "objectListPage_tableTbody_posXpath": ipObjectListPage_tableTbody_posXpath
                        },
                        "delete": {
                            "objectListPage_allSelect_posXpath": imsiObjectListPage_allSelect_posXpath,
                            "objectListPage_deleteButton_posId": imsiObjectListPage_deleteButton_posId,
                            "objectListPage_deleteButton_warningYes_posXpath": imsiObjectListPage_deleteButton_warningYes_posXpath
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
                    test_keywords_object_element_position = {
                        "page_jump": {
                            "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                            "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                            "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                            # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                            "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                            "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_keywords_posId
                        },
                        "create": {
                            "objectListPage_createButton_posId": keywordsObjectListPage_createButton_posId,
                            "objectListPage_dropDown_createButton_posId": keywordsObjectListPage_dropDown_createButton_posId,
                            "objectPage_inputName_posXpath": keywordsObjectPage_inputName_posXpath,
                            "objectPage_addItem_posId": keywordsObjectPage_addItem_posId,
                            "objectPage_item_value_select_posXpath": keywordsObjectPage_item_value_select_posXpath,
                            "objectPage_inputItem_posXpath": keywordsObjectPage_inputItem_posXpath,
                            "objectPage_item_value_plus_posXpath": keywordsObjectPage_item_value_plus_posXpath,
                            "objectPage_button_saveItem_posXpath": keywordsObjectPage_button_saveItem_posXpath,
                            "objectPage_okButton_posId": keywordsObjectPage_okButton_posId,
                            "objectPage_okButton_warningYes_posXpath": keywordsObjectPage_okButton_warningYes_posXpath
                        },
                        "search": {
                            "objectListPage_searchLabel_posId": keywordsObjectListPage_searchLabel_posId,
                            "objectListPage_searchLabel_selectName_posXpath": keywordsObjectListPage_searchLabel_selectName_posXpath,
                            "objectListPage_tableTbody_posXpath": keywordsObjectListPage_tableTbody_posXpath
                        },
                        "delete": {
                            "objectListPage_allSelect_posXpath": keywordsObjectListPage_allSelect_posXpath,
                            "objectListPage_deleteButton_posId": keywordsObjectListPage_deleteButton_posId,
                            "objectListPage_deleteButton_warningYes_posXpath": keywordsObjectListPage_deleteButton_warningYes_posXpath
                        }
                    }
                    test_account_object_element_position = {
                        "page_jump": {
                            "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                            "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                            "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                            # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                            "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                            "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_account_posId
                        },
                        "create": {
                            "objectListPage_createButton_posId": accountObjectListPage_createButton_posId,
                            "objectListPage_dropDown_createButton_posId": accountObjectListPage_dropDown_createButton_posId,
                            "objectPage_inputName_posXpath": accountObjectPage_inputName_posXpath,
                            "objectPage_addItem_posId": accountObjectPage_addItem_posId,
                            # item简单定位
                            "objectPage_inputItem_posXpath": accountObjectPage_inputItem_posXpath,
                            "objectPage_button_saveItem_posXpath": accountObjectPage_button_saveItem_posXpath,
                            "objectPage_okButton_posId": accountObjectPage_okButton_posId,
                            "objectPage_okButton_warningYes_posXpath": accountObjectPage_okButton_warningYes_posXpath
                        },
                        "search": {
                            "objectListPage_searchLabel_posId": accountObjectPage_searchLabel_posId,
                            "objectListPage_searchLabel_selectName_posXpath": accountObjectListPage_searchLabel_selectName_posXpath,
                            "objectListPage_tableTbody_posXpath": accountObjectPage_tableTbody_posXpath
                        },
                        "delete": {
                            "objectListPage_allSelect_posXpath": accountObjectPage_allSelect_posXpath,
                            "objectListPage_deleteButton_posId": accountObjectListPage_deleteButton_posId,
                            "objectListPage_deleteButton_warningYes_posXpath": accountObjectListPage_deleteButton_warningYes_posXpath
                        }
                    }
                    test_dns_records_profile_element_position = {
                        "page_jump": {
                            "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                            "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                            "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                            # "mainPage_vsysTree_vsysName_posXpath": mainPage_vsysTree_vsysName_posXpath,
                            "mainPage_profileFirstLevelMenu_posId": mainPage_firstLevelMenu_profiles_posId,
                            "mainPage_profileSecondLevelMenu_posId": mainPage_secondLevelMenu_dnsRecords_posId
                        },
                        "create": {
                            "profileListPage_createButton_posId": listPage_profile_dnsRecords_createButton_posId,
                            "profilePage_inputName_posId": dnsRecordsProfilePage_input_Name_posId,
                            "profilePage_Type_A_posId": dnsRecordsProfilePage_radioButton_typeA_posId,
                            "dnsRecordsProfiles_input_item_posXpath": dnsRecordsProfilePage_input_addItem_posXpath,
                            "dnsRecordsProfile_save_item_posXpath": dnsRecordsProfilePage_button_saveItemByIndex_posXpath,
                            "profilePage_button_oK_posCss": dnsRecordsProfilePage_button_oK_posCss,
                            "profilePage_button_cancel_posCss": dnsRecordsProfilePage_button_cancel_posCss,
                            "profilePage_button_warningSaveYes_posCss": dnsRecordsProfilePage_button_warningSaveYes_posCss,
                            # action
                        },
                        "edit": {
                            "templates_button_chartEdit_posXpath": listPage_profile_dnsRecords_editButton_posId
                        },
                        "search": {
                            "profileListPage_searchLabel_posId": listPage_profileSearch_dnsRecords_selectLabel_posId,
                            "profileListPage_searchLabel_selectName_posXpath": listPage_profileSearch_dnsRecords_dropDown_item_posXpath,
                            "profileListPage_searchLabel_inputContent_posXpath": listPage_profileSearch_dnsRecords_input_itemContent_posXpath,
                            "profileListPage_tableTbody_posXpath": listPage_profilTable_dnsRecords_tableTbody_posXpath
                        },
                        "delete": {
                            "profileListPage_allSelect_posXpath": mainPage_profileBottomPage_button_allSelect_posXpath,
                            "profileListPage_deleteButton_posId": listPage_profile_dnsRecords_delButton_posId,
                            "profileListPage_deleteButton_warningYes_posXpath": listPage_dialogTips_dnsRecords_button_yes_posXpath
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
                            # srcip
                            "policyRulePage_addSrcIP_posXpath": securityRulePage_addSrcIP_posXpath,
                            "policyRulePage_searchSrcIP_posXpath": securityRulePage_searchSrcIP_posXpath,
                            "policyRulePage_selectSrcIP_posXpath": securityRulePage_selectSrcIP_posXpath,
                            "policyRulePage_closeSrcIP_posXpath": securityRulePage_closeSrcIP_posXpath,
                            # external ip
                            "policyRulePage_addConditionExternalIP_posXpath": securityRulePage_addCondition_externalIP_posXpath,
                            "policyRulePage_addExternalIP_posXpath": securityRulePage_addExternalIP_posXpath,
                            "policyRulePage_searchExternalIP_posXpath": securityRulePage_searchExternalIP_posXpath,
                            "policyRulePage_selectExternalIP_posXpath": securityRulePage_selectExternalIP_posXpath,
                            "policyRulePage_closeExternalIP_posXpath": securityRulePage_closeExternalIP_posXpath,
                            # imsi
                            "policyRulePage_addConditionImsi_posXpath": securityRulePage_addCondition_imsi_posXpath,
                            "policyRulePage_addImsi_posXpath": securityRulePage_addImsi_posXpath,
                            "policyRulePage_searchImsi_posXpath": policyRulePage_searchImsi_posXpath,
                            "policyRulePage_selectImsi_posXpath": policyRulePage_selectImsi_posXpath,
                            "policyRulePage_closeImsi_posXpath": policyRulePage_closeImsi_posXpath,
                            # phone number
                            "policyRulePage_choosePhoneNumber_posXpath": securityRulePage_choosePhoneNumber_posXpath,
                            # internal ip
                            "policyRulePage_addConditionInternalIP_posXpath": securityRulePage_addCondition_internalIP_posXpath,
                            "policyRulePage_addInternalIP_posXpath": securityRulePage_addInternalIP_posXpath,
                            "policyRulePage_searchInternalIP_posXpath": securityRulePage_searchInternalIP_posXpath,
                            "policyRulePage_selectInternalIP_posXpath": securityRulePage_selectInternalIP_posXpath,
                            "policyRulePage_closeInternalIP_posXpath": securityRulePage_closeInternalIP_posXpath,
                            # internal port
                            "policyRulePage_addConditionInternalPort_posXpath": securityRulePage_addCondition_internalPort_posXpath,
                            "policyRulePage_addInternalPort_posXpath": securityRulePage_addInternalPort_posXpath,
                            "policyRulePage_searchInternalPort_posXpath": securityRulePage_searchInternalPort_posXpath,
                            "policyRulePage_selectInternalPort_posXpath": securityRulePage_selectInternalPort_posXpath,
                            "policyRulePage_closeInternalPort_posXpath": securityRulePage_closeInternalPort_posXpath,
                            #dst Port
                            "policyRulePage_addConditionDstPort_posXpath": securityRulePage_addCondition_dstPort_posXpath,
                            "policyRulePage_addDstPort_posXpath": securityRulePage_addDstPort_posXpath,
                            "policyRulePage_searchDstPort_posXpath": securityRulePage_searchDstPort_posXpath,
                            "policyRulePage_selectDstPort_posXpath": securityRulePage_selectDstPort_posXpath,
                            "policyRulePage_closeDstPort_posXpath": securityRulePage_closeDstPort_posXpath,
                            # External Port
                            "policyRulePage_addConditionExternalPort_posXpath": policyRulePage_addCondition_externalPort_posXpath,
                            "policyRulePage_addExternalPort_posXpath": policyRulePage_addExternalPort_posXpath,
                            "policyRulePage_searchExternalPort_posXpath": policyRulePage_searchExternalPort_posXpath,
                            "policyRulePage_selectExternalPort_posXpath": policyRulePage_selectExternalPort_posXpath,
                            "policyRulePage_closeExternalPort_posXpath": policyRulePage_closeExternalPort_posXpath,
                            # application
                            "policyRulePage_addApplication_posXpath": securityRulePage_addApplication_posXpath,
                            "policyRulePage_searchApplication_posXpath": securityRulePage_searchApplication_posXpath,
                            "policyRulePage_selectApplication_posXpath": securityRulePage_selectApplication_posXpath,
                            "policyRulePage_closeApplication_posXpath": securityRulePage_closeApplication_posXpath,
                            "policyRulePage_selectApplicationLabel_posXpath": securityRulePage_selectApplicationLabel_posXpath,
                            "policyRulePage_addCondition_posXpath": securityRulePage_addCondition_posXpath,
                            "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                            # fqdn
                            "policyRulePage_addConditionServerFqdn_posXpath": securityRulePage_addCondition_serverFqdn_posXpath,
                            "policyRulePage_addServerFqdn_posXpath": securityRulePage_addServerFqdn_posXpath,
                            "policyRulePage_searchServerFqdn_posXpath": securityRulePage_searchServerFqdn_posXpath,
                            "policyRulePage_selectServerFqdn_posXpath": securityRulePage_selectServerFqdn_posXpath,
                            "policyRulePage_closeServerFqdn_posXpath": securityRulePage_closeServerFqdn_posXpath,
                            # ftp协议
                            # ftp account
                            "policyRulePage_addConditionFtpAccount_posXpath": securityRulePage_addCondition_ftpAccount_posXpath,
                            "policyRulePage_addFtpAccount_posXpath": securityRulePage_addftpAccount_posXpath,
                            "policyRulePage_searchFtpAccount_posXpath": securityRulePage_searchftpAccount_posXpath,
                            "policyRulePage_selectFtpAccount_posXpath": securityRulePage_selectftpAccount_posXpath,
                            "policyRulePage_closeFtpAccount_posXpath": securityRulePage_closeftpAccount_posXpath,
                            # ftp content
                            "policyRulePage_addConditionFtpContent_posXpath": securityRulePage_addCondition_ftpContent_posXpath,
                            "policyRulePage_addFtpContent_posXpath": securityRulePage_addftpContent_posXpath,
                            "policyRulePage_searchFtpContent_posXpath": securityRulePage_searchftpContent_posXpath,
                            "policyRulePage_selectFtpContent_posXpath": securityRulePage_selectftpContent_posXpath,
                            "policyRulePage_closeFtpContent_posXpath": securityRulePage_closeftpContent_posXpath,
                            # http协议
                            # url
                            "policyRulePage_addConditionUrl_posXpath": securityRulePage_addCondition_url_posXpath,
                            "policyRulePage_addUrl_posXpath": policyRulePage_addUrl_posXpath,
                            "policyRulePage_searchUrl_posXpath": policyRulePage_searchUrl_posXpath,
                            "policyRulePage_selectUrl_posXpath": policyRulePage_selectUrl_posXpath,
                            "policyRulePage_closeUrl_posXpath": policyRulePage_closeUrl_posXpath,
                            # req header
                            "policyRulePage_addConditionRequestHeader_posXpath": securityRulePage_addCondition_requestHeader_posXpath,
                            "policyRulePage_addRequestHeader_posXpath": manipulationRulePage_addRequestHeader_posXpath,
                            "policyRulePage_searchRequestHeader_posXpath": securityRulePage_searchRequestHeader_posXpath,
                            "policyRulePage_selectRequestHeader_posXpath": securityRulePage_selectRequestHeader_posXpath,
                            "policyRulePage_closeRequestHeader_posXpath": securityRulePage_closeRequestHeader_posXpath,
                            "policyRulePage_addCondition_close_posXpath": securityRulePage_addCondition_close_posXpath,
                            "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
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
                            # ip protocol
                            "policyRulePage_addConditionIpProtocol_posXpath": policyRulePage_addCondition_IpProtocol_posXpath,
                            "policyRulePage_addIpProtocol_posXpath": policyRulePage_addIpProtocol_posXpath,
                            "policyRulePage_searchIpProtocol_posXpath": policyRulePage_searchIpProtocol_posXpath,
                            "policyRulePage_selectIpProtocol_posXpath": policyRulePage_selectIpProtocol_posXpath,
                            "policyRulePage_closeIpProtocol_posXpath": policyRulePage_closeIpProtocol_posXpath,
                            # mail协议
                            #mail attachment name
                            "policyRulePage_addConditionMailAttachmentName_posXpath": policyRulePage_addCondition_mailAttachmentName_posXpath,
                            "policyRulePage_addMailAttachmentName_posXpath": policyRulePage_addMailAttachmentName_posXpath,
                            "policyRulePage_searchMailAttachmentName_posXpath": policyRulePage_searchMailAttachmentName_posXpath,
                            "policyRulePage_selectMailAttachmentName_posXpath": policyRulePage_selectMailAttachmentName_posXpath,
                            "policyRulePage_closeMailAttachmentName_posXpath": policyRulePage_closeMailAttachmentName_posXpath,
                            #mail attachment content
                            "policyRulePage_addConditionMailAttachmentContent_posXpath": policyRulePage_addCondition_mailAttachmentContent_posXpath,
                            "policyRulePage_addMailAttachmentContent_posXpath": policyRulePage_addMailAttachmentContent_posXpath,
                            "policyRulePage_searchMailAttachmentContent_posXpath": policyRulePage_searchMailAttachmentContent_posXpath,
                            "policyRulePage_selectMailAttachmentContent_posXpath": policyRulePage_selectMailAttachmentContent_posXpath,
                            "policyRulePage_closeMailAttachmentContent_posXpath": policyRulePage_closeMailAttachmentContent_posXpath,
                            #mail content
                            "policyRulePage_addConditionMailContent_posXpath": policyRulePage_addCondition_mailContent_posXpath,
                            "policyRulePage_addMailContent_posXpath": policyRulePage_addMailContent_posXpath,
                            "policyRulePage_searchMailContent_posXpath": policyRulePage_searchMailContent_posXpath,
                            "policyRulePage_selectMailContent_posXpath": policyRulePage_selectMailContent_posXpath,
                            "policyRulePage_closeMailContent_posXpath": policyRulePage_closeMailContent_posXpath,
                            # mail from
                            "policyRulePage_addConditionMailFrom_posXpath": policyRulePage_addCondition_mailFrom_posXpath,
                            "policyRulePage_addMailFrom_posXpath": monitorRulePage_addmailFrom_posXpath,
                            "policyRulePage_searchMailFrom_posXpath": monitorRulePage_searchmailFrom_posXpath,
                            "policyRulePage_selectMailFrom_posXpath": monitorRulePage_selectmailFrom_posXpath,
                            "policyRulePage_closeMailFrom_posXpath": monitorRulePage_closemailFrom_posXpath,
                            #添加mail subject
                            "policyRulePage_addConditionMailSubject_posXpath": policyRulePage_addCondition_mailSubject_posXpath,
                            "policyRulePage_addMailSubject_posXpath": monitorRulePage_addmailSubject_posXpath,
                            "policyRulePage_searchMailSubject_posXpath": monitorRulePage_searchmailSubject_posXpath,
                            "policyRulePage_selectMailSubject_posXpath": monitorRulePage_selectmailSubject_posXpath,
                            "policyRulePage_closeMailSubject_posXpath": monitorRulePage_closemailSubject_posXpath,
                            # mail to
                            "policyRulePage_addConditionMailTo_posXpath": policyRulePage_addCondition_mailTo_posXpath,
                            "policyRulePage_addMailTo_posXpath": monitorRulePage_addmailTo_posXpath,
                            "policyRulePage_searchMailTo_posXpath": monitorRulePage_searchmailTo_posXpath,
                            "policyRulePage_selectMailTo_posXpath": monitorRulePage_selectmailTo_posXpath,
                            "policyRulePage_closeMailTo_posXpath": monitorRulePage_closemailTo_posXpath,
                            # ssl 协议
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
                            #add ssl no sni
                            "policyRulePage_addConditionBoolean_posXpath": policyRulePage_addCondition_Boolean_posXpath,
                            "policyRulePage_addBoolean_posXpath": policyRulePage_addBoolean_posXpath,
                            "policyRulePage_searchBoolean_posXpath": policyRulePage_searchBoolean_posXpath,
                            "policyRulePage_selectBoolean_posXpath": policyRulePage_selectBoolean_posXpath,
                            "policyRulePage_closeBoolean_posXpath": policyRulePage_closeBoolean_posXpath,
                            "policyRulePage_little_button_addBoolean_posXpath":policyRulePage_little_button_addBoolean_posXpath,
                            # dns 协议
                            # qname
                            "policyRulePage_addConditionQname_posXpath": securityRulePage_addCondition_qname_posXpath,
                            "policyRulePage_addQname_posXpath": securityRulePage_addQname_posXpath,
                            "policyRulePage_searchQname_posXpath": securityRulePage_searchQname_posXpath,
                            "policyRulePage_selectQname_posXpath": securityRulePage_selectQname_posXpath,
                            "policyRulePage_closeQname_posXpath": securityRulePage_closeQname_posXpath,
                            # deny子动作
                            # rate limit
                            "policyRulePage_subAction_rateLimit_posXpath": securityRulePage_subAction_rateLimit_posXpath,
                            "policyRulePage_subAction_rateLimit_rate_posXpath": securityRulePage_subAction_rateLimit_rate_posXpath,
                            # tamper
                            "policyRulePage_subAction_tamper_posXpath": securityRulePage_subAction_tamper_posXpath,
                            # drop
                            "policyRulePage_subAction_override_posXpath": securityRulePage_subAction_override_posXpath,
                            "policyRulePage_subAction_drop_posXpath": securityRulePage_subAction_drop_posXpath,
                            "policyRulePage_subAction_drop_dropPkt_posXpath": securityRulePage_subAction_drop_dropPkt_posXpath,
                            "policyRulePage_subAction_drop_sendTcpRst_posXpath": securityRulePage_subAction_drop_sendTcpRst_posXpath,
                            "policyRulePage_subAction_drop_sendIcmp_posXpath": securityRulePage_subAction_drop_sendIcmp_posXpath,
                            # block动作
                            "policyRulePage_subAction_block_posXpath": securityRulePage_subAction_block_posXpath,
                            "policyRulePage_subAction_block_responseCode_posXpath": securityRulePage_subAction_block_responseCode_posXpath,
                            "policyRulePage_subAction_block_responseCode_change_posXpath": securityRulePage_subAction_block_responseCode_change_posXpath,
                            "policyRulePage_subAction_block_responseContent_posXpath": securityRulePage_subAction_block_responseContent_posXpath,
                            "policyRulePage_subAction_block_responseContent_change_posXpath": securityRulePage_subAction_block_responseContent_change_posXpath,
                            "policyRulePage_subAction_block_responseContent_clickProfile_posXpath": securityRulePage_subAction_block_responseContent_clickProfile_posXpath,
                            "policyRulePage_subAction_block_responseContent_searchProfile_posXpath": securityRulePage_subAction_block_responseContent_searchProfile_posXpath,
                            "policyRulePage_subAction_block_responseContent_selectProfile_posId": securityRulePage_subAction_block_responseContent_selectProfile_posId,
                            "policyRulePage_subAction_block_responseContent_text_posId": securityRulePage_subAction_block_responseContent_text_posId,
                            # alert动作
                            "policyRulePage_subAction_alert_posXpath": securityRulePage_subAction_alert_posXpath,
                            "policyRulePage_subAction_alert_responseCode_posXpath": securityRulePage_subAction_alert_responseCode_posXpath,
                            "policyRulePage_subAction_alert_responseCode_change_posXpath": securityRulePage_subAction_alert_responseCode_change_posXpath,
                            "policyRulePage_subAction_alert_responseContent_posXpath": securityRulePage_subAction_alert_responseContent_posXpath,
                            "policyRulePage_subAction_alert_responseContent_change_posXpath": securityRulePage_subAction_alert_responseContent_change_posXpath,
                            "policyRulePage_subAction_alert_responseContent_clickProfile_posXpath": securityRulePage_subAction_alert_responseContent_clickProfile_posXpath,
                            "policyRulePage_subAction_alert_responseContent_searchProfile_posXpath": securityRulePage_subAction_alert_responseContent_searchProfile_posXpath,
                            "policyRulePage_subAction_alert_responseContent_selectProfile_posId": securityRulePage_subAction_alert_responseContent_selectProfile_posId,
                            "policyRulePage_subAction_alert_responseContent_text_posId": securityRulePage_subAction_alert_responseContent_text_posId,
                            # http redirect 动作
                            "policyRulePage_subAction_redirect_posXpath": securityRulePage_subAction_redirect_posXpath,
                            "policyRulePage_subAction_redirect_input_posId": securityRulePage_subAction_redirect_input_posXpath,
                            # dns redirect
                            "policyRulePage_dnsAnswer0ValueType_posId":  securityRulePage_subAction_redirect_answer0ValueType_posId,
                            "policyRulePage_dnsAnswer0ValueTypeChoose_posXpath":  securityRulePage_subAction_redirect_answer0ValueTypeChoose_posXpath,
                            "policyRulePage_dnsAnswer0ValueTypeChoose_posXpath":  securityRulePage_subAction_redirect_answer0ValueTypeChoose_posXpath,
                            "policyRulePage_dnsAnswerValueSelectPlaceholder_posId": securityRulePage_subAction_redirect_dnsAnswerValueSelectPlaceholder_posId,
                            "policyRulePage_dnsAnswerValueNameSearch_posId": securityRulePage_subAction_redirect_dnsAnswerValueNameSearch_posId,
                            "policyRulePage_dnsAnswerType0Choose_posId": securityRulePage_subAction_redirect_dnsAnswerType0choose_posId,
                            "policyRulePage_dnsAnswerType0ChooseValue_posXpath": securityRulePage_subAction_redirect_dnsAnswerType0chooseValue_posXpath,
                            "policyRulePage_dnsAnswerValueNameSelect_posId": securityRulePage_subAction_redirect_dnsAnswerValueNameSelect_posId,
                            "policyRulePage_dnsAnswer0ATextPlaceholder_posId": securityRulePage_subAction_redirect_dnsAnswer0ATextPlaceholder_posId,
                            "policyRulePage_dnsAnswerValueTTL0_posId": securityRulePage_subAction_redirect_dnsAnswerValueTTL0_posId,
                            # enable 按钮
                            "policyRulePage_enable_posXpath": securityRulePage_enable_posXpath,
                            # ok按钮
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
                    if test_data["rule_action"] == "allow":
                        test_rule_element_position["create"]["policyRulePage_selectAction_posId"] = securityRulePage_selectAllow_posId
                    elif test_data["rule_action"] == "shunt":
                        test_rule_element_position["create"]["policyRulePage_selectAction_posId"] = securityRulePage_selectShunt_posId
                    if "application" in test_data['condition'] and len(test_data['condition']["application"]) == 1 and test_data['condition']["application"][0]['name'] == "ftp":
                        test_rule_element_position["create"]["policyRulePage_addConditionUrl_posXpath"] = securityRulePage_addCondition_uri_posXpath

                # 创建IP
                create_ip_code = 200
                ip_keys = ["source_ip", "external_ip", "internal_ip"]
                for key in ip_keys:
                    if key in test_data["condition"] and test_data["condition"][key]:
                        ip_data = test_data["condition"][key]
                        create_ip = CreateObject(driver)
                        for ip in ip_data:
                            create_ip_code = create_ip.create(ip, test_ip_object_element_position)
                            if create_ip_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create ip object successfully.", flush=True)
                            else:
                                ui_result = "Fail to create ip."
                                break
                # 创建port
                port_keys = ["internal_port", "destination_port", "external_port"]
                for key in port_keys:
                    if key in test_data["condition"] and test_data["condition"][key]:
                        port_data = test_data["condition"][key]
                        create_port = CreateObject(driver)
                        for port in port_data:
                            create_port_code = create_port.create(port, test_port_object_element_position)
                            if create_port_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create port object successfully.", flush=True)
                            else:
                                ui_result = "Fail to create port."
                                break
                # 创建server fqdn
                if "server_fqdn" in test_data["condition"] and len(test_data["condition"]["server_fqdn"]) != 0:
                    fqdn_data = test_data["condition"]["server_fqdn"]
                    create_fqdn = CreateObject(driver)
                    for i in range(len(fqdn_data)):
                        create_fqdn_code = create_fqdn.create(fqdn_data[i], test_fqdn_object_element_position)
                        if create_fqdn_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create fqdn object successfully.", flush=True)
                        elif create_fqdn_code != 200:
                            result = "Fail to create fqdn."
                            break

                # 创建imsi
                if "device" in test_data["condition"] and len(test_data["condition"]["device"]) != 0:
                    device_data = test_data["condition"]["device"]
                    create_device = CreateObject(driver)
                    for i in range(len(device_data)):
                        object_sub_type = device_data[i]['item'][0]['item_type']
                        if object_sub_type == 'imsi':
                            create_device_code = create_device.create(device_data[i], test_imsi_object_element_position)
                        elif object_sub_type == 'phone_number':
                            create_device_code = create_device.create(device_data[i], test_phone_number_object_element_position)
                        if create_device_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_sub_type), flush=True)
                        elif create_device_code != 200:
                            result = "Fail to create {} object.".format(object_sub_type)
                            break

                if "action_parameter" in test_data.keys():
                    for prfi_key, prfi_value in(test_data["action_parameter"]).items():
                        prfi_status = 0
                        prfi_key_out = prfi_key.replace("_", " ")
                        if len(prfi_value) != 0:   # 需要创建profile数据
                            prfi_data = prfi_value
                            prfi = CreateProfile(driver)
                            for i in range(len(prfi_data)): # 遍历创建所有 profile
                                element_position_map = get_element_position(prfi_key)
                                prfi_code = prfi.create(prfi_data[i], element_position_map)
                                if prfi_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(prfi_key_out), flush=True)
                                else:
                                    result = "Fail to create {} profile.".format(prfi_key_out)
                                    prfi_status = 1
                                    break
                        if prfi_status == 1:  # 创建失败，退出遍历创建
                            break
                # 创建dns record profile
                if "profile" in test_data  and len(test_data["profile"]) != 0:
                    profile_data = test_data["profile"]
                    dnsRecords_profile = CreateDnsProfile(driver,test_dns_records_profile_element_position)
                    for i in range(len(profile_data)):
                        create_profile_code = dnsRecords_profile.create_dns_records_profile(profile_data[i],test_dns_records_profile_element_position,test_data["profile"][i]["name"])
                        if create_profile_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create traffic dns records profile successfully.", flush=True)
                        elif create_profile_code != 200:
                            result = "Fail to create Dns Records Profiles profile."
                            break

                # 创建protocol_filed
                if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
                    protocol_field_data = test_data["condition"]["protocol_filed"]
                    create_protocol_filed = CreateObject(driver)
                    for x in range(len(protocol_field_data)):
                        object_type = protocol_field_data[x]['object_type']
                        if object_type == 'url':
                            create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_url_object_element_position)
                        elif object_type == 'fqdn':
                            create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_fqdn_object_element_position)
                        elif object_type == 'keywords':
                            create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_keywords_object_element_position)
                        elif object_type == 'account':
                            create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_account_object_element_position)
                        elif object_type == 'http_signature':
                            create_protocol_filed_code = create_protocol_filed.create(protocol_field_data[x], test_http_signature_object_element_position)
                        else:
                            create_protocol_filed_code = 200
                        if create_protocol_filed_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_type), flush=True)
                        elif create_protocol_filed_code != 200:
                            result = "Fail to create {}.".format(object_type)
                            break
                # 创建rule
                if create_ip_code == 200:
                    create_rule = CreateRule(driver)
                    create_rule_code = create_rule.create(test_data, test_rule_element_position)
                    if create_rule_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create security rule successfully.", flush=True)
                    elif create_rule_code != 200:
                        ui_result = "Fail to create security rule."

                # 触发流量验证
                if create_rule_code == 200:
                    search_rule = SearchRule(driver)
                    search_rule_code, rule_id = search_rule.get_rule_id(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
                    if search_rule_code == 200:
                        # rule_id = search_rule.get_rule_id()
                        test_data["rule_id"] = rule_id
                        verification = Verify()
                        verification_result = verification.verify_result(driver, parameter, test_data, [], test_rule_element_position)
                        if len(verification_result) == 4:
                            driver = verification_result[3]
                        elif len(verification_result) == 5:
                            driver = verification_result[4]

                # 分析验证结果，并返回给flask
                if len(verification_result) != 0:
                    analysis = Analyse()
                    ui_result = analysis.analyse_result(test_data, [], verification_result)

                # 删除rule
                if create_rule_code == 200:
                    search_rule = SearchRule(driver)
                    search_rule_code, first_row_checkbox_element = search_rule.search(test_data["policy_type"], test_data["rule_name"], test_rule_element_position)
                    if search_rule_code == 200:
                        delete_rule = DeleteRule(driver)
                        delete_rule_code = delete_rule.delete(test_rule_element_position, first_row_checkbox_element, True)
                        if delete_rule_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete security rule successfully.", flush=True)
                        elif delete_rule_code != 200:
                            ui_result = ui_result + " In addition, fail to delete security rule."
                    else:
                        ui_result = ui_result + " In addition, fail to search security rule."

                # 删除response profile
                if delete_rule_code == 200 and "action_parameter" in test_data.keys():
                    # 删除
                    for prfi_key, prfi_value in (test_data["action_parameter"].items()):  # 遍历所有cond数据
                        if prfi_key in manipulation_profile_no_create_list:
                            continue  # 直接跳过
                        prfi_status = 0
                        prfi_key_out = prfi_key.replace("_", " ")
                        if len(prfi_value) != 0:  # 不为空
                            for i in range(len(prfi_value)):  # 遍历查询所有profile
                                search_prfi = SearchProfile(driver)
                                element_position_map = get_element_position(prfi_key)
                                prfi_name = prfi_value[i]["profile_file"]["name"].strip()
                                search_prfi_code, first_row_checkbox_element = search_prfi.search(prfi_name, element_position_map)
                                if search_prfi_code == 200:
                                    delete_prfi = DeleteProfile(driver)
                                    delete_prfi_code = delete_prfi.delete(element_position_map, first_row_checkbox_element, True)
                                    if delete_prfi_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} profile successfully.".format(prfi_key_out), flush=True)
                                    else:
                                        result = result + " In addition, fail to delete {} profile.".format(prfi_key_out)
                                        break
                                else:
                                    result = result + " In addition, fail to search {} profile.".format(prfi_key_out)
                                    break
                                # 退出遍历标志
                                if prfi_status == 1:  # 失败，退出遍历创建
                                    break
                        # 退出遍历标志
                        if prfi_status == 1:  # 失败，退出遍历创建
                            break
                #删除dns profile
                delete_rule_code = 200
                profile_data = test_data["profile"]
                if delete_rule_code == 200:
                    for x in range(len(profile_data)):
                        search_dns_records_profile = SearchProfile(driver)
                        profile_return_code,first_row_checkbox_element=search_dns_records_profile.search(profile_data[x]['name'],test_dns_records_profile_element_position)
                        if profile_return_code == 200:
                            delete_mirror_profile = DeleteProfile(driver)
                            delete_profile_code = delete_mirror_profile.delete(test_dns_records_profile_element_position,first_row_checkbox_element,True)
                            if delete_profile_code == 200:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete dns records profile successfully.", flush=True)
                            elif delete_profile_code != 200:
                                result = result + " In addition, fail to delete profile."
                                break
                        else:
                            result = result + " In addition, fail to search profile."
                            break
                # 删除object
                if delete_rule_code == 200:
                    # 删除ip
                    for ip_key in ["source_ip", "external_ip", "internal_ip"]:
                        if ip_key in test_data["condition"] and len(test_data["condition"][ip_key]) != 0:
                            for x in range(len(ip_data)):
                                search_ip = SearchObject(driver)
                                search_ip_code, first_row_checkbox_element = search_ip.search(ip_data[x]["name"], test_ip_object_element_position)
                                if search_ip_code == 200:
                                    delete_ip = DeleteObject(driver)
                                    delete_ip_code = delete_ip.delete(test_ip_object_element_position, first_row_checkbox_element, True)
                                    if delete_ip_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete ip object successfully.", flush=True)
                                    elif delete_ip_code != 200:
                                        ui_result = ui_result + " In addition, fail to delete ip object."
                                        break
                                else:
                                    ui_result = ui_result + " In addition, fail to search ip object."
                                    break

                    # 删除port
                    for port_key in ["internal_port", "destination_port", "external_port"]:
                        if port_key in test_data["condition"] and len(test_data["condition"][port_key]) != 0:
                            for x in range(len(ip_data)):
                                search_port = SearchObject(driver)
                                search_port_code, first_row_checkbox_element = search_port.search(ip_data[x]["name"], test_port_object_element_position)
                                if search_port_code == 200:
                                    delete_port = DeleteObject(driver)
                                    delete_port_code = delete_port.delete(test_port_object_element_position, first_row_checkbox_element, True)
                                    if delete_port_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete port object successfully.", flush=True)
                                    elif delete_port_code != 200:
                                        ui_result = ui_result + " In addition, fail to delete port object."
                                        break
                                else:
                                    ui_result = ui_result + " In addition, fail to search port object."
                                    break
                    if len(test_data["condition"]["server_fqdn"]) != 0:
                        # 删除fqdn
                        for x in range(len(fqdn_data)):
                            search_fqdn = SearchObject(driver)
                            search_fqdn_code, first_row_checkbox_element = search_fqdn.search(fqdn_data[x]["name"], test_fqdn_object_element_position)
                            if search_fqdn_code == 200:
                                delete_fqdn = DeleteObject(driver)
                                delete_fqdn_code = delete_fqdn.delete(test_fqdn_object_element_position, first_row_checkbox_element, True)
                                if delete_fqdn_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete fqdn object successfully.", flush=True)
                                elif delete_fqdn_code != 200:
                                    result = result + " In addition, fail to delete fqdn object."
                                    break
                            else:
                                result = result + " In addition, fail to search fqdn object."
                                break
                    if "protocol_filed" in test_data["condition"] and len(test_data["condition"]["protocol_filed"]) != 0:
                        object_positions = {
                            'url': test_url_object_element_position,
                            'http_signature': test_http_signature_object_element_position,
                            'fqdn': test_fqdn_object_element_position,
                            'keywords': test_keywords_object_element_position,
                            'account': test_account_object_element_position
                        }
                        # protocol_filed
                        for q in range(len(protocol_field_data)):
                            object_type = protocol_field_data[q]['object_type']
                            if object_type != 'boolean':
                                search_protocol_filed = SearchObject(driver)
                                if object_type in object_positions:
                                    search_protocol_filed_code, first_row_checkbox_element = search_protocol_filed.search(
                                        protocol_field_data[q]["name"], object_positions[object_type]
                                    )

                                    if search_protocol_filed_code == 200:
                                        delete_protocol_filed = DeleteObject(driver)

                                        delete_protocol_filed_code = delete_protocol_filed.delete(
                                            object_positions[object_type], first_row_checkbox_element, True
                                        )

                                        if delete_protocol_filed_code == 200:
                                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(object_type), flush=True)
                                        else:
                                            result += " In addition, fail to delete {} object.".format(object_type)
                                            break
                                else:
                                    result = result + " In addition, fail to search {} object.".format(object_type)
                                    break
                    # 删除device相关的object
                    if "device" in test_data["condition"] and len(test_data["condition"]["device"]) != 0:
                        for y in range(len(device_data)):
                            search_device = SearchObject(driver)
                            object_sub_type = device_data[i]['item'][0]['item_type']
                            if object_sub_type == 'imsi':
                                search_device_code, first_row_checkbox_element = search_device.search(device_data[y]["name"], test_imsi_object_element_position)
                            elif object_sub_type == 'phone_number':
                                search_device_code, first_row_checkbox_element = search_device.search(device_data[y]["name"], test_phone_number_object_element_position)
                            if search_device_code == 200:
                                delete_device = DeleteObject(driver)
                                if object_sub_type == 'imsi':
                                    delete_device_code = delete_device.delete(test_imsi_object_element_position, first_row_checkbox_element, True)
                                elif object_sub_type == 'phone_number':
                                    delete_device_code = delete_device.delete(test_phone_number_object_element_position, first_row_checkbox_element, True)
                                if delete_device_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(object_sub_type), flush=True)
                                elif delete_device_code != 200:
                                    result = result + " In addition, fail to delete {} object.".format(object_sub_type)
                                    break
                            else:
                                result = result + " In addition, fail to search {} object.".format(object_sub_type)
            finally:
                # 清理环境
                result["ui_result"] = ui_result
                support.ui_utils.env.teardown()
        
        if parameter["script_type"] == "api" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run api test case", flush=True)

                parameter["script_type"] = "api"

                # 数据转换，适配API的test_data
                if test_data["rule_num"] == 1:
                    translation = DataTranslation()
                    test_data = translation.data_translation(parameter, test_data)

                self.api_name_list = get_name_list(test_data)
                # 添加测试过程中涉及的template
                template_path = {}
                template_path["rule_template"] = parameter["root_path"] + "/support/api_utils/template/rule_template.json"
                template_path["object_template"] = parameter["root_path"] + "/support/api_utils/template/object_template.json"
                template_path["profile_dns_record_template"] = parameter["root_path"] + "/support/api_utils/template/profile_dns_record_template.json"
                # 添加测试过程中涉及的response pages
                if "profile_condition" in test_data and len(test_data["profile_condition"]) > 0:
                    tmp_dir = parameter["root_path"] + "/support/ui_utils/profile/profile_file/"
                    profile_type = test_data["profile_condition"][0]["profile_type"].strip()
                    if profile_type == "response_page":
                        template_path["profiles_deny_path"] = tmp_dir + "response_pages/" + test_data["profile_condition"][0]["content_name"]

                # 创建Object、Profile、Rule
                create = CreatePolicy()
                cfg_list = create.create_policy(parameter, test_data, template_path)

                # 流量验证
                verification = Verify()
                verification_result = verification.verify_result("", parameter, test_data, cfg_list, "")

                # 分析验证结果，并返回给flask
                analysis = Analyse()
                api_result = analysis.analyse_result(test_data, cfg_list, verification_result)
            finally:
                result["api_result"] = api_result
                # 删除配置
                delete = DeletePolicy()
                delete.delele_policy_by_cfg(token, parameter, cfg_list)
    
        return result

    def delete_data(self):
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.ui_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        if isinstance(self.api_name_list, list) and self.api_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)
            
if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "script_type": "api",
        "env": "tsgx",
        "vsys_id": 5,
        "is_log": 1,
        "debug_flag": "local",
        "root_path": "D:/Document/Project-TSG/Code/git/tsg_test",
        "path": "D:/Document/Project-TSG/Code/git/tsg_test/tests/api",
        "module_name": "dos_protection",
        "test_case_name": "dos_protect_srcip_http_rate_srcip_d3"
    }