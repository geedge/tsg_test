# -*- coding: UTF-8 -*-
import json
import requests
from datetime import datetime

class CreateObjects:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
    
    def create_objects(self, policy_configuration):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        root_path = self.parameter["root_path"]
        try:
            object_template = root_path + "/support/api_utils/template/object_template_2410.json"
            with open(object_template, 'r', encoding='utf-8') as f:
                object_template_json = json.load(f)
            for key in policy_configuration.keys():
                if key == "and_conditions":
                    condition_temp = policy_configuration[key]
                    object_uuids_list = []
                    for i in range(len(condition_temp)):
                        object_temp = condition_temp[i]["or_conditions"]
                        for j in range(len(object_temp)):
                            if object_temp[j]["type"] != "application":
                                object_template_json["vsys"] = vsys
                                object_template_json["object"]["name"] = object_temp[j]["name"]
                                object_template_json["object"]["type"] = object_temp[j]["type"]
                                object_template_json["object"]["sub_type"] = object_temp[j]["sub_type"]
                                object_template_json["object"]["member_type"] = "item"
                                item_temp = object_temp[j]["items"]
                                item_list = []
                                if object_temp[j]["type"] == "ip":
                                    for t in range(len(item_temp)):
                                        item_dict = {}
                                        if "ip" in item_temp[t]:
                                            item_dict = dict(ip=item_temp[t]["ip"], op=item_temp[t]["op"], interval=item_temp[t]["interval"])
                                            item_list.append(item_dict)
                                object_template_json["object"]["items"] = item_list
                                object_type_dict = {
                                    "ip": "ip-addresses",
                                    "url": "urls",
                                    "fqdn": "fqdns",
                                    "keyword": "keywords",
                                    "subscriberid": "subscriber-ids",
                                    "account": "accounts",
                                    "mobile_identity": "mobile-identities",
                                    "apn": "apns",
                                    "application": "applications",
                                    "tunnel": "tunnels",
                                    "flag": "flags",
                                    "interval": "intervals",
                                    "port": "ports",
                                    "boolean": "boolean",
                                    "ip_protocol": "ip-protocols",
                                    "tunnel_level": "tunnel-levels"
                                }
                                url = api_server + "/v1/objects/{}".format(object_type_dict[object_temp[j]["type"]])
                                response = requests.post(url, headers=self.headers, json=object_template_json, verify=False)
                                if response.status_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_template_json["object"]["type"].replace("_", " ")), flush=True)
                                    response_dict = json.loads(response.text)
                                    object_uuids, object_geo_uuid = self.get_uuids(response_dict, object_temp[j]["type"])
                                    object_uuids_temp_dict = {}
                                    object_uuids_temp_dict["type"] = object_temp[j]["type"]
                                    object_uuids_temp_dict["uuid"] = object_uuids
                                    object_uuids_temp_dict["name"] = object_temp[j]["name"]
                                    object_uuids_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                                    # object_uuids_temp_dict["negate_option"] = condition_temp[i]["negate_option"]
                                    object_uuids_list.append(object_uuids_temp_dict)
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object failed.".format(object_template_json["object"]["type"].replace("_", " ")), flush=True)
                                    return "", "Create {} object failed.".format(object_template_json["object"]["type"].replace("_", " "))
            object_uuids_tuple = tuple(object_uuids_list)
            return object_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating object, the exception error: ", str(e), flush=True)
            return "" ,"When creating object, the exception error: " + str(e)
        
    def get_uuids(self, response_dict, type):
        if type == "ip":
            uuid = response_dict["data"]["object"]["uuid"]
            return uuid, ""
        elif type == "geolocation":
            uuid = ""
            geo_name_uuid = ""
            print("to be added...")
            return uuid, geo_name_uuid