# -*- coding: UTF-8 -*-
import json
import pymysql
import requests
from datetime import datetime

class CreateLibraries:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
        self.api_server = self.parameter["api_server"]
        self.vsys = self.parameter["vsys"]
        self.root_path = self.parameter["root_path"]
    
    def create_libraries(self, policy_configuration):
        try:
            tag_uuids_tuple, error = self.create_tags(policy_configuration)
            if error:
                return "", error
            catalog_uuids_tuple, error = self.create_catalogs(policy_configuration, tag_uuids_tuple)
            if error:
                return "", error
            # library_uuids_list = []
            # library_uuids_list.append(tag_uuids_tuple)
            # library_uuids_list.append(catalog_uuids_tuple)
            # library_uuids_tuple = tuple(library_uuids_list)
            # return library_uuids_tuple, ""
            return catalog_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating library, the exception error: ", str(e), flush=True)
            return "" ,"When creating library, the exception error: " + str(e)

    def create_tags(self, policy_configuration):
        try:
            tag_template = self.root_path + "/support/api_utils/template/tag_template.json"
            with open(tag_template, 'r', encoding='utf-8') as f:
                tag_template_json = json.load(f)
            for key in policy_configuration.keys():
                if key == "and_conditions":
                    condition_temp = policy_configuration[key]
                    tag_uuids_list = []
                    for i in range(len(condition_temp)):
                        object_temp = condition_temp[i]["or_conditions"]
                        for j in range(len(object_temp)):
                            if object_temp[j]["type"] == "library" and "catalog" in object_temp[j].keys() and len(object_temp[j]["catalog"]) > 0:
                                catalog_temp = object_temp[j]["catalog"]
                                for t in range(len(catalog_temp)):
                                    if "tag" in catalog_temp[t] and len(catalog_temp[t]["tag"]) > 0:
                                        tag_temp = catalog_temp[t]["tag"]
                                        for k in range(len(tag_temp)):
                                            tag_template_json["vsys"] = self.vsys
                                            tag_template_json["tag"]["category"] = tag_temp[k]["category"]
                                            if tag_temp["parent_uuid"] != 0:
                                                tag_template_json["tag"]["parent_uuid"] = self.query_tag_uuid(tag_temp[k]["parent_uuid"])
                                            tag_template_json["tag"]["tag_key"] = tag_temp[k]["tag_key"]
                                            tag_template_json["tag"]["tag_value"] = tag_temp[k]["tag_value"]
                                            url = "{}/v1/library/tags".format(self.api_server)
                                            response = requests.post(headers=self.headers, url=url, json=tag_template_json, verify=False)
                                            if response.status_code == 200:
                                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} tag successfully.".format(tag_temp[k]["category"].replace("_", " ")), flush=True)
                                                response_data = response.json()
                                                tag_uuids_temp_dict = {}
                                                tag_uuids_temp_dict["type"] = "tag"
                                                tag_uuids_temp_dict["uuid"] = response_data["data"]["uuid"]
                                                tag_uuids_temp_dict["name"] = ""
                                                tag_uuids_temp_dict["attribute_name"] = ""
                                                tag_uuids_list.append(tag_uuids_temp_dict)
                                            else:
                                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} tag failed.".format(tag_temp[k]["category"].replace("_", " ")), flush=True)
                                                return "", "Create {} tag failed.".format(tag_temp[k]["category"].replace("_", " "))
            tag_uuids_tuple = tuple(tag_uuids_list)
            return tag_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating tag, the exception error: ", str(e), flush=True)
            return "" ,"When creating tag, the exception error: " + str(e)
        
    def query_tag_uuid(self, tag_value):
        try:
            db = pymysql.connect(host=self.api_server, user='test', password='test', database='tsg-bifang')
            sql = "select uuid from library_tag where tag_value= 'tag_value'"
            sql = sql.replace("tag_value", tag_value)
            mycursor = db.cursor()
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            parent_tag_uuid = myresult[0][0]
            return parent_tag_uuid
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When querying tag, the exception error: ", str(e), flush=True)
            return "" ,"When querying tag, the exception error: " + str(e)
    
    def create_catalogs(self, policy_configuration, tag_uuids_tuple):
        try:
            catalog_template = self.root_path + "/support/api_utils/template/catalog_template.json"
            with open(catalog_template, 'r', encoding='utf-8') as f:
                catalog_template_json = json.load(f)
            tag_uuids_list = list(tag_uuids_tuple)
            for key in policy_configuration.keys():
                if key == "and_conditions":
                    condition_temp = policy_configuration[key]
                    catalog_uuids_list = []
                    for i in range(len(condition_temp)):
                        object_temp = condition_temp[i]["or_conditions"]
                        for j in range(len(object_temp)):
                            if object_temp[j]["type"] == "library" and "catalog" in object_temp[j].keys() and len(object_temp[j]["catalog"]) > 0:
                                catalog_temp = object_temp[j]["catalog"]
                                for t in range(len(catalog_temp)):
                                    catalog_template_json["vsys"] = self.vsys
                                    catalog_template_json["category"] = catalog_temp[t]["category"]
                                    if "ip_entries" in catalog_temp[t].keys() and len(catalog_temp[t]["ip_entries"]) > 0:
                                        catalog_template_json["catalog"]["ip_entries"] = catalog_temp[t]["ip_entries"]
                                    if "fqdn_entries" in catalog_temp[t].keys() and len(catalog_temp[t]["fqdn_entries"]) > 0:
                                        catalog_template_json["catalog"]["fqdn_entries"] = catalog_temp[t]["fqdn_entries"]
                                    if len(tag_uuids_list) == 1:
                                        catalog_template_json["catalog"]["tag_uuids"] = tag_uuids_list[0]["uuid"]
                                    elif len(tag_uuids_list) > 1:
                                        for z in range(len(tag_uuids_list)):
                                            separator = ","  
                                            catalog_template_json["catalog"]["tag_uuids"] = separator.join(tag_uuids_list[z]["uuid"])
                                    url = "{}/v1/library/catalogs".format(self.api_server)
                                    response = requests.post(headers=self.headers, url=url, json=catalog_template_json, verify=False)
                                    if response.status_code == 200:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} catalog successfully.".format(catalog_temp[t]["category"].replace("_", " ")), flush=True)
                                        response_data = response.json()
                                        catalog_uuids_temp_dict = {}
                                        catalog_uuids_temp_dict["type"] = "catalog"
                                        catalog_uuids_temp_dict["uuid"] = response_data["data"]["uuid"]
                                        catalog_uuids_temp_dict["name"] = ""
                                        catalog_uuids_temp_dict["attribute_name"] = ""
                                        catalog_uuids_list.append(catalog_uuids_temp_dict)
                                    else:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} catalog failed.".format(catalog_temp[t]["category"].replace("_", " ")), flush=True)
                                        return "", "Create {} tag failed.".format(catalog_temp[t]["category"].replace("_", " "))
            catalog_uuids_tuple = tuple(catalog_uuids_list)
            return catalog_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating catalog, the exception error: ", str(e), flush=True)
            return "" ,"When creating catalog, the exception error: " + str(e)

if __name__ == "__main__":
    library_uuids_list = [
        {
            "type": "tag",
            "uuid": 123,
            "name": "",
            "attribute_name": ""
        },
        {
            "type": "catalog",
            "uuid": 456,
            "name": "",
            "attribute_name": ""
        }
    ]