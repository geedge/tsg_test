# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.instance_utils.instance_manipulation import InstanceManipulation
from support.instance_utils.instance_dos_protection import InstanceDosProtection
from support.instance_utils.instance_objects import InstanceObjects
from support.instance_utils.instance_statistics import InstanceStatistics
from support.instance_utils.instance_security import InstanceSecurity
from support.instance_utils.instance_service_chaining import InstanceServiceChaining
from support.instance_utils.instance_monintor import InstanceMonitor
from support.instance_utils.instance_dashboard import InstanceDashbboard
from support.instance_utils.instance_intercept import InterceptInstance
from support.instance_utils.instance_temp import InstanceTemp

class InstanceTestData:
    def __init__(self, policy_configuration, parameter):
        self.policy_configuration = policy_configuration
        self.parameter = parameter

    def create(self):
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
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "temp":
            result = self.create_temp_policy(self.policy_configuration, self.parameter, loop_number=0)
        else:
            pass
        return result

    def create_security_policy(self, policy_configuration, parameter):
        self.security = InstanceSecurity(policy_configuration, parameter)
        result = self.security.run()
        return result

    def create_monitor_policy(self, policy_configuration, parameter):
        self.monitor = InstanceMonitor(policy_configuration,parameter)
        result = self.monitor.run()
        return result

    def create_statistics_policy(self, policy_configuration, parameter):
        self.statistics = InstanceStatistics(policy_configuration, parameter)
        result = self.statistics.run()
        return result

    def create_dos_protection_policy(self, policy_configuration, parameter):
        self.dos_protection = InstanceDosProtection(policy_configuration, parameter)
        result = self.dos_protection.run()
        return result

    def create_intercept_policy(self, policy_configuration, parameter):
        self.intercept = InterceptInstance(policy_configuration, parameter)
        result = self.intercept.run()
        return result

    def create_manipulation_policy(self, policy_configuration, parameter):
        self.manipulation = InstanceManipulation(policy_configuration, parameter)
        result = self.manipulation.run()
        return result

    def create_shaping_policy(self, policy_configuration, parameter):
        print("todo")

    def create_dashboard(self, policy_configuration, parameter):
        self.dashboard = InstanceDashbboard(policy_configuration,parameter)
        result = self.dashboard.run()
        return result

    def create_service_chaining_policy(self, policy_configuration, parameter):
        self.service_chaining =InstanceServiceChaining(policy_configuration, parameter)
        result = self.service_chaining.run()
        return result

    def create_objects(self,policy_configuration, parameter):
        self.objects = InstanceObjects(policy_configuration, parameter)
        result = self.objects.run()
        return result

    def create_temp_policy(self, policy_configuration, parameter, loop_number):
        self.temp = InstanceTemp(policy_configuration, parameter, loop_number)
        result = self.temp.create()
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
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] in ["proxy_intercept", "pxy_intercept"]:
            self.intercept.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.policy_configuration["policy_type"] in ["proxy_manipulation", "pxy_manipulation"]:
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
        