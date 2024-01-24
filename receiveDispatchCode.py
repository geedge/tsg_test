import os
import glob
import importlib
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/tsg', methods=["POST"])
def ReceiveCaseParameter():
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
            "api_host": "http://192.168.44.72",
            "is_log": 0,
            "env": "tsgx",
            "vsys_id": 6,
            "path": "",
            "module_name": "",
            "test_case_name": ""
        }
        project_path = "D:/Document/Project-TSG/Code/git/tsg_test"
        parameter["path"] = f"{project_path}/testcase/"
        parameter["module_name"] = module_name
        temp_folder_path = f"{project_path}/testcase/" + module_name
        folder_list = os.listdir(temp_folder_path)
        print("Test cases contain the folder: ", folder_list)
        # 匹配测试用例
        path = f"{temp_folder_path}/*.py"
        files = glob.glob(path, recursive=True)
        for file in files:
            file_name = file.split("\\")[-1]
            if file_name == test_case_name + ".py":
                parameter["test_case_name"] = test_case_name
                new_path = "testcase." + module_name + "." + test_case_name
                module = importlib.import_module(new_path)
                result = module.run(parameter)
                response_result = {}
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

if __name__ == '__main__':
    app.run(host = "192.168.32.54", port = 8800)
    # app.run(host = "192.168.64.59", port = 8800)