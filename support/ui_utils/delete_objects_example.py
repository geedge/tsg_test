# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.api_utils.log_in import LogIn
from support.api_utils.delete_objects import DeleteObjects as DeleteObjectsAPI
from support.general_ui_utils.object.search_objects import SearchObjects
from support.general_ui_utils.object.delete_objects import DeleteObjects
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime

class DeleteObjectsExample:
    def delete_objects(self, parameter, objects_tuple, driver):
        result = ""
        for obj in objects_tuple:
            # 删除object
            search_object = SearchObjects(driver)
            element_position_map = get_element_position(obj["type"])
            search_object_code, first_row_checkbox_element = search_object.get_first_object(obj["uuid"],element_position_map)
            if search_object_code == 200:
                delete_Object = DeleteObjects(driver)
                delete_object_code = delete_Object.delete(element_position_map,first_row_checkbox_element)
                if delete_object_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Delete {} object successfully.".format(obj["type"]), flush=True)
                elif delete_object_code != 200:
                    result = result + " In addition, fail to delete {} object.".format(obj["type"])
            else:
                result = result + " In addition, fail to search {} object.".format(obj["type"])
        # 环境清理
        support.ui_utils.env.teardown()
        # 强制删除
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        headers = {"Content-Type": "application/json", "Authorization": token}
        objects = DeleteObjectsAPI(parameter, headers)
        objects.delete_objects(objects_tuple)
        return result
