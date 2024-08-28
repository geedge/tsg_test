from support.common.manipulation_generator import ManipulationGenerator

class CaseGenerator:
    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter
    
    def run(self):
        result = self._run(self.test_data, self.parameter)
        return result

    def _run(self, test_data, parameter):
        if test_data["policy_type"] == "security":
            result = self._run_security(test_data, parameter)
        elif test_data["policy_type"] == "monitor":
            print("todo")
        elif test_data["policy_type"] == "statistics":
            print("todo")
        elif test_data["policy_type"] == "dos_protection":
            print("todo")
        elif test_data["policy_type"] == "pxy_intercept":
            print("todo")
        elif test_data["policy_type"] == "pxy_manipulation":
            result = self._run_manipulation(test_data, parameter)
        elif test_data["policy_type"] == "shaping":
            print("todo")
        elif test_data["policy_type"] == "service_chaining":
            print("todo")
        else:
            pass
        return result

    def _run_security(self, test_data, parameter):
        print("todo")

    def _run_monitor(self, test_data, parameter):
        print("todo")

    def _run_statistics(self, test_data, parameter):
        print("todo")

    def _run_dos_protection(self, test_data, parameter):
        print("todo")

    def _run_intercept(self, test_data, parameter):
        print("todo")

    def _run_manipulation(self, test_data, parameter):
        self.manipulation = ManipulationGenerator(test_data, parameter)
        result = self.manipulation.run()
        return result

    def _run_shaping(self, test_data, parameter):
        print("todo")

    def _run_service_chaining(self, test_data, parameter):
        print("todo")

    def delete_data(self):
        if self.test_data["policy_type"] == "security":
            pass
        elif self.test_data["policy_type"] == "monitor":
            print("todo")
        elif self.test_data["policy_type"] == "statistics":
            print("todo")
        elif self.test_data["policy_type"] == "dos_protection":
            print("todo")
        elif self.test_data["policy_type"] == "pxy_intercept":
            print("todo")
        elif self.test_data["policy_type"] == "pxy_manipulation":
            self.manipulation.delete_data()
        elif self.test_data["policy_type"] == "shaping":
            print("todo")
        elif self.test_data["policy_type"] == "service_chaining":
            print("todo")
        else:
            pass
        