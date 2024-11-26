# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env
from support.ui_utils.create_objects_example import CreateObjectsExample
from support.ui_utils.delete_objects_example import DeleteObjectsExample
from support.ui_utils.edit_objects_example import EditObjectsExample
from support.ui_utils.object.create_objects_example import CreateObjects
from support.ui_utils.policy.create_rules import CreateRules
from support.ui_utils.policy.search_rules import SearchRules
from support.ui_utils.policy.edit_rules import EditRules
from support.ui_utils.policy.delete_rules import DeleteRules
from support.ui_utils.query_rule_metric import QueryRuleMetric
from support.ui_utils.query_rule_log import QueryRuleLog
from support.api_utils.log_in import LogIn
from support.api_utils.delete_objects import DeleteObjects as DeleteObjectsAPI
from support.api_utils.delete_rules import DeleteRules as DeleteRulesAPI
from support.ui_utils.object.search_objects_example import SearchObjects
from support.ui_utils.object.delete_objects_example import DeleteObjects
from support.ui_utils.object.edit_objects_example import EditObjects

class UIClient:
    def __init__(self, parameter):
        self.parameter = parameter
        support.ui_utils.env.initiate_selenium_request()
        self.driver = support.ui_utils.env.my_driver()
        support.ui_utils.env.setup()
    
    def create_objects(self, policy_configuration):
        objects = CreateObjects(self.driver)
        code = objects.create_objects(policy_configuration)
        return code

    def search_objects(self, name, policy_configuration, search_type):
        objects = SearchObjects(self.driver)
        objects_tuple, code = objects.get_object_uuid(name, policy_configuration)
        self.objects_tuple = objects_tuple
        return objects_tuple, code

    def edit_objects(self, objects_tuple, src_item,new_item):
        objects = EditObjects(self.driver)
        code = objects.edit(objects_tuple, src_item,new_item)
        return code
    
    def delete_objects(self, objects_tuple):
        objects = DeleteObjects(self.driver)
        objects.delete(self.parameter, objects_tuple)
    
    def create_rules(self, policy_configuration):
        self.policy_configuration = policy_configuration
        rules = CreateRules(self.driver)
        element_position, code = rules.create_rules(policy_configuration)
        self.element_position = element_position
        return code

    def search_rules(self, policy_configuration):
        rules = SearchRules(self.driver)
        rule_tuple, code = rules.search_rules(policy_configuration, self.element_position)
        self.rule_tuple = rule_tuple
        return rule_tuple, code

    def edit_rules(self, policy_configuration):
        rules = EditRules(self.driver)
        code = rules.edit_rules(policy_configuration, self.element_position)
        return code
    
    def delete_rules(self, rule_tuple):
        rules = DeleteRules(self.driver)
        rules.delete_rules(self.parameter, rule_tuple)

    def query_rule_metric(self, verification_result, traffic_result):
        query = QueryRuleMetric(self.policy_configuration, verification_result, self.driver, self.element_position, traffic_result)
        metric_result = query.query_rule_metric()
        return metric_result
    
    def query_rule_log(self, verification_result, rule_tuple, traffic_result):
        query = QueryRuleLog(self.policy_configuration, verification_result, rule_tuple, self.driver, self.element_position, traffic_result)
        log_result = query.query_rule_log()
        return log_result

    def cleanup(self):
        # 清理环境
        support.ui_utils.env.teardown()
        # 按uuid还是按name进行强制删除？？
        log_in = LogIn()
        pwd = log_in.encryptPwd(self.parameter["password"], self.parameter["api_server"])
        token = log_in.login(self.parameter["username"], pwd, self.parameter["api_server"])
        headers = {"Content-Type": "application/json", "Authorization": token}
        rules = DeleteRulesAPI(self.parameter, headers)
        rules.delete_rules(self.rule_tuple)
        objects = DeleteObjectsAPI(self.parameter, headers)
        objects.delete_objects(self.objects_tuple)
