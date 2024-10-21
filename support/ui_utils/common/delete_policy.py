# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.common.delete_security_policy_example import DeleteSecurityPolicyExample

class DeletePolicy:
    def delete_policy(self, parameter, policy_configuration, configured_policy):
        if "type" in policy_configuration.keys() and policy_configuration["type"] == "security":
            delete = DeleteSecurityPolicyExample()
            result = delete.delete_policy(parameter, policy_configuration, configured_policy)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "monitor":
            print("to be added")
        return result