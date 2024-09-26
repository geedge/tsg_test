import time
import pytest
import os
from datetime import datetime
import support.ui_utils.env
from datetime import datetime

from support.api_utils.delete_policy import DeletePolicy
from support.api_utils.log_in import *
from support.general_ui_utils.object.create_objects import CreateObjects
from support.general_ui_utils.object.search_objects import SearchObjects
from support.general_ui_utils.object.delete_objects import DeleteObjects
from support.general_ui_utils.element_position.object_element_position import *
from support.report_update import ReportUpdate


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run test case: " + parameter["test_case_name"], flush=True)
        #参数初始化
        result,exception_result = "",""

        #脚本启动时间
        start_time = time.time()

        # 环境初始化
        support.ui_utils.env.initiate_selenium_request()
        driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()

        #测试数据
        test_data =  {
            "name": "create_ip_object",
            "object_type": "ip",
            "fuzzy_search": False,
            "search_type": "id",
            "item": [
                {
                    "item_operation": "new",
                    "item_type": "",
                    "item_value": ["1.1.1.1","1.1.1.1-1.1.1.1","192.168.2.1/24","1:1:1::1/24","94E5:E27A::6041"]
                }
            ]
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
                "objectListPage_dropDown_createButton_posId":listPage_object_ip_address_create_ip_address_Button_posId,
                "objectPage_inputName_posXpath": ip_addressObjectPage_input_Name_posXpath,
                "objectPage_inputDescription_posXpath":ip_addressObjectPage_textArea_Description_posXpath,
                "objectPage_ipType_posId": ipObjectPage_ipType_posId,
                "objectPage_addItem_posXpath": ip_addressObjectPage_button_addItem_posXpath,
                "objectPage_inputItem_posXpath": ip_addressObjectPage_button_inputItem_posXpath,
                "objectPage_button_saveItem_posXpath": ip_addressObjectPage_button_Save_Item_posXpath,
                "objectPage_okButton_posXpath": ip_addressObjectPage_button_OK_posXpath,
                "objectPage_okButton_warningYes_posXpath": ip_addressObjectPage_button_warningSaveYes_posXpath
            },
            "delete": {
                "objectListPage_deleteButton_posId": listPage_object_ip_address_delButton_posId,
                "objectListPage_deleteButton_warningYes_posXpath": listPage_object_ip_address_del_yes_Button_posXpath
            }
        }

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token

        name_list = [
            {
                "name": "create_ip_object",
                "type": "ip",
            }
        ]

        #创建object
        create_ip_object = CreateObjects(driver)
        create_port_code = create_ip_object.create(test_data,test_ip_object_element_position)
        object_info = create_ip_object.object_info
        if create_port_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                  "Create ip object successfully.", flush=True)
        elif create_port_code != 200:
            result = "Fail to create ip."

        #搜索object
        search_ip = SearchObjects(driver)
        search_ip_code,first_row_checkbox_element = search_ip.search(object_info,test_data,test_ip_object_element_position)
        if search_ip_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                  "Search ip object successfully.", flush=True)
        elif create_port_code != 200:
            result = "Fail to search ip."

        # 删除bject
        delete_ip = DeleteObjects(driver)
        delete_ip_code = delete_ip.delete(test_ip_object_element_position,first_row_checkbox_element)
        if delete_ip_code == 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Delete ip object successfully.", flush=True)
        elif delete_ip_code != 200:
            result = result + " In addition, fail to delete ip object."

    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e,flush=True)
        return "Error: " + str(e)
    finally:
        #清理环境
        support.ui_utils.env.teardown()
        delete = DeletePolicy()
        delete.delete_policy_by_name(token, parameter, name_list)
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