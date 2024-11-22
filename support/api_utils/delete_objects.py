# -*- coding: UTF-8 -*-
import requests
from datetime import datetime

class DeleteObjects:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
    
    def delete_objects(self, object_uuids_tuple):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        try:
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
            object_uuids_list = list(object_uuids_tuple)
            object_uuids_list.reverse()
            for i in range(len(object_uuids_list)):
                type = object_uuids_list[i]["type"]
                deleted_object_dict = {"type": type, "uuids": [], "vsys": 1}
                deleted_object_dict["uuids"].append(object_uuids_list[i]["uuid"])
                deleted_object_dict["vsys"] = vsys
                if type == "signature":
                    url = api_server + "/v1/objects/applications/customized-signatures"
                elif type == "user_defined_attribute":
                    url = api_server + "/v1/objects/applications/customized-attributes"
                else:
                    url = api_server + "/v1/objects/{}".format(object_type_dict[type])
                if type == "boolean" or type == "ip_protocol" or type == "tunnel_level" or (type == "application" and "name" not in object_uuids_list[i]):
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "{} object is built in, no need to be deleted.".format(type.replace("_", " ")).capitalize(), flush=True)
                    continue
                response = requests.delete(url, headers=self.headers, json=deleted_object_dict, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(type.replace("_", " ")), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object failed.".format(type.replace("_", " ")), flush=True)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting object, the exception error: ", str(e), flush=True)
            return "" ,"When deleting object, the exception error: " + str(e)