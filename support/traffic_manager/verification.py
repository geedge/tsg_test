# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import support.ui_utils.env
import subprocess
import configparser
import json
import platform
import pytz
from support.traffic_manager.traffic_verification import *
from support.traffic_manager.ui_verification import *
from support.traffic_manager.workpath import workdir
from datetime import datetime

class Verification():
    def verification(self, driver, parameter, test_data, cfg_list):
        my_driver = driver
        script_type = parameter["script_type"]
        if script_type == "ui":
            traffic_verification = TrafficVerification()
            api_verification_result = traffic_verification.traffic_verification(my_driver, parameter, test_data, [])
            ui_verification = UiVerification()
            ui_verification_result = ui_verification.ui_verification(my_driver, parameter, test_data, [])
            
        elif script_type == "api":
            traffic_verification = TrafficVerification()
            verification_result = traffic_verification.traffic_verification("", parameter, test_data, cfg_list)
        return verification_result

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")