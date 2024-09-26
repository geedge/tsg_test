from support.instance_utils.manipulation_instance_generator import ManipulationInstanceGenerator
from support.instance_utils.dos_protection_instance_generator import DosProtectionInstanceGenerator
from support.instance_utils.objects_instance_generator import ObjectsInstanceGenerator
from support.instance_utils.statistics_instance_generator import StatisticsInstanceGenerator
from support.instance_utils.security_instance_generator import SecurityGenerator
from support.instance_utils.service_chaining_instance_generator import ServiceChainingInstanceGenerator
from support.instance_utils.monintor_instance_generator import MonitorInstanceGenerator
from support.instance_utils.dashboard_instance_generator import DashbboardInstanceGenerator

class CaseInstanceGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter
    
    def run(self):
        result = self._run(self.test_data, self.parameter)
        return result

    def _run(self, test_data, parameter):
        if "policy_type" in test_data.keys() and test_data["policy_type"] == "security":
            result = self._run_security(test_data, parameter)
        elif "policy_type" in test_data.keys() and test_data["policy_type"] == "monitor":
            result = self._run_monitor(test_data,parameter)
        elif "policy_type" in test_data.keys() and test_data["policy_type"] == "statistics":
            result = self._run_statistics(test_data, parameter)
        elif "policy_type" in test_data.keys() and test_data["policy_type"] == "dos_protection":
            result = self._run_dos_protection(test_data, parameter)
        elif "policy_type" in test_data.keys() and test_data["policy_type"] == "pxy_intercept":
            print("todo")
        elif "policy_type" in test_data.keys() and test_data["policy_type"] == "pxy_manipulation":
            result = self._run_manipulation(test_data, parameter)
        elif "policy_type" in test_data.keys() and test_data["policy_type"] == "shaping":
            print("todo")
        elif "policy_type" in test_data.keys() and test_data["policy_type"] == "service_chaining":
            result = self._run_service_chaining(test_data, parameter)
        elif "type" in test_data.keys() and test_data["type"] == "dashboard":
            result = self._run_dashboard(test_data, parameter)
        elif "type" in test_data.keys() and test_data["type"] == "objects":
            result = self._run_objects(test_data, parameter)
        else:
            pass
        return result

    def _run_security(self, test_data, parameter):
        self.security = SecurityGenerator(test_data, parameter)
        result = self.security.run()
        return result

    def _run_monitor(self, test_data, parameter):
        self.monitor = MonitorInstanceGenerator(test_data,parameter)
        result = self.monitor.run()
        return result

    def _run_statistics(self, test_data, parameter):
        self.statistics = StatisticsInstanceGenerator(test_data, parameter)
        result = self.statistics.run()
        return result

    def _run_dos_protection(self, test_data, parameter):
        self.dos_protection = DosProtectionInstanceGenerator(test_data, parameter)
        result = self.dos_protection.run()
        return result

    def _run_intercept(self, test_data, parameter):
        print("todo")

    def _run_manipulation(self, test_data, parameter):
        self.manipulation = ManipulationInstanceGenerator(test_data, parameter)
        result = self.manipulation.run()
        return result

    def _run_shaping(self, test_data, parameter):
        print("todo")

    def _run_dashboard(self, test_data, parameter):
        self.dashboard = DashbboardInstanceGenerator(test_data,parameter)
        result = self.dashboard.run()
        return result

    def _run_service_chaining(self, test_data, parameter):
        self.service_chaining =ServiceChainingInstanceGenerator(test_data, parameter)
        result = self.service_chaining.run()
        return result

    def _run_objects(self,test_data, parameter):
        self.objects = ObjectsInstanceGenerator(test_data, parameter)
        result = self.objects.run()
        return result

    def delete_data(self):
        if "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "security":
             self.security.delete_data()
        elif "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "monitor":
             self.monitor.delete_data()
        elif "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "statistics":
            self.statistics.delete_data()
        elif "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "dos_protection":
            self.dos_protection.delete_data()
        elif "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "pxy_intercept":
            print("todo")
        elif "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "pxy_manipulation":
            self.manipulation.delete_data()
        elif "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "shaping":
            print("todo")
        elif "policy_type" in self.test_data.keys() and self.test_data["policy_type"] == "service_chaining":
            self.service_chaining.delete_data()
        elif "type" in self.test_data.keys() and self.test_data["type"] == "dashboard":
            self.dashboard.delete_data()
        else:
            pass
        