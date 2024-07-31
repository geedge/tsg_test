# import os
import sys
import time
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from support.ui_utils.profile.page_jump import PageJump
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime 

class CreateStatisticsTemplate:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(self.driver)

    def create(self, data, template_element_position):
        page_jump_element_position = template_element_position["page_jump"]
        create_element_position = template_element_position["create"]
        try:
            # 页面跳转
            page_jump = PageJump(self.driver)
            page_jump.jump_sub_profile_page(page_jump_element_position)
            # 点击create
            self.driver.find_element(By.ID, create_element_position["templateListPage_createButton_posId"]).click()
            # 输入name
            template_name = data["name"]
            self.driver.find_element(By.ID, create_element_position["templatePage_inputName_posId"]).send_keys(
                template_name)
            self.data = data
            # 循环操作每个chart
            charts = data["charts"]  # charts数据列表
            operation_type = "create"
            no_modify = ""
            data_index = 0
            for i in range(len(charts)):
                chart_id = "{}".format(i + 1)  # 用于图表排序定位使用
                # 点击chart add添加按钮
                if operation_type == "create":  # 创建时点击添加图表，修改时不点击添加图表
                    self.driver.find_element(By.XPATH,
                                             create_element_position["templates_button_chartAdd_posXpath"]).click()
                else:  # 修改数据，先点击修改按钮  "Edit"编辑修改
                    statisticsTemplates_button_chartEdit_posXpath_1 = create_element_position[
                        "templates_button_chartEdit_posXpath"].format(
                        replaceChart=chart_id)
                    self.driver.find_element(By.XPATH, statisticsTemplates_button_chartEdit_posXpath_1).click()
                time.sleep(2)
                # 页面滚动到最底部
                # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # 内嵌页面滚动条向下滚动到最底部
                #time.sleep(2)
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template5,scroll")
                div_paper_grid = self.driver.find_element(By.XPATH,
                                                          create_element_position["templates_div_paperGrid_posXpath"])
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", div_paper_grid)
                # Visualization Type 操作
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template6,Visualization Type")
                self._operate_radio(charts[i], data_index=data_index, no_modify=no_modify,
                                    data_key="visualization_type",
                                    ep_radio=create_element_position["templates_radio_visualizationType_posXpath"],
                                    chart_id=chart_id)
                # metrics 操作
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template7,metrics")
                self._operate_metrics_or_dimensions_dropdown(charts[i], data_index=data_index, no_modify=no_modify,
                                                             data_key="metrics", chart_id=chart_id)
                visualization_type_temp = charts[i]["visualization_type"].split("->")[data_index].strip().lower()
                metrics_no_dimension_temp = {"session_identifier_sketch", "client_ip_sketch", "server_ip_sketch'"}
                first_metric_temp = charts[i]["metrics"][0].split(":")[0]
                # if first_metric_temp not in{"","不修改","刪除"}:#修改数据待补充处理方式
                if visualization_type_temp == "table" or visualization_type_temp == "bar" or visualization_type_temp == "line":  # 只有table\Bar 图的 有order by操作
                    if visualization_type_temp == "line" and ( first_metric_temp in metrics_no_dimension_temp or len(charts[i]["metrics"]) > 1):
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Line No Dimensions")
                    else:
                        # dimensions 操作
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template8,dimensions")
                        self._operate_metrics_or_dimensions_dropdown(charts[i], data_index=data_index, no_modify=no_modify,
                                                             data_key="dimensions", chart_id=chart_id)
                # 如果有Order By，则操作
                if visualization_type_temp == "table" or visualization_type_temp == "bar":  # 只有table\Bar 图的 有order by操作
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template9,Order By")
                    self._operate_order_by(charts[i], data_index=data_index, no_modify=no_modify,
                                           data_key="order_by", chart_id=chart_id)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "No Order By")
                # Row Limit 操作
                visualization_type_temp = charts[i]["visualization_type"].split("->")[data_index].strip().lower()
                if visualization_type_temp == "line" or visualization_type_temp == "table"  or visualization_type_temp == "bar":  # line 图的 row limit 操作方式不一样
                    if visualization_type_temp == "line" and (
                            first_metric_temp in metrics_no_dimension_temp or len(charts[i]["metrics"]) > 1):
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "No Row Limit")
                    else:
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template10,No Row Limit")
                        self._operate_series_limit(charts[i], data_index=data_index, no_modify=no_modify,
                                                   data_key="row_limit",
                                                   element_position=create_element_position[
                                                       "templates_input_other_posXpath"],
                                                   chart_id=chart_id)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "No Row Limit")
                """
                elif charts[i]["visualization_type"].split("->")[
                    data_index].strip().lower() == "table":  # table 图的 row limit 操作
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "table---row limit")
                    self._operate_input(charts[i], data_index=data_index, no_modify=no_modify, data_key="row_limit",
                                        element_position=create_element_position["templates_input_other_posXpath"],
                                        chart_id=chart_id)
                """
                # Thresholds - Minimum incoming size 操作
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template11,No Row Limit")
                self._operate_input(charts[i], data_index=data_index, no_modify=no_modify, data_key="min_in_size",
                                    element_position=create_element_position["templates_input_other_posXpath"],
                                    chart_id=chart_id)
                # Thresholds - Minimum outgoing  size 操作
                self._operate_input(charts[i], data_index=data_index, no_modify=no_modify, data_key="max_out_size",
                                    element_position=create_element_position["templates_input_other_posXpath"],
                                    chart_id=chart_id)
                # 输入chart name
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template12,chart name")
                self._operate_input(charts[i], data_index=data_index, no_modify=no_modify, data_key="chart_name",
                                    element_position=create_element_position["templates_input_other_posXpath"],
                                    chart_id=chart_id)
                # 点击chart的OK保存按钮
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Click the chart OK save button")
                #self.driver.find_element(By.XPATH, create_element_position["templates_button_ChartOK_posXpath"]).click()
                chart_ok_btn = self.driver.find_element(By.XPATH, create_element_position["templates_button_ChartOK_posXpath"])
                self.driver.execute_script("arguments[0].scrollIntoView();", chart_ok_btn)
                self.driver.execute_script("arguments[0].click();", chart_ok_btn)
            # 确认创建，点击Template的OK保存按钮
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template14,Template OK")
            self.driver.find_element(By.CSS_SELECTOR, create_element_position["templates_button_oK_posCss"]).click()

            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template14,Template warningSaveYes")
            #self.driver.find_element(By.CSS_SELECTOR,create_element_position["templates_button_warningSaveYes_posCss"]).click()
            warning_save_yes_btn = self.driver.find_element(By.CSS_SELECTOR,create_element_position["templates_button_warningSaveYes_posCss"])
            self.driver.execute_script("arguments[0].scrollIntoView();", warning_save_yes_btn)
            self.driver.execute_script("arguments[0].click();", warning_save_yes_btn)
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.driver.find_element(By.CSS_SELECTOR,
            #                         create_element_position["templates_button_warningSaveYes_posCss"]).is_enabled())
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template14,Template warningSaveYes after")
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400

    def _operate_radio(self, chart, data_index=0, no_modify="不修改", data_key="", ep_radio="", chart_id=""):
        """
        单选按钮操作
        :param data:
        :param data_index: 0 -1  创建或修改数据索引
        :param no_modify:
        :param data_key:   搜索 visualization_type  和 sampling
        :param ep_radio:   单选按钮定位
        :param chart_id:   图表id
        :return:
        """
        try:
            # 解析输入data数据的数据
            data_value: str = self._get_value_from_data(chart, key=data_key, data_index=data_index)  # 提取数据 Table
            data_value = "_".join(data_value.lower().split())  # Table
            if data_value != no_modify:  # 判断修改时不修改时跳过操作。
                if data_key == "visualization_type":  # visualization_type 元素定位重组
                    replace_type_dict = {'table': 'Table', 'line': 'Line', 'bar': 'Bar', 'histogram': 'Histogram'}
                    repalceLabel = "Visualization Type"
                    ep_attackType_radio = ep_radio.format(replaceChart=chart_id, repalceLabel=repalceLabel,
                                                          replaceType=replace_type_dict[data_value])
                else:  # sampling  元素定位重组
                    replace_sampling_dict = {'comprehensive': 'Comprehensive',
                                             'top-k': 'Top-K'}  # Comprehensive:***, Top-K:***:***
                    repalceLabel = "Sampling"
                    ep_attackType_radio = ep_radio.format(replaceChart=chart_id, repalceLabel=repalceLabel,
                                                          replaceSampling=replace_sampling_dict[
                                                              data_value.split(":")[0]])
                # 点击点选按钮
                self.driver.find_element(By.XPATH, ep_attackType_radio).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", file=sys.stderr)
            return 400

    def _get_value_from_data(self, data, key="", data_index=0):
        """
        从data数据中，根据key提取值
        :param data:
        :param key:
        :param data_index: 0 -1
        :return:
        """
        try:
            switch_value: str = data[key].split("->")[data_index].strip() # 用例数据
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
        return switch_value

    def _operate_order_by(self, chart, data_index=0, no_modify="不修改", data_key="", chart_id=""):
        try:
            data_value: str = self._get_value_from_data(chart, key=data_key, data_index=data_index)  # 提取数据 Table
            if data_value == "":
                return 0
            if data_value != no_modify:  # 判断修改时不修改时跳过操作。
                dropdown_name = "Order By"
                # 组织元素并点击下拉菜单
                ep_order_by_Select = statisticsTemplates_input_other_posXpath.format(replaceChart=chart_id,
                                                                                     repalceLabel=dropdown_name)  # 下拉框定位
                # 将span替换为label,定位不一样
                ep_order_by_Select = ep_order_by_Select.replace("span", "label")
                self.driver.find_element(By.XPATH, ep_order_by_Select).click()
                # 点击下拉列表的item选项
                ep_metricsAndDimensionsDropdownItem = statisticsTemplates_dropdown_posXpath.format(
                    replaceChart=chart_id, repalceLabel=dropdown_name, replaceDropdownIterm=data_value)
                element_dropdown_item = self.driver.find_element(By.XPATH, ep_metricsAndDimensionsDropdownItem)
                # 移动元素到页面，在执行点击
                #self.actions.move_to_element(element_dropdown_item).perform()
                self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                self.driver.execute_script("arguments[0].click();", element_dropdown_item)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400

    def _operate_metrics_or_dimensions_dropdown(self, chart, data_index=0, no_modify="不修改", data_key="",
                                                chart_id=""):
        """
        操作metrics dimensions函数
        :param chart:   每个chart的字典数据
        :param data_index:
        :param no_modify:
        :param data_key: 可取值：metrics  dimensions
        :param chart_id:    chart_id  UI页面中chart id序号
        :return:
        """
        dropdown_item_metrics_dict = {'in_bytes': 'Incoming Bytes', 'out_bytes': 'Outgoing Bytes',
                                      'bytes': 'Bytes', 'new_c2s_flows': 'New Client-to-Server Flows',
                                      'new_s2c_flows': 'New Server-to-Client Flows', 'sessions': 'Sessions',
                                      'new_in_sessions': 'New Incoming Sessions',
                                      'new_out_sessions': 'New Outgoing Sessions',
                                      'new_unestablished_sessions': 'New Unestablished Sessions',
                                      'in_pkts': 'Incoming Packets',
                                      'out_pkts': 'Outgoing Packets',
                                      'pkts': 'Packets',
                                      'syn_pkts': 'SYN Packets',
                                      'c2s_ip_fragments': 'Client-to-Server IP Fragments',
                                      's2c_ip_fragments': 'Server-to-Client IP Fragments',
                                      'ip_fragments': 'IP Fragments',
                                      'session_identifier_sketch': 'Session IDs', 'client_ip_sketch': 'Client IPs',
                                      'server_ip_sketch': 'Server IPs', 'in_latency_ms_sketch': 'Incoming Latency',
                                      'out_latency_ms_sketch': 'Outgoing Latency', 'latency_ms_sketch': 'Latency',
                                      'in_pkt_length_sketch': 'Incoming Packet Length',
                                      'out_pkt_length_sketch': 'Outgoing Packet Length',
                                      'pkt_length_sketch': 'Packet Length'
                                      }
        """
        dropdown_item_dimensions_dict23 = {'time':'Time', 'client_ip': 'Client IP', 'server_ip': 'Server IP', 'server_fqdn': 'Server FQDN', 'server_domain': 'Server Domain',
                                         'application': 'Application', 'websketch_categories': 'WebSketch Categories', 'client_ip_object': 'Client IP Matched Objects',
                                         'server_ip_matched_objects': 'Server IP Matched Objects'}
        """
        dropdown_item_dimensions_dict = {'time': 'Time', 'device_group': 'Device Group', 'client_ip': 'Client IP',
                                         'server_ip': 'Server IP', 'client_asn': 'Client ASN',
                                         'server_asn': 'Server ASN', 'client_country': 'Client Country',
                                         'server_country': 'Server Country',
                                         'server_fqdn': 'Server FQDN', 'server_domain': 'Server Domain',
                                         'application': 'Application',
                                         'fqdn_category': 'WebSketch Categories',
                                         'client_ip_object': 'Client IP Matched Objects',
                                         'server_ip_object': 'Server IP Matched Objects', 'c2s_ttl': 'Client-to-Server TTL',
                                         's2c_ttl': 'Server-to-Client TTL',
                                         'c2s_link_id': 'Client-to-Server Link ID', 's2c_link_id': 'Server-to-Client Link ID',
                                         'client_port': 'Client Port','server_port':'Server Port'}

        if data_key == "metrics":
            metrics_or_dimensions = chart[data_key]  # metrics 数据列表
            dropdown_item_dict = dropdown_item_metrics_dict
            repalceLabel = "Metrics"
        else:  # dimensions
            metrics_or_dimensions = chart[data_key]  # dimensions 数据列表
            dropdown_item_dict = dropdown_item_dimensions_dict
            repalceLabel = "Dimensions"
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], metrics_or_dimensions)
        try:
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 666)
            for j in range(len(metrics_or_dimensions)):  # 循环操作metrics
                # repalceLabel = "Metrics"   # 定位重组参数使用
                dropdown_item = metrics_or_dimensions[j].strip().split("->")[data_index].lower()  # 提取数据
                #dropdown_item = "_".join(dropdown_item.split())  # outgoing_bytes
                drop_item_old = metrics_or_dimensions[j].strip().split("->")[0].lower()  # 创建的数据，修改或删除使用
                #drop_item_old = "_".join(drop_item_old.split())
                if dropdown_item != no_modify:  # 编辑遇到不修改时，不处理
                    if dropdown_item == "":  # 修改数据参数中，creat为空
                        continue
                    elif dropdown_item == "删除":  # 执行删除命令
                        self.dropdown_del(chart_id=chart_id, dropdown_name=repalceLabel, old_value=drop_item_old,
                                          dropdown_item_dict=dropdown_item_dict)
                    else:  # 新增或修改
                        if data_index == -1:  # 修改数据,修改数据情况
                            if drop_item_old == "":  # ->3.4.3.2的的格式数据，表示修改中的新增
                                self.dropdown_add(chart_id=chart_id, dropdown_name=repalceLabel,
                                                  new_value=dropdown_item, dropdown_item_dict=dropdown_item_dict)
                            else:  # 4.3.4.3->4.5.6.8   表示修改原数据
                                self.dropdown_modify(chart_id=chart_id, dropdown_name=repalceLabel,
                                                     old_value=drop_item_old, new_value=dropdown_item,
                                                     dropdown_item_dict=dropdown_item_dict)
                        else:  # 新增数据  4.5.6.3->
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to dropdown_add")
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], dropdown_item)
                            self.dropdown_add(chart_id=chart_id, dropdown_name=repalceLabel, new_value=dropdown_item,
                                              dropdown_item_dict=dropdown_item_dict)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400

    def _operate_input(self, chart, data_index=0, no_modify="不修改", data_key="", element_position="",
                       chart_id=""):
        """
        页面中输入框类型操作
        :param data:
        :param data_index:
        :param no_modify:
        :param data_key: 数据key
        :param element_position: 输入框元素定位
        :return:
        """
        try:
            data_value: str = self._get_value_from_data(chart, key=data_key, data_index=data_index)  # 提取value数据
            if data_value == "":  # 无值时不操作
                return 0
            if data_value != no_modify:  # 编辑时，有不修改则不用执行
                if data_key == "row_limit":
                    if chart["visualization_type"].strip().lower() == "line":  # line图的 row limit 改变了
                        repalceLabel = "Series Limit"
                    else:
                        repalceLabel = "Row Limit"
                elif data_key == "min_in_size":
                    repalceLabel = "Minimum Incoming size"
                elif data_key == "max_out_size":  # Minimum outgoing size
                    repalceLabel = "Minimum Outgoing size"
                else:  # chart name 输入框
                    repalceLabel = "Chart Name"
                if repalceLabel == "Chart Name":
                    data_value = "_".join(data_value.lower().split())
                    if data_value == "default_name":
                        # 点击Default Name
                        element_position_1 = element_position.format(replaceChart=chart_id,
                                                                     repalceLabel=repalceLabel)  # input的定位，接下来向上反找,在向下找
                        element_position_1 = element_position_1.replace("span",
                                                                        "label")  # chart name中的定位，需要将span替换为label
                        #self.driver.find_element(By.XPATH, element_position_1).find_element(By.XPATH,
                        #                                                                    "./parent::*/parent::*//span").click()
                        element_dropdown_item = self.driver.find_element(By.XPATH, element_position_1).find_element(By.XPATH,
                                                                                            "./parent::*/parent::*//span")
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template12,chart name")
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], element_dropdown_item.is_enabled())
                        self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                        #self.actions.move_to_element(element_dropdown_item).perform()
                        self.driver.execute_script("arguments[0].click();", element_dropdown_item)
                        return 0
                    elif data_value == "":  # 输入框为空
                        return 0
                data_value_1 = data_value
                element_position_1 = element_position.format(replaceChart=chart_id, repalceLabel=repalceLabel)
                # 定位元素中span换成label
                element_position_1 = element_position_1.replace("span", "*")
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], element_position_1)
                self.driver.find_element(By.XPATH, element_position_1).clear()
                self.driver.find_element(By.XPATH, element_position_1).send_keys(data_value_1)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400

    def _operate_series_limit(self, chart, data_index=0, no_modify="不修改", data_key="", element_position="",
                              chart_id=""):
        """
        页面中输入框类型操作
        :param data:
        :param data_index:
        :param no_modify:
        :param data_key: 数据key
        :param element_position: 输入框元素定位
        :return:
        """
        try:
            data_value: str = self._get_value_from_data(chart, key=data_key, data_index=data_index)  # 提取value数据
            if data_value == "":  # 无值时不操作
                return 0
            if data_value != no_modify:  # 编辑时，有不修改则不用执行
                if data_key == "row_limit":
                    if chart["visualization_type"].strip().lower() == "line":  # line图的 row limit 改变了
                        repalceLabel = "Series Limit"
                    else:
                        repalceLabel = "Row Limit"
                data_value_1 = data_value
                element_position_1 = element_position.format(replaceChart=chart_id, repalceLabel=repalceLabel)
                # 定位元素中span换成label
                element_position_1 = element_position_1.replace("span", "*")
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "element_position_1"+element_position_1)
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], self.driver.find_element(By.XPATH, element_position_1).is_enabled())
                #self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                #self.driver.execute_script("arguments[0].click();", element_dropdown_item)
                #浏览器模式下定位
                self.driver.find_element(By.XPATH, element_position_1).click()
                #无浏览器模式下定位
                #element_position_1 = self.driver.find_element(By.XPATH, element_position_1)
                #self.driver.execute_script("arguments[0].scrollIntoView();", element_position_1)
                #self.driver.execute_script("arguments[0].click();", element_position_1)
                self.driver.find_element(By.XPATH, element_position_1).send_keys(data_value_1)
                element_dropdown_item = self.driver.find_element(By.XPATH, element_position_1). \
                    find_element(By.XPATH,
                                 f"./ancestor::*[contains(@class, 'el-form-item el-form-item--small')]//*[contains(@class, 'el-select-dropdown__list')]/li/span[normalize-space(text())='{data_value_1}']")
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "template10,No Row Limit")
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], element_dropdown_item.is_enabled())
                #self.actions.move_to_element(element_dropdown_item).perform()
                self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                self.driver.execute_script("arguments[0].click();", element_dropdown_item)
                # self.driver.find_element(By.XPATH, element_position_1).send_keys(data_value_1)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400

    def dropdown_add(self, chart_id="", dropdown_name="", new_value="", dropdown_item_dict={}):
        """
        下拉列表添加内容选项操作
        :param chart_id:   新增数据chart id
        :param dropdown_name:下拉列表框名称类型，例如Metrics
        :param new_value:   下拉列表中新增的值item
        :param dropdown_item_dict:  下拉列表新增值item映射的字典
        :return:
        """
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 5555)
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], dropdown_name)
        dropdown_aggragate_dict = {"sum": "SUM", "rate": "RATE", "bitrate": "BITRATE",
                                   "percentiles_hdr": "PERCENTILES_HDR", "median_hdr": "MEDIAN_HDR",
                                   "p95_percentile_hdr": "P95_PERCENTILE_HDR",
                                   "p99_percentile_hdr": "P99_PERCENTILE_HDR",
                                   "approx_count_distinct_hlld": "APPROX_COUNT_DISTINCT_HLLD"}

        try:
            #time.sleep(3)
            # ep_metricsAndDimensionsAdd = statisticsTemplates_button_metricsAndDimensionsAdd_posXpath.format(replaceChart=chart_id, repalceLabel=dropdown_name)   #添加按钮定位
            ep_metricsAndDimensionsSelects = statisticsTemplates_input_metricsAndDimensionsSelect_posXpath.format(
                replaceChart=chart_id, repalceLabel=dropdown_name)  # 下拉框定位，可能存在多个
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 6666)
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], ep_metricsAndDimensionsSelects)
            element_metricsAndDimensionsSelects = self.driver.find_elements(By.XPATH,
                                                                            ep_metricsAndDimensionsSelects)  # 下拉框元素列表
            element_metricsAndDimensionsAdd = element_metricsAndDimensionsSelects[-1].find_element(By.XPATH,
                                                                                                   ".//i")  # 下拉框元素列表中最后一个为add添加按钮
            # 点击添加按钮
            # 下拉列表
            time.sleep(1)
            is_click_add = "yes_click"
            for dropdownSelect_item in element_metricsAndDimensionsSelects[1:-1]:  # 下拉框元素列表中第二个到倒数第二个为操作数据
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 7777)
                dropdownSelect_item_input_value = dropdownSelect_item.find_element(By.XPATH,
                                                                                   "./div[1]//input").get_attribute(
                    "value")
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], dropdownSelect_item_input_value)
                if dropdownSelect_item_input_value == "":  # 有空数据时，就跳过点击添加按钮
                    is_click_add = "no_click"
                    break
            if is_click_add == "yes_click":
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 8888)
                element_metricsAndDimensionsAdd.click()  # 全部都有数据时，需要点击添加
            # 点击空的下拉列表框选项
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 9999)
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], ep_metricsAndDimensionsSelects)
            element_metricsAndDimensionsSelects2 = self.driver.find_elements(By.XPATH,
                                                                             ep_metricsAndDimensionsSelects)  # 下拉框元素列表  重新获取一次
            if dropdown_name == "Metrics":
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1010)
                create_class = element_metricsAndDimensionsSelects2[-1].find_element(By.XPATH, ".//i").get_attribute(
                    "class")
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], create_class)
                if ("icon-Create1" not in create_class):  # 没有添加的元素时
                    tmp_element_metricsAndDimensionsSelects2 = element_metricsAndDimensionsSelects2[1:]
                else:  # 有添加的元素时
                    tmp_element_metricsAndDimensionsSelects2 = element_metricsAndDimensionsSelects2[1:-1]
            else:
                tmp_element_metricsAndDimensionsSelects2 = element_metricsAndDimensionsSelects2[1:-1]
            for dropdownSelect_item in tmp_element_metricsAndDimensionsSelects2:
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1111)
                dropdownSelect_item_list = dropdownSelect_item.find_elements(By.XPATH, "./div")  # 所有列的集合
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], dropdownSelect_item_list)
                dropdownSelect_item_input_value = dropdownSelect_item.find_element(By.XPATH,
                                                                                   "./div[1]//input").get_attribute(
                    "value")
                if dropdownSelect_item_input_value == "":  # 在空的下拉菜单中添加数据
                    # 遍历添加每一个列的下拉列表数据
                    col_n = 0
                    if dropdown_name == "Metrics":
                        # 因为metrics需要操作三列
                        tmp_dropdownSelect_item_list = dropdownSelect_item_list[0:3]
                    else:
                        # dimension需要操作一列
                        tmp_dropdownSelect_item_list = dropdownSelect_item_list[0:1]
                    for col_dropdownSelect in tmp_dropdownSelect_item_list:  # 需要操作的每一个行中列的数量
                        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1212)
                        col_dropdownSelect.find_element(By.XPATH, ".//input").click()

                        # 异常断言判断 "reverse_case": "....",   # 主要校验不同chart类型，可以选择不同的metrics   # 只是断言使用，无实际页面操作
                        if "reverse_case" in self.data["charts"][0].keys():
                            reverse_case_case = self.data["charts"][0]["reverse_case"].strip().lower()
                            if reverse_case_case == "table_chart_check_metrics" or reverse_case_case == "bar_chart_check_metrics":  # 校验table or bar chart 可选择 metrics类型
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Invalid Metric Verification Test Cases for Table and Bar Charts")
                                info_execpt = "is-disabled"
                                is_disabled_list = ["Session IDs", "Client IPs", "Server IPs", "Incoming Latency",
                                                    "Outgoing Latency", "Latency"]
                                el_drop_item_class_xpath = "//*[contains(@class, 'Metric')]//div[contains(@class, 'multipleSelect')]//div[@class='el-scrollbar']//li[contains(@class, 'el-select-dropdown__item')]"
                                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1313)
                                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], el_drop_item_class_xpath)
                                drop_items = self.driver.find_elements(By.XPATH, el_drop_item_class_xpath)
                                for i in drop_items:
                                    item_name = i.find_element(By.XPATH, ".//span").text.strip()
                                    item_class = i.get_attribute("class")
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], item_name, "==>>", item_class)
                                    #if item_name in is_disabled_list:
                                        #pytest_check.is_in(info_execpt, item_class,
                                        #                   msg="所在行数{}".format(inspect.currentframe().f_lineno))
                            elif reverse_case_case == "histogram_chart_check_metrics":  # 校验histogram chart 可选择 metrics类型
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Invalid Metric Verification Test Cases for Histogram Charts")
                                info_execpt = "is-disabled"
                                is_disabled_list = ["Incoming Bytes", "Outgoing Bytes ", "Bytes",
                                                    'Outgoing Packets','Incoming Packets','Packets',"New C2S Flows",
                                                    "New S2C Flows",
                                                    "New Incoming Sessions", "New Outgoing Sessions", "Sessions",
                                                    "New Unestablished Sessions",
                                                    "SYN Packets", "Session IDs", "Client IPs", "Server IPs"]
                                el_drop_item_class_xpath = "//*[contains(@class, 'Metric')]//div[contains(@class, 'multipleSelect')]//div[@class='el-scrollbar']//li[contains(@class, 'el-select-dropdown__item')]"
                                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1414)
                                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], el_drop_item_class_xpath)
                                drop_items = self.driver.find_elements(By.XPATH, el_drop_item_class_xpath)
                                for i in drop_items:
                                    item_name = i.find_element(By.XPATH, ".//span").text.strip()
                                    item_class = i.get_attribute("class")
                                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], item_name, "==>>", item_class)
                                    #if item_name in is_disabled_list:
                                    #    pytest_check.is_in(info_execpt, item_class,
                                    #                       msg="所在行数{}".format(inspect.currentframe().f_lineno))

                        # 从下拉列表中选择Item选项值
                        if ":" in new_value:  # metrics数据，需要操作三列
                            new_value_list = new_value.split(":")
                            col_name = new_value_list[col_n]
                            if col_n == 0:  # 第一列数据值
                                replaceDropdownIterm = dropdown_item_dict[col_name]
                            elif col_n == 1:  # 第二列数据值
                                replaceDropdownIterm = dropdown_aggragate_dict[col_name]
                            else:
                                replaceDropdownIterm = col_name
                            if col_n == 0 or col_n == 1:
                                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1515)
                                element_dropdown_item = col_dropdownSelect.find_element(By.XPATH,
                                                                                        f".//div[contains(@class,'el-select-dropdown__wrap')]//span[normalize-space(text())='{replaceDropdownIterm}']")

                                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], element_dropdown_item)
                                # 移动元素到页面，在执行点击
                                #self.actions.move_to_element(element_dropdown_item).perform()
                                self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                                self.driver.execute_script("arguments[0].click();", element_dropdown_item)
                            elif col_n == 2:
                                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1616)
                                # 输入label值
                                col_dropdownSelect.find_element(By.XPATH, ".//input").clear()
                                col_dropdownSelect.find_element(By.XPATH, ".//input").send_keys(replaceDropdownIterm)
                            col_n += 1
                        else:  # demesions数据操作
                            col_name = new_value
                            replaceDropdownIterm = dropdown_item_dict[col_name]
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], replaceDropdownIterm)
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1717)
                            #time.sleep(3)
                            elements = col_dropdownSelect.find_elements(By.XPATH,f".//div[contains(@class,'el-select-dropdown__wrap')]//span[normalize-space(text())='{replaceDropdownIterm}']")
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], len(elements))
                            element_dropdown_item = col_dropdownSelect.find_element(By.XPATH,f".//div[contains(@class,'el-select-dropdown__wrap')]//span[normalize-space(text())='{replaceDropdownIterm}']")
                            #element_dropdown_item = col_dropdownSelect.find_element(By.XPATH, f".//div[contains(@class,'el-select-dropdown__wrap')]//span[normalize-space(text())='{replaceDropdownIterm}']")
                            #col_dropdownSelect.execute_script("window.scrollTo(0," + str(element_dropdown_item.location["y"]) + ")")
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], element_dropdown_item)
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], element_dropdown_item.is_enabled())
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 1818)
                            self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
                            self.driver.execute_script("arguments[0].click();", element_dropdown_item)
                            #element_dropdown_item.click()
                            # 移动元素到页面，在执行点击
                            #self.actions.move_to_element(element_dropdown_item).perform()
                            #self.driver.execute_script("arguments[0].click();", element_dropdown_item)
                    break
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400

    def dropdown_del(self, chart_id="", dropdown_name="", old_value="", dropdown_item_dict={}):
        """
        删除下拉列表选项
        :param chart_id:
        :param dropdown_name:
        :param old_value:   删除的选项值
        :param dropdown_item_dict:  同add的方法
        :return:
        """
        try:
            old_value_list = old_value.split(":")
            ui_old_value = dropdown_item_dict[old_value_list[0]]
            ep_metricsAndDimensionsSelects = statisticsTemplates_input_metricsAndDimensionsSelect_posXpath.format(
                replaceChart=chart_id, repalceLabel=dropdown_name)  # 下拉框定位，可能存在多个
            element_metricsAndDimensionsSelects = self.driver.find_elements(By.XPATH,
                                                                            ep_metricsAndDimensionsSelects)  # 下拉框元素列表
            # 需要选择，需要删除的元素
            for dropdownSelect_item in element_metricsAndDimensionsSelects[1:-1]:  # 类别中第一个和最后一个元素不是选择框元素，这个只遍历选择框元素
                dropdownSelect_item_input_value = dropdownSelect_item.find_element(By.XPATH,
                                                                                   "./div[1]//input").get_attribute(
                    "value")
                if dropdownSelect_item_input_value == ui_old_value:  # 删除该元素
                    if ":" in old_value:  # metrics的删除点击
                        dropdownSelect_item.find_element(By.XPATH, "./div[4]//i").click()  # 点击删除按钮
                    else:  # dimensions的删除点击操作
                        dropdownSelect_item.find_element(By.XPATH, "./div[3]//i").click()  # 点击删除按钮
                    break
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400

    def dropdown_modify(self, chart_id="", dropdown_name="", old_value="", new_value="", dropdown_item_dict={}):
        """
        修改下拉列表选项，更换为新值
        :param chart_id:
        :param dropdown_name:
        :param old_value:   创建的值
        :param new_value:   修改的值
        :param dropdown_item_dict:
        :return:
        """
        dropdown_aggragate_dict = {"sum": "SUM", "rate": "RATE", "bitrate": "BITRATE",
                                   "percentiles_hdr": "PERCENTILES_HDR", "median_hdr": "MEDIAN_HDR",
                                   "p95_percentile_hdr": "P95_PERCENTILE_HDR",
                                   "p99_percentile_hdr": "P99_PERCENTILE_HDR",
                                   "approx_count_distinct_hlld": "APPROX_COUNT_DISTINCT_HLLD"}
        try:
            old_value_list = old_value.split(":")
            new_value_list = new_value.split(":")
            ep_metricsAndDimensionsSelects = statisticsTemplates_input_metricsAndDimensionsSelect_posXpath.format(
                replaceChart=chart_id, repalceLabel=dropdown_name)  # 下拉框定位，可能存在多个
            element_metricsAndDimensionsSelects = self.driver.find_elements(By.XPATH,
                                                                            ep_metricsAndDimensionsSelects)  # 下拉框元素列表
            # 选择需要修改的下拉列表，并重新选择新值
            for dropdownSelect_item in element_metricsAndDimensionsSelects[1:-1]:  # 类别中第一个和最后一个元素不是选择框元素，这个只遍历选择框元素
                dropdownSelect_item_input_value = dropdownSelect_item.find_element(By.XPATH,
                                                                                   "./div[1]//input").get_attribute(
                    "value")
                if dropdownSelect_item_input_value == dropdown_item_dict[old_value_list[0]]:  # 删除该元素
                    dropdownSelect_item.find_element(By.XPATH, ".//div[1]//input").click()
                    break
            # 点击下拉列表的的新item选项
            ep_metricsAndDimensionsDropdownItem = statisticsTemplates_dropdown_posXpath.format(replaceChart=chart_id,
                                                                                               repalceLabel=dropdown_name,
                                                                                               replaceDropdownIterm=
                                                                                               dropdown_item_dict[
                                                                                                   new_value_list[0]])
            element_dropdown_item = self.driver.find_element(By.XPATH, ep_metricsAndDimensionsDropdownItem)
            # 移动元素到页面，在执行点击
            #self.actions.move_to_element(element_dropdown_item).perform()
            self.driver.execute_script("arguments[0].scrollIntoView();", element_dropdown_item)
            self.driver.execute_script("arguments[0].click();", element_dropdown_item)
            # Metrics列数据，还需要修改Aggregate label数据
            if dropdown_name == "Metrics":
                # 操作aggregate数据
                dropdownSelect_item.find_element(By.XPATH, "./div[2]//input").click()  # 点击选择框
                ep_aggregateItem = statisticsTemplates_dropdown_posXpath.format(replaceChart=chart_id,
                                                                                repalceLabel=dropdown_name,
                                                                                replaceDropdownIterm=
                                                                                dropdown_aggragate_dict[
                                                                                    new_value_list[1]])
                self.driver.find_element(By.XPATH, ep_aggregateItem).click()
                # 操作label数据
                dropdownSelect_item.find_element(By.XPATH, "./div[3]//input").clear()  # label输入框数据
                dropdownSelect_item.find_element(By.XPATH, "./div[3]//input").send_keys(new_value_list[2])
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400