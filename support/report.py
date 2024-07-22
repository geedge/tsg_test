import os
import csv
import pandas as pd

class GenerateReport():
    def generate_report(self, script_type, root_path):
        report_folder_path = root_path + "/report"
        bool = self.is_file_in_directory(report_folder_path, "{}_report.csv".format(script_type))
        if bool == False:
            report_path = report_folder_path + "/{}_report.csv".format(script_type)
            title_data = []
            title_data.append(["Name", "Result", "Failure Reason"])
            df = pd.DataFrame(title_data, columns=["", "", ""])
            df.to_csv(report_path)
    
    def is_file_in_directory(self, directory, filename):  
        file_path = os.path.join(directory, filename)  
        return os.path.exists(file_path) and os.path.isfile(file_path) 
    
    def insert_data(self, parameter, report_data):
        report_path = parameter["root_path"] + "/report/{}_report.csv".format(parameter["script_type"])
        row_count = 0
        with open(report_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                row_count += 1
        new_report_data = [row_count-1, report_data[0], report_data[1], report_data[2]]
        table_data = []
        table_data.append(new_report_data)
        with open(report_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in table_data:
                writer.writerow(row)
        
if __name__ == '__main__':
    root_path = "D:/Document/Project-TSG/Code/git/tsg_test"
    report = GenerateReport()
    report.generate_report(root_path)
    i = 1
    while i <= 10:
        case_name = "shunt_ip_flag_app-allow_ip_flag_app_" + str(i)
        report_data = ["", "Pass", "The verification results of policy effect and logs are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs."]
        report_data[0] = case_name
        report.insert_data(report_data)
        i += 1