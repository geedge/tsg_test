
class DeleteInstantiation:
    def __init__(self, parameter, policy_configuration, loop_number):
        self.parameter = parameter
        self.policy_configuration = policy_configuration
        self.loop_number = loop_number
        
    def delete(self):
        if "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "temp":
            delete_temp_instantiation = DeleteTempInstantiation()
            result = delete_temp_instantiation.delete(self.policy_configuration, self.parameter, self.loop_number)
            return result
             
    def clean_up(self):
        if "type" in self.policy_configuration.keys() and self.policy_configuration["type"] == "temp":
            self.temp.clean_up()
