import subprocess
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import importlib
from contextlib import redirect_stdout
from support.traffic_manager.workpath import workdir
from support.ui_utils.element_position.map_element_position_library import *


time.sleep(1)



parameter = {
    "username": "zcw3",
    "password": "qa123456",
    "test_pc_ip": "192.168.64.93",
    "api_server": "http://192.168.44.72",
    "test_subcriber_id": "test68",
    "debug_flag": "local",
    "script_type": "api",
    "env": "tsgx",
    "vsys_id": 4,
    "is_log": 0,
    "root_path": "C:/zcw/tsg_test",
    "path": "C:/zcw/tsg_test/tests/api",
    "module_name": "statistics",
    "test_case_name": "",
}
parameter = replace_paras(parameter)
cur_path = os.getcwd()
print(os.getcwd())

all_list = os.listdir()
man_list = []    # 要执行的测试文件名称
for i in all_list:
    if "stats_" in i:
        i_1 = i[:-3]
        man_list.append(i_1)

n = 1
sum_all = len(man_list)
print(sum_all)
#print(man_list)
# 打开文件准备写入
with open("C:\\zcw\\tsg_test\\tests\\api\\statistics\\result.txt", "w", encoding="utf-8") as f:
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
            #break

print("Done writing to result.txt")


