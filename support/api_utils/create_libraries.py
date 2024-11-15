# -*- coding: UTF-8 -*-
import json
import requests
from datetime import datetime

class CreateLibraries:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
        self.api_server = self.parameter["api_server"]
        self.vsys = self.parameter["vsys"]
        self.root_path = self.parameter["root_path"]
    
    def create_libraries(self, policy_configuration):
        try:
            tag_uuids_tuple, error = self.create_tags(policy_configuration)
            if error:
                return "", error
            catalog_uuids_tuple, error = self.create_catalogs(policy_configuration, tag_uuids_tuple)
            if error:
                return "", error
            library_uuids_list = []
            library_uuids_list.append(tag_uuids_tuple)
            library_uuids_list.append(catalog_uuids_tuple)
            library_uuids_tuple = tuple(library_uuids_list)
            return library_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating library, the exception error: ", str(e), flush=True)
            return "" ,"When creating library, the exception error: " + str(e)

    def create_tags(self, policy_configuration):
        try:
            tag_template = self.root_path + "/support/api_utils/template/tag_template.json"
            with open(tag_template, 'r', encoding='utf-8') as f:
                tag_template_json = json.load(f)
            tag_uuids_list = []
            for key in policy_configuration.keys():
                if key == "and_conditions":
                    condition_temp = policy_configuration[key]
                    
            tag_uuids_tuple = tuple(tag_uuids_list)
            return tag_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating tag, the exception error: ", str(e), flush=True)
            return "" ,"When creating tag, the exception error: " + str(e)
        
    def create_catalogs(self, policy_configuration, tag_uuids_tuple):
        try:
            catalog_template = self.root_path + "/support/api_utils/template/catalog_template.json"
            with open(catalog_template, 'r', encoding='utf-8') as f:
                catalog_template_json = json.load(f)
            catalog_uuids_list = []
            for key in policy_configuration.keys():
                if key == "and_conditions":
                    condition_temp = policy_configuration[key]
                    
            catalog_uuids_tuple = tuple(catalog_uuids_list)
            return catalog_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating catalog, the exception error: ", str(e), flush=True)
            return "" ,"When creating catalog, the exception error: " + str(e)

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