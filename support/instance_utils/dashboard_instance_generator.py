import os
import sys
import random

from support.api_utils.log_in import LogIn
from support.general_ui_utils.dashboard.create_dashboard import CreateDashboard
from support.general_ui_utils.dashboard.edit_dashboard import EditDashboard
from support.general_ui_utils.dashboard.delete_dashboard import DeleteDashboard
from support.api_utils.delete_policy import DeletePolicy
import support.ui_utils.env
from datetime import datetime

class DashbboardInstanceGenerator:


    def __init__(self, test_data, parameter):
        self.test_data = test_data
        self.parameter = parameter

    def run(self):
        ui_result = self._run(self.test_data, self.parameter)
        return ui_result

    def _run(self, test_data, parameter):
        ui_result, api_result = "", ""
        result = {
            "ui_result": "",
            "api_result": ""
        }

        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        test_data["token"] = token
        self.test_data["token"] = token

        need_initialization = False
        if len(parameter["script_type"]) == 0:
            need_initialization = True

        if parameter["script_type"] == "ui" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run ui test case", flush=True)

                parameter["script_type"] = "ui"

                # 环境初始化
                support.ui_utils.env.initiate_selenium_request()
                driver = support.ui_utils.env.my_driver()
                support.ui_utils.env.setup()

                # name_list汇总
                self.ui_name_list =  [
                    {
                        "name": "New Dashboard",
                        "type": "dashboard",
                    }
                ]

                select_metric_type = ["single", "multiple"]
                multiple_dimension = [True, False]
                if test_data["sub_type"] == "error_metric":
                    metric_type = "multiple"
                    multiple_dimension = False
                    visualization_type = test_data["visualization_type"]
                elif test_data["sub_type"] == "error_dimensions":
                    metric_type = "single"
                    multiple_dimension = True
                    visualization_type = test_data["visualization_type"]
                elif test_data["sub_type"] == "error_name":
                    metric_type = random.choice(select_metric_type)
                    multiple_dimension = False
                    visualization_type = test_data["visualization_type"]
                else:
                    # 随机metric与dimension格式
                    visualization_type = test_data["visualization_type"]
                    metric_type = random.choice(select_metric_type)
                    if test_data["visualization_type"] == "Table":
                        multiple_dimension = random.choice(multiple_dimension)
                    else:
                        multiple_dimension = False

                # 创建Dashboard-Chart
                create_dashboard = CreateDashboard(driver)
                if test_data["sub_type"] == "error_metric" or test_data["sub_type"] == "error_dimensions" or test_data["sub_type"] == "error_name":
                    create_code = create_dashboard.create(test_data, visualization_type, metric_type, multiple_dimension)
                    if create_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create chart successfully.", flush=True)
                    else:
                        ui_result = "Fail to create chart"
                    result["ui_result"] = ui_result
                    return result
                elif test_data["sub_type"] == "empty_chart":
                    create_code, verify_alter = create_dashboard.empty_chart()
                    if create_code == 200 and verify_alter == "INVALID REQUEST:Dataview cannot be empty.":
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Empty chart save hint right", flush=True)
                    else:
                        ui_result = "Fail to create chart"
                    result["ui_result"] = ui_result
                    return result
                elif test_data["sub_type"] == "limit_twenty_chart":
                    create_code = create_dashboard.limit_chart(test_data, visualization_type, "single", "false")
                    if create_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Out of range 20 chart save hint right", flush=True)
                    else:
                        ui_result = "Fail to create chart"
                    result["ui_result"] = ui_result
                    return result
                else:
                    create_code = create_dashboard.create(test_data, visualization_type, metric_type, multiple_dimension)
                    if create_code == 200:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create chart successfully.", flush=True)
                    else:
                        ui_result = "Fail to create chart"

                # 新建chart输入数据校验
                create_verify_code = create_dashboard.create_chart_data_verify(test_data, visualization_type, metric_type,
                                                                               multiple_dimension)
                if create_verify_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Create chart data verify successfully.", flush=True)
                else:
                    ui_result = "Fail to chart data verify"

                # 修改metric与dimension格式
                if metric_type == "single":
                    metric_type = "multiple"
                else:
                    metric_type = "single"
                if test_data["visualization_type"] == "Table":
                    if multiple_dimension == True:
                        multiple_dimension = False
                    else:
                        multiple_dimension = True

                # 编辑操作
                edit_dashboard = EditDashboard(driver)
                edit_dashboard_code = edit_dashboard.edit(test_data, visualization_type, metric_type, multiple_dimension)
                if edit_dashboard_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit chart successfully.", flush=True)
                else:
                    ui_result = "Fail to Edit chart"
                # 修改内容数据校验
                edit_verify_code = edit_dashboard.modify_data_verify(test_data, visualization_type)
                if edit_verify_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit chart verify successfully.", flush=True)
                else:
                    ui_result = "Fail to Edit chart verify"

                # 删除dashboard
                delete_dashboard = DeleteDashboard(driver)
                delete_dashboard_code = delete_dashboard.delete()
                if delete_dashboard_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Delete chart successfully.", flush=True)
                else:
                    ui_result = "Fail to Delete chart"
            except Exception as e:
                raise
            finally:
                # 清理环境
                result["ui_result"] = ui_result
                support.ui_utils.env.teardown()

        if parameter["script_type"] == "api" or need_initialization == True:
            try:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Begin to run api test case", flush=True)

                parameter["script_type"] = "api"
                self.api_name_list = []

                "todo api 集成"
            except Exception as e:
                raise
            finally:
                result["api_result"] = api_result
                # 删除配置
                delete = DeletePolicy()
                #delete.delele_policy_by_cfg(token, parameter, cfg_list)

        return result

    def delete_data(self):
        # 删除配置
        delete = DeletePolicy()
        if isinstance(self.ui_name_list, list) and self.ui_name_list != []:
            delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.ui_name_list)
        # if isinstance(self.api_name_list, list) and self.api_name_list != []:
        #     delete.delete_policy_by_name(self.test_data["token"], self.parameter, self.api_name_list)