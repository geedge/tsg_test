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
def receive_parameter():
    try:
        # 从MS或Jmeter等工具的请求体中获取参数
        sys.stdout.write("Begin to receive request.\n")
        req_json = request.get_json()
        run_status = req_json.get("run_status")
        module_name = req_json.get("module_name")
        test_case_name = req_json.get("test_case_name")
        tag = req_json.get("tag")
        
        if run_status == 1:
            sys.stdout.write("Begin to build test parameter.\n")
            parameter = {
                "username": "",
                "password": "",
                "api_server": "",
                "test_pc_ip": "",
                "script_type": "",
                "root_path": "",
                "path": "",
                "module_name": "",
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
            
            parameter["test_pc_ip"] = parse.get("test_pc", "ip")
            
            project_path = parse.get("root_path", "path")
            
            if tag == "api":
                parameter["path"] = f"{project_path}/tests/api"
                parameter["env"] = "tsgx"
                parameter["vsys_id"] = 6
                parameter["is_log"] = 0
            elif tag == "ui":
                parameter["path"] = f"{project_path}/tests/ui"
                parameter["vsys_id"] = 6
                parameter["is_log"] = 1
            elif tag == "general_ui":
                print("to be added.")
            elif tag == "app":
                parameter["path"] = f"{project_path}/tests/app"
                parameter["app_name"] = req_json.get("app_name")
                parameter["app_full_name"] = req_json.get("app_full_name")
            
            parameter["script_type"] = tag
            
            parameter["module_name"] = module_name
            
            temp_folder_path = parameter["path"] + "/" + module_name
            
            folder_list = os.listdir(temp_folder_path)
            sys.stdout.write("The test folder contain: {}\n".format(folder_list))
            # 匹配测试用例
            path = f"{temp_folder_path}/*.py"
            files = glob.glob(path, recursive=True)
            response_result = {}
            sys.stdout.write("Begin to match test case.\n")
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
                    # module.run()返回的结果是failure reason，如果是空，则表示测试通过。
                    if len(result) == 0:
                        response_result["code"] = 200
                        response_result["msg"] = "Pass"
                        response_result["data"] = None
                        response_result["success"] = True
                    elif len(result) != 0:
                        response_result["code"] = 417
                        response_result["msg"] = result
                        response_result["data"] = None
                        response_result["success"] = False
                    break
        
            response = jsonify(response_result)
            response.status_code = response_result["code"]
        else:
            response_result = {}
            response_result["code"] = 418
            response_result["msg"] = "The run status code is False, do not run test case."
            response_result["data"] = None
            response_result["success"] = False    
            response = jsonify(response_result)
            response.status_code = response_result["code"]
        
        sys.stdout.write("Response is: {}\n".format(response))
        return response
    except subprocess.CalledProcessError as e:
        sys.stderr.write("Fail to execute the command. The return code: {}\n".format(e.returncode))
        response_result = {}
        response_result["code"] = 419
        response_result["msg"] = "Fail to parse or build parameter."
        response_result["data"] = None
        response_result["success"] = False
        response = jsonify(response_result)
        response.status_code = response_result["code"]
        sys.stdout.write("Response is: {}\n".format(response))
        return response

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8800)