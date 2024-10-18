import subprocess
import time
import os
import sys
import json
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import importlib
from contextlib import redirect_stdout
from support.packet_generator.workpath import workdir
from support.ui_utils.element_position.map_element_position_library import *
import re
time.sleep(1)


def local_run():
    """本地执行所有用例"""
    print("Get-Content result.txt -Encoding UTF8  -Wait")
    parameter = {
        "username": "zcw3",
        "password": "qa111111",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "ui",
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/testcase/ui",
        "module_name": "manipulation",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    cur_path = os.getcwd()
    print(os.getcwd())

    all_list = os.listdir()
    man_list = []    # 要执行的测试文件名称
    for i in all_list:
        if "man_" in i:
            i_1 = i[:-3]
            man_list.append(i_1)

    n = 1
    sum_all = len(man_list)
    # 打开文件准备写入
    with open("C:\\zcw\\tsg_test\\tests\\manipulation\\result.txt", "w", encoding="utf-8") as f:
        # 使用redirect_stdout将print的输出重定向到文件
        with redirect_stdout(f):
            for mani in man_list:
                print("执行第{}个用例，还剩{}个用例未执行".format(n, sum_all - n))
                mo = importlib.import_module(mani)
                parameter["test_case_name"] = mani
                rl = mo.run(parameter)
                n += 1
                # 手动刷新缓冲区，确保所有输出写入文件
                f.flush()

    print("Done writing to result.txt")

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

def get_excel_formate_from_case(case_directory_path='C:/zcw/tsg_test/tests/ui/manipulation', file_startwith = "man_", file_endswith = ".py"):
    # 使用excel统计测试用例，
    # 存储文件名（去掉.py后缀）
    file_names = []
    # 获取目录下所有文件的名称
    for filename in os.listdir(case_directory_path):
        if filename.endswith(file_endswith) and filename.startswith(file_startwith):
            # 去掉.py后缀并添加到列表中
            name_without_extension = filename[:-3]
            file_names.append(name_without_extension)
    a = [["aa", 1, 1, 0, 1],
         ["aa", 1, 1, 0, 1]]
    excel_list = []
    # 表头参数
    first_table_header = ['action', 'srcip', 'user', 'srcport', 'dstip', 'fqdn', 'dstport', 'intip', 'intport', 'extip', 'extport', 'app', 'url', 'reqheader', 'reqbody', 'resheader', 'resbody', 'logall', 'case']
    excel_list.append(first_table_header)
    for i in range(len(file_names)):
        raw = file_names[i]
        tmp_raw_list = []
        raw_dict = {
            "action_col" : 0,
            "srcip_col" : 0,
            "user_col" : 0,
            "srcport_col" : 0,
            "dstip_col" : 0,
            "fqdn_col" : 0,
            "dstport_col" : 0,
            "intip_col" : 0,
            "intport_col" : 0,
            "extip_col" : 0,
            "extport_col" : 0,
            "app_col" : 0,
            "url_col" : 0,
            "reqheader_col" : 0,
            "reqbody_col" : 0,
            "resheader_col" : 0,
            "resbody_col" : 0,
            "logall_col" : 0,
            "case_col" : 0
        }

        # 列统计
        if "allow" in raw:
            raw_dict["action_col"] = "allow"
        elif "deny" in raw:
            raw_dict["action_col"] = "deny"
        elif "monitor" in raw:
            raw_dict["action_col"] = "monitor"
        elif "redirect" in raw:
            raw_dict["action_col"] = "redirect"
        elif "replace" in raw:
            raw_dict["action_col"] = "replace"
        elif "hijack" in raw:
            raw_dict["action_col"] = "hijack"
        elif "insert" in raw:
            raw_dict["action_col"] = "insert"
        elif "edit_element" in raw:
            raw_dict["action_col"] = "edit_element"
        else:
            raw_dict["action_col"] = "run_script"
        # 列统计
        if "srcip" in raw:
            raw_dict["srcip_col"] = 1
        if "user" in raw:
            raw_dict["user_col"] = 1
        if "srcport" in raw:
            raw_dict["srcport_col"] = 1
        if "dstip" in raw:
            raw_dict["dstip_col"] = 1
        if "fqdn" in raw:
            raw_dict["fqdn_col"] = 1
        if "dstport" in raw:
            raw_dict["dstport_col"] = 1
        if "intip" in raw:
            raw_dict["intip_col"] = 1
        if "intport" in raw:
            raw_dict["intport_col"] = 1
        if "extip" in raw:
            raw_dict["extip_col"] = 1
        if "extport" in raw:
            raw_dict["extport_col"] = 1
        # application
        if "http" in raw:
            raw_dict["app_col"] = "http"
        else:
            raw_dict["app_col"] = "doh"
        if "url" in raw:
            raw_dict["url_col"] = 1
        if "reqheader" in raw:
            raw_dict["reqheader_col"] = 1
        if "reqbody" in raw:
            raw_dict["reqbody_col"] = 1
        if "resheader" in raw:
            raw_dict["resheader_col"] = 1
        if "resbody" in raw:
            raw_dict["resbody_col"] = 1
        if "logall" in raw:
            raw_dict["logall_col"] = 1
        raw_dict["case_col"] = raw

        # 组成一行数据
        for j in range(len(first_table_header)):
            col_name = "{}_col".format(first_table_header[j])
            tmp_raw_list.append(raw_dict[col_name])

        # 组成excel数据
        excel_list.append(copy.deepcopy(tmp_raw_list))
    #print(file_names)
    print(excel_list)
    # 将excel list数据写入text，包含有制表符
    # 写入文件
    file_path = "test_excel_info.txt"
    # 确定每一列的宽度
    # column_widths = [max(len(str(item)) for item in column) for column in zip(*excel_list)]
    # # 格式化字符串，每列保持对齐
    # with open(file_path, "w") as file:
    #     for row in excel_list:
    #         aligned_row = [f"{item:<{width}}" for item, width in zip(row, column_widths)]
    #         file.write("\t".join(aligned_row) + "\n")

    # 简单模式，没有对其显示
    with open(file_path, "w") as f:
        for row in excel_list:
            f.write("\t".join(map(str, row)) + "\n")

    test_excel_info_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
    print("完成。原数据保存路径：{}".format(test_excel_info_path))

def replace_test_data_from_py(case_directory_path='C:/zcw/tsg_test/tests/ui/目录名', file_startwith = "man_", file_endswith = ".py"):
    # 替换源文件中test_data内容
    #原始数据格式内容，替换其中的  “        replace_text”
    resource_text = \
"""# -*- coding: UTF-8 -*-
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import traceback
from datetime import datetime
from support.instance_utils.test_data_instance import TestDataInstance
from support.report_update import ReportUpdate


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)
        # 参数初始化
        exception_result = ""
        result = {}

        # 脚本启动时间
        start_time = time.time()

        # 测试数据
        replace_text

        # 测试用例实例化
        instantiation = InstanceTestData(test_data, parameter)
        result = instantiation.create()

        # 脚本结束时间和耗时
        end_time = time.time()
        duration = end_time - start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        return result
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Error: ", e, flush=True)
        traceback.print_exc()
        return "Error: " + str(e)
    finally:
        # 清理环境
        if isinstance(instantiation, InstanceTestData):
            instantiation.clean_up()
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)


if __name__ == '__main__':
    from support.ui_utils.element_position.map_element_position_library import replace_paras
    from support.ui_utils.workpath import workdir

    parameter = {
        "username": "zcw3",
        "password": "qa111111",
        "test_pc_ip": "192.168.64.93",
        "test_subcriber_id": "test6491",
        "api_server": "http://192.168.44.72",
        "debug_flag": "local",
        "script_type": "api",  # api  ui  空字符串
        "is_log": 1,
        "env": "tsgx",
        "vsys_id": 1,
        "root_path": workdir,
        "path": workdir + "/testcase/ui",
        "module_name": "manipulation",
        "test_case_name": os.path.basename(__file__)[:-3]
    }
    parameter = replace_paras(parameter)
    run(parameter)
    """
    #print(resource_text)

    file_names = []
    # 获取目录下所有文件的名称
    for filename in os.listdir(case_directory_path):
        if filename.endswith(file_endswith) and filename.startswith(file_startwith):
            # 去掉.py后缀并添加到列表中
            file_names.append(filename)

    for i in range(len(file_names)):
        file_0 = file_names[i]
        print(file_0)
        tmp_resource_text = copy.deepcopy(resource_text)
        with open(file_0, "r", encoding="utf-8") as f:
            text = f.read()

        # 正则表达式匹配从# 测试数据到log_in = LogIn()之间的内容
        pattern = re.compile(r'测试数据(.*?)log_in = LogIn\(\)', re.DOTALL)
        matches = re.findall(pattern, text)
        if len(matches) == 0:
            print("{}，替换失败".format(file_0))
            continue
        match_text = matches[0]
        match_text = match_text.rstrip()
        match_text = match_text.lstrip("\n")
        # 输出匹配的内容
        #print(match_text)
        result_text = tmp_resource_text.replace("        replace_text", match_text)

        # 覆盖源文件内容 谨慎执行
        with open(file_0, "w", encoding="utf-8") as f2:
            f2.write(result_text)
        # 覆盖源文件内容 谨慎执行

        print("{}，替换完成".format(file_0))
        #break
    print("替换完成")

if __name__ == '__main__':
    # 定义目录和目标文件  需要调整的变量
    ms_json_path = 'C:/Users/root/Downloads/Metersphere_Api_TSG (20).json'
    case_directory_path = 'C:/zcw/tsg_test/tests/ui/manipulation'
    file_startwith = "man_"
    file_endswith = ".py"

    # 本地运行所有用例
    local_run()

    # 对比MS工具
    #diff_ms(ms_json_path=ms_json_path, case_directory_path=case_directory_path, file_startwith=file_startwith, file_endswith=file_endswith)

    # 生成excle使用数据工具
    #get_excel_formate_from_case(case_directory_path=case_directory_path, file_startwith=file_startwith, file_endswith=file_endswith)

    # 替换test_data
    #replace_test_data_from_py(case_directory_path=case_directory_path, file_startwith=file_startwith, file_endswith=file_endswith)
