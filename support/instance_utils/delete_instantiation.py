# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.instance_utils.delete_temp_instantiation import DeleteTempInstantiation

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
            
    def clean_up(self, parameter, test_data, instantiation_result):
        policy_configuration = test_data["policy_configuration"]
        if "type" in policy_configuration.keys() and policy_configuration["type"] == "temp":
            self.delete_temp_instantiation.delete(parameter, instantiation_result)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "security":
            print("to be added.")
