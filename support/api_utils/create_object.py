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

    def create_object_from_template(self, token, condition, template, api_host, test_pc_ip, vsys_id):
        # 此处的condition为测试用例json中obj_condition_{i}的相关数据
        headers = {"Content-Type": "application/json", "Authorization": token}
        with open(template, 'r', encoding='utf-8') as f:
            obj_template_dict = json.load(f)
        source_list = []
        dst_list = []
        filter_list = []
        flag_list = []
        timeout_result = True
        # 依次创建object
        if len(condition) > 0:
            for key in condition:
                attribute_name = key['attribute_name']
                is_repeat = 0
                if 'is_repeat' in key:
                    is_repeat = key['is_repeat']
                if is_repeat == 1:
                    granularity = key["granularity"]
                    run_times = key["run_times"]
                    for i in range(run_times):
                        index = i + 1
                        objects_list, timeout_result = self.organize_objects_data(obj_template_dict, key, headers, api_host, test_pc_ip, vsys_id, token, index, run_times)
                        if attribute_name == 'ATTR_SOURCE_IP' or attribute_name == 'ATTR_SUBSCRIBER_ID':
                            for obj_dict in objects_list:
                                source_list.append(obj_dict)
                        elif attribute_name == 'ATTR_DESTINATION_IP' or attribute_name == "ATTR_DESTINATION_LOCATION" or attribute_name == "ATTR_SERVER_FQDN":
                            for obj_dict in objects_list:
                                dst_list.append(obj_dict)
                        elif attribute_name == 'ATTR_FLAG':
                            for obj_dict in objects_list:
                                flag_list.append(obj_dict)
                        else:
                            for obj_dict in objects_list:
                                filter_list.append(obj_dict)
                        time.sleep(granularity)
                        # if index < run_times:
                        #     erase = deleteConfig.DeleteConfig()
                        #     erase.delele_cfg(token, parameter, cfg_list)
                        #     erase.del_config(token, [], [], self.subid_ids, self.fqdn_ids, self.url_ids, self.flag_ids, self.keywords_ids, self.account_ids, self.http_signature_ids, [], api_host, vsys_id)
                else:
                    # 将测试用例中的数据传入模板文件后创建object
                    index = 1
                    run_times = 1
                    objects_list, timeout_result = self.organize_objects_data(obj_template_dict, key, headers, api_host, test_pc_ip, vsys_id, token, index, run_times)
                    if attribute_name == 'ATTR_SOURCE_IP' or attribute_name == 'ATTR_SUBSCRIBER_ID':
                        for obj_dict in objects_list:
                            source_list.append(obj_dict)
                    elif attribute_name == 'ATTR_DESTINATION_IP' or attribute_name == "ATTR_DESTINATION_LOCATION" or attribute_name == "ATTR_SERVER_FQDN":
                        for obj_dict in objects_list:
                            dst_list.append(obj_dict)
                    elif attribute_name == 'ATTR_FLAG':
                        for obj_dict in objects_list:
                            flag_list.append(obj_dict)
                    else:
                        for obj_dict in objects_list:
                            filter_list.append(obj_dict)
        return timeout_result, source_list, dst_list, filter_list, flag_list, self.ip_ids, self.subid_ids, self.fqdn_ids, self.url_ids, self.flag_ids, self.keywords_ids, self.account_ids, self.http_signature_ids
    
    # 对多个objects的处理（处理之后要调用create_object）
    def organize_objects_data(self, obj_template_dict, condition, headers, api_host, test_pc_ip, vsys_id, token, index, run_times):
        # object中的is_repeat，用于判定是否需要将数据组建为按照文件读取为多个items的形式
        is_repeat = 0
        is_import = 0
        if 'is_repeat' in condition:
            is_repeat = condition['is_repeat']
        if 'is_import' in condition:
            is_import = condition['is_import']
        attribute_name = condition['attribute_name']
        obj_list = condition["object_list"]
        obj_type = condition["object_type"]
        obj_sub_type = condition['object_sub_type']
        if 'is_negate' in condition.keys():
            is_negate = condition['is_negate']
        else:
            is_negate = 0
        obj_template_dict['object']['type'] = obj_type
        obj_template_dict['object']['sub_type'] = obj_sub_type
        obj_template_dict['vsys_id'] = vsys_id
        for obj in obj_list:
            add_item_list = obj["add_item_list"]
            if "context_name" in obj.keys():
                context_name = obj['context_name']
            else:
                context_name = ''
            if is_import == 0:
                member = self.combine_object_data(obj_type, obj_sub_type, add_item_list, test_pc_ip, context_name, is_repeat)
                obj_template_dict['object']['member'] = member
                object_ids_temp_list, timeout_result = self.create_object(obj_template_dict, headers, api_host, is_repeat)
            else:
                object_ids_temp_list, timeout_result = self.import_object(obj_type, vsys_id, add_item_list, api_host, token, is_repeat)
        if attribute_name != '' and len(object_ids_temp_list) != 0:
            objects_list = self.obj_ids_to_policy_obj_list(object_ids_temp_list, attribute_name, is_negate)
        else:
            objects_list = []
        object_temp_list = []
        if len(objects_list) > 0 and is_repeat == 0:
            object_temp_list.append(objects_list)
        elif len(objects_list) > 0 and is_repeat == 1 and index > run_times-1:
            object_temp_list.append(objects_list)
        return object_temp_list, timeout_result 
    
    # 组织创建通过items进行新增的object的数据
    def combine_object_data(self, obj_type, obj_sub_type, add_item_list, test_pc_ip, context_name, is_repeat):
        items = []
        object_dict = {}
        if is_repeat == 0:
            if obj_type == "ip" and obj_sub_type != "geo_location":
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
            else:
                for item in add_item_list:
                    patterns = []
                    keywords = item["keyword_array"][0]
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
        
        member = dict(items=items, type=1)
        return member
           
    def import_object(self, obj_type, vsys_id, add_item_list, api_host, token, is_repeat):
        headers = {"Authorization": token}
        data = {'type': obj_type, 'vsys_id': vsys_id}
        for item in add_item_list:
            object_file = item["keyword_array"][0]
            file_name = object_file.split("/")[-1]
            files = {"file":(file_name, open(object_file, 'rb'), "text/plain")}
        url = api_host + "/v1/policy/object/import"
        time1 = datetime.now()
        response = requests.post(url, data=data, headers=headers, files= files, verify=False)
        time.sleep(20)
        time2 = datetime.now()
        time_difference = time2 - time1
        seconds_difference = time_difference.total_seconds()
        assert response.status_code == 200
        if seconds_difference > 180:
            timeout_result = False
        else:
            timeout_result = True
        response_dict = json.loads(response.text)
        object_ids = self.get_object_ids(response_dict)
        # 为了每次清空需要反复创建的object的组合使用，否则会反复删除已经存在的object
        if is_repeat == 1 and obj_type != 'ip':
            self.fqdn_ids = []
            self.url_ids = []
        elif is_repeat == 1 and obj_type == 'ip':
            self.ip_ids = []
        # 这里把if和elif后面的语句都写成一个函数，然后再判断，否则if_elif占用了36行
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
        return object_ids, timeout_result
    
    # 调用创建object的接口
    def create_object(self, obj_template_dict, headers, api_host, is_repeat):
        url = api_host + "/v1/policy/object"
        response = requests.post(url, headers=headers, json=obj_template_dict, verify=False)
        assert response.status_code == 200
        time1 = datetime.now()
        response_dict = json.loads(response.text)
        time2 = datetime.now()
        time_difference = time2 - time1
        seconds_difference = time_difference.total_seconds()
        if seconds_difference > 60:
            timeout_result = False
        else:
            timeout_result = True
        # 从返回数据中获取object_type，方便后续判断将id添加到哪个全局变量里边
        if is_repeat == 1:
            time.sleep(20)
        obj_type = response_dict['data']['object']['type']
        object_ids = self.get_object_ids(response_dict)
        # 为了每次清空需要反复创建的object的组合使用，否则会反复删除已经存在的object
        obj_template_dict['object']['type'] = obj_type
        if is_repeat  == 1 and obj_type != 'ip':
            self.fqdn_ids = []
            self.url_ids = []
        elif is_repeat  == 1 and obj_type == 'ip':
            self.ip_ids = []
        # 这里把if和elif后面的语句都写成一个函数，然后再判断，否则if_elif占用了36行
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
        return object_ids, timeout_result
    
    # 获取返回结果中的objectsid
    def get_object_ids(self, response_dict):
        temp_list = []
        object_id = response_dict['data']['object']['id']
        temp_list.append(object_id)
        return temp_list
    
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