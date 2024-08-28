# -*- coding: UTF-8 -*-
import configparser
import os
import glob
import importlib
import subprocess
import platform
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
from support.common.report import *
from support.case_tag import *
from datetime import datetime

app = Flask(__name__)

@app.route('/v1/security_ui', methods=["POST"])
@app.route('/v1/intercept_ui', methods=["POST"])
@app.route('/v1/manipulation_ui', methods=["POST"])
@app.route('/v1/monitor_ui', methods=["POST"])
@app.route('/v1/statistics_ui', methods=["POST"])
@app.route('/v1/service_chaining_ui', methods=["POST"])
@app.route('/v1/shaping_ui', methods=["POST"])
@app.route('/v1/security_api', methods=["POST"])
@app.route('/v1/intercept_api', methods=["POST"])
@app.route('/v1/manipulation_api', methods=["POST"])
@app.route('/v1/monitor_api', methods=["POST"])
@app.route('/v1/statistics_api', methods=["POST"])
@app.route('/v1/service_chaining_api', methods=["POST"])
@app.route('/v1/shaping_api', methods=["POST"])
@app.route('/v1/dashboard', methods=["POST"])
@app.route('/v1/object', methods=["POST"])
@app.route('/v1/case_tag', methods=["POST"])
def receive_parameter():
    try:
        # 从MS或Jmeter等工具的请求体中获取参数
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "==========Receive request from Metersphere.==========", flush=True)
        req_json = request.get_json()
        run_status = req_json.get("run_status")
        
        if run_status == 1:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to build test parameter.", flush=True)
            module_name = req_json.get("module_name")
            sub_module_name = req_json.get("sub_module_name")
            test_case_name = req_json.get("test_case_name")
            tag = req_json.get("tag")
        
            parameter = {
                "username": "",
                "password": "",
                "api_server": "",
                "test_pc_ip": "",
                "test_subcriber_id": "",
                "test_imsi": "",
                "test_phone_number": "",
                "test_imei": "",
                "test_apn": "",
                "script_type": "",
                "root_path": "",
                "path": "",
                "module_name": "",
                "sub_module_name": "",
                "test_case_name": "",
                "app_name": "",
                "app_full_name": "",
                "env": "",
                "vsys_id": 0,
                "is_log": 0
            }
            
            parse = configparser.ConfigParser()
            parse_dir = os.path.join("configuration_file.ini")
            parse.read(parse_dir, encoding="utf-8")
            
            parameter["username"] = parse.get("account", "username")
            
            parameter["password"] = parse.get("account", "password")
            
            parameter["api_server"] = parse.get("tsg_url", "login_url")
            
            project_path = parse.get("root_path", "path")
            parameter["root_path"] = project_path
            
            if tag == "api":
                parameter["test_pc_ip"] = parse.get("test_pc", "ip_for_api")
                parameter['test_subcriber_id'] = parse.get("test_pc", "subcriber_id_for_api")
                parameter["path"] = f"{project_path}/tests/api"
                parameter["env"] = "tsgx"
                parameter["vsys_id"] = parse.get("vsys", "id_for_api")
                parameter["is_log"] = parse.get("is_log", "api")
            elif tag == "ui" or tag == "":
                parameter["test_pc_ip"] = parse.get("test_pc", "ip_for_ui_with_traffic")
                parameter['test_subcriber_id'] = parse.get("test_pc", "subcriber_id_for_ui_with_traffic")
                parameter['test_imsi'] = parse.get("test_pc", "imsi_for_ui_with_traffic")
                parameter['test_phone_number'] = parse.get("test_pc", "phone_number_for_ui_with_traffic")
                parameter["path"] = f"{project_path}/tests/ui"
                parameter["vsys_id"] = parse.get("vsys", "id_for_ui")
                parameter["is_log"] = parse.get("is_log", "ui")
            elif tag == "general_ui":
                parameter["path"] = f"{project_path}/tests/ui"
                parameter["sub_module_name"] = sub_module_name
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added.", flush=True)
            elif tag == "app":
                parameter["path"] = f"{project_path}/tests/app"
                parameter["app_name"] = req_json.get("app_name")
                parameter["app_full_name"] = req_json.get("app_full_name")
            
            parameter["script_type"] = tag
            
            parameter["module_name"] = module_name
            
            temp_folder_path = parameter["path"] + "/" + module_name
            
            # 考虑到MS的报告无法快速过滤结果，会生成csv格式的report
            new_report = GenerateReport()
            new_report.generate_report(tag, project_path)
            
            # folder_list = os.listdir(temp_folder_path)
            # sys.stdout.write("The test folder contain: {}\n".format(folder_list))
            # 匹配测试用例
            path = f"{temp_folder_path}/*.py"
            files = glob.glob(path, recursive=True)
            response_result = {}
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to match test case.", flush=True)
            for file in files:
                os_name = platform.system()
                if os_name == "Linux":
                    file_name = file.split("/")[-1]
                elif os_name == "Windows":
                    file_name = file.split("\\")[-1]
                if file_name == test_case_name + ".py":
                    parameter["test_case_name"] = test_case_name
                    new_path = "tests." + tag + "." + module_name + "." + test_case_name
                    module = importlib.import_module(new_path)
                    result = module.run(parameter)
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Test caes response is: {}".format(result), flush=True)
                    # module.run()返回的结果是failure reason，如果是空，则表示测试通过。
                    if len(result) == 0:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is passed.", flush=True)
                        response_result["code"] = 200
                        if tag == "ui":
                            response_result["ui_automation_result"] = "pass"
                        elif tag == "api":
                            response_result["api_automation_result"] = "pass"
                        elif tag == "":
                            response_result["ui_automation_result"] = "pass"
                            response_result["api_automation_result"] = "pass"
                        response_result["data"] = None
                        response_result["success"] = True
                    elif len(result) != 0:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "The test case is failed. The failure reason is: ", result, flush=True)
                        response_result["code"] = 416
                        if tag == "ui":
                            response_result["ui_automation_result"] = result
                        elif tag == "api":
                            response_result["api_automation_result"] = result
                        elif tag == "":
                            response_result["ui_automation_result"] = result["ui_result"]
                            response_result["api_automation_result"] = result["api_result"]
                        response_result["result"] = result
                        response_result["data"] = None
                        response_result["success"] = False
                    break
            
            value = response_result.get("code", None)
            if value is None or value == '':
                response_result["code"] = 417
            response = jsonify(response_result)
            response.status_code = response_result["code"]
        elif run_status == 2:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Count cases number as required.", flush=True)
            policy_rule = req_json.get("policy")
            protocol = req_json.get("app")
            action = req_json.get("action")
            sub_action = req_json.get("sub_action")
            script_type = req_json.get("script_type")
            case_tag = CaseTag()
            result_list = case_tag.case_statistic_info(policy_rule, protocol, action, sub_action, script_type)
            response_result = {}
            if len(result_list) != 0:
                response_result["code"] = 200
                response_result["success"] = True
                for i in range(len(result_list)):
                    temp = result_list[i]
                    temp_key = temp.split(": ")[0]
                    temp_value = temp.split(": ")[1]
                    response_result[temp_key] = temp_value
                response = jsonify(response_result)
                response.status_code = response_result["code"]
        else:
            response_result = {}
            response_result["code"] = 418
            response_result["result"] = "The run status code is False, do not run test case."
            response_result["data"] = None
            response_result["success"] = False    
            response = jsonify(response_result)
            response.status_code = response_result["code"]
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Response is: {}".format(response), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "==========Send the result to Metersphere.==========", flush=True)
        return response
    except subprocess.CalledProcessError as e:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to execute the command. The return code: {}".format(e.returncode), flush=True)
        response_result = {}
        response_result["code"] = 419
        response_result["result"] = "Fail to parse or build parameter."
        response_result["data"] = None
        response_result["success"] = False
        response = jsonify(response_result)
        response.status_code = response_result["code"]
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Response is: {}".format(response), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "==========Send the result to Metersphere.==========", flush=True)
        return response

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8800)