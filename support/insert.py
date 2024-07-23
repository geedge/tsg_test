import os
from datetime import datetime

def insert(keyword, new_content):
    folder_path = 'D:/Document/Project-TSG/Code/git/tsg_test/tests/api/intercept'
    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            # 构造文件的完整路径
            file_path = os.path.join(folder_path, filename)
            
            # ============在某关键字下一行添加内容=============
            # 提取文件名（不包括扩展名）和扩展名
            base_filename, file_extension = os.path.splitext(filename)
            # 临时文件用于存储修改后的内容 
            temp_file_path = 'D:/Document/Project-TSG/Code/git/tsg_test/tests/ui/temp/' + base_filename + '.py'
            with open(file_path, 'r', encoding='utf-8') as file, open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                for line in file:
                    temp_file.write(line)
                    if keyword in line:
                        temp_file.write(new_content)

            # 替换原文件
            os.replace(temp_file_path, file_path)
            # ============在某关键字下一行添加内容=============
            
            # ============在某关键字前一行添加内容=============
            # with open(file_path, 'r', encoding='utf-8') as file:
            #     lines = file.readlines()
            # # 查找关键字的索引
            # keyword_index = next((i for i, line in enumerate(lines) if keyword in line), None)
            # # 如果关键字不存在于文件中，直接返回（或可以选择抛出异常
            # if keyword_index is None:
            #     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Keyword '{keyword}' not found in file.")
            #     return
            # # 检查是否有足够的行在关键字前插入
            # if keyword_index >= 2:
            #     # 插入新字符串到指定位置
            #     lines.insert(keyword_index - 2 + 1, new_content + '\n')  # 添加换行符以保持格式
            # # 将修改后的内容写回到文件
            # with open(file_path, 'w', encoding='utf-8') as file: 
            #     file.writelines(lines)
            # ============在某关键字前一行添加内容=============
    
if __name__ == "__main__":
    # keyword = "delete.delete_policy_by_name"
    # new_content = """        # 生成csv报告
    #     file_path = parameter["root_path"] + "/report/{}_report.csv".format(parameter["script_type"])
    #     if os.path.exists(file_path) and os.path.isfile(file_path):  
    #         if result is not None and result != "" and len(result) != 0:
    #             report_data = []
    #             report_data.append(parameter["test_case_name"])
    #             if False in verification_result:
    #                 result_flag = "Fail"
    #             else:
    #                 result_flag = "Pass"
    #             report_data.append(result_flag)
    #             report_data.append(result)
    #             new_report = GenerateReport()
    #             new_report.insert_data(parameter, report_data)
    # """
    keyword = "except "
    new_content = """        exception_result = str(e)
"""
    # keyword = "report_data.append(result)"
    # new_content = """            elif exception_result is not None and exception_result != "" and len(exception_result) != 0:
    #             report_data = []
    #             report_data.append("test_case_name")
    #             result_flag = "Fail"
    #             report_data.append(result_flag)
    #             report_data.append(exception_result)
    #         elif result == "" and len(result) == 0 and exception_result == "" and len(exception_result) == 0:
    #             report_data = []
    #             report_data.append("test_case_name")
    #             result_flag = "Pass"
    #             report_data.append(result_flag)
    #             report_data.append("")
    #         new_report = GenerateReport()
    #         new_report.insert_data(parameter, report_data)"""
    # keyword = "def run"
    # new_content = "from datetime import datetime"""
    insert(keyword, new_content)