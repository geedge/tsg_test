# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from datetime import datetime
from support.api_utils.log_in import LogIn
# from support.packet_generator.workpath import workdir
from support.api_utils.create_objects import CreateObjects
from support.api_utils.create_libraries import CreateLibraries
from support.api_utils.create_profiles import CreateProfiles
from support.api_utils.create_rules import CreateRules
from support.api_utils.query_rule_metric import QueryRuleMetric
from support.api_utils.query_rule_log import QueryRuleLog
from support.api_utils.delete_objects import DeleteObjects
from support.api_utils.delete_libraries import DeleteLibraries
from support.api_utils.delete_profiles import DeleteProfiles
from support.api_utils.delete_rules import DeleteRules

class APIClient:
    def __init__(self, parameter):
        log_in = LogIn()
        pwd = log_in.encryptPwd(parameter["password"], parameter["api_server"])
        self.token = log_in.login(parameter["username"], pwd, parameter["api_server"])
        self.headers = {"Content-Type": "application/json", "Authorization": self.token}
        self.parameter = parameter
        
    def create_objects(self, policy_configuration):
        objects = CreateObjects(self.parameter, self.headers)
        object_uuids_tuple, error = objects.create_objects(policy_configuration)
        return object_uuids_tuple, error
    
    def create_libraries(self, policy_configuration):
        libraries = CreateLibraries(self.parameter, self.headers)
        library_uuids_tuple, error = libraries.create_libraries(policy_configuration)
        return library_uuids_tuple, error 
    
    def create_profiles(self, policy_configuration):
        profiles = CreateProfiles(self.parameter, self.headers)
        profile_uuids_tuple, error = profiles.create_profiles(policy_configuration)
        return profile_uuids_tuple, error
        
    def create_rules(self, policy_configuration, object_uuids_tuple, library_uuids_tuple, profile_uuids_tuple):
        self.policy_configuration = policy_configuration
        rules = CreateRules(self.parameter, self.headers, object_uuids_tuple, library_uuids_tuple, profile_uuids_tuple)
        rule_uuids_tuple, error = rules.create_rules(policy_configuration)
        return rule_uuids_tuple, error
    
    def query_rule_metric(self, verification_result, rule_uuids_tuple, start_time, traffic_result):
        query = QueryRuleMetric(self.parameter, self.policy_configuration, self.token, traffic_result)
        metric_result = query.query_rule_metric(verification_result, rule_uuids_tuple, start_time)
        return metric_result
    
    def query_rule_log(self, traffic_generation, verification_result, rule_uuids_tuple, start_time, traffic_result):
        query = QueryRuleLog(self.parameter, self.policy_configuration, self.token, traffic_result)
        log_result = query.query_rule_log(traffic_generation, verification_result, rule_uuids_tuple, start_time)
        #if not log_result:
        #    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 'DEBUG:log_result:{};traffic_generation:{};verification_result：{}'.format(log_result, traffic_generation, verification_result), flush=True)
        return log_result
    
    def delete_objects(self, object_uuids_tuple):
        objects = DeleteObjects(self.parameter, self.headers)
        objects.delete_objects(object_uuids_tuple)
        
    def delete_libraries(self, library_uuids_tuple):
        libraries = DeleteLibraries(self.parameter, self.headers)
        libraries.delete_catalogs(library_uuids_tuple)
        libraries.delete_tags(library_uuids_tuple)
        
    def delete_profiles(self, profile_uuids_tuple):
        profiles = DeleteProfiles(self.parameter, self.headers)
        profiles.delete_profiles(profile_uuids_tuple)
    
    def delete_rules(self, rule_uuids_tuple):
        rules = DeleteRules(self.parameter, self.headers)
        rules.delete_rules(rule_uuids_tuple)
        
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    parameter = {
        "username": "zhaokun",
        "password": "zhaokun1",
        "test_pc_ip": "192.168.64.86",
        "test_subcriber_id": "test6776",
        "api_server": "http://192.168.44.72",
        "debug": "local",
        "initiation_method": "api",
        "env": "tsgx",
        "vsys": 5,
        "root_path": "",
        "path": "" + "/tests",
        "module_name": "security",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    api_client = APIClient(parameter)
    configuration_manager = {}
    """
    object_uuids = [
        {
            "attribute_name": "ATTR_SOURCE_IP",
            "name": "sec_srcip",
            "uuid": "111",
            "type": "ip"
        },
        {
            "attribute_name": "ATTR_SOURCE_IP",
            "name": "sec_srcip_2",
            "uuid": "222",
            "type": "ip"
        },
        {
            "attribute_name": "ATTR_SOURCE_IP",
            "name": "sec_srcip_3",
            "uuid": "333",
            "type": "ip"
        }
        {
            "attribute_name": "ATTR_SOURCE_PORT",
            "name": "sec_port",
            "uuid": "444",
            "type": "port"
        }
    ]
    """
    """
    rule_uuids = [
        {
            "attribute_name": "SECURITY_RULE",
            "name": "sec_deny",
            "uuid": "111",
            "type": "security"
        },
        {
            "attribute_name": "MONITOR_RULE",
            "name": "monit",
            "uuid": "222",
            "type": "monitor"
        }
    ]
    """
    policy_configuration = {
        "name": "automation_test_zk",
        "type": "security",
        "action": "deny",
        "and_conditions": [ # 一个rule选了两个source、一个destination、一个application
            {
                "negate_option": 0,
                "or_conditions": [ # 一个source ip address选了两个object
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip",
                        "items": [ # 一个object中包含多个item
                            {
                                "op": "add",
                                "ip": "1.1.1.1",
                                "interval": "0-65535"
                            },
                            {
                                "op": "add",
                                "ip": "2.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    },
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip_2",
                        "items": [
                            {
                                "op": "add",
                                "ip": "3.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_SOURCE_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip_3",
                        "items": [
                            {
                                "op": "add",
                                "ip": "4.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_DESTINATION_IP",
                        "type": "ip",
                        "sub_type": "ip",
                        "name": "sec_srcip_4",
                        "items": [
                            {
                                "op": "add",
                                "ip": "5.1.1.1",
                                "interval": "0-65535"
                            }
                        ]
                    }
                ]
            },
            {
                "negate_option": 0,
                "or_conditions": [
                    {
                        "attribute_name": "ATTR_APP_ID",
                        "type": "application",
                        "items": ["http", "ssl"]
                    }
                ],
            }
        ],
        "action_parameter": {
            "sub_action": "drop",
            "packet_capture": {
                "enable": 0
            },
            "send_tcp_reset": 1,
            "send_icmp_unreachable": 0,
            "after_n_packets": 1
        },
        "is_enabled": 1
    }
    object_uuids, _ = api_client.create_objects(policy_configuration)
    # configuration_manager["object_uuid_list"] = cmdb_collector.collect(object_uuids)
    rule_uuids, _ = api_client.create_rules(policy_configuration, object_uuids)
    # configuration_manager["rule_uuids_list"] = cmdb_collector.collect(rule_uuids)