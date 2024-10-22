#!/usr/bin/python3
# coding=utf-8
import copy
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import requests
import json
from support.api_utils.delete_policy import *
from datetime import datetime


class CreateObject:
    def __init__(self):
        self.ip_ids = []
        self.port_ids = []
        self.imsi_ids = []
        self.phone_number_ids = []
        self.imei_ids = []
        self.apn_ids = []
        self.subid_ids = []
        self.fqdn_ids = []
        self.flag_ids = []
        self.url_ids = []
        self.keywords_ids = []
        self.account_ids = []
        self.http_signature_ids = []
        self.geo_ids = []
        self.geo_name_ids = []

    def create_object_from_template(self, token, parameter, condition, template):
        # 此处的condition为测试用例json中obj_condition_{i}的相关数据
        headers = {"Content-Type": "application/json", "Authorization": token}
        with open(template, 'r', encoding='utf-8') as f:
            obj_template_dict = json.load(f)
        # source_list = []
        # dst_list = []
        # internal_list = []
        # external_list = []
        # filter_list = []
        # flag_list = []
        and_condition_list = []
        condition_ids_by_api_dict = {}  # 搜集所有object通过api创建时返回的id字典
        timeout_result = True

        # 依次创建object
        if len(condition) > 0:
            for key in condition:
                attribute_name = key['attribute_name']
                if "repeat_time" not in key.keys():
                    repeat_time = 1
                else:
                    repeat_time = key["repeat_time"]
                for i in range(repeat_time):
                    index = i + 1
                    objects_list, timeout_result = self.organize_objects_data(obj_template_dict, key, headers, parameter, index, repeat_time)
                    # 构造condi数据，创建策略时的引用数据
                    # if attribute_name in ["ATTR_SOURCE_IP", "ATTR_SUBSCRIBER_ID", "ATTR_SOURCE_PORT", "ATTR_GTP_IMSI", "ATTR_GTP_PHONE_NUMBER", "ATTR_GTP_IMEI", "ATTR_GTP_APN"]:
                    #     for obj_dict in objects_list:
                    #         source_list.append(copy.deepcopy(obj_dict))
                    # elif attribute_name in ["ATTR_DESTINATION_IP", "ATTR_DESTINATION_PORT", "ATTR_DESTINATION_GEO_COUNTRY", "ATTR_SERVER_FQDN"]:
                    #     for obj_dict in objects_list:
                    #         dst_list.append(copy.deepcopy(obj_dict))
                    # elif attribute_name in ["ATTR_EXTERNAL_IP", "ATTR_EXTERNAL_PORT"]:
                    #     for obj_dict in objects_list:
                    #         external_list.append(copy.deepcopy(obj_dict))
                    # elif attribute_name in ["ATTR_INTERNAL_IP", "ATTR_INTERNAL_PORT"]:
                    #     for obj_dict in objects_list:
                    #         internal_list.append(copy.deepcopy(obj_dict))
                    # elif attribute_name == 'ATTR_FLAG':
                    #     for obj_dict in objects_list:
                    #         flag_list.append(copy.deepcopy(obj_dict))
                    # else:
                    #     for obj_dict in objects_list:
                    #         filter_list.append(copy.deepcopy(obj_dict))
                    for obj_dict in objects_list:
                        and_condition_list.append(copy.deepcopy(obj_dict)) 
                    # 删除创建的object，且删除次数等于repeat_time-1，保留最后一次的object用于验证功能
                    if repeat_time > 1:
                        time.sleep(60)
                        if index < repeat_time:
                            create_ip_ids, create_fqdn_ids, create_url_ids, create_port_ids = [], [], [], []
                            cfg_list = {
                                "create_ip_ids": [],
                                "create_port_ids": [],
                                "create_fqdn_ids": [],
                                "create_url_ids": [],
                                "create_subid_ids": [],
                                "create_flag_ids": [],
                                "create_phone_number_ids": [],
                                "create_imei_ids": [],
                                "create_apn_ids":[],
                                "create_imsi_ids": [],
                                "create_keywords_ids": [],
                                "create_account_ids": [],
                                "create_http_signature_ids": [],
                                "create_profile_ids": [],
                                "create_policies_ids": [],
                                "create_geo_name_ids": [],
                                "statistics_sc_info_list": []
                            }
                            if obj_template_dict["object"]["type"] == "ip" and len(self.ip_ids) > 0:
                                create_ip_ids.extend(self.ip_ids)
                                cfg_list["create_ip_ids"] = create_ip_ids
                            if obj_template_dict["object"]["type"] == "fqdn" and len(self.fqdn_ids) > 0:
                                create_fqdn_ids.extend(self.fqdn_ids)
                                cfg_list["create_fqdn_ids"] = create_fqdn_ids
                            if obj_template_dict["object"]["type"] == "url" and len(self.url_ids) > 0:
                                create_url_ids.extend(self.url_ids)
                                cfg_list["create_url_ids"] = create_url_ids
                            if obj_template_dict["object"]["type"] == "port" and len(self.port_ids) > 0:
                                create_port_ids.extend(self.port_ids)
                                cfg_list["create_port_ids"] = create_port_ids
                            delete = DeletePolicy()
                            delete.delele_policy_by_uuid(token, parameter, cfg_list)

        # condition_ids_by_api_dict["src_list"] = source_list
        # condition_ids_by_api_dict["dst_list"] = dst_list
        # condition_ids_by_api_dict["int_list"] = internal_list
        # condition_ids_by_api_dict["ext_list"] = external_list
        # condition_ids_by_api_dict["filter_list"] = filter_list
        # condition_ids_by_api_dict["flag_list"] = flag_list
        condition_ids_by_api_dict["and_conditions"] = and_condition_list
        condition_ids_by_api_dict["ip_ids"] = self.ip_ids
        condition_ids_by_api_dict["subid_ids"] = self.subid_ids
        condition_ids_by_api_dict["port_ids"] = self.port_ids
        condition_ids_by_api_dict["imsi_ids"] = self.imsi_ids
        condition_ids_by_api_dict["imei_ids"] = self.imei_ids
        condition_ids_by_api_dict["apn_ids"] = self.apn_ids
        condition_ids_by_api_dict["phone_number_ids"] = self.phone_number_ids
        condition_ids_by_api_dict["fqdn_ids"] = self.fqdn_ids
        condition_ids_by_api_dict["url_ids"] = self.url_ids
        condition_ids_by_api_dict["flag_ids"] = self.flag_ids
        condition_ids_by_api_dict["keywords_ids"] = self.keywords_ids
        condition_ids_by_api_dict["account_ids"] = self.account_ids
        condition_ids_by_api_dict["http_signature_ids"] = self.http_signature_ids
        condition_ids_by_api_dict["geo_name_ids"] = self.geo_name_ids
        return timeout_result, condition_ids_by_api_dict

    # 对多个objects的处理（处理之后要调用create_object）
    def organize_objects_data(self, obj_template_dict, condition, headers, parameter, index, repeat_time):
        vsys_id = parameter["vsys_id"]
        # object中的is_repeat，用于判定是否需要将数据组建为按照文件读取为多个items的形式
        is_repeat = 0
        is_import = 0
        if repeat_time > 1:
            is_repeat = 1
            is_import = 1

        attribute_name = condition['attribute_name']
        if "objects" in condition.keys():  # 如果是SSL相关True False相关属性则不进行新增操作,直接使用数据
            object_temp_list = []
            object_temp_list.append(copy.deepcopy(condition))
            timeout_result = True
        else:
            obj_type = condition["object_type"]
            obj_template_dict['object']['type'] = obj_type
            obj_template_dict['vsys'] = int(vsys_id)
            obj_sub_type = condition['object_sub_type']
            obj_template_dict['object']['sub_type'] = obj_sub_type
            obj_template_dict['object']['statistics_option'] = 'elaborate'
            if "name" in condition:
                obj_template_dict["object"]["name"] = condition["name"]

            if 'is_negate' in condition.keys():
                is_negate = condition['is_negate']
            else:
                is_negate = 0

            obj_list = condition["object_list"]
            for obj in obj_list:
                add_item_list = obj["add_item_list"]
                if is_import == 0:
                    type_op = "create"
                    member = self.combine_object_data(obj_type, add_item_list, is_repeat)
                    obj_template_dict['object']['items'] = member
                else:
                    type_op = "import"
                    obj_template_dict['object']['statistics_option'] = 'none'
                    obj_template_dict["data"] = {'type': obj_type, 'sub_type': obj_sub_type, 'vsys_id': vsys_id, 'statistics_option': 'elaborate'}
                    obj_template_dict["dry_data"] = {'type': obj_type, 'sub_type': obj_sub_type, 'vsys_id': vsys_id, 'is_dry_run': 1, 'statistics_option': 'elaborate'}
                    for item in add_item_list:
                        object_file = item["keyword_array"][0]
                        file_name = object_file.split("/")[-1]
                        obj_template_dict["file_dry"] = {"file": (file_name, open(object_file, 'rb'), "text/plain")}
                        obj_template_dict["file_import"] = {"file": (file_name, open(object_file, 'rb'), "text/plain")}
                object_ids_temp_list, timeout_result = self.create_or_import_object(type_op, obj_template_dict, headers, parameter, is_repeat)

            objects_list = []
            object_temp_list = []
            if attribute_name != '' and len(object_ids_temp_list) != 0:
                objects_list = self.obj_ids_to_policy_obj_dict(object_ids_temp_list, attribute_name, is_negate)
            if len(objects_list) > 0 and is_repeat == 0:
                object_temp_list.append(objects_list)
            elif len(objects_list) > 0 and is_repeat == 1 and index > repeat_time - 1:
                object_temp_list.append(objects_list)

        return object_temp_list, timeout_result

        # 组织创建通过items进行新增的object的数据

    def combine_object_data(self, obj_type, add_item_list, is_repeat):
        items = []
        object_dict = {}
        geolocation = {}
        if is_repeat == 0:
            if obj_type == "ip":
                for item in add_item_list:
                    tmp_item = {
                        "op": "add",
                        "ip": "5.5.5.6",
                        "interval": "0-65535"
                    }
                    if "op" in item:
                        tmp_item["op"] = item["op"]
                    else:
                        tmp_item["op"] = "add"
                    if "ip" in item:
                        tmp_item["ip"] = item["ip"]
                    else:
                        tmp_item["ip"] = item["ip_address"]
                    # tmp_item["ip"] = item["ip"]
                    if "interval" in item:
                        tmp_item["interval"] = item["interval"]
                    else:
                        tmp_item["interval"] = item["port_range"]
                    # tmp_item["interval"] = item["interval"]
                    items.append(copy.deepcopy(tmp_item))
            elif obj_type == "port":
                for item in add_item_list:
                    tmp_item = {
                        "op": "add",
                        "interval": "0-65535"
                    }
                    tmp_item["op"] = item["op"]
                    tmp_item["interval"] = item["interval"]
                    items.append(copy.deepcopy(tmp_item))
            elif obj_type == "http_signature":
                for item in add_item_list:
                    tmp_item = {
                        "op": "add",
                        "context_name": "Set-Cookie",
                        "expr_type": "and",
                        "expression": "example.com"
                    }
                    tmp_item["op"] = item["op"]
                    tmp_item["context_name"] = item["context_name"]
                    tmp_item["expr_type"] = item["expr_type"]
                    tmp_item["expression"] = item["expression"]
                    items.append(copy.deepcopy(tmp_item))
            elif obj_type in ["fqdn", "subscriberid", "keyword", "url", "account", "mobile_identity", "apn"]:
                for item in add_item_list:
                    tmp_item = {
                        "op": "add",
                        "expr_type": "and",
                        "expression": "example.com"
                    }
                    if "op" in item:
                        tmp_item["op"] = item["op"]
                    else:
                        tmp_item["op"] = "add"
                    if "expr_type" in item:
                        tmp_item["expr_type"] = item["expr_type"]
                    else:
                        tmp_item["expr_type"] = "and"
                    if "expression" in item:
                        tmp_item["expression"] = item["expression"]
                    else:
                        tmp_item["expression"] = item["keyword_array"][0]
                    items.append(copy.deepcopy(tmp_item))
            elif obj_type == "flag":
                for item in add_item_list:
                    tmp_item = {
                        "op": "add",
                        "flag": "64",
                        "mask": "64"
                    }
                    if "op" in item:
                        tmp_item["op"] = item["op"]
                    else:
                        tmp_item["op"] = "add"
                    tmp_item["flag"] = item["flag"]
                    tmp_item["mask"] = item["mask"]
                    items.append(copy.deepcopy(tmp_item))
            elif obj_type == "geolocation":
                geo_ip_address = []
                for item in add_item_list:
                    if 'continent' in item:
                        geolocation['continent'] = item['continent']
                    if 'geoname_id' in item:
                        geolocation['geoname_id'] = item['geoname_id']
                    if 'super_administrative_area' in item:
                        geolocation['super_administrative_area'] = item['super_administrative_area']
                    if 'administrative_area' in item:
                        geolocation['administrative_area'] = item['administrative_area']
                    if 'country_abbr' in item:
                        geolocation['country_abbr'] = item['country_abbr']
                    if 'country' in item:
                        geolocation['country'] = item['country']
                    if 'location_type' in item:
                        geolocation['location_type'] = item['location_type']
                    if 'latitude' in item:
                        geolocation['latitude'] = item['latitude']
                    if 'longitude' in item:
                        geolocation['longitude'] = item['longitude']
                    if 'addr_type' in item:
                        addr_type = item['addr_type']
                    if 'ip_address' in item:
                        ip_address = item['ip_address']
                    geo_ip_address_dict = dict(addr_type=addr_type, ip_address=ip_address, op='add')
                    geo_ip_address.append(geo_ip_address_dict)
                    geolocation['ip_addresses'] = geo_ip_address
            else:
                for item in add_item_list:
                    print("todo...{}".format(item))
        elif is_repeat == 1 and obj_type != 'ip':
            for item in add_item_list:
                patterns = []
                object_file = item["keyword_array"][0]
                with open(object_file, 'r', encoding="utf-8-sig") as file:
                    lines = file.readlines()
                    for line in lines:
                        keywords = line.strip()
                        patterns = []
                        object_dict = dict(keywords=keywords)
                        patterns.append(object_dict)
                        patterns = dict(patterns=patterns)
                        string = dict(string=patterns, op='add')
                        items.append(string)
        elif is_repeat == 1 and obj_type == 'ip':
            for item in add_item_list:
                # patterns = []
                object_file = item["keyword_array"][0]
                with open(object_file, 'r', encoding="utf-8-sig") as file:
                    lines = file.readlines()
                    for line in lines:
                        ip = line.strip()
                        # patterns = []
                        object_dict['ip_address'] = ip
                        object_dict = dict(ip=object_dict, op='add')
                        items.append(object_dict)
        return items

    def create_or_import_object(self, type_op, obj_template_dict, headers, parameter, is_repeat):
        try:
            api_host = parameter["api_server"]
            vsys_id = parameter["vsys_id"]
            obj_type = obj_template_dict['object']['type']
            api_path_map = {
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
            api_path_obj_type = api_path_map.get(obj_type)
            if type_op == "create":
                url = api_host + "/v1/objects/{}".format(api_path_obj_type)
                time1 = datetime.now()
                #print(json.dumps(obj_template_dict))
                response = requests.post(url, headers=headers, json=obj_template_dict, verify=False)
                #print(response.json())
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object successfully.".format(obj_template_dict['object']['type']), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} object failed.".format(obj_template_dict['object']['type']), flush=True)
                time2 = datetime.now()
                time_difference = time2 - time1
                time_difference = time_difference.total_seconds()
                if time_difference > 60:
                    timeout_result = False
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Creating {} object takes too long.".format(obj_template_dict['object']['type']), flush=True)
                else:
                    timeout_result = True
            elif type_op == "import":
                import_url = api_host + "/v1/objects/import"
                if 'Content-Type' in headers:
                    del headers['Content-Type']
                response = requests.post(import_url, data=obj_template_dict["dry_data"], headers=headers, files=obj_template_dict["file_dry"], verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Verify the imported {} object successfully.".format(obj_template_dict['object']['type']), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Verify the imported {} object failed.".format(obj_template_dict['object']['type']), flush=True)
                time1 = datetime.now()
                url = api_host + "/v1/objects/import"
                import_data = obj_template_dict["data"]
                if "sub_type" in import_data:
                    del import_data["sub_type"]
                response = requests.post(url, data=import_data, headers=headers, files=obj_template_dict["file_import"], verify=False)
                time.sleep(20)
                time2 = datetime.now()
                time_difference = time2 - time1
                time_difference = time_difference.total_seconds()
                assert response.status_code == 200
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Import {} object successfully.".format(obj_template_dict['object']['type']), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Import {} object failed.".format(obj_template_dict['object']['type']), flush=True)
                if time_difference > 180:
                    timeout_result = False
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Importing {} object takes too long.".format(obj_template_dict['object']['type']), flush=True)
                else:
                    timeout_result = True

            response_dict = json.loads(response.text)
            object_ids, geo_name_id_list = self.get_object_ids(response_dict, obj_type)

            #print("object_ids: {}".format(object_ids))

            # 是否可取消，待验证？？
            if is_repeat == 1 and obj_type != 'ip':
                self.fqdn_ids = []
                self.url_ids = []
            elif is_repeat == 1 and obj_type == 'ip':
                self.ip_ids = []

            obj_type = obj_template_dict['object']['type']
            if "sub_type" in obj_template_dict['object']:
                object_sub_type = obj_template_dict['object']['sub_type']
            else:
                object_sub_type = ''
            if obj_type == 'ip':
                self.ip_ids = self.handle_ids(object_ids, self.ip_ids)
            elif obj_type == 'port':
                self.port_ids = self.handle_ids(object_ids, self.port_ids)
            elif obj_type == 'mobile_identity' and object_sub_type == "imsi":
                self.imsi_ids = self.handle_ids(object_ids, self.imsi_ids)
            elif obj_type == 'mobile_identity' and object_sub_type == "phone_number":
                self.phone_number_ids = self.handle_ids(object_ids, self.phone_number_ids)
            elif obj_type == 'mobile_identity' and object_sub_type == "imei":
                self.imei_ids = self.handle_ids(object_ids, self.imei_ids)
            elif obj_type == 'apn' and object_sub_type == "apn":
                self.apn_ids = self.handle_ids(object_ids, self.apn_ids)
            elif obj_type == 'subscriberid':
                self.subid_ids = self.handle_ids(object_ids, self.subid_ids)
            elif obj_type == 'fqdn':
                self.fqdn_ids = self.handle_ids(object_ids, self.fqdn_ids)
            elif obj_type == 'flag':
                self.flag_ids = self.handle_ids(object_ids, self.flag_ids)
            elif obj_type == 'url':
                self.url_ids = self.handle_ids(object_ids, self.url_ids)
            elif obj_type == 'keyword':
                self.keywords_ids = self.handle_ids(object_ids, self.keywords_ids)
            elif obj_type == 'account':
                self.account_ids = self.handle_ids(object_ids, self.account_ids)
            elif obj_type == 'http_signature':
                self.http_signature_ids = self.handle_ids(object_ids, self.http_signature_ids)
            elif obj_type == 'geolocation':
                self.geo_ids = self.handle_ids(object_ids, self.geo_ids)
                self.geo_name_ids = self.handle_ids(geo_name_id_list, self.geo_name_ids)

            return object_ids, timeout_result
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    # 获取返回结果中的objectsid
    def get_object_ids(self, response_dict, obj_type):
        temp_list = []
        temp_geo_name_id_list = []
        if obj_type == 'geolocation':
            object_id = response_dict['data']['object']['member']['geolocation']['country_object_id']
            geoname_id = response_dict['data']['object']['member']['geolocation']['geoname_id']
            temp_geo_name_id_list.append(geoname_id)
        else:
            object_id = response_dict['data']['object']['uuid']
        temp_list.append(object_id)
        return temp_list, temp_geo_name_id_list

    # 组织在策略中使用的source,filter等数据
    def obj_ids_to_policy_obj_dict(self, object_ids, attribute_name, is_negate):
        # temp_list = []
        # temp_dict = {
        #     "negate_option": False,
        #     "attribute_name": "ATTR_SUBSCRIBER_ID",
        #     "objects": [
        #         {
        #             "object_uuids": [
        #                 # "157"
        #             ]
        #         }
        #     ]
        # }
        
        and_condition_dict = {
            "negate_option": False,
            "or_conditions": [],
        }
        or_condition_dict = {}
        or_condition_dict["attribute_name"] = attribute_name
        or_condition_dict["object_uuids"] = object_ids
        copy_dict = copy.deepcopy(or_condition_dict)
        and_condition_dict["or_conditions"].append(copy_dict)
        # or_condition_dict.append(and_condition_dict["or_conditions"])
        # print(json.dumps(and_condition_dict))
        return and_condition_dict

    def handle_ids(self, object_ids, target_ids):
        if len(target_ids) != 0 and len(object_ids) != 0:
            for obj in object_ids:
                target_ids.append(obj)
        elif len(target_ids) == 0 and len(object_ids) != 0:
            target_ids = object_ids
        return target_ids


if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")