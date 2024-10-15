# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from datetime import datetime
from support.report_update import ReportUpdate
from support.instance_utils.case_instance_generator import CaseInstanceGenerator
from support.packet_generator.verify import Verify
from support.packet_generator.trigger_traffic import *
from support.api_utils.analyse_result import Analyse
from support.ui_utils.workpath import workdir

def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        
        # 参数初始化
        exception_result = ""
        result = {
            "ui_result": "",
            "api_result": ""
        }
        
        # 脚本启动时间
        start_time = time.time()
        
        # 测试数据
        test_data = {
            "policy_configuration":{
                "name": "automation_test_zk",
                "type": "security",
                "action": "deny",
                "source": [
                    {
                        "negate_option": False,
                        "objects": [
                            {
                                "type": "ip",
                                "sub_type": "ip",
                                "statistics_option": "elaborate",
                                "name": "secy_srcip",
                                "description": "test",
                                "member_type": "item",
                                "items": [
                                    {
                                        "op": "add",
                                        "ip": "1.1.1.1",
                                        "interval": "0-65535"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "destination": [
                    {
                        "negate_option": False,
                        "objects": [
                            {
                                "type": "fqdn",
                                "sub_type": "fqdn",
                                "statistics_option": "elaborate",
                                "name": "secy_fqdn",
                                "description": "test",
                                "member_type": "item",
                                "items": [
                                    {
                                        "op": "add",
                                        "keywords": "*example.com"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "application": {
                    "objects": [
                        {
                            "name": "http"
                        }
                    ],
                    "negate_option": False
                },
                "action_parameter": {
                    "method": "block",
                    "packet_capture": {
                        "enable": 0
                        # "capture_depth": 2000
                    },
                    "code": 403,
                    "profile": {
                        "format": "html",
                        "name": "secy_respage",
                        "content_name": workdir + "/support/ui_utils/profile/profile_file/testa.html",
                    },
                    "message": "html_profile"
                },
            },
            "traffic_generation": {
                "protocol": "http",
                "type": "curl",
                "command": "curl -kv --connect-timeout 10 -m 10 http://www.example.com/"
            },
            "verification":{
                "expected_return": "Example Domain",
                "counters": {"hits": 2},
                "log_query_param": [
                    {"query_field_key":"server_fqdn", "query_value": "www.example.com"}
                ]
            },
        }
        
        number = 1
        if len(parameter["script_type"]) == 0:
            number = 2
        for _ in range(number):
            # 测试用例实例化
            case_instance_generator = CaseInstanceGenerator(test_data["policy_configuration"], parameter, number)
            generator_result = case_instance_generator.create()
            # 创建时如果返回的ui_result和api_result值为空，意味着创建成功，接下来进行流量验证
            if len(generator_result["create_ui_result"]) == 0 and len(generator_result["create_api_result"]) == 0:
                # 触发流量
                trigger = TriggerTraffic()
                traffic_result = trigger.send_traffic(parameter, test_data)
                # 验证
                verification = Verify()
                # verification_result = verification.verify_result(driver, parameter, test_data, cfg_list, element_position_map)
                verification_result = verification.verify_result(parameter, test_data, generator_result, traffic_result)
                if len(verification_result) != 0:
                    if len(verification_result) == 4:
                        generator_result["driver"] = verification_result[3]
                    elif len(verification_result) == 5:
                        generator_result["driver"] = verification_result[4]
                    # 分析结果
                    analysis = Analyse()
                    # result = analysis.analyse_result(test_data, generator_result["cfg_list"], verification_result)
                    result["ui_result"] = analysis.analyse_result(test_data, generator_result, verification_result)
            # 删除配置
            if isinstance(case_instance_generator, CaseInstanceGenerator):
                delete_result = case_instance_generator.delete_data(test_data, generator_result)
                if len(delete_result["delete_ui_result"]) > 0:
                    result["ui_result"] = result["ui_result"] + delete_result["delete_ui_result"]
                if len(delete_result["delete_api_result"]) > 0:
                    result["api_result"] = result["api_result"] + delete_result["delete_api_result"]
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        return "Error: " + str(e)
    finally:
        # 统计脚本用时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)
            
if __name__ == '__main__':
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/tests/api",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    run(parameter)