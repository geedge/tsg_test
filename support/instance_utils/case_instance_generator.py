# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.instance_utils.manipulation_instance_generator import ManipulationInstanceGenerator
from support.instance_utils.dos_protection_instance_generator import DosProtectionInstanceGenerator
from support.instance_utils.objects_instance_generator import ObjectsInstanceGenerator
from support.instance_utils.statistics_instance_generator import StatisticsInstanceGenerator
from support.instance_utils.security_instance_generator import SecurityGenerator
from support.instance_utils.service_chaining_instance_generator import ServiceChainingInstanceGenerator
from support.instance_utils.monintor_instance_generator import MonitorInstanceGenerator
from support.instance_utils.dashboard_instance_generator import DashbboardInstanceGenerator
from support.instance_utils.intercept_instance_generator import InterceptInstanceGenerator
from support.instance_utils.temp_instance_generator import TempInstanceGenerator

class CaseInstanceGenerator:
    def __init__(self, policy_configuration, parameter):
        self.policy_configuration = policy_configuration
        self.parameter = parameter
    
    def create(self):
        result = self._run(self.policy_configuration, self.parameter)
        return result

    def _run(self, policy_configuration, parameter):
        if "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "security":
            result = self._run_security(policy_configuration, parameter)
        elif "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "monitor":
            result = self._run_monitor(policy_configuration,parameter)
        elif "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "statistics":
            result = self._run_statistics(policy_configuration, parameter)
        elif "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "dos_protection":
            result = self._run_dos_protection(policy_configuration, parameter)
        elif "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "pxy_intercept":
            result = self._run_intercept(policy_configuration, parameter)
        elif "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "pxy_manipulation":
            result = self._run_manipulation(policy_configuration, parameter)
        elif "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "shaping":
            print("todo")
        elif "policy_type" in policy_configuration.keys() and policy_configuration["policy_type"] == "service_chaining":
            result = self._run_service_chaining(policy_configuration, parameter)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "dashboard":
            result = self._run_dashboard(policy_configuration, parameter)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "objects":
            result = self._run_objects(policy_configuration, parameter)
        elif "type" in policy_configuration.keys() and policy_configuration["type"] == "temp":
            result = self._run_temp(policy_configuration, parameter)
        else:
            pass
        return result

    def _run_security(self, policy_configuration, parameter):
        self.security = SecurityGenerator(policy_configuration, parameter)
        result = self.security.run()
        return result

    def _run_monitor(self, policy_configuration, parameter):
        self.monitor = MonitorInstanceGenerator(policy_configuration,parameter)
        result = self.monitor.run()
        return result

    def _run_statistics(self, policy_configuration, parameter):
        self.statistics = StatisticsInstanceGenerator(policy_configuration, parameter)
        result = self.statistics.run()
        return result

    def _run_dos_protection(self, policy_configuration, parameter):
        self.dos_protection = DosProtectionInstanceGenerator(policy_configuration, parameter)
        result = self.dos_protection.run()
        return result

    def _run_intercept(self, policy_configuration, parameter):
        self.intercept = InterceptInstanceGenerator(policy_configuration, parameter)
        result = self.intercept.run()
        return result

    def _run_manipulation(self, policy_configuration, parameter):
        self.manipulation = ManipulationInstanceGenerator(policy_configuration, parameter)
        result = self.manipulation.run()
        return result

    def _run_shaping(self, policy_configuration, parameter):
        print("todo")

    def _run_dashboard(self, policy_configuration, parameter):
        self.dashboard = DashbboardInstanceGenerator(policy_configuration,parameter)
        result = self.dashboard.run()
        return result

    def _run_service_chaining(self, policy_configuration, parameter):
        self.service_chaining =ServiceChainingInstanceGenerator(policy_configuration, parameter)
        result = self.service_chaining.run()
        return result

    def _run_objects(self,policy_configuration, parameter):
        self.objects = ObjectsInstanceGenerator(policy_configuration, parameter)
        result = self.objects.run()
        return result

    def _run_temp(self, policy_configuration, parameter):
        self.temp = TempInstanceGenerator(policy_configuration, parameter)
        result = self.temp.run()
        return result
    
    # =============required begin=============
    def delete(self, policy_configuration, case_generator_result):
        if "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "temp":
             self.temp.delete(policy_configuration, case_generator_result)
    # =============required end=============
    
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
        elif "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "temp":
            self.temp.clean_up()
        else:
            pass
        