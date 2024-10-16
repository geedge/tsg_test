# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.instance_utils.delete_temp_instantiation import DeleteTempInstantiation
from support.api_utils.delete_policy import DeletePolicy

class DeleteInstantiation:
    def __init__(self):
        self.delete_temp_instantiation = DeleteTempInstantiation()
        
    def delete(self, parameter, test_data, instantiation_result):
        policy_configuration = test_data["policy_configuration"]
        if "type" in policy_configuration.keys() and policy_configuration["type"] == "temp":
            result = self.delete_temp_instantiation.delete(parameter, test_data, instantiation_result)
            return result
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "security":
            print("to be added.")
            
    def clean_up(self, parameter, instantiation_result):
        ui_name_list = instantiation_result["ui_name_list"]
        api_name_list = instantiation_result["api_name_list"]
        delete = DeletePolicy()
        if isinstance(ui_name_list, list) and ui_name_list != []:
            # 环境清理
            support.ui_utils.env.teardown()
            # 强行删除，防止有配置残留影响其他用例测试
            delete.delete_policy_by_name(instantiation_result["token"], parameter, ui_name_list)
        if isinstance(api_name_list, list) and api_name_list != []:
            # 强行删除，防止有配置残留影响其他用例测试
            delete.delete_policy_by_name(instantiation_result["token"], parameter, api_name_list)
