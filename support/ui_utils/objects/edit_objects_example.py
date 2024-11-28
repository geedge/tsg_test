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
from support.ui_utils.objects.search_objects import SearchObject

class EditObjects:
    def __init__(self, driver):
        self.driver = driver

    def edit_objects(self, objects_tuple,src_item, new_item):
        try:
            for object in objects_tuple:
                element_position_library = get_element_position(object["type"])
                page_jump_element_position = element_position_library["page_jump"]
                edit_element_position = element_position_library["edit"]
                search_element_position = element_position_library["search"]
                page_jump = PageJump(self.driver)
                time.sleep(0.5)
                page_jump.jump_sub_object_page(page_jump_element_position)
                time.sleep(3)
                self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_posXpath"]).click()
                self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_posXpath"]).send_keys(object["uuid"])
                self.driver.find_element(By.XPATH, search_element_position["objectListPage_searchLabel_selectID_posXpath"]).click()
                self.driver.find_element(By.XPATH, search_element_position["objectListPage_search_button_posXpath"]).click()
                time.sleep(2)
                self.driver.find_element(By.XPATH,'(//input[@aria-label="Select row"])[1]').click()
                self.driver.find_element(By.XPATH, edit_element_position["ObjectListPage_editButton_posXpath"]).click()
                object_type = object["type"]
                if object_type in ["keyword", "http_signature"]:
                        # temp_element_position = edit_element_position["objectPage_item_value_select_posXpath"].format(replaceValue=object["items"][i]["expression"])
                        # self.driver.find_element(By.XPATH, temp_element_position).click()
                        if src_item == "":  # 直接 新增 模式
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_addItem_posXpath"]).click()
                            item_value_str = new_item.strip()
                            # 匹配多个multiple substrings 类型
                            if "&" in item_value_str:  # & 含有多个 and multiple substrings
                                item_values = item_value_str.split("&")
                            else:
                                item_values = [item_value_str]
                        else:  # 修改模式，未完成
                            self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_search_item_posXpath"]).send_keys(src_item + Keys.ENTER)
                            self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_edit_item_posXpath"]).click()
                            input_field = self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputItem_posXpath"].format(replaceValue=1))
                            input_field.send_keys(Keys.CONTROL, 'a')  # 或使用 Keys.COMMAND 在 macOS
                            input_field.send_keys(Keys.DELETE)
                            if "&" in new_item:  # & 含有多个 and multiple substrings
                                item_values = new_item.split("&")
                            else:
                                item_values = [new_item]
                        for j, item_value in enumerate(item_values):  # 遍历添加 multi substr，第一个元素不用点击 + 图标
                            item_value = item_value.strip()
                            temp_element_position = edit_element_position["objectPage_inputItem_posXpath"].format(replaceValue=j + 1)
                            if j == 0:
                                for char in str(item_value):
                                    self.driver.find_element(By.XPATH, temp_element_position).send_keys(char)
                                    time.sleep(0.1)
                            else:
                                self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_sameItem_addItem_posXpath"]).click()
                                self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_sameItem_inputItem_posXpath"]).send_keys(item_value)
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()
                elif object_type in ["url", "account", "phone_number", "fqdn", "subscriberid", "apn"]:
                    if src_item == "":  # 编辑 新增 模式
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_addItem_posXpath"]).click()
                        item_value_str = new_item
                        # 匹配多个multiple substrings 类型
                        if "&" in item_value_str:  # & 含有多个 and multiple substrings
                            item_values = item_value_str.split("&")
                        else:
                            item_values = [item_value_str]
                    else:  # 修改模式
                        self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_search_item_posXpath"]).send_keys(src_item + Keys.ENTER)
                        self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_edit_item_posXpath"]).click()
                        input_field = self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputItem_posXpath"])
                        input_field.send_keys(Keys.CONTROL, 'a')  # 或使用 Keys.COMMAND 在 macOS
                        input_field.send_keys(Keys.DELETE)
                        item_values = [new_item]
                    for j, item_value in enumerate(item_values):  # 遍历添加 multi substr，第一个元素不用点击 + 图标
                        item_value = item_value.strip()
                        if j == 0:
                            # 适配24.10 版本，需要逐个字符输入
                            input_field = self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputItem_posXpath"])
                            for char in str(item_value):
                                input_field.send_keys(char)
                                time.sleep(0.1)
                        else:
                            self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_sameItem_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_sameItem_inputItem_posXpath"]).send_keys(item_value)
                    self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()
                elif object_type == "flag":
                    if src_item == "":  # 直接 新增 模式
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_addItem_posXpath"]).click()
                        for key_flag in new_item:
                            if key_flag == "Bulky" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[2]").click()
                            elif key_flag == "CBR Streaming":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[3]").click()
                            elif key_flag == "Client is Local" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[4]").click()
                            elif key_flag == "Server is Local" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[5]").click()
                            elif key_flag == "Download" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[6]").click()
                            elif key_flag == "Interactive" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[7]").click()
                            elif key_flag == "Inbound" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[8]").click()
                            elif key_flag == "Outbound" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[9]").click()
                            elif key_flag == "Pseudo Unidirectional" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[10]").click()
                            elif key_flag == "Streaming" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[11]").click()
                            elif key_flag == "Unidirectional" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[12]").click()
                            elif key_flag == "Random looking" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[13]").click()
                            elif key_flag == "C2S" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[14]").click()
                            elif key_flag == "S2C" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[15]").click()
                            elif key_flag == "Bidirectional" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[16]").click()
                            elif key_flag == "Tunneling" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[17]").click()
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()
                    elif src_item != "":
                        self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_edit_item_posXpath"]).click()
                        #对源item双击取消
                        for key_flag in src_item:
                            if key_flag == "Bulky":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[2]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[2]").click()
                            elif key_flag == "CBR Streaming":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[3]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[3]").click()
                            elif key_flag == "Client is Local" :
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[4]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[4]").click()
                            elif key_flag == "Server is Local":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[5]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[5]").click()
                            elif key_flag == "Download":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[6]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[6]").click()
                            elif key_flag == "Interactive":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[7]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[7]").click()
                            elif key_flag == "Inbound" :
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[8]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[8]").click()
                            elif key_flag == "Outbound":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[9]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[9]").click()
                            elif key_flag == "Pseudo Unidirectional":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[10]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[10]").click()
                            elif key_flag == "Streaming":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[11]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[11]").click()
                            elif key_flag == "Unidirectional":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[12]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[12]").click()
                            elif key_flag == "Random looking":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[13]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[13]").click()
                            elif key_flag == "C2S":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[14]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[14]").click()
                            elif key_flag == "S2C":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[15]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[15]").click()
                            elif key_flag == "Bidirectional" :
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[16]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[16]").click()
                            elif key_flag == "Tunneling":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[17]").click()
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[17]").click()
                        #添加新item
                        for key_flag in new_item:
                            if key_flag == "Bulky" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[2]").click()
                            elif key_flag == "CBR Streaming":
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[3]").click()
                            elif key_flag == "Client is Local" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[4]").click()
                            elif key_flag == "Server is Local" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[5]").click()
                            elif key_flag == "Download" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[6]").click()
                            elif key_flag == "Interactive" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[7]").click()
                            elif key_flag == "Inbound" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[8]").click()
                            elif key_flag == "Outbound" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[9]").click()
                            elif key_flag == "Pseudo Unidirectional" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[10]").click()
                            elif key_flag == "Streaming" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[11]").click()
                            elif key_flag == "Unidirectional" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[12]").click()
                            elif key_flag == "Random looking" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[13]").click()
                            elif key_flag == "C2S" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[14]").click()
                            elif key_flag == "S2C" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[15]").click()
                            elif key_flag == "Bidirectional" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[16]").click()
                            elif key_flag == "Tunneling" and new_item[key_flag] == True:
                                self.driver.find_element(By.XPATH, "//*[@class='flag-object-flag']//span[17]").click()
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()
                elif object_type == "interval":
                    if src_item == "":
                        data_int = new_item.split("-")
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_addItem_posXpath"]).click()  # 点击“+”按钮
                        # 在空内容的输入框中，输入新增的数据
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_lowBoundary_posXpath"]).send_keys(eval(str(data_int))[0])  # 于item 下low_boundary value输入框键入item_value
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_upBoundary_posXpath"]).send_keys(eval(str(data_int))[1])  # 于item 下up_boundary value输入框键入item_value
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_button_saveItem_posXpath"]).click()  # 点击保存按钮
                    elif src_item != "":
                        data_int = new_item.split("-")
                        self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_search_item_posXpath"]).send_keys(src_item + Keys.ENTER)
                        self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_edit_item_posXpath"]).click()
                        # 清空内容：模拟 Ctrl + A 全选后删除
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_lowBoundary_posXpath"]).send_keys(Keys.CONTROL, 'a')  # 或使用 Keys.COMMAND 在 macOS
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_lowBoundary_posXpath"]).send_keys(Keys.DELETE)
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputItem_upBoundary_posXpath"]).send_keys(Keys.CONTROL,'a')  # 或使用 Keys.COMMAND 在 macOS
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputItem_upBoundary_posXpath"]).send_keys(Keys.DELETE)
                        time.sleep(0.5)
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputItem_lowBoundary_posXpath"]).send_keys(eval(str(data_int))[0])  # 于item 下low_boundary value输入框键入item_value
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputItem_upBoundary_posXpath"]).send_keys(eval(str(data_int))[1])  # 于item 下up_boundary value输入框键入item_value
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_button_saveItem_posXpath"]).click()  # 点击保存按钮
                elif object_type == "application":
                    if src_item == "":
                        #添加signature
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_addItem_posXpath"]).click()
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_create_signature_posXpath"]).click()
                        for m in range(len(new_item)):
                            app_surrogates= new_item[m]
                            for i in range(len(app_surrogates["signature_sequence"])):
                                app_signature= app_surrogates["signature_sequence"][i]
                                self.driver.find_element(By.XPATH,edit_element_position["signature_inputName_posXpath"]).send_keys(app_signature["signature"]["name"])
                                self.driver.find_element(By.XPATH, edit_element_position["signature_add_artibutem_posXpath"]).click()
                                for j in range(len(app_signature["signature"]["and_conditions"])):
                                    app_and_condition= app_signature["signature"]["and_conditions"][j]
                                    self.driver.find_element(By.XPATH, edit_element_position["signature_condition_select_up_posXpath"]).click()
                                    if app_and_condition["negate_option"] == False:
                                        self.driver.find_element(By.XPATH, edit_element_position["signature_new_condition__posXpath"]).click()
                                    else:self.driver.find_element(By.XPATH, edit_element_position["signature_new_not_condition__posXpath"]).click()
                                    self.driver.find_element(By.XPATH, edit_element_position["signature_add_artibute_button_posXpath"]).click()
                                    for n in range(len(app_and_condition["or_conditions"])):
                                        app_or_condition= app_and_condition["or_conditions"][n]
                                        self.driver.find_element(By.XPATH,"//li[@class = 'MuiTreeItem-root css-105mfs8']//div[text()='common']").click()
                                        self.driver.find_element(By.XPATH,edit_element_position["signature_artibute_protocols"].format(replaceValue=app_or_condition["attribute_name"])).click()
                                        self.driver.find_element(By.XPATH,"(//div[@class='MuiDrawer-content css-10lcz44'])[4]//button[text()='Cancel']").click()
                                        self.driver.find_element(By.XPATH,edit_element_position["attribute_add_object_posXpath"]).click()
                                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_create_signature_posXpath"]+"[2]").click()
                                        common_object_element_position = get_element_position(app_or_condition["type"])
                                        self.create_objects_by_side_slide(app_or_condition,common_object_element_position)
                                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_okButton_posXpath"]+"[4]").click()
                                        self.driver.find_element(By.XPATH,"(//div[@class='MuiDrawer-content css-10lcz44'])[4]//button[text()='Cancel']").click()
                                self.driver.find_element(By.XPATH,edit_element_position["objectPage_okButton_posXpath"]+"[3]").click()
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_okButton_posXpath"]+"[2]").click()
                        self.driver.find_element(By.XPATH,"(//div[@class='MuiDrawer-content css-10lcz44'])[1]//button[text()='Cancel']").click()
                    elif src_item != "":
                        self.driver.find_element(By.XPATH, edit_element_position["objectPage_addItem_posXpath"]).click()
                        self.driver.find_element(By.XPATH,"//input[@class='MuiInput-input css-za5rna']").send_keys(src_item["signature_sequence"][0]["signature"]["name"] + Keys.ENTER)
                        self.driver.find_element(By.XPATH,"//i[@class='iconfont icon-Edit !text-[var(--color-text)]']").click()
                        name_input_field = self.driver.find_element(By.XPATH, edit_element_position["signature_inputName_posXpath"])
                        name_input_field.send_keys(Keys.CONTROL, 'a')  # 或使用 Keys.COMMAND 在 macOS
                        name_input_field.send_keys(Keys.DELETE)
                        name_input_field.send_keys("signature_edit_name")
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_okButton_posXpath"] + "[2]").click()

                elif object_type == "tunnel":
                    if src_item == "":
                        if len(new_item) == 1:
                            tunnel_endition_a = new_item[0]
                        elif len(new_item) == 2:
                            tunnel_endition_a = new_item[0]
                            tunnel_endition_b = new_item[1]

                        for i in range(len(tunnel_endition_a["or_conditions"])):
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_endition_a_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH, edit_element_position["objectPage_side_slic_create_button_posXpath"]).click()
                            time.sleep(1)
                            common_object_element_position = get_element_position(tunnel_endition_a["or_conditions"][i]["type"])
                            self.create_objects_by_side_slide(tunnel_endition_a["or_conditions"][i],common_object_element_position)
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_okButton_posXpath"]+"[2]").click()
                            self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_side_slic_Cancel_posXpath"]).click()
                        if len(new_item) == 2:
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_endition_b_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_endition_b_addItem_posXpath"]).click()
                            self.driver.find_element(By.XPATH, edit_element_position["objectPage_side_slic_create_button_posXpath"]).click()

                            for i in range(len(tunnel_endition_b["or_conditions"])):
                                self.create_objects_by_side_slide(tunnel_endition_b["or_conditions"][i], common_object_element_position)
                                self.driver.find_element(By.XPATH,edit_element_position["objectPage_okButton_posXpath"] + "[2]").click()
                                self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_side_slic_Cancel_posXpath"]).click()
                    elif src_item != "":
                        if len(src_item) == 1:
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_endition_a_editItem_posXpath"]).click()
                            name_input_field = self.driver.find_element(By.XPATH,"//div[@class='ip-object-name']//input")
                            name_input_field.send_keys(Keys.CONTROL, 'a')  # 或使用 Keys.COMMAND 在 macOS
                            name_input_field.send_keys(Keys.DELETE)
                            name_input_field.send_keys("tunnel_edit_A")
                            self.driver.find_element(By.XPATH, edit_element_position["objectPage_okButton_posXpath"] + "[2]").click()
                            self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_side_slic_Cancel_posXpath"]).click()
                elif object_type == "ip_learning":
                    self.driver.find_element(By.XPATH,edit_element_position["objectPage_ipLearningType_posXpath"]).click()
                    if object["op"] == "add":
                        for i in range(0,len(object["learning_plan"]["fqdn_ip_learning_plan"]["from_fqdns"])):
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_addItem_posXpath"]).click()
                            send_data = object["learning_plan"]["fqdn_ip_learning_plan"]["from_fqdns"][i]
                            input_field = self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_posXpath"])
                            for char in str(send_data):
                                input_field.send_keys(char)
                                time.sleep(0.1)
                            self.driver.find_element(By.XPATH, edit_element_position["objectPage_button_saveItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH, edit_element_position["objectPage_learnFromProtocols_up_select_posXpath"]).click()
                    if object["learning_plan"]["fqdn_ip_learning_plan"]["from_protocol"] == "HTTP":
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_learnFromProtocols_http_posXpath"]).click()
                    elif object["learning_plan"]["fqdn_ip_learning_plan"]["from_protocol"]  == "SSL":
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_learnFromProtocols_ssl_posXpath"]).click()
                    # self.driver.find_element(By.XPATH, ip_addressObjectPage_button_IP_learn_from_protocols_up_posXpath).click()
                    self.driver.find_element(By.XPATH, edit_element_position["objectPage_agingTimes_posXpath"]).send_keys(object["learning_plan"]["fqdn_ip_learning_plan"]["aging_time"] )
                    self.driver.find_element(By.XPATH,edit_element_position["objectPage_voteClients_posXpath"]).send_keys(object["learning_plan"]["fqdn_ip_learning_plan"]["vote_client_num"])
                    self.driver.find_element(By.XPATH,edit_element_position["objectPage_learnedIPLimits_posXpath"]).send_keys(object["learning_plan"]["fqdn_ip_learning_plan"]["goal_upper_limit"])
                else:
                    if src_item == "":
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_addItem_posXpath"]).click()
                        # 适配24.10 版本，需要逐个字符输入
                        input_field = self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_posXpath"])
                        for char in str(new_item):
                            input_field.send_keys(char)
                            time.sleep(0.1)
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()
                    elif src_item != "":
                        self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_search_item_posXpath"]).send_keys(src_item + Keys.ENTER)
                        self.driver.find_element(By.XPATH,edit_element_position["ObjectPage_edit_item_posXpath"]).click()
                        input_field = self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_posXpath"])
                        # 清空内容：模拟 Ctrl + A 全选后删除
                        input_field.send_keys(Keys.CONTROL, 'a')  # 或使用 Keys.COMMAND 在 macOS
                        input_field.send_keys(Keys.DELETE)
                        time.sleep(0.5)
                        for char in str(new_item):
                            self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_posXpath"]).send_keys(char)
                            time.sleep(0.1)
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()
    
                if "statistics_option" in object.keys():
                    # 如果修改Object的统计参数则进行操作
                    statistics_option_temp = object["statistics_option"]
                    time.sleep(1)
                    if statistics_option_temp in {"brief", "elaborate"}:
                        self.driver.find_element(By.XPATH,edit_element_position["objectPage_statistics_select_posXpath"]).click()
                        element_dropdown_item = self.driver.find_element(By.XPATH, edit_element_position["objectPage_statistics_select_option_posXpath"].format(statistics_option_temp))
                        # 移动元素到页面，在执行点击
                        self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                        self.driver.execute_script("arguments[0].click();", element_dropdown_item)
                # 确认创建
                self.driver.find_element(By.XPATH, edit_element_position["objectPage_okButton_posXpath"]).click()
                # self.driver.find_element(By.XPATH, edit_element_position["objectPage_okButton_warningYes_posXpath"]).click()
                return 200
        except Exception as e:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            # return 400

    def create_group(self, object, object_type, object_element_position):
        page_jump_element_position = object_element_position["page_jump"]
        edit_element_position = object_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_object_page(page_jump_element_position)
            # 点击create group
            self.driver.find_element(By.ID, edit_element_position["objectListPage_createButton_posId"]).click()
            if object_type == "ApplicationGroup":
                pass
            else:
                self.driver.find_element(By.ID, edit_element_position[
                    "objectListPage_dropDown_createGroupButton_posId".format(object_type)]).click()
            # 输入name
            object_name = object["name"]
            self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputName_posXpath"]).send_keys(
                object_name)
            # 切换type
            if object["select_type"] == True:
                self.driver.find_element(By.ID, edit_element_position[
                    "groupObjectPage_selectType{}_posId".format(object_type)]).click()
            # 点subordinate的+
            self.driver.find_element(By.XPATH,
                                     edit_element_position["groupObjectPage_addSubordinate_posXpath"]).click()
            # 添加subordinate
            group_subordinate_data = object["group_subordinate"]
            if len(group_subordinate_data) != 0:
                for x in range(len(group_subordinate_data)):
                    time.sleep(0.5)
                    self.driver.find_element(By.XPATH, edit_element_position[
                        "groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(
                        group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, edit_element_position[
                        "groupObjectPage_searchSubordinate{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = edit_element_position[
                        "groupObjectPage_selectSubordinate{}_posXpath".format(object_type)].format(
                        replaceValue=group_subordinate_data[x]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, edit_element_position[
                        "groupObjectPage_closeSubordinate{}_posXpath".format(object_type)]).click()
                    if len(group_subordinate_data) > 1 and x < len(group_subordinate_data) - 1:
                        self.driver.find_element(By.ID, edit_element_position[
                            "groupObjectPage_addSubordinateObject_posId"]).click()
            # 判断是否存在exclude
            group_exclude_data = object["group_exclude"]
            if len(group_exclude_data) != 0:
                # 使能exclude
                self.driver.find_element(By.XPATH,
                                         edit_element_position["groupObjectPage_enableExclude_posXpath"]).click()
                # 点exclude的+
                self.driver.find_element(By.XPATH,
                                         edit_element_position["groupObjectPage_addExclude_posXpath"]).click()
                # 添加exclude
                group_exclude_data = object["group_exclude"]
                for y in range(len(group_exclude_data)):
                    time.sleep(0.5)
                    self.driver.find_element(By.XPATH, edit_element_position[
                        "groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(
                        group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, edit_element_position[
                        "groupObjectPage_searchExclude{}_posXpath".format(object_type)]).send_keys(Keys.ENTER)
                    temp_element_position = edit_element_position[
                        "groupObjectPage_selectExclude{}_posXpath".format(object_type)].format(
                        replaceValue=group_exclude_data[y]["name"])
                    self.driver.find_element(By.XPATH, temp_element_position).click()
                    self.driver.find_element(By.XPATH, edit_element_position[
                        "groupObjectPage_closeExclude{}_posXpath".format(object_type)]).click()
                    if len(group_exclude_data) > 1 and y < len(group_exclude_data) - 1:
                        self.driver.find_element(By.ID, edit_element_position[
                            "groupObjectPage_addExcludeObject_posId"]).click()
            # 确认创建
            self.driver.find_element(By.XPATH, edit_element_position["objectPage_okButton_posXpath"]).click()
            self.driver.find_element(By.XPATH,
                                     edit_element_position["objectPage_okButton_warningYes_posXpath"]).click()
            return 200
        except Exception as e:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", file=sys.stderr, flush=True)
            raise
            # return 400


    def create_objects_by_side_slide(self,object,common_object_element_position):
        object_type = object["type"]
        edit_element_position = common_object_element_position["create"]
        self.driver.find_element(By.XPATH,'//ul[@class="base-Popper-root MuiMenu-root Mui-expanded MuiMenu-variantOutlined MuiMenu-colorNeutral MuiMenu-sizeMd css-131n2dh"]/li[1]').click()
        object_name = object["name"]
        self.driver.find_element(By.XPATH, edit_element_position["objectPage_inputName_posXpath"]).send_keys(object_name)
        if object_type in ["url", "account", "phone_number", "fqdn", "subscriberid", "apn"]:
            if object_type == "phone_number":
                self.driver.find_element(By.XPATH,edit_element_position["objectPage_phnoeNumberType_posXpath"]).click()
            for i in range(len(object["items"])):  #
                self.driver.find_element(By.XPATH, edit_element_position["objectPage_addItem_posXpath"]).click()
                if object["items"][i]["op"] == "add":  # 直接 新增 模式
                    if "->" in object["items"][i]["expression"]:  # -> 存在，需要拆分
                        item_value_str = object["items"][i]["expression"].split("->")[0].strip()
                    else:  # -> 不存在，直接取值
                        item_value_str = object["items"][i]["expression"].strip()
                    # 匹配多个multiple substrings 类型
                    if "&" in item_value_str:  # & 含有多个 and multiple substrings
                        item_values = item_value_str.split("&")
                    else:
                        item_values = [item_value_str]
                else:  # 修改模式，未完成
                    # print("todo modify moudle ...")
                    item_values = [object["items"][i]["item_value"]]
                for j, item_value in enumerate(item_values):  # 遍历添加 multi substr，第一个元素不用点击 + 图标
                    item_value = item_value.strip()
                    if j == 0:
                        # 适配24.10 版本，需要逐个字符输入
                        input_field = self.driver.find_element(By.XPATH,
                                                               edit_element_position["objectPage_inputItem_posXpath"])
                        for char in str(item_value):
                            input_field.send_keys(char)
                            time.sleep(0.1)
                    else:
                        self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_sameItem_addItem_posXpath"]).click()
                        self.driver.find_element(By.XPATH, edit_element_position["ObjectPage_sameItem_inputItem_posXpath"]).send_keys(item_value)
                self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()
        elif object_type == "ip":
            for i in range(len(object["items"])):
                if object["items"][i]["op"] == "add":
                    self.driver.find_element(By.XPATH, edit_element_position["objectPage_addItem_posXpath"]).click()
                    # 适配24.10 版本，需要逐个字符输入
                    input_field = self.driver.find_element(By.XPATH,edit_element_position["objectPage_inputItem_posXpath"])
                    for char in str(object["items"][i]["ip"]):
                        input_field.send_keys(char)
                        time.sleep(0.1)
                    self.driver.find_element(By.XPATH,edit_element_position["objectPage_button_saveItem_posXpath"]).click()


