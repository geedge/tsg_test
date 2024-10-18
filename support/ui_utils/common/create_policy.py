# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.common.create_manipulation_policy import CreateManipulationPolicy
from support.ui_utils.common.create_dos_protection_policy import CreateDosProtectionPolicy
from support.ui_utils.common.create_statistics_policy import CreateStatisticsPolicy
from support.ui_utils.common.create_security_policy import CreateSecurityPolicy
from support.ui_utils.common.create_service_chaining_policy import CreateServiceChainingPolicy
from support.ui_utils.common.create_monintor_policy import CreateMonitorPolicy
from support.ui_utils.common.create_intercept_policy import CreateInterceptPolicy
from support.ui_utils.common.create_security_policy_example import CreateSecurityPolicyExample

class CreatePolicy:
    def create_policy(self, parameter, policy_configuration, driver):
        if "type" in policy_configuration.keys() and policy_configuration["type"] == "security":
            result = self.create_security_policy(parameter, policy_configuration, driver)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "monitor":
            result = self.create_monitor_policy(parameter, policy_configuration, driver)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "statistics":
            result = self.create_statistics_policy(parameter, policy_configuration, driver)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "dos_protection":
            result = self.create_dos_protection_policy(parameter, policy_configuration, driver)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "pxy_intercept":
            result = self.create_intercept_policy(parameter, policy_configuration, driver)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "pxy_manipulation":
            result = self.create_manipulation_policy(parameter, policy_configuration, driver)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "service_chaining":
            result = self.create_service_chaining_policy(parameter, policy_configuration, driver)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "example":
            result = self.create_security_policy_example(parameter, policy_configuration, driver)
        else:
            pass
        return result

    def create_security_policy(self, parameter, policy_configuration, driver):
        security = CreateSecurityPolicy()
        result = security.create_policy(parameter, policy_configuration, driver)
        return result

    def create_monitor_policy(self, parameter, policy_configuration, driver):
        create = CreateMonitorPolicy()
        result = create.create_policy(parameter, policy_configuration, driver)
        return result

    def create_statistics_policy(self, parameter, policy_configuration, driver):
        create = CreateStatisticsPolicy()
        result = create.create_policy(parameter, policy_configuration, driver)
        return result

    def create_dos_protection_policy(self, parameter, policy_configuration, driver):
        create = CreateDosProtectionPolicy()
        result = create.create_policy(parameter, policy_configuration, driver)
        return result

    def create_intercept_policy(self, parameter, policy_configuration, driver):
        create = CreateInterceptPolicy()
        result = create.create_policy(parameter, policy_configuration, driver)
        return result

    def create_manipulation_policy(self, parameter, policy_configuration, driver):
        create = CreateManipulationPolicy()
        result = create.create_policy(parameter, policy_configuration, driver)
        return result

    def create_service_chaining_policy(self, parameter, policy_configuration, driver):
        create = CreateServiceChainingPolicy()
        result = create.create_policy(parameter, policy_configuration, driver)
        return result

    def create_security_policy_example(self, parameter, policy_configuration, driver):
        create = CreateSecurityPolicyExample()
        result = create.create_policy(parameter, policy_configuration, driver)
        return result
        