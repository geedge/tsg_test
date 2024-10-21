# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import support.ui_utils.env
from datetime import datetime

class CMDBCollector:
    def collect(self, uuid):
        uuid_list = []
        for key, value in uuid.items():
            temp_dict = {}
            if key == "ip" and len(value) > 0:
                temp_dict = [{"ip": ip} for ip in uuid["ip"]]
                uuid_list.extend(temp_dict)
            if key == "port" and len(value) > 0:
                temp_dict = [{"port": port} for port in uuid["port"]]
                uuid_list.extend(temp_dict)
            if key == "security" and len(value) > 0:
                temp_dict = [{"security": security} for security in uuid["security"]]
                uuid_list.extend(temp_dict)
        return uuid_list
        
    def cleanup(self, parameter, token, configuration_manager):
        if parameter["initiation_method"] == "ui":
            support.ui_utils.env.teardown()
        
        headers = {"Authorization": token}
        api_server = parameter["api_server"]
        vsys_id = parameter["vsys_id"]
        
        object_uuid_list = configuration_manager["object_uuid_list"]
        if len(object_uuid_list) > 0:
            deleted_object_dict = {"type": "ip", "ids": [], "vsys_id": 1}
            for i in range(len(object_uuid_list)):
                deleted_object_dict['type'] = list(object_uuid_list[i].keys())[0]
                deleted_object_dict['ids'] = list(object_uuid_list[i].values())[0]
                deleted_object_dict["vsys_id"] = vsys_id
                url = api_server + "/v1/policy/object"
                response = requests.delete(url, headers=headers, params=deleted_object_dict, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully.".format(list(object_uuid_list[i].keys())[0]), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed.".format(list(object_uuid_list[i].keys())[0]), flush=True)
        
        rule_uuid_list = configuration_manager["rule_uuid_list"]
        if len(rule_uuid_list) > 0:
            delete_rule_dict = {"ids": [], "type": "tsg_security", "vsys_id": 1}
            for i in range(len(rule_uuid_list)):
                delete_rule_dict['type'] = list(rule_uuid_list[i].keys())[0]
                delete_rule_dict['ids'] = list(rule_uuid_list[i].values())[0]
                delete_rule_dict['vsys_id'] = vsys_id
                url = api_server + "/v1/policy/rule"
                response = requests.delete(url, headers=headers, params=delete_rule_dict, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully.".format(list(rule_uuid_list[i].keys())[0]), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed.".format(list(rule_uuid_list[i].keys())[0]), flush=True)
        
if __name__ == "__main__":
    # uuid = {
    #     "ip": ["111", "222"],
    #     "port": ["333", "444"]
    # }
    uuid = {
        "security": ["111"]
    }
    test = CMDBCollector()
    uuid_list = test.collect(uuid)
    parameter = {
        "api_server": "http://192.168.44.72",
        "vsys_id": 1
    }
    configuration_manager = {}
    configuration_manager["object_uuid_list"] = uuid_list
    test.cleanup(parameter, "", configuration_manager)