# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import support.ui_utils.env
from datetime import datetime

class CMDBCollector:
    # configuration management database resource collector
    def collect(self, uuid):
        uuid_dict = {}
        for key, value in uuid.items():
            uuid_list = []
            for i in range(len(value)):
                uuid_list.append(value[i]["uuid"])
            if key == "ip":
                uuid_dict["ip"] = uuid_list
            if key == "port":
                uuid_dict["port"] = uuid_list
            if key == "security":
                uuid_dict["security"] = uuid_list
        return uuid_dict
        
    def cleanup(self, parameter, token, configuration_manager):
        if parameter["initiation_method"] == "ui":
            support.ui_utils.env.teardown()
        
        headers = {"Authorization": token}
        api_server = parameter["api_server"]
        vsys = parameter["vsys"]
        
        if len(configuration_manager["rule_uuid_list"]) > 0:
            rule_type_dict = {
                "security": "security-rules",
                "proxy_intercept": "proxy-intercept-rules",
                "proxy_manipulation": "proxy-manipulation-rules",
                "traffic_shaping": "traffic-shaping-rules",
                "service_chaining": "service-chaining-rules",
                "statistics": "statistics-rules",
                "monitor": "monitor-rules",
                "dos_protection": "dos-protection-rules",
            }
            rule_uuid_list = configuration_manager["rule_uuid_list"]
            if len(rule_uuid_list) > 0:
                for key, value in rule_uuid_list.items():
                    if key == "security":
                        deleted_rule_dict = {"type": key, "ids": [], "vsys_id": 1}
                        # ========24.10 begin========
                        # deleted_rule_dict = {"type": key, "uuids": [], "vsys": 1}
                        # ========24.10 end==========
                    for i in range(len(value)):
                        deleted_rule_dict["ids"] = value[i]
                        deleted_rule_dict["vsys_id"] = vsys
                        url = api_server + "/v1/policy/rule"
                        # ========24.10 begin========
                        # deleted_rule_dict["uuids"] = value[i]
                        # deleted_rule_dict["vsys"] = vsys
                        # url = api_server + "/v1/policies/{}".format(rule_type_dict[key])
                        # ========24.10 end==========
                        response = requests.delete(url, headers=headers, params=deleted_rule_dict, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully.".format(key), flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed.".format(key), flush=True)
               
        if len(configuration_manager["object_uuid_list"]) > 0:
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
            object_uuid_list = configuration_manager["object_uuid_list"]
            if len(object_uuid_list) > 0:
                for key, value in object_uuid_list.items():
                    deleted_object_dict = {"type": key, "ids": [], "vsys_id": 1}
                    # ========24.10 begin========
                    # deleted_object_dict = {"type": key, "uuids": [], "vsys": 1}
                    # ========24.10 end==========
                    for i in range(len(value)):
                        deleted_object_dict["ids"] = value[i]
                        deleted_object_dict["vsys_id"] = vsys
                        url = api_server + "/v1/policy/object"
                        # ========24.10 begin========
                        # deleted_object_dict["uuids"] = value[i]
                        # deleted_object_dict["vsys"] = vsys
                        # url = api_server + "/v1/objects/{}".format(object_type_dict[key])
                        # ========24.10 end==========
                        response = requests.delete(url, headers=headers, params=deleted_object_dict, verify=False)
                        assert response.status_code == 200
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully.".format(key), flush=True)
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed.".format(key), flush=True)
        
if __name__ == "__main__":
    uuid = {
        "ip": [
            {
                "attribute_name": "ATTR_SOURCE_IP",
                "name": "sec_ip",
                "uuid": "111",
                # "negate_option": False
            },
            {
                "attribute_name": "ATTR_SOURCE_IP",
                "name": "sec_ip_2",
                "uuid": "222",
                # "negate_option": False
            }
        ],
        "port": [
            {
                "attribute_name": "ATTR_SOURCE_PORT",
                "name": "sec_port",
                "uuid": "333",
                # "negate_option": False
            }
        ]
    }
    # uuid = {
    #     "security": [
    #         {
    #             "attribute_name": "RULE",
    #             "name": "sec_rule",
    #             "uuid": "111"
    #         }
    #     ]
    # }
    test = CMDBCollector()
    uuid_list = test.collect(uuid)
    parameter = {
        "api_server": "http://192.168.44.72",
        "vsys": 1,
        "initiation_method": "api"
    }
    configuration_manager = {}
    configuration_manager["object_uuid_list"] = uuid_list
    test.cleanup(parameter, "", configuration_manager)