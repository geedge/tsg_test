# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from support.packet_generator.capture_packet import *
from support.packet_generator.traffic_generator import *
# from support.packet_generator.api_verification import *
from support.api_verification import *
# from support.packet_generator.ui_verification import *
from support.ui_verification import *
from support.packet_generator.workpath import workdir
from datetime import datetime
from threading import Thread

class Verify:
    def verify_traffic_result(self, verification, traffic_result):
        try:
            debug = "local"
            if debug == "local":
                traffic_result_temp = traffic_result["result"]
            else:
                traffic_result_temp = traffic_result
            expected_result_temp = verification["expected_result"].split(',')
            result = all(word in traffic_result_temp for word in expected_result_temp)
            if result == True:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The traffic return traffic result match the expected result.', flush=True)
                return True, ""
            elif result == False:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'The traffic return result does not match the expected result.', flush=True)
                return False, "The traffic returned result does not match the expected result."
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception Error: ", str(e), flush=True)
            return False, "Exception Error when verify excepted traffic result: " + str(e)
        
    def verify_metric_log(self, parameter, policy_configuration, traffic_generation, verification, configuration_manager, traffic_result):
        try:
            initiation_method = parameter["initiation_method"]
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to send traffic.", flush=True)
            if initiation_method == "api":
                time.sleep(3)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Start to verify the effect of the policy rule.", flush=True)
            if initiation_method == "ui":
                api_verification = APIVerification(parameter, policy_configuration, traffic_generation, verification, configuration_manager)
                api_verification_result = api_verification.api_verification(traffic_result)
                if len(api_verification_result) == 3:
                    my_driver = api_verification_result[2]
                rule_type = policy_configuration["type"]
                if len(api_verification_result) > 0 and rule_type != "statistics":
                    verification_result = [False for _ in range(3)]
                    ui_verification = UIVerification(policy_configuration, traffic_generation, verification, configuration_manager)
                    ui_verification_result = ui_verification.ui_verification(my_driver, api_verification_result, traffic_result)
                    if len(ui_verification_result) == 1:
                        return ui_verification_result
                    # 对比api和ui返回的每个结果，如果都一样，则结果是true，如果二者有一个不同，就为false
                    if rule_type == "security" or rule_type == "service_chaining" or rule_type == "proxy_intercept" or rule_type == "proxy_manipulation" or rule_type == "monitor":
                        if api_verification_result[0] == True and ui_verification_result[0] == True or (api_verification_result[0] == 'no_set' and ui_verification_result[0] == 'no_set'):
                            verification_result[0] = True
                        else:
                            verification_result[0] = False
                        if api_verification_result[1] == True and ui_verification_result[1] == True:
                            verification_result[1] = True
                        else:
                            verification_result[1] = False
                        verification_result[2] = ui_verification_result[2]
                        return verification_result
                else:
                    return api_verification_result
            elif initiation_method == "api":
                api_verification = APIVerification(parameter, policy_configuration, traffic_generation, verification, configuration_manager)
                verification_result = api_verification.api_verification(traffic_result)
                return verification_result
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception Error when verify metric and log: ", str(e), flush=True)
            return "Exception Error when verify metric and log: " + str(e)

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")