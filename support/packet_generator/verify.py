# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from support.packet_generator.capture_packet import *
from support.packet_generator.trigger_traffic import *
from support.packet_generator.api_verification import *
from support.packet_generator.ui_verification import *
from support.packet_generator.workpath import workdir
from datetime import datetime
from threading import Thread

class Verify:
    def verify_result(self, driver, parameter, test_data, cfg_list, test_rule_element_position):
        try:
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
            #     sender = SendTraffic()
            #     capture_thread = Thread(target=capture_packet.capture_packet, args=(intf, filter, source_ip, int(timeout)))
            #     traffic_thread = Thread(target=sender.send_traffic, args=(parameter, test_data))
            #     # 启动线程
            #     capture_thread.start()
            #     traffic_thread.start()
            #     # 等待线程完成
            #     capture_thread.join()
            #     traffic_thread.join()
            # else:
            # 等待配置同步
            if script_type == "api":
                time.sleep(3)
            sender = SendTraffic()
            traffic_result = sender.send_traffic(parameter, test_data)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule.", flush=True)
            if script_type == "ui":
                traffic_verification = ApiVerification()
                api_verification_result = traffic_verification.api_verification(my_driver, parameter, test_data, traffic_result, cfg_list)
                if len(api_verification_result) == 4:
                    my_driver = api_verification_result[3]
                elif len(api_verification_result) == 5:
                    my_driver = api_verification_result[4]
                policy_type = test_data["policy_type"]
                if len(api_verification_result) > 0 and policy_type != "statistics":
                    verification_result = [False for _ in range(4)]
                    ui_verification = UiVerification()
                    ui_verification_result = ui_verification.ui_verification(my_driver, parameter, test_data, api_verification_result, test_rule_element_position, traffic_result, cfg_list)
                    # 对比api和ui返回的每个结果，如果都一样，则结果是true，如果二者有一个不同，就为false
                    if policy_type == "security" or policy_type == "service_chaining" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor":
                        if api_verification_result[0] == True and ui_verification_result[0] == True:
                            verification_result[0] = True
                        else:
                            verification_result[0] = False
                        if api_verification_result[1] == True and ui_verification_result[1] == True or (api_verification_result[1] == 'no_set' and ui_verification_result[1] == 'no_set'):
                            verification_result[1] = True
                        else:
                            verification_result[1] = False
                        if api_verification_result[2] == True and ui_verification_result[2] == True:
                            verification_result[2] = True
                        else:
                            verification_result[2] = False
                        verification_result[3] = ui_verification_result[3]
                        return verification_result
                else:
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"testapi_verification_result:{api_verification_result}")
                    return api_verification_result
            elif script_type == "api":
                traffic_verification = ApiVerification()
                verification_result = traffic_verification.api_verification("", parameter, test_data, traffic_result, cfg_list)
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"verification_result:{verification_result}")
                return verification_result
        except Exception as e:
            # 返回此异常有时导致执行结果为成功，本地参数和配置文件参数中的vsys修改为不一致可复现
            #return f"Exception: {e}"
            # 所以修改为如下返回
            return (False, False, False, f"Exception: {e}", f"Exception: {e}")

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")