# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import requests
from datetime import datetime
from support.ui_utils.workpath import workdir

class DeleteLibraries:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
        self.api_server = self.parameter["api_server"]
        self.vsys = self.parameter["vsys"]
    
    def delete_catalogs(self, library_uuids_tuple):
        try:
            library_uuids_list = list(library_uuids_tuple)
            catalog_uuids_list = self.extract_uuids(library_uuids_list, "catalog")
            deleted_catalog_dict = {"uuids": [], "vsys":1}
            deleted_catalog_dict["vsys"] = self.vsys
            deleted_catalog_dict["uuids"] = catalog_uuids_list
            if catalog_uuids_list == []:
                return 0
            url = self.api_server + "/v1/library/catalogs"
            response = requests.delete(url, headers=self.headers, json=deleted_catalog_dict, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete catalog successfully.", flush=True)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete catalog failed.", flush=True)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting catalog, the exception error: ", str(e), flush=True)
            return "" ,"When deleting catalog, the exception error: " + str(e)
        
    def delete_tags(self, library_uuids_tuple):
        try:
            tag_uuids_list = self.extract_uuids(library_uuids_tuple, "tag")
            delete_tag_dict = {"uuids": [], "vsys":1}
            delete_tag_dict["vsys"] = self.vsys
            delete_tag_dict["uuids"] =tag_uuids_list
            if tag_uuids_list == []:
                return 0
            url = self.api_server + "/v1/library/tags"
            response = requests.delete(url, headers=self.headers, json=delete_tag_dict, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete tag successfully.", flush=True)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete tag failed.", flush=True)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting tag, the exception error: ", str(e), flush=True)
            return "" ,"When deleting tag, the exception error: " + str(e)

    def extract_uuids(self, library_uuids_list, type):
        temp_uuids_list = []
        for library_uuids_tuple in library_uuids_list:
            library_uuids = list(library_uuids_tuple)
            for library_uuid in library_uuids:
                if library_uuid["type"] == type:
                    temp_uuids_list.append(library_uuid["uuid"])
        return temp_uuids_list

if __name__ == "__main__":
    library_uuids_list = [
        {
            "type": "tag",
            "uuid": 123,
            "name": "",
            "attribute_name": ""
        },
        {
            "type": "catalog",
            "uuid": 456,
            "name": "",
            "attribute_name": ""
        }
    ]
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.87",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "initiation_method": "api",
        "env": "tsgx",
        "vsys": 5,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    test = DeleteLibraries(parameter, "")
    test.delete_catalogs(library_uuids_list)