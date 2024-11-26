import time
from support.api_utils.log_in import *
from support.report_update import ReportUpdate
from support.ui_utils.ui_client import UIClient


def run(parameter):
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to run test case: " + parameter["test_case_name"], flush=True)

        # 参数初始化
        result, exception_result = "", ""

        # 脚本启动时间
        script_start_time = time.time()

        #测试数据
        object_configuration =  [
            {
                "name": "create_ip_object",
                "type": "ip",
                "sub_type": "ip",
                "member_type": "item",
                "statistics_option": "",  # random
                "items": [
                    {
                        "op": "add",
                        "ip": "1.1.1.1",
                        "interval": "0-65535"
                    },
                    {
                        "op": "add",
                        "ip": "192.168.2.1/24",
                        "interval": "0-65535"
                    }
                ]
            }
        ]

        ui_client = UIClient(parameter)
        
        # 创建
        code = ui_client.create_objects(object_configuration)
        if code != 200:
            return "Fail to create object."
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create Object successful ")

        search_type ={
            "is_fuzzy": False,
            "type": "",
        }
        # 查询
        objects_tuple, code = ui_client.search_objects("create_ip_object",object_configuration,search_type)
        objects_list = list(objects_tuple)
        if len(objects_list) == 0:
            return "Fail to get object uuid."
        if code != 200:
            return "Fail to search object."
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Search Object successful ")

        # 编辑
        # 如果src_item是空，则表示该item是新加
        code = ui_client.edit_objects(objects_tuple, src_item="", new_item="3.3.3.3")
        if code != 200:
            return "Fail to edit object."
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit Object successful ")
        # 如果src_item是不是空，在item输入框，输入src_item，找到item，点击item的编辑按钮，删除src_item，输入new_item，点击保存按钮
        code = ui_client.edit_objects(objects_tuple, src_item="1.1.1.1", new_item="2.2.2.2")
        if code != 200:
            return "Fail to edit object."
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Edit Object successful ")

        return ""
    except Exception as e:
        exception_result = str(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "When running test case, the exception error: ", str(e), flush=True)
        return "When running test case, the exception error: " + str(e)
    finally:
        # 删除
        if objects_tuple:
            ui_client.delete_objects(objects_tuple)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3],"Delete Object successful ")
        # ui_client.cleanup()
        # 统计脚本用时
        script_end_time = time.time()
        duration = script_end_time - script_start_time
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Duration of running the test case: ", "{:.3f}".format(duration), flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Finish test case: " + parameter["test_case_name"], flush=True)
        
        # 生成csv报告
        update = ReportUpdate()
        update.write_result(parameter, result, exception_result)

if __name__ == '__main__':
    parameter = {
        "username": "auto_ui_yzj",
        "password": "auto_ui_yzj",
        "test_pc_ip": "192.168.64.28",
        "test_subcriber_id": "",
        "api_server": "http://192.168.44.72",
        "initiation_method": "ui",
        "env": "tsgx",
        "vsys": 2,
        "is_log": 0,
        "root_path": "D:/PycharmProjects/tsg_test",
        "path": "D:/PycharmProjects/tsg_test/tests/ui",
        "module_name": "",
        "test_case_name": "create_table_traffic_spectrum"
    }
    run(parameter)
    """
    # 在测试文件的当前路径执行如下命令执行测试用例：
    pytest –cache-clear  -v  pytest_json.py --alluredir ./allure

    # 执行如下命令生成测试报告（自动打开浏览器）：
    allure serve allure
    """