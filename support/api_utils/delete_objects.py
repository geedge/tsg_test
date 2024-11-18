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
            for i in range(len(object_uuids_list)):
                type = object_uuids_list[i]["type"]
                deleted_object_dict = {"type": type, "uuids": [], "vsys": 1}
                deleted_object_dict["uuids"] = object_uuids_list[i]
                deleted_object_dict["vsys"] = vsys
                url = api_server + "/v1/objects/{}".format(object_type_dict[type])
                response = requests.delete(url, headers=self.headers, params=deleted_object_dict, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object successfully.".format(type.replace("_", " ")), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} object failed.".format(type.replace("_", " ")), flush=True)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting object, the exception error: ", str(e), flush=True)
            return "" ,"When deleting object, the exception error: " + str(e)