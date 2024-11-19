# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.general_ui_utils.object.create_objects_temp import CreateObject
from support.general_ui_utils.object.search_objects import SearchObjects
from support.ui_utils.element_position.map_element_position_library import *
from datetime import datetime


class CreateObjectsExample:
    def create_objects(self, policy_configuration, driver):
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run ui test case", flush=True)

            result = ""

            # if "condition" in policy_configuration.keys():
            #     for cond_key, cond_value in (policy_configuration["condition"].items()):
            #         cond_status = 0
            #         if cond_key == "application":
            #             continue  # 直接跳过
            #         cond_key_out = cond_key.replace("_", " ")
            #         if len(cond_value) != 0:  # 不为空
            #             cond_data = cond_value
            #             create_ip = CreateObject(driver)
            #             for i in range(len(cond_data)):  # 遍历创建所有condition
            #                 if cond_key == "protocol_filed":
            #                     tmp_key = cond_data[i]["object_type"]
            #                     if tmp_key == "boolean":  # "object_type": "boolean"时无需创建
            #                         continue
            #                     cond_key_out = tmp_key.replace("_", " ")
            #                     element_position_map = get_element_position(tmp_key)
            #                 else:
            #                     element_position_map = get_element_position(cond_key)
            #                 cond_code = create_ip.create(cond_data[i], element_position_map)
            #                 if cond_code == 200:
            #                     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
            #                           "Create {} object successfully.".format(cond_key_out), flush=True)
            #                 else:
            #                     result = "Fail to create {} object.".format(cond_key_out)
            #                     cond_status = 1
            #                     break
            #         if cond_status == 1:  # 创建失败，退出遍历创建
            #             break
            #
            # # 创建rule
            # if cond_code == 200:
            create_objects = CreateObject(driver)
            #获取当前所需的element
            element_position_map = get_element_position(policy_configuration["type"])
            #执行创建操作
            create_object_code = create_objects.create(policy_configuration, element_position_map)
            if create_object_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create {} rule successfully.".format(policy_configuration["policy_type"], flush=True))
            elif create_object_code != 200:
                result = "Fail to create {} rule.".format(policy_configuration["policy_type"])
                return "", "", result

            search_objects = SearchObjects(driver)
            # element_position_map = get_element_position(policy_configuration["policy_type"])
            search_rule_code, object_uuid = search_objects.search(policy_configuration,element_position_map)
            if search_rule_code != 200:
                result = "Fail to search {} rule uuid.".format(policy_configuration["policy_type"])
                return "", "", result
            object_uuids_list = []
            object_uuids_temp_dict = {}
            object_uuids_temp_dict["type"] = policy_configuration["type"]
            object_uuids_temp_dict["uuid"] = object_uuid
            object_uuids_temp_dict["name"] = policy_configuration["name"]
            object_uuids_temp_dict["description"] = policy_configuration["type"]
            object_uuids_list.append(object_uuids_temp_dict)
            rule_uuids_tuple = tuple(object_uuids_list)

            return rule_uuids_tuple, result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                  "When creating rule by ui, the exception error: ", str(e), flush=True)
            return "", "When creating rule by ui, the exception error: " + str(e)
