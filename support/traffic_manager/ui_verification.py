# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import support.api_utils.get_log
import support.api_utils.policy_verify
import support.ui_utils.env
import subprocess
import configparser
import json
import platform
import pytz
import support.traffic_manager.trex_replay as trex_replay
from support.traffic_manager.workpath import workdir
from datetime import datetime
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.policy_element_position import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from support.traffic_manager.traffic_replay import TrafficReplay

class UiVerification():
    def ui_verification(self, driver, parameter, test_data, cfg_list):
        my_driver = driver
        result = ""
        policy_type = test_data["policy_type"]
        if policy_type == "security" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor":
            return result
        elif policy_type == "statistics":
            return result
        elif policy_type == "service_chaining":
            return result

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")