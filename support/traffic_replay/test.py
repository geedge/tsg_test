import requests
import json

def call_rest_api(api_server, data):
    url = api_server + "/v1/traffic"
    headers = {"Content-Type": "application/json"} 
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200: 
        jsonData = json.loads(response.text)
        jsonData = response.json()
    return jsonData

if __name__ == "__main__":
    print("test")
    data = {
        "type": "curl",
        "command": "curl -kv https://www.google.com"
    }
    # json = {
    #     "type": "trex",
    #     "pcap_name": "http_get_347pkts.pcap",
    #     "yaml": "http_50.yaml",
    #     "m": 100,
    #     "d": 1,
    # }
    call_rest_api("http://192.168.38.49:8900", data)