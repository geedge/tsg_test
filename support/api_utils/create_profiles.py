# -*- coding: UTF-8 -*-
import json
import requests
from datetime import datetime

class CreateProfiles:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
    
    def create_profiles(self, policy_configuration):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        root_path = self.parameter["root_path"]
        try:
            print("to be added...")
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating profile, the exception error: ", str(e), flush=True)
            return "" ,"When creating profile, the exception error: " + str(e)
        
    def get_uuids(self, response_dict, type):
        if type == "statistics_template":
            uuid = response_dict["data"]["profile"]["uuid"]
            return uuid, ""