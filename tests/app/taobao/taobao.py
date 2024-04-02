# -*- encoding=utf8 -*-
__author__ = "app"

import os
import sys
extract_app_signature_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(extract_app_signature_dir)
# import logging
# logger = logging.getLogger("airtest")
# logger.setLevel(logging.ERROR)
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

def open():
    stop_app("com.taobao.taobao")  # 关闭app
    start_app("com.taobao.taobao")  # 打开app
    sleep(20)
    if poco(text="同意").exists():
        poco(text="同意").click()
    try:
        snapshot(msg="taobao_open")
        assert_equal(poco(text="订阅").exists(), True, "taobao_open succeeded")
        return print('taobao_open succeeded', flush=True)
    except AssertionError:
        return print('taobao_open failed', flush=True)

def close():
    stop_app("com.taobao.taobao")

if __name__ == '__main__':
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    
    auto_setup(__file__, logdir=True)
    device_id = "emulator-5554"
    auto_setup(__file__, devices=["android://127.0.0.1:5037/" + device_id], logdir=True)

    operation = sys.argv
    for i in operation:
        if i == 'open':
            open()
            close()