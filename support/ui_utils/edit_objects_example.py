# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.general_ui_utils.object.edit_objects_temp import EditObjects
from support.general_ui_utils.object.search_objects import SearchObjects
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime


class EditObjectsExample:
    def edit_objects(self, objects_tuple,first_row_checkbox_element,object_configuration, driver):
        try:
            for obj in objects_tuple:
                # 删除object
                search_object = SearchObjects(driver)
                element_position_map = get_element_position(obj["type"])
                search_object_code, first_row_checkbox_element = search_object.get_first_object(obj["uuid"],element_position_map)
                if search_object_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Search {} object successfully.".format(obj["type"], flush=True))
                    edit_objects = EditObjects(driver)
                    edit_object_code = edit_objects.edit(object_configuration, element_position_map,first_row_checkbox_element)
                    if edit_object_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit {} object successfully.".format(obj["type"], flush=True))
                    elif edit_object_code != 200:
                        result = "Fail to create {} rule.".format(obj["type"])
                        return "", "", result
                elif search_object_code == 200:
                    result = "Fail to search {} rule uuid.".format(obj["type"])
                    return "", "", result

        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"When creating rule by ui, the exception error: ", str(e), flush=True)
            return "", "When creating rule by ui, the exception error: " + str(e)
