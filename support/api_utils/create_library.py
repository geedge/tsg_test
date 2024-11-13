import copy
import os.path
import sys
import ipaddress
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import requests
from datetime import datetime

class CreateLibrary:
    def __init__(self):
        self.tag_ids = []
        self.catalog_ids = []
    
    def create_library(self, token, library_condition, api_host, vsys_id):
        try:
            library_tag_ids_dict = []
            headers = {"Authorization": token, "Content_Type":"application/json"}
            for library in library_condition:
                library_data = library["library"]
                attribute_name = library["attribute_name"]
                negate = library["is_negate"]
                if negate:
                    is_negate = 1
                else:
                    is_negate = 0
                for i in range (len(library_data)):
                    tags_data = library_data[i]["tags"]
                    for j in range(len(tags_data)):
                        tag_data = tags_data[j]
                        tag_template = self.process_tag_data(tag_data,vsys_id)
                        tag_template["tag"]["category"] = library_data[i]["category"]
                        tag_template["vsys"] = vsys_id
                        tag_id = self.create_tag(headers, tag_template, api_host)
                    self.tag_ids.append(tag_id)
                    catalogs_data = library_data[i]["catalogs"]
                    for k in range(len(catalogs_data)):
                        catalog_data = catalogs_data[k]
                        catalog_template = self.process_catalog_data(catalog_data,vsys_id)
                        catalog_template["catalog"]["category"] = library_data[i]["category"]
                        catalog_template["vsys"] = vsys_id
                        catalog_id = self.create_catalog(headers, catalog_template, api_host)
                        self.catalog_ids.append(catalog_id)
                library_tag_id_dict = self.tag_ids_to_policy_obj_list(attribute_name,is_negate)
            library_tag_ids_dict.append(library_tag_id_dict)    
            return library_tag_ids_dict, self.tag_ids, self.catalog_ids
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def create_tag(self, headers, tag_data, api_host):
        try:
            url = "{}/v1/library/tags".format(api_host)
            response = requests.post(headers=headers, url=url, json=tag_data, verify=False)
            response_data = response.json()
            tag_id = response_data["data"]["uuid"]
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create library tag successfully.", flush=True)
            return tag_id
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def process_tag_data(self, tag_data, vsys_id):
        try:
            tag_template = {
                "vsys_id": vsys_id,
                "op":"",
                "return_data":1,
                "tag":{
                    "category":"",
                    "tag_key":"testkey",
                    "tag_value":"testvalue",
                    "description":"autotest"
                }
            }
            tag_template["op"] = tag_data["op"]
            tag_template["tag"]["tag_key"] = tag_data["tag_key"]
            tag_template["tag"]["tag_value"] = tag_data["tag_value"]
            return tag_template
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def create_catalog(self, headers, catalog_data, api_host):
        try:
            url = "{}/v1/library/catalogs".format(api_host)
            response = requests.post(headers=headers, url=url, json=catalog_data, verify=False)
            catalog_data = response.json()
            catalog_id = catalog_data["data"]["uuid"]
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create library catalog successfully.", flush=True)
            return catalog_id
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    def process_catalog_data(self,catalog_data,vsys_id):
        catalog_template = {
            "vsys_id": vsys_id,
            "op":"add",
            "return_data": 1,
            "is_dry_run": 0,
            "catalog":{
                "category":"",
                "tag_ids":"",
                "ip_entries":[],
                "fqdn_entries":[]
            }
        }
        if "ip_entries" in catalog_data.keys() and catalog_data["ip_entries"] != "":
            ips = catalog_data["ip_entries"].split(",")
            for ip in ips:
                ip_template = {
                    "op":"",
                    # "entry_id":None,
                    "uuid": None,
                    "add_type":4,
                    # "port":"0-65535"
                }
                ip_template["op"] = catalog_data["op"]
                if "-" in ip:
                    ip_template["ip"] = ip
                elif "/" in ip:
                    ip_template["ip"] = ip
                else:
                    ip_template["ip"] = ip
                ip_type = self.identify_ip_type(ip)
                ip_template["add_type"] = ip_type
                catalog_template["catalog"]["ip_entries"].append(ip_template)
        if "fqdn_entries" in catalog_data.keys() and catalog_data["fqdn_entries"] != "":
            fqdns = catalog_data["fqdn_entries"].split(",")
            for fqdn in fqdns:
                fqdn_template = {
                    "op":"",
                    "uuid": None,
                    "fqdn":""
                }
                # 处理fqdn适配24.10版本新格式
                if "$" in fqdn:
                    fqdn = fqdn.replace("$","")
                fqdn_template["op"] = catalog_data["op"]
                fqdn_template["fqdn"] = fqdn
                catalog_template["catalog"]["fqdn_entries"].append(fqdn_template)
        tag_count = len(self.tag_ids)
        if tag_count == 1:
                catalog_template["catalog"]["tag_uuids"] = str(self.tag_ids[0])
        elif tag_count > 1:
            separator = ","  
            catalog_template["catalog"]["tag_uuids"] = separator.join(self.tag_ids)
        return catalog_template
    
    def identify_ip_type(self, ip_data):
        if "-" in ip_data:
            ip_list = ip_data.split("-")
            for ip in ip_list:
                ip_obj = ipaddress.ip_address(ip)
        elif "/" in ip_data:
            ip_obj = ipaddress.ip_network(ip_data, strict=True)
        else:
            ip_obj = ipaddress.ip_address(ip_data)
        ip_type = ip_obj.version
        return ip_type



    def tag_ids_to_policy_obj_list(self, attribute_name, is_negate): # 处理tag_id
        temp_list = []
        for tag in self.tag_ids:
            # tag = int(tag)
            tag_id_list = []
            tag_id_list.append(tag)
            tag_dict = dict(tag_uuids=tag_id_list)
            temp_list.append(tag_dict)
            temp_dict = dict(library_tags=temp_list, attribute_name=attribute_name, negate_option=is_negate)
        return temp_dict
    
    def tags_ids_to_policy_condition_list(self, library_condition_ids_dict, condition_ids_by_api_dict):
        for library_condition in library_condition_ids_dict:
            and_condition_dict = {
                "negate_option": False,
                "or_conditions": [],
            }
            or_condition_dict = {}
            or_condition_dict["attribute_name"] = library_condition["attribute_name"]
            or_condition_dict["object_uuids"] = library_condition["library_tags"][0]["tag_uuids"]
            copy_dict = copy.deepcopy(or_condition_dict)
            and_condition_dict["or_conditions"].append(copy_dict)
            condition_ids_by_api_dict["and_conditions"].append(and_condition_dict)
        return condition_ids_by_api_dict

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")