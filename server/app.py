# -*- coding: UTF-8 -*-
import os
import glob
import importlib
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/tsg', methods=["POST"])
def ReceiveCaseParameter():
    try:
        # 安装python3和相关包
        command = "python installPython3.py"
        # subprocess.check_call(["python2", "installPython3.py"])
        subprocess.check_output(command, shell=True)
        print("The command is executed successfully.")
        
        # 从MS或Jmeter等工具的请求体中获取参数
        req_json = request.get_json()
        run_status = req_json.get("run_status")
        module_name = req_json.get("module_name")
        test_case_name = req_json.get("test_case_name")
        tag = req_json.get("tag")
        if run_status == 1:
            print("Begin to build test parameter.")
            parameter = {
                "username": "zhaokun",
                "password": "zhaokun1",
                "test_pc_ip": "192.168.64.76",
                "api_server": "http://192.168.44.72",
                "is_log": 0,
                "env": "tsgx",
                "vsys_id": 6,
                "root_path": "",
                "path": "",
                "module_name": "",
                "test_case_name": ""
            }
            project_path = "D:/Document/Project-TSG/Code/git/tsg_test"
            parameter["root_path"] = project_path
            if tag == "api":
                parameter["path"] = f"{project_path}/testcase/api"
            elif tag == "ui":
                parameter["path"] = f"{project_path}/testcase/ui"
            parameter["module_name"] = module_name
            temp_folder_path = parameter["path"] + "/" + module_name
            folder_list = os.listdir(temp_folder_path)
            print("The test folder contain: ", folder_list)
            # 匹配测试用例
            path = f"{temp_folder_path}/*.py"
            files = glob.glob(path, recursive=True)
            for file in files:
                print("Begin to match test case.")
                file_name = file.split("\\")[-1]
                if file_name == test_case_name + ".py":
                    parameter["test_case_name"] = test_case_name
                    new_path = "testcase." + tag + "." + module_name + "." + test_case_name
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
        print("Fail to execute the command. The return code: {}".format(e.returncode))
        response_result = {}
        response_result["code"] = 417
        response_result["msg"] = ""
        response_result["data"] = None
        response_result["success"] = False
        response = jsonify(response_result)
        response.status_code = response_result["code"]
        return response

if __name__ == '__main__':
    app.run(host = "192.168.32.54", port = 8800)
    # app.run(host = "192.168.38.49", port = 8800)