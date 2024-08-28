# -*- coding: UTF-8 -*-
import os
from support.common.report import *
from datetime import datetime

class GenerateCSV:
    def generate_csv(parameter, result, exception_result):
        if len(parameter["script_type"]) == 0:
            file_path = parameter["root_path"] + "/report/automation_test_report.csv"
        else:
            file_path = parameter["root_path"] + "/report/{}_automation_test_report.csv".format(parameter["script_type"])
        if os.path.exists(file_path) and os.path.isfile(file_path):  
            if result is not None and result != "" and len(result) != 0:
                report_data = []
                report_data.append(parameter["test_case_name"])
                result_flag = "Fail"
                report_data.append(result_flag)
                temp_result = "UI automation result: " + result["ui_result"] + " API automation result: " + result["api_result"]
                report_data.append(temp_result)
            elif exception_result is not None and exception_result != "" and len(exception_result) != 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Fail"
                report_data.append(result_flag)
                report_data.append(exception_result)
            elif result == "" and len(result) == 0 and exception_result == "" and len(exception_result) == 0:
                report_data = []
                report_data.append("test_case_name")
                result_flag = "Pass"
                report_data.append(result_flag)
                report_data.append("")
            new_report = GenerateReport()
            new_report.insert_data(parameter, report_data)

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")