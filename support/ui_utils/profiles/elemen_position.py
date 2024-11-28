# -*- coding: UTF-8 -*-
from support.ui_utils.element_position.map_element_position_library import get_element_position


class ElementPosition:
    def __init__(self, policy_configuration):
        self.policy_configuration = policy_configuration

    @property
    def get_profile_element_position_library(self):
        """
        从action_parameter中提取要定位的key_name，再从map_element_position_library到入定位信息
        """
        action_parameter = self.policy_configuration["action_parameter"]
        key_name = ""
        if "html_profile" in action_parameter:
            key_name = "response_page"
        elif "resolution" in action_parameter:
            # 需要处理
            key_name = "dns_resource_record"
        elif "traffic_mirroring" in action_parameter:
            key_name = "traffic_mirroring_profile"
        elif "keyring_for_trusted" in action_parameter:
            key_name = "ssl_decryption_keyring"
        elif "keyring_for_untrusted" in action_parameter:
            key_name = "ssl_decryption_keyring"
        elif "decryption_profile" in action_parameter:
            key_name = "ssl_decryption_profile"
        elif "tcp_option_profile" in action_parameter:
            key_name = "tcp_option_profile"
        elif "replacement_file" in action_parameter:
            key_name = "replacement_file"
        elif "js_file" in action_parameter:
            key_name = "js_file"
        elif "css_file" in action_parameter:
            key_name = "css_file"
        elif "lua_script" in action_parameter:
            key_name = "run_script"
        elif "profile_chain" in action_parameter:
            key_name = "shaping_profile"
        elif "sff_profiles" in action_parameter:
            # 需要处理
            key_name = "sff_profiles"
        elif "template_profile" in action_parameter:
            key_name = "statistics_template"
        else:
            return {}, key_name
        element_position_library = get_element_position(key_name)
        return element_position_library, key_name
