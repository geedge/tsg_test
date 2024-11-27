# import os
import random
import sys
import time
from traceback import print_tb
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.objects.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.map_element_position_library import *
from support.ui_utils.element_position.object_element_position import *
from datetime import datetime


class CreateObjects:
    def __init__(self, driver):
        self.driver = driver

    def create(self, data, object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        create_element_position = object_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            if "sub_type" in data.keys():
                object_type = data["sub_type"]
            else:
                object_type = data["type"]
            # 点击creat
            time.sleep(8)
            self.driver.find_element(By.XPATH, create_element_position["objectListPage_createButton_posXpath"]).click()
            time.sleep(1)
            if object_type not in  ["application","tunnel"]:
                self.driver.find_element(By.XPATH,create_element_position["objectListPage_dropDown_createButton_posXpath"]).click()
            time.sleep(1)
            # 输入name
            object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
            # 添加item
            """
            if object_type == "http_signature":
                for i in range(len(data["items"])):
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_item_key_dropDown_posXpath"]).click()
                    temp_element_position = create_element_position["objectPage_item_key_dropDown_select_posXpath"].format(replaceValue=data["items"][i]["item_key"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    temp_element_position = create_element_position["objectPage_item_value_select_posXpath"].format(replaceValue=data["items"][i]["item_value"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    # 如果有range，则需要点击range
                    if "range" in data["items"][i] and len(data["items"][i]["range"]) > 0:
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_item_value_select_posXpath"].format(replaceValue="Range")).click()
                    if data["items"][i]["item_operation"] == "add":   # 直接 新增 模式
                        if "->" in data["items"][i]["value"][0]:   # -> 存在，需要拆分
                            item_value_str = data["items"][i]["value"][0].split("->")[0].strip()
                        else:    # -> 不存在，直接取值
                            item_value_str = data["items"][i]["value"][0].strip()
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
                        temp_element_position = create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j+1, replaceValueInput=1)
                        if j == 0:
                            self.driver.find_element(By.XPATH, temp_element_position).send_keys(item_value)
                        else:
                            self.driver.find_element(By.XPATH,create_element_position["objectPage_item_value_plus_posXpath"]).click()
                            self.driver.find_element(By.XPATH, temp_element_position).send_keys(item_value)
                        # 如果有range，需要输入 offset depth
                        if "range" in data["items"][i] and len(data["items"][i]["range"]) > 0:
                            offset = data["items"][i]["range"][j]["offset"]
                            depth =  data["items"][i]["range"][j]["depth"]
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j+1, replaceValueInput=2), find_after_wait_time=0.5).send_keys(offset)
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j+1, replaceValueInput=3), find_after_wait_time=0.5).send_keys(depth)

                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
            el"""



            if object_type in ["keyword", "http_signature"]:
                for i in range(len(data["items"])):
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    # temp_element_position = create_element_position["objectPage_item_value_select_posXpath"].format(replaceValue=data["items"][i]["expression"])
                    # self.driver.find_element(By.XPATH, temp_element_position).click()
                    if data["items"][i]["op"] == "add":  # 直接 新增 模式
                        if "->" in data["items"][i]["expression"]:  # -> 存在，需要拆分
                            item_value_str = data["items"][i]["expression"].split("->")[0].strip()
                        else:  # -> 不存在，直接取值
                            item_value_str = data["items"][i]["expression"].strip()
                        # 匹配多个multiple substrings 类型
                        if "&" in item_value_str:  # & 含有多个 and multiple substrings
                            item_values = item_value_str.split("&")
                        else:
                            item_values = [item_value_str]
                    else:  # 修改模式，未完成
                        # print("todo modify moudle ...")
                        item_values = [data["items"][i]["expression"]]
                    for j, item_value in enumerate(item_values):  # 遍历添加 multi substr，第一个元素不用点击 + 图标
                        item_value = item_value.strip()
                        temp_element_position = create_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j + 1)
                        if j == 0:
                            for char in str(item_value):
                                self.driver.find_element(By.XPATH, temp_element_position).send_keys(char)
                                time.sleep(0.1)
                        else:
                            self.driver.find_element(By.XPATH, create_element_position["objectPage_item_value_plus_posXpath"]).click()
                            for char in str(item_value):
                                self.driver.find_element(By.XPATH, temp_element_position).send_keys(char)
                                time.sleep(0.1)
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif object_type in ["url", "account", "phone_number", "fqdn", "subscriberid", "apn"]:
                if object_type == "phone_number":
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_phnoeNumberType_posXpath"]).click()
                for i in range(len(data["items"])):  #
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    if data["items"][i]["op"] == "add":  # 直接 新增 模式
                        if "->" in data["items"][i]["expression"]:  # -> 存在，需要拆分
                            item_value_str = data["items"][i]["expression"].split("->")[0].strip()
                        else:  # -> 不存在，直接取值
                            item_value_str = data["items"][i]["expression"].strip()
                        # 匹配多个multiple substrings 类型
                        if "&" in item_value_str:  # & 含有多个 and multiple substrings
                            item_values = item_value_str.split("&")
                        else:
                            item_values = [item_value_str]
                    else:  # 修改模式，未完成
                        # print("todo modify moudle ...")
                        item_values = [data["items"][i]["item_value"]]
                    for j, item_value in enumerate(item_values):  # 遍历添加 multi substr，第一个元素不用点击 + 图标
                        item_value = item_value.strip()
                        if j == 0:
                            # 适配24.10 版本，需要逐个字符输入
                            input_field = self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"])
                            for char in str(item_value):
                                input_field.send_keys(char)
                                time.sleep(0.1)
                        else:
                            self.driver.find_element(By.XPATH, create_element_position["ObjectPage_sameItem_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH, create_element_position["ObjectPage_sameItem_inputItem_posXpath"]).send_keys(item_value)
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif object_type == "flag":
                for i in range(len(data["items"])):  #
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    if data["items"][i]["op"] == "add":  # 直接 新增 模式
                        for key_flag in data["items"][i]["flag"]:
                            if key_flag == "Bulky" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[2]").click()
                            elif key_flag == "CBR Streaming":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[3]").click()
                            elif key_flag == "Client is Local" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[4]").click()
                            elif key_flag == "Server is Local" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[5]").click()
                            elif key_flag == "Download" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[6]").click()
                            elif key_flag == "Interactive" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[7]").click()
                            elif key_flag == "Inbound" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[8]").click()
                            elif key_flag == "Outbound" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[9]").click()
                            elif key_flag == "Pseudo Unidirectional" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[10]").click()
                            elif key_flag == "Streaming" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[11]").click()
                            elif key_flag == "Unidirectional" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[12]").click()
                            elif key_flag == "Random looking" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[13]").click()
                            elif key_flag == "C2S" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[14]").click()
                            elif key_flag == "S2C" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[15]").click()
                            elif key_flag == "Bidirectional" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[16]").click()
                            elif key_flag == "Tunneling" and data["items"][i]["flag"][key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[17]").click()
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif object_type == "interval":
                for i in range(len(data["items"])):
                    data_int = data["items"][i]["interval"].split("-")
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()  # 点击“+”按钮
                    # 在空内容的输入框中，输入新增的数据
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_lowBoundary_posXpath"]).send_keys(eval(str(data_int))[0])  # 于item 下low_boundary value输入框键入item_value
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_upBoundary_posXpath"]).send_keys(eval(str(data_int))[1])  # 于item 下up_boundary value输入框键入item_value
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()  # 点击保存按钮
            elif object_type == "application":
                self.driver.find_element(By.XPATH, create_element_position["objectPage_inputLongName_posXpath"]).send_keys(data["application"]["app_longname"])  # input long name
                # self.driver.find_element(By.XPATH, create_element_position[""]).send_keys("Your description")  # input description
                self.driver.find_element(By.XPATH, create_element_position["objectPage_select_category_dropwmn_posXpath"]).click()  # category
                self.driver.find_element(By.XPATH, create_element_position["objectPage_category_xpath"].format(replaceValue=data["application"]["app_properties"]["category"])).click()  #
                self.driver.find_element(By.XPATH, create_element_position["objectPage_select_subcategory_dropwmn_posXpath"]).click()  # subcategory
                self.driver.find_element(By.XPATH, create_element_position["objectPage_sub_category_xpath"].format(replaceValue=data["application"]["app_properties"]["subcategory"])).click()  #
                self.driver.find_element(By.XPATH, create_element_position["objectPage_select_content_dropwmn_posXpath"]).click()  # content
                self.driver.find_element(By.XPATH, create_element_position["objectPage_content_xpath"].format(replaceValue=data["application"]["app_properties"]["content"])).click()  #
                self.driver.find_element(By.XPATH, create_element_position["objectPage_select_risk_dropwmn_posXpath"]).click()  # risk 0
                self.driver.find_element(By.XPATH, create_element_position["objectPage_risi_xpath"].format(replaceValue=data["application"]["app_properties"]["risk"])).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_characteristics_xpath"].format(replaceValue=data["application"]["app_properties"]["characteristics"])).click()
                #添加signature
                self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_create_signature_posXpath"]).click()
                for m in range(len(data["app_surrogates"])):
                    app_surrogates= data["app_surrogates"][m]
                    for i in range(len(app_surrogates["signature_sequence"])):
                        app_signature= app_surrogates["signature_sequence"][i]
                        self.driver.find_element(By.XPATH,create_element_position["signature_inputName_posXpath"]).send_keys(app_signature["signature"]["name"])
                        self.driver.find_element(By.XPATH, create_element_position["signature_add_artibutem_posXpath"]).click()
                        for j in range(len(app_signature["signature"]["and_conditions"])):
                            app_and_condition= app_signature["signature"]["and_conditions"][j]
                            self.driver.find_element(By.XPATH, create_element_position["signature_condition_select_up_posXpath"]).click()
                            if app_and_condition["negate_option"] == False:
                                self.driver.find_element(By.XPATH, create_element_position["signature_new_condition__posXpath"]).click()
                            else:self.driver.find_element(By.XPATH, create_element_position["signature_new_not_condition__posXpath"]).click()
                            self.driver.find_element(By.XPATH, create_element_position["signature_add_artibute_button_posXpath"]).click()
                            for n in range(len(app_and_condition["or_conditions"])):
                                app_or_condition= app_and_condition["or_conditions"][n]
                                self.driver.find_element(By.XPATH,"//li[@class = 'MuiTreeItem-root css-105mfs8']//div[text()='common']").click()
                                self.driver.find_element(By.XPATH,create_element_position["signature_artibute_protocols"].format(replaceValue=app_or_condition["attribute_name"])).click()
                                self.driver.find_element(By.XPATH,"(//div[@class='MuiDrawer-content css-10lcz44'])[4]//button[text()='Cancel']").click()
                                self.driver.find_element(By.XPATH,create_element_position["attribute_add_object_posXpath"]).click()
                                self.driver.find_element(By.XPATH,create_element_position["objectPage_create_signature_posXpath"]+"[2]").click()
                                common_object_element_position = get_element_position(app_or_condition["type"])
                                self.create_common_objects(app_or_condition,common_object_element_position)
                                self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_posXpath"]+"[4]").click()
                                self.driver.find_element(By.XPATH,"(//div[@class='MuiDrawer-content css-10lcz44'])[4]//button[text()='Cancel']").click()
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_posXpath"]+"[3]").click()
                self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_posXpath"]+"[2]").click()
                self.driver.find_element(By.XPATH,"(//div[@class='MuiDrawer-content css-10lcz44'])[1]//button[text()='Cancel']").click()
            elif object_type == "tunnel":
                if len(data["tunnel"]["and_conditions"]) == 1:
                    tunnel_endition_a = data["tunnel"]["and_conditions"][0]
                elif len(data["tunnel"]["and_conditions"]) == 2:
                    tunnel_endition_a = data["tunnel"]["and_conditions"][0]
                    tunnel_endition_b = data["tunnel"]["and_conditions"][1]

                self.driver.find_element(By.XPATH, create_element_position["objectPage_edit_tunnel_type_posXpath"]).click()
                if data["tunnel"]["action_parameter"]["type"] == "IP":
                    self.driver.find_element(By.XPATH, create_element_position["objectListPage_type_ip_posXpath"]).click()
                elif data["tunnel"]["action_parameter"]["type"] == "GRE":
                    self.driver.find_element(By.XPATH, create_element_position["objectListPage_type_gre_posXpath"]).click()

                for i in range(len(tunnel_endition_a["or_conditions"])):
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_endition_a_addItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_side_slic_create_button_posXpath"]).click()
                    common_object_element_position = get_element_position(tunnel_endition_a["or_conditions"][i]["type"])
                    self.create_common_objects(tunnel_endition_a["or_conditions"][i],common_object_element_position)
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_posXpath"]+"[2]").click()
                    self.driver.find_element(By.XPATH,create_element_position["ObjectPage_side_slic_Cancel_posXpath"]).click()
                if len(data["tunnel"]["and_conditions"]) == 2:
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_endition_b_addItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_endition_b_addItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_side_slic_create_button_posXpath"]).click()

                    for i in range(len(tunnel_endition_b["or_conditions"])):
                        self.create_common_objects(tunnel_endition_b["or_conditions"][i], common_object_element_position)
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_okButton_posXpath"] + "[2]").click()
                        self.driver.find_element(By.XPATH,create_element_position["ObjectPage_side_slic_Cancel_posXpath"]).click()



            elif object_type == "port":
                for i in range(len(data["items"])):
                    if data["items"][i]["op"] == "add":
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                        # 适配24.10 版本，需要逐个字符输入
                        send_data = data["items"][i]["interval"]
                        input_field = self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_posXpath"])
                        for char in str(send_data):
                            input_field.send_keys(char)
                            time.sleep(0.1)
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()
            elif object_type == "ip_learning":
                self.driver.find_element(By.XPATH,create_element_position["objectPage_ipLearningType_posXpath"]).click()
                if data["op"] == "add":
                    for i in range(0,len(data["learning_plan"]["fqdn_ip_learning_plan"]["from_fqdns"])):
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_addItem_posXpath"]).click()
                        send_data = data["learning_plan"]["fqdn_ip_learning_plan"]["from_fqdns"][i]
                        input_field = self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_posXpath"])
                        for char in str(send_data):
                            input_field.send_keys(char)
                            time.sleep(0.1)
                        self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_learnFromProtocols_up_select_posXpath"]).click()
                if data["learning_plan"]["fqdn_ip_learning_plan"]["from_protocol"] == "HTTP":
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_learnFromProtocols_http_posXpath"]).click()
                elif data["learning_plan"]["fqdn_ip_learning_plan"]["from_protocol"]  == "SSL":
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_learnFromProtocols_ssl_posXpath"]).click()
                # self.driver.find_element(By.XPATH, ip_addressObjectPage_button_IP_learn_from_protocols_up_posXpath).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_agingTimes_posXpath"]).send_keys(data["learning_plan"]["fqdn_ip_learning_plan"]["aging_time"] )
                self.driver.find_element(By.XPATH,create_element_position["objectPage_voteClients_posXpath"]).send_keys(data["learning_plan"]["fqdn_ip_learning_plan"]["vote_client_num"])
                self.driver.find_element(By.XPATH,create_element_position["objectPage_learnedIPLimits_posXpath"]).send_keys(data["learning_plan"]["fqdn_ip_learning_plan"]["goal_upper_limit"])
            else:
                for i in range(len(data["items"])):
                    if object_type == "ip":
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_ipType_posXpath"]).click()
                        send_data = data["items"][i]["ip"]
                    if object_type == "imsi":
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_imsiType_posXpath"]).click()
                        send_data = data["items"][i]["expression"]
                    elif object_type == "imei":
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_imeiType_posXpath"]).click()
                        send_data = data["items"][i]["expression"]
                    if data["items"][i]["op"] == "add":
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_addItem_posXpath"]).click()
                        # 适配24.10 版本，需要逐个字符输入
                        input_field = self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_posXpath"])
                        for char in str(send_data):
                            input_field.send_keys(char)
                            time.sleep(0.1)
                        self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()

            if "statistics_option" in data.keys():
                # 如果修改Object的统计参数则进行操作
                statistics_option_temp = data["statistics_option"]
                time.sleep(1)
                if statistics_option_temp in {"None", "Brief", "Elaborate"}:
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_statistics_select_posXpath"]).click()
                    element_dropdown_item = self.driver.find_element(By.XPATH, create_element_position["objectPage_statistics_select_option_posXpath"].format(statistics_option_temp))
                    # 移动元素到页面，在执行点击
                    self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                    self.driver.execute_script("arguments[0].click();", element_dropdown_item)
            # 确认创建
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            # self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except Exception as e:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            # return 400

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
                self.driver.find_element(By.ID, create_element_position[
                    "objectListPage_dropDown_createGroupButton_posId".format(object_type)]).click()
            # 输入name
            object_name = data["name"]
            self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(
                object_name)
            # 切换type
            if data["select_type"] == True:
                self.driver.find_element(By.ID, create_element_position[
                    "groupObjectPage_selectType{}_posId".format(object_type)]).click()
            # 点subordinate的+
            self.driver.find_element(By.XPATH,
                                     create_element_position["groupObjectPage_addSubordinate_posXpath"]).click()
            # 添加subordinate
            group_subordinate_data = data["group_subordinate"]
            if len(group_subordinate_data) != 0:
                for x in range(len(group_subordinate_data)):
                    time.sleep(0.5)
                    self.driver.find_element(By.XPATH, create_element_position[
                        "groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(
                        group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, create_element_position[
                        "groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = create_element_position[
                        "groupObjectPage_selectSubordinate{}_posXpath".format(object_type)].format(
                        replaceValue=group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position[
                        "groupObjectPage_closeSubordinate{}_posXpath".format(object_type)]).click()
                    if len(group_subordinate_data) > 1 and x < len(group_subordinate_data) - 1:
                        self.driver.find_element(By.ID, create_element_position[
                            "groupObjectPage_addSubordinateObject_posId"]).click()
            # 判断是否存在exclude
            group_exclude_data = data["group_exclude"]
            if len(group_exclude_data) != 0:
                # 使能exclude
                self.driver.find_element(By.XPATH,
                                         create_element_position["groupObjectPage_enableExclude_posXpath"]).click()
                # 点exclude的+
                self.driver.find_element(By.XPATH,
                                         create_element_position["groupObjectPage_addExclude_posXpath"]).click()
                # 添加exclude
                group_exclude_data = data["group_exclude"]
                for y in range(len(group_exclude_data)):
                    time.sleep(0.5)
                    self.driver.find_element(By.XPATH, create_element_position[
                        "groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(
                        group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, create_element_position[
                        "groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = create_element_position[
                        "groupObjectPage_selectExclude{}_posXpath".format(object_type)].format(
                        replaceValue=group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, create_element_position[
                        "groupObjectPage_closeExclude{}_posXpath".format(object_type)]).click()
                    if len(group_exclude_data) > 1 and y < len(group_exclude_data) - 1:
                        self.driver.find_element(By.ID, create_element_position[
                            "groupObjectPage_addExcludeObject_posId"]).click()
            # 确认创建
            self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            self.driver.find_element(By.XPATH,
                                     create_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except Exception as e:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", file=sys.stderr, flush=True)
            raise
            # return 400


    def create_common_objects(self,data,common_object_element_position):
        object_type = data["type"]
        create_element_position = common_object_element_position["create"]
        self.driver.find_element(By.XPATH,'//ul[@class="base-Popper-root MuiMenu-root Mui-expanded MuiMenu-variantOutlined MuiMenu-colorNeutral MuiMenu-sizeMd css-131n2dh"]/li[1]').click()
        object_name = data["name"]
        self.driver.find_element(By.XPATH, create_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
        if object_type in ["url", "account", "phone_number", "fqdn", "subscriberid", "apn"]:
            if object_type == "phone_number":
                self.driver.find_element(By.XPATH,create_element_position["objectPage_phnoeNumberType_posXpath"]).click()
            for i in range(len(data["items"])):  #
                self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                if data["items"][i]["op"] == "add":  # 直接 新增 模式
                    if "->" in data["items"][i]["expression"]:  # -> 存在，需要拆分
                        item_value_str = data["items"][i]["expression"].split("->")[0].strip()
                    else:  # -> 不存在，直接取值
                        item_value_str = data["items"][i]["expression"].strip()
                    # 匹配多个multiple substrings 类型
                    if "&" in item_value_str:  # & 含有多个 and multiple substrings
                        item_values = item_value_str.split("&")
                    else:
                        item_values = [item_value_str]
                else:  # 修改模式，未完成
                    # print("todo modify moudle ...")
                    item_values = [data["items"][i]["item_value"]]
                for j, item_value in enumerate(item_values):  # 遍历添加 multi substr，第一个元素不用点击 + 图标
                    item_value = item_value.strip()
                    if j == 0:
                        # 适配24.10 版本，需要逐个字符输入
                        input_field = self.driver.find_element(By.XPATH,
                                                               create_element_position["objectPage_inputItem_posXpath"])
                        for char in str(item_value):
                            input_field.send_keys(char)
                            time.sleep(0.1)
                    else:
                        self.driver.find_element(By.XPATH, create_element_position["ObjectPage_sameItem_addItem_posXpath"]).click()
                        self.driver.find_element(By.XPATH, create_element_position["ObjectPage_sameItem_inputItem_posXpath"]).send_keys(item_value)
                self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()
        elif object_type == "ip":
            for i in range(len(data["items"])):
                if data["items"][i]["op"] == "add":
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    # 适配24.10 版本，需要逐个字符输入
                    input_field = self.driver.find_element(By.XPATH,create_element_position["objectPage_inputItem_posXpath"])
                    for char in str(data["items"][i]["ip"]):
                        input_field.send_keys(char)
                        time.sleep(0.1)
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_button_saveItem_posXpath"]).click()


