import random
from datetime import datetime 
class GenerateRandomIP:
    def __init__(self,driver):
        self.driver = driver

    # 将ip改为随机
    def generate_random_ip(self, data, run_env):
        for condition_key in data["condition"].keys():
            if condition_key == "source_ip" or condition_key == "destination_ip":
                for obj in data["condition"][condition_key]:
                    src_ip = obj["item"][0]["item_value"]
                    if "default" in src_ip:
                        src_ip = "192.168.64.91"
                    if "-" not in src_ip and "/" not in src_ip:
                        src_ip_list = src_ip.split(".")
                        src_ip_list[2] = str(random.randint(0, 255))
                        src_ip_list[3] = str(random.randint(0, 255))
                        if run_env == "9140":
                            src_ip_list[0] = "172"
                            src_ip_list[1] = "56"
                        elif run_env == "tsgx":
                            src_ip_list[0] = "10"
                            src_ip_list[1] = "64"
                        new_src_ip = ".".join(src_ip_list)
                        obj["item"][0]["item_value"] = new_src_ip
                    elif "-" in src_ip and "/" not in src_ip:
                        two_ip_list = src_ip.split("-")
                        ip_list_1 = two_ip_list[0].split(".")
                        ip_list_2 = two_ip_list[1].split(".")
                        ip_list_1[2] = str(random.randint(0, 255))
                        ip_list_1[3] = str(random.randint(0, 55))
                        ip_list_2[2] = ip_list_1[2]
                        ip_list_2[3] = str(int(ip_list_1[3]) + 200)
                        new_ip_1 = ".".join(ip_list_1)
                        new_ip_2 = ".".join(ip_list_2)
                        if run_env == "9140":
                            ip_list_1[0] = "172"
                            ip_list_1[1] = "56"
                            ip_list_2[0] = "172"
                            ip_list_2[1] = "56"
                        elif run_env == "tsgx":
                            ip_list_1[0] = "10"
                            ip_list_1[1] = "64"
                            ip_list_2[0] = "10"
                            ip_list_2[1] = "64"
                        new_two_ip_list = []
                        new_two_ip_list.append(new_ip_1)
                        new_two_ip_list.append(new_ip_2)
                        new_two_ip = "-".join(new_two_ip_list)
                        obj["item"][0]["item_value"] = new_two_ip
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Setrandom ip for statistics or sc rule.", flush=True)
        return data