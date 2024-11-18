# -*- coding: UTF-8 -*-
import ast
import json
import requests
import pymysql.cursors
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
            object_template = root_path + "/support/api_utils/template/object_template.json"
            with open(object_template, 'r', encoding='utf-8') as f:
                object_template_json = json.load(f)
            for key in policy_configuration.keys():
                if key == "and_conditions":
                    condition_temp = policy_configuration[key]
                    object_uuids_list = []
                    for i in range(len(condition_temp)):
                        object_temp = condition_temp[i]["or_conditions"]
                        for j in range(len(object_temp)):
                            if object_temp[j]["type"] not in ["library", "ip_protocol", "boolean", "application"]:
                                object_template_json["vsys"] = vsys
                                if "sub_type" in object_temp[j]:
                                    object_template_json["object"]["sub_type"] = object_temp[j]["sub_type"]
                                if object_temp[j]["type"] == "tunnel":
                                    object_template_json["object"]["member_type"] = "tunnel"
                                else:
                                    object_template_json["object"]["member_type"] = "item"
                                
                                if object_temp[j]["type"] != "tunnel":
                                    object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, object_temp, j, object_temp[j]["type"], "")
                                elif object_temp[j]["type"] == "tunnel":
                                    tunnel = {}
                                    tunnel["action_parameter"] = object_temp[j]["tunnel"]["action_parameter"]                                    
                                    
                                    tunnel["and_conditions"] = []

                                    tunnel_and_conditions = object_temp[j]["tunnel"]["and_conditions"]
                                    for k in range(len(tunnel_and_conditions)):
                                        tunnel["and_conditions"].append({})
                                        tunnel["and_conditions"][k]["negate_option"] = tunnel_and_conditions[k]["negate_option"]
                                        tunnel_or_conditions = tunnel_and_conditions[k]["or_conditions"]
                                        tunnel["and_conditions"][k]["or_conditions"] = []
                                        # tunnel_or_conditions_list = []
                                        for l in range(len(tunnel_or_conditions)):
                                            ip_object_uuids_list = []
                                            ip_object_uuids_list = self.create_common_objects(api_server, ip_object_uuids_list, object_template_json, tunnel_or_conditions, l, "ip", "")
                                            for item in ip_object_uuids_list:
                                                object_ip_uuid_list = []
                                                uuid = item["uuid"]
                                                object_ip_uuid_list.append(uuid)
                                                attribute_name = item["attribute_name"]
                                                or_condition_dict = dict(attribute_name = attribute_name, object_uuids = object_ip_uuid_list)
                                                tunnel["and_conditions"][k]["or_conditions"].append(or_condition_dict)

                                    object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, object_temp, j, "tunnel", tunnel)
                            elif object_temp[j]["type"] in ["ip_protocol", "boolean"] or ("sub_type" not in object_temp[j] and object_temp[j]["type"] == "application"):
                                object_template_json["object"]["type"] = object_temp[j]["type"]
                                if "sub_type" in object_temp[j]:
                                    object_template_json["object"]["sub_type"] = object_temp[j]["sub_type"]
                                item_temp = object_temp[j]["items"]
                                object_uuids_temp_dict = {}
                                object_uuids_temp_dict["uuid"] = self.query_uuids_by_sql(item_temp, api_server, object_temp[j]["type"])
                                object_uuids_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                                object_uuids_list.append(object_uuids_temp_dict)

            object_uuids_tuple = tuple(object_uuids_list)
            return object_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating object, the exception error: ", str(e), flush=True)
            return "" ,"When creating object, the exception error: " + str(e)

    def get_uuids(self, response_dict, type):
        uuid = response_dict["data"]["object"]["uuid"]
        return uuid
    def query_uuids_by_sql(self, item_temp, api_server, type):
        mysql_host = api_server[7:]
        if "https" in api_server:
            mysql_host = api_server[8:]
        if "192.168.44.3" in api_server:
            db = pymysql.connect(host=mysql_host,
                                user='test',
                                password='test@cm',
                                database='tsg-bifang')
        else:
            db = pymysql.connect(host=mysql_host,
                                user='test',
                                password='test',
                                database='tsg-bifang')
        uuid_list = []
        # 该方法用于将字符串类型的['ssl', 'http']转换为list类型的['ssl', 'http']（在无法使用list函数直接转换的情况下）
        for item_name in item_temp:
            if type == "application":
                sql = "select object_uuid from app_id_dict where app_name= 'item_name'"
            elif type == "ip_protocol" or type == "boolean":
                sql = "select uuid from  policy_object where object_name= 'item_name'"
            sql = sql.replace("item_name", item_name)
            # 连接数据库
            mycursor = db.cursor()
            # 根据sql查询
            mycursor.execute(sql)
            # 获取查询结果
            myresult = mycursor.fetchall()
            # 处理查询结果，获取uuid
            uuid = myresult[0][0]
            uuid_list.append(uuid)
        return uuid_list

    def create_common_objects(self, api_server, object_uuids_list, object_template_json, object_temp, j, object_type, item_uuids_list):
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
            if object_type != "tunnel":
                item_temp = object_temp[j]["items"]
                item_list = []
                if object_type == "ip":
                    for t in range(len(item_temp)):
                        item_dict = {}
                        if "ip" in item_temp[t]:
                            item_dict = dict(ip=item_temp[t]["ip"], op=item_temp[t]["op"], interval=item_temp[t]["interval"])
                            item_list.append(item_dict)
                elif object_type in ["fqdn", "url", "keyword", "subscriberid", "account", "mobile_identity", "apn"]:
                    for t in range(len(item_temp)):
                        item_dict = {}
                        item_dict = dict(op=item_temp[t]["op"],expr_type=item_temp[t]["expr_type"],expression=item_temp[t]["expression"])
                        item_list.append(item_dict)
                elif object_type == "port":
                    for t in range(len(item_temp)):
                        item_dict = {}
                        item_dict = dict(op=item_temp[t]["op"], interval=item_temp[t]["interval"])
                        item_list.append(item_dict)
                object_template_json["object"]["items"] = item_list

                object_template_json["object"]["type"] = object_temp[j]["type"]
                object_template_json["object"]["name"] = object_temp[j]["name"]
                url = api_server + "/v1/objects/{}".format(object_type_dict[object_temp[j]["type"]])
                response = requests.post(url, headers=self.headers, json=object_template_json, verify=False)
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_template_json["object"]["type"].replace("_", " ")), flush=True)
                    response_dict = json.loads(response.text)
                    object_uuids = self.get_uuids(response_dict, object_temp[j]["type"])
                    object_uuids_temp_dict = {}
                    object_uuids_temp_dict["type"] = object_temp[j]["type"]
                    object_uuids_temp_dict["uuid"] = object_uuids
                    object_uuids_temp_dict["name"] = object_temp[j]["name"]
                    object_uuids_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                    object_uuids_list.append(object_uuids_temp_dict)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object failed.".format(object_template_json["object"]["type"].replace("_", " ")), flush=True)
                    return "", "Create {} object failed.".format(object_template_json["object"]["type"].replace("_", " ")) 
            if object_type == "tunnel":
                object_template_json["object"]["type"] = object_temp[j]["type"]
                object_template_json["object"]["name"] = object_temp[j]["name"]
                del object_template_json["object"]["items"]
                object_template_json["object"]["tunnel"] = {}
                object_template_json["object"]["tunnel"] = item_uuids_list
                url = api_server + "/v1/objects/{}".format(object_type_dict[object_temp[j]["type"]])
                response = requests.post(url, headers=self.headers, json=object_template_json, verify=False)
            return object_uuids_list
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When running test case, the exception error: ", str(e), flush=True)
            return "When running test case, the exception error: " + str(e)