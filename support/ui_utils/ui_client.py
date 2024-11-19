# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.ui_utils.create_security_rules_example import CreateSecurityRulesExample
from support.ui_utils.query_rule_metric import QueryRuleMetric
from support.ui_utils.query_rule_log import QueryRuleLog
from support.ui_utils.delete_security_rules_example import DeleteSecurityRulesExample
from support.ui_utils.create_objects_example import CreateObjectsExample


class UIClient:
    def __init__(self):
        support.ui_utils.env.initiate_selenium_request()
        self.driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()
    
    def create_rules(self, policy_configuration):
        self.policy_configuration = policy_configuration
        if "type" in policy_configuration.keys() and policy_configuration["type"] == "security":
            rules = CreateSecurityRulesExample()
            rule_uuids_tuple, element_position, result = rules.create_rules(policy_configuration, self.driver)
            self.element_position = element_position
        return rule_uuids_tuple, result

    def query_rule_metric(self, verification_result, traffic_result):
        query = QueryRuleMetric(self.policy_configuration, verification_result, self.driver, self.element_position, traffic_result)
        metric_result = query.query_rule_metric()
        return metric_result
    
    def query_rule_log(self, verification_result, rule_uuids_tuple, traffic_result):
        query = QueryRuleLog(self.policy_configuration, verification_result, rule_uuids_tuple, self.driver, self.element_position, traffic_result)
        log_result = query.query_rule_log()
        return log_result
    
    def delete_rules(self, parameter, policy_configuration):
        if "type" in policy_configuration.keys() and policy_configuration["type"] == "security":
            rules = DeleteSecurityRulesExample()
            rules.delete_rules(parameter, policy_configuration, self.driver)

    def create_objects(self,policy_configuration):
        self.policy_configuration = policy_configuration
        objects = CreateObjectsExample()
        objects_uuids_tuple, element_position, result = objects.create_objects(policy_configuration, self.driver)
        self.element_position = element_position
        return objects_uuids_tuple, result
