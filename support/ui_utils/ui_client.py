# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.ui_utils.objects.create_objects_example import CreateObjects
from support.ui_utils.policies.create_rules import CreateRules
from support.ui_utils.policies.search_rules import SearchRules
from support.ui_utils.policies.edit_rules import EditRules
from support.ui_utils.policies.delete_rules import DeleteRules
from support.ui_utils.query_rule_metric import QueryRuleMetric
from support.ui_utils.query_rule_log import QueryRuleLog
from support.api_utils.log_in import LogIn
from support.ui_utils.objects.search_objects_example import SearchObjects
from support.ui_utils.objects.delete_objects_example import DeleteObjects
from support.ui_utils.objects.edit_objects_example import EditObjects
from support.ui_utils.profiles.create_profiles import CreateProfiles
from support.ui_utils.profiles.search_profiles import SearchProfiles
from support.ui_utils.profiles.edit_profiles import EditProfiles
from support.ui_utils.profiles.delete_profiles import DeleteProfiles

class UIClient:
    def __init__(self, parameter):
        self.parameter = parameter
        support.ui_utils.env.initiate_selenium_request()
        self.driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()
    
    def create_objects(self, policy_configuration):
        objects = CreateObjects(self.driver)
        error = objects.create_objects(policy_configuration)
        return error

    def search_objects(self, name, policy_configuration, search_type):
        objects = SearchObjects(self.driver)
        error = objects.search_objects(name, policy_configuration)
        return error
    
    def get_objects_uuid(self, policy_configuration):
        objects = SearchObjects(self.driver)
        objects_tuple, error = objects.get_objects_uuid(policy_configuration)
        # self.objects_tuple = objects_tuple
        return objects_tuple, error

    def edit_objects(self, objects_tuple, src_item,new_item):
        objects = EditObjects(self.driver)
        error = objects.edit_objects(objects_tuple, src_item,new_item)
        return error
    
    def delete_objects(self, objects_tuple):
        objects = DeleteObjects(self.driver)
        objects.delete_objects(self.parameter, objects_tuple)

    def create_profiles(self, policy_configuration):
        profiles = CreateProfiles(self.driver)
        error = profiles.create_profiles(policy_configuration)
        return error

    def search_profiles(self, policy_configuration, search_type):
        profiles = SearchProfiles(self.driver)
        error = profiles.search_profiles(policy_configuration)
        return error
    
    def get_profiles_uuid(self, policy_configuration):
        profiles = SearchProfiles(self.driver)
        profiles_tuple, error = profiles.get_profiles_uuid(policy_configuration)
        # self.profiles_tuple = profiles_tuple
        return profiles_tuple, error

    def create_rules(self, policy_configuration):
        self.policy_configuration = policy_configuration
        rules = CreateRules(self.driver)
        error = rules.create_rules(policy_configuration)
        return error

    def search_rules(self, policy_configuration, search_type):
        rules = SearchRules(self.driver)
        error = rules.search_rules(policy_configuration)
        return error
    
    def get_rules_uuid(self, policy_configuration):
        rules = SearchRules(self.driver)
        rules_tuple, error = rules.get_rules_uuid(policy_configuration)
        # self.rules_tuple = rules_tuple
        return rules_tuple, error

    def edit_rules(self, policy_configuration):
        rules = EditRules(self.driver)
        error = rules.edit_rules(policy_configuration)
        return error
    
    def delete_rules(self, rules_tuple):
        rules = DeleteRules(self.driver)
        rules.delete_rules(rules_tuple)

    def query_rule_metric(self, verification_result, traffic_result):
        query = QueryRuleMetric(self.policy_configuration, verification_result, self.driver, traffic_result)
        metric_result = query.query_rule_metric()
        return metric_result
    
    def query_rule_log(self, verification_result, rules_tuple, traffic_result):
        query = QueryRuleLog(self.policy_configuration, verification_result, rules_tuple, self.driver, traffic_result)
        log_result = query.query_rule_log()
        return log_result

    def cleanup(self, policy_configuration):
        # 清理环境
        support.ui_utils.env.teardown()
        # 按name进行强制删除
        log_in = LogIn()
        pwd = log_in.encryptPwd(self.parameter["password"], self.parameter["api_server"])
        token = log_in.login(self.parameter["username"], pwd, self.parameter["api_server"])
        headers = {"Content-Type": "application/json", "Authorization": token}
        rules = DeleteRules(self.driver)
        rules.delete_rules_by_name(self.parameter, policy_configuration, headers)
        objects = DeleteObjects(self.driver)
        objects.delete_objects_by_name(self.parameter, policy_configuration, headers)
