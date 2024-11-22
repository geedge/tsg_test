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
                                if "included_sub_object_uuids" in object_temp[j]:
                                    object_template_json["object"]["included_sub_object_uuids"] = []
                                    include_object_temp = object_temp[j]["included_sub_object_uuids"]
                                    for u in range(len(include_object_temp)):
                                        object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, include_object_temp, u, include_object_temp[u]["type"], "")
                                    filter_object_uuids_list = [item for item in object_uuids_list if "type" in item and item["type"] == object_temp[j]["type"]]  
                                    object_template_json["object"]["included_sub_object_uuids"].append(filter_object_uuids_list[0]["uuid"])
                                if "excluded_sub_object_uuids" in object_temp[j]:
                                    object_template_json["object"]["excluded_sub_object_uuids"] = []
                                    excluded_object_temp = object_temp[j]["excluded_sub_object_uuids"]
                                    for v in range(len(excluded_object_temp)):
                                        object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, excluded_object_temp, v, excluded_object_temp[v]["type"], "")
                                    filter_object_uuids_list = [item for item in object_uuids_list if "type" in item and item["type"] == object_temp[j]["type"]] 
                                    object_template_json["object"]["excluded_sub_object_uuids"].append(filter_object_uuids_list[1]["uuid"])
                                # 调用接口创建group
                                if "included_sub_object_uuids" in object_temp[j]:
                                    object_template_json["object"]["member_type"] = "subordinate"
                                    object_template_json["object"]["statistics_option"] = object_temp[j]["statistics_option"]
                                    if "items" in object_template_json["object"]:
                                        del object_template_json["object"]["items"]
                                    if object_temp[j]["type"] not in ["ip", "mobile_identity"]:
                                        del object_template_json["object"]["sub_type"]
                                    object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, object_temp, u, object_temp[j]["type"], "")
                                if object_temp[j]["type"] != "tunnel" and "included_sub_object_uuids" not in object_temp[j]:
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
                                            object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, tunnel_or_conditions, l, "ip", "")
                                    for s in range(len(object_uuids_list)): 
                                        item = object_uuids_list[s]
                                        object_ip_uuid_list = []
                                        uuid = item["uuid"]
                                        object_ip_uuid_list.append(uuid)
                                        attribute_name = item["attribute_name"]
                                        or_condition_dict = dict(attribute_name = attribute_name, object_uuids = object_ip_uuid_list)
                                        tunnel["and_conditions"][s]["or_conditions"].append(or_condition_dict)

                                    object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, object_temp, j, "tunnel", tunnel)
                            elif object_temp[j]["type"] in ["ip_protocol", "boolean"] or ("sub_type" not in object_temp[j] and object_temp[j]["type"] == "application"):
                                object_template_json["object"]["type"] = object_temp[j]["type"]
                                if "sub_type" in object_temp[j]:
                                    object_template_json["object"]["sub_type"] = object_temp[j]["sub_type"]
                                if "included_sub_object_uuids" in object_temp[j]:
                                    object_uuids_temp_dict = {}
                                    object_template_json["object"]["included_sub_object_uuids"] = []
                                    include_object_temp = object_temp[j]["included_sub_object_uuids"]
                                    for w in range(len(include_object_temp)):
                                        item_temp = include_object_temp[w]["items"]
                                        object_uuids_temp_dict["uuid"] = self.query_uuids_by_sql(item_temp, api_server, object_temp[w]["type"])
                                        object_uuids_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                                        object_uuids_temp_dict["type"] = object_temp[j]["type"]
                                        object_uuids_list.append(object_uuids_temp_dict)
                                    filter_object_uuids_list = [item for item in object_uuids_list if "type" in item and item["type"] == object_temp[j]["type"]]  
                                    object_template_json["object"]["included_sub_object_uuids"]= filter_object_uuids_list[0]["uuid"]
                                if "excluded_sub_object_uuids" in object_temp[j]:
                                    object_template_json["object"]["excluded_sub_object_uuids"] = []
                                    excluded_object_temp = object_temp[j]["excluded_sub_object_uuids"]
                                    for x in range(len(excluded_object_temp)):
                                        item_temp = excluded_object_temp[x]["items"]
                                        object_uuids_temp_dict["uuid"] = self.query_uuids_by_sql(item_temp, api_server, excluded_object_temp[x]["type"])
                                        object_uuids_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                                        object_uuids_temp_dict["type"] = object_temp[j]["type"]
                                        object_uuids_list.append(object_uuids_temp_dict)
                                    filter_object_uuids_list = [item for item in object_uuids_list if "type" in item and item["type"] == object_temp[j]["type"]] 
                                    object_template_json["object"]["excluded_sub_object_uuids"] = filter_object_uuids_list[1]["uuid"]
                                # 调用接口创建group
                                if "included_sub_object_uuids" in object_temp[j]:
                                    object_template_json["object"]["member_type"] = "subordinate"
                                    object_template_json["object"]["statistics_option"] = object_temp[j]["statistics_option"]
                                    if "items" in object_template_json["object"]:
                                        del object_template_json["object"]["items"]
                                    if "sub_type" in object_template_json["object"]:
                                        del object_template_json["object"]["sub_type"]
                                    object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, object_temp, w, object_temp[j]["type"], "")
                                if "included_sub_object_uuids" not in object_temp[j]:
                                    item_temp = object_temp[j]["items"]
                                    object_uuids_temp_dict = {}
                                    object_uuids_temp_dict["uuid"] = self.query_uuids_by_sql(item_temp, api_server, object_temp[j]["type"])
                                    object_uuids_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                                    object_uuids_temp_dict["type"] = object_temp[j]["type"]
                                    object_uuids_list.append(object_uuids_temp_dict)
                            elif object_temp[j]["type"] == "application" and "sub_type" in object_temp[j]:
                                object_template_json["object"]["sub_type"] = object_temp[j]["sub_type"]
                                object_template_json["object"]["type"] = object_temp[j]["type"]
                                if "name" in object_template_json["object"]:
                                    del object_template_json["object"]["name"]
                                application = {}
                                app_surrogates = object_temp[j]["application"]["app_surrogates"]
                                application["app_surrogates"] = []
                                application["app_properties"] = object_temp[j]["application"]["app_properties"]
                                application["app_name"] = object_temp[j]["application"]["app_name"]
                                application["app_longname"] = object_temp[j]["application"]["app_longname"]
                                for m in range(len(app_surrogates)):
                                    application["app_surrogates"].append({})
                                    application["app_surrogates"][m]["group_by"] = app_surrogates[m]["group_by"]
                                    application["app_surrogates"][m]["ordered_match"] = app_surrogates[m]["ordered_match"]
                                    application["app_surrogates"][m]["signature_sequence"] = []
                                    application["app_surrogates"][m]["signature_sequence"].append({})
                                    signature_sequence = app_surrogates[m]["signature_sequence"]
                                    # 在signature_sequence中配置signature_uuid
                                    for n in range(len(signature_sequence)):
                                        signature = {}
                                        signature["and_conditions"] = []
                                        signature["name"] = signature_sequence[n]["signature"]["name"]
                                        signature["is_enabled"] = signature_sequence[n]["signature"]["is_enabled"]
                                        signature_and_conditions = signature_sequence[n]["signature"]["and_conditions"]
                                        for o in range(len(signature_and_conditions)):
                                            signature["and_conditions"].append({})
                                            signature["and_conditions"][o]["negate_option"] = signature_and_conditions[o]["negate_option"]
                                            signature["and_conditions"][o]["or_conditions"] = []
                                            signature_object_temp = signature_and_conditions[o]["or_conditions"]
                                            for p in range(len(signature_and_conditions)):
                                                if signature_object_temp[p]["type"] not in ["library", "ip_protocol", "boolean", "application"]:
                                                    object_template_json["vsys"] = vsys
                                                    if "sub_type" in signature_object_temp[p]:
                                                        object_template_json["object"]["sub_type"] = signature_object_temp[p]["sub_type"]
                                                    if signature_object_temp[p]["type"] == "tunnel":
                                                        object_template_json["object"]["member_type"] = "tunnel"
                                                    else:
                                                        object_template_json["object"]["member_type"] = "item"
                                                    
                                                    if signature_object_temp[p]["type"] != "tunnel":
                                                        # 创建objects
                                                        for r in range(len(signature_object_temp)):
                                                            # 此时代表自定义attrbute
                                                            if "user_defined_attribute" in signature_object_temp[r]:
                                                                user_defined_attribute_temp = signature_object_temp[r]["user_defined_attribute"]
                                                                object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, object_temp, p, "user_defined_attribute", user_defined_attribute_temp)
                                                            object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, signature_object_temp, p, signature_object_temp[p]["type"], "")
                                                            signature_object_list = [item for item in object_uuids_list if "type" in item and item["type"] != "user_defined_attribute"] 
                                                            for item in signature_object_list:
                                                                signature_object_uuid_list = []
                                                                uuid = item["uuid"]
                                                                signature_object_uuid_list.append(uuid)
                                                                if "user_defined_attribute" in signature_object_temp[r]:
                                                                    attribute_name  = signature_object_temp[r]["user_defined_attribute"]["name"]
                                                                else:
                                                                    attribute_name = item["attribute_name"]
                                                                or_condition_dict = dict(attribute_name = attribute_name, object_uuids = signature_object_uuid_list)
                                                                signature["and_conditions"][r]["or_conditions"].append(or_condition_dict)
                                                        # 创建signature
                                                        signature_dict = dict(vsys = vsys, signature = signature, return_data = 1)
                                                        object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, signature_object_temp, n, "signature", signature_dict)
                                        # 提取signature，组织application数据
                                        for t in range(len(object_uuids_list)):
                                            if object_uuids_list[t]["type"] == "signature":
                                                signature_uuid = object_uuids_list[t]["uuid"]
                                                application["app_surrogates"][m]["signature_sequence"][m]["signature_uuid"] = signature_uuid
                                                application["app_surrogates"][m]["signature_sequence"][m]["exclude"] = signature_sequence[m]["exclude"]
                                object_template_json["object"]["application"] = application
                                if "name" in object_template_json["object"]:
                                    del object_template_json["object"]["name"]
                                if "items" in object_template_json["object"]:
                                    del object_template_json["object"]["items"]
                                # 请求接口创建application
                                object_uuids_list = self.create_common_objects(api_server, object_uuids_list, object_template_json, object_temp, j, "application", "")
            object_uuids_tuple = tuple(object_uuids_list)
            return object_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating object, the exception error: ", str(e), flush=True)
            return "" ,"When creating object, the exception error: " + str(e)

    def get_uuids(self, response_dict, type):
        if type not in ["signature", "user_defined_attribute"]:
            uuid = response_dict["data"]["object"]["uuid"]
        else:
            uuid = response_dict["data"]["uuid"]
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
                    "tunnel_level": "tunnel-levels",
                }
            if object_type not in ["tunnel", "application", "signature", "user_defined_attribute"] and "included_sub_object_uuids" not in object_temp[j]:
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
                elif object_type in ["port", "interval"]:
                    for t in range(len(item_temp)):
                        item_dict = {}
                        item_dict = dict(op=item_temp[t]["op"], interval=item_temp[t]["interval"])
                        item_list.append(item_dict)
                elif object_type == "flag":
                    for t in range(len(item_temp)):
                        item_dict = {}
                        flag, mask = self.escape_flags_data(item_temp[t]["flag"])
                        item_dict = dict(op=item_temp[t]["op"], flag = str(flag), mask = str(mask))
                        item_list.append(item_dict)
                object_template_json["object"]["items"] = item_list
                object_template_json["object"]["type"] = object_temp[j]["type"]
                object_template_json["object"]["name"] = object_temp[j]["name"]
            elif "included_sub_object_uuids" in object_temp[j]:
                object_template_json["object"]["type"] = object_temp[j]["type"]
                object_template_json["object"]["name"] = object_temp[j]["name"]
                # object_template_json["object"]["member_type"] = "application"
            elif object_type == "tunnel":
                object_template_json["object"]["type"] = object_temp[j]["type"]
                object_template_json["object"]["name"] = object_temp[j]["name"]
                if "items" in object_template_json["object"]:
                    del object_template_json["object"]["items"]
                object_template_json["object"]["tunnel"] = {}
                object_template_json["object"]["tunnel"] = item_uuids_list
            elif object_type == "application":
                object_template_json["object"]["type"] = object_temp[j]["type"]
                object_template_json["object"]["member_type"] = "application"
            if object_type != "signature" and object_type != "user_defined_attribute":
                if object_type == "application" and object_template_json["object"]["member_type"] == "subordinate":
                    url = api_server + "/v1/objects/application-groups"
                else:
                    url = api_server + "/v1/objects/{}".format(object_type_dict[object_temp[j]["type"]])
                response = requests.post(url, headers=self.headers, json=object_template_json, verify=False)
            elif object_type == "signature":
                url = api_server + "/v1/objects//applications/customized-signatures"
                response = requests.post(url, headers=self.headers, json=item_uuids_list, verify=False)
            elif object_type == "user_defined_attribute":
                url = api_server + "/v1/objects/applications/customized-attributes"
                file_path = item_uuids_list["file_path"]
                del item_uuids_list["file_path"]
                root_path = self.parameter["root_path"].replace("\\","/")
                user_defined_attribute_data = item_uuids_list
                user_defined_attribute_data["vsys"] = self.parameter["vsys"]
                user_defined_attribute_data["return_data"] = 1
                files = {"file": (
                file_path, open("{}/support/configuration_management/profile/{}".format(root_path, file_path), 'rb'), "text/plain")}
                temp_headers = self.headers
                del temp_headers["Content-Type"]
                response = requests.post(url=url, data=user_defined_attribute_data, headers=self.headers, files=files, verify=False)
            if response.status_code == 200:
                if "included_sub_object_uuids" not in object_temp[j]:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(object_type), flush=True)
                elif "included_sub_object_uuids" in object_temp[j]:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object group successfully.".format(object_type), flush=True)
                response_dict = json.loads(response.text)
                object_uuids = self.get_uuids(response_dict, object_type)
                object_uuids_temp_dict = {}
                if object_type not in ["signature", "user_defined_attribute"]:
                    object_uuids_temp_dict["type"] = object_temp[j]["type"]
                elif object_type == "signature":
                    object_uuids_temp_dict["type"] = "signature"
                elif object_type == "user_defined_attribute":
                    object_uuids_temp_dict["type"] = "user_defined_attribute"
                object_uuids_temp_dict["uuid"] = object_uuids
                if object_type == "user_defined_attribute":
                    object_uuids_temp_dict["name"] = user_defined_attribute_data["name"]
                elif object_type == "application":
                    object_uuids_temp_dict["name"] = object_temp[j]["application"]["app_name"]
                else:
                    object_uuids_temp_dict["name"] = object_temp[j]["name"]
                if object_type != "signature":
                    object_uuids_temp_dict["attribute_name"] = object_temp[j]["attribute_name"]
                object_uuids_list.append(object_uuids_temp_dict)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object failed.".format(object_template_json["object"]["type"].replace("_", " ")), flush=True)
                return "", "Create {} object failed.".format(object_template_json["object"]["type"].replace("_", " ")) 
            return object_uuids_list
        except Exception as e:
            exception_result = str(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When running test case, the exception error: ", str(e), flush=True)
            return "When running test case, the exception error: " + str(e)
    
    def escape_flags_data(self, config):
        # 初始化 flag 和 mask
        flag = 0
        mask = 0
        # 根据输入字典里的值设置 flag 和 mask，第0位不对应任何flag，从第1位开始
        if 'Bulky' in config:
            flag |= (1 << 1) if config['Bulky'] else 0
            mask |= (1 << 1)
        if 'CBR Streaming' in config:
            flag |= (1 << 2) if config['CBR Streaming'] else 0
            mask |= (1 << 2)
        if 'Client is Local' in config:
            flag |= (1 << 3) if config['Client is Local'] else 0
            mask |= (1 << 3)
        if 'Server is Local' in config:
            flag |= (1 << 4) if config['Server is Local'] else 0
            mask |= (1 << 4)
        if 'Download' in config:  
            flag |= (1 << 5) if config['Download'] else 0
            mask |= (1 << 5)
        if 'Interactive' in config:
            flag |= (1 << 6) if config['Interactive'] else 0
            mask |= (1 << 6)
        if 'Inbound' in config:
            flag |= (1 << 7) if config['Inbound'] else 0
            mask |= (1 << 7)
        if 'Outbound' in config:
            flag |= (1 << 8) if config['Outbound'] else 0
            mask |= (1 << 8)
        if 'Pseudo Unidirectional' in config:
            flag |= (1 << 9) if config['Pseudo Unidirectional'] else 0
            mask |= (1 << 9)
        if 'Streaming' in config:
            flag |= (1 << 10) if config['Streaming'] else 0
            mask |= (1 << 10)
        if 'Unidirectional' in config:
            flag |= (1 << 11) if config['Unidirectional'] else 0
            mask |= (1 << 11)
        if 'Random looking' in config:
            flag |= (1 << 12) if config['Random looking'] else 0
            mask |= (1 << 12)
        if 'C2S' in config:
            flag |= (1 << 13) if config['C2S'] else 0
            mask |= (1 << 13)
        if 'S2C' in config:
            flag |= (1 << 14) if config['S2C'] else 0
            mask |= (1 << 14)
        if 'Bidirectional' in config:
            flag |= (1 << 15) if config['Bidirectional'] else 0
            mask |= (1 << 15)
        if 'Tunneling' in config:
            flag |= (1 << 16) if config['Tunneling'] else 0
            mask |= (1 << 16)
        return flag, mask