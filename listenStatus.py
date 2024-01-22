from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/airtest', methods=["POST"])
def get_request_body():
    # 从MS或Jmeter等工具的请求体中获取参数
    req_json = request.get_json()
    code = req_json.get("code")
    policy_type = req_json.get("policy_type")
    policy_src_ip = req_json.get("source_ip")
    policy_dst_ip = req_json.get("destination_ip")
    policy_action = req_json.get("action")
    policy_app_name = req_json.get("app_name")
    policy_app_full_name = req_json.get("app_full_name")
    while 1:
        if code == 200:
            print("Dispatch configure to tsg")
    return jsonify(policy_type, code, policy_src_ip, policy_dst_ip, policy_action, policy_app_name, policy_app_full_name)

if __name__ == '__main__':
    app.run(host = "192.168.32.54", port = 8800)