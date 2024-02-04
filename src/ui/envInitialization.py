import time
import pytest
import time
import atexit
import sys
import os
import signal
import configparser
from workpath import workdir
from selenium import webdriver
from myWebDriver import MyWebDriver
from logInOut import LogInOut

driver = None  # 全局变量用户保存webdirver实例

def my_driver():
    print("\n用例开始时执行。。。")
    global driver
    # 初始化
    loginout_parse = configparser.ConfigParser()
    loginout_parse_dir = os.path.join(workdir, "ui", "loginout.ini")
    loginout_parse.read(loginout_parse_dir, encoding="utf-8")
    remote_url = loginout_parse.get("remote_url", "url")
    chrome_option = webdriver.ChromeOptions()
    # 添加启用无痕模式的选项
    chrome_option.add_argument("--incognito")
    # chrome_option.add_argument('--headless')  # 启用Headless模式
    driver = MyWebDriver(
        command_executor=remote_url,
        options=chrome_option
    )
    # driver.implicitly_wait(2)
    driver.maximize_window()
    return driver

def setup():
    # global driver
    # driver = my_driver()
    loginout = LogInOut(driver)
    loginout.login()

def teardown():
    global driver
    if driver:
        print("\n用例结束时执行。。。")
        print("\n切换到默认语言:English!")
        driver.quit()
        time.sleep(1)

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