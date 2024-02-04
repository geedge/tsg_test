import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import getLog
import policyVerify
import subprocess
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from traffic_replay.traffic_replay import TrafficReplay

class TrafficVerification():
    def traffic_verification(self, parameter, condition, template_path, cfg_list):
    # def traffic_verification(self, condition, test_pc_ip, is_log, statistics_sc_info_list, api_server, vsys_id, path_dict):
        is_log = parameter["is_log"]
        test_pc_ip = parameter["test_pc_ip"]
        api_server = parameter["api_server"]
        vsys_id = parameter["vsys_id"]
        if "api" in parameter["path"]:
            token = parameter["token"]
        isMultiPriority = condition['isMultiPriority']
        if isMultiPriority:
            rule_num = condition['ruleNum']
        else:
            rule_num = 1
        if len(cfg_list) != 0 :
            create_policies_ids = cfg_list["create_policies_ids"]
            statistics_sc_info_list = cfg_list["statistics_sc_info_list"]
            policy_id = list(create_policies_ids[0].values())[0]
        # 判断，如果condition中包含名为command的key，则读取command来执行，否则执行默认的
        policy_type = condition["policyType"]
        log = getLog.GetLog()
        if policy_type == "tsg_security" or policy_type == "pxy_intercept" or policy_type == "pxy_manipulation" or policy_type == "monitor":
            # 获取开始时间
            now = datetime.utcnow()
            start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            # 等待时间，等待策略生效
            time.sleep(30)
            # 触发流量
            command = condition['command']
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
            output, error = p.communicate()
            output = output + error
            # cmd_return = output.decode(errors='ignore')
            cmd_return = output
            print(output)
            hope_return = condition['hope_return']
            # 获取结束时间
            now = datetime.utcnow()
            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            cmd_result = self.is_in(cmd_return, hope_return)
            loop_num = condition['ruleNum']
            is_counters, is_log_query = self.is_verify(condition, loop_num, 'counters', 'log_query_param')
            if is_log == 1:
                if is_log_query == 1:
                    # 考虑到有5分钟后才出日志的情况，循环5次
                    for _ in range(5):
                        now = datetime.utcnow()
                        end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                        # 等待产生日志
                        time.sleep(30)
                        log_result = log.get_log_by_condition(token, rule_num, start_time, end_time, test_pc_ip, create_policies_ids, condition, api_server, vsys_id)
                        if log_result == True:
                            break
                elif is_log_query == 0:
                    # 此时代表不需要进行logs模块的校验，可能为security shunt动作或statistics，sc策略等
                    log_result = True
                if is_counters == 1:
                    for _ in range(5):
                        now = datetime.utcnow()
                        end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                        time.sleep(30)
                        metric_result = log.get_metric(token, rule_num, start_time, end_time, create_policies_ids, condition, api_server, vsys_id)
                        if log_result == True:
                            break
                elif is_counters == 0:
                    metric_result = True
            else:
                metric_result = True
                log_result = True
            return cmd_result, log_result, metric_result
        elif policy_type == "statistics":      # statistics 使用trex流量回放验证
            # 获取开始时间
            #time.sleep(1)
            #print(55)
            #return 1, 1, 1, "调试"
            time.sleep(5)
            now = datetime.utcnow()
            start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            print("trex，回放流量方法")
            # 解析trex使用参数， 解析client server ip
            for ip_item in condition["obj_condition_1"]:
                if "ATTR_SOURCE_ADDR" in ip_item.values():
                    if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                        clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                        clients_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                    else:
                        clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                        clients_end = clients_start
                if "ATTR_DESTINATION_ADDR" in ip_item.values():
                    if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                        servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                        servers_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                    else:
                        servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                        servers_end = servers_start
            # 解析trex 命令行参数，-m -d
            if "trex" in condition.keys():
                m = condition["trex"]["m"]
                d = condition["trex"]["d"]
                yaml_name = condition["trex"]["yaml_name"].strip()
                pcap_name = condition["trex"]["pcap_name"].strip()
            else:
                print("trex参数使用默认值：")
                m = 1
                d = 1
                yaml_name = "http_50.yaml"
                pcap_name = "http_get_347pkts.pcap"
            # 执行trex命令前，策略验证，查看下发策略是否生效
            ######## 不要删除
            verify_policy_break_count = 0
            while True:      # 多次策略验证
                verify_attribute_dict = {"src_ip": clients_start, "dst_ip": servers_start}
                print(verify_attribute_dict)
                policy_verif = policyVerify.PolicyVerify()
                hit_policy_list = policy_verif(condition, verify_attribute_dict, token, api_server, vsys_id)
                if policy_id in hit_policy_list:   # 策略生效，验证通过，跳出验证
                    break
                if verify_policy_break_count > 40:    # 预计验证10分钟，仍然不生效，则结束执行，报异常。
                    # 直接调用清空策略方法
                    print("测试不生效，结束测试：策略id：{}".format(policy_id))
                    return False, False, False
                verify_policy_break_count += 1
                time.sleep(20)
                print("间隔{}秒，第{}次策略验证结果：策略验证失败，策略没有生效，{}策略id：{} ...".format(20*verify_policy_break_count, verify_policy_break_count, condition["policyType"], policy_id))
            time.sleep(5)     # 策略验证通过后，延迟五秒启动流量回放
            # 执行回放命令
            traffic_replay = TrafficReplay(template_path)
            statistics_metircs = traffic_replay.trex_playback(yaml_name, pcap_name, m=m, d=d, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
            time.sleep(50)
            now = datetime.utcnow()
            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            cmd_return = hope_return = condition['hope_return']
            # 断言判断
            trex_ip_info = {}
            trex_ip_info["clients_start"] = clients_start
            trex_ip_info["clients_end"] = clients_end
            trex_ip_info["servers_start"] = servers_start
            trex_ip_info["servers_end"] = servers_end
            if len(statistics_sc_info_list) > 0:  # 非空
                for statistics_info in statistics_sc_info_list:
                    n = 1    #自增变量
                    fail_count = 1   #失败重试变量
                    while n < 3:
                        now = datetime.utcnow()
                        end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')   # 重新获取结束时间
                        metric_results = log.get_livechart_statistics(token, start_time, end_time, statistics_info, statistics_metircs, trex_ip_info, api_server, vsys_id)
                        metric_result = metric_results[0]
                        if metric_result == True:  # 返回结果不等于333，则退出循环查询
                            break
                        elif metric_result == False:  # 查询验证失败时，再查询验证一次
                            if fail_count > 2:
                                break
                            fail_count += 1
                        time.sleep(60)
                        n += 1
                if  metric_results[0] == 333:     # API 查询失败时变量赋值
                    metric_result = False
            return metric_result, metric_result, metric_result, metric_results[1]    # 匹配其它策略模式
        elif policy_type == "service_chaining":
            active_dest_ips_list = ["2.2.2.53", "2.2.2.56", "2.2.2.57"] # vxlan时判断dest_ip是否在bfd探测为active的ip里
            if condition["targeted_traffic"] == "raw":
                # 获取开始时间
                time.sleep(5)
                now = datetime.utcnow()
                start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                print("trex，回放流量方法")
                # 解析trex使用参数， 解析client server ip
                for ip_item in condition["obj_condition_1"]:
                    if "ATTR_SOURCE_ADDR" in ip_item.values():
                        if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                            clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                            clients_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                        else:
                            clients_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                            clients_end = clients_start
                    if "ATTR_DESTINATION_ADDR" in ip_item.values():
                        if "-" in ip_item["objectList"][0]["addItemList"][0]["ip_address"]:
                            servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[0]
                            servers_end = ip_item["objectList"][0]["addItemList"][0]["ip_address"].split("-")[-1]
                        else:
                            servers_start = ip_item["objectList"][0]["addItemList"][0]["ip_address"]
                            servers_end = servers_start
                # 解析trex 命令行参数，-m -d
                if "trex" in condition.keys():
                    m = condition["trex"]["m"]
                    d = condition["trex"]["d"]
                    yaml_name = condition["trex"]["yaml_name"].strip()
                    pcap_name = condition["trex"]["pcap_name"].strip()
                else:
                    print("trex参数使用默认值：")
                    m = 1
                    d = 1
                    yaml_name = "http_50.yaml"
                    pcap_name = "http_get_347pkts.pcap"
                # 执行回放命令
                traffic_replay = TrafficReplay(template_path)
                sc_metircs = traffic_replay.trex_playback(yaml_name, pcap_name, m=m, d=d, clients_start=clients_start, clients_end=clients_end, servers_start=servers_start, servers_end=servers_end)
                time.sleep(20)
                now = datetime.utcnow()
                end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                cmd_return = hope_return = condition["hope_return"]
                # 断言判断
                if len(statistics_sc_info_list) > 0:   # 非空
                    for statistics_info in statistics_sc_info_list:
                        n = 0    #自增变量
                        fail_count = 0   #失败重试变量
                        while n <= 4:
                            now = datetime.utcnow()
                            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')   # 重新获取结束时间
                            metric_result = log.get_sc_metric(token, start_time, end_time, statistics_info, sc_metircs, active_dest_ips_list, api_server)
                            if metric_result == True:  # 返回结果不等于333，则退出循环查询
                                break
                            elif metric_result == False or metric_result == 333:  # 查询验证失败时，再查询验证两次
                                if fail_count >= 2:
                                    break
                                fail_count += 1
                            time.sleep(60)
                            n += 1
                    if metric_result == 333:
                        if statistics_info["sf_method"] == "vxlan_g" and statistics_info["sf_dest_ip"] not in active_dest_ips_list:
                            metric_result = True
                        else:
                            metric_result = False
                    elif metric_result == 444:
                        metric_result = False
                cmd_result = metric_result
            elif condition["targeted_traffic"] == "decrypted":
                # 获取开始时间
                now = datetime.utcnow()
                start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                # 等待时间，等待策略生效
                time.sleep(30)
                # 触发流量
                command = condition['command']
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, _ = p.communicate()
                cmd_return = output.decode()
                hope_return = condition['hope_return']
                # 获取结束时间
                now = datetime.utcnow()
                end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                cmd_result = self.is_in(cmd_return, hope_return)
                if len(statistics_sc_info_list) > 0:  # 非空
                    for statistics_info in statistics_sc_info_list:
                        n = 0  # 自增变量
                        fail_count = 0  # 失败重试变量
                        while n <= 6:
                            now = datetime.utcnow()
                            end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')  # 重新获取结束时间
                            metric_result = log.get_sc_metric(token, start_time, end_time, statistics_info,"", active_dest_ips_list, api_server)
                            if metric_result == True:  # 返回结果不等于333，则退出循环查询
                                break
                            elif metric_result == False or metric_result == 333:  # 查询验证失败时，再查询验证两次
                                if fail_count >= 2:
                                    break
                                fail_count += 1
                            time.sleep(60)
                            n += 1
                    if metric_result == 333:
                        if statistics_info["sf_method"] == "vxlan_g" and statistics_info["sf_dest_ip"] not in active_dest_ips_list:
                            metric_result = True
                        else:
                            metric_result = False
                    elif metric_result == 444:
                        metric_result = False
            return cmd_result, metric_result, metric_result
        elif policy_type == "shaping":
            # 假数据
            return True, True, True

    def is_in(self, full_str, sub_str):
        sub_str = sub_str.split(',')
        # 遍历sub_str中的每个单词，并检查该单词是否在full_str中
        cmd_result = all(word in full_str for word in sub_str)
        return cmd_result # 返回：True or False

    def is_verify(self, condition, loop_num, counters, log_query_param):
        # 判断传入了验证日志、metric相关的参数
        is_counters = 0
        is_log_query = 0
        for i in range(loop_num):
            index = i + 1
            counters_data = condition[counters + '_' + str(index)]
            if counters_data != {}:
                is_counters = 1
                break
        for i in range(loop_num):
            index = i + 1
            log_query_param_data = condition[log_query_param + '_' + str(index)]
            if len(log_query_param_data) > 0:
                is_log_query = 1
                break
        return is_counters, is_log_query

if __name__ == "__main__":
    print("test")