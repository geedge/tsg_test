# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.common_utils.create_manipulation_policy import CreateManipulationPolicy
from support.common_utils.create_dos_protection_policy import CreateDosProtectionPolicy
from support.common_utils.create_objects import CreateObjects
from support.common_utils.create_statistics_policy import CreateStatisticsPolicy
from support.common_utils.create_security_policy import CreateSecurityPolicy
from support.common_utils.create_service_chaining_policy import CreateServiceChainingPolicy
from support.common_utils.create_monintor_policy import CreateMonitorPolicy
from support.common_utils.create_dashboard import CreateDashbboard
from support.common_utils.create_intercept_policy import CreateInterceptPolicy

class CreatePolicy:
    def __init__(self, policy_configuration, parameter):
        self.policy_configuration = policy_configuration
        self.parameter = parameter

    def create_policy(self):
        if "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "security":
            result = self.create_security_policy(self.policy_configuration, self.parameter)
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "monitor":
            result = self.create_monitor_policy(self.policy_configuration, self.parameter)
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "statistics":
            result = self.create_statistics_policy(self.policy_configuration, self.parameter)
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "dos_protection":
            result = self.create_dos_protection_policy(self.policy_configuration, self.parameter)
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "pxy_intercept":
            result = self.create_intercept_policy(self.policy_configuration, self.parameter)
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "pxy_manipulation":
            result = self.create_manipulation_policy(self.policy_configuration, self.parameter)
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "shaping":
            print("todo")
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "service_chaining":
            result = self.create_service_chaining_policy(self.policy_configuration, self.parameter)
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "dashboard":
            result = self.create_dashboard(self.policy_configuration, self.parameter)
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "objects":
            result = self.create_objects(self.policy_configuration, self.parameter)
        else:
            pass
        return result

    def create_security_policy(self, policy_configuration, parameter):
        self.security = CreateSecurityPolicy(policy_configuration, parameter)
        result = self.security.run()
        return result

    def create_monitor_policy(self, policy_configuration, parameter):
        self.monitor = CreateMonitorPolicy(policy_configuration,parameter)
        result = self.monitor.run()
        return result

    def create_statistics_policy(self, policy_configuration, parameter):
        self.statistics = CreateStatisticsPolicy(policy_configuration, parameter)
        result = self.statistics.run()
        return result

    def create_dos_protection_policy(self, policy_configuration, parameter):
        self.dos_protection = CreateDosProtectionPolicy(policy_configuration, parameter)
        result = self.dos_protection.run()
        return result

    def create_intercept_policy(self, policy_configuration, parameter):
        self.intercept = CreateInterceptPolicy(policy_configuration, parameter)
        result = self.intercept.run()
        return result

    def create_manipulation_policy(self, policy_configuration, parameter):
        self.manipulation = CreateManipulationPolicy(policy_configuration, parameter)
        result = self.manipulation.run()
        return result

    def create_shaping_policy(self, policy_configuration, parameter):
        print("todo")

    def create_dashboard(self, policy_configuration, parameter):
        self.dashboard = CreateDashbboard(policy_configuration,parameter)
        result = self.dashboard.run()
        return result

    def create_service_chaining_policy(self, policy_configuration, parameter):
        self.service_chaining =CreateServiceChainingPolicy(policy_configuration, parameter)
        result = self.service_chaining.run()
        return result

    def create_objects(self,policy_configuration, parameter):
        self.objects = CreateObjects(policy_configuration, parameter)
        result = self.objects.run()
        return result

    def clean_up(self):
        if "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "security":
             self.security.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "monitor":
             self.monitor.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "statistics":
            self.statistics.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "dos_protection":
            self.dos_protection.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "pxy_intercept":
            self.intercept.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "pxy_manipulation":
            self.manipulation.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "shaping":
            print("todo")
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] == "service_chaining":
            self.service_chaining.clean_up()
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "dashboard":
            self.dashboard.clean_up()
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "objects":
            self.objects.clean_up()
        else:
            pass
        