from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/tsg', methods=["POST"])
def get_request_body():
    # 从MS或Jmeter等工具的请求体中获取参数
    req_json = request.get_json()
    req_json =  {
        "run_status" : 1,
        "test_case": "all",
        "tag": "all"
        # "code": 200,
        # "policy_type": "security",
        # "source_ip": ["192.168.64.59", "192.168.64.60"],
        # "destination_ip": ["1.1.1.1", "1.1.1.2"],
        # "action": "deny",
        # "app_name": "taobao",
        # "app_full_name": "com.taobao.taobao"
    }
    run_status = req_json.get("run_status")
    test_case = req_json.get("test_case")
    tag = req_json.get("tag")
    while 1:
        if run_status == 1:
            print("Dispatch configure to tsg.")
            result = "pass"
            break
    return jsonify(result)

if __name__ == '__main__':
    app.run(host = "192.168.32.54", port = 8800)