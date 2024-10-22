# import os
import sys
import time
from traceback import print_tb
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.object.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.object_element_position import *
from datetime import datetime 

class CreateObject:
    def __init__(self, driver):
        self.driver = driver
        
    def create(self, data, object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击creat
            time.sleep(1)
            self.driver.find_element(By.XPATH, create_element_position["objectListPage_createButton_posXpath"]).click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, create_element_position["objectListPage_dropDown_createButton_posXpath"]).click()
            time.sleep(1)
            # 输入name
            object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            # 添加item
            if data["object_type"] == "http_signature":
                for i in range(len(data["item"])):
                    self.driver.find_element(By.ID, create_element_position["objectPage_addItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_item_key_dropDown_posXpath"]).click()
                    temp_element_position = create_element_position["objectPage_item_key_dropDown_select_posXpath"].format(replaceValue=data["item"][i]["item_key"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    temp_element_position = create_element_position["objectPage_item_value_select_posXpath"].format(replaceValue=data["item"][i]["item_value"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    # 如果有range，则需要点击range
                    if "range" in data["item"][i] and len(data["item"][i]["range"]) > 0:
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_item_value_select_posXpath"].format(replaceValue="Range")).click()
                    if data["item"][i]["item_operation"] == "add":   # 直接 新增 模式
                        if "->" in data["item"][i]["value"][0]:   # -> 存在，需要拆分
                            item_value_str = data["item"][i]["value"][0].split("->")[0].strip()
                        else:    # -> 不存在，直接取值
                            item_value_str = data["item"][i]["value"][0].strip()
                        # 匹配多个multiple substrings 类型
                        if "&" in item_value_str:   # & 含有多个 and multiple substrings
                            item_values = item_value_str.split("&")
                        else:
                            item_values = [item_value_str]
                    else:    # 修改模式，未完成
                        # print("todo modify moudle ...")
                        item_values = [data["item"][i]["item_value"]]
                    for j, item_value in enumerate(item_values): # 遍历添加 multi substr，第一个元素不用点击 + 图标
                        item_value = item_value.strip()
                        temp_element_position = create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j+1, replaceValueInput=1)
                        if j == 0:
                            self.driver.find_element(By.XPATH, temp_element_position).send_keys(item_value)
                        else:
                            self.driver.find_element(By.XPATH,create_element_position["objectPage_item_value_plus_posXpath"]).click()
                            self.driver.find_element(By.XPATH, temp_element_position).send_keys(item_value)
                        # 如果有range，需要输入 offset depth
                        if "range" in data["item"][i] and len(data["item"][i]["range"]) > 0:
                            offset = data["item"][i]["range"][j]["offset"]
                            depth =  data["item"][i]["range"][j]["depth"]
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j+1, replaceValueInput=2), find_after_wait_time=0.5).send_keys(offset)
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j+1, replaceValueInput=3), find_after_wait_time=0.5).send_keys(depth)

                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif data["object_type"] == "keywords":
                for i in range(len(data["item"])):
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    temp_element_position = create_element_position["objectPage_item_value_select_posXpath"].format(replaceValue=data["item"][i]["item_value"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    if data["item"][i]["item_operation"] == "add":   # 直接 新增 模式
                        if "->" in data["item"][i]["value"][0]:   # -> 存在，需要拆分
                            item_value_str = data["item"][i]["value"][0].split("->")[0].strip()
                        else:    # -> 不存在，直接取值
                            item_value_str = data["item"][i]["value"][0].strip()
                        # 匹配多个multiple substrings 类型
                        if "&" in item_value_str:   # & 含有多个 and multiple substrings
                            item_values = item_value_str.split("&")
                        else:
                            item_values = [item_value_str]
                    else:    # 修改模式，未完成
                        # print("todo modify moudle ...")
                        item_values = [data["item"][i]["item_value"]]
                    for j, item_value in enumerate(item_values): # 遍历添加 multi substr，第一个元素不用点击 + 图标
                        item_value = item_value.strip()
                        temp_element_position = create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j+1)
                        if j == 0:
                            self.driver.find_element(By.XPATH, temp_element_position).send_keys(item_value)
                        else:
                            self.driver.find_element(By.XPATH,create_element_position["objectPage_item_value_plus_posXpath"]).click()
                            self.driver.find_element(By.XPATH, temp_element_position).send_keys(item_value)
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif data["object_type"] in ["url", "account", "phone_number", "fqdn", "subscriberid", "apn"]:
                for i in range(len(data["items"])):   #
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    if data["items"][i]["item_operation"] == "add":   # 直接 新增 模式
                        if "->" in data["items"][i]["item_value"]:   # -> 存在，需要拆分
                            item_value_str = data["items"][i]["item_value"].split("->")[0].strip()
                        else:    # -> 不存在，直接取值
                            item_value_str = data["items"][i]["item_value"].strip()
                        # 匹配多个multiple substrings 类型
                        if "&" in item_value_str:   # & 含有多个 and multiple substrings
                            item_values = item_value_str.split("&")
                        else:
                            item_values = [item_value_str]
                    else:    # 修改模式，未完成
                        # print("todo modify moudle ...")
                        item_values = [data["items"][i]["item_value"]]
                    for j, item_value in enumerate(item_values): # 遍历添加 multi substr，第一个元素不用点击 + 图标
                        item_value = item_value.strip()
                        if j == 0:
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"]).send_keys(item_value)
                        else:
                            self.driver.find_element(By.XPATH,create_element_position["ObjectPage_sameItem_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH,create_element_position["ObjectPage_sameItem_inputItem_posXpath"]).send_keys(item_value)
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif data["object_type"] == "tunnel":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added...")
            elif data["object_type"] == "flag":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added...")
            elif data["object_type"] == "interval":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added...")
            elif data["object_type"] == "application":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added...")
            elif data["object_type"] == "ip_learning":
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added...")
            else:
                for i in range(len(data["item"])):
                    if data["object_type"] == "ip":
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_ipType_posXpath"]).click()
                    if data["item"][i]["item_type"] == "imsi":
                        self.driver.find_element(By.ID, create_element_position["objectPage_imsiType_posId"]).click()
                    elif data["item"][i]["item_type"] == "phone_number":
                        self.driver.find_element(By.ID, create_element_position["objectPage_phnoeNumberType_posId"]).click()
                    elif data["item"][i]["item_type"] == "imei":
                        self.driver.find_element(By.ID, create_element_position["objectPage_imeiType_posId"]).click()
                    if data["item"][i]["item_operation"] == "add":
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                        # 适配24.10 版本，需要逐个字符输入
                        send_data = data["item"][i]["item_value"]
                        input_field = self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"])
                        for char in str(send_data):
                            input_field.send_keys(char)
                            time.sleep(0.1)
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()

            if "statistics_option" in data.keys():
                # 如果修改Object的统计参数则进行操作
                statistics_option_temp = data["statistics_option"]
                time.sleep(1)
                if statistics_option_temp in {"None","Brief","Elaborate"}:
                    self.driver.find_element(By.ID, create_element_position["objectPage_statistics_select_posId"]).click()
                    element_dropdown_item = self.driver.find_element(By.XPATH, create_element_position["objectPage_statistics_select_option_posXpath"].format(statistics_option_temp))
                    # 移动元素到页面，在执行点击
                    self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                    self.driver.execute_script("arguments[0].click();", element_dropdown_item)
            # 确认创建
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            #self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except Exception as e:
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            #return 400
    
    def create_group(self, data, object_type, object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击create group
            self.driver.find_element(By.ID, create_element_position["objectListPage_createButton_posId"]).click()
            if object_type == "ApplicationGroup":
                pass
            else:
                self.driver.find_element(By.ID, create_element_position["objectListPage_dropDown_createGroupButton_posId".format(object_type)]).click()
            # 输入name
            object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            # 切换type
            if data["select_type"] == True:
                self.driver.find_element(By.ID, create_element_position["groupObjectPage_selectType{}_posId".format(object_type)]).click()
            # 点subordinate的+
            self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_addSubordinate_posXpath"]).click()
            # 添加subordinate
            group_subordinate_data = data["group_subordinate"]
            if len(group_subordinate_data) != 0:
                for x in range(len(group_subordinate_data)):
                    time.sleep(0.5)
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = create_element_position["groupObjectPage_selectSubordinate{}_posXpath".format(object_type)].format(replaceValue=group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_closeSubordinate{}_posXpath".format(object_type)]).click()
                    if len(group_subordinate_data) > 1 and x < len(group_subordinate_data) - 1:
                        self.driver.find_element(By.ID, create_element_position["groupObjectPage_addSubordinateObject_posId"]).click()
            # 判断是否存在exclude
            group_exclude_data = data["group_exclude"]
            if len(group_exclude_data) != 0:
                # 使能exclude
                self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_enableExclude_posXpath"]).click()
                # 点exclude的+
                self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_addExclude_posXpath"]).click()
                # 添加exclude
                group_exclude_data = data["group_exclude"]
                for y in range(len(group_exclude_data)):
                    time.sleep(0.5)
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = create_element_position["groupObjectPage_selectExclude{}_posXpath".format(object_type)].format(replaceValue=group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_closeExclude{}_posXpath".format(object_type)]).click()
                    if len(group_exclude_data) > 1 and y < len(group_exclude_data) - 1:
                        self.driver.find_element(By.ID, create_element_position["groupObjectPage_addExcludeObject_posId"]).click()
            # 确认创建
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except Exception as e:
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", file=sys.stderr, flush=True)
            raise
            #return 400
        