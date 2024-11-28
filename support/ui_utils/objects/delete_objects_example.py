# -*- coding: UTF-8 -*-
import json
import requests
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.map_element_position_library import get_element_position
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.objects.page_jump import PageJump
from support.ui_utils.objects.search_objects_example import SearchObjects
class DeleteObjects:

    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(5)

    def delete_objects(self,parmameter,objects_tuple):
        try:
            for object in objects_tuple:
                element_position_library = get_element_position(object["type"])
                deletion_element_position = element_position_library["delete"]
                page_jump_element_position = element_position_library["page_jump"]
                search_element_position = element_position_library["search"]
                page_jump = PageJump(self.driver)
                time.sleep(0.5)
                page_jump.jump_sub_object_page(page_jump_element_position)
                time.sleep(3)
                self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"]).click()
                self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"]).send_keys(object["uuid"])
                self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_selectID_posXpath"]).click()
                self.driver.find_element(By.XPATH,search_element_position["objectListPage_search_button_posXpath"]).click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, '(//input[@aria-label="Select row"])[1]').click()
                #点击删除按钮
                self.driver.find_element(By.XPATH, deletion_element_position["objectListPage_deleteButton_posXpath"]).click()
                self.driver.find_element(By.XPATH,deletion_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
                time.sleep(3)
                if object["type"] == "tunnel":
                    element_position_library = get_element_position("ip")
                    page_jump_element_position = element_position_library["page_jump"]
                    search_element_position = element_position_library["search"]
                    page_jump = PageJump(self.driver)
                    time.sleep(0.5)
                    page_jump.jump_sub_object_page(page_jump_element_position)
                    time.sleep(3)
                    self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"]).click()
                    self.driver.find_element(By.XPATH,search_element_position["objectListPage_searchLabel_posXpath"]).send_keys("tunnel")
                    self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_selectName_posXpath"]).click()
                    self.driver.find_element(By.XPATH,search_element_position["objectListPage_search_button_posXpath"]).click()
                    time.sleep(2)
                    objects_list_elements = self.driver.find_elements(By.XPATH,"//div[@class='MuiDataGrid-virtualScrollerContent css-0']/div/div")
                    if len(objects_list_elements) != 0:
                        self.driver.find_element(By.XPATH,"//input[@class='MuiCheckbox-input css-1jj0cvj']").click()
                        self.driver.find_element(By.XPATH,deletion_element_position["objectListPage_deleteButton_posXpath"]).click()
                        self.driver.find_element(By.XPATH, deletion_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
                return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400

    def delete_sub_objects(self,object_element_position,first_row_checkbox_element):
        deletion_element_position = object_element_position["delete"]
        try:
            first_row_checkbox_element.click()
            self.driver.find_element(By.ID, deletion_element_position["objectListPage_deleteButton_posId"]).click()
            self.driver.find_element(By.XPATH,deletion_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(3)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",
                  flush=True)
            return 400
        
    def delete_objects_by_name(self, parameter, policy_configuration, headers):
        try:
            api_server = parameter["api_server"]
            object_info_list = self.get_objects_info(policy_configuration)
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
            for i in range(len(object_info_list)):
                type = object_info_list[i]["type"]
                url = api_server + "/v1/objects/{}".format(object_type_dict[type])
                template = {"type": "", "name": "", "with_sub_vsys": 0, "vsys": parameter["vsys"]}
                template["name"] = object_info_list[i]["name"]
                template["type"] = object_info_list[i]["type"]
                response = requests.get(url, headers=headers, params=template, verify=False)
                if response.status_code != 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Search {} object failed.".format(policy_configuration["type"]))
                    return "Search {} object failed.".format(policy_configuration["type"])
                return_json_data = json.loads(response.text)
                if "/objects" in url:
                    data_list = return_json_data["data"]["list"]
                    deletion_object_type = template["type"].title() + " " + "object"
                if len(data_list) > 0:
                    deletion_uuids_list = self.combine_object_uuids(template, data_list)
                    for i in range(len(deletion_uuids_list)):
                        deletion_template = {"uuids": "", "vsys": parameter["vsys"]}
                        deletion_template["uuids"] = deletion_uuids_list[i]
                        response = requests.delete(url, headers=headers, json=deletion_template, verify=False)
                    if len(deletion_uuids_list) > 0:
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully by name.".format(deletion_object_type), flush=True)
                            return ""
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed by name.".format(deletion_object_type))
                            return "Delete {} failed by name.".format(deletion_object_type)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting object by name, the exception error: ", str(e), flush=True)
            return "When deleting object by name, the exception error: " + str(e)
    
    def get_objects_info(policy_configuration):
        object_info_list = []
        object_info_dict = {}
        if "and_conditions" in policy_configuration:
            and_conditions = policy_configuration["and_conditions"]
            for i in range(len(and_conditions)):
                or_conditions = and_conditions[i]["or_conditions"]
                for j in range(len(or_conditions)):
                    # 需要做深入判断？？
                    object_info_dict["type"] = or_conditions[j]["type"]
                    object_info_dict["name"] = or_conditions[j]["name"]
                    object_info_list.append(object_info_dict)
        return object_info_list
    
    def combine_object_uuids(self, template, data_list):
        uuid_list = []
        # 遍历列表中的每个 JSON 对象
        for i, json_obj in enumerate(data_list):
            # 提取 uuid 键的值
            if template["name"] == json_obj["name"]:
                uuid = json_obj["uuid"]
                uuid_list.append(uuid)
        return uuid_list