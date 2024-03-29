import time
import pytest
import time
import atexit
import sys
import os
import signal
import configparser
import platform
import requests
import psutil
import subprocess
from workpath import workdir
from selenium import webdriver
from support.ui_utils.my_web_driver import MyWebDriver
from support.ui_utils.login_logout import LogInOut

driver = None  # 全局变量用户保存webdirver实例

def my_driver():
    global driver
    # 初始化
    chrome_option = webdriver.ChromeOptions()
    os_name = platform.system()
    if os_name == "Linux":
        # result = subprocess.check_output("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' automation", shell=True)
        # output = result.decode("utf-8")
        interfaces = psutil.net_if_addrs()
        if "eth0" in interfaces:
            for addr in interfaces["eth0"]:
                if addr.family == 2:
                    docker_ip = addr.address
                    remote_url = "http://" + docker_ip + ":4444"
        # 启用无窗口模式
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument("--headless")
        chrome_option.add_argument('--window-size=1920, 1200')
    elif os_name == "Windows":
        remote_url = read_config("remote_url", "url")
        # 启用无痕模式
        # chrome_option.add_argument("--headless")
        chrome_option.add_argument("--incognito")
    # 打开chrome浏览器
    driver = MyWebDriver(
        command_executor=remote_url,
        options=chrome_option
    )
    # driver.implicitly_wait(2)
    driver.maximize_window()
    return driver

def read_config(url, value):
    loginout_parse = configparser.ConfigParser()
    loginout_parse_dir = os.path.join(workdir, "ui_utils", "login_logout.ini")
    loginout_parse.read(loginout_parse_dir, encoding="utf-8")
    remote_url = loginout_parse.get(url, value)
    return remote_url

def setup():
    # global driver
    # driver = my_driver()
    loginout = LogInOut(driver)
    loginout.login()

def teardown():
    global driver
    if driver:
        driver.quit()
        time.sleep(1)
        
def initiate_selenium_request():
    for i in range(5):
        try:
            print("Run selenium server for the {} time.".format(i+1))
            # run_selenium()
            remote_url = read_config("remote_url", "url")
            response = requests.get(remote_url)
            print(response.text)
            if len(response.text) != 0:
                break
        except:
            print("Fail to start selenium server.")

def run_selenium():
    os_name = platform.system()
    if os_name == "Windows":
        jar_path = "D:/java_selenium/selenium-server-4.8.1.jar"
        command = ["java", "-jar", jar_path, "standalone"]
    elif os_name == "Linux":
        # jar_path = "/opt/tsg_test/package/selenium-server-4.8.1.jar"
        jar_path = "/app/package/selenium-server-4.8.1.jar"
        command = ["java", "-jar", jar_path, "standalone"]
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    print(f"Standard Output: {result.stdout}")

def kill_selenium():
    os_name = platform.system()
    if os_name == "Windows":
        for proc in psutil.process_iter(['name']):
            try:
                # print(proc.info['name'])
                if proc.info['name'] == "java.exe":
                    proc.kill()
                    print(f"The process {proc.info['name']} is killed.")
            except:
                pass
    elif os_name == "Linux":
        print("to be added...")

# @pytest.fixture()
# def demo_fixture():
#     global driver
#     setup()
#     yield driver
#     teardown()

# def pytest_collection_modifyitems(items):
#     """
#     测试用例收集完成时，将收集到的name和nodeid的中文显示在控制台上,中文转换
#     https://www.cnblogs.com/canglongdao/p/13418305.html
#     https://blog.csdn.net/weixin_46043193/article/details/114284643
#     """
#     for i in items:
#         i.name = i.name.encode("utf-8").decode("unicode_escape")
#         i._nodeid = i.nodeid.encode("utf-8").decode("unicode_escape")

# 处理ctrl+c中断
def handle_interrupt(sinnum, frame):
    global driver
    print(driver, "主动中断")
    time.sleep(1)
    if driver:
        driver.close()
    exit(1)

# 注册Ctrl+C中断处理函数，该函数切勿打开，因为：该函数不能在子线程中运行，只能在主线程中运行
# signal.signal(signal.SIGINT, handle_interrupt)