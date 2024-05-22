# -*- coding: UTF-8 -*-
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

@app.route('/v1/tsg', methods=["POST"])
def receive_parameter():
    try:
        # 从MS或Jmeter等工具的请求体中获取参数
        req_json = request.get_json()
        run_status = req_json.get("run_status")
        module_name = req_json.get("module_name")
        test_case_name = req_json.get("test_case_name")
        tag = req_json.get("tag")
        if run_status == 1:
            sys.stdout.write("Begin to build test parameter.\n")
            parameter = {
                "username": "zhaokun",
                "password": "zhaokun1",
                "api_server": "http://192.168.44.72",
                "script_type": "",
                "root_path": "",
                "path": "",
                "module_name": "",
                "test_case_name": "",
                "app_name": "",
                "app_full_name": ""
            }
            os_name = platform.system()
            if os_name == "Linux":
                # project_path = "/opt/tsg_test"
                project_path = "/app"
            elif os_name == "Windows":
                project_path = "D:/Document/Project-TSG/Code/git/tsg_test"
            parameter["root_path"] = project_path
            if tag == "api":
                parameter["path"] = f"{project_path}/tests/api"
            elif tag == "ui":
                parameter["path"] = f"{project_path}/tests/ui"
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
            for file in files:
                sys.stdout.write("Begin to match test case.")
                if os_name == "Linux":
                    file_name = file.split("/")[-1]
                elif os_name == "Windows":
                    file_name = file.split("\\")[-1]
                if file_name == test_case_name + ".py":
                    parameter["test_case_name"] = test_case_name
                    new_path = "tests." + tag + "." + module_name + "." + test_case_name
                    module = importlib.import_module(new_path)
                    result = module.run(parameter)
                    response_result = {}
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
        return response
    except subprocess.CalledProcessError as e:
        sys.stderr.write("Fail to execute the command. The return code: {}\n".format(e.returncode))
        response_result = {}
        response_result["code"] = 418
        response_result["msg"] = ""
        response_result["data"] = None
        response_result["success"] = False
        response = jsonify(response_result)
        response.status_code = response_result["code"]
        return response

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8800)