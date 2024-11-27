# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
from support.ui_utils.policies.page_jump import PageJump

class SearchRules:
    def __init__(self, driver):
        self.driver = driver
        
    def search_rules(self, policy_configuration, element_position, vsys_name=""):
        try:
            name = policy_configuration["name"]
            search_element_position = element_position["search"]
            page_jump_element_position = element_position["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_policy_page(page_jump_element_position)
            # 点击search查询框
            #self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_posXpath"]).click()
            btn = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_posXpath"])
            self.driver.execute_script("arguments[0].click()", btn)
            # 查询框输入搜索内容
            self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_input_itemContent_posXpath"]).send_keys(name)
            #input_item_posXpath = search_element_position["policyRuleListPage_searchLabel_input_itemContent_posXpath"]
            #self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)
            # 选择匹配的选项，内容示例：Name contains rulename 定位：//div[@class='dune-search-option-content']//span[normalize-space(text())='Name']/parent::*
            dropdown_item_posXpath = search_element_position["policyRuleListPage_searchLabel_dropDown_item_posXpath"].format(replaceValue="Name")
            btn = self.driver.find_element(By.XPATH, dropdown_item_posXpath)
            self.driver.execute_script("arguments[0].click()", btn)

            # 强制点击js方法
            # btn = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_searchButton_posId"])
            # self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
            self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_searchButton_posId"]).click()
            time.sleep(0.3)
            #self.driver.find_element(By.ID, search_element_position["policyRuleListPage_searchLabel_searchButton_posId"]).click()
            element_tr = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_tableTbody_posXpath"])
            row = element_tr.find_elements(By.XPATH, "div")
            if len(row) != 0:
                first_row = row[0]
                first_row_checkBox_element = first_row.find_element(By.XPATH, '//*[@inputprops="[object Object]"]')
                return 200, first_row_checkBox_element
            else:
                return 400, ""
        except Exception as e:
            raise

    def get_rule_uuid(self, policy_configuration, element_position, vsys_name=""):
        try:
            type = policy_configuration["type"]
            name = policy_configuration["name"]
            search_element_position = element_position["search"]
            page_jump_element_position = element_position["page_jump"]
            # 打开该列表
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_policy_page(page_jump_element_position)
            # 强制点击search查询框
            btn = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_posXpath"])
            self.driver.execute_script("arguments[0].click()", btn)
            # 通过name 查询时
            # 先输入Name，下拉列表显示Name contains rulename后选择对应选项
            self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_posXpath"]).send_keys(Keys.CONTROL + "a")
            self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_posXpath"]).send_keys(name)
            # 下拉列表显示Name contains rulename后选择对应选项
            btn = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_dropDown_item_posXpath"].format(replaceValue="Name"))
            self.driver.execute_script("arguments[0].click()", btn)  # 点击查询下拉菜单中item
            btn = self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_searchButton_posId"])
            self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
            time.sleep(1)
            if type == "security":
                rule_uuid = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            elif type == "service_chaining":
                rule_uuid = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault mouseSchedule el-popover__reference']//span").text
            elif type == "monitor":
                rule_uuid = self.driver.find_element(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            elif type == "proxy_intercept":
                rule_uuid = self.driver.find_elements(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span")[0].text.strip()
            elif type == "proxy_manipulation":
                rule_uuid = self.driver.find_elements(By.XPATH,"//span[@class='idWidth cursorDefault el-popover__reference']//span")[0].text.strip()
            elif type == "statistics":
                # 点击列设置打开列设置界面
                self.driver.find_element(By.XPATH, ruleListPage_column_set_button_posXpath).click()
                # 选择UUID
                self.driver.find_element(By.XPATH, ruleListPage_column_set_field_posXpath.format(replaceFiled="UUID")).click()
                rule_uuid = self.driver.find_element(By.XPATH, "//div[contains(@class,'MuiDataGrid-row')][1]//div[@data-field='uuid']").text
                #点击其他地方比如再次点击搜索按钮,不然影响菜单切换
                self.driver.find_element(By.XPATH, search_element_position["policyRuleListPage_searchLabel_searchButton_posId"]).click()
            elif type == "dos_protection":
                rule_uuid = self.driver.find_element(By.XPATH, "//span[@class='idWidth cursorDefault el-popover__reference']//span").text
            rule_uuids_list = []
            rule_uuids_temp_dict = {}
            rule_uuids_temp_dict["type"] = policy_configuration["type"]
            rule_uuids_temp_dict["uuid"] = rule_uuid
            rule_uuids_temp_dict["name"] = policy_configuration["name"]
            rule_uuids_temp_dict["attribute_name"] = policy_configuration["type"].upper() + "_" + "RULE"
            rule_uuids_list.append(rule_uuids_temp_dict)
            rule_uuids_tuple = tuple(rule_uuids_list)
            return rule_uuids_tuple, 200
        except Exception as e:
            return "", 400