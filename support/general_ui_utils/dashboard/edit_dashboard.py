import random
import time

from selenium.webdriver.common.by import By
from support.general_ui_utils.element_position.dashboard_element_position import *
from datetime import datetime
class EditDashboard:

    def __init__(self,driver):
        self.driver = driver
        self.model = 1

    def edit(self,data,visualization_type,metric_type,multiple_dimension):
        try:
            #进入chart编辑页面
            edit_btn = self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath)
            self.driver.execute_script("arguments[0].click()", edit_btn)  # 强制点击
            self.driver.find_element(By.XPATH, dashboard_chart_up_button_posXpath).click()
            self.driver.find_element(By.XPATH, dashboard_chart_up_edit_button_posXpath).click()
            #清空metrci
            self.delete_metric(visualization_type)
            #重新添加metric
            select_count = 1
            row_count = 1
            if metric_type == "single":
                if visualization_type == "Table":
                    for metric_len in range(len(data["metric"]["single_type"])):
                        if metric_len != 0:
                            self.is_allow_element_click(dashboard_chart_metric_add_button_posXpath)
                            self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
                        # 添加field选项
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{data['metric']['single_type'][metric_len]['field']}'])[{row_count}]").click()
                        # 添加aggregate
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        select_count += 2
                        if data['metric']['single_type'][metric_len]['aggregate'] == "random":
                            self.random_select()
                        else:
                            self.driver.find_element(By.XPATH,
                                                     f"//div[@x-placement='bottom-start']//span[text()='{data['metric']['single_type'][metric_len]['aggregate']}']").click()
                        # 修改时对label进行修改
                        if data['metric']['single_type'][metric_len]['label'] != "":
                            self.driver.find_element(By.XPATH,
                                                     f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                            self.driver.find_element(By.XPATH,
                                                     f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(
                                data['metric']['single_type'][metric_len]['label'])
                        row_count += 1
                else:
                    self.metric = data['metric']['single_type'][1]
                    self.driver.find_element(By.XPATH,
                                             f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    self.driver.find_element(By.XPATH,
                                             f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{self.metric['field']}'])[{row_count}]").click()
                    self.driver.find_element(By.XPATH,
                                             f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    select_count += 2
                    if self.metric['aggregate'] == "random":
                        self.random_select()
                    else:
                        self.driver.find_element(By.XPATH,
                                                 f"//div[@x-placement='bottom-start']//span[text()='{self.metric['aggregate']}']").click()
                    if self.metric['label'] != "":
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(
                            self.metric['label'])
            elif metric_type == "multiple":
                if visualization_type == "Table":
                    for metric_len in range(len(data["metric"]["multiple_type"])):
                        if metric_len != 0:
                            self.is_allow_element_click(dashboard_chart_metric_add_button_posXpath)
                            self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        for metric in data['metric']['multiple_type'][metric_len]['field']:
                            self.driver.find_element(By.XPATH,
                                                     f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{metric}'])[{row_count}]").click()
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        select_count += 2
                        if data['metric']['multiple_type'][metric_len]['aggregate'] == "random":
                            self.random_select()
                        else:
                            self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{data['metric']['single_type'][metric_len]['aggregate']}']").click()
                        if data['metric']['single_type'][metric_len]['label'] != "":
                            self.driver.find_element(By.XPATH,
                                                     f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                            self.driver.find_element(By.XPATH,
                                                     f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(
                                data['metric']['single_type'][metric_len]['label'])
                        row_count += 1
                else:
                    self.metric = data['metric']['multiple_type'][0]
                    self.driver.find_element(By.XPATH,
                                             f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    for metric_field in self.metric['field']:
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{metric_field}'])[{row_count}]").click()
                    self.driver.find_element(By.XPATH,
                                             f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    select_count += 2
                    if self.metric['aggregate'] == "random":
                        self.random_select()
                    else:
                        self.driver.find_element(By.XPATH,
                                                 f"//div[@x-placement='bottom-start']//span[text()='{self.metric['aggregate']}']").click()
                    if self.metric['label'] != "":
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                        self.driver.find_element(By.XPATH,
                                                 f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(
                            self.metric['label'])
            #清空dimension
            self.delete_dimensions()
            #重新添加dimension
            dimension_select = 1
            if data["dimensions"] != "":
                # dimensions选择多个
                if multiple_dimension == True:
                    if data["data_source"] == "Proxy Rule Hits" or data["data_source"] == "Service Chaining Rule Hits":
                        self.dimensions = random.sample(data["dimensions"], 5)
                    else:
                        self.dimensions = data["dimensions"]
                    for dimension in self.dimensions:
                        scrollable_div = self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath)
                        self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)
                        self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath).click()
                        self.driver.find_element(By.XPATH,
                                                 f"(//label[text()='Dimensions']/parent::*//div[@class='el-input el-input--small el-input--suffix'])[{dimension_select}]").click()
                        dimension_select += 1
                        self.driver.find_element(By.XPATH,
                                                 f"//div[@x-placement='bottom-start']//span[text()='{dimension}']").click()
                # dimensions选择单个，随机选择
                elif multiple_dimension == False:
                    self.dimension = random.choice(data["dimensions"])
                    if visualization_type == "Line" or visualization_type == "Area":
                        while self.dimension == "Time":
                            self.dimension = random.choice(data["dimensions"])
                    scrollable_div = self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath)
                    self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)
                    self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath).click()
                    self.driver.find_element(By.XPATH,
                                             f"(//label[text()='Dimensions']/parent::*//div[@class='el-input el-input--small el-input--suffix'])[{dimension_select}]").click()
                    self.driver.find_element(By.XPATH,
                                             f"//div[@x-placement='bottom-start']//span[text()='{self.dimension}']").click()
            else:
                pass
            #添加order_by
            if visualization_type != "Line" and visualization_type != "Area":
                self.driver.find_element(By.XPATH, dashboard_chart_order_by_posXpath).click()
                if data["order_by"] != "" :
                    self.driver.find_element(By.XPATH,
                                             f"//div[@x-placement='bottom-start']//ul//span[text()='{data['order_by']}']").click()
                else:
                    self.driver.find_element(By.XPATH, dashboard_chart_order_by_down_posXpath).click()
            #清空filter
            self.delete_filter()
            #重新添加filter
            field_len = 1
            for filter_len in range(len(data["filter"])):
                value_len = 1
                # 点击添加or条件
                if field_len == 1:
                    self.is_allow_element_click(element=dashboard_chart_filter_add_button_posYpath)
                    self.driver.find_element(By.XPATH, dashboard_chart_filter_add_button_posYpath).click()
                else:
                    self.is_allow_element_click(element=dashboard_chart_filter_or_button_posXpath)
                    self.driver.find_element(By.XPATH, dashboard_chart_filter_or_button_posXpath).click()
                # 可视化field操作框，点击并添加field
                self.is_allow_element_click(
                    element=f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]")
                self.driver.find_element(By.XPATH,
                                         f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]").click()
                value_len += 1
                self.driver.find_element(By.XPATH,
                                         f"//div[contains(@x-placement,'start')]//span[text()='{data['filter'][filter_len]['field']}']").click()
                # 点击并添加operator
                filter_operator = data['filter'][filter_len]['operator']
                self.driver.find_element(By.XPATH,
                                         f"(//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-6']").click()
                if data['filter'][filter_len]['operator'] == "random":
                    filter_operator = self.random_select()
                else:
                    self.driver.find_element(By.XPATH,
                                             f"//div[contains(@x-placement,'start')]//span[text()='{data['filter'][filter_len]['operator']}']").click()
                # 点击并添加value
                if "NULL" not in filter_operator and "EMPTY" not in filter_operator:
                    self.driver.find_element(By.XPATH,
                                             f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]").click()
                    for value in data['filter'][filter_len]['value']:
                        if value == "":
                            self.random_select()
                        elif value == "text":
                            self.driver.find_element(By.XPATH,
                                                     f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]//input").send_keys(
                                "123456")
                        else:
                            self.is_allow_element_click(element=f"//span[text()='{value}']")
                            self.driver.find_element(By.XPATH,
                                                     f"//div[contains(@x-placement,'start')]//span[text()='{value}']").click()
                field_len += 1

            self.driver.find_element(By.XPATH, dashboard_chart_save_OK_button_posXpath).click()
            if self.model == "2":
                if data["sub_type"] == "error_name":
                    error_text = self.driver.find_element(By.XPATH, dashboard_chart_name_error_text_posYpath).text
                    assert self.driver.find_element(By.XPATH,dashboard_chart_name_error_text_posYpath).text == "Please enter"
                elif data["sub_type"] == "error_metric":
                    error_text = self.driver.find_element(By.XPATH,dashboard_chart_different_metric_error_text_posYpath).text
                    assert error_text == "The units of the composite fields are different and cannot be selected at the same time" or \
                           error_text == "The label cannot be empty or the same"
                elif data["sub_type"] == "error_dimensions":
                    error_text = self.driver.find_element(By.XPATH, dashboard_chart_dimensions_error_text_posXpath).text
                    assert error_text == "The dimensions cannot be empty and can only have one dimension"
            else:
                self.driver.find_element(By.XPATH, mainPage_save_dashboard_button_posXpath).click()
                assert self.driver.find_element(By.XPATH,
                                                "//div[@class='el-card box-card is-never-shadow']//div[@class='vbox-title']/span").text == "Create_" + \
                       data["data_source"]
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400

    def delete_metric(self,visualization_type):
        if visualization_type != "Table":
            pass
        else:
            metric_elements = self.driver.find_elements(By.XPATH,dashboard_delete_metrci_posXpath)
            metric_count = len(metric_elements)
            while metric_count > 1:
                self.driver.find_element(By.XPATH,"("+dashboard_delete_metrci_posXpath+")"+f"[{metric_count}]").click()
                metric_count -= 1
            self.driver.find_element(By.XPATH,dashboard_no_delete_metrci_posXpath)
        for element in self.driver.find_elements(By.XPATH,"//div[@class='Metrics']//i[@class='el-tag__close el-icon-close']"):
            time.sleep(0.5)
            element.click()
        assert self.driver.find_element(By.XPATH, dashboard_chart_different_metric_error_text_posYpath).text == "Please select"

    def delete_dimensions(self):
        dimension_elements = self.driver.find_elements(By.XPATH,dashboard_delete_dimensions_posXpath)
        dimension_count = len(dimension_elements)
        while dimension_count > 0:
            self.is_allow_element_click("(" + dashboard_delete_dimensions_posXpath + ")" + f"[{dimension_count}]")
            self.driver.find_element(By.XPATH,"(" + dashboard_delete_dimensions_posXpath + ")" + f"[{dimension_count}]").click()
            dimension_count -= 1

    def delete_filter(self):
        filter_elements = self.driver.find_elements(By.XPATH,dashboard_delete_filter_posXpath)
        filter_count = len(filter_elements)
        while filter_count > 0:
            self.is_allow_element_click("(" + dashboard_delete_filter_posXpath + ")" + f"[{filter_count}]")
            self.driver.find_element(By.XPATH,"(" + dashboard_delete_filter_posXpath + ")" + f"[{filter_count}]").click()
            filter_count -= 1

    def is_allow_element_click(self,element):
        scrollable_div = self.driver.find_element(By.XPATH,element)
        self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)
        
    def random_select(self):
        time.sleep(1)
        limit_elements = self.driver.find_elements(By.XPATH, "//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li")
        # print(len(limit_elements))
        limit_id = random.randint(1, len(limit_elements))
        self.is_allow_element_click(f"//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li[{limit_id}]")
        filter_operator = self.driver.find_element(By.XPATH, f"//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li[{limit_id}]").text
        self.driver.find_element(By.XPATH, f"//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li[{limit_id}]").click()
        limit_elements.clear()
        return filter_operator
    
    def modify_data_verify(self,data,visualization_type):
        try:
            edit_btn = self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath)
            self.driver.execute_script("arguments[0].click()", edit_btn)  # 强制点击
            self.driver.find_element(By.XPATH, dashboard_chart_up_button_posXpath).click()
            self.driver.find_element(By.XPATH, dashboard_chart_up_edit_button_posXpath).click()
            # if visualization_type != "Line" and visualization_type != "Area":
            if visualization_type == "Bar" or visualization_type == "Pie":
                assert self.driver.find_element(By.XPATH,"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[1]").get_attribute('title') == data["order_by"]
            elif visualization_type == "Table":
                assert self.driver.find_element(By.XPATH,"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[2]").get_attribute('title') == data["order_by"]
            assert len(self.driver.find_elements(By.XPATH,"//div[@class='Filters']//span[normalize-space(text())='or']")) == len(data["filter"]) \
                    and len(self.driver.find_elements(By.XPATH,"//div[@class='Filters']//span[normalize-space(text())='and']")) == 1

            self.driver.find_element(By.XPATH, dashboard_chart_save_OK_button_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_save_dashboard_button_posXpath).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400