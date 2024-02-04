import requests
import json

class LogIn():
    def encryptPwd(self, password, api_server):
        url = api_server + "/v1/user/encryptpwd"
        pwJson = {"password": ""}
        pwJson["password"] = password
        response = requests.get(url, params=pwJson)
        data = json.loads(response.text)
        pwd = data["data"]["encryptpwd"]
        return pwd

    def login(self, user, pwd, api_server):
        url = api_server + "/v1/user/login"
        loginJson = {"username": "", "password": ""}
        loginJson["username"] = user
        loginJson["password"] = pwd
        response = requests.post(url, json=loginJson)
        jsonData = json.loads(response.text)
        token = jsonData["data"]["token"]
        return token

if __name__ == "__main__":
    print("test")