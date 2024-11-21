# -*- coding: UTF-8 -*-
import requests
from datetime import datetime

class DeleteRules:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
    
    def delete_rules(self, rule_uuids_tuple):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        try:
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
            rule_uuids_list = list(rule_uuids_tuple)
            for i in range(len(rule_uuids_list)):
                type = rule_uuids_list[i]["type"]
                deleted_rule_dict = {"uuids": [], "vsys": 1}
                deleted_rule_dict["uuids"].append(rule_uuids_list[i]["uuid"])
                deleted_rule_dict["vsys"] = vsys
                url = api_server + "/v1/policies/{}".format(rule_type_dict[type])
                response = requests.delete(url, headers=self.headers, json=deleted_rule_dict, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} rule successfully.".format(type.replace("_", " ")), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} rule failed.".format(type.replace("_", " ")), flush=True)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting rule, the exception error: ", str(e), flush=True)
            return "" ,"When deleting rule, the exception error: " + str(e)