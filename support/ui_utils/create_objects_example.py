# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.general_ui_utils.object.create_objects_temp import CreateObjects
from support.general_ui_utils.object.search_objects import SearchObjects
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime

class CreateObjectsExample:
    def create_objects(self, object_configuration, driver):
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run ui test case", flush=True)

            result = ""
            object_uuids_list = []
            object_uuids_temp_dict = {}

            for object in object_configuration["or_conditions"]:
                #获取当前所需的element
                if "sub_type" in object.keys():
                    object_type = object["sub_type"]
                else:
                    object_type = object["type"]
                element_position_library = get_element_position(object_type)
                #执行创建操作
                create_objects = CreateObjects(driver)
                created_object_code = create_objects.create(object, element_position_library)
                if created_object_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object["type"], flush=True))
                elif created_object_code != 200:
                    result = "Fail to create {} rule.".format(object_configuration["type"])
                    return "", "", result

                search_objects = SearchObjects(driver)
                element_position_library = get_element_position(object_type)
                searched_object_code, object_uuid, object_description = search_objects.get_object_uuid(object["name"], element_position_library)
                if searched_object_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Search {} object successfully.".format(object["type"], flush=True))
                elif searched_object_code == 200:
                    result = "Fail to search {} rule uuid.".format(object_configuration["type"])
                    return "", "", result

                object_uuids_temp_dict["type"] = object["type"]
                object_uuids_temp_dict["uuid"] = object_uuid
                object_uuids_temp_dict["name"] = object["name"]
                object_uuids_temp_dict["description"] = object_description
                object_uuids_list.append(object_uuids_temp_dict)
                rule_uuids_tuple = tuple(object_uuids_list)

            return rule_uuids_tuple,result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating object by ui, the exception error: ", str(e), flush=True)
            return "", "When creating object by ui, the exception error: " + str(e)
