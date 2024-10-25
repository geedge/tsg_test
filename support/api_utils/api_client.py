# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import json
import requests
from support.api_utils.log_in import LogIn
from datetime import datetime
from support.packet_generator.workpath import workdir
from support.api_utils.get_application_id import get_group_id

class APIClient:
    def __init__(self, parameter):
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        self.token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        self.headers = {"Content-Type": "application/json", "Authorization": self.token}
        self.api_server = parameter["api_server"]
        self.vsys = parameter["vsys"]
        self.root_path = parameter["root_path"]
        
    def create_object(self, policy_configuration):
        try:
            object_template = self.root_path + "/support/api_utils/template/object_template.json"
            with open(object_template, 'r', encoding='utf-8') as f:
                object_template_json = json.load(f)
            object_uuid_dict = {}
            for key in policy_configuration.keys():
                if key == "and_conditions":
                    condition_temp = policy_configuration[key]
                    ip_uuid_temp_list = []
                    port_uuid_temp_list = []
                    for i in range(len(condition_temp)):
                        object_temp = condition_temp[i]["or_conditions"]
                        for j in range(len(object_temp)):
                            if object_temp[j]["type"] != "application":
                                object_template_json["vsys_id"] = self.vsys
                                object_template_json["object"]["type"] = object_temp[j]["type"]
                                object_template_json["object"]["name"] = object_temp[j]["name"]
                                object_template_json["object"]["sub_type"] = object_temp[j]["sub_type"]
                                item_temp = object_temp[j]["items"]
                                item_list = []
                                if object_temp[j]["type"] == "ip":
                                    for t in range(len(item_temp)):
                                        item_dict = {}
                                        if "ip" in item_temp[t]:
                                            item_dict["ip"] = item_temp[t]["ip"]
                                            item_dict = dict(ip=item_dict, op=item_temp[t]["op"])
                                            item_list.append(item_dict)
                                member = dict(items=item_list, type="item")
                                object_template_json["object"]["member"] = member
                                url = self.api_server + "/v1/policy/object"
                                response = requests.post(url, headers=self.headers, json=object_template_json, verify=False)
                                if response.status_code == 200:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_template_json["object"]["type"]), flush=True)
                                    response_dict = json.loads(response.text)
                                    object_uuid, object_geo_uuid = self.get_uuid(response_dict, object_temp[j]["type"])
                                    object_uuid_temp_dict = {}
                                    object_uuid_temp_dict["name"] = object_temp[j]["name"]
                                    object_uuid_temp_dict["uuid"] = object_uuid
                                    object_uuid_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                                    # object_uuid_temp_dict["negate_option"] = condition_temp[i]["negate_option"]
                                    if object_temp[j]["type"] == "ip":
                                        ip_uuid_temp_list.append(object_uuid_temp_dict)
                                    elif object_temp[j]["type"] == "port":
                                        port_uuid_temp_list.append(object_uuid_temp_dict)
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object failed.".format(object_template_json["object"]["type"]), flush=True)
                                    return "", "Create {} object failed.".format(object_template_json["object"]["type"])
                    if len(ip_uuid_temp_list) > 0:
                        object_uuid_dict["ip"] = ip_uuid_temp_list
                    if len(port_uuid_temp_list) > 0:
                        object_uuid_dict["port"] = port_uuid_temp_list
            return object_uuid_dict, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create object exception error: ", str(e), flush=True)
            return "" ,"Create object exception error: " + str(e)
    
    def get_uuid(self, response_dict, type):
        if type == "ip":
            # uuid = response_dict["data"]["object"]["uuid"]
            uuid = response_dict["data"]["object"]["id"]
            return uuid, ""
        elif type == "security":
            # uuid = response_dict["data"]["rule"]["uuid"]
            uuid = response_dict["data"]["rule"]["id"]
            return uuid
        elif type == "geolocation":
            uuid = ""
            geo_name_uuid = ""
            print("to be added...")
            return uuid, geo_name_uuid
    
    def create_profile(self, policy_configuration):
        print("to be added...")
        
    def create_rule(self, policy_configuration, object_uuid):
        try:
            rule_template = self.root_path + "/support/api_utils/template/rule_template.json"
            with open(rule_template, 'r', encoding='utf-8') as f:
                rule_template_json = json.load(f)
            rule_uuid_dict = {}
            rule_template_json["rule"]["name"] = policy_configuration["name"]
            rule_template_json["rule"]["type"] = policy_configuration["type"]
            rule_template_json["rule"]["action"] = policy_configuration["action"]
            rule_template_json["rule"]["vsys_id"] = self.vsys
            rule_template_json["vsys_id"] = self.vsys
            # rule_template_json["rule"]["do_log"] = 2
            rule_template_json["rule"]["is_enabled"] = policy_configuration["is_enabled"]
            source_condition_temp_list, destination_condition_temp_list, application_condition_temp_list = [], [], []
            for i in range(len(policy_configuration["and_conditions"])):
                if "attr_source" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    source_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_destination" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    destination_condition_temp_list.append(policy_configuration["and_conditions"][i])
                if "attr_app" in policy_configuration["and_conditions"][i]["or_conditions"][0]["attribute_name"].lower():
                    application_condition_temp_list.append(policy_configuration["and_conditions"][i])
            if len(source_condition_temp_list) > 0:
                rule_template_json["rule"]["source"] = self.generate_rule_condition_list(source_condition_temp_list, object_uuid, "attr_source")
            if len(destination_condition_temp_list) > 0:
                rule_template_json["rule"]["destination"] = self.generate_rule_condition_list(destination_condition_temp_list, object_uuid, "attr_destination")
            if len(application_condition_temp_list) > 0:
                rule_template_json["rule"]["application"] = self.generate_rule_condition_list(application_condition_temp_list, object_uuid, "attr_app")
            if len(policy_configuration["action_parameter"]) > 0:
                if policy_configuration["type"] == "security" and policy_configuration["action"] == "deny":
                    rule_template_json["rule"]["user_region"]["method"] = policy_configuration["action_parameter"]["sub_action"]
                    rule_template_json["rule"]["user_region"]["packet_capture"] = {}
                    rule_template_json["rule"]["user_region"]["packet_capture"]["enable"] = policy_configuration["action_parameter"]["packet_capture"]["enable"]
                    rule_template_json["rule"]["user_region"]["after_n_packets"] = policy_configuration["action_parameter"]["after_n_packets"]
                    rule_template_json["rule"]["user_region"]["send_icmp_unreachable"] = policy_configuration["action_parameter"]["send_icmp_unreachable"]
                    rule_template_json["rule"]["user_region"]["send_tcp_reset"] = policy_configuration["action_parameter"]["send_tcp_reset"]
            rule_template_json["rule"]["internal"] = []
            rule_template_json["rule"]["external"] = []
            rule_template_json["rule"]["flag"] = None
            url = self.api_server + "/v1/policy/rule"
            response = requests.post(url, headers=self.headers, json=rule_template_json, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule successfully.".format(policy_configuration["type"]), flush=True)
                response_dict = json.loads(response.text)
                uuid = self.get_uuid(response_dict, policy_configuration["type"])
                rule_uuid_temp_dict = {}
                rule_uuid_temp_dict["name"] = policy_configuration["name"]
                rule_uuid_temp_dict["uuid"] = uuid
                rule_uuid_temp_dict["attribute_name"] = policy_configuration["type"].upper() + "_" + "RULE"
                rule_uuid_temp_list = []
                rule_uuid_temp_list.append(rule_uuid_temp_dict)
                if policy_configuration["type"] == "security":
                    rule_uuid_dict["security"] = rule_uuid_temp_list
                elif policy_configuration["type"] == "monitor":
                    rule_uuid_dict["monitor"] = rule_uuid_temp_list
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} rule failed.".format(policy_configuration["type"]), flush=True)
                return "", "Create {} rule failed.".format(policy_configuration["type"])
            return rule_uuid_dict, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create rule exception error: ", str(e), flush=True)
            return "", "Create rule exception error: " + str(e)
    
    def generate_rule_condition_list(self, and_condition, object_uuid, condition_type):
        if condition_type in ["attr_source", "attr_destination"]:
            condition_list = []
            for i in range(len(and_condition)):
                is_negate = and_condition[i]["negate_option"]
                attribute_name = and_condition[i]["or_conditions"][0]["attribute_name"]
                objects_configuration = and_condition[i]["or_conditions"]
                object_list = []
                object_uuids = []
                for j in range(len(objects_configuration)):
                    object_uuid_temp = object_uuid[objects_configuration[0]["type"]]
                    for t in range(len(object_uuid_temp)):
                        if objects_configuration[j]["name"] == object_uuid_temp[t]["name"]:
                            object_uuids.append(object_uuid_temp[t]["uuid"])
                object_temp_dict = dict(object_ids=object_uuids)
                object_list.append(object_temp_dict)
                temp_dict = dict(objects=object_list, attribute_name=attribute_name, is_negate=is_negate)
                condition_list.append(temp_dict)
            return condition_list
        if condition_type == "attr_app":
            is_negate = and_condition[0]["negate_option"]
            application_name_list = []
            application_id_list = []
            application_configuration = and_condition[0]["or_conditions"]
            for i in range(len(application_configuration)):
                application_name = application_configuration[i]["items"]
                application_id_temp_list = []
                for j in range(len(application_name)):
                    application_name_list.append(application_name[j])
                    application_id = get_group_id(str(application_name_list), self.api_server)
                    application_id_temp_list.append(application_id)
                application_id_dict = dict(object_ids=application_id_temp_list[len(application_id_temp_list)-1])
                application_id_list.append(application_id_dict)
            application_dict = dict(objects=application_id_list, attribute_name='ATTR_APP_ID', is_negate=is_negate)
            return application_dict
    
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.86",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "debug": "local",
        "initiation_method": "api",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 5,
        "root_path": workdir,
        "path": workdir + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    api_client = APIClient(parameter)
    from support.cmdb_collector import CMDBCollector
    cmdb_collector = CMDBCollector()
    configuration_manager = {}
    """
    # object_uuid = {
    #     "ip": [
    #         {
    #             "attribute_name": "ATTR_SOURCE_IP",
    #             "name": "sec_srcip",
    #             "uuid": "111",
    #             "negate_option": False
    #         },
    #         {
    #             "attribute_name": "ATTR_SOURCE_IP",
    #             "name": "sec_srcip_2",
    #             "uuid": "222",
    #             "negate_option": False
    #         },
    #         {
    #             "attribute_name": "ATTR_SOURCE_IP",
    #             "name": "sec_srcip_3",
    #             "uuid": "333",
    #             "negate_option": False
    #         }
    #     ],
    #     "port": [
    #         {
    #             "attribute_name": "ATTR_SOURCE_PORT",
    #             "name": "sec_port",
    #             "uuid": "444",
    #             "negate_option": False
    #         }
    #     ]
    # }
    """
    policy_configuration = {
        "name": "automation_test_zk",
        "type": "security",
        "action": "deny",
        "and_conditions": [ # 一个rule选了两个source、一个destination、一个application
            {
                "negate_option": 0,
                "or_conditions": [ # 一个source ip address选了两个object
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip",
                        "items": [ # 一个object中包含多个item
                            {
                                "op": "add",
                                "ip": "1.1.1.1",
                                "interval": "0-65535"
                            },
                            {
                                "op": "add",
                                "ip": "2.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    },
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip_2",
                        "items": [
                            {
                                "op": "add",
                                "ip": "3.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip_3",
                        "items": [
                            {
                                "op": "add",
                                "ip": "4.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_DESTINATION_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip_4",
                        "items": [
                            {
                                "op": "add",
                                "ip": "5.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_APP_ID",
                        "type": "application",
                        "items": ["http", "ssl"]
                    }
                ],
            }
        ],
        "action_parameter": {
            "sub_action": "drop",
            "packet_capture": {
                "enable": 0
            },
            "send_tcp_reset": 1,
            "send_icmp_unreachable": 0,
            "after_n_packets": 1
        },
        "is_enabled": 1
    }
    object_uuid, _ = api_client.create_object(policy_configuration)
    configuration_manager["object_uuid_list"] = cmdb_collector.collect(object_uuid)
    rule_uuid, _ = api_client.create_rule(policy_configuration, object_uuid)
    configuration_manager["rule_uuid_list"] = cmdb_collector.collect(rule_uuid)
    temp = json.dumps(configuration_manager)
    print(temp)
    api_client.generate_rule_condition_list(policy_configuration, object_uuid, "source")