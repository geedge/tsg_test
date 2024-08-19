import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import copy
import requests
import support.api_utils.get_application_id as get_application_id
from datetime import datetime 

class PolicyVerify:
    def policy_verify(self, condition, verify_attribute_dict, token, host_api, vsys_id):
        """
        :param condition:
        :param verify_attribute_dict:    {key:value}形式的验证条件，只支持ip
        :param token:
        :param host_api:
        :param vsys_id:
        :return:
        """
        # 简单策略验证策略是否生效，验证ip+http
        verify_list_dict = {'verify_list': [{'type': 'statistics', 'vsys_id': 6, 'verify_session': {'attributes': []}}], 'vsys_id': 6}    # 重组请求体使用基本数据格式
        url = "{}/v1/policy/trouble_shooting/verify_policy".format(host_api)
        headers = {"Content-Type": "application/json", "Authorization": token}
        verify_src_ip = {'attribute_type': 'ip', 'attribute_name': 'source', 'attribute_value': {'ip': '10.64.244.236', 'port': 1000, 'table_name': '', 'addrType': 4, 'protocol': '6'}}
        verify_dst_ip = {'attribute_type': 'ip', 'attribute_name': 'destination', 'attribute_value': {'ip': '10.64.218.174', 'port': 80, 'table_name': '', 'addrType': 4, 'protocol': '6'}}
        verify_app = {'attribute_type': 'numeric', 'attribute_name': 'app_id', 'attribute_value': {'numeric': 67}}
        verify_fqdn_dict = {'attribute_type': 'string', 'attribute_name': 'server_fqdn', 'attribute_value': {'string': 'www.ct.cn', 'table_name': 'ATTR_SERVER_FQDN', 'protocol': '6'}}
        verify_http_req_hdr_dict = {'attribute_type': 'signature', 'attribute_name': 'req_hdr', 'appId': 67, 'appName': 'http', 'attribute_value': {'district': 'test'}}
        verify_http_res_hdr_dict = {'attribute_type': 'signature', 'attribute_name': 'res_hdr', 'appId': 67, 'appName': 'http', 'attribute_value': {'district': 'test'}}
        verify_obj_comm_dict = {'attribute_type': 'string', 'attribute_name': 'responder', 'appId': 182, 'appName': 'sip', 'attribute_value': {'string': 'test'}}
        # filter_attribute_name_dict 中的key都是使用上面的 verify_obj_comm_dict
        filter_attribute_name_dict = {
            "ATTR_HTTP_URL": "url", "ATTR_HTTP_REQ_BODY": "req_body", "ATTR_HTTP_RES_BODY": "res_body", "ATTR_SSL_SAN": "san", "ATTR_SSL_CN": "cn",
            "ATTR_DNS_QNAME": "qname", "ATTR_FTP_URI": "url", "ATTR_FTP_ACCOUNT": "account", "ATTR_FTP_CONTENT": "content", "ATTR_MAIL_SUBJECT": "subject",
            "ATTR_MAIL_CONTENT": "account", "ATTR_MAIL_ATT_NAME": "att_name", "ATTR_MAIL_ATT_CONTENT": "att_content", "ATTR_MAIL_FROM": "from", "ATTR_MAIL_TO": "to",
            "ATTR_MAIL_ACCOUNT": "att_name", "ATTR_SIP_ORIGINATOR_DESCRIPTION": "originator", "ATTR_SIP_RESPONDER_DESCRIPTION": "responder"
        }
        appId = 67
        appName = "http"
        # 重组type
        verify_list_dict["verify_list"][0]["type"] = condition["policy_type"]
        # 重组 vsys_id
        verify_list_dict["verify_list"][0]["vsys_id"] = vsys_id
        verify_list_dict["vsys_id"] = vsys_id
        # 重组 src ip
        if "src_ip" in verify_attribute_dict.keys():
            #verify_list_dict["verify_list"][0]["verify_session"]["attributes"][0]["attribute_value"]["ip"] = verify_attribute_dict["src_ip"]
            verify_src_ip["attribute_value"]["ip"] = verify_attribute_dict["src_ip"]
            verify_list_dict["verify_list"][0]["verify_session"]["attributes"].append(verify_src_ip)
        # 重组 dst_ip
        if "dst_ip" in verify_attribute_dict.keys():
            #verify_list_dict["verify_list"][0]["verify_session"]["attributes"][1]["attribute_value"]["ip"] = verify_attribute_dict["dst_ip"]
            verify_dst_ip["attribute_value"]["ip"] = verify_attribute_dict["dst_ip"]
            verify_list_dict["verify_list"][0]["verify_session"]["attributes"].append(verify_dst_ip)
        # 重组查询 application
        if condition["application_1"] != []:
            app_list = get_application_id.get_app_id(str(condition["application_1"]), host_api)
            verify_app["attribute_value"]["numeric"] = app_list[0]
            appId = app_list[0]
            appName = str(condition["application_1"][0])
        verify_list_dict["verify_list"][0]["verify_session"]["attributes"].append(verify_app)
        # 重组 filter
        for obj_cond in condition["obj_condition_1"]:    # 遍历添加filter条件
            attribute_name = obj_cond["attribute_name"]
            if attribute_name == "ATTR_SERVER_FQDN":     # fqdn
                verify_fqdn_dict_0 = copy.deepcopy(verify_fqdn_dict)
                verify_fqdn_dict_0["attribute_value"]["string"] = obj_cond["object_list"][0]["add_item_list"][0]["keyword_array"][0]
                verify_list_dict["verify_list"][0]["verify_session"]["attributes"].append(verify_fqdn_dict_0)
            elif attribute_name == "ATTR_HTTP_REQ_HDR":     # url
                verify_http_req_hdr_dict_0 = copy.deepcopy(verify_http_req_hdr_dict)
                verify_http_req_hdr_dict_0["attribute_value"]["string"] = obj_cond["object_list"][0]["add_item_list"][0]["keyword_array"][0]
                verify_http_req_hdr_dict_0["appId"] = appId
                verify_http_req_hdr_dict_0["appName"] = appName
                verify_list_dict["verify_list"][0]["verify_session"]["attributes"].append(verify_http_req_hdr_dict_0)
            elif attribute_name == "ATTR_HTTP_RES_HDR":  # url
                verify_http_res_hdr_dict_0 = copy.deepcopy(verify_http_res_hdr_dict)
                verify_http_res_hdr_dict_0["attribute_value"]["string"] = obj_cond["object_list"][0]["add_item_list"][0]["keyword_array"][0]
                verify_http_res_hdr_dict_0["appId"] = appId
                verify_http_res_hdr_dict_0["appName"] = appName
                verify_list_dict["verify_list"][0]["verify_session"]["attributes"].append(verify_http_res_hdr_dict_0)
            elif attribute_name in filter_attribute_name_dict.keys():     #通用的构造
                verify_obj_comm_dict_0 = copy.deepcopy(verify_obj_comm_dict)
                verify_obj_comm_dict_0["attribute_value"]["string"] = obj_cond["object_list"][0]["add_item_list"][0]["keyword_array"][0]
                verify_obj_comm_dict_0["attribute_name"] = filter_attribute_name_dict[attribute_name]
                verify_obj_comm_dict_0["appId"] = appId
                verify_obj_comm_dict_0["appName"] = appName
                verify_list_dict["verify_list"][0]["verify_session"]["attributes"].append(verify_obj_comm_dict_0)
        response = requests.post(url, json=verify_list_dict, headers=headers, verify=False)
        r_dict = response.json()
        hit_policy_list = []
        if "hit_policy_list" in r_dict["data"].keys():
            for policy_id in r_dict["data"]["hit_policy_list"]:
                hit_policy_list.append(policy_id["id"])
        return hit_policy_list
        
if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")