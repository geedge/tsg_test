import os
import json

def diff_ms(ms_json_path='C:/Users/root/Downloads/Metersphere_Api_TSG (9).json', case_directory_path='C:/zcw/tsg_test/tests/ui/manipulation', file_startwith = "man_", file_endswith = ".py"):
    """
    比较MS和自动化脚本不同内容
    :param ms_json_path: MS导出的json文件路径
    :param case_directory_path:  对比用例case所在目录的路径
    :param file_startwith:  用例文件开始字符，例如 man_xxx_.py 选择 man_
    :param file_endswith:  用例文件结束字符，例如 man_xxx_.py  选择 .py
    """
    # 存储文件名（去掉.py后缀）
    file_names = []
    # 获取目录下所有文件的名称
    for filename in os.listdir(case_directory_path):
        if filename.endswith(file_endswith) and filename.startswith(file_startwith):
            # 去掉.py后缀并添加到列表中
            name_without_extension = filename[:-3]
            file_names.append(name_without_extension)

    # 读取MS json文件内容
    with open(ms_json_path, 'r', encoding="utf-8") as f:
        tmp_d = json.load(f)
    #print(tmp_d)

    ms_names = []   # MS case名称和请求体用例名称字段的列表  [{'ms_name': 'man_mon', 'test_case_name': 'man_mon'}]
    ms_case_names = []   # 只有MS case名称   ["man_mon"]
    # 从MS中读取到name
    for i in range(len(tmp_d["cases"])):
        ms_one_dict = {}
        #print(tmp_d["cases"][i]["name"])
        #print(tmp_d["cases"][i]["request"])
        request_dict = json.loads(tmp_d["cases"][i]["request"])
        body_dict = json.loads(request_dict["body"]["raw"])
        #print(request_dict)
        #print(body_dict)
        #print(body_dict["test_case_name"])
        ms_one_dict["ms_name"] = tmp_d["cases"][i]["name"]
        ms_one_dict["test_case_name"] = body_dict["test_case_name"]
        ms_names.append(ms_one_dict)
        ms_case_names.append(tmp_d["cases"][i]["name"])
        #print(ms_one_dict)

    # print(file_names)
    # print(ms_names)
    print("自动化脚本个数：{}".format(len(file_names)))
    print("MS统计脚本个数：{}".format(len(ms_names)))

    # 排查MS中ms_name、test_case_name名称不同选项
    diff_name = []
    for i in range(len(ms_names)):
        if ms_names[i]["ms_name"] != ms_names[i]["test_case_name"]:
            diff_name.append(ms_names[i])
    print("MS的用例名称和请求体中test_case_name不一致共有 {} 个：包括：{}".format(len(diff_name), diff_name))

    # 排查自动化脚本比MS多的用例
    print("检查自动化脚本和MS脚本不同用例：")
    file_names_set = set(file_names)
    ms_case_names_set = set(ms_case_names)
    only_in_file_names_set = file_names_set.difference(ms_case_names_set)
    only_in_ms_case_names_set = ms_case_names_set.difference(file_names_set)
    print("自动化脚本比MS多 {} 个用例：包括：{}".format(len(only_in_file_names_set), list(only_in_file_names_set)))
    print("MS比自动化脚本多 {} 个用例：包括：{}".format(len(only_in_ms_case_names_set), list(only_in_ms_case_names_set)))

if __name__ == '__main__':
    # 定义目录和目标文件  需要调整的变量
    ms_json_path = 'C:/Users/root/Downloads/Metersphere_Api_TSG (9).json'
    case_directory_path = 'C:/zcw/tsg_test/tests/ui/manipulation'
    file_startwith = "man_"
    file_endswith = ".py"
    diff_ms(ms_json_path=ms_json_path, case_directory_path=case_directory_path, file_startwith=file_startwith, file_endswith=file_endswith)