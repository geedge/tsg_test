import time
import pytest
import os
from datetime import datetime
import support.ui_utils.env
from datetime import datetime

from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.log_in import *
from support.general_ui_utils.object.create_objects import CreateObjects
from support.general_ui_utils.object.edit_objects import EditObjects
from support.general_ui_utils.object.search_objects import SearchObjects
from support.general_ui_utils.object.delete_objects import DeleteObjects
from support.general_ui_utils.element_position.object_element_position import *
from support.instance_utils.case_instance_generator import CaseInstanceGenerator
from support.report_update import ReportUpdate


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run test case: " + parameter["test_case_name"], flush=True)
        #参数初始化
        result,exception_result = "",""

        #脚本启动时间
        start_time = time.time()

        #测试数据
        test_data =  {
            "type": "objects",
            "case_type": "group",
            "name": "create_ip_group_and_add_item",
            "object_type": "ip",
            "sub_object": 1,
            "object_operation":{
                "create": [
                    {
                        "item_operation": "add",
                        "item_type": "",
                        "item_value": ["1.1.1.1"]
                    }
                ],
                "edit":[
                    {
                        "item_operation": "add",
                        "item_type": "",
                        "item_value": ["1.1.1.1-1.1.1.1"]
                    }
                ]
            },
            "search": {
                "is_fuzzy": False,
                "type": "name"
            },
            "statistics": "",  # random
            "audit_log": False  # system
        }

        test_ip_object_element_position = {
            "page_jump": {
                "mainPage_navigationBar_logo_posCss": mainPage_navigationBar_logo_posCss,
                "mainPage_currentPage_vsysName_posXpath": mainPage_currentPage_vsysName_posXpath,
                "mainPage_button_menu_posXCss": mainPage_button_menu_posXCss,
                "mainPage_policyFirstLevelMenu_posId": mainPage_firstLevelMenu_Objects_posId,
                "mainPage_policySecondLevelMenu_posId": mainPage_secondLevelMenu_ipAddress_posId
            },
            "create": {
                "objectListPage_createButton_posId": listPage_object_ip_address_createButton_posId,
                "objectListPage_dropDown_createGroupButton_posId":listPage_object_ip_address_create_ip_address_Group_Button_posId,
                "objectListPage_dropDown_createButton_posId":listPage_object_ip_address_create_ip_address_Button_posId,
                "objectPage_inputName_posXpath": ip_addressObjectPage_input_Name_posXpath,
                "objectPage_inputDescription_posXpath":ip_addressObjectPage_textArea_Description_posXpath,
                "objectPage_ipType_posId": ipObjectPage_ipType_posId,
                "objectPage_addItem_posXpath": ip_address_Group_sub_Object_add_new_add_item_Button_posXpath,
                "objectPage_inputItem_posXpath": ip_address_Group_sub_Object_add_new_addIP_item_inputName_posXpath,
                "objectPage_button_saveItem_posXpath": ip_addressObjectPage_button_Save_Item_posXpath,
                "objectPage_okButton_posXpath": ip_addressObjectPage_button_OK_posXpath,
                "objectPage_okButton_warningYes_posXpath": ip_addressObjectPage_button_warningSaveYes_posXpath,
                "groupObjectPage_addSubordinate_posXpath":ip_address_Group_sub_Object_addButton_posXpath,
                "groupObjectPage_subObject_OK_button_posXpath":ip_address_Group_sub_Object_add_new_one_OK1_Button_posXpath,
                "groupObjectPage_subObject_OK_Warning_Yes_posXpath":ip_address_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath
            },
            "edit":{
                "objectPage_Group_edit_subObject_Button_posXpath":ip_address_Group_sub_Object_edit_subObject_Button_posXpath,
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

        # 测试用例实例化
        case_instance_generator = CaseInstanceGenerator(test_data, parameter)
        result = case_instance_generator.run()

    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,flush=True)
        return "Error: " + str(e)
    finally:
        # 清理环境并删除配置
        case_instance_generator.delete_data()
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)

if __name__ == '__main__':
    parameter = {
        "username": "auto_ui_yzj",
        "password": "auto_ui_yzj",
        "test_pc_ip": "192.168.64.28",
        "test_subcriber_id": "",
        "api_server": "http://192.168.44.72",
        "script_type": "ui",
        "env": "tsgx",
        "vsys_id": 2,
        "is_log": 0,
        "root_path": "D:/PycharmProjects/tsg_test",
        "path": "D:/PycharmProjects/tsg_test/tests/ui",
        "module_name": "",
        "test_case_name": "create_table_traffic_spectrum"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """