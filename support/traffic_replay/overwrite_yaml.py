import os
import yaml

class OverwriteYaml():
    def __init__(self, path_dict):
        self.traffic_playback_workpath = path_dict["traffic_playback_workpath"]
        self.data_path = os.path.join(self.traffic_playback_workpath, "traffic_pcap")

    def replace_from_yaml(self, yaml_name, pcap_name, clients_start="10.50.36.1", clients_end="10.50.36.1", servers_start="10.50.66.1", servers_end="10.50.66.1"):
        # 组织yaml路径、pcap路径
        yaml_abs_path = os.path.join(self.data_path, yaml_name)
        pcap_abs_path = os.path.join(self.data_path, pcap_name)
        #print(yaml_abs_path, pcap_abs_path)
        with open(yaml_abs_path, "r", encoding="utf-8") as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        # 修改pcap文件路径
        result[0]["cap_info"][0]["name"] = pcap_abs_path
        result[0]["generator"]["clients_start"] = clients_start
        result[0]["generator"]["clients_end"] = clients_end
        result[0]["generator"]["servers_start"] = servers_start
        result[0]["generator"]["servers_end"] = servers_end
        # 修改后重写数据
        with open(yaml_abs_path, "w", encoding="utf-8") as f:
            yaml.dump(result, f)
        # print(result)