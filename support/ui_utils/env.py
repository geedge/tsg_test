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
from support.ui_utils.workpath import workdir
from selenium import webdriver
from support.ui_utils.my_web_driver import MyWebDriver
from support.ui_utils.login_logout import LogInOut
from datetime import datetime 

driver = None  # 全局变量用户保存webdirver实例

def my_driver():
    global driver
    # 初始化
    chrome_option = webdriver.ChromeOptions()
    os_name = platform.system()
    prefs = {
    "download.default_directory": workdir  # 设置下载路径
    }
    chrome_option.add_experimental_option("prefs", prefs)
    if os_name == "Linux":
        remote_url = get_docker_ip()
        # 启用无窗口模式
        chrome_option.add_argument("--no-sandbox")
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--disable-gpu")
        chrome_option.add_argument("--disable-dev-shm-usage")
        chrome_option.add_argument("--window-size=1920, 1200")
    elif os_name == "Windows":
        remote_url = read_config("selenium_server", "url")
        # 启用无痕模式
        chrome_option.add_argument("--incognito")
        # 启用无窗口模式
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--disable-gpu")
        chrome_option.add_argument("--window-size=1920, 1200")
    # 关闭“chrome正受到自动测试软件的控制”
    # chrome_option.add_experimental_option('useAutomationExtension', False)
    # chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 取消idle timeout
    # chrome_option.add_argument("--disable-idle-timeout")
    # 不关闭浏览器窗口
    # chrome_option.add_experimental_option("detach", True)
    # 打开chrome浏览器
    driver = MyWebDriver(
        command_executor=remote_url,
        options=chrome_option
    )
    # driver.implicitly_wait(2)
    driver.maximize_window()
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Web Driver has been initialized successfully.", flush=True)
    return driver

def read_config(url, value):
    loginout_parse = configparser.ConfigParser()
    loginout_parse_dir = os.path.join(workdir, "configuration_file.ini")
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
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Web Driver has been closed successfully.", flush=True)
        time.sleep(1)
        
def initiate_selenium_request():
    for i in range(5):
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Run Selenium Server for the {} time.".format(i+1), flush=True)
            os_name = platform.system()
            if os_name == "Linux":
                remote_url = get_docker_ip()
            elif os_name == "Windows":
                remote_url = read_config("selenium_server", "url")
            response = requests.get(remote_url)
            if len(response.text) != 0:
                break
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Fail to start selenium server.", flush=True)

def get_docker_ip():
    interfaces = psutil.net_if_addrs()
    if "docker0" in interfaces:
        for addr in interfaces["docker0"]:
            if addr.family == 2:
                docker_ip = addr.address
                remote_url = "http://" + docker_ip + ":4444"
                return remote_url

# 处理ctrl+c中断
def handle_interrupt(sinnum, frame):
    global driver
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], driver, "主动中断")
    time.sleep(1)
    if driver:
        driver.close()
    exit(1)
