#!/usr/bin/python3
# coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import requests
import json
from support.api_utils.delete_config import DeleteConfig
from datetime import datetime

class CreateObject():
    def __init__(self):
        self.ip_ids = []
        self.subid_ids = []
        self.fqdn_ids = []
        self.flag_ids = []
        self.url_ids = []
        self.keywords_ids = []
        self.account_ids = []
        self.http_signature_ids = []
        self.geo_ids = []
        self.geo_name_ids = []

    def create_object_from_template(self, token, parameter, condition, template, api_host, vsys_id):
        # 此处的condition为测试用例json中obj_condition_{i}的相关数据
        headers = {"Content-Type": "application/json", "Authorization": token}
        with open(template, 'r', encoding='utf-8') as f:
            obj_template_dict = json.load(f)
        source_list = []
        dst_list = []
        filter_list = []
        flag_list = []
        timeout_result = True

        test_pc_ip = parameter['test_pc_ip']
        test_subcriber_id = parameter['test_subcriber_id']
        
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
                    objects_list, timeout_result = self.organize_objects_data(obj_template_dict, key, headers, api_host, test_pc_ip, test_subcriber_id, vsys_id, index, repeat_time)
                    if attribute_name == 'ATTR_SOURCE_IP' or attribute_name == 'ATTR_SUBSCRIBER_ID':
                        for obj_dict in objects_list:
                            source_list.append(obj_dict)
                    elif attribute_name == 'ATTR_DESTINATION_IP' or attribute_name == "ATTR_DESTINATION_GEO_COUNTRY" or attribute_name == "ATTR_SERVER_FQDN":
                        for obj_dict in objects_list:
                            dst_list.append(obj_dict)
                    elif attribute_name == 'ATTR_FLAG':
                        for obj_dict in objects_list:
                            flag_list.append(obj_dict)
                    else:
                        for obj_dict in objects_list:
                            filter_list.append(obj_dict)
                    
                    # 删除创建的object，且删除次数等于repeat_time-1，保留最后一次的object用于验证功能
                    if repeat_time > 1:
                        time.sleep(60)
                        if index < repeat_time:
                            create_ip_ids, create_fqdn_ids, create_url_ids = [], [], []
                            cfg_list = {
                                "create_ip_ids": [],
                                "create_fqdn_ids": [],
                                "create_url_ids": [],
                                "create_subid_ids": [],
                                "create_flag_ids": [],
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
                            erase = DeleteConfig()
                            erase.delele_cfg(token, parameter, cfg_list)
        
        return timeout_result, source_list, dst_list, filter_list, flag_list, self.ip_ids, self.subid_ids, self.fqdn_ids, self.url_ids, self.flag_ids, self.keywords_ids, self.account_ids, self.http_signature_ids, self.geo_name_ids
    
    # 对多个objects的处理（处理之后要调用create_object）
    def organize_objects_data(self, obj_template_dict, condition, headers, api_host, test_pc_ip, test_subcriber_id, vsys_id, index, repeat_time):
        # object中的is_repeat，用于判定是否需要将数据组建为按照文件读取为多个items的形式
        is_repeat = 0
        is_import = 0
        if repeat_time > 1:
            is_repeat = 1
            is_import = 1
        
        attribute_name = condition['attribute_name']
        
        obj_type = condition["object_type"]
        obj_template_dict['object']['type'] = obj_type
        
        obj_sub_type = condition['object_sub_type']
        obj_template_dict['object']['sub_type'] = obj_sub_type
        obj_template_dict['object']['statistics_option'] = 'elaborate'
        
        if 'is_negate' in condition.keys():
            is_negate = condition['is_negate']
        else:
            is_negate = 0

        obj_template_dict['vsys_id'] = vsys_id
        
        obj_list = condition["object_list"]
        for obj in obj_list:
            add_item_list = obj["add_item_list"]
            if "context_name" in obj.keys():
                context_name = obj['context_name']
            else:
                context_name = ''
            if is_import == 0:
                type = "create"
                member = self.combine_object_data(obj_type, obj_sub_type, add_item_list, test_pc_ip, test_subcriber_id, context_name, is_repeat)
                obj_template_dict['object']['member'] = member
            else:
                type = "import"
                obj_template_dict["data"] = {'type': obj_type, 'sub_type': obj_sub_type, 'vsys_id': vsys_id, 'statistics_option': 'elaborate'}
                obj_template_dict["dry_data"] = {'type': obj_type, 'sub_type': obj_sub_type, 'vsys_id': vsys_id, 'is_dry_run': 1, 'statistics_option': 'elaborate'}
                for item in add_item_list:
                    object_file = item["keyword_array"][0]
                    file_name = object_file.split("/")[-1]
                    obj_template_dict["file_dry"] = {"file":(file_name, open(object_file, 'rb'), "text/plain")}
                    obj_template_dict["file_import"] = {"file":(file_name, open(object_file, 'rb'), "text/plain")}
            object_ids_temp_list, timeout_result = self.create_or_import_object(type, obj_template_dict, headers, api_host, is_repeat)
        
        objects_list = []
        object_temp_list = []
        if attribute_name != '' and len(object_ids_temp_list) != 0:
            objects_list = self.obj_ids_to_policy_obj_list(object_ids_temp_list, attribute_name, is_negate)
        if len(objects_list) > 0 and is_repeat == 0:
            object_temp_list.append(objects_list)
        elif len(objects_list) > 0 and is_repeat == 1 and index > repeat_time-1:
            object_temp_list.append(objects_list)
        
        return object_temp_list, timeout_result 
    
    # 组织创建通过items进行新增的object的数据
    def combine_object_data(self, obj_type, obj_sub_type, add_item_list, test_pc_ip, test_subcriber_id, context_name, is_repeat):
        items = []
        object_dict = {}
        geolocation = {}
        if is_repeat == 0:
            if obj_type == "ip":
                for item in add_item_list:
                    if 'ip_cidr' in item:
                        object_dict['ip_cidr'] = item['ip_cidr']
                    if 'ip_range' in item:
                        object_dict['ip_range'] = item['ip_range']
                    if 'ip_address' in item:
                        ip_temp = item['ip_address']
                        if ip_temp == 'default':
                            object_dict['ip_address'] = test_pc_ip
                        else:
                            object_dict['ip_address'] = item['ip_address']
                    if 'port' in item:
                        object_dict['port'] = item['port']
                    # if 'port_range' in item:
                    #     object_dict['port_range'] = item['port_range']
                    if 'protocol' in item:
                        object_dict['protocol'] = item['protocol']
                    if 'addr_type' in item:
                        object_dict['addr_type'] = item['addr_type']
                    object_dict = dict(ip=object_dict, op='add')
                    items.append(object_dict)
            elif obj_type == "flag":
                for item in add_item_list:
                    if 'flag' in item:
                        object_dict['flag'] = item['flag']
                    if 'mask' in item:
                        object_dict['mask'] = item['mask']
                    object_dict = dict(flag=object_dict, op='add')
                    items.append(object_dict)
                member = dict(items=items, type=1)            
            elif obj_type == "http_signature":
                for item in add_item_list:
                    patterns = []
                    keywords = item["keyword_array"][0]
                    object_dict = dict(keywords=keywords)
                    patterns.append(object_dict)
                    patterns = dict(patterns=patterns)
                    string = dict(contextual_string=patterns, op='add')
                    string['contextual_string']['context_name'] = context_name
                    items.append(string)
            elif obj_type == "geolocation":
                geo_ip_address = []
                # geo_ip_address_dict = {}
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
                    geo_ip_address_dict = dict(addr_type = addr_type, ip_address = ip_address, op = 'add')    
                    geo_ip_address.append(geo_ip_address_dict)
                    geolocation['ip_addresses'] = geo_ip_address
            else:
                for item in add_item_list:
                    patterns = []
                    keywords = item["keyword_array"][0]
                    if obj_type == "subscriberid" and keywords == "default":
                        keywords = '$' + test_subcriber_id
                    object_dict = dict(keywords=keywords)
                    patterns.append(object_dict)
                    patterns = dict(patterns=patterns)
                    string = dict(string=patterns, op='add')
                    items.append(string)                 
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
        if obj_type == 'geolocation':
            member = dict(geolocation = geolocation, type = 'library')
        else:
            member = dict(items=items, type=1)
        return member
           
    def create_or_import_object(self, type, obj_template_dict, headers, api_host, is_repeat):
        try:
            if type == "create":
                url = api_host + "/v1/policy/object"
                time1 = datetime.now()
                response = requests.post(url, headers=headers, json=obj_template_dict, verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print("Create {} object successfully.".format(obj_template_dict['object']['type']))
                else:
                    print("Create {} object failed.".format(obj_template_dict['object']['type']))
                time2 = datetime.now()
                time_difference = time2 - time1
                time_difference = time_difference.total_seconds()
                if time_difference > 60:
                    timeout_result = False
                    print("Creating {} object takes too long.".format(obj_template_dict['object']['type']))
                else:
                    timeout_result = True
            elif type == "import":
                import_url = api_host + "/v1/policy/object/import"
                if 'Content-Type' in headers:
                    del headers['Content-Type']
                response = requests.post(import_url, data=obj_template_dict["dry_data"], headers=headers, files=obj_template_dict["file_dry"], verify=False)
                assert response.status_code == 200
                if response.status_code == 200:
                    print("Verify the imported {} object successfully.".format(obj_template_dict['object']['type']))
                else:
                    print("Verify the imported {} object failed.".format(obj_template_dict['object']['type']))
                time1 = datetime.now()
                url = api_host + "/v1/policy/object/import"
                response = requests.post(url, data=obj_template_dict["data"], headers=headers, files=obj_template_dict["file_import"], verify=False)
                time.sleep(20)
                time2 = datetime.now()
                time_difference = time2 - time1
                time_difference = time_difference.total_seconds()
                assert response.status_code == 200
                if response.status_code == 200:
                    print("Import {} object successfully.".format(obj_template_dict['object']['type']))
                else:
                    print("Import {} object failed.".format(obj_template_dict['object']['type']))
                if time_difference > 180:
                    timeout_result = False
                    print("Importing {} object takes too long.".format(obj_template_dict['object']['type']))
                else:
                    timeout_result = True
            
            obj_type = obj_template_dict['object']['type']
            response_dict = json.loads(response.text)
            object_ids, geo_name_id_list = self.get_object_ids(response_dict, obj_type)
            
            # 是否可取消，待验证？？
            if is_repeat == 1 and obj_type != 'ip':
                self.fqdn_ids = []
                self.url_ids = []
            elif is_repeat == 1 and obj_type == 'ip':
                self.ip_ids = []
                
            obj_type = obj_template_dict['object']['type'] 
            if obj_type == 'ip':
                self.ip_ids = self.handle_ids(object_ids, self.ip_ids)
            elif obj_type == 'subscriberid':
                self.subid_ids = self.handle_ids(object_ids, self.subid_ids)
            elif obj_type == 'fqdn':
                self.fqdn_ids = self.handle_ids(object_ids, self.fqdn_ids)
            elif obj_type == 'flag':
                self.flag_ids = self.handle_ids(object_ids, self.flag_ids)
            elif obj_type == 'url':
                self.url_ids = self.handle_ids(object_ids, self.url_ids)
            elif obj_type == 'keywords':
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
            print(f"AssertionError: {e}")
    
    # 获取返回结果中的objectsid
    def get_object_ids(self, response_dict, obj_type):
        temp_list = []
        temp_geo_name_id_list = []
        if obj_type == 'geolocation':
            object_id = response_dict['data']['object']['member']['geolocation']['country_object_id']
            geoname_id = response_dict['data']['object']['member']['geolocation']['geoname_id']
            temp_geo_name_id_list.append(geoname_id)
        else:
            object_id = response_dict['data']['object']['id']      
        temp_list.append(object_id)
        return temp_list, temp_geo_name_id_list
    
    # 组织在策略中使用的source,filter等数据
    def obj_ids_to_policy_obj_list(self, object_ids, attribute_name, is_negate):
        temp_list = []
        for obj in object_ids:
            obj = int(obj)
            object_id_list = []
            object_id_list.append(obj)
            object_dict = dict(object_ids=object_id_list)
            temp_list.append(object_dict)
            temp_dict = dict(objects=temp_list, attribute_name=attribute_name, is_negate=is_negate)
        return temp_dict

    def handle_ids(self, object_ids, target_ids):
        if len(target_ids) != 0 and len(object_ids) != 0:
            for obj in object_ids:
                target_ids.append(obj)
        elif len(target_ids) == 0 and len(object_ids) != 0:
            target_ids = object_ids
        return target_ids

if __name__ == '__main__':
    print("test")