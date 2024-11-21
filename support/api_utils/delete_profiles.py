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
            reversed_tuple = tuple(reversed(profile_uuids_tuple))
            profile_uuids_list = list(reversed_tuple)
            for i in range(len(profile_uuids_list)):
                type = profile_uuids_list[i]["type"]
                deleted_object_dict = {"uuids": [profile_uuids_list[i]["uuid"]], "vsys": vsys}
                url = api_server + "/v1/profiles/{}".format(type)
                response = requests.delete(url, headers=self.headers, json=deleted_object_dict, verify=False)
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Delete {} profile successfully.".format(type.replace("-", " ")), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                          "Delete {} profile failed.".format(type.replace("-", " ")), flush=True)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting profile, the exception error: ", str(e), flush=True)
            return "" ,"When deleting profile, the exception error: " + str(e)