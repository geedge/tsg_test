import os
import sys
import time

class EditProfiles:
    def __init__(self, driver):
        self.driver = driver

    def edit_profiles(self, policy_configuration):
        if "action_parameter" not in policy_configuration.keys():
            return ""