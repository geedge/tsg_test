# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from support.traffic_manager.capture_packet import *
from support.traffic_manager.trigger_traffic import *
from support.traffic_manager.api_verification import *
from support.traffic_manager.ui_verification import *
from support.traffic_manager.workpath import workdir
from datetime import datetime
from threading import Thread

class Verification():
    def verification(self, driver, parameter, test_data, cfg_list, test_rule_element_position):
        my_driver = driver
        script_type = parameter["script_type"]
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to trigger traffic.", flush=True)
        # if test_data["policy_type"] == "service_chaining" and test_data["targeted_traffic"] == "decrypted":
        #     # SC解密流量相对特殊，只能用curl进行验证，但curl不能统计pkt和byte，故通过网口抓包来进行功能对比。
        #     parse = configparser.ConfigParser()
        #     parse_dir = os.path.join(workdir, "configuration_file.ini")
        #     parse.read(parse_dir, encoding="utf-8")
        #     intf = parse.get("capture", "intf")
        #     filter = parse.get("capture", "filter")
        #     source_ip = parse.get("capture", "source_ip")
        #     timeout = parse.get("capture", "timeout")
        #     capture_packet = CapturePacket()
        #     trigger_traffic = TriggerTraffic()
        #     capture_thread = Thread(target=capture_packet.capture_packet, args=(intf, filter, source_ip, int(timeout)))
        #     traffic_thread = Thread(target=trigger_traffic.trigger_traffic, args=(parameter, test_data))
        #     # 启动线程
        #     capture_thread.start()
        #     traffic_thread.start()
        #     # 等待线程完成
        #     capture_thread.join()
        #     traffic_thread.join()
        # else:
        trigger_traffic = TriggerTraffic()
        traffic_result = trigger_traffic.trigger_traffic(parameter, test_data)
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule.", flush=True)
        if script_type == "ui":
            traffic_verification = ApiVerification()
            api_verification_result = traffic_verification.api_verification(my_driver, parameter, test_data, traffic_result, cfg_list)
            api_verification_result = [True, True, True, True]
            policy_type = test_data["policy_type"]
            if len(api_verification_result) > 0 and policy_type != "statistics":
                verification_result = [False for _ in range(4)]
                ui_verification = UiVerification()
                ui_verification_result = ui_verification.ui_verification(my_driver, parameter, test_data, api_verification_result, test_rule_element_position, traffic_result, cfg_list)
                # 对比api和ui返回的每个结果，如果都一样，则结果是true，如果二者有一个不同，就为false
                if policy_type == "security" or policy_type == "service_chaining" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor":
                    if api_verification_result[0] == True and ui_verification_result[0] == True:
                        verification_result[0] = True
                    else :
                        verification_result[0] = False
                    if api_verification_result[1] == True and ui_verification_result[1] == True:
                        verification_result[1] = True
                    else :
                        verification_result[1] = False
                    if api_verification_result[2] == True and ui_verification_result[2] == True:
                        verification_result[2] = True
                    else :
                        verification_result[2] = False
                    verification_result[3] = ui_verification_result[3]
                    return verification_result
            else:
                return api_verification_result
        elif script_type == "api":
            traffic_verification = ApiVerification()
            verification_result = traffic_verification.api_verification("", parameter, test_data, traffic_result, cfg_list)
            return verification_result

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")