import requests
import json
from datetime import datetime 

class LogIn:
    def encryptPwd(self, password, api_server):
        url = api_server + "/v1/users/encryptpwd"
        pwJson = {"password": ""}
        pwJson["password"] = password
        response = requests.get(url, params=pwJson, verify=False)
        data = json.loads(response.text)
        pwd = data["data"]["encryptpwd"]
        return pwd

    def login(self, user, pwd, api_server):
        url = api_server + "/v1/users/login"
        loginJson = {"username": "", "password": "", "auth_mode": 1, "ldap_id": "", "vsys_id": 0}
        loginJson["username"] = user
        loginJson["password"] = pwd
        response = requests.post(url, json=loginJson, verify=False)
        jsonData = json.loads(response.text)
        token = jsonData["data"]["token"]
        return token

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")