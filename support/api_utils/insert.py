import os

def insert(keyword, new_content):
    folder_path = 'D:/Document/Project-TSG/Code/git/tsg_test/tests/api/statistics'
    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            # 构造文件的完整路径
            file_path = os.path.join(folder_path, filename)
            # 提取文件名（不包括扩展名）和扩展名
            base_filename, file_extension = os.path.splitext(filename)
            # 临时文件用于存储修改后的内容 
            temp_file_path = 'D:/Document/Project-TSG/Code/git/tsg_test/tests/api/tt/' + base_filename + '.py'
            with open(file_path, 'r', encoding='utf-8') as file, open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                for line in file:
                    temp_file.write(line)
                    if keyword in line:
                        temp_file.write(new_content)
            # 替换原文件
            os.replace(temp_file_path, file_path)  
    
if __name__ == "__main__":
    keyword = "str(e)"
    new_content = """    finally:
        name_list = []
        erase = DeleteConfig()
        erase.clear_config(token, parameter, name_list)
    """
    insert(keyword, new_content)