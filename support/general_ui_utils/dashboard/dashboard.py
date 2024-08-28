import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from support.general_ui_utils.element_position.dashboard_element_position import *
import random
from datetime import datetime
class Dashboard:

    def __init__(self, driver):
        self.driver = driver
        self.model = "0" #0为首次创建，1为编辑，2为错误校验
        self.filter_operations = []

    def dashboard_case(self,data,visualization_type,metric_type,multiple_dimension):
        self.driver.implicitly_wait(10)
        self.create(data,visualization_type,metric_type,multiple_dimension)
        if self.model == "1":
            self.new_chart_data_verify(data, visualization_type, metric_type, multiple_dimension)
            self.modify(data,visualization_type,metric_type,multiple_dimension)
            self.delete()
        elif self.model == "2":
            pass

    def create(self,data,visualization_type,metric_type,multiple_dimension):
        self.driver.find_element(By.XPATH, mainPage_main_dashboard_posXpath).click()
        self.driver.find_element(By.XPATH,mainPage_create_button_dashboard_posXpath).click()
        self.driver.find_element(By.XPATH,mainPage_add_chart_button_posXpath).click()
        self.add_chart(data,visualization_type,metric_type,multiple_dimension)
        if "error" in data["subtype"]:
            self.model = "2"
        else:
            self.model = "1"
        self.confirm_creation(data)

    def new_chart_data_verify(self,data,visualization_type,metric_type,multiple_dimension):
        self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath).click()
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
        if multiple_dimension == "true":
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

        self.confirm_creation(data)



    def add_chart(self,data,visualization_type,metric_type,multiple_dimension):
        # 添加Name
        if data["subtype"] == "name_error":
            self.driver.find_element(By.XPATH, dashboard_chart_name_text_input_posXpath).send_keys("")
        else:
            self.driver.find_element(By.XPATH, dashboard_chart_name_text_input_posXpath).send_keys("Create_" + data["data_source"])
        # #根据data选择type
        visualization_type_element = dashboard_chart_visualization_type_posXpath.replace("type",visualization_type)
        self.driver.find_element(By.XPATH,visualization_type_element).click()
        # #根据data切换Data Source
        self.driver.find_element(By.XPATH,dashboard_chart_data_source_select_up_posXpath).click()
        self.is_allow_element_click(element=f"//span[text()='{data['data_source']}']")  #下滑到元素可见位置
        self.driver.find_element(By.XPATH,f"//span[text()='{data['data_source']}']").click()
        if "Top" in data['data_source']:
            assert  len(self.driver.find_elements(By.XPATH,"//div[@role='radiogroup']//label[@class='el-radio is-disabled']")) == 3
        # #添加Metric
        self.add_metric(data,visualization_type,metric_type)
        #添加Dimensions
        self.add_dimensions(data,visualization_type,multiple_dimension)
        #选择order by
        if visualization_type != "Line" and visualization_type != "Area":
            self.add_order_by(data)
        #选择limit
        self.add_limit()
        #添加add filter
        self.add_filter(data)


    def add_metric(self,data,visualization_type,metric_type):
        # if self.model == "0" :
            select_count = 1
            row_count = 1
            if data['data_source'] == "Traffic Metrics" and self.model == "0":
                self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
            if metric_type == "single":
                if visualization_type == "Table":
                    for metric_len in range(len(data["metric"]["single_type"])):
                        if metric_len != 0:
                            self.is_allow_element_click(dashboard_chart_metric_add_button_posXpath)
                            self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
                        #添加field选项
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        self.driver.find_element(By.XPATH,f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{data['metric']['single_type'][metric_len]['field']}'])[{row_count}]").click()
                        #添加aggregate
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        select_count += 2
                        if data['metric']['single_type'][metric_len]['aggregate'] == "random":
                            self._select_random()
                        else:
                            self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{data['metric']['single_type'][metric_len]['aggregate']}']").click()
                        #修改时对label进行修改
                        if self.model == "1" and data['metric']['single_type'][metric_len]['label'] !="":
                            self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                            self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(data['metric']['single_type'][metric_len]['label'])
                        row_count += 1
                else:
                    if self.model == "0":
                        self.metric = random.choice(data['metric']['single_type'])
                    elif self.model == "1":
                        self.metric = data['metric']['single_type'][1]
                    self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    self.driver.find_element(By.XPATH,f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{self.metric['field']}'])[{row_count}]").click()
                    self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    select_count += 2
                    if self.metric['aggregate'] == "random":
                        self._select_random()
                    else:
                        self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{self.metric['aggregate']}']").click()
                    if self.model == "1" and self.metric['label'] !="":
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(self.metric['label'])
            elif metric_type == "multiple":
                if visualization_type == "Table":
                    for metric_len in range(len(data["metric"]["multiple_type"])):
                        if metric_len != 0 :
                            self.is_allow_element_click(dashboard_chart_metric_add_button_posXpath)
                            self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        for metric in data['metric']['multiple_type'][metric_len]['field']:
                            self.driver.find_element(By.XPATH,f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{metric}'])[{row_count}]").click()
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                        select_count += 2
                        if data['metric']['multiple_type'][metric_len]['aggregate'] == "random":
                            self._select_random()
                        else:
                            self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{data['metric']['single_type'][metric_len]['aggregate']}']").click()
                        if self.model == "1" and data['metric']['single_type'][metric_len]['label'] != "":
                            self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                            self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(data['metric']['single_type'][metric_len]['label'])
                        row_count += 1
                else:
                    if self.model == "0":
                        self.metric = random.choice(data['metric']['multiple_type'])
                    elif self.model == "1":
                        self.metric = data['metric']['multiple_type'][0]
                    self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    for metric_field in self.metric['field']:
                        self.driver.find_element(By.XPATH,f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{metric_field}'])[{row_count}]").click()
                    self.driver.find_element(By.XPATH, f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
                    select_count += 2
                    if self.metric['aggregate'] == "random":
                        self._select_random()
                    else:
                        self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{self.metric['aggregate']}']").click()
                    if self.model == "1" and self.metric['label'] != "":
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").clear()
                        self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[{row_count}]").send_keys(self.metric['label'])

    def add_dimensions(self,data,visualization_type,multiple_dimension):
        dimension_select = 1
        if data["dimensions"] != "":
            #dimensions选择多个
            if multiple_dimension == "true":
                if data["data_source"] == "Proxy Rule Hits" or data["data_source"] == "Service Chaining Rule Hits":
                   self.dimensions = random.sample(data["dimensions"],5)
                else:
                    self.dimensions = data["dimensions"]
                for dimension in self.dimensions:
                    scrollable_div = self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath)
                    self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)
                    self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath).click()
                    self.driver.find_element(By.XPATH,f"(//label[text()='Dimensions']/parent::*//div[@class='el-input el-input--small el-input--suffix'])[{dimension_select}]").click()
                    dimension_select += 1
                    self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{dimension}']").click()
            # dimensions选择单个，随机选择
            elif multiple_dimension == "false":
                self.dimension = random.choice(data["dimensions"])
                if visualization_type == "Line" or visualization_type == "Area":
                    while self.dimension == "Time":
                        self.dimension = random.choice(data["dimensions"])
                scrollable_div = self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath)
                self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)
                self.driver.find_element(By.XPATH, dashboard_chart_dimension_add_button_posYpath).click()
                self.driver.find_element(By.XPATH,f"(//label[text()='Dimensions']/parent::*//div[@class='el-input el-input--small el-input--suffix'])[{dimension_select}]").click()
                self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{self.dimension}']").click()
        else:
            pass

    def add_order_by(self,data):
        self.driver.find_element(By.XPATH,dashboard_chart_order_by_posXpath).click()
        if self.model == "0":
           self._select_random()
        elif data["order_by"] != "" and self.model == "1":
            self.driver.find_element(By.XPATH, f"//div[@x-placement='bottom-start']//ul//span[text()='{data['order_by']}']").click()
        else:
            self.driver.find_element(By.XPATH, dashboard_chart_order_by_down_posXpath).click()
    def add_limit(self):
        self.driver.find_element(By.XPATH,dashboard_chart_limit_posXpath).click()
        self._select_random()


    def _select_random(self):
        limit_elements = self.driver.find_elements(By.XPATH, "//div[contains(@x-placement,'start')]//ul/li")
        limit_id = random.randint(0, len(limit_elements) - 1)
        self.is_allow_element_click(f"//div[contains(@x-placement,'start')]//ul/li[{limit_id + 1}]")
        filter_operator = self.driver.find_element(By.XPATH, f"//div[contains(@x-placement,'start')]//ul/li[{limit_id + 1}]").text
        self.driver.find_element(By.XPATH, f"//div[contains(@x-placement,'start')]//ul/li[{limit_id + 1}]").click()
        limit_elements.clear()
        return filter_operator

    def add_filter(self,data):
        field_len = 1
        for filter_len in range(len(data["filter"])):
            value_len = 1
            #点击添加and条件
            if self.model == "0":
                self.is_allow_element_click(element=dashboard_chart_filter_add_button_posYpath)
                self.driver.find_element(By.XPATH,dashboard_chart_filter_add_button_posYpath).click()
            elif self.model == "1":
                if field_len == 1:
                    self.is_allow_element_click(element=dashboard_chart_filter_add_button_posYpath)
                    self.driver.find_element(By.XPATH, dashboard_chart_filter_add_button_posYpath).click()
                else:
                    self.is_allow_element_click(element=dashboard_chart_filter_or_button_posXpath)
                    self.driver.find_element(By.XPATH, dashboard_chart_filter_or_button_posXpath).click()
            # 可视化field操作框，点击并添加field
            self.is_allow_element_click(element=f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]")
            self.driver.find_element(By.XPATH, f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]").click()
            value_len += 1
            self.driver.find_element(By.XPATH, f"//div[contains(@x-placement,'start')]//span[text()='{data['filter'][filter_len]['field']}']").click()
            #点击并添加operator
            filter_operator = data['filter'][filter_len]['operator']
            self.driver.find_element(By.XPATH,f"(//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-6']").click()
            if data['filter'][filter_len]['operator'] == "random":
                filter_operator = self._select_random()
            else:
                self.driver.find_element(By.XPATH,f"//div[contains(@x-placement,'start')]//span[text()='{data['filter'][filter_len]['operator']}']").click()
            # 点击并添加value
            if "NULL" not in filter_operator and "EMPTY" not in filter_operator:
                self.driver.find_element(By.XPATH, f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]").click()
                for value in data['filter'][filter_len]['value']:
                    if value == "":
                         self._select_random()
                    elif value == "text":
                        self.driver.find_element(By.XPATH,f"((//div[@class='report-edit-filter-content'])[{field_len}]//div[@class='el-col el-col-8'])[{value_len}]//input").send_keys("123456")
                    else:
                        self.is_allow_element_click(element=f"//span[text()='{value}']")
                        self.driver.find_element(By.XPATH,f"//div[contains(@x-placement,'start')]//span[text()='{value}']").click()
            field_len += 1
            self.filter_operations.append(filter_operator)

    def is_allow_element_click(self,element):
        scrollable_div = self.driver.find_element(By.XPATH,element)
        self.driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)

    def confirm_creation(self,data):
        self.driver.find_element(By.XPATH, dashboard_chart_save_OK_button_posXpath).click()
        if self.model == "2":
            if data["subtype"] == "name_error":
                error_text = self.driver.find_element(By.XPATH,dashboard_chart_name_error_text_posYpath).text
                assert self.driver.find_element(By.XPATH,dashboard_chart_name_error_text_posYpath).text == "Please enter"
            elif data["subtype"] == "metric_error":
                error_text = self.driver.find_element(By.XPATH,dashboard_chart_different_metric_error_text_posYpath).text
                assert error_text == "The units of the composite fields are different and cannot be selected at the same time" or\
                       error_text == "The label cannot be empty or the same"
            elif data["subtype"] == "dimensions_error":
                error_text = self.driver.find_element(By.XPATH,dashboard_chart_dimensions_error_text_posXpath).text
                assert error_text == "The dimensions cannot be empty and can only have one dimension"
        else:
            self.driver.find_element(By.XPATH,mainPage_save_dashboard_button_posXpath).click()
            assert self.driver.find_element(By.XPATH,"//div[@class='el-card box-card is-never-shadow']//div[@class='vbox-title']/span").text == "Create_" + data["data_source"]

    def modify(self,data,visualization_type,metric_type,multiple_dimension):
        self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_up_button_posXpath).click()
        self.driver.find_element(By.XPATH,dashboard_chart_up_edit_button_posXpath).click()
        self.delete_metric(visualization_type)
        if metric_type == "single":
            metric_type = "multiple"
        else: metric_type = "single"
        self.add_metric(data,visualization_type,metric_type)
        self.delete_dimensions()
        if visualization_type == "Table":
            if multiple_dimension == "true":
                multiple_dimension = "false"
            else: multiple_dimension = "true"
        self.add_dimensions(data,visualization_type,multiple_dimension)
        if visualization_type != "Line" and visualization_type != "Area":
            self.add_order_by(data)
        self.select_random()
        self.add_filter(data)
        self.confirm_creation(data)
        self.modify_verify(data,visualization_type)

    def modify_verify(self,data,visualization_type):
        self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_up_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_up_edit_button_posXpath).click()
        # if visualization_type != "Line" and visualization_type != "Area":
        if visualization_type == "Bar" or visualization_type == "Pie":
            assert self.driver.find_element(By.XPATH,"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[1]").get_attribute('title') == data["order_by"]
        elif visualization_type == "Table":
            assert self.driver.find_element(By.XPATH,"(//div[@class='Metrics']//div[@class='el-input el-input--small']/input)[2]").get_attribute('title') == data["order_by"]
        assert len(self.driver.find_elements(By.XPATH,"//div[@class='Filters']//span[normalize-space(text())='or']")) == len(data["filter"]) \
                and len(self.driver.find_elements(By.XPATH,"//div[@class='Filters']//span[normalize-space(text())='and']")) == 1
        self.confirm_creation(data)


    def delete(self):
        self.driver.find_element(By.XPATH,mainPage_edit_dashboard_button_posXpath).click()
        self.driver.find_element(By.XPATH,mainPage_delete_dashboard_posXpath).click()
        self.driver.find_element(By.XPATH,mainPage_delete_Delete_button_posXpath).click()

    def delete_metric(self,visualization_type):
        if self.model == "1" and visualization_type != "Table":
            pass
        else:
            metric_elements = self.driver.find_elements(By.XPATH,dashboard_delete_metrci_posXpath)
            metric_count = len(metric_elements)
            while metric_count > 1:
                self.driver.find_element(By.XPATH,"("+dashboard_delete_metrci_posXpath+")"+f"[{metric_count}]").click()
                metric_count -= 1
            self.driver.find_element(By.XPATH,dashboard_no_delete_metrci_posXpath)
        for element in self.driver.find_elements(By.XPATH,"//div[@class='Metrics']//i[@class='el-tag__close el-icon-close']"):
            element.click()
        assert self.driver.find_element(By.XPATH, dashboard_chart_different_metric_error_text_posYpath).text == "Please select"


    def delete_dimensions(self):
        dimension_elements = self.driver.find_elements(By.XPATH,dashboard_delete_dimensions_posXpath)
        dimension_count = len(dimension_elements)
        while dimension_count > 0:
            self.is_allow_element_click("(" + dashboard_delete_dimensions_posXpath + ")" + f"[{dimension_count}]")
            self.driver.find_element(By.XPATH,"(" + dashboard_delete_dimensions_posXpath + ")" + f"[{dimension_count}]").click()
            dimension_count -= 1

    def select_random(self):
        filter_elements = self.driver.find_elements(By.XPATH,dashboard_delete_filter_posXpath)
        filter_count = len(filter_elements)
        while filter_count > 0:
            self.is_allow_element_click("(" + dashboard_delete_filter_posXpath + ")" + f"[{filter_count}]")
            self.driver.find_element(By.XPATH,"(" + dashboard_delete_filter_posXpath + ")" + f"[{filter_count}]").click()
            filter_count -= 1

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
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",
                  flush=True)
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

    def modify_type(self,data,metric_type,multiple_dimension):
        visualization_type = data["visualization_type"]
        type = random.choice(visualization_type)
        temp = visualization_type.pop(visualization_type.index(type))
        self.create(data,type,metric_type,multiple_dimension)
        self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_up_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_up_edit_button_posXpath).click()
        #切换visualization_type
        modiy_type = random.choice(visualization_type)
        visualization_type_element = dashboard_chart_visualization_type_posXpath.replace("type", modiy_type)
        self.driver.find_element(By.XPATH, visualization_type_element).click()
        #判断Demensions是否恢复初始状态
        dimensions_elements = self.driver.find_elements(By.XPATH,"//label[text()='Dimensions']/parent::*//div[@class='el-input el-input--small el-input--suffix']")
        if  len(dimensions_elements) != 0:
            raise AssertionError("Demensions未恢复初始状态")
        #切换data source
        self.driver.find_element(By.XPATH,dashboard_chart_save_Cancel_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_up_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_up_edit_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_data_source_select_up_posXpath).click()
        self._select_random()
        # 判断Demensions，Metric是否恢复初始状态
        error_text = self.driver.find_element(By.XPATH, dashboard_chart_different_metric_error_text_posYpath).text
        dimensions_elements = self.driver.find_elements(By.XPATH,"//label[text()='Dimensions']/parent::*//div[@class='el-input el-input--small el-input--suffix']")
        if len(dimensions_elements) == 0 and error_text =="Please select":
            pass
        else:
            raise AssertionError("Demensions,Metirc未恢复初始状态")
        self.driver.find_element(By.XPATH, dashboard_chart_save_Cancel_button_posXpath).click()
        self.driver.find_element(By.XPATH, mainPage_save_dashboard_button_posXpath).click()
        self.delete()

    def verify_same_metric(self,data,visualization_type):
        self.driver.find_element(By.XPATH, mainPage_main_dashboard_posXpath).click()
        self.driver.find_element(By.XPATH, mainPage_create_button_dashboard_posXpath).click()
        self.driver.find_element(By.XPATH, mainPage_add_chart_button_posXpath).click()
        self.driver.find_element(By.XPATH, dashboard_chart_name_text_input_posXpath).send_keys("Create_" + data["data_source"])
        # #根据data选择type
        visualization_type_element = dashboard_chart_visualization_type_posXpath.replace("type",visualization_type)
        self.driver.find_element(By.XPATH,visualization_type_element).click()
        # #根据data切换Data Source
        self.driver.find_element(By.XPATH,dashboard_chart_data_source_select_up_posXpath).click()
        self.is_allow_element_click(element=f"//span[text()='{data['data_source']}']")  #下滑到元素可见位置
        self.driver.find_element(By.XPATH,f"//span[text()='{data['data_source']}']").click()
        if "Top" in data['data_source']:
            assert  len(self.driver.find_elements(By.XPATH,"//div[@role='radiogroup']//label[@class='el-radio is-disabled']")) == 3
        select_count = 1
        row_count = 1
        for metric_len in range(len(data["metric"]["single_type"])):
            self.driver.find_element(By.XPATH, dashboard_chart_metric_add_button_posXpath).click()
            # 添加field选项
            self.driver.find_element(By.XPATH, f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
            self.driver.find_element(By.XPATH, f"(//div[@class='el-select-dropdown el-popper is-multiple']//span[text()='{data['metric']['single_type'][metric_len]['field']}'])[{row_count}]").click()
            # 添加aggregate
            self.driver.find_element(By.XPATH,f"(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[{select_count}]").click()
            select_count += 2
            self.driver.find_element(By.XPATH,f"//div[@x-placement='bottom-start']//span[text()='{data['metric']['single_type'][metric_len]['aggregate']}']").click()
            row_count += 1
        self.model = "2"
        self.confirm_creation(data)







