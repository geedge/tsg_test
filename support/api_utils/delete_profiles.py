# -*- coding: UTF-8 -*-
import requests
from datetime import datetime

class DeleteProfiles:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
    
    def delete_profiles(self, profile_uuids_tuple):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        try:
            print("to be added...")
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting profile, the exception error: ", str(e), flush=True)
            return "" ,"When deleting profile, the exception error: " + str(e)