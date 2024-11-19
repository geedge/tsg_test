# -*- coding: UTF-8 -*-
import json
import requests
from datetime import datetime

class CreateProfiles:
    def __init__(self, parameter, headers):
        self.parameter = parameter
        self.headers = headers
    
    def create_profiles(self, policy_configuration):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        root_path = self.parameter["root_path"]
        profile_type = ""
        profile_uuids_list = []
        try:
            if "template_profile" in policy_configuration["action_parameter"].keys():
                #http://192.168.44.72/v1/profiles/statistics-templates
                profile_type = "statistics-templates"
                if "vsys" in policy_configuration["action_parameter"]["template_profile"].keys():
                    policy_configuration["action_parameter"]["template_profile"]["vsys"] = vsys
                template_uuids, template_temp = self.create_text_profile(policy_configuration["action_parameter"]["template_profile"], profile_type)
                profile_uuids_list.append(template_uuids)
                #profile_template = root_path + "/support/api_utils/template/profile_statistics_template.json"
            elif "sff_profiles" in policy_configuration["action_parameter"].keys():
                sff_profile_list = []
                for sff_profile in policy_configuration["action_parameter"]["sff_profiles"]:
                    sf_profile_list = []
                    if "vsys" in sff_profile.keys():
                        sff_profile["vsys"] = vsys
                    for sf_profile in sff_profile["service_func_profiles"]:
                        if "vsys" in sf_profile.keys():
                            sf_profile["vsys"] = vsys
                        profile_type = "service-functions"
                        sf_uuids, sf_temp = self.create_text_profile(sf_profile, profile_type)
                        sf_profile_list.append(sf_uuids)
                    sff_profile["service_func_profiles"] = sf_profile_list
                    profile_type = "service-function-forwarders"
                    sff_uuids, sf_temp = self.create_text_profile(sff_profile, profile_type)
                    profile_uuids_list.append(sff_uuids)
            elif "profile_chain" in policy_configuration["action_parameter"].keys():
                profile_type = "traffic-shaping-profiles"
            elif "html_profile" in policy_configuration["action_parameter"].keys():
                profile_type = "response-pages"
                #"html_profile": {
                #    "name": "test",
                #    "format": "html",
                #    "content_name": "Response-Pages_1.html"
                #}
                response_uuids, sf_temp = self.create_file_upload_profile(policy_configuration["action_parameter"]["html_profile"], profile_type, policy_configuration["action_parameter"]["html_profile"]["content_name"])
                profile_uuids_list.append(response_uuids)
            elif "record_profile"  in policy_configuration["action_parameter"].keys():
                print("to do ...")
            elif "traffic_mirroring" in policy_configuration["action_parameter"].keys():
                profile_type = "traffic-mirroring-profiles"
                mirroring_uuids, template_temp = self.create_text_profile(policy_configuration["action_parameter"]["traffic_mirroring"]["mirroring_profile"], profile_type)
                profile_uuids_list.append(mirroring_uuids)
            elif "tcp_option_profile"  in policy_configuration["action_parameter"].keys():
                profile_type = "response-pages"
                print("to do ...")
            elif "keyring_for_trusted"  in policy_configuration["action_parameter"].keys():
                profile_type = "response-pages"
                print("to do ...")
            elif "keyring_for_untrusted"  in policy_configuration["action_parameter"].keys():
                profile_type = "response-pages"
                print("to do ...")
            elif "decryption_profile" in policy_configuration["action_parameter"].keys():
                profile_type = "response-pages"
                print("to do ...")
            elif "replacement_file" in policy_configuration["action_parameter"].keys():
                profile_type = "replacement_file"
                response_uuids, sf_temp = self.create_file_upload_profile(
                    policy_configuration["action_parameter"]["proxy_replacement_file"], profile_type,
                    policy_configuration["action_parameter"]["html_profile"]["content_name"])
                profile_uuids_list.append(response_uuids)
            elif "js_file" in policy_configuration["action_parameter"].keys() :
                profile_type = "response-pages"
                print("to do ...")
            elif "css_file" in policy_configuration["action_parameter"].keys():
                profile_type = "response-pages"
                print("to do ...")
            elif "lua_script" in policy_configuration["action_parameter"].keys():
                profile_type = "response-pages"
                print("to do ...")

            profile_uuids_tuple = tuple(profile_uuids_list)
            return profile_uuids_tuple, ""
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When creating profile, the exception error: ", str(e), flush=True)
            return "" ,"When creating profile, the exception error: " + str(e)

    def create_text_profile(self, post_data, profile_type):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        root_path = self.parameter["root_path"]
        post_common_data = {"vsys":vsys,"return_data":1}
        match profile_type:
            case "statistics-templates":
                post_common_data = {"vsys": vsys, "return_data": 1, "statistics_template": post_data}
            case "service-functions":
                post_common_data = {"vsys": vsys, "return_data": 1, "service_function": post_data}
            case "service-function-forwarders":
                post_common_data = {"vsys": vsys, "return_data": 1, "service_function_forwarder": post_data}
            case "traffic-mirroring-profiles":
                post_common_data = {"vsys": vsys, "return_data": 1, "traffic_mirroring_profile": post_data}
            case _:
                return "", "When creating {} profile, the exception error: ".format(profile_type)
        try:
            profile_uuids_list = []
            url = "{}/v1/profiles/{}".format(api_server, profile_type)
            response = requests.post(url, headers=self.headers, json=post_common_data, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Create {} profile successfully.".format(profile_type), flush=True)
                response_dict = json.loads(response.text)
                profile_uuids, object_geo_uuid = self.get_uuids(response_dict, profile_type)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Create {} profile failed.".format(profile_type), flush=True)
                return "", "Create {} profile failed.".format(profile_type)
            return profile_uuids, object_geo_uuid
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                  "When creating {} profile, the exception error: ".format(profile_type), str(e), flush=True)
            return "", "When creating {} profile, the exception error: ".format(profile_type) + str(e)
    def create_file_upload_profile(self, post_data, profile_type,file_name):
        api_server = self.parameter["api_server"]
        vsys = self.parameter["vsys"]
        root_path = self.parameter["root_path"].replace("\\","/")
        post_common_data = {"vsys":vsys,"return_data":1}
        headers = {"Authorization": self.headers["Authorization"]}
        match profile_type:
            case "response-pages":
                post_data["vsys"] = post_common_data["vsys"]
                post_data["return_data"] = post_common_data["return_data"]
            case _:
                return "", "When creating {} profile, the exception error: ".format(profile_type)
        try:
            files = {"file": (file_name,open(root_path + "/support/api_utils/preset_profile/"+file_name, 'rb'), "text/plain")}
            url = "{}/v1/profiles/{}".format(api_server, profile_type)
            #response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
            response = requests.post(url=url, data=post_data, headers=headers, files=files, verify=False)
            if response.status_code == 200:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Create {} profile successfully.".format(profile_type), flush=True)
                response_dict = json.loads(response.text)
                profile_uuids, object_geo_uuid = self.get_uuids(response_dict, profile_type)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                      "Create {} profile failed.".format(profile_type), flush=True)
                return "", "Create {} profile failed.".format(profile_type)
            return profile_uuids, object_geo_uuid
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],
                  "When creating {} profile, the exception error: ".format(profile_type), str(e), flush=True)
            return "", "When creating {} profile, the exception error: ".format(profile_type) + str(e)
    def get_uuids(self, response_dict, type):
        match type:
            case "statistics-templates":
                uuid = response_dict["data"]["statistics_template"]["uuid"]
            case "service-functions":
                uuid = response_dict["data"]["service_function"]["uuid"]
            case "service-function-forwarders":
                uuid = response_dict["data"]["service_function_forwarder"]["uuid"]
            case "response-pages":
                uuid = response_dict["data"]["response_page"]["uuid"]
            case "traffic-mirroring-profiles":
                uuid = response_dict["data"]["traffic_mirroring_profile"]["uuid"]
            case "replacement_file":
                uuid = response_dict["data"]["proxy_replacement_file"]["uuid"]
            case _:
                uuid = ""
        return uuid, ""