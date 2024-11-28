import json
import random
import time
import traceback
import requests
from support.ui_utils.element_position.profile_element_position import *
from selenium.webdriver.common.by import By
from datetime import datetime 

class DeleteProfiles:
    def __init__(self, driver):
        self.driver = driver
        
    def delete_profiles(self, profiles_tuple):
        profile_element_position = {}
        first_row_checkbox_element = {}
        is_del_all = False
        delete_element_position = profile_element_position["delete"]
        try:
            if is_del_all == True:
                element = self.driver.find_element(By.XPATH, mainPage_profileBottomPage_button_allSelect_posXpath).click()
                #self.driver.find_element(By.XPATH, delete_element_position["profileListPage_allSelect_posXpath"]).click()   #遇到无reference count在优化
                rows = self.driver.find_element(By.XPATH, listPage_profilTable_dnsRecords_tableTbody_posXpath).find_elements(By.XPATH, "./tr")
                self.select_lock_and_referenceCount(rows)

            else:
                first_row_checkbox_element.click()
            self.driver.find_element(By.XPATH, delete_element_position["profileListPage_deleteButton_posXpath"]).click()
            time.sleep(0.5)
            self.driver.find_element(By.XPATH, delete_element_position["profileListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(2)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            #self.driver.find_element(By.XPATH, delete_element_position["profileListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(0.5)
            raise
            #return 200

    def select_lock_and_referenceCount(self, rows, islock=False, referenceCount=0):
        """
        筛选点击是 否有锁、引用数是否为0的数据，默认选择列表列中无锁且引用为0的数据。
        :param rows:   查询的所有行数据， 例如：self.driver.find_element(By.XPATH, listPage_profilTable_dnsRecords_tableTbody_posXpath).find_elements(By.XPATH, "./tr")
        :param lock: False True
        :param referenceCount: 0， 1
        :return:  0 表示有删除对象， 1表示没有删除对象
        """
        return_code = 1
        try:
            for row_item in rows:
                # 查找元素是引用是否不为0,因为已经全选，不为0的点击取消选择//div[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']/div/div[@data-field='referenced_by']/button/parent::*/parent::*
                el_td_list = row_item.find_elements(By.XPATH, "./div[@data-field='referenced_by']//button")
                for el_td_item in el_td_list:
                    test = el_td_item.text
                    if test != '0':
                        el_td_item.find_elements(By.XPATH, "./parent::*/parent::*").click()
                        break

            return return_code
        except Exception as e:
            raise

    def delete_profiles_by_name(self, parameter, policy_configuration, headers):
        try:
            api_server = parameter["api_server"]
            profile_info_list = self.get_profiles_info(policy_configuration)
            profile_type_dict = {
                "service_function_forwarder": "service-function-forwarders",
                "service_function": "service-functions",
                "statistics_template": "statistics-templates",
                "response_page": "response-pages",
                "hijack_file": "proxy-replacement-files",
                "insert_script": "proxy-inject-scripts",
                "proxy_css_file": "proxy-css-files",
                "proxy_js_file": "proxy-js-files",
                "traffic_mirror": "traffic-mirroring-profiles",
                "run_script": "proxy-lua-scripts",
                "dns_record": "dns-resource-records",
                "ssl_keyring": "decryption-keyrings",
                "ssl_decryption": "decryption-profiles",
                "tcp_option": "proxy-tcp-option-profiles"
            }
            for i in range(len(profile_info_list)):
                type = profile_info_list[i]["type"]
                url = api_server + "/v1/profiles/{}".format(profile_type_dict[type])
                template = {"type": "", "name": "", "with_sub_vsys": 0, "vsys": parameter["vsys"]}
                template["name"] = profile_info_list[i]["name"]
                template["type"] = profile_info_list[i]["type"]
                response = requests.get(url, headers=headers, params=template, verify=False)
                if response.status_code != 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Search {} profile failed.".format(profile_info_list[i]["type"]))
                    return "Search {} profile failed.".format(profile_info_list[i]["type"])
                return_json_data = json.loads(response.text)
                if "-" in type:
                    data_list = return_json_data["data"]["list"]
                    deletion_profile_type = template["type"].replace("-", " ") + " " + "profile"
                if len(data_list) > 0:
                    deletion_uuids_list = self.combine_profiles_uuid(template, data_list)
                    for i in range(len(deletion_uuids_list)):
                        deletion_template = {"uuids": "", "vsys": parameter["vsys"]}
                        deletion_template["uuids"] = deletion_uuids_list[i]
                        response = requests.delete(url, headers=headers, json=deletion_template, verify=False)
                    if len(deletion_uuids_list) > 0:
                        if response.status_code == 200:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} successfully by name.".format(deletion_profile_type), flush=True)
                            return ""
                        else:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Delete {} failed by name.".format(deletion_profile_type))
                            return "Delete {} failed by name.".format(deletion_profile_type)
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When deleting profile by name, the exception error: ", str(e), flush=True)
            return "When deleting profile by name, the exception error: " + str(e)

    def get_profiles_info(policy_configuration):
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

    def combine_profiles_uuid(self, template, data_list):
        uuid_list = []
        for _, json_obj in enumerate(data_list):
            if template["name"] == json_obj["name"]:
                uuid = json_obj["uuid"]
                uuid_list.append(uuid)
        return uuid_list