import os  
  
def count_py_files_in_directory(directory):  
    count = 0  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            if file.endswith('.py'):  
                count += 1  
    return count  
  
# 示例  
directory_path = 'C:/automation_project/tsg_test/tests/service_chaining'  
py_file_count = count_py_files_in_directory(directory_path)  
print(f"Number of .py files: %d" % py_file_count)