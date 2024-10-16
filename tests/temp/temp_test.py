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
    result = {
        "ui_result": "",
        "api_result": "",
        "exception_result": ""
    }
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        
        # 参数初始化
        exception_result = ""
        
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
        
        exit_flag = False
        loop_number = 1
        if len(parameter["script_type"]) == 0:
            loop_number = 2
        for _ in range(loop_number):
            # 测试用例实例化，创建测试需要的object、profile、policy rule
            case_instance_generator = CaseInstanceGenerator(test_data["policy_configuration"], parameter, loop_number)
            case_generator_result = case_instance_generator.create()
            # 完成创建后如果返回的ui_result和api_result值为空，意味着创建成功，并进行流量验证，否则返回异常值并跳过验证阶段，走清理删除步骤
            if isinstance(case_generator_result, dict) and len(case_generator_result["ui_result"]) == 0 and len(case_generator_result["api_result"]) == 0:
                # 触发流量
                sender = SendTraffic()
                traffic_result = sender.send_traffic(parameter, test_data)
                # 验证metric和log
                verification = Verify()
                verification_result = verification.verify_result(parameter, test_data, case_generator_result, traffic_result)
                if len(verification_result) == 4:
                    case_generator_result["driver"] = verification_result[3]
                    # 分析结果
                    analysis = Analyse()
                    if "driver" in case_generator_result and len(case_generator_result["driver"]) > 0:
                        result["ui_result"] = analysis.analyse_result(test_data, case_generator_result, verification_result)
                    if "cfg_list" in case_generator_result and len(case_generator_result["cfg_list"]) > 0:
                        result["api_result"] = analysis.analyse_result(test_data, case_generator_result, verification_result)
                else:
                    result["exception_result"] = verification_result
                    exit_flag = True
            elif isinstance(case_generator_result, str) and len(case_generator_result) != 0:
                result["exception_result"] = case_generator_result
                exit_flag = True
            elif isinstance(result, dict) and len(case_generator_result["ui_result"]) != 0:
                result["ui_result"] = case_generator_result["ui_result"]
                exit_flag = True
            elif isinstance(result, dict) and len(case_generator_result["api_result"]) != 0:
                result["api_result"] = case_generator_result["ui_result"]
                exit_flag = True
            # 删除配置
            if isinstance(case_instance_generator, CaseInstanceGenerator):
                deletion_result = case_instance_generator.clean_up(test_data, case_generator_result)
                if len(deletion_result["ui_result"]) > 0:
                    result["ui_result"] = result["ui_result"] + deletion_result["ui_result"]
                if len(deletion_result["api_result"]) > 0:
                    result["api_result"] = result["api_result"] + deletion_result["api_result"]
            # 针对同时执行ui和api脚本的场景，只要接收到异常，就要提前退出for循环
            if exit_flag == True and loop_number == 2:
                break
        return result
    except Exception as e:
        exception_result = str(e)
        result["exception_result"] = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Exception Error: ", e, flush=True)
        # return "Exception Error: " + str(e)
        return result
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
        "test_pc_ip": "192.168.64.86",
        "test_subcriber_id": "test6776",
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