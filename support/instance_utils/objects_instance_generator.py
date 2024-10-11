import time
import pytest
import os
from datetime import datetime
import support.ui_utils.env

from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.log_in import *
from support.general_ui_utils.object.create_objects import CreateObjects
from support.general_ui_utils.object.edit_objects import EditObjects
from support.general_ui_utils.object.search_objects import SearchObjects
from support.general_ui_utils.object.delete_objects import DeleteObjects
from support.general_ui_utils.object.detail_audit_log_check import AuditLogCheck
from support.general_ui_utils.object.view_statistics_page import ViewStatisticsPage
from support.general_ui_utils.object.export_objects import ExportObjects
from support.general_ui_utils.object.system_audit_log_check import SystemAuditLogCheck
from support.general_ui_utils.element_position.object_element_position import *
from support.general_ui_utils.preset_file.preset_object_create import PresetObjectCreate
from support.report_update import ReportUpdate

class ObjectsInstanceGenerator:

    def __init__(self,test_data,parameter):
        self.test_data = test_data
        self.parameter = parameter
        self.object_exit = False

    def run(self):
        ui_result = self._run(self.test_data,self.parameter)
        return ui_result

    def _run(self,test_data,parameter):
        ui_result, api_result = "", ""
        self.api_name_list, self.ui_name_list = [], []
        object_element_position = {}
        result = {
            "ui_result": "",
            "api_result": ""
        }

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        self.test_data["token"] = token

        # 环境初始化
        support.ui_utils.env.initiate_selenium_request()
        driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()
        tmp_name_dict = {}
        tmp_name_dict["type"] = test_data["object_type"]
        tmp_name_dict["name"] = test_data["name"]
        self.ui_name_list.append(tmp_name_dict)

        test_ip_object_element_position = {
            "page_jump": {
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_ipAddress_posId
            },
            "create": {
                "objectPage_ipType_posId": ipObjectPage_ipType_posId,
                "objectListPage_createButton_posId": listPage_object_ip_address_createButton_posId,
                "objectListPage_dropDown_createButton_posId": listPage_object_ip_address_create_ip_address_Button_posId,
                "objectPage_inputName_posXpath": ip_addressObjectPage_input_Name_posXpath,
                "objectPage_inputDescription_posXpath": ip_addressObjectPage_textArea_Description_posXpath,
                "objectPage_addItem_posXpath": ip_addressObjectPage_button_addItem_posXpath,
                "objectPage_inputItem_posXpath": ip_addressObjectPage_button_inputItem_posXpath,
                "objectPage_button_saveItem_posXpath": ip_addressObjectPage_button_Save_Item_posXpath,
                "objectPage_okButton_posXpath": ip_addressObjectPage_button_OK_posXpath,
                "objectPage_okButton_warningYes_posXpath": ip_addressObjectPage_button_warningSaveYes_posXpath,
                "objectPage_importItem_posXpath": main_button_import_files_button_posXpath,
                "importPage_uploadFile_posXpath": main_ObjectPage_Input_path_Import_files_posXpath,
                "objectPage_import_ok_button_posXpath": main_ObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath,
                "objectPage_addItem_error_tips_posXpath":ip_addressObjectPage_addItem_error_tips_posXpath,
                "error_tips_text":"IP format error",
                "objectListPage_dropDown_createGroupButton_posId":listPage_object_ip_address_create_ip_address_Group_Button_posId,
                "objectGroupPage_addItem_posXpath":ip_address_Group_sub_Object_add_new_add_item_Button_posXpath,
                "objectGroupPage_inputItem_posXpath":ip_address_Group_sub_Object_add_new_addIP_item_inputName_posXpath,
                "groupObjectPage_addSubordinate_posXpath": ip_address_Group_sub_Object_addButton_posXpath,
                "groupObjectPage_subObject_OK_button_posXpath": ip_address_Group_sub_Object_add_new_one_OK1_Button_posXpath,
                "groupObjectPage_subObject_OK_Warning_Yes_posXpath": ip_address_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath
            },
            "edit": {
                "objectPage_Group_edit_subObject_Button_posXpath": ip_address_Group_sub_Object_edit_subObject_Button_posXpath,
                "objectListPage_editButton_posId": listPage_object_ip_address_editButton_posId,
                "objectPage_editItem_Button_posXpath": ip_addressObjectPage_button_editItem_posXpath,
                "objectPage_Item_text_posXpath": ip_addressObjectPage_button_ip_text_posXpath,
                "objectPage_editItem_Save_Button_posXpath": ip_addressObjectPage_button_add_itemIP_Save_posXpath,
                "objectPage_addItem_first_item_posXpath": ip_addressObjectPage_button_addItem_first_item_posXpath,
            },
            "delete": {
                "objectListPage_deleteButton_posId": listPage_object_ip_address_delButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": listPage_object_ip_address_del_yes_Button_posXpath
            }
        }

        test_ip_learning_object_element_position = {
            "page_jump": {
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_ipAddress_posId
            },
            "create":{
                "objectPage_ipLearing_type_posId": ip_addressObjectPage_radioButton_IP_learning_posId,
                "objectListPage_createButton_posId": listPage_object_ip_address_createButton_posId,
                "objectListPage_dropDown_createButton_posId": listPage_object_ip_address_create_ip_address_Button_posId,
                "objectPage_inputName_posXpath": ip_addressObjectPage_input_Name_posXpath,
                "objectPage_inputDescription_posXpath": ip_addressObjectPage_textArea_Description_posXpath,
                "objectPage_addItem_posXpath": ip_addressObjectPage_button_addItem_posXpath,
                "objectPage_inputItem_posXpath": ip_addressObjectPage_IP_learning_inputItem_posXpath,
                "objectPage_button_saveItem_posXpath": ip_addressObjectPage_button_Save_Item_posXpath,
                "objectPage_okButton_posXpath": ip_addressObjectPage_button_OK_posXpath,
                "objectPage_okButton_warningYes_posXpath": ip_addressObjectPage_button_warningSaveYes_posXpath,
                "objectPage_addItem_error_tips_posXpath": ip_addressObjectPage_addItem_error_tips_posXpath,
                "error_tips_text": "Format error"
            },
            "edit": {
                "objectListPage_editButton_posId": listPage_object_ip_address_editButton_posId,
                "objectPage_editItem_Button_posXpath": ip_addressObjectPage_button_editItem_posXpath,
                "objectPage_Item_text_posXpath": ip_addressObjectPage_button_ip_learing_text_posXpath,
                "objectPage_editItem_Save_Button_posXpath": ip_addressObjectPage_button_add_itemIP_Save_posXpath,
                "objectPage_addItem_first_item_posXpath": ip_addressObjectPage_button_addItem_first_item_posXpath,
            },
            "delete": {
                "objectListPage_deleteButton_posId": listPage_object_ip_address_delButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": listPage_object_ip_address_del_yes_Button_posXpath
            }
        }

        if test_data["object_type"] == "ip":
            object_element_position = test_ip_object_element_position
        elif test_data["object_type"] == "ip_learning":
            object_element_position = test_ip_learning_object_element_position

        need_initialization = False
        if len(parameter["script_type"]) == 0:
            need_initialization = True

        if parameter["script_type"] == "ui" or need_initialization == True:
            if self.test_data["case_type"] == "single":
                for index in range(len(test_data["object_operation"]["create"])):
                    # 创建object
                    create_ip_object = CreateObjects(driver)
                    create_port_code = create_ip_object.create(test_data,index, object_element_position)
                    object_info = create_ip_object.object_info
                    self.object_exit = object_info["object_exit"]
                    if create_port_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create object successfully.", flush=True)
                    elif create_port_code != 200:
                        ui_result = "Fail to create ip."


                search_ip = SearchObjects(driver)
                # 判断当前用例是否需要进行view点击的statistics页面校验
                if test_data["statistics"] != "" and create_ip_object.object_info["object_exit"] == True:
                    search_ip_code, first_row_checkbox_element = search_ip.search(object_info, test_data,object_element_position)
                    if search_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Search object successfully.", flush=True)
                    elif create_port_code != 200:
                        ui_result = "Fail to search ip."
                    view_statistics = ViewStatisticsPage(driver)
                    view_statistics_code = view_statistics.view_statistics_check(test_data["statistics"],object_element_position,first_row_checkbox_element)
                    if view_statistics_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"view statistics button click successfully.", flush=True)
                    elif view_statistics_code != 200:
                        ui_result = "Fail to view statistics button click check"

                # 校验审计日志创建Object
                audit_log = AuditLogCheck(driver)
                if test_data["object_operation"]["create"][0]["item_operation"] == "add":
                    object_info["operation"] = "Create"
                elif test_data["object_operation"]["create"][0]["item_operation"] == "import":
                    object_info["operation"] = "Import"
                search_ip_code, first_row_checkbox_element = search_ip.search(object_info, test_data,object_element_position)
                audit_log_code = audit_log.audit_log_check(object_info, object_element_position,first_row_checkbox_element)
                if audit_log_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create object audit log check successfully.", flush=True)
                elif audit_log_code != 200:
                    ui_result = "Fail to create audit log check"

                if "edit" in test_data["object_operation"].keys():
                    # object编辑修改操作
                    for index in range(len(test_data["object_operation"]["edit"])):
                        search_ip_code, first_row_checkbox_element = search_ip.search(object_info, test_data,object_element_position)
                        if search_ip_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Search object successfully.", flush=True)
                        elif create_port_code != 200:
                            ui_result = "Fail to search ip."
                        edit_ip = EditObjects(driver)
                        edit_ip_code = edit_ip.edit(test_data,index,object_element_position, first_row_checkbox_element)
                        if edit_ip_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit object successfully.", flush=True)
                        elif edit_ip_code != 200:
                            ui_result = ui_result + " In addition, fail to edit ip object."

                        # 校验修改完成后的审计日志查看
                        if test_data["object_operation"]["edit"][index]["item_operation"] == "import":
                            object_info["operation"] = "Import"
                        else:
                            object_info["operation"] = "Edit"
                        audit_log_code = audit_log.audit_log_check(object_info, object_element_position,first_row_checkbox_element)
                        if audit_log_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit object audit log check successfully.", flush=True)
                        elif audit_log_code != 200:
                            ui_result = "Fail to Edit ip object audit log check"

                #判断是否为正常创建object,如item异常校验等未保存object无需删除
                if object_info["object_exit"] == True:
                    # 删除object
                    search_ip_code, first_row_checkbox_element = search_ip.search(object_info, test_data,object_element_position)
                    if search_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Search  object successfully.", flush=True)
                    elif create_port_code != 200:
                        ui_result = "Fail to search ip."

                    if "export" in test_data["object_operation"]:
                        export_object = ExportObjects(driver)
                        export_object_code = export_object.export_objects(object_info,first_row_checkbox_element)
                        if export_object_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Export object successfully.", flush=True)
                        elif create_port_code != 200:
                            ui_result = "Fail to export ip."

                    delete_ip = DeleteObjects(driver)
                    delete_ip_code = delete_ip.delete(object_element_position, first_row_checkbox_element)
                    if delete_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Delete object successfully.", flush=True)
                    elif delete_ip_code != 200:
                        ui_result = ui_result + " In addition, fail to delete ip object."

                if test_data["audit_log"] == True:
                    system_audit_log =SystemAuditLogCheck(driver)
                    system_audit_log_code = system_audit_log.system_audit_log_check(test_data,object_info)
                    if system_audit_log_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"System audit log verify successfully.", flush=True)
                    elif system_audit_log_code != 200:
                        ui_result = ui_result + " In addition, fail to System audit log verify."

            elif self.test_data["audit_log"] == True:
                pass

            elif self.test_data["case_type"] == "group":
                #若为多层嵌套，预先创建object
                if test_data["sub_object"] > 1:
                    preset_object = PresetObjectCreate(driver)
                    preset_object_code = preset_object.create(test_data["object_type"], object_element_position)
                    if preset_object_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                              "Create preset object successfully.", flush=True)
                    elif preset_object_code != 200:
                        ui_result = "Fail to create preset object."

                # 创建object
                for index in range(len(test_data["object_operation"]["create"])):
                    create_ip_object = CreateObjects(driver)
                    create_object_code = create_ip_object.create_group(test_data,index,object_element_position)
                    object_info = create_ip_object.object_info
                    self.object_exit = object_info["object_exit"]
                    if create_object_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                              "Create ip object successfully.", flush=True)
                    elif create_object_code != 200:
                        ui_result = "Fail to create ip."

                # 校验审计日志创建Object
                search_ip = SearchObjects(driver)
                search_ip_code, first_row_checkbox_element = search_ip.search(object_info, test_data,object_element_position)
                if search_ip_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Search ip object successfully.", flush=True)
                elif search_ip_code != 200:
                    ui_result = "Fail to search ip."

                audit_log = AuditLogCheck(driver)


                if test_data["object_operation"]["create"][0]["item_operation"] == "add" or test_data["object_operation"]["create"][0]["item_operation"] == "quote":
                    object_info["operation"] = "Create"
                elif test_data["object_operation"]["create"][0]["item_operation"] == "import":
                    object_info["operation"] = "Import"

                audit_log_code = audit_log.audit_log_check(object_info, object_element_position,first_row_checkbox_element)
                if audit_log_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create object audit log check successfully.", flush=True)
                elif audit_log_code != 200:
                    ui_result = "Fail to create audit log check"

                if "edit" in test_data["object_operation"].keys():
                    # object编辑修改操作
                    for index in range(len(test_data["object_operation"]["edit"])):
                        search_ip_code, first_row_checkbox_element = search_ip.search(object_info, test_data,object_element_position)
                        if search_ip_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Search ip object successfully.", flush=True)
                        elif search_ip_code != 200:
                            ui_result = "Fail to search ip."
                        edit_ip = EditObjects(driver)
                        edit_ip_code = edit_ip.edit_group(test_data,index, object_element_position, first_row_checkbox_element)
                        if edit_ip_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit ip object successfully.", flush=True)
                        elif edit_ip_code != 200:
                            ui_result = ui_result + " In addition, fail to edit ip object."

                # 删除object
                for i in range(test_data["sub_object"] + 1):
                    search_ip_code, first_row_checkbox_element = search_ip.search(object_info, test_data,object_element_position)
                    if search_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Search ip object successfully.", flush=True)
                    elif search_ip_code != 200:
                        ui_result = "Fail to search ip."

                    delete_ip = DeleteObjects(driver)
                    delete_ip_code = delete_ip.delete(object_element_position, first_row_checkbox_element)
                    if delete_ip_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                              "Delete ip object successfully.", flush=True)
                    elif delete_ip_code != 200:
                        ui_result = ui_result + " In addition, fail to delete ip object."

            elif self.test_data["case_type"] == "multiple":
                pass

            result["ui_result"] = ui_result

        if parameter["script_type"] == "api" or need_initialization == True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run api test case", flush=True)

            parameter["script_type"] = "api"

            self.api_name_list = []

            "todo api 集成"

        return result

    def delete_data(self):
        # 清理环境
        support.ui_utils.env.teardown()
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.object_exit == True:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        # if isinstance(self.api_name_list, list):
        #     delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)