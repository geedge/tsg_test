import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from support.general_ui_utils.element_position.dashboard_element_position import *

class CreateDashboard:

    def __init__(self,driver):
        self.driver = driver
        self.filter_operations =[]

    def create(self, data, visualization_type, metric_type, multiple_dimension):
        try:
            # 进入自定义Dashboard下Chart创建页面
            self.driver.find_element(By.XPATH, mainPage_main_dashboard_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_create_button_dashboard_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_add_chart_button_posXpath).click()

            self.add_chart(data, visualization_type, metric_type, multiple_dimension)

            #点击OK
            self.driver.find_element(By.XPATH, dashboard_chart_save_OK_button_posXpath).click()

            if data["sub_type"] == "error_name":
                error_text = self.driver.find_element(By.XPATH, dashboard_chart_name_error_text_posYpath).text
                assert error_text == "Please enter"
            elif data["sub_type"] == "error_metric":
                error_text = self.driver.find_element(By.XPATH,dashboard_chart_different_metric_error_text_posYpath).text
                assert error_text == "The units of the composite fields are different and cannot be selected at the same time" or \
                       error_text == "The label cannot be empty or the same"
            elif data["sub_type"] == "error_dimensions":
                error_text = self.driver.find_element(By.XPATH, dashboard_chart_dimensions_error_text_posXpath).text
                assert error_text == "The dimensions cannot be empty and can only have one dimension"
            else:
                self.driver.find_element(By.XPATH, mainPage_save_dashboard_button_posXpath).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],f"Exception: {e}", flush=True)
            return 400

    def add_chart(self,data, visualization_type, metric_type, multiple_dimension):
        # 添加Name
        if data["sub_type"] == "error_name":
            self.driver.find_element(By.XPATH, dashboard_chart_name_text_input_posXpath).send_keys("")
        else:
            self.driver.find_element(By.XPATH, dashboard_chart_name_text_input_posXpath).send_keys(
                "Create_" + data["data_source"])

        # #根据data选择type
        visualization_type_element = dashboard_chart_visualization_type_posXpath.replace("type", visualization_type)
        self.driver.find_element(By.XPATH, visualization_type_element).click()

        # #根据data切换Data Source
        self.driver.find_element(By.XPATH, dashboard_chart_data_source_select_up_posXpath).click()
        self.is_allow_element_click(element=f"//span[text()='{data['data_source']}']")  # 下滑到元素可见位置
        self.driver.find_element(By.XPATH, f"//span[text()='{data['data_source']}']").click()

        select_count = 1
        row_count = 1
        if data['data_source'] == "Traffic Metrics":
            self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
        if metric_type == "single":
            if visualization_type == "Table":
                for metric_len in range(len(data["metric"]["single_type"])):
                    if metric_len != 0:
                        self.is_allow_element_click(dashboard_chart_metric_add_button_posXpath)
                        self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
                    # 添加field选项
                    self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    self.driver.find_element(By.XPATH,f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{data['metric']['single_type'][metric_len]['field']}'])[{row_count}]").click()
                    # 添加aggregate
                    self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    select_count += 2
                    if data['metric']['single_type'][metric_len]['aggregate'] == "random":
                        self.random_select()
                    else:
                        self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{data['metric']['single_type'][metric_len]['aggregate']}']").click()
                    row_count += 1
            else:
                self.metric = random.choice(data['metric']['single_type'])
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
                        self.driver.find_element(By.XPATH,
                                                 f"//div[@x-placement='bottom-start']//span[text()='{data['metric']['single_type'][metric_len]['aggregate']}']").click()
                    row_count += 1
            else:
                self.metric = random.choice(data['metric']['multiple_type'])
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

        # 添加dimension
        dimension_select = 1
        if data["dimensions"] != "":
            # dimensions选择多个
            if multiple_dimension == True:
                if data["data_source"] == "Proxy Rule Hits" or data["data_source"] == "Service Chaining Rule Hits":
                    self.dimensions = random.sample(data["dimensions"], 5)
                else:
                    self.dimensions = data["dimensions"]
                for dimension in self.dimensions:
                    scrollable_div = self.driver.find_element(By.XPATH,
                                                              dashboard_chart_dimension_add_button_posYpath)
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

        # 添加order_by
        if visualization_type != "Line" and visualization_type != "Area":
            self.driver.find_element(By.XPATH, dashboard_chart_order_by_posXpath).click()
            self.random_select()

        # 添加limit
        self.driver.find_element(By.XPATH, dashboard_chart_limit_posXpath).click()
        self.random_select()

        # 添加filter
        field_len = 1
        for filter_len in range(len(data["filter"])):
            value_len = 1
            # 点击添加and条件
            self.is_allow_element_click(element=dashboard_chart_filter_add_button_posYpath)
            self.driver.find_element(By.XPATH, dashboard_chart_filter_add_button_posYpath).click()
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
            self.filter_operations.append(filter_operator)


    #将元素可见
    def is_allow_element_click(self,element):
        scrollable_div = self.driver.find_element(By.XPATH,element)
        self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)

    #选中随即元素
    def random_select(self):
        time.sleep(1)
        limit_elements = self.driver.find_elements(By.XPATH, "//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li")
        limit_id = random.randint(1, len(limit_elements))
        # print(len(limit_elements),limit_id)
        self.is_allow_element_click(f"//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li[{limit_id}]")
        filter_operator = self.driver.find_element(By.XPATH,f"//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li[{limit_id}]").text
        self.driver.find_element(By.XPATH, f"//div[contains(@x-placement,'start')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li[{limit_id}]").click()
        limit_elements.clear()
        return filter_operator

    def create_chart_data_verify(self,data,visualization_type,metric_type,multiple_dimension):
        try:
            edit_btn = self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath)
            self.driver.execute_script("arguments[0].click()", edit_btn)  # 强制点击
            self.driver.find_element(By.XPATH, dashboard_chart_up_button_posXpath).click()
            self.driver.find_element(By.XPATH, dashboard_chart_up_edit_button_posXpath).click()
            # visualization_type校验
            chart_visualization_type = self.driver.find_element(By.XPATH,dashboard_chart_visualization_type_text_posXpath).text
            assert visualization_type == chart_visualization_type
            #data source校验
            data_source = self.driver.find_element(By.XPATH,dashboard_chart_data_source_select_text_posXpath).get_attribute("innerText")
            assert data_source == data["data_source"]
            #校验metric
            if metric_type == "single":
                if visualization_type == "Table":
                    metric_len = len(data["metric"]["single_type"])
                    for row in range(metric_len):
                        field = data["metric"]["single_type"][row]["field"]
                        field_text = self.driver.find_element(By.XPATH,dashboard_chart_metric_text_posXpath.format(row + 1, 1)).text
                        assert field_text == field
                else:
                    metric_len = 1
                    for row in range(metric_len):
                        field = self.metric["field"]
                        field_text = self.driver.find_element(By.XPATH,dashboard_chart_metric_text_posXpath.format(row + 1, 1)).text
                        assert field_text == field

            else:
                if visualization_type == "Table":
                    metric_len = len(data["metric"]["multiple_type"])
                    for row in range(metric_len):
                        field = data["metric"]["multiple_type"][row]["field"]
                        for i in range(len(field)):
                            field_text = self.driver.find_element(By.XPATH, dashboard_chart_metric_text_posXpath.format(row + 1,i + 1)).text
                            assert field_text == field[i]
                else:
                    metric_len = 1
                    for row in range(metric_len):
                        field = self.metric["field"]
                        for i in range(len(field)):
                            field_text = self.driver.find_element(By.XPATH, dashboard_chart_metric_text_posXpath.format(row + 1,i + 1)).text
                            assert field_text == field[i]


            #校验Dimensions
            if multiple_dimension == True:
                for i in range(len(self.dimensions)):
                    dimension = self.dimensions[i]
                    dimension_text = self.driver.find_element(By.XPATH,dashboard_chart_dimension_text_posYpath.format(i + 1)).get_attribute("innerText")
                    assert dimension_text == dimension
            else:
                dimension_text = self.driver.find_element(By.XPATH,dashboard_chart_dimension_text_posYpath.format(1)).get_attribute("innerText")
                assert dimension_text == self.dimension

            #校验filter
            for i in range(len(data["filter"])):
                filter_text_index = 2 * i + 1  # 计算筛选文本的索引
                operation_text_index = 2 * i + 2  # 计算操作文本的索引
                filte_text = self.driver.find_element(By.XPATH,dashboard_chart_filter_text_posYpath.format(filter_text_index)).get_attribute("innerText")
                assert data["filter"][i]["field"] == filte_text
                operation_text = self.driver.find_element(By.XPATH,dashboard_chart_filter_text_posYpath.format(operation_text_index)).get_attribute("innerText")
                assert operation_text == self.filter_operations[i]

            self.driver.find_element(By.XPATH, dashboard_chart_save_OK_button_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_save_dashboard_button_posXpath).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],f"Exception: {e}", flush=True)
            return 400

    def empty_chart(self):
        try:
            self.driver.find_element(By.XPATH, mainPage_main_dashboard_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_create_button_dashboard_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_save_dashboard_button_posXpath).click()
            return 200,self.driver.find_element(By.XPATH,dashboard_empty_chart_save_alter_text_posXpath).text
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400

    def limit_chart(self,data,visualization_type,metric_type,multiple_dimension):
        try:
            self.driver.find_element(By.XPATH, mainPage_main_dashboard_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_create_button_dashboard_posXpath).click()
            for i in range(21):
                self.driver.find_element(By.XPATH, mainPage_add_chart_button_posXpath).click()
                if i == 20:
                    assert self.driver.find_element(By.XPATH, dashboard_empty_chart_save_alter_text_posXpath).text == "Only up to 20 Widgets can be added"
                    break
                self.add_chart(data,visualization_type,metric_type,multiple_dimension)
                self.driver.find_element(By.XPATH, dashboard_chart_save_OK_button_posXpath).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400