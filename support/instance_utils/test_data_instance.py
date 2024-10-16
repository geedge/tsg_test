# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.instance_utils.manipulation_instance import ManipulationInstance
from support.instance_utils.dos_protection_instance import DosProtectionInstance
from support.instance_utils.objects_instance import ObjectsInstance
from support.instance_utils.statistics_instance import StatisticsInstance
from support.instance_utils.security_instance import SecurityInstance
from support.instance_utils.service_chaining_instance import ServiceChainingInstance
from support.instance_utils.monintor_instance import MonitorInstance
from support.instance_utils.dashboard_instance import DashbboardInstance
from support.instance_utils.intercept_instance import InterceptInstance
from support.instance_utils.temp_instance import TempInstance

class TestDataInstance:
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
        self.security = SecurityInstance(policy_configuration, parameter)
        result = self.security.run()
        return result

    def create_monitor_policy(self, policy_configuration, parameter):
        self.monitor = MonitorInstance(policy_configuration,parameter)
        result = self.monitor.run()
        return result

    def create_statistics_policy(self, policy_configuration, parameter):
        self.statistics = StatisticsInstance(policy_configuration, parameter)
        result = self.statistics.run()
        return result

    def create_dos_protection_policy(self, policy_configuration, parameter):
        self.dos_protection = DosProtectionInstance(policy_configuration, parameter)
        result = self.dos_protection.run()
        return result

    def create_intercept_policy(self, policy_configuration, parameter):
        self.intercept = InterceptInstance(policy_configuration, parameter)
        result = self.intercept.run()
        return result

    def create_manipulation_policy(self, policy_configuration, parameter):
        self.manipulation = ManipulationInstance(policy_configuration, parameter)
        result = self.manipulation.run()
        return result

    def create_shaping_policy(self, policy_configuration, parameter):
        print("todo")

    def create_dashboard(self, policy_configuration, parameter):
        self.dashboard = DashbboardInstance(policy_configuration,parameter)
        result = self.dashboard.run()
        return result

    def create_service_chaining_policy(self, policy_configuration, parameter):
        self.service_chaining =ServiceChainingInstance(policy_configuration, parameter)
        result = self.service_chaining.run()
        return result

    def create_objects(self,policy_configuration, parameter):
        self.objects = ObjectsInstance(policy_configuration, parameter)
        result = self.objects.run()
        return result

    def create_temp_policy(self, policy_configuration, parameter, loop_number):
        self.temp = TempInstance(policy_configuration, parameter, loop_number)
        result = self.temp.create()
        return result
    
    # =============required begin=============
    def delete(self):
        if "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "temp":
             self.temp.delete()
    # =============required end=============
    
    def clean_up(self):
        if "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "security":
             self.security.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "monitor":
             self.monitor.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "statistics":
            self.statistics.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "dos_protection":
            self.dos_protection.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "pxy_intercept":
            self.intercept.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "pxy_manipulation":
            self.manipulation.clean_up()
        elif "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "shaping":
            print("todo")
        elif "policy_type" in self.policy_configuration.keys() and self.self.policy_configuration["policy_type"] == "service_chaining":
            self.service_chaining.clean_up()
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "dashboard":
            self.dashboard.clean_up()
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "objects":
            self.objects.clean_up()
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "temp":
            self.temp.clean_up()
        else:
            pass
        